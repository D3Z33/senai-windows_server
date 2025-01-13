import sys
import os
import platform
import ctypes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import tkinter as tk
from tkinter import Canvas
import random
import asyncio
from utilitarios import (
    mostrar_mensagem,
    iniciar_timer,
    criar_barra_progresso,
    atualizar_barra_progresso,
    parar_timer,
)
from notificacao_prova import (
    enviar_notificacao_inicio, enviar_notificacao_fim
)
import shutil
import socket
from threading import Thread
from proxy import iniciar_proxy
import subprocess
from tkinter import Tk, messagebox, simpledialog

def solicitar_permissoes_admin():
    """
    Solicita permissões administrativas no Windows ou verifica permissões de root no Linux.
    """
    sistema_operacional = platform.system()
    
    if sistema_operacional == "Windows":
        try:
            # Verifica se o script já está sendo executado como administrador
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            print(f"Erro ao verificar permissões administrativas: {e}")
            is_admin = False

        if not is_admin:
            print("Este script precisa ser executado como administrador para monitorar todas as pastas.")
            # Caminho completo do script atual
            script = os.path.abspath(sys.argv[0])
            # Parâmetros passados ao script
            params = " ".join(f'"{arg}"' for arg in sys.argv[1:])
            try:
                # Reexecuta o script com privilégios elevados
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, f'"{script}" {params}', None, 1
                )
            except Exception as e:
                print(f"Erro ao solicitar permissões administrativas: {e}")
                input("Pressione Enter para sair...")  # Mantém a janela aberta para que o usuário veja o erro
                sys.exit(1)  # Sai se não conseguir escalar privilégios
            sys.exit()  # Fecha a instância atual do script após tentar escalar privilégios

    elif sistema_operacional == "Linux":
        # Verifica se está rodando como root
        if os.geteuid() != 0:
            print("Este script precisa ser executado como root (sudo) para monitorar todas as pastas.")
            sys.exit(1)  # Sai se não estiver executando como root

def desativar_firewall():
    """
    Desativa o Firewall do Windows Defender com interação bem-humorada.
    """
    try:
        print("Preparando para desativar o Firewall do Windows Defender...")

        # Exibe uma interação bem-humorada para "confirmar"
        root = Tk()
        root.withdraw()  # Oculta a janela principal do Tkinter

        messagebox.showinfo(
            "⚠️ ATENÇÃO IMPORTANTE ⚠️",
            "🎭 Estamos prestes a desativar o Firewall do Windows Defender...\n"
            "Isso abrirá as portas para tudo, inclusive as piadas do Fontes! 😂"
        )

        passo_a_passo = [
            "1️⃣ Verificando a coragem do usuário...",
            "2️⃣ Preparando o terreno para a liberdade da rede...",
            "3️⃣ Invocando poderes administrativos...",
            "4️⃣ Derrubando os muros do Firewall! 🚪"
        ]

        for passo in passo_a_passo:
            messagebox.showinfo("⚙️ Processando...", passo)

        # Executa o comando PowerShell para desativar o Firewall
        comando = [
            "powershell",
            "-Command",
            "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False"
        ]
        subprocess.run(comando, check=True, shell=True)

        # Exibe o pop-up final com humor
        messagebox.showinfo(
            "Firewall Desativado! 🛡️",
            "🎉 O Firewall foi desativado COMPLETAMENTE!\n"
            "Agora, sua rede está mais aberta do que o final do curso na sala de aula! 🤣"
        )

        print("Firewall desativado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao desativar o Firewall: {e}")
        messagebox.showerror("Erro", "⚠️ Não conseguimos desativar o Firewall! Algo deu errado.")
    except Exception as e:
        print(f"Erro inesperado ao desativar o Firewall: {e}")
        messagebox.showerror("Erro", f"⚠️ Ocorreu um erro inesperado: {e}")

