import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))

import excel_handler

pasta_input = Path(r"C:\Projetos\Portfolio\automated-excel-report\input")
arquivos = list(pasta_input.glob("*.xlsx"))

print("Iniciando teste do excel_handler...")
print("─" * 40)
print(f"Arquivos encontrados: {len(arquivos)}")

for arquivo in arquivos:
    print(f"\nProcessando: {arquivo.name}")
    caminho_consolidado, df = excel_handler.processar(arquivo)
    print(f"Linhas adicionadas : {len(df)}")

print("─" * 40)
print(f"Consolidado salvo em: {caminho_consolidado}")
print("Teste concluído!")