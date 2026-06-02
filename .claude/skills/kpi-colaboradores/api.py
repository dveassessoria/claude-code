"""
DVE Assessoria — KPI Colaboradores
Importa tarefas do ClickUp e escreve direto no Google Sheets.

Uso:
  python3 api.py importar <colaborador> <mes>
  python3 api.py mensal   <colaborador> <mes>

Exemplos:
  python3 api.py importar ariana maio
  python3 api.py mensal   ariana maio
  python3 api.py importar ariana junho
  python3 api.py mensal   ariana junho
"""

import sys
import os
import json
import requests
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from dotenv import dotenv_values

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent.parent.parent  # raiz do projeto
_env = dotenv_values(BASE_DIR / ".env")

CLICKUP_TOKEN    = _env.get("CLICKUP_API_TOKEN", "")
TEAM_ID          = "9011393934"
SPREADSHEET_ID   = _env.get("KPI_SPREADSHEET_ID", "")
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

# ── Campo customizado ClickUp ─────────────────────────────────────────────────
FIELD_DATA_ENTREGA = "e6187410-0f09-4f62-8828-510842081759"

# ── Categorias para visão mensal ──────────────────────────────────────────────
# Ordem importa: primeira correspondência vence
CATEGORIAS_REGRAS = [
    ("Anúncios",       ["ADS"]),
    ("Social Media",   ["COPY SM", "Social Media", "Carrossel", "Carrosséis", "Carrosseis",
                        "Legenda", "Destaques", "Planejamento Mensal", "Calendário de Publicações"]),
    ("Blog",           ["Blog"]),
    ("Roteiro",        ["Roteiro", "roteiro"]),
    ("Bot / WhatsApp", ["BotConversa"]),
    ("Landing Page",   ["Landing Page"]),
]
CATEGORIA_DEFAULT = "Documentos"

def categorizar(nome_tarefa):
    nome_lower = nome_tarefa.lower()
    for categoria, keywords in CATEGORIAS_REGRAS:
        for kw in keywords:
            if kw.lower() in nome_lower:
                return categoria
    return CATEGORIA_DEFAULT

# ── ClickUp ───────────────────────────────────────────────────────────────────
def buscar_tarefas(user_id, mes_num, ano):
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

# ── Google Sheets — conexão ───────────────────────────────────────────────────
def get_spreadsheet():
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=scopes)
    gc = gspread.authorize(creds)
    return gc.open_by_key(SPREADSHEET_ID)

def get_sheet(nome_aba):
    import gspread
    planilha = get_spreadsheet()
    try:
        sheet = planilha.worksheet(nome_aba)
    except gspread.exceptions.WorksheetNotFound:
        sheet = planilha.add_worksheet(title=nome_aba, rows=500, cols=15)
        configurar_cabecalhos(sheet, nome_aba)
    return sheet

def configurar_cabecalhos(sheet, nome_aba):
    mes_titulo = nome_aba.split(" (")[0]
    sheet.merge_cells("A1:M1")
    sheet.update("A1", [[mes_titulo]])
    sheet.format("A1", {"textFormat": {"bold": True, "fontSize": 14},
                        "horizontalAlignment": "CENTER",
                        "backgroundColor": {"red": 0.776, "green": 0.937, "blue": 0.808}})

    headers = ["NOME TAREFA", "CLIENTE", "LINK", "STATUS", "INICIAL",
               "VENCIMENTO", "CONCLUSÃO", "NO PRAZO", "CORREÇÕES", "QUALIDADE", "TEMPO (dias)"]
    sheet.update("A2", [headers])
    sheet.format("A2:K2", {"textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
                            "backgroundColor": {"red": 0, "green": 0, "blue": 0}})

