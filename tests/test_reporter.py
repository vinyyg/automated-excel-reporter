import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))

import reporter

print("Iniciando teste do reporter...")
print("─" * 40)

reporter.iniciar()

reporter.registrar("Arquivos lidos", "OK", "24 linhas consolidadas")
reporter.registrar("Fórmulas aplicadas", "OK")
reporter.registrar("Formatação aplicada", "OK")
reporter.registrar("Arquivo salvo", "OK", "output/Relatorio Consolidado - 01-05-2026.xlsx")
reporter.registrar("E-mail enviado", "ERRO", "Credenciais inválidas")

reporter.finalizar()