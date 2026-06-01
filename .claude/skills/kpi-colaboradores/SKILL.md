---
name: kpi-colaboradores
description: Importa tarefas do ClickUp para a planilha de KPIs dos colaboradores da DVE no Google Sheets. Suporta qualquer colaborador e qualquer mês sem precisar abrir a planilha ou editar scripts.
---

# KPI Colaboradores

Importa tarefas do ClickUp direto para a planilha de KPIs no Google Sheets.

## Quando usar

Sempre que o usuário pedir para importar, puxar ou atualizar tarefas de um colaborador na planilha de KPI. Exemplos:
- "importa as tarefas da Ariana de maio"
- "puxa junho da Ariana"
- "atualiza os KPIs de julho"
- "importar tarefas do Wesley de maio"

## Colaboradores disponíveis

- **Ariana** (ariana) — Copywriter e Social Media
- **Wesley** (wesley) — Designer
- **Davi** (davi) — Gestor de Projetos e CS

## Como executar

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/kpi-colaboradores/api.py importar <colaborador> <mes>
```

### Exemplos

```bash
# Importar maio da Ariana
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/kpi-colaboradores/api.py importar ariana maio

# Importar junho
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/kpi-colaboradores/api.py importar ariana junho

# Importar julho
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/kpi-colaboradores/api.py importar ariana julho
```

## O que é importado automaticamente

- Nome da tarefa
- Cliente (pasta do ClickUp)
- Link direto para a tarefa no ClickUp
- Status (mapeado para o dropdown da planilha)
- Data inicial
- Data de vencimento

## O que fica para preenchimento manual

- **Entrega** — data em que o colaborador avisou entrega nos comentários da tarefa
- **No Prazo** — calculado automaticamente pelo Apps Script ao preencher Entrega
- **Correções** e **Qualidade** — avaliação manual

## Aba de destino

O script detecta o mês e escreve na aba `{Mês} - Diário` da planilha.
- maio → `Maio - Diário`
- junho → `Junho - Diário`
- julho → `Julho - Diário`

Se a aba não existir, cria automaticamente com os cabeçalhos corretos.

## Status ignorados (não importados)

Tarefas com os seguintes status são ignoradas pois são de postagem, não de produção:
- Pronto para postar
- Programado
- Postado
- Publicado
- Agendado