# ── Google Sheets — escrita diária ────────────────────────────────────────────
def escrever_tarefas(sheet, tasks):
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

        # Ler campo "Data de Entrega" preenchido pela automação do ClickUp
        conclusao = ""
        no_prazo = ""
        for cf in t.get("custom_fields", []):
            if cf.get("id") == FIELD_DATA_ENTREGA and cf.get("value"):
                conclusao_dt = datetime.fromtimestamp(int(cf["value"]) / 1000)
                conclusao = conclusao_dt.strftime("%d/%m/%Y")
                if t.get("due_date"):
                    due_dt = datetime.fromtimestamp(int(t["due_date"]) / 1000)
                    no_prazo = "SIM" if conclusao_dt.date() <= due_dt.date() else "NÃO"
                break

        linhas.append([
            t.get("name", ""),
            cliente,
            "Abrir no ClickUp",
            status,
            start,
            due,
            conclusao,  # G - CONCLUSÃO (automático via campo ClickUp)
            no_prazo,   # H - NO PRAZO (calculado automaticamente)
        ])
        links.append(task_url)

    if not linhas:
        return 0

    sheet.update(f"A3:H{2 + len(linhas)}", linhas, value_input_option="USER_ENTERED")

    # Hiperlinks na coluna C via textFormatRuns (evita erro com HYPERLINK())
    requests_body = []
    for i, url in enumerate(links):
        row = i + 3
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

    # Fórmulas em H (NO PRAZO) e J (TEMPO dias) — recalculam ao preencher G (CONCLUSÃO)
    for i in range(len(linhas)):
        row = i + 3
        # H: SIM se CONCLUSÃO <= VENCIMENTO, NÃO se passou do prazo
        requests_body.append({
            "updateCells": {
                "range": {"sheetId": sheet.id,
                          "startRowIndex": row - 1, "endRowIndex": row,
                          "startColumnIndex": 7, "endColumnIndex": 8},
                "rows": [{"values": [{"userEnteredValue": {
                    "formulaValue": f'=IF(G{row}="","",IF(G{row}<=F{row},"SIM","NÃO"))'
                }}]}],
                "fields": "userEnteredValue"
            }
        })
        # J: dias entre INICIAL e CONCLUSÃO
        requests_body.append({
            "updateCells": {
                "range": {"sheetId": sheet.id,
                          "startRowIndex": row - 1, "endRowIndex": row,
                          "startColumnIndex": 9, "endColumnIndex": 10},
                "rows": [{"values": [{"userEnteredValue": {
                    "formulaValue": f'=IF(G{row}="","",DAYS(G{row},E{row}))'
                }}]}],
                "fields": "userEnteredValue"
            }
        })

    if requests_body:
        sheet.spreadsheet.batch_update({"requests": requests_body})

    return len(linhas)

