[![Tests](https://github.com/vinyyg/automated-excel-reporter/actions/workflows/tests.yml/badge.svg)](https://github.com/vinyyg/automated-excel-reporter/actions/workflows/tests.yml)

# Automated Excel Report

Sistema de automação que monitora uma pasta, consolida arquivos Excel de vendas, envia o relatório por e-mail e arquiva os arquivos processados.

## Funcionalidades

- Monitoramento automático de pasta via watchdog
- Consolidação de múltiplos arquivos `.xlsx` em um único relatório
- Formatação condicional por status (Aprovado, Cancelado, Pendente)
- Envio de e-mail via SMTP/Gmail com o relatório em anexo
- Arquivamento dos arquivos processados em pasta com timestamp
- Log de execução com status de cada etapa

## Estrutura do projeto

```
automated-excel-report/
├── main.py                  # Ponto de entrada — inicia o monitoramento
├── config.py                # Leitura de variáveis de ambiente
├── requirements.txt
├── .env                     # Variáveis de ambiente (não versionado)
├── .env.example             # Modelo de configuração
├── input/                   # Pasta monitorada — coloque os .xlsx aqui
├── output/                  # Relatórios consolidados gerados
├── repository/              # Arquivos processados arquivados por data/hora
├── logs/
│   └── execucao.log
├── src/
│   ├── excel_handler.py     # Leitura, processamento e consolidação dos Excel
│   ├── mail_sender.py       # Montagem e envio de e-mail
│   ├── reporter.py          # Relatório de execução e log
│   └── scheduler.py        # Monitoramento de pasta com watchdog
└── tests/
    ├── test_excel.py
    ├── test_email.py
    ├── test_reporter.py
    └── test_main.py         # Teste completo do fluxo
```

## Configuração

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Copie o `.env.example` para `.env` e preencha os valores:

```env
PASTA_INPUT=C:\caminho\para\input
PASTA_REPOSITORY=C:\caminho\para\repository
ARQUIVO_SAIDA=C:\caminho\para\output\relatorio.xlsx
ARQUIVO_LOG=C:\caminho\para\logs\execucao.log

EMAIL_REMETENTE=seu@gmail.com
EMAIL_SENHA=sua_senha_de_app
EMAIL_DESTINATARIO=destinatario@email.com
ASSUNTO_EMAIL=Relatório Automático

HORARIO_EXECUCAO=08:00
```

> **Gmail:** a `EMAIL_SENHA` deve ser uma **senha de app**, não a senha da conta.
> Gere em: Conta Google → Segurança → Verificação em 2 etapas → Senhas de app.

### 3. Formato esperado dos arquivos de entrada

Os arquivos `.xlsx` devem ter cabeçalho na linha 2 e conter as colunas:

| Coluna | Descrição |
|--------|-----------|
| Quantidade | Quantidade vendida |
| Valor Unit. (R$) | Valor unitário |
| Status | `Aprovado`, `Cancelado` ou `Pendente` |

## Uso

```bash
python main.py
```

O sistema inicia o monitoramento da pasta `input/`. Ao detectar um novo arquivo `.xlsx`:

1. Aguarda 2 segundos (garante que o arquivo terminou de ser copiado)
2. Processa e consolida todos os arquivos presentes na pasta
3. Envia o relatório por e-mail com o arquivo consolidado em anexo
4. Move os arquivos processados para `repository/<data>_<hora>/`
5. Registra o resultado em `logs/execucao.log`

## Fluxo de execução

```
input/*.xlsx detectado
       │
       ▼
excel_handler.processar()
  ├── lê os dados (pandas)
  ├── calcula Total (R$) = Quantidade × Valor Unit.
  └── grava em output/ com formatação condicional
       │
       ▼
mail_sender.enviar_email()
  ├── monta corpo com resumo (total, aprovados, cancelados, pendentes)
  └── envia com anexo via SMTP Gmail
       │
       ▼
excel_handler.mover_arquivos_processados()
  └── move input/*.xlsx → repository/YYYY-MM-DD_HH-MM-SS/
```

## Testes

```bash
python tests/test_main.py     # fluxo completo
python tests/test_excel.py    # processamento Excel
python tests/test_email.py    # envio de e-mail
python tests/test_reporter.py # log de execução
```
