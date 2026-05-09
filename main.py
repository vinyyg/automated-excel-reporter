import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

import excel_handler
import mail_sender
import reporter
import scheduler

def executar():
    reporter.iniciar()

    try:
        # ─── Excel ────────────────────────────────────────
        pasta_input = Path(__file__).parent / "input"
        arquivos = list(pasta_input.glob("*.xlsx"))

        reporter.registrar("Arquivos encontrados", "OK", f"{len(arquivos)} arquivos")

        if not arquivos:
            reporter.registrar("Nenhum arquivo encontrado", "ERRO", str(pasta_input))
            return

        caminho_consolidado, df = None, None
        for arquivo in arquivos:
            caminho_consolidado, df = excel_handler.processar(arquivo)
            reporter.registrar(f"Processado: {arquivo.name}", "OK", f"{len(df)} linhas")

        # ─── E-mail ───────────────────────────────────────
        from datetime import datetime
        data_atual = datetime.now().strftime("%d/%m/%Y")

        mail_sender.enviar_email(
            para          = "guerramarcosv@gmail.com",
            assunto       = f"Relatório Automático - {data_atual}",
            corpo         = mail_sender.montar_corpo(df),
            caminho_anexo = caminho_consolidado
        )
        reporter.registrar("E-mail enviado", "OK", "guerramarcosv@gmail.com")

         # ───Move Files ───────────────────────────────────────
        pasta_destino = excel_handler.mover_arquivos_processados()
        reporter.registrar("Arquivos movidos", "OK", str(pasta_destino))
        
    except Exception as e:
        reporter.registrar("Erro na execução", "ERRO", str(e))

    finally:
        reporter.finalizar()

if __name__ == "__main__":
    scheduler.iniciar_monitoramento(executar)