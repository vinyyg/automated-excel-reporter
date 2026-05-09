import smtplib
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


def conectar_servidor():
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(config.EMAIL_REMETENTE, config.EMAIL_SENHA)
    return servidor


def montar_corpo(df):
    total_geral  = df["Total (R$)"].sum()
    total_vendas = len(df)
    aprovados    = len(df[df["Status"] == "Aprovado"])
    cancelados   = len(df[df["Status"] == "Cancelado"])
    pendentes    = len(df[df["Status"] == "Pendente"])

    corpo = f"""
Olá,

Segue o relatório consolidado de vendas gerado automaticamente.

📊 RESUMO
─────────────────────────────
Total de vendas : {total_vendas}
Aprovados    : {aprovados}
Cancelados   : {cancelados}
Pendentes    : {pendentes}
Total geral  : R$ {total_geral:,.2f}
─────────────────────────────

O arquivo completo está em anexo.

Atenciosamente,
Sistema de Relatórios Automáticos
    """
    return corpo


def _anexar_arquivo(msg, caminho_anexo):
    anexo = Path(caminho_anexo)
    with open(anexo, "rb") as f:
        parte = MIMEBase("application", "octet-stream")
        parte.set_payload(f.read())
        encoders.encode_base64(parte)
        parte.add_header("Content-Disposition", f'attachment; filename="{anexo.name}"')
        msg.attach(parte)


def enviar_email(para, assunto, corpo, caminho_anexo):
    msg = MIMEMultipart()
    msg["From"]    = config.EMAIL_REMETENTE
    msg["To"]      = para
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain", "utf-8"))
    _anexar_arquivo(msg, caminho_anexo)

    with conectar_servidor() as servidor:
        servidor.sendmail(config.EMAIL_REMETENTE, para, msg.as_string())