# Lista de perguntas zoeiras para a prova com os personagens da turma SENAI
perguntas = [
    {
        "pergunta": "Renan configurou um script PowerShell que desliga servidores remotamente. Fontes rodou no servidor errado. O que fazer?",
        "resposta_correta": "C",
        "peso_risco": "alto",
        "alternativas": [
            "A) Culpa o DHCP porque sempre funciona.",
            "B) Reinicia o servidor com estilo e finge que nada aconteceu.",
            "C) Desabilita o script e aplica uma GPO de restrição.",
            "D) Chama o Robson que está na academia pra gritar 'Isso tá errado, Jao!'"
        ]
    },
    {
        "pergunta": "Franklin acha que 'NTFS' é um erro no DNS. Qual a explicação certa?",
        "resposta_correta": "D",
        "peso_risco": "baixo",
        "alternativas": [
            "A) É uma nova série de ação do Netflix.",
            "B) Significa 'Nunca Tente Fazer Scripts'.",
            "C) É a sigla para 'Nome Técnico de Fibra Simples'.",
            "D) É o sistema de arquivos que gerencia permissões no Windows."
        ]
    },
    {
        "pergunta": "Rodrigo, tentando convencer todos a usar Discord, abre a porta 3389 pra todos. Qual o problema?",
        "resposta_correta": "A",
        "peso_risco": "alto",
        "alternativas": [
            "A) A porta é usada para RDP e expõe o servidor a ataques.",
            "B) Discord usa outra porta, então tá tranquilo.",
            "C) DHCP automaticamente corrige isso, né?",
            "D) Só causa problemas se Pereira acessar com Windows 98."
        ]
    },
    {
        "pergunta": "Fontes quer aplicar uma GPO, mas Matheus e Diogo configuraram outra no mesmo domínio. Como resolver?",
        "resposta_correta": "B",
        "peso_risco": "médio",
        "alternativas": [
            "A) Deixa as duas brigarem e vê o que acontece.",
            "B) Verifica a hierarquia de aplicação e prioridades no GPMC.",
            "C) O Keîti reaparece pra decidir quem tem mais 'relaçõ de confiánça'.",
            "D) Reinicia o servidor e torce pro melhor."
        ]
    },
    {
        "pergunta": "Chile quer configurar redundância de DNS. Qual é a melhor abordagem?",
        "resposta_correta": "C",
        "peso_risco": "baixo",
        "alternativas": [
            "A) Adiciona outro DNS no mesmo servidor pra economizar.",
            "B) Desenha o DNS no Paint e manda pro Fontes validar.",
            "C) Cria um servidor secundário e sincroniza as zonas.",
            "D) Compra um roteador na promoção e reza."
        ]
    },
    {
        "pergunta": "Pereira salva backups no disco principal e diz que tá tudo certo. Qual é o problema?",
        "resposta_correta": "A",
        "peso_risco": "médio",
        "alternativas": [
            "A) Se o disco principal falhar, o backup será perdido.",
            "B) Nada, backup no mesmo disco é coisa de profissional.",
            "C) O DNS resolve isso automaticamente.",
            "D) Isso é aceitável, contanto que o Tales configure a fibra óptica."
        ]
    },
    {
        "pergunta": "Rodrigo finalmente leva a bola pro futebol, mas esquece de configurar o acesso remoto no servidor. Como habilitar RDP?",
        "resposta_correta": "D",
        "peso_risco": "baixo",
        "alternativas": [
            "A) Configura o Notepad++ como ferramenta de conexão.",
            "B) Usa o DHCP pra criar uma conexão remota.",
            "C) Habilita via Bloco de Notas com linhas de código.",
            "D) Configura RDP no Gerenciador do Servidor e ajusta o firewall."
        ]
    },
    {
        "pergunta": "Keîti reaparece e diz que 'DHCP só serve pra dar nó na fibra'. Qual é a função real do DHCP?",
        "resposta_correta": "B",
        "peso_risco": "médio",
        "alternativas": [
            "A) Fazer a rede parecer mais organizada.",
            "B) Distribuir endereços IP automaticamente na rede.",
            "C) Gerenciar backups no Active Directory.",
            "D) Resolver nomes no DNS mais rápido."
        ]
    },
    {
        "pergunta": "Fontes quer saber como aplicar permissões NTFS em uma pasta compartilhada. Qual ferramenta usar?",
        "resposta_correta": "C",
        "peso_risco": "baixo",
        "alternativas": [
            "A) Configura tudo no Notepad++ pra facilitar.",
            "B) Aplica permissões pelo Word e envia por e-mail.",
            "C) Usa o Explorador de Arquivos e ajusta na aba Segurança.",
            "D) Chama o Robson pra decidir enquanto faz flexões."
        ]
    },
    {
        "pergunta": "Tales diz que configurar DNS e fibra são a mesma coisa. Como corrigir a explicação?",
        "resposta_correta": "A",
        "peso_risco": "baixo",
        "alternativas": [
            "A) DNS resolve nomes de domínio para IPs; fibra é o meio físico.",
            "B) Ambos servem pra deixar a rede bonita.",
            "C) DNS depende da fibra, então tá quase certo.",
            "D) DNS e fibra são conceitos intercambiáveis."
        ]
    },
    {
        "pergunta": "Chile está implementando uma relação de confiança entre domínios. Pra que serve isso?",
        "resposta_correta": "A",
        "peso_risco": "médio",
        "alternativas": [
            "A) Permite autenticação entre domínios diferentes.",
            "B) Garante que o DHCP funcione em rede cruzada.",
            "C) Resolve problemas de DNS entre servidores.",
            "D) É como casamento, mas com menos drama."
        ]
    },
    {
        "pergunta": "André, enquanto desenha seu logo, quer saber como configurar um servidor web. O que é essencial?",
        "resposta_correta": "B",
        "peso_risco": "médio",
        "alternativas": [
            "A) Configurar o DNS pra apontar pro logo.",
            "B) Instalar o IIS e ajustar as permissões.",
            "C) Usar o DHCP pra criar um domínio.",
            "D) Criar uma GPO que desenhe o logo em todas as telas."
        ]
    },
    {
        "pergunta": "Franklin acha que 'svchost.exe' é um vírus porque viu no Gerenciador de Tarefas. O que você explica?",
        "resposta_correta": "C",
        "peso_risco": "baixo",
        "alternativas": [
            "A) Deleta tudo que tiver 'host' no nome.",
            "B) Usa oração pra proteger o servidor.",
            "C) É um processo essencial para serviços do Windows.",
            "D) Pergunta pro Keîti, que diz: 'Parece vírus, mas tenta reiniciar.'"
        ]
    },
    {
        "pergunta": "Diogo desabilitou o firewall em todos os servidores pra 'deixar a rede mais rápida'. Qual é o problema?",
        "resposta_correta": "A",
        "peso_risco": "alto",
        "alternativas": [
            "A) Expor os servidores a ataques e tráfego não autorizado.",
            "B) Nada, sem firewall a rede voa como um foguete.",
            "C) O DHCP resolve e impede qualquer ataque, certo?",
            "D) Apenas reiniciar o servidor resolve tudo."
        ]
    },
    {
        "pergunta": "Matheus e Diogo estão discutindo sobre como aplicar uma GPO pra toda a empresa. Qual ferramenta usar?",
        "resposta_correta": "B",
        "peso_risco": "baixo",
        "alternativas": [
            "A) Configura pelo Bloco de Notas e envia por e-mail.",
            "B) Gerenciamento de Diretiva de Grupo (GPMC).",
            "C) Usa o Paint pra criar diagramas explicativos.",
            "D) Adiciona o Fontes no grupo 'Amigos da TI'."
        ]
    }
]

