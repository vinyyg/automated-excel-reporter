[![Tests](https://github.com/vinyyg/automated-excel-reporter/actions/workflows/tests.yml/badge.svg)](https://github.com/vinyyg/automated-excel-reporter/actions/workflows/tests.yml)

# Automated Excel Report

An automation system that monitors a folder, consolidates Excel sales files, sends the report by email, and archives the processed files.

## Features

- Automatic folder monitoring via watchdog
- Consolidation of multiple `.xlsx` files into a single report
- Conditional formatting by status (Approved, Cancelled, Pending)
- Email delivery via SMTP/Gmail with the report as an attachment
- Processed files archived in a timestamped folder
- Execution log with per-step status

## Project structure

```
automated-excel-report/
├── main.py                  # Entry point — starts the folder monitoring
├── config.py                # Environment variable loading
├── requirements.txt
├── .env                     # Environment variables (not versioned)
├── .env.example             # Configuration template
├── input/                   # Monitored folder — place .xlsx files here
├── output/                  # Generated consolidated reports
├── repository/              # Processed files archived by date/time
├── logs/
│   └── execucao.log
├── src/
│   ├── excel_handler.py     # Excel reading, processing and consolidation
│   ├── mail_sender.py       # Email composition and delivery
│   ├── reporter.py          # Execution report and log
│   └── scheduler.py         # Folder monitoring with watchdog
└── tests/
    ├── test_excel.py
    ├── test_email.py
    ├── test_reporter.py
    └── test_main.py         # Full flow test
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in the values:

```env
PASTA_INPUT=C:\path\to\input
PASTA_REPOSITORY=C:\path\to\repository
ARQUIVO_SAIDA=C:\path\to\output\report.xlsx
ARQUIVO_LOG=C:\path\to\logs\execucao.log

EMAIL_REMETENTE=you@gmail.com
EMAIL_SENHA=your_app_password
EMAIL_DESTINATARIO=recipient@email.com
ASSUNTO_EMAIL=Automated Report

HORARIO_EXECUCAO=08:00
```

> **Gmail:** `EMAIL_SENHA` must be an **app password**, not your account password.
> Generate one at: Google Account → Security → 2-Step Verification → App passwords.

### 3. Expected input file format

The `.xlsx` files must have a header on row 2 and contain the following columns:

| Column | Description |
|--------|-------------|
| Quantidade | Units sold |
| Valor Unit. (R$) | Unit price |
| Status | `Aprovado`, `Cancelado` or `Pendente` |

## Usage

```bash
python main.py
```

The system starts monitoring the `input/` folder. When a new `.xlsx` file is detected:

1. Waits 2 seconds to ensure the file has finished copying
2. Processes and consolidates all files present in the folder
3. Sends the report by email with the consolidated file as an attachment
4. Moves the processed files to `repository/<date>_<time>/`
5. Records the result in `logs/execucao.log`

## Execution flow

```
input/*.xlsx detected
       │
       ▼
excel_handler.processar()
  ├── reads data (pandas)
  ├── calculates Total (R$) = Quantidade × Valor Unit.
  └── writes to output/ with conditional formatting
       │
       ▼
mail_sender.enviar_email()
  ├── builds body with summary (total, approved, cancelled, pending)
  └── sends with attachment via SMTP Gmail
       │
       ▼
excel_handler.mover_arquivos_processados()
  └── moves input/*.xlsx → repository/YYYY-MM-DD_HH-MM-SS/
```

## Tests

```bash
python tests/test_main.py     # full flow
python tests/test_excel.py    # Excel processing
python tests/test_email.py    # email delivery
python tests/test_reporter.py # execution log
```
