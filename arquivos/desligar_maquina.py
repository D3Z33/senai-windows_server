import os
import tkinter as tk
import ctypes

# Lista manual de IPs das máquinas
ips_maquinas = [
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX",
    "10.105.77.XX"
]

# IP da máquina que executa o script (para ignorar no comando)
meu_ip = "10.105.77.XX"

# Função para desligar todas as máquinas
def tudo_ou_nada():
    for ip in ips_maquinas:
        if ip != meu_ip:
            os.system(f'shutdown /m \\\\{ip} /s /t 0')
    tk.messagebox.showinfo("Ação Concluída", "Todas as máquinas foram desligadas.")

# Função para verificar e elevar privilégios automaticamente
def autoelevar():
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", os.path.abspath(__file__), None, None, 1
            )
            exit()
    except:
        tk.messagebox.showerror("Erro", "Falha ao elevar privilégios. Execute como administrador manualmente.")
        exit()

# Interface gráfica com um único botão
def criar_interface():
    root = tk.Tk()
    root.title("Tudo ou Nada!")
    root.geometry("400x200")
    root.resizable(False, False)

    # Centralizar a janela na tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (200 // 2)
    root.geometry(f"400x200+{x}+{y}")

    # Título e botão único
    tk.Label(root, text="Tudo ou Nada!", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Button(root, text="1", command=tudo_ou_nada, font=("Arial", 14), width=10).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    autoelevar()  # Eleva privilégios automaticamente
    criar_interface()
