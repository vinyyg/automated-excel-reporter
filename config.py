from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

PASTA_INPUT   = os.getenv("PASTA_INPUT")
ARQUIVO_SAIDA = os.getenv("ARQUIVO_SAIDA")
ARQUIVO_LOG   = os.getenv("ARQUIVO_LOG")

EMAIL_REMETENTE    = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA        = os.getenv("EMAIL_SENHA")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")
ASSUNTO_EMAIL      = os.getenv("ASSUNTO_EMAIL")

HORARIO_EXECUCAO = os.getenv("HORARIO_EXECUCAO")

PASTA_REPOSITORY = os.getenv("PASTA_REPOSITORY")