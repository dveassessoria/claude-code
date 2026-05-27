---
name: minuta
description: Gera minuta de reunião com clientes. Busca automaticamente as reuniões mais recentes no TLDV via API, extrai transcrição, gera resumo + próximos passos, salva no ClickUp Docs (hierarquia ano → mês → dia) e entrega mensagem de WhatsApp pronta. Dispara com /minuta, "fazer minuta", "gerar minuta", "minuta da reunião".
---

## O que essa skill faz

Processo 100% automatizado de minuta:
1. Lista as 5 reuniões mais recentes do TLDV
2. Usuário confirma qual processar
3. Busca transcrição completa via API
4. Gera minuta + próximos passos separados por responsável
5. Salva no doc "Reuniões" do cliente no ClickUp com hierarquia ano → mês → dia
6. Entrega mensagem de WhatsApp pronta com o link

**Script helper:** `.claude/skills/minuta/api.py`
**Raiz do projeto:** `/Users/macbookairm4/Documents/DVE Assessoria/Claude Code`

Todos os comandos devem ser executados com:
```
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code"
```

---

## Passo 1 — Listar reuniões recentes

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py tldv_list
```

Apresente as reuniões de forma limpa. Exemplo:
```
Aqui estão as últimas 5 reuniões gravadas:

1. Gramado - CS Danilo  |  27/05/2026 14:30  |  38 min
2. DVE & MrSul          |  27/05/2026 14:00  |  49 min
3. Altitude - CS Davi   |  26/05/2026 10:00  |  42 min
...

Qual vamos processar?
```

Aguarde o usuário escolher (número, nome ou "a última").

---

## Passo 2 — Buscar transcrição e metadados

Com o ID da reunião escolhida, execute os dois comandos em paralelo:

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py tldv_transcript {MEETING_ID}
```

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py tldv_info {MEETING_ID}
```

O `tldv_info` retorna JSON com:
- `company` — nome da empresa/cliente (extraído do título da reunião)
- `client_contact` — nome do contato do cliente
- `date` — DD/MM/YYYY
- `year`, `month`, `day_page`
- `invitees` — lista de participantes

---

## Passo 3 — Gerar a minuta

Com a transcrição, gere o conteúdo completo da minuta.

### Regras de geração

- Extraia APENAS o que foi explicitamente dito ou combinado na reunião. Nunca invente tarefas.
- Se a transcrição estiver incompleta ou confusa, avise antes de continuar.
- Mantenha o tom direto e profissional.
- Próximos passos: apenas ações concretas, não observações gerais.

### Nome do cliente na minuta

- Se for pessoa física (médico, advogado, nome individual): use o primeiro nome do `client_contact`
- Se for empresa (CNPJ, nome corporativo, marca): use o `company`

### Formato obrigatório para salvar no ClickUp

```markdown
# Reunião {date} — {company_or_client}

**Data:** {date}
**Participantes:** {lista com nomes dos participantes}
**Duração:** {duration_min} min

---

## Resumo

{3 a 5 parágrafos cobrindo: objetivo da reunião, principais pontos discutidos, decisões tomadas, observações relevantes}

---

## Próximos Passos

### DVE

- {tarefa 1}
- {tarefa 2}
- ...

### {Nome do Cliente ou Empresa}

- {tarefa 1}
- {tarefa 2}
- ...
```

Salve esse conteúdo em `/tmp/minuta_dve.md`.

---

## Passo 4 — Encontrar o doc de Reuniões no ClickUp

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py clickup_find "{company}"
```

Retorna JSON com `id`, `name` e `score` (0 a 1).

**Se score >= 0.4:** use o doc encontrado. Confirme para o usuário: "Vou salvar em '{name}'."

**Se score < 0.4 ou der erro:** liste todos os docs disponíveis e pergunte:

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py clickup_docs
```

Mostre a lista e pergunte: "Não achei o doc automaticamente. Qual é o correto?"

---

## Passo 5 — Salvar no ClickUp

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py clickup_save "{DOC_ID}" "{date_DD/MM/YYYY}" "/tmp/minuta_dve.md"
```

O script cria automaticamente:
- Página do ano (`Reuniões 2026`) se não existir
- Subpágina do mês (`Maio`) se não existir
- Subpágina do dia (`27/05/26`) com o conteúdo da minuta

Retorna JSON com `url`. Guarde essa URL para o próximo passo.

---

## Passo 6 — Gerar mensagem de WhatsApp

Gere a mensagem pronta para copiar. Formato obrigatório:

```
{saudação} time! Tudo bem?

Segue o resumo da nossa reunião de hoje:
{url_clickup}

✅ Próximas Etapas

DVE

• {tarefa 1}
• {tarefa 2}

{Nome do Cliente ou Empresa}

• {tarefa 1}
• {tarefa 2}
```

**Saudação baseada no horário atual (BRT):**
- 05h–11h59 → "Bom dia"
- 12h–17h59 → "Boa tarde"
- 18h–04h59 → "Boa noite"

Mostre a mensagem dentro de um bloco de código para facilitar o copy.

---

## Regras gerais

- Uma pergunta por vez. Não pergunte sobre dois pontos ao mesmo tempo.
- Se a reunião não tiver próximos passos claros, avise o usuário e pergunte se quer prosseguir assim mesmo.
- Nunca use travessão (—) nos textos gerados.
- A minuta no ClickUp é completa e detalhada. A mensagem de WhatsApp é só o resumo executivo + próximas ações.
