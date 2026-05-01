from datetime import datetime
import config

# ─── Relatório de Execução ────────────────────────────────

relatorio = {
    "inicio"  : None,
    "fim"     : None,
    "etapas"  : [],
    "status"  : "SUCESSO"
}

def iniciar():
    relatorio["inicio"] = datetime.now()

def registrar(etapa, status="OK", detalhe=""):
    relatorio["etapas"].append({
        "etapa"  : etapa,
        "status" : status,
        "detalhe": detalhe
    })
    if status == "ERRO":
        relatorio["status"] = "FALHA"

def finalizar():
    relatorio["fim"] = datetime.now()
    duracao = (relatorio["fim"] - relatorio["inicio"]).total_seconds()

    linhas = [
        "============================================",
        "   RELATÓRIO DE EXECUÇÃO",
        "============================================",
        f"Início  : {relatorio['inicio'].strftime('%d/%m/%Y %H:%M:%S')}",
        f"Fim     : {relatorio['fim'].strftime('%d/%m/%Y %H:%M:%S')}",
        f"Duração : {duracao:.1f} segundos",
        "--------------------------------------------",
    ]

    for e in relatorio["etapas"]:
        icone = "✅" if e["status"] == "OK" else "❌"
        linha = f"{icone} {e['etapa']}"
        if e["detalhe"]:
            linha += f" : {e['detalhe']}"
        linhas.append(linha)

    linhas += [
        "--------------------------------------------",
        f"Status final : {relatorio['status']}",
        "============================================",
    ]

    output = "\n".join(linhas)
    print(output)
    salvar_log(output)

def salvar_log(output):
    with open(config.ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(output + "\n\n")