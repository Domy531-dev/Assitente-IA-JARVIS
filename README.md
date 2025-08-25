# Assistente IA (Texto + Voz) com Flask, Gemini, Whisper e gTTS

Interaja por **texto ou voz**. A aplicação:
- Transcreve áudio (Whisper - open source)
- Gera respostas com Gemini (Google)
- Converte a resposta em áudio (gTTS, PT-BR)
- Interface web simples com captura de microfone

## Requisitos

- Python 3.10+
- **FFmpeg** instalado e disponível no PATH (necessário para Whisper e pydub)
- Chave da **Gemini API** (GEMINI_API_KEY)
- Navegador com suporte a `MediaRecorder` (Chrome/Edge/Firefox)

## Instalação

```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Copie e edite o .env
cp .env.example .env  # ou manualmente crie .env
```

Edite o `.env` e preencha `GEMINI_API_KEY`.

## Executando

```bash
python app.py
# Abra http://localhost:5000
```

## Dicas

- Se sua máquina for fraca, defina `WHISPER_MODEL=tiny` no `.env` para transcrição mais leve.
- Quer resposta mais rápida? Troque o modelo do Gemini para `gemini-1.5-flash` (já configurado).
- Para português-BR mais natural no TTS, você pode integrar serviços como Azure TTS ou Google Cloud TTS — basta substituir a função `synthesize_tts_ptbr`.

## WhatsApp (opcional)

Se quiser usar no WhatsApp, você precisará de um gateway (Cloud API do Meta ou um provedor). Configure o webhook para apontar para rotas que façam:
1) baixar o áudio recebido,
2) enviar para `/api/voice`,
3) devolver o `audio_url` como mensagem de áudio e o `reply` como texto.

Este repositório foca em UI web local para simplificar.

---

Feito para você começar rápido. Qualquer ajuste, me chame!
