import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))

import mail_sender
import excel_handler
caminho_consolidado = Path(r"C:\Projetos\Portfolio\automated-excel-report\output\Relatorio Consolidado - 01-05-2026.xlsx")

print("Iniciando teste do mail_sender...")
print("─" * 40)

# Gera o consolidado para anexar
pasta_input = Path(r"C:\Projetos\Portfolio\automated-excel-report\input")
arquivos = list(pasta_input.glob("*.xlsx"))

for arquivo in arquivos:
    caminho_consolidado, df = excel_handler.processar(arquivo)

# Envia o e-mail
mail_sender.enviar_email(
    para          = "guerramarcosv@gmail.com",
    assunto       = "Teste - Relatório Automático",
    corpo         = mail_sender.montar_corpo(df),
    caminho_anexo = caminho_consolidado
)

print("E-mail enviado com sucesso!")
print("─" * 40)
print("Teste concluído!")