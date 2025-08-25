import os
import uuid
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask, request, jsonify, send_from_directory, render_template
from gtts import gTTS
import google.generativeai as genai
import whisper
from pydub import AudioSegment

# ---------- Setup ----------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Defina a variável de ambiente GEMINI_API_KEY no seu .env")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Load Whisper once (base model for balance speed/quality; you can try 'small' or 'tiny' for weaker hardware)
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL", "base")
whisper_model = whisper.load_model(WHISPER_MODEL_NAME)

app = Flask(__name__)

# Ensure folders
RESPONSES_DIR = Path(app.root_path) / "static" / "responses"
RESPONSES_DIR.mkdir(parents=True, exist_ok=True)

# ---------- Helpers ----------

def synthesize_tts_ptbr(text: str) -> str:
    """Generate an MP3 from text using gTTS and return the relative file path."""
    uid = str(uuid.uuid4())
    out_path = RESPONSES_DIR / f"reply_{uid}.mp3"
    tts = gTTS(text=text, lang="pt", slow=False)
    tts.save(str(out_path))
    # Return URL path
    return f"/static/responses/{out_path.name}"

def run_gemini(prompt: str) -> str:
    resp = model.generate_content(prompt)
    if hasattr(resp, 'text'):
        return resp.text.strip()
    # Fallback parsing
    return str(resp).strip()

def transcribe_audio_to_text(file_storage) -> str:
    """Accept an uploaded audio file and return transcribed text using Whisper.
    Requires FFmpeg installed on the system (ffmpeg in PATH).
    """
    # Convert any incoming format to WAV (16k) for best compatibility
    # First, read into memory then via pydub
    raw = file_storage.read()
    audio = AudioSegment.from_file(BytesIO(raw))
    audio = audio.set_frame_rate(16000).set_channels(1)
    tmp_wav = RESPONSES_DIR / f"input_{uuid.uuid4()}.wav"
    audio.export(tmp_wav, format="wav")
    # Whisper expects a file path
    result = whisper_model.transcribe(str(tmp_wav), fp16=False, language="pt" )
    try:
        os.remove(tmp_wav)
    except Exception:
        pass
    return result.get("text", "").strip()

# ---------- Routes ----------

@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/text")
def api_text():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Mensagem vazia."}), 400

    reply = run_gemini(message)
    audio_url = synthesize_tts_ptbr(reply)

    return jsonify({
        "input": message,
        "reply": reply,
        "audio_url": audio_url
    })


@app.post("/api/voice")
def api_voice():
    if "audio" not in request.files:
        return jsonify({"error": "Envie um arquivo 'audio' no formulário."}), 400
    audio_file = request.files["audio"]
    try:
        text = transcribe_audio_to_text(audio_file)
    except Exception as e:
        return jsonify({"error": f"Falha ao transcrever áudio: {e}"}), 500

    if not text:
        return jsonify({"error": "Não foi possível extrair texto do áudio."}), 400

    reply = run_gemini(text)
    audio_url = synthesize_tts_ptbr(reply)

    return jsonify({
        "transcript": text,
        "reply": reply,
        "audio_url": audio_url
    })


if __name__ == "__main__":
    # For local dev only; use a production server (gunicorn/uvicorn) for deployment
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
