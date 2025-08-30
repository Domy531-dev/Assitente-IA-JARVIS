import openai
import json

# Carregar config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

openai.api_key = config["openai_api_key"]

def conversar(mensagem: str) -> str:
    """Envia mensagem para o modelo GPT"""
    try:
        resposta = openai.ChatCompletion.create(
            model=config.get("modelo", "gpt-4o-mini"),
            messages=[{"role": "user", "content": mensagem}]
        )
        return resposta.choices[0].message["content"]
    except Exception as e:
        return f"❌ Erro ao conectar com a IA: {e}"
