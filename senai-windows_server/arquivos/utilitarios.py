import tkinter as tk
import os
import time
from threading import Thread
import shutil
import pyperclip 
import socket
import ctypes
import requests
import re
from telegram import Bot
import asyncio

def mostrar_mensagem(msg, tipo="info", duracao=5000, callback=None, titulo="Mensagem", botoes=None, campos_adicionais=None):
    """
    Exibe um pop-up dinâmico para diferentes finalidades.
    
    :param msg: Mensagem principal do pop-up.
    :param tipo: Tipo da mensagem (correto, erro, info).
    :param duracao: Tempo em milissegundos antes de fechar automaticamente.
    :param callback: Função chamada após o fechamento.
    :param titulo: Título do pop-up.
    :param botoes: Lista de botões personalizados, onde cada item é um dicionário {'texto': str, 'acao': func}.
    :param campos_adicionais: Lista de campos de texto adicionais.
    """
    popup = tk.Toplevel()
    popup.overrideredirect(1)  # Remove a barra nativa de título
    largura_popup = 500
    altura_popup = 400
    largura_tela = popup.winfo_screenwidth()
    altura_tela = popup.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_popup // 2)
    pos_y = (altura_tela // 2) - (altura_popup // 2)
    popup.geometry(f"{largura_popup}x{altura_popup}+{pos_x}+{pos_y}")
    popup.configure(bg="#0f0f0f", relief="ridge", bd=2)

    # Barra superior com título
    barra_superior = tk.Frame(popup, bg="#c0c0c0", height=30, relief="raised", bd=1)
    barra_superior.pack(fill="x")
    label_titulo = tk.Label(barra_superior, text=titulo, bg="#c0c0c0", fg="#000000", font=("MS Sans Serif", 12))
    label_titulo.pack(side="left", padx=5)

    botao_fechar = tk.Button(barra_superior, text="X", bg="#c0c0c0", fg="#000000", relief="flat", font=("MS Sans Serif", 12),
                             command=lambda: fechar_popup(popup, callback))
    botao_fechar.pack(side="right", padx=5)

    # Mensagem principal
    msg_label = tk.Label(popup, text=msg, fg="#00ff00" if tipo == "correto" else "#ff0000", bg="#0f0f0f",
                         font=("Courier New", 14), wraplength=450, justify="center")
    msg_label.pack(expand=True, pady=10)

    # Campos adicionais (ex.: lista de arquivos)
    if campos_adicionais:
        for campo in campos_adicionais:
            tk.Label(popup, text=campo, bg="#1e1e1e", fg="#00ff00", font=("Courier New", 12), wraplength=450, justify="left").pack(pady=5)

    # Botões personalizados
    if botoes:
        for botao in botoes:
            tk.Button(
                popup,
                text=botao['texto'],
                bg="#00FF00",
                fg="#0f0f0f",
                font=("Courier New", 12),
                command=botao['acao']
            ).pack(pady=5)

    # Temporizador para fechar automaticamente
    contador_label = tk.Label(popup, text=f"Fechando em {duracao // 1000}s...", fg="#00ff00", bg="#0f0f0f", font=("Courier New", 12))
    contador_label.pack()

    def fechar_popup(popup, callback):
        popup.destroy()
        if callback:
            callback()

    def fechar_popup_contador(tempo_restante):
        if tempo_restante > 0:
            contador_label.config(text=f"Fechando em {tempo_restante}s...")
            popup.after(1000, fechar_popup_contador, tempo_restante - 1)
        else:
            fechar_popup(popup, callback)

    fechar_popup_contador(duracao // 1000)

def copiar_para_area_transferencia(texto):
    """Copia o texto para a área de transferência."""
    pyperclip.copy(texto)
    print("Texto copiado para a área de transferência.")

def iniciar_timer(contador_label, janela, callback_tempo_esgotado, prova_concluida):
    """
    Inicializa o temporizador para a questão atual.
    
    Args:
        contador_label: Label para exibir o tempo restante.
        janela: Instância da janela Tkinter.
        callback_tempo_esgotado: Função a ser chamada quando o tempo esgotar.
        prova_concluida: Função para verificar se a prova foi concluída.
    """
    global tempo_restante

    def atualizar_timer():
        global tempo_restante
        # Verifica se a prova foi concluída
        if prova_concluida():  
            return

        if tempo_restante > 0:
            contador_label.config(text=f"Tempo restante: {tempo_restante}s")
            tempo_restante -= 1
            janela._timer_id = janela.after(1000, atualizar_timer)
        else:
            contador_label.config(text="Tempo restante: 0s")
            callback_tempo_esgotado()
    
    def animar_opacidade(alpha):
        # Controla a animação da opacidade
        if tempo_restante > 0 and not prova_concluida():
            nova_cor = f"#{int(205 * alpha):02x}{int(220 * alpha):02x}{int(57 * alpha):02x}"
            contador_label.config(fg=nova_cor)
            novo_alpha = alpha - 0.05 if alpha > 0.0 else 1.0
            janela.after(50, lambda: animar_opacidade(novo_alpha))
        else:
            contador_label.config(fg="#00ff00")

    # Cancela qualquer timer ativo antes de iniciar um novo
    if hasattr(janela, '_timer_id'):
        janela.after_cancel(janela._timer_id)

    tempo_restante = 60
    atualizar_timer()
    animar_opacidade(1.0)

# Cancela o Timer Ativo
def parar_timer(janela):
    """
    Cancela o timer ativo.
    """
    if hasattr(janela, '_timer_id'):
        janela.after_cancel(janela._timer_id)

def criar_barra_progresso(janela, largura=300, altura=20, bg="#1e1e1e", cor_progresso="#00ff00"):
    barra_progresso = tk.Canvas(janela, width=largura, height=altura, bg=bg, highlightthickness=0)
    barra_progresso_rect = barra_progresso.create_rectangle(0, 0, 0, altura, fill=cor_progresso, outline="", tags="barra_progresso")
    barra_progresso.pack(pady=10)
    return barra_progresso, barra_progresso_rect

def atualizar_barra_progresso(barra_progresso, progresso_atual, total_questoes, progresso_label):
    if total_questoes > 0:
        proporcao = progresso_atual / total_questoes
        largura_atual = 300 * proporcao
        barra_progresso.coords("barra_progresso", 0, 0, largura_atual, 20)
        percentual = int(proporcao * 100)
        progresso_label.config(text=f"Progresso: {percentual}% Concluído." if percentual > 0 else "Progresso: 0% Concluído.")
    else:
        print("Aviso: Não é possível calcular o progresso com um total de questões igual a zero.")