# ── Google Sheets — escrita mensal ────────────────────────────────────────────
def escrever_mensal(planilha, mes_nome, dados_diarios):
    import gspread

    nome_aba = f"{mes_nome} (mensal)"

    # Agregar por categoria
    grupos = defaultdict(lambda: {"total": 0, "sim": 0, "tempos": []})

    for row in dados_diarios:
        nome = row[0].strip() if len(row) > 0 else ""
        if not nome:
            continue

        inicial_str    = row[4].strip() if len(row) > 4 else ""
        vencimento_str = row[5].strip() if len(row) > 5 else ""
        no_prazo       = row[7].strip().upper() if len(row) > 7 else ""

        cat = categorizar(nome)
        grupos[cat]["total"] += 1

        if no_prazo == "SIM":
            grupos[cat]["sim"] += 1

        if inicial_str and vencimento_str:
            try:
                ini = datetime.strptime(inicial_str, "%d/%m/%Y")
                ven = datetime.strptime(vencimento_str, "%d/%m/%Y")
                dias = (ven - ini).days
                if dias >= 0:
                    grupos[cat]["tempos"].append(dias)
            except Exception:
                pass

    if not grupos:
        return 0

    # Montar linhas ordenadas por total (maior primeiro)
    linhas = []
    total_geral_ent = 0
    total_geral_sim = 0

    for cat, g in sorted(grupos.items(), key=lambda x: x[1]["total"], reverse=True):
        total  = g["total"]
        sim    = g["sim"]
        atraso = total - sim
        pct_prazo  = f"{sim / total * 100:.2f}%".replace(".", ",") if total > 0 else "0,00%"
        pct_atraso = f"{atraso / total * 100:.2f}%".replace(".", ",") if total > 0 else "0,00%"
        tempos = g["tempos"]
        tempo_medio = str(round(sum(tempos) / len(tempos), 1)).replace(".", ",") if tempos else "-"

        linhas.append([cat, total, sim, pct_prazo, atraso, pct_atraso, tempo_medio])
        total_geral_ent += total
        total_geral_sim += sim

    # Linha de total
    t_atraso    = total_geral_ent - total_geral_sim
    t_pct_prazo  = f"{total_geral_sim / total_geral_ent * 100:.2f}%".replace(".", ",") if total_geral_ent > 0 else "0,00%"
    t_pct_atraso = f"{t_atraso / total_geral_ent * 100:.2f}%".replace(".", ",") if total_geral_ent > 0 else "0,00%"
    linha_total  = ["Total", total_geral_ent, total_geral_sim, t_pct_prazo, t_atraso, t_pct_atraso, "-"]

    # Aba mensal
    try:
        sheet = planilha.worksheet(nome_aba)
    except gspread.exceptions.WorksheetNotFound:
        sheet = planilha.add_worksheet(title=nome_aba, rows=100, cols=10)

    sheet.clear()

    # Linha 1: título
    sheet.merge_cells("A1:G1")
    sheet.update(values=[[mes_nome]], range_name="A1")
    sheet.format("A1", {
        "textFormat": {"bold": True, "fontSize": 14, "italic": True},
        "horizontalAlignment": "RIGHT",
        "backgroundColor": {"red": 0.851, "green": 0.918, "blue": 0.827}
    })

    # Linha 2: cabeçalhos
    headers = ["DEMANDA", "ENTREGAS (total)", "NO PRAZO (total)",
               "% NO PRAZO", "EM ATRASO", "% EM ATRASO", "TEMPO MÉDIO"]
    sheet.update(values=[headers], range_name="A2:G2")
    sheet.format("A2:G2", {
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "backgroundColor": {"red": 0, "green": 0, "blue": 0},
        "horizontalAlignment": "CENTER"
    })

    # Linhas de categoria
    ultima = 2 + len(linhas)
    sheet.update(values=linhas, range_name=f"A3:G{ultima}")

    # Linha de total
    num_total = ultima + 1
    sheet.update(values=[linha_total], range_name=f"A{num_total}:G{num_total}")
    sheet.format(f"A{num_total}:G{num_total}", {
        "textFormat": {"bold": True},
        "backgroundColor": {"red": 0.851, "green": 0.918, "blue": 0.827}
    })

    return total_geral_ent

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


def cmd_mensal(colaborador_key, mes_key):
    colaborador = COLABORADORES.get(colaborador_key.lower())
    if not colaborador:
        disponiveis = ", ".join(COLABORADORES.keys())
        print(f"Colaborador '{colaborador_key}' não encontrado. Disponíveis: {disponiveis}")
        sys.exit(1)

    mes_num = MESES.get(mes_key.lower())
    if not mes_num:
        print(f"Mês '{mes_key}' não reconhecido.")
        sys.exit(1)

    mes_nome = MESES_NOME[mes_num]
    nome_aba_diario = f"{mes_nome} (diário)"

    planilha = get_spreadsheet()

    print(f"Lendo dados de '{nome_aba_diario}'...")
    try:
        import gspread
        sheet_diario = planilha.worksheet(nome_aba_diario)
    except Exception:
        print(f"Aba '{nome_aba_diario}' não encontrada. Rode 'importar {colaborador_key} {mes_key}' primeiro.")
        sys.exit(1)

    rows = sheet_diario.get_all_values()
    dados = rows[2:]  # pula título (row 0) e cabeçalho (row 1)

    print(f"Gerando visão mensal...")
    total = escrever_mensal(planilha, mes_nome, dados)
    print(f"✅ Mensal de {mes_nome} gerada — {total} tarefas em {len([r for r in dados if r[0].strip()])} linhas.")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    if args[0] == "importar" and len(args) == 3:
        cmd_importar(args[1], args[2])
    elif args[0] == "mensal" and len(args) == 3:
        cmd_mensal(args[1], args[2])
    else:
        print(f"Comando não reconhecido: {' '.join(args)}")
        print(__doc__)
        sys.exit(1)
