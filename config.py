"""Carrega e valida configurações a partir do .env."""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


def _path_or_default(env_var: str, default: Path) -> Path:
    """Lê uma variável de caminho do .env ou usa o default. Sempre retorna Path."""
    valor = os.getenv(env_var)
    return Path(valor) if valor else default


PASTA_INPUT      = _path_or_default("PASTA_INPUT",      BASE_DIR / "input")
PASTA_REPOSITORY = _path_or_default("PASTA_REPOSITORY", BASE_DIR / "repository")
ARQUIVO_SAIDA    = _path_or_default("ARQUIVO_SAIDA",    BASE_DIR / "output" / "report.xlsx")
ARQUIVO_LOG      = _path_or_default("ARQUIVO_LOG",      BASE_DIR / "logs" / "execucao.log")

EMAIL_REMETENTE    = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA        = os.getenv("EMAIL_SENHA")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")
ASSUNTO_EMAIL      = os.getenv("ASSUNTO_EMAIL", "Relatório Automático")

HORARIO_EXECUCAO = os.getenv("HORARIO_EXECUCAO", "08:00")


def validar() -> None:
    """Garante que variáveis sensíveis estão definidas. Falha cedo com mensagem clara."""
    obrigatorios = {
        "EMAIL_REMETENTE": EMAIL_REMETENTE,
        "EMAIL_SENHA": EMAIL_SENHA,
        "EMAIL_DESTINATARIO": EMAIL_DESTINATARIO,
    }
    faltando = [k for k, v in obrigatorios.items() if not v]
    if faltando:
        raise ValueError(
            f"Variáveis obrigatórias não definidas no .env: {', '.join(faltando)}. "
            f"Use .env.example como referência."
        )