"""Testes do módulo excel_handler."""

import pandas as pd

from excel_reporter import excel_handler


def test_aplicar_formula_calcula_total_corretamente():
    """Total (R$) deve ser Quantidade × Valor Unit. (R$)."""
    df = pd.DataFrame({
        "Produto": ["Caneta", "Caderno"],
        "Quantidade": [10, 3],
        "Valor Unit. (R$)": [2.50, 15.00],
    })

    resultado = excel_handler.aplicar_formula(df)

    assert "Total (R$)" in resultado.columns
    assert resultado.loc[0, "Total (R$)"] == 25.0
    assert resultado.loc[1, "Total (R$)"] == 45.0


def test_aplicar_formula_nao_quebra_com_dataframe_vazio():
    """Função deve lidar com DataFrame vazio sem levantar exceção."""
    df = pd.DataFrame({
        "Quantidade": pd.Series(dtype=float),
        "Valor Unit. (R$)": pd.Series(dtype=float),
    })

    resultado = excel_handler.aplicar_formula(df)

    assert "Total (R$)" in resultado.columns
    assert len(resultado) == 0


def test_obter_caminho_consolidado_gera_nome_com_timestamp(monkeypatch, tmp_path):
    """O caminho consolidado deve estar na pasta de saída e conter timestamp."""
    fake_output = tmp_path / "report.xlsx"
    monkeypatch.setattr(excel_handler.config, "ARQUIVO_SAIDA", fake_output)

    caminho = excel_handler.obter_caminho_consolidado()

    assert caminho.parent == tmp_path
    assert caminho.suffix == ".xlsx"
    assert "Relatorio Consolidado" in caminho.name