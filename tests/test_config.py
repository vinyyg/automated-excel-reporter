"""Testes do módulo config."""

import pytest

from excel_reporter import config


def test_validar_passa_com_credenciais_completas(monkeypatch):
    """validar() não levanta exceção quando todas as variáveis estão definidas."""
    monkeypatch.setattr(config, "EMAIL_REMETENTE", "test@example.com")
    monkeypatch.setattr(config, "EMAIL_SENHA", "fake-password")
    monkeypatch.setattr(config, "EMAIL_DESTINATARIO", "dest@example.com")

    config.validar()  # não deve levantar


def test_validar_levanta_erro_se_falta_credencial(monkeypatch):
    """validar() levanta ValueError citando a variável faltante."""
    monkeypatch.setattr(config, "EMAIL_REMETENTE", "test@example.com")
    monkeypatch.setattr(config, "EMAIL_SENHA", None)
    monkeypatch.setattr(config, "EMAIL_DESTINATARIO", "dest@example.com")

    with pytest.raises(ValueError, match="EMAIL_SENHA"):
        config.validar()