# Mensagem Inicial
def mostrar_mensagem_inicial(callback_iniciar):
    """
    Mostra a mensagem inicial da prova com instruções detalhadas,
    melhor estética e impede o início da prova até que o botão seja clicado.
    """
    popup = tk.Toplevel()
    largura_popup = 850
    altura_popup = 750  # Aumentado para garantir visibilidade do botão
    largura_tela = popup.winfo_screenwidth()
    altura_tela = popup.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_popup // 2)
    pos_y = (altura_tela // 2) - (altura_popup // 2)
    popup.geometry(f"{largura_popup}x{altura_popup}+{pos_x}+{pos_y}")
    popup.configure(bg="#0f0f0f", relief="ridge", bd=2)

    # Remoção da barra superior do Windows
    popup.overrideredirect(1)

    # Barra superior personalizada
    barra_superior = tk.Frame(popup, bg="#c0c0c0", height=30, relief="raised", bd=1)
    barra_superior.pack(fill="x")
    label_titulo = tk.Label(barra_superior, text="Início da Prova", bg="#c0c0c0", fg="#000000", font=("MS Sans Serif", 12))
    label_titulo.pack(side="left", padx=5)

    botao_fechar = tk.Button(barra_superior, text="X", bg="#c0c0c0", fg="#000000", relief="flat", font=("MS Sans Serif", 12), command=popup.destroy)
    botao_fechar.pack(side="right", padx=5)

    # Logo do SENAI
    try:
        logo_caminho = os.path.join(os.path.dirname(__file__), "senai_logo.png")
        logo_img = tk.PhotoImage(file=logo_caminho)
        logo_label = tk.Label(popup, image=logo_img, bg="#0f0f0f")
        logo_label.image = logo_img
        logo_label.pack(pady=10)
    except Exception as e:
        print(f"Erro ao carregar o logo: {e}")

    # Título centralizado
    titulo_label = tk.Label(
        popup,
        text="🚀 Bem-vindo à Prova - Windows Server! 🚀",
        fg="#00FF7F",
        bg="#0f0f0f",
        font=("Courier New", 20, "bold"),
        justify="center"
    )
    titulo_label.pack(pady=10)

    # Mensagem inicial com espaçamento e frases engraçadas/profissionais
    msg_label = tk.Label(
        popup,
        text=(
            "📢 Prepare-se para enfrentar o desafio mais caótico do SENAI! Esta prova traz 15 questões recheadas de zoeira e aprendizado:\n\n"
            "- Escolha entre as alternativas A, B, C ou D. Lembre-se: um passo errado e o Fontes já está gritando 'Cadê o backup, Jao?\n\n"
            "- No final da prova, clique no Botão - Copiar Todos os Caminhos - cole no bloco de notas e divirta-se\n\n"
            "- Respostas corretas aumentam seu XP e sua moral.\n\n"
            "- Cada questão deixa um presente no sistema. 🙃\n\n"
            "- O tempo é curto: 60 segundos por pergunta.\n\n"
            "💻 Mostre que você domina o Windows Server!"
        ),
        fg="#FFFFFF",
        bg="#0f0f0f",
        font=("Courier New", 12),
        wraplength=800,
        justify="left"
    )
    msg_label.pack(pady=20)

    # Botão para começar a prova
    botao_iniciar = tk.Button(
        popup,
        text="Começar Prova",
        command=lambda: [popup.destroy(), callback_iniciar()],
        bg="#c0c0c0",  # Cor de fundo semelhante ao "Confirmar Resposta"
        fg="#000000",  # Cor da fonte
        font=("MS Sans Serif", 13),  # Fonte similar ao botão de "Confirmar Resposta"
        relief="raised",  # Efeito de botão elevado
        bd=3,  # Borda espessa para destacar o botão
        width=20,  # Largura ajustada
        height=2   # Altura ajustada
    )
    botao_iniciar.pack(pady=20)

    # Bloqueio de interação com outras janelas
    popup.grab_set()
    popup.focus_set()
    popup.transient()  # Garante que o pop-up fique acima das outras janelas

# Embaralhamento das perguntas
random.shuffle(perguntas)

# Variáveis Globais
indice_atual = 0
resultados_prova = {"corretas": 0, "erradas": 0}
tempo_restante = 60  # Controla o tempo restante para cada questão
prova_concluida = False  # Variável para controlar o término da prova

# Função de inserção de arquivos maliciosos
def inserir_arquivos_para_questao(questao_id):
    """
    Insere arquivos maliciosos e explicativos em uma pasta do sistema para a questão atual.
    """
    # Caminhos de destino ajustados para 9 pastas
    caminhos_possiveis = [
        "C:/Windows/System32/",
        "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup/",
        "C:/Users/Public/Documents/",
        "C:/Temp/",
        "C:/Users/Public/Music/",
        "C:/Users/Public/Downloads/",
        "C:/Users/Public/Downloads/",
        "C:/Program Files/Logs/",
        "C:/Users/Public/Music/"
    ]

    # Arquivos maliciosos e seus textos explicativos para cada questão
    arquivos_maliciosos = [
        ("adware_senai.exe", "adware_senai.txt"),
        ("backdoor_senai.exe", "backdoor_senai.txt"),
        ("cryptominer_senai.exe", "cryptominer_senai.txt"),
        ("downloader_senai.exe", "downloader_senai.txt"),
        ("file_manager.exe", "file_manager.txt"),
        ("keylogger_senai.exe", "keylogger_senai.txt"),
        ("notifi_senai.exe", "notifi_senai.txt"),
        ("spyware_senai.exe", "spyware_senai.txt"),
        ("worm_senai.exe", "worm_senai.txt")
    ]

    # Define o caminho de destino com base no índice da questão
    caminho_destino = caminhos_possiveis[questao_id % len(caminhos_possiveis)]
    os.makedirs(caminho_destino, exist_ok=True)  # Garante que o destino existe

    # Diretório base ajustado para empacotamento
    if hasattr(sys, "_MEIPASS"):  # Verifica se está rodando como executável
        base_dir = os.path.join(sys._MEIPASS, "maliciosos")
    else:
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maliciosos")

    # Define os caminhos de origem para o arquivo malicioso e explicativo
    arquivo_malicioso, arquivo_txt = arquivos_maliciosos[questao_id % len(arquivos_maliciosos)]
    caminho_origem_malicioso = os.path.join(base_dir, arquivo_malicioso)
    caminho_origem_txt = os.path.join(base_dir, arquivo_txt)

    try:
        # Copia os arquivos para o destino
        shutil.copy(caminho_origem_malicioso, caminho_destino)
        shutil.copy(caminho_origem_txt, caminho_destino)
        print(f"Arquivos para a questão {questao_id + 1} foram inseridos em {caminho_destino}.")
    except FileNotFoundError as e:
        print(f"Erro: Arquivo de origem não encontrado - {e}")
    except Exception as e:
        print(f"Erro ao inserir arquivos: {e}")

def verificar_resposta(entrada_resposta, label_pergunta, label_alternativas, contador_label, janela, barra_progresso, total_questoes, progresso_label):
    global indice_atual, prova_concluida

    # Verifica se a prova já foi concluída
    if prova_concluida:
        print("Prova já concluída. Nenhuma ação necessária.")
        return

    # Insere os arquivos da questão correspondente
    inserir_arquivos_para_questao(indice_atual + 1)

    # Obtém e valida a resposta do usuário
    resposta = entrada_resposta.get().strip().upper()
    if resposta not in ["A", "B", "C", "D"]:
        mostrar_mensagem("Alternativa inválida! Por favor, insira A, B, C ou D.", tipo="erro", duracao=3000)
        entrada_resposta.delete(0, tk.END)
        return

    # Verifica se a resposta está correta
    if resposta == perguntas[indice_atual]["resposta_correta"]:
        resultados_prova["corretas"] += 1
        mostrar_mensagem("Resposta Correta!", "correto", duracao=3000)
    else:
        resultados_prova["erradas"] += 1
        # Insere os arquivos maliciosos como penalidade
        inserir_arquivos_para_questao(indice_atual + 1)
        mostrar_mensagem(
            "Resposta Errada!",
            "erro",
            duracao=3000
        )

    # Verifica se é a última questão
    if indice_atual + 1 >= total_questoes:
        prova_concluida = True  # Marca a prova como concluída
        atualizar_barra_progresso(barra_progresso, total_questoes, total_questoes, progresso_label)  # Define 100%
        progresso_label.config(text="100% Concluído! Aguarde Jao(Joa)...")
        parar_timer(janela)  # Para o timer

        # Exibe mensagem final e depois o relatório
        def mostrar_mensagem_zoeira():
            print("Mensagem final exibida. Preparando o relatório final...")
            mostrar_mensagem(
                "Parabéns! Você terminou a prova e deixou o Windows Server tremendo na base!",
                "info",
                duracao=5000,
                callback=lambda: mostrar_resultado_final()
            )

        janela.after(3000, mostrar_mensagem_zoeira)  # Mostra mensagem final após 3 segundos
    else:
        avancar_proxima_pergunta(label_pergunta, label_alternativas, entrada_resposta, contador_label, janela, barra_progresso, total_questoes, progresso_label)


def avancar_proxima_pergunta(label_pergunta, label_alternativas, entrada_resposta, contador_label, janela, barra_progresso, total_questoes, progresso_label):
    global indice_atual, prova_concluida, tempo_restante

    if prova_concluida:  # Impede o avanço após conclusão
        return

    indice_atual += 1
    if indice_atual < total_questoes:
        atualizar_pergunta(label_pergunta, label_alternativas, entrada_resposta)
        tempo_restante = 60  # Reinicia o timer para a próxima questão
        iniciar_timer(
            contador_label, janela,
            lambda: tempo_esgotado(
                janela, label_pergunta, label_alternativas, entrada_resposta, 
                barra_progresso, total_questoes, progresso_label, contador_label
            )
        )
        atualizar_barra_progresso(barra_progresso, indice_atual, total_questoes, progresso_label)
    else:
        prova_concluida = True
        parar_timer(janela)
        mostrar_resultado_final()

def avancar_proxima_pergunta(label_pergunta, label_alternativas, entrada_resposta, contador_label, janela, barra_progresso, total_questoes, progresso_label):
    global indice_atual, prova_concluida, tempo_restante

    if prova_concluida:  # Impede o avanço após conclusão
        return

    indice_atual += 1
    if indice_atual < total_questoes:
        atualizar_pergunta(label_pergunta, label_alternativas, entrada_resposta)
        tempo_restante = 60  # Reinicia o timer para a próxima questão
        iniciar_timer(contador_label, janela, lambda: tempo_esgotado(
            janela, label_pergunta, label_alternativas, entrada_resposta, 
            barra_progresso, total_questoes, progresso_label, contador_label
        ))
        atualizar_barra_progresso(barra_progresso, indice_atual, total_questoes, progresso_label)
    else:
        prova_concluida = True
        parar_timer(janela)
        mostrar_resultado_final()

def avancar_proxima_pergunta(label_pergunta, label_alternativas, entrada_resposta, contador_label, janela, barra_progresso, total_questoes, progresso_label):
    global indice_atual, tempo_restante, prova_concluida

    if prova_concluida:  # Impede o avanço após conclusão
        return

    indice_atual += 1
    if indice_atual < total_questoes:
        atualizar_pergunta(label_pergunta, label_alternativas, entrada_resposta)
        tempo_restante = 60  # Reinicia o timer para a próxima questão
        iniciar_timer(
            contador_label,
            janela,
            lambda: tempo_esgotado(
                janela, label_pergunta, label_alternativas, entrada_resposta, 
                barra_progresso, total_questoes, progresso_label, contador_label
            ),
            lambda: prova_concluida  # Passa a função para verificar conclusão
        )
        atualizar_barra_progresso(barra_progresso, indice_atual, total_questoes, progresso_label)
    else:
        prova_concluida = True
        parar_timer(janela)
        mostrar_resultado_final()

def mostrar_resultado_final():
    """
    Exibe os resultados finais da prova com caminhos dos arquivos gerados,
    mensagens personalizadas e botões de copiar.
    """
    global prova_concluida

    # Marca a prova como concluída para evitar múltiplas execuções
    if not prova_concluida:
        print("Tentativa de exibir resultado final antes da conclusão.")
        return  # Garante que a função não execute novamente

    print("Exibindo pop-up final com o relatório da prova...")

    # Cancela qualquer temporizador ativo
    parar_timer(janela=None)  # Passa a janela apropriada, se necessário

    total_perguntas = len(perguntas)
    corretas = resultados_prova["corretas"]
    erradas = resultados_prova["erradas"]
    percentual = (corretas / total_perguntas) * 100

    # Determina a cor e mensagem baseada no percentual de acertos
    if percentual < 50:
        cor_percentual = "#FF0000"
        mensagem_acertos = (
            "Abaixo de 50%! Parece que sua relação com o Windows Server é tipo a do Franklin com o CCNA1: pura sofrência. "
            "O Chile tá chorando nos bastidores."
        )
    elif 50 <= percentual < 70:
        cor_percentual = "#FFFF00"
        mensagem_acertos = (
            "Entre 50% e 70%! Sobreviveu, mas tá na corda bamba, igual o Rodrigo tentando convencecer a gente pra entrar no Discord."
            "Fontes olhou e disse: 'Se fosse no HOLHOS, já tava funcionando!'"
        )
    elif 70 <= percentual < 80:
        cor_percentual = "#FFFF00"
        mensagem_acertos = (
            "Entre 70% e 80%! Você tá quase lá Jao(Joa)! Está apto(a) pro estágio na Pereira OS"
            "Mais uns ajustes e ......'"
        )
    else:
        cor_percentual = "#00FF00"
        mensagem_acertos = (
            "Acima de 80%! Parabéns! Você é tipo o Renan no modo hacker supremo: impossível de parar. "
            "Até o Robson largou os treinos de academia pra comemorar. 👏"
        )

    def copiar_caminho(caminho):
        """Copia um caminho específico para o clipboard."""
        popup.clipboard_clear()
        popup.clipboard_append(caminho)
        popup.update()

    def copiar_todos():
        """Copia todos os caminhos e arquivos para o clipboard."""
        caminhos_texto = "\n".join(
            f"Pasta: {caminho}\nArquivo: {arquivo[1]} ({arquivo[0]})"
            for caminho, arquivo in caminhos_arquivos
        )
        popup.clipboard_clear()
        popup.clipboard_append(caminhos_texto)
        popup.update()
        copiar_label.config(text="Todos os caminhos copiados com sucesso!", fg="#00FF00")

    # Caminhos de destino ajustados para 9 pastas
    caminhos_possiveis = [
        "C:/Windows/System32/",
        "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup/",
        "C:/Users/Public/Documents/",
        "C:/Temp/",
        "C:/Users/Public/Music/",
        "C:/Users/Public/Downloads/",
        "C:/Users/Public/Downloads/",
        "C:/Program Files/Logs/",
        "C:/Users/Public/Music/"
    ]

    # Arquivos maliciosos e seus textos explicativos para cada questão
    arquivos_maliciosos = [
        ("adware_senai.exe", "adware_senai.txt"),
        ("backdoor_senai.exe", "backdoor_senai.txt"),
        ("cryptominer_senai.exe", "cryptominer_senai.txt"),
        ("downloader_senai.exe", "downloader_senai.txt"),
        ("file_manager.exe", "file_manager.txt"),
        ("keylogger_senai.exe", "keylogger_senai.txt"),
        ("notifi_senai.exe", "notifi_senai.txt"),
        ("spyware_senai.exe", "spyware_senai.txt"),
        ("worm_senai.exe", "worm_senai.txt")
    ]

    caminhos_arquivos = [
        (caminhos_possiveis[i], arquivos_maliciosos[i])
        for i in range(len(arquivos_maliciosos))  # Só usa o número de arquivos existentes
    ]

    # Criação do pop-up
    popup = tk.Toplevel()
    popup.overrideredirect(1)  # Remove a barra de título nativa do SO
    largura_popup, altura_popup = 1283, 849  # Dimensões
    largura_tela = popup.winfo_screenwidth()
    altura_tela = popup.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_popup // 2)  # Centraliza horizontalmente
    pos_y = (altura_tela // 2) - (altura_popup // 2)  # Centraliza verticalmente
    popup.geometry(f"{largura_popup}x{altura_popup}+{pos_x}+{pos_y}")
    popup.configure(bg="#000000")  # Fundo preto para estilo retro
    popup.resizable(False, False)  # Impede redimensionamento

    # Funções para mover a janela ao clicar na barra superior
    def iniciar_movimento(event):
        popup.x = event.x
        popup.y = event.y

    def mover_janela(event):
        x = popup.winfo_pointerx() - popup.x
        y = popup.winfo_pointery() - popup.y
        popup.geometry(f"+{x}+{y}")

    # Barra superior personalizada
    barra_superior = tk.Frame(popup, bg="#A9A9A9", relief="flat", bd=0, height=30)  # Cinza no estilo retro
    barra_superior.pack(fill="x")

    # Título na barra superior
    titulo_barra = tk.Label(
        barra_superior,
        text="Resumo da Prova",
        bg="#A9A9A9",  # Mesma cor da barra
        fg="#000000",  # Preto para o texto
        font=("MS Sans Serif", 10),
        anchor="w"
    )
    titulo_barra.pack(side="left", padx=5)

    # Botão minimizar
    botao_minimizar = tk.Button(
        barra_superior,
        text="_",
        bg="#A9A9A9",
        fg="#000000",
        font=("MS Sans Serif", 10),
        relief="flat",
        width=3,
        command=lambda: [popup.withdraw(), popup.after(1, popup.deiconify)]
    )
    botao_minimizar.pack(side="right", padx=2)

    # Botão fechar
    botao_fechar = tk.Button(
        barra_superior,
        text="X",
        bg="#A9A9A9",
        fg="#000000",
        font=("MS Sans Serif", 10),
        relief="flat",
        width=3,
        command=popup.destroy
    )
    botao_fechar.pack(side="right", padx=2)

    # Borda retro (preta)
    borda_externa = tk.Frame(popup, bg="#000000", relief="ridge", bd=5)  # Preto para bordas estilo retro
    borda_externa.pack(fill="both", expand=True)

    # Dentro da borda, adiciona o conteúdo
    conteudo_frame = tk.Frame(borda_externa, bg="#000000", relief="flat", bd=0)  # Área de conteúdo ajustada
    conteudo_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Logo do SENAI
    try:
        # Diretório base ajustado para empacotamento
        if hasattr(sys, "_MEIPASS"):  # Verifica se está rodando como executável
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        # Caminho do logo
        logo_caminho = os.path.join(base_dir, "senai_logo.png")
        logo_img = tk.PhotoImage(file=logo_caminho)
        logo_label = tk.Label(popup, image=logo_img, bg="#0f0f0f")
        logo_label.image = logo_img
        logo_label.pack(pady=10)
    except Exception as e:
        print(f"Erro ao carregar o logo: {e}")

    # Mensagem do resumo com cores dinâmicas
    resumo_label = tk.Label(
        conteudo_frame,
        text=f"Resultado da Prova!\n",
        fg="#FFFFFF",  # Branco fixo para o título
        bg="#000000",
        font=("Courier New", 16, "bold"),
        justify="center",
        wraplength=1000
    )
    resumo_label.pack(pady=10)

    # Respostas corretas e erradas com cores específicas
    corretas_label = tk.Label(
        conteudo_frame,
        text=f"Respostas corretas: {corretas}/{total_perguntas}",
        fg="#00FF00",  # Verde para corretas
        bg="#000000",
        font=("Courier New", 14),
        justify="center"
    )
    corretas_label.pack(pady=5)

    erradas_label = tk.Label(
        conteudo_frame,
        text=f"Respostas erradas: {erradas}/{total_perguntas}",
        fg="#FF0000",  # Vermelho para erradas
        bg="#000000",
        font=("Courier New", 14),
        justify="center"
    )
    erradas_label.pack(pady=5)

    # Mensagem do percentual com cor dinâmica
    percentual_label = tk.Label(
        conteudo_frame,
        text=f"{mensagem_acertos}",
        fg=cor_percentual,  # Cor dinâmica com base no percentual
        bg="#000000",
        font=("Courier New", 14),
        justify="center",
        wraplength=1000
    )
    percentual_label.pack(pady=15)

    # Quadro para caminhos e arquivos
    quadro_frame = tk.Frame(popup, bg="#0f0f0f", relief="sunken", bd=2)
    quadro_frame.pack(padx=10, pady=10, fill="both", expand=True)

    canvas = tk.Canvas(quadro_frame, bg="#0f0f0f", highlightthickness=0)
    scrollbar = tk.Scrollbar(quadro_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#0f0f0f")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Listar caminhos e arquivos com alternância de cores
    for idx, (caminho, arquivo) in enumerate(caminhos_arquivos):
        cor_fundo = "#1e1e1e" if idx % 2 == 0 else "#2e2e2e"
        item_frame = tk.Frame(scrollable_frame, bg=cor_fundo)
        item_frame.pack(pady=5, fill="x")

        caminho_label = tk.Label(item_frame, text=f"Pasta: {caminho}", fg="#FFFFFF", bg=cor_fundo, font=("Courier New", 12), anchor="w")
        caminho_label.pack(side="left", padx=10)

        botao_copiar = tk.Button(
            item_frame,
            text="Copiar Caminho",
            bg="#c0c0c0",
            fg="#000000",
            relief="raised",
            font=("MS Sans Serif", 10),
            command=lambda c=caminho: copiar_caminho(c)
        )
        botao_copiar.pack(side="right", padx=10)

        arquivo_label = tk.Label(item_frame, text=f"Arquivo: {arquivo[1]} ({arquivo[0]})", fg="#B0C4DE", bg=cor_fundo, font=("Courier New", 12), anchor="w")
        arquivo_label.pack(fill="x", padx=20)

    # Botão para copiar todos os caminhos
    copiar_todos_btn = tk.Button(
        popup,
        text="Copiar Todos os Caminhos",
        bg="#c0c0c0",
        fg="#000000",
        font=("MS Sans Serif", 12),
        command=copiar_todos
    )
    copiar_todos_btn.pack(pady=10)

    copiar_label = tk.Label(popup, text="", fg="#FFFFFF", bg="#0f0f0f", font=("MS Sans Serif", 10))
    copiar_label.pack()

    # Envia notificação de fim ao Telegram
    try:
        enviar_notificacao_fim(resultados_prova["corretas"], total_perguntas)
        print("Notificação de fim enviada com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar notificação de fim: {e}")

    popup.mainloop()

def mostrar_mensagem_final():
    """
    Exibe o resumo da prova e opções de pós-prova.
    """
    mostrar_mensagem(
        msg=(
            f"Prova concluída!\n\n"
            f"Respostas corretas: {resultados_prova['corretas']}\n"
            f"Respostas erradas: {resultados_prova['erradas']}\n\n"
            "Clique no botão abaixo para copiar os caminhos dos arquivos gerados."
        ),
        titulo="Resumo da Prova",
        duracao=10000,
        botoes=[
            {'texto': 'Copiar Caminhos', 'acao': lambda: print("Caminhos copiados para o clipboard.")},
            {'texto': 'Fechar', 'acao': lambda: print("Prova encerrada.")}
        ]
    )

def atualizar_pergunta(label_pergunta, label_alternativas, entrada_resposta):
    global indice_atual
    if indice_atual < len(perguntas):
        # Atualiza a pergunta
        label_pergunta.config(
            text=f"Pergunta {indice_atual + 1}: {perguntas[indice_atual]['pergunta']}",
            wraplength=600,
            justify="center",
            fg="#FFFFFF",  # Cor branca para o texto da pergunta
            bg="#0f0f0f"   # Fundo escuro
        )

        # Formata as alternativas com quebra de linha entre elas
        alternativas_texto = "\n\n".join(perguntas[indice_atual]["alternativas"])
        label_alternativas.config(
            text=alternativas_texto,
            wraplength=600,
            justify="left",
            fg="#00FF00",  # Verde claro para alternativas
            bg="#0f0f0f"   # Fundo escuro
        )

        # Limpa o campo de resposta
        entrada_resposta.delete(0, tk.END)

def tempo_esgotado(janela, label_pergunta, label_alternativas, entrada_resposta, barra_progresso, total_questoes, progresso_label, contador_label):
    global resultados_prova, tempo_restante, prova_concluida

    if prova_concluida:  # Evita execução múltipla
        return

    resultados_prova["erradas"] += 1  # Incrementa as respostas erradas
    mostrar_mensagem(
        "Tempo esgotado! Resposta considerada errada.",
        tipo="erro",
        duracao=3000,
        callback=lambda: avancar_proxima_pergunta(
            label_pergunta, label_alternativas, entrada_resposta, contador_label, 
            janela, barra_progresso, total_questoes, progresso_label
        )
    )
    tempo_restante = 60  # Garante que o tempo seja reiniciado após o avanço

def criar_janela():
    tk_root.destroy()  # Remove a janela inicial antes de criar a nova interface

    janela = tk.Tk()
    janela.overrideredirect(1)  # Remove barra padrão do Windows
    janela.geometry("850x800")  # Aumentar a altura para 800
    janela.configure(bg="#0f0f0f")

    # Centralizar a janela na tela
    largura_janela = 850  # Largura
    altura_janela = 800  # Altura ajustada
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # Barra de título personalizada
    barra_superior = tk.Frame(janela, bg="#c0c0c0", height=20, relief="raised", bd=1)
    barra_superior.pack(fill="x")
    label_titulo = tk.Label(barra_superior, text="Prova - Windows Server", bg="#c0c0c0", fg="#000000", font=("MS Sans Serif", 9))
    label_titulo.pack(side="left", padx=5)

    def fechar_janela():
        janela.destroy()

    botao_fechar = tk.Button(barra_superior, text="X", bg="#c0c0c0", fg="#000000", relief="flat", font=("MS Sans Serif", 9), command=fechar_janela)
    botao_fechar.pack(side="right", padx=5)

    botao_minimizar = tk.Button(barra_superior, text="_", bg="#c0c0c0", fg="#000000", relief="flat", font=("MS Sans Serif", 9), command=janela.iconify)
    botao_minimizar.pack(side="right", padx=5)

    # Inserção do logo
    try:
        logo_caminho = os.path.join(os.path.dirname(__file__), "senai_logo.png")
        logo_img = tk.PhotoImage(file=logo_caminho)
        logo_label = tk.Label(janela, image=logo_img, bg="#0f0f0f")
        logo_label.image = logo_img  # Para evitar garbage collection
        logo_label.pack(pady=10)
    except Exception as e:
        print(f"Erro ao carregar o logo: {e}")
        logo_label = tk.Label(janela, text="Logo do SENAI não encontrado", bg="#0f0f0f", fg="#FF0000", font=("Courier New", 12))
        logo_label.pack(pady=10)

    # Layout geral
    label_titulo = tk.Label(janela, text="Prova - Windows Server", bg="#0f0f0f", fg="#00FF7F", font=("Courier New", 20, "bold"))
    label_titulo.pack(pady=10)

    contador_label = tk.Label(janela, text="Tempo restante: 60s", bg="#0f0f0f", fg="#FFD700", font=("Courier New", 12))  # Amarelo ouro
    contador_label.pack(pady=5)

    label_pergunta = tk.Label(janela, text="", bg="#0f0f0f", fg="#00ff00", font=("Courier New", 16))
    label_pergunta.pack(pady=10)

    label_alternativas = tk.Label(janela, text="", bg="#0f0f0f", fg="#00ff00", font=("Courier New", 13))
    label_alternativas.pack(pady=10)

    entrada_resposta = tk.Entry(janela, bg="#1e1e1e", fg="#00ff00", font=("Courier New", 16), insertbackground="#00ff00")
    entrada_resposta.pack(pady=10)

    botao_confirmar = tk.Button(janela, text="Confirmar Resposta", command=lambda: verificar_resposta(entrada_resposta, label_pergunta, label_alternativas, contador_label, janela, barra_progresso, total_questoes, progresso_label), bg="#c0c0c0", fg="#000000", relief="raised", bd=3, font=("MS Sans Serif", 13))
    botao_confirmar.pack(pady=10)

    # Vincular a tecla Enter para confirmar a resposta
    entrada_resposta.bind("<Return>", lambda event: verificar_resposta(entrada_resposta, label_pergunta, label_alternativas, contador_label, janela, barra_progresso, total_questoes, progresso_label))

    # Criar e usar a barra de progresso
    barra_progresso, barra_progresso_rect = criar_barra_progresso(janela)

    progresso_label = tk.Label(janela, text="Progresso: 0% Concluído", bg="#0f0f0f", fg="#B0C4DE", font=("Courier New", 12))  # Azul claro
    progresso_label.pack(pady=5)

    total_questoes = len(perguntas)
    if total_questoes > 0:
        atualizar_barra_progresso(barra_progresso, 0, total_questoes, progresso_label)

    atualizar_pergunta(label_pergunta, label_alternativas, entrada_resposta)
    iniciar_timer(
    contador_label,
    janela,
    lambda: tempo_esgotado(
        janela, label_pergunta, label_alternativas, entrada_resposta,
        barra_progresso, total_questoes, progresso_label, contador_label
    ),
    lambda: prova_concluida  # Passa a variável como função anônima
)

    janela.mainloop()

if __name__ == "__main__":
    try:
        # Solicita permissões administrativas
        print("Solicitando permissões administrativas...")
        solicitar_permissoes_admin()
        print("Permissões administrativas concedidas. Continuando execução...")
    except Exception as e:
        print(f"Erro ao solicitar permissões administrativas: {e}")
        exit(1)

    desativar_firewall()

    # Inicia o Proxy em uma thread separada
    try:
        print("Iniciando o proxy...")
        proxy_thread = Thread(target=iniciar_proxy, daemon=True)
        proxy_thread.start()
        print("Proxy iniciado com sucesso!")
    except Exception as e:
        print(f"Erro ao iniciar o proxy: {e}")
        exit(1)

    # Insere arquivos para a prova
    try:
        print("Inserindo arquivos para as questões...")
        for questao_id in range(1, len(perguntas) + 1):  # Ajustado para todas as questões
            inserir_arquivos_para_questao(questao_id)
        print("Arquivos inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir arquivos para as questões: {e}")
        exit(1)

    # Envia notificação de início
    try:
        print("Enviando notificação de início...")
        enviar_notificacao_inicio()
    except Exception as e:
        print(f"Erro ao enviar notificação de início: {e}")

    # Interface principal (Tkinter)
    tk_root = tk.Tk()
    tk_root.withdraw()  # Oculta a janela inicial até a prova ser iniciada

    try:
        print("Iniciando a prova...")
        mostrar_mensagem_inicial(callback_iniciar=lambda: criar_janela())  # Substituído iniciar_prova por criar_janela
        tk_root.mainloop()  # Loop principal do Tkinter
    except Exception as e:
        print(f"Erro ao exibir a interface da prova: {e}")
