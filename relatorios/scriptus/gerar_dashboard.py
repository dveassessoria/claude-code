#!/usr/bin/env python3
"""Dashboard Google Ads — Scriptus Comunicação
Gera dashboard.html e atualiza a planilha Google Sheets.
Rodar: python3 gerar_dashboard.py
"""

import subprocess
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import gspread

CUSTOMER_ID = "7294357892"
SKILLS_DIR = Path.home() / ".claude/skills/google-ads-ratos/scripts"
OUTPUT_FILE = Path(__file__).parent / "dashboard.html"
SHEETS_CREDENTIALS = Path.home() / ".claude/skills/google-ads-ratos/planilha-kpis.json"
SPREADSHEET_ID = "1KRTWZ-t2jZGqK0VbCJkCgOffkA8rQHiDSqgrqO8ZnSU"


def run_insights(subcommand, extra_args):
    script = SKILLS_DIR / "insights.py"
    cmd = ["python3", str(script), subcommand, "--customer-id", CUSTOMER_ID] + extra_args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro ao rodar insights.py {subcommand}: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    # Pula a linha "Client inicializado via..."
    lines = result.stdout.strip().split("\n")
    json_start = next(i for i, l in enumerate(lines) if l.strip().startswith("["))
    return json.loads("\n".join(lines[json_start:]))


def run_campaigns(extra_args):
    script = SKILLS_DIR / "insights.py"
    cmd = ["python3", str(script), "campaign", "--customer-id", CUSTOMER_ID] + extra_args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    lines = result.stdout.strip().split("\n")
    json_start = next(i for i, l in enumerate(lines) if l.strip().startswith("["))
    return json.loads("\n".join(lines[json_start:]))


