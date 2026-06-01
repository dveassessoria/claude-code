"""
DVE Assessoria — KPI Colaboradores
Importa tarefas do ClickUp e escreve direto no Google Sheets.

Uso:
  python3 api.py importar <colaborador> <mes>

Exemplos:
  python3 api.py importar ariana maio
  python3 api.py importar ariana junho
  python3 api.py importar ariana julho
"""

import sys
import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import dotenv_values

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent.parent.parent  # raiz do projeto
_env = dotenv_values(BASE_DIR / ".env")

CLICKUP_TOKEN   = _env.get("CLICKUP_API_TOKEN", "")
TEAM_ID         = "9011393934"
SPREADSHEET_ID  = _env.get("KPI_SPREADSHEET_ID", "")
CREDENTIALS_PATH = BASE_DIR / _env.get("GOOGLE_CREDENTIALS_PATH", "")

# ── Colaboradores ─────────────────────────────────────────────────────────────
COLABORADORES = {
    "ariana": {"user_id": "290564417", "nome": "Ariana"},
    "ari":    {"user_id": "290564417", "nome": "Ariana"},
    "wesley": {"user_id": "55136626",  "nome": "Wesley"},
    "davi":   {"user_id": "81566218",  "nome": "Davi"},
}

# ── Meses ─────────────────────────────────────────────────────────────────────
MESES = {
    "janeiro": 1,  "fevereiro": 2, "março": 3,   "marco": 3,
    "abril": 4,    "maio": 5,      "junho": 6,
    "julho": 7,    "agosto": 8,    "setembro": 9,
    "outubro": 10, "novembro": 11, "dezembro": 12,
}

MESES_NOME = {v: k.capitalize() for k, v in MESES.items() if k != "marco"}

# ── Status a ignorar (postagem) ───────────────────────────────────────────────
STATUS_IGNORAR = {"pronto para postar", "programado", "postado", "publicado", "agendado"}

# ── Mapeamento de status ──────────────────────────────────────────────────────
STATUS_MAP = {
    "backlog": "BACKLOG", "to do": "BACKLOG", "open": "BACKLOG",
    "andamento": "ANDAMENTO", "in progress": "ANDAMENTO",
    "revisão interna": "REVISÃO INTERNA", "revisao interna": "REVISÃO INTERNA",
    "revisão": "REVISÃO INTERNA", "revisao": "REVISÃO INTERNA", "review": "REVISÃO INTERNA",
    "aprovação copy": "REVISÃO INTERNA", "aprovacao copy": "REVISÃO INTERNA",
    "correção": "CORREÇÃO", "correcao": "CORREÇÃO",
    "enviar no grupo": "ENVIAR NO GRUPO",
    "enviado p/ cliente": "ENVIADO P/ CLIENTE",
    "aprovação cliente": "ENVIADO P/ CLIENTE", "aprovacao cliente": "ENVIADO P/ CLIENTE",
    "aprovado": "APROVADO", "aprovado internamente": "APROVADO",
    "concluido": "CONCLUIDO", "concluído": "CONCLUIDO", "complete": "CONCLUIDO", "done": "CONCLUIDO",
    "finalizado": "FINALIZADO", "closed": "FINALIZADO",
}

# ── ClickUp ───────────────────────────────────────────────────────────────────
def buscar_tarefas(user_id, mes_num, ano):
    """Busca todas as tarefas do colaborador e filtra pelo mês/ano de vencimento."""
    todas = []
    page = 0

    while True:
        url = (
            f"https://api.clickup.com/api/v2/team/{TEAM_ID}/task"
            f"?assignees[]={user_id}&include_closed=true&subtasks=true&page={page}"
        )
        r = requests.get(url, headers={"Authorization": CLICKUP_TOKEN})
        r.raise_for_status()
        tasks = r.json().get("tasks", [])
        todas.extend(tasks)
        if len(tasks) < 100:
            break
        page += 1

    # Filtrar por mês/ano e remover tarefas de postagem
    resultado = []
    for t in todas:
        if not t.get("due_date"):
            continue
        due = datetime.fromtimestamp(int(t["due_date"]) / 1000)
        if due.month != mes_num or due.year != ano:
            continue
        status = (t.get("status", {}).get("status") or "").lower().strip()
        if status in STATUS_IGNORAR:
            continue
        resultado.append(t)

    return resultado

# ── Google Sheets ─────────────────────────────────────────────────────────────
def get_sheet(nome_aba):
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=scopes)
    gc = gspread.authorize(creds)
    planilha = gc.open_by_key(SPREADSHEET_ID)

    try:
        sheet = planilha.worksheet(nome_aba)
    except gspread.exceptions.WorksheetNotFound:
        sheet = planilha.add_worksheet(title=nome_aba, rows=500, cols=15)
        configurar_cabecalhos(sheet, nome_aba)

    return sheet

