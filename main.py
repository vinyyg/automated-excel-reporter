"""Ponto de entrada — monitora a pasta de input e processa arquivos Excel."""

import logging
from datetime import datetime

from excel_reporter import config, excel_handler, mail_sender, reporter, scheduler

logger = logging.getLogger(__name__)


def executar() -> None:
    """Executa um ciclo completo: lê arquivos, consolida, envia e arquiva."""
    reporter.iniciar()
    try:
        config.validar()

        arquivos = list(config.PASTA_INPUT.glob("*.xlsx"))
        reporter.registrar("Arquivos encontrados", "OK", f"{len(arquivos)} arquivos")

        if not arquivos:
            reporter.registrar(
                "Nenhum arquivo encontrado", "ERRO", str(config.PASTA_INPUT)
            )
            return

        caminho_consolidado, df = None, None
        for arquivo in arquivos:
            caminho_consolidado, df = excel_handler.processar(arquivo)
            reporter.registrar(
                f"Processado: {arquivo.name}", "OK", f"{len(df)} linhas"
            )

        data_atual = datetime.now().strftime("%d/%m/%Y")
        mail_sender.enviar_email(
            para=config.EMAIL_DESTINATARIO,
            assunto=f"{config.ASSUNTO_EMAIL} - {data_atual}",
            corpo=mail_sender.montar_corpo(df),
            caminho_anexo=caminho_consolidado,
        )
        reporter.registrar("E-mail enviado", "OK", config.EMAIL_DESTINATARIO)

        pasta_destino = excel_handler.mover_arquivos_processados()
        reporter.registrar("Arquivos movidos", "OK", str(pasta_destino))

    except Exception:
        logger.exception("Erro na execução do pipeline")
        reporter.registrar("Erro na execução", "ERRO", "ver logs/execucao.log")
    finally:
        reporter.finalizar()


if __name__ == "__main__":
    scheduler.iniciar_monitoramento(executar)