def fmt_brl(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(value):
    return f"{value * 100:.2f}%".replace(".", ",")


def fmt_int(value):
    return f"{int(value):,}".replace(",", ".")


def build_dashboard(account, campaigns_data, daily_data):
    # Métricas da conta
    m = account[0]["metrics"]
    total_cost = m["cost"]
    total_clicks = int(m["clicks"])
    total_impressions = int(m["impressions"])
    total_conv = m["conversions"]
    ctr = m["ctr"]
    cpa = m["cost_per_conversion"] / 1_000_000 if total_conv > 0 else 0
    cpc = m["average_cpc"] / 1_000_000
    imp_share = m["search_impression_share"]

    # Agrega dados diários por data
    daily_by_date = {}
    for row in daily_data:
        date = row["segments"]["date"]
        dm = row["metrics"]
        if date not in daily_by_date:
            daily_by_date[date] = {"clicks": 0, "conversions": 0.0, "cost": 0.0, "impressions": 0}
        daily_by_date[date]["clicks"] += int(dm["clicks"])
        daily_by_date[date]["conversions"] += dm["conversions"]
        daily_by_date[date]["cost"] += dm["cost"]
        daily_by_date[date]["impressions"] += int(dm["impressions"])

    sorted_dates = sorted(daily_by_date.keys())
    chart_labels = [datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m") for d in sorted_dates]
    chart_clicks = [daily_by_date[d]["clicks"] for d in sorted_dates]
    chart_conv = [daily_by_date[d]["conversions"] for d in sorted_dates]
    chart_cost = [round(daily_by_date[d]["cost"], 2) for d in sorted_dates]

    # Linhas da tabela de campanhas
    camp_rows = ""
    for row in sorted(campaigns_data, key=lambda x: x["metrics"]["cost"], reverse=True):
        c = row["campaign"]
        cm = row["metrics"]
        status = c["status"]
        status_class = "status-active" if status == "ENABLED" else "status-paused"
        status_label = "Ativa" if status == "ENABLED" else "Pausada"
        name = c["name"]
        camp_cpa = cm["cost_per_conversion"] / 1_000_000 if cm["conversions"] > 0 else None
        cpa_str = fmt_brl(camp_cpa) if camp_cpa else "—"
        camp_rows += f"""
        <tr>
            <td class="camp-name">{name}</td>
            <td><span class="status-badge {status_class}">{status_label}</span></td>
            <td>{fmt_int(cm['clicks'])}</td>
            <td>{fmt_int(cm['impressions'])}</td>
            <td>{fmt_pct(cm['ctr'])}</td>
            <td>{fmt_brl(cm['cost'])}</td>
            <td>{cm['conversions']:.0f}</td>
            <td>{cpa_str}</td>
        </tr>"""

    updated_at = datetime.now().strftime("%d/%m/%Y às %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Google Ads — Scriptus | DVE Assessoria</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Plus+Jakarta+Sans:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --bg: #0F2A33;
    --card: #1E2328;
    --accent: #01FF96;
    --text: #F4F3EE;
    --text-muted: rgba(244,243,238,0.5);
    --border: rgba(244,243,238,0.08);
    --radius: 10px;
  }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Plus Jakarta Sans', sans-serif;
    min-height: 100vh;
    padding: 32px 24px 48px;
  }}
  .header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 32px;
    flex-wrap: wrap;
    gap: 12px;
  }}
  .header-left {{ display: flex; flex-direction: column; gap: 4px; }}
  .header-brand {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
  }}
  .header-title {{
    font-family: 'Montserrat', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
  }}
  .header-period {{
    font-size: 13px;
    color: var(--text-muted);
    font-weight: 300;
  }}
  .updated {{
    font-size: 12px;
    color: var(--text-muted);
    text-align: right;
  }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 14px;
    margin-bottom: 28px;
  }}
  .kpi-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 18px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .kpi-label {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--text-muted);
  }}
  .kpi-value {{
    font-family: 'Montserrat', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
  }}
  .kpi-value.accent {{ color: var(--accent); }}
  .section {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    margin-bottom: 20px;
  }}
  .section-title {{
    font-family: 'Montserrat', sans-serif;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 20px;
  }}
  .chart-wrap {{
    position: relative;
    height: 260px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  thead th {{
    text-align: left;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 0 12px 12px 0;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
  }}
  tbody td {{
    padding: 12px 12px 12px 0;
    border-bottom: 1px solid var(--border);
    vertical-align: middle;
  }}
  tbody tr:last-child td {{ border-bottom: none; }}
  .camp-name {{
    max-width: 280px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 400;
  }}
  .status-badge {{
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 20px;
    white-space: nowrap;
  }}
  .status-active {{ background: rgba(1,255,150,0.15); color: var(--accent); }}
  .status-paused {{ background: rgba(244,243,238,0.08); color: var(--text-muted); }}
  .footer {{
    margin-top: 32px;
    text-align: center;
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 300;
  }}
  .footer strong {{ color: var(--accent); font-weight: 600; }}
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <span class="header-brand">DVE Assessoria</span>
    <h1 class="header-title">Scriptus Comunicação</h1>
    <span class="header-period">Google Ads · Últimos 30 dias</span>
  </div>
  <div class="updated">Atualizado em<br>{updated_at}</div>
</div>

<div class="kpi-grid">
  <div class="kpi-card">
    <span class="kpi-label">Investimento</span>
    <span class="kpi-value accent">{fmt_brl(total_cost)}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">Conversões</span>
    <span class="kpi-value">{total_conv:.0f}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">CPA</span>
    <span class="kpi-value">{fmt_brl(cpa)}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">Cliques</span>
    <span class="kpi-value">{fmt_int(total_clicks)}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">Impressões</span>
    <span class="kpi-value">{fmt_int(total_impressions)}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">CTR</span>
    <span class="kpi-value">{fmt_pct(ctr)}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">CPC Médio</span>
    <span class="kpi-value">{fmt_brl(cpc)}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">Imp. Share</span>
    <span class="kpi-value">{fmt_pct(imp_share)}</span>
  </div>
</div>

<div class="section">
  <div class="section-title">Evolução Diária — Cliques e Conversões</div>
  <div class="chart-wrap">
    <canvas id="dailyChart"></canvas>
  </div>
</div>

<div class="section">
  <div class="section-title">Campanhas</div>
  <table>
    <thead>
      <tr>
        <th>Campanha</th>
        <th>Status</th>
        <th>Cliques</th>
        <th>Impressões</th>
        <th>CTR</th>
        <th>Investimento</th>
        <th>Conv.</th>
        <th>CPA</th>
      </tr>
    </thead>
    <tbody>{camp_rows}
    </tbody>
  </table>
</div>

<div class="footer">
  Gerado por <strong>DVE Assessoria</strong> · Dados via Google Ads API
</div>

<script>
const ctx = document.getElementById('dailyChart').getContext('2d');
new Chart(ctx, {{
  type: 'bar',
  data: {{
    labels: {json.dumps(chart_labels)},
    datasets: [
      {{
        label: 'Cliques',
        data: {json.dumps(chart_clicks)},
        backgroundColor: 'rgba(1,255,150,0.25)',
        borderColor: 'rgba(1,255,150,0.8)',
        borderWidth: 1.5,
        borderRadius: 4,
        yAxisID: 'y',
      }},
      {{
        label: 'Conversões',
        data: {json.dumps(chart_conv)},
        type: 'line',
        borderColor: '#F4F3EE',
        backgroundColor: 'transparent',
        borderWidth: 2,
        pointBackgroundColor: '#F4F3EE',
        pointRadius: 4,
        tension: 0.3,
        yAxisID: 'y1',
      }}
    ]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    interaction: {{ mode: 'index', intersect: false }},
    plugins: {{
      legend: {{
        labels: {{
          color: 'rgba(244,243,238,0.7)',
          font: {{ family: 'Plus Jakarta Sans', size: 12 }}
        }}
      }},
      tooltip: {{
        backgroundColor: '#1E2328',
        borderColor: 'rgba(244,243,238,0.1)',
        borderWidth: 1,
        titleColor: '#F4F3EE',
        bodyColor: 'rgba(244,243,238,0.7)',
      }}
    }},
    scales: {{
      x: {{
        ticks: {{ color: 'rgba(244,243,238,0.5)', font: {{ size: 11 }} }},
        grid: {{ color: 'rgba(244,243,238,0.05)' }}
      }},
      y: {{
        position: 'left',
        ticks: {{ color: 'rgba(244,243,238,0.5)', font: {{ size: 11 }} }},
        grid: {{ color: 'rgba(244,243,238,0.05)' }},
        title: {{ display: true, text: 'Cliques', color: 'rgba(1,255,150,0.7)', font: {{ size: 11 }} }}
      }},
      y1: {{
        position: 'right',
        ticks: {{ color: 'rgba(244,243,238,0.5)', font: {{ size: 11 }} }},
        grid: {{ drawOnChartArea: false }},
        title: {{ display: true, text: 'Conversões', color: 'rgba(244,243,238,0.7)', font: {{ size: 11 }} }}
      }}
    }}
  }}
}});
</script>
</body>
</html>"""

    return html


def update_sheets(account, campaigns_data, daily_data):
    gc = gspread.service_account(filename=str(SHEETS_CREDENTIALS))
    sh = gc.open_by_key(SPREADSHEET_ID)
    now = datetime.now()
    since_date = (now - timedelta(days=29)).strftime("%d/%m/%Y")
    today_fmt = now.strftime("%d/%m/%Y")

    # --- Aba 1: Resumo e Campanhas ---
    ws1 = sh.worksheet("Resumo e Campanhas")
    ws1.clear()

    m = account[0]["metrics"]
    total_cost = m["cost"]
    total_clicks = int(m["clicks"])
    total_impressions = int(m["impressions"])
    total_conv = m["conversions"]
    cpa = round(m["cost_per_conversion"] / 1_000_000, 2) if total_conv > 0 else ""
    cpc = round(m["average_cpc"] / 1_000_000, 2)
    ctr = round(m["ctr"] * 100, 2)
    cvr = round(m["conversions_from_interactions_rate"] * 100, 2)
    imp_share = round(m["search_impression_share"] * 100, 2)

    resumo_rows = [
        [f"SCRIPTUS COMUNICAÇÃO - Google Ads"],
        [f"Período: {since_date} a {today_fmt}"],
        ["Atualizado em: " + now.strftime("%d/%m/%Y %H:%M")],
        [],
        ["RESUMO DA CONTA"],
        ["Métrica", "Valor"],
        ["Investimento (R$)", round(total_cost, 2)],
        ["Cliques", total_clicks],
        ["Impressões", total_impressions],
        ["CTR (%)", ctr],
        ["Conversões", total_conv],
        ["CPA (R$)", cpa],
        ["CPC Médio (R$)", cpc],
        ["Taxa de Conversão (%)", cvr],
        ["Impression Share (%)", imp_share],
        [],
        ["CAMPANHAS"],
        ["Campanha", "Status", "Cliques", "Impressões", "CTR (%)", "Investimento (R$)", "Conversões", "CPA (R$)"],
    ]

    for row in sorted(campaigns_data, key=lambda x: x["metrics"]["cost"], reverse=True):
        c = row["campaign"]
        cm = row["metrics"]
        status = "Ativa" if c["status"] == "ENABLED" else "Pausada"
        camp_cpa = round(cm["cost_per_conversion"] / 1_000_000, 2) if cm["conversions"] > 0 else ""
        resumo_rows.append([
            c["name"], status,
            int(cm["clicks"]), int(cm["impressions"]),
            round(cm["ctr"] * 100, 2),
            round(cm["cost"], 2),
            cm["conversions"],
            camp_cpa,
        ])

    ws1.update(resumo_rows, "A1")

    # --- Aba 2: Dados Diários ---
    ws2 = sh.worksheet("Dados Diários")
    ws2.clear()

    daily_by_date = {}
    for row in daily_data:
        date = row["segments"]["date"]
        dm = row["metrics"]
        if date not in daily_by_date:
            daily_by_date[date] = {"clicks": 0, "conversions": 0.0, "cost": 0.0, "impressions": 0}
        daily_by_date[date]["clicks"] += int(dm["clicks"])
        daily_by_date[date]["conversions"] += dm["conversions"]
        daily_by_date[date]["cost"] += dm["cost"]
        daily_by_date[date]["impressions"] += int(dm["impressions"])

    daily_rows = [["Data", "Cliques", "Impressões", "Investimento (R$)", "Conversões", "CTR (%)", "CPA (R$)"]]
    for date in sorted(daily_by_date.keys()):
        d = daily_by_date[date]
        day_ctr = round(d["clicks"] / d["impressions"] * 100, 2) if d["impressions"] > 0 else 0
        day_cpa = round(d["cost"] / d["conversions"], 2) if d["conversions"] > 0 else ""
        daily_rows.append([
            date,
            d["clicks"],
            d["impressions"],
            round(d["cost"], 2),
            d["conversions"],
            day_ctr,
            day_cpa,
        ])

    ws2.update(daily_rows, "A1")
    print(f"Planilha atualizada: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")


def main():
    print("Buscando dados do Google Ads — Scriptus...")

    today = datetime.now().strftime("%Y-%m-%d")
    since = (datetime.now() - timedelta(days=29)).strftime("%Y-%m-%d")

    account = run_insights("account", ["--date-range", "LAST_30_DAYS"])
    campaigns_data = run_campaigns(["--date-range", "LAST_30_DAYS"])
    daily_data = run_insights("daily", ["--since", since, "--until", today])

    print("Atualizando planilha Google Sheets...")
    update_sheets(account, campaigns_data, daily_data)

    print("Gerando dashboard HTML...")
    html = build_dashboard(account, campaigns_data, daily_data)
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"Dashboard salvo em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