def configurar_cabecalhos(sheet, nome_aba):
    mes_titulo = nome_aba.split(" - ")[0]
    sheet.merge_cells("A1:M1")
    sheet.update("A1", [[mes_titulo]])
    sheet.format("A1", {"textFormat": {"bold": True, "fontSize": 14},
                        "horizontalAlignment": "CENTER",
                        "backgroundColor": {"red": 0.776, "green": 0.937, "blue": 0.808}})

    headers = ["NOME TAREFA", "CLIENTE", "LINK", "STATUS", "INICIAL",
               "VENCIMENTO", "ENTREGA", "NO PRAZO", "CORREÇÕES", "NO PRAZO",
               "QUALIDADE", "TEMPO (dias)"]
    sheet.update("A2", [headers])
    sheet.format("A2:L2", {"textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
                            "backgroundColor": {"red": 0, "green": 0, "blue": 0}})

def escrever_tarefas(sheet, tasks):
    """Limpa dados anteriores e escreve as tarefas a partir da linha 3."""
    # Limpar dados existentes (mantém cabeçalho)
    ultima_linha = max(len(tasks) + 10, 50)
    sheet.batch_clear([f"A3:M{ultima_linha}"])

    linhas = []
    links = []

    for t in tasks:
        start = ""
        if t.get("start_date"):
            start = datetime.fromtimestamp(int(t["start_date"]) / 1000).strftime("%d/%m/%Y")

        due = ""
        if t.get("due_date"):
            due = datetime.fromtimestamp(int(t["due_date"]) / 1000).strftime("%d/%m/%Y")

        cliente = (t.get("folder") or {}).get("name") or (t.get("list") or {}).get("name") or ""
        status_raw = (t.get("status") or {}).get("status") or ""
        status = STATUS_MAP.get(status_raw.lower().strip(), "")
        task_url = f"https://app.clickup.com/t/{t['id']}"

        linhas.append([
            t.get("name", ""),  # A - NOME TAREFA
            cliente,             # B - CLIENTE
            "Abrir no ClickUp",  # C - LINK (texto; URL aplicada abaixo)
            status,              # D - STATUS
            start,               # E - INICIAL
            due,                 # F - VENCIMENTO
            "",                  # G - CONCLUSÃO (manual em maio; automático a partir de junho)
            "",                  # H - NO PRAZO (manual em maio; automático a partir de junho)
        ])
        links.append(task_url)

    if not linhas:
        return 0

    sheet.update(f"A3:H{2 + len(linhas)}", linhas, value_input_option="USER_ENTERED")

    # Aplicar hiperlinks na coluna C via textFormatRuns (evita erro com HYPERLINK())
    requests_body = []
    for i, url in enumerate(links):
        row = i + 3  # começa na linha 3
        requests_body.append({
            "updateCells": {
                "range": {
                    "sheetId": sheet.id,
                    "startRowIndex": row - 1,
                    "endRowIndex": row,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3,
                },
                "rows": [{"values": [{
                    "userEnteredValue": {"stringValue": "Abrir no ClickUp"},
                    "textFormatRuns": [
                        {"startIndex": 0, "format": {"link": {"uri": url}}}
                    ]
                }]}],
                "fields": "userEnteredValue,textFormatRuns"
            }
        })

    if requests_body:
        sheet.spreadsheet.batch_update({"requests": requests_body})

    return len(linhas)


# ── CLI ───────────────────────────────────────────────────────────────────────
def cmd_importar(colaborador_key, mes_key):
    colaborador = COLABORADORES.get(colaborador_key.lower())
    if not colaborador:
        disponiveis = ", ".join(COLABORADORES.keys())
        print(f"Colaborador '{colaborador_key}' não encontrado. Disponíveis: {disponiveis}")
        sys.exit(1)

    mes_num = MESES.get(mes_key.lower())
    if not mes_num:
        print(f"Mês '{mes_key}' não reconhecido.")
        sys.exit(1)

    ano = datetime.now().year
    mes_nome = MESES_NOME[mes_num]
    nome_aba = f"{mes_nome} (diário)"

    print(f"Buscando tarefas de {colaborador['nome']} em {mes_nome}/{ano}...")
    tasks = buscar_tarefas(colaborador["user_id"], mes_num, ano)
    print(f"{len(tasks)} tarefas encontradas.")

    if not tasks:
        print("Nenhuma tarefa para importar.")
        return

    print(f"Escrevendo na aba '{nome_aba}'...")
    sheet = get_sheet(nome_aba)
    total = escrever_tarefas(sheet, tasks)
    print(f"✅ {total} tarefas importadas na aba '{nome_aba}'.")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    if args[0] == "importar" and len(args) == 3:
        cmd_importar(args[1], args[2])
    else:
        print(f"Comando não reconhecido: {' '.join(args)}")
        print(__doc__)
        sys.exit(1)
