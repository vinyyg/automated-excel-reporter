import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from pathlib import Path
import config

# ─── Cores ────────────────────────────────────────────────
VERDE    = PatternFill("solid", start_color="C6EFCE")
VERMELHO = PatternFill("solid", start_color="FFC7CE")
AMARELO  = PatternFill("solid", start_color="FFEB9C")

# ─── Funções ──────────────────────────────────────────────

def abrir_excel(caminho):
    return load_workbook(caminho)

def ler_dados():
    pasta = Path(config.ARQUIVO_ENTRADA).parent
    arquivos = list(pasta.glob("*.xlsx"))

    dfs = []
    for arquivo in arquivos:
        df = pd.read_excel(arquivo)
        dfs.append(df)

    consolidado = pd.concat(dfs, ignore_index=True)
    return consolidado

def aplicar_formula(ws):
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        linha = row[0].row
        qtd_col   = "D"
        valor_col = "E"
        total_col = "F"
        ws[f"{total_col}{linha}"] = f"={qtd_col}{linha}*{valor_col}{linha}"

def aplicar_formatacao(ws):
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        status = row[6].value
        if status == "Aprovado":
            fill = VERDE
        elif status == "Cancelado":
            fill = VERMELHO
        elif status == "Pendente":
            fill = AMARELO
        else:
            continue
        for cell in row:
            cell.fill = fill

def salvar_excel(df):
    df.to_excel(config.ARQUIVO_SAIDA, index=False)

def processar():
    df = ler_dados()
    salvar_excel(df)
    wb = abrir_excel(config.ARQUIVO_SAIDA)
    ws = wb.active
    aplicar_formula(ws)
    aplicar_formatacao(ws)
    wb.save(config.ARQUIVO_SAIDA)
    return df