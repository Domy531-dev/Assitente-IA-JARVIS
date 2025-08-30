import speech_recognition as sr
import pyttsx3
import json

# Carregar config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Inicializar motor de voz
engine = pyttsx3.init()
engine.setProperty("rate", config.get("voz_velocidade", 180))
engine.setProperty("volume", config.get("voz_volume", 1.0))

def falar(texto: str):
    """Transforma texto em fala"""
    print("🔊 Falando...")
    engine.say(texto)
    engine.runAndWait()

def ouvir() -> str:
    """Captura voz do microfone e retorna texto"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Ouvindo...")
        audio = r.listen(source)

        try:
            texto = r.recognize_google(audio, language=config.get("idioma", "pt-BR"))
            print(f"Você disse: {texto}")
            return texto
        except sr.UnknownValueError:
            print("⚠️ Não entendi o que você disse.")
            return ""
        except sr.RequestError:
            print("❌ Erro no serviço de reconhecimento de voz.")
            return ""
