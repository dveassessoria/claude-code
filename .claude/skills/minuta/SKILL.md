---
name: minuta
description: Gera minuta de CS com temperatura do cliente, análise de churn, pontos de alerta e próximos passos. Busca reuniões no TLDV via API, gera doc completo no ClickUp e mensagem de WhatsApp com link da gravação. Dispara com /minuta, "fazer minuta", "gerar minuta", "minuta da reunião".
---

## O que essa skill faz

Processo 100% automatizado de minuta de CS:
1. Lista as 5 reuniões mais recentes do TLDV
2. Usuário confirma qual processar
3. Busca transcrição completa via API
4. Gera doc completo: temperatura, resumo, pontos críticos, oportunidades, análise do CS, próximos passos
5. Salva no doc "Reuniões" do cliente no ClickUp com hierarquia ano → mês → dia
6. Entrega mensagem de WhatsApp com link da gravação no TLDV
7. (Opcional) Cria tarefas da DVE no ClickUp com template padrão

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

Guarde também a URL da gravação: `https://tldv.io/app/meetings/{MEETING_ID}` — será usada no Passo 6.

---

## Passo 3 — Gerar a minuta

Com a transcrição, gere o conteúdo completo da minuta de CS.

### Regras de geração

- Extraia APENAS o que foi explicitamente dito ou combinado na reunião. Nunca invente informações.
- Se a transcrição estiver incompleta ou confusa, avise antes de continuar.
- Mantenha o tom direto e profissional.
- O doc é base de conhecimento interna — pode ser mais rico em análise, mas sem ser prolixo.
- Próximos passos: apenas ações concretas, não observações gerais.

### Nome do cliente na minuta

- Se for pessoa física (médico, advogado, nome individual): use o primeiro nome do `client_contact`
- Se for empresa (CNPJ, nome corporativo, marca): use o `company`

### Escala de temperatura

Avalie o estado geral do cliente com base na transcrição:

- 🔴 **Crítico** — sinais claros de insatisfação, risco real de churn, problemas sem solução
- 🟡 **Atenção** — preocupações pontuais, expectativas não atendidas, frição notável
- 🟢 **Saudável** — cliente engajado, satisfeito, alinhado com a DVE

### Formato obrigatório para salvar no ClickUp

```markdown
# Reunião {date} — {company_or_client}

**Data:** {date}
**Participantes:** {lista com nomes dos participantes}
**Duração:** {duration_min} min

---

## Temperatura

{🔴 Crítico / 🟡 Atenção / 🟢 Saudável}

_{1-2 linhas justificando a avaliação com base no que foi dito}_

---

## Resumo

{2-3 parágrafos: objetivo da reunião, principais pontos discutidos, decisões tomadas}

---

## Pontos Positivos

- {o que está funcionando bem no relacionamento ou nos resultados}

---

## Pontos de Alerta

- {riscos, insatisfações, sinais de churn, expectativas não atendidas}

_(Se não houver, escrever "Nenhum identificado nesta reunião.")_

---

## Oportunidades de Melhoria

- {o que podemos fazer melhor para esse cliente: serviço, entrega, comunicação, resultado}

---

## Análise do CS

- {onde o responsável pelo CS errou ou poderia ter conduzido melhor essa reunião}

_(Análise interna. Se a reunião foi bem conduzida, registrar "Reunião bem conduzida." e não inventar críticas.)_

---

## Próximos Passos

### DVE

- {tarefa}
- ...

### {Nome do Cliente ou Empresa}

- {tarefa}
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
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py clickup_save "{DOC_ID}" "{date_DD/MM/YYYY}" "/tmp/minuta_dve.md" "{TLDV_MEETING_URL}"
```

O `TLDV_MEETING_URL` é `https://tldv.io/app/meetings/{MEETING_ID}` (construído a partir do ID no Passo 1).

O script:
- Navega a hierarquia existente no doc: página raiz → ano ("2026") → mês ("Maio")
- Cria o nível de ano ou mês somente se não existir
- Cria a página do dia com o conteúdo da minuta e um link clicável para a gravação no TLDV no topo

### 5b — Salvar localmente no workspace

Imediatamente após o ClickUp, salve também no workspace local. Converta a data de DD/MM/YYYY para YYYY-MM-DD para o nome do arquivo.

```bash
mkdir -p "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code/clientes/{company}/reunioes"
cp /tmp/minuta_dve.md "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code/clientes/{company}/reunioes/{YYYY-MM-DD}.md"
```

Exemplo real: se `company = "Gramado"` e `date = "27/05/2026"`, o arquivo fica em:
`clientes/Gramado/reunioes/2026-05-27.md`

Após salvar nos dois lugares, siga direto para o Passo 6.

---

## Passo 6 — Gerar mensagem de WhatsApp

Use o `TLDV_MEETING_URL` (`https://tldv.io/app/meetings/{MEETING_ID}`) como link da mensagem.

Formato obrigatório:

```
{saudação} time! Tudo bem?

Segue o resumo da nossa reunião de hoje:
{tldv_meeting_url}

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

## Passo 7 — Criar tarefas da DVE no ClickUp

Após gerar a mensagem de WhatsApp, pergunte:

> "Quer que eu crie as tarefas da DVE no ClickUp agora?"

Se o usuário confirmar:

### 7a — Salvar tarefas em arquivo JSON

Salve a lista de tarefas da DVE (somente DVE, não as do cliente) em `/tmp/dve_tasks.json`:

```json
["Tarefa 1", "Tarefa 2", "Tarefa 3"]
```

**Regras para nomes de tarefas:**
- Máximo 5 palavras
- Sempre começar com verbo no infinitivo (ex: "Criar", "Enviar", "Revisar", "Ajustar")
- Sem artigos desnecessários — direto ao ponto
- O detalhe vai na descrição (via template do ClickUp), não no nome
- Exemplos corretos: "Criar proposta comercial", "Enviar relatório de tráfego", "Ajustar campanha Meta"
- Exemplos errados: "Precisamos criar uma proposta atualizada com os novos valores", "Ver como está a campanha"

### 7b — Encontrar a lista Tarefas do cliente

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py clickup_find_list "{company}"
```

Retorna JSON com `list_id`, `folder_name` e `score`.

**Se score < 0.4:** mostre os resultados disponíveis e pergunte ao usuário qual é a pasta correta.

### 7c — Criar as tarefas

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py clickup_create_tasks "{LIST_ID}" "/tmp/dve_tasks.json"
```

Retorna JSON com `created` (quantidade) e `tasks` (lista com nome e URL de cada tarefa criada).

### 7d — Confirmar para o usuário

Mostre um resumo limpo:

```
✅ {N} tarefas criadas em [Nome da Pasta] > Tarefas:

• Tarefa 1
• Tarefa 2
• ...

Template aplicado | Status: backlog | Atribuição: manual
```

---

## Regras gerais

- Uma pergunta por vez. Não pergunte sobre dois pontos ao mesmo tempo.
- Se a reunião não tiver próximos passos claros, avise o usuário e pergunte se quer prosseguir assim mesmo.
- Nunca use travessão (—) nos textos gerados.
- O doc no ClickUp é completo e rico — base de conhecimento interna do CS.
- A mensagem de WhatsApp é o resumo executivo + próximas ações para o cliente.
- A temperatura e a análise do CS são internas — não aparecem na mensagem do WhatsApp.
