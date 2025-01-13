import os

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

# Arquivos gerados pela prova
arquivos_gerados = [
    "adware_senai.py", "adware_senai.txt",
    "backdoor_senai.py", "backdoor_senai.txt",
    "botnet_senai.py", "botnet_senai.txt",
    "cryptominer_senai.py", "cryptominer_senai.txt",
    "downloader_senai.py", "downloader_senai.txt",
    "exploit_senai.py", "exploit_senai.txt",
    "keylogger_senai.py", "keylogger_senai.txt",
    "ransomware_senai.py", "ransomware_senai.txt",
    "ransonware_notificador_senai.py", "ransonware_notificador_senai.txt",
    "rogue_software_senai.py", "rogue_software_senai.txt",
    "rootkit_senai.py", "rootkit_senai.txt",
    "scareware_senai.py", "scareware_senai.txt",
    "spyware_senai.py", "spyware_senai.txt",
    "trojan_senai.py", "trojan_senai.txt",
    "worm_senai.py", "worm_senai.txt",
]

def remover_arquivos():
    """
    Remove os arquivos gerados pela prova das pastas especificadas.
    """
    print("Removendo arquivos gerados pela prova...")
    for caminho in caminhos_possiveis:
        if not os.path.exists(caminho):
            print(f"Pasta não encontrada: {caminho}")
            continue
        
        for arquivo in arquivos_gerados:
            caminho_arquivo = os.path.join(caminho, arquivo)
            if os.path.exists(caminho_arquivo):
                try:
                    os.remove(caminho_arquivo)
                    print(f"Arquivo removido: {caminho_arquivo}")
                except Exception as e:
                    print(f"Erro ao remover arquivo {caminho_arquivo}: {e}")

if __name__ == "__main__":
    remover_arquivos()
