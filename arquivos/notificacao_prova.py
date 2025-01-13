import os
import socket
import platform
import psutil
import asyncio
from telegram import Bot
from datetime import datetime
import ctypes

# Configuração do Telegram
TELEGRAM_TOKEN = "<SEU_TOKEN_TELEGRAM>"
TELEGRAM_CHAT_ID = "<SEU_ID_TELEGRAM>"

def verificar_admin():
    """
    Verifica se o script está sendo executado com privilégios de administrador.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except Exception as e:
        print(f"Erro ao verificar privilégios administrativos: {e}")
        return False

async def enviar_mensagem_telegram(mensagem):
    """
    Envia uma mensagem ao Telegram usando o bot configurado.
    """
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensagem, parse_mode="HTML")
        print("Mensagem enviada ao Telegram com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar mensagem ao Telegram: {e}")

def obter_todos_ips():
    """
    Coleta todos os endereços IPs da máquina.
    """
    ips = []
    for interface, enderecos in psutil.net_if_addrs().items():
        for endereco in enderecos:
            if endereco.family == socket.AF_INET:
                ips.append(endereco.address)
    return ips

def obter_detalhes_sistema():
    """
    Coleta detalhes do sistema operacional, processador, memória, disco e outros usuários.
    """
    so = platform.system()
    versao_so = platform.version()
    processador = platform.processor()
    memoria_total = round(psutil.virtual_memory().total / (1024**3), 2)  # Convertido para GB
    memoria_disponivel = round(psutil.virtual_memory().available / (1024**3), 2)  # Convertido para GB
    hostname = socket.gethostname()
    disco_livre = round(psutil.disk_usage('/').free / (1024**3), 2)  # Convertido para GB
    usuarios_logados = ", ".join([u.name for u in psutil.users()])
    python_versao = platform.python_version()
    return {
        "Sistema Operacional": f"{so} {versao_so}",
        "Processador": processador,
        "Memória Total (GB)": memoria_total,
        "Memória Disponível (GB)": memoria_disponivel,
        "Disco Livre (GB)": disco_livre,
        "Hostname": hostname,
        "Usuários Logados": usuarios_logados if usuarios_logados else "Apenas o usuário atual",
        "Versão do Python": python_versao,
    }

def escape_html(text):
    """
    Escapa caracteres especiais para HTML.
    """
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )

def enviar_notificacao_inicio():
    """
    Envia uma notificação ao Telegram indicando o início da prova.
    """
    try:
        usuario = os.getlogin()
        ips = obter_todos_ips()
        detalhes_sistema = obter_detalhes_sistema()
        admin_status = "Concedida ✅" if verificar_admin() else "Não Concedida ❌"
        horario_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        mensagem = (
            f"<b>🟢 PROVA INICIADA</b>\n"
            f"<b>👤 Usuário:</b> {escape_html(usuario)}\n"
            f"<b>⏰ Horário:</b> {escape_html(horario_inicio)}\n"
            f"<b>🌐 IPs:</b>\n" + "\n".join(f"  - {escape_html(ip)}" for ip in ips) + "\n"
            f"<b>🖥 Sistema:</b> {escape_html(detalhes_sistema['Sistema Operacional'])}\n"
            f"<b>⚙️ Processador:</b> {escape_html(detalhes_sistema['Processador'])}\n"
            f"<b>💾 Memória RAM:</b> {escape_html(str(detalhes_sistema['Memória Total (GB)']))} GB\n"
            f"<b>💾 Memória Disponível:</b> {escape_html(str(detalhes_sistema['Memória Disponível (GB)']))} GB\n"
            f"<b>🖴 Disco Livre:</b> {escape_html(str(detalhes_sistema['Disco Livre (GB)']))} GB\n"
            f"<b>🔐 Privilégios Administrativos:</b> {admin_status}\n"
            f"<b>👥 Usuários Logados:</b> {escape_html(detalhes_sistema['Usuários Logados'])}\n"
            f"<b>🐍 Versão do Python:</b> {escape_html(detalhes_sistema['Versão do Python'])}\n"
            f"<b>📌 Detalhes:</b> A prova foi iniciada com sucesso!"
        )
        asyncio.run(enviar_mensagem_telegram(mensagem))
    except Exception as e:
        print(f"Erro ao enviar notificação de início: {e}")

def enviar_notificacao_fim(acertos, total_questoes):
    """
    Envia uma notificação ao Telegram indicando o fim da prova.
    """
    try:
        usuario = os.getlogin()
        ips = obter_todos_ips()
        detalhes_sistema = obter_detalhes_sistema()
        admin_status = "Concedida ✅" if verificar_admin() else "Não Concedida ❌"
        horario_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        mensagem = (
            f"<b>✅ PROVA FINALIZADA</b>\n"
            f"<b>👤 Usuário:</b> {escape_html(usuario)}\n"
            f"<b>⏰ Horário:</b> {escape_html(horario_fim)}\n"
            f"<b>🌐 IPs:</b>\n" + "\n".join(f"  - {escape_html(ip)}" for ip in ips) + "\n"
            f"<b>🖥 Sistema:</b> {escape_html(detalhes_sistema['Sistema Operacional'])}\n"
            f"<b>⚙️ Processador:</b> {escape_html(detalhes_sistema['Processador'])}\n"
            f"<b>💾 Memória RAM:</b> {escape_html(str(detalhes_sistema['Memória Total (GB)']))} GB\n"
            f"<b>💾 Memória Disponível:</b> {escape_html(str(detalhes_sistema['Memória Disponível (GB)']))} GB\n"
            f"<b>🖴 Disco Livre:</b> {escape_html(str(detalhes_sistema['Disco Livre (GB)']))} GB\n"
            f"<b>🔐 Privilégios Administrativos:</b> {admin_status}\n"
            f"<b>👥 Usuários Logados:</b> {escape_html(detalhes_sistema['Usuários Logados'])}\n"
            f"<b>🐍 Versão do Python:</b> {escape_html(detalhes_sistema['Versão do Python'])}\n"
            f"<b>📊 Resultado:</b> {escape_html(str(acertos))}/{escape_html(str(total_questoes))} questões corretas.\n"
            f"<b>🎓 Parabéns por concluir a prova!</b>"
        )
        asyncio.run(enviar_mensagem_telegram(mensagem))
    except Exception as e:
        print(f"Erro ao enviar notificação de fim: {e}")
