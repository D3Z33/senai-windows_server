import os
import win32file
import win32con
import requests

# Configuração do Telegram
TELEGRAM_TOKEN = "7692442307:AAHFgnUWu9hkFkAzRGk8rHw7M_YnqDfBGJ8"
TELEGRAM_CHAT_ID = "511867448"

# Lista de arquivos .txt específicos para monitorar
ARQUIVOS_TXT_MONITORADOS = [
    "adware_senai.txt",
    "backdoor_senai.txt",
    "botnet_senai.txt",
    "cryptominer_senai.txt",
    "downloader_senai.txt",
    "exploit_senai.txt",
    "keylogger_senai.txt",
    "ransomware_senai.txt",
    "rogue_software_senai.txt",
    "rootkit_senai.txt",
    "scareware_senai.txt",
    "spyware_senai.txt",
    "trojan_senai.txt",
    "worm_senai.txt",
]

# Caminhos das pastas a serem monitoradas
caminhos_possiveis = [
    "C:/Windows/System32/",
    "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup/",
    "C:/Users/Public/Documents/",
    "C:/Temp/",
    "C:/Windows/Tasks/",
    "C:/Program Files/Common Files/",
    "C:/Windows/Prefetch/",
    "C:/Windows/Debug/",
    "C:/Windows/System/",
    "C:/Users/Public/Music/",
    "C:/Windows/INF/",
    "C:/ProgramData/",
    "C:/Users/Default/AppData/Local/",
    "C:/Windows/Resources/",
    "C:/Windows/Fonts/",
]

def enviar_alerta_telegram(nome_arquivo, pasta):
    """
    Envia um alerta ao Telegram quando um arquivo monitorado .txt é aberto.
    """
    mensagem = (
        f"📄 ALERTA: O arquivo '{nome_arquivo}' foi aberto.\n"
        f"📂 Localização: {pasta}\n"
        f"⚠️ Simulação educacional."
    )
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
        requests.post(url, data=payload)
        print(f"Alerta enviado para o arquivo: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao enviar alerta ao Telegram: {e}")

def monitorar_pastas():
    """
    Monitora as pastas e detecta abertura de arquivos .txt específicos.
    """
    print("Iniciando monitoramento de arquivos .txt...")
    for caminho in caminhos_possiveis:
        if not os.path.exists(caminho):
            print(f"Pasta não encontrada: {caminho}")
            continue

        print(f"Monitorando: {caminho}")
        try:
            handle = win32file.CreateFile(
                caminho,
                win32file.FILE_LIST_DIRECTORY,
                win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE | win32file.FILE_SHARE_DELETE,
                None,
                win32file.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS,
                None,
            )
            while True:
                results = win32file.ReadDirectoryChangesW(
                    handle,
                    1024,
                    True,
                    win32con.FILE_NOTIFY_CHANGE_LAST_ACCESS,
                )
                for action, file_name in results:
                    if action == win32con.FILE_ACTION_MODIFIED and file_name in ARQUIVOS_TXT_MONITORADOS:
                        enviar_alerta_telegram(file_name, caminho)
        except Exception as e:
            print(f"Erro ao monitorar {caminho}: {e}")

if __name__ == "__main__":
    monitorar_pastas()
