from ia import conversar
from voz import ouvir, falar
import json

# Carregar configurações
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

def main():
    print("🤖 Jarvis 1.5 Flash iniciado!")
    print("Digite 'voz' para falar ou 'texto' para digitar. (sair para encerrar)\n")

    while True:
        escolha = input("Modo [voz/texto]: ").lower().strip()

        if escolha == "voz":
            mensagem = ouvir()
        elif escolha == "texto":
            mensagem = input("Você: ")
        else:
            print("❌ Opção inválida.")
            continue

        if not mensagem:
            continue

        if mensagem.lower() in ["sair", "exit", "fechar"]:
            print("👋 Encerrando Jarvis...")
            break

        resposta = conversar(mensagem)
        print(f"Jarvis: {resposta}\n")
        falar(resposta)


if __name__ == "__main__":
    main()
