---
name: onboarding-revops
description: Executa o onboarding completo de um novo cliente de RevOps. Busca a reunião de onboarding no TLDV, gera o documento de base de conhecimento, cria toda a estrutura no ClickUp (pasta, listas, docs, tarefas) e no Google Drive. Dispara com /onboarding-revops, "onboarding RevOps", "novo cliente RevOps", "configurar cliente RevOps".
---

## O que essa skill faz

Processo completo de onboarding de um novo cliente de RevOps:
1. Busca a reunião de onboarding no TLDV
2. Gera documento de base de conhecimento a partir da transcrição
3. Cria estrutura completa no ClickUp (pasta, listas Anúncios e Tarefas, docs, tarefas de onboarding)
4. Cria estrutura completa no Google Drive (pasta do cliente com subpastas)
5. Busca o contrato no ZapSign e cria guia no ClickUp com os links

**Script helper:** `.claude/skills/onboarding-revops/api.py`
**Raiz do projeto:** `/Users/macbookairm4/Documents/DVE Assessoria/Claude Code`

Todos os comandos Bash devem ser executados com:
```
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code"
```

---

## Passo 1 — Identificar a reunião de onboarding no TLDV

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py tldv_list
```

Apresente as reuniões e pergunte qual é a do onboarding. Aguarde o usuário confirmar (número, nome ou "a última").

---

## Passo 2 — Buscar transcrição e metadados

Com o ID da reunião confirmada, execute em paralelo:

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py tldv_transcript {MEETING_ID}
```

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/minuta/api.py tldv_info {MEETING_ID}
```

Do `tldv_info`, extraia:
- `company` — nome do cliente (extraído do título da reunião, após " - ")
- `date` — DD/MM/YYYY
- `year`, `month` (em português), `day_page`
- `invitees` — participantes

**Importante:** O `tldv_info` extrai o company do título antes do " - ". Se o título for "Onboarding - T2 Elevadores", o company será "Onboarding". Nesse caso, extraia manualmente o nome real do cliente do título da reunião.

Guarde também: `TLDV_MEETING_URL = https://tldv.io/app/meetings/{MEETING_ID}`

---

## Passo 3 — Gerar documento de base de conhecimento

Com a transcrição completa, gere o documento de onboarding. Use a habilidade de um CS senior especialista em documentar reuniões de onboarding de RevOps.

### Regras de geração

- Extraia APENAS o que foi explicitamente dito na reunião. Nunca invente informações.
- Se a transcrição estiver incompleta, avise antes de continuar.
- Tom direto e profissional. É base de conhecimento interna.
- Nunca usar travessão (—) em nenhuma parte do documento.

### Formato obrigatório

```markdown
# Base de Conhecimento — {COMPANY}

**Data do onboarding:** {date}
**Serviço contratado:** RevOps
**Responsável DVE:** Danilo Santana
**CS DVE:** Davi Vinicius
**Participantes do cliente:** {nomes e cargos}
**Investimento em mídia paga:** R$ {valor}/mês
**Contatos de e-mail:** {emails}

---

## A empresa

{2-3 parágrafos: o que faz, fundação, estrutura, faturamento aproximado se mencionado}

---

## Território de atendimento

{lista de cidades/regiões}

---

## Como a empresa chegou até aqui

{origem dos clientes atuais, histórico de marketing, experiências anteriores com agências}

---

## Público-alvo

**Quem decide:** {perfil do decisor}
**Perfil:** {faixa etária, gênero, comportamento}
**Tipo de cliente:** {características principais}

---

## Processo comercial atual

{passo a passo numerado de como vendem hoje}

**Etapa em que mais perde leads:** {onde a conversão cai}
**O que está sendo estruturado agora:** {mudanças em andamento}

---

## Proposta de valor e diferenciais

- {lista de diferenciais mencionados}

---

## Objeções do mercado

{objeções identificadas com argumentos de resposta}

---

## Presença digital atual

- **Site:** {url e situação}
- **Instagram:** {situação}
- **Facebook/Meta:** {situação}
- **Google Meu Negócio:** {situação}

---

## Estratégia de canais definida

- **Foco:** {canais prioritários}
- {outros detalhes de estratégia acordados}
- **Investimento inicial:** R$ {valor}/mês em mídia paga

---

## Acessos necessários

| Acesso | Responsável | Status |
|---|---|---|
| {acesso} | {quem vai fornecer} | Pendente |

---

## Próximos passos acordados

**DVE — até {data}:**
- {lista de ações}

**Reunião técnica — {data} às {hora}:**
- {pauta}

**{Nome do Cliente} — até {data}:**
- {lista de ações}

---

## Notas operacionais

- {pontos importantes sobre o cliente, contatos, avisos}
```

Salve o conteúdo em `/tmp/onboarding_{COMPANY_SLUG}.md` (company_slug = nome em minúsculas com hífens, sem acentos).

---

## Passo 4 — Salvar localmente no workspace

```bash
mkdir -p "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code/clientes/{COMPANY_SLUG}"
cp /tmp/onboarding_{COMPANY_SLUG}.md "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code/clientes/{COMPANY_SLUG}/base-conhecimento-onboarding.md"
```

---

## Passo 5 — Criar estrutura no ClickUp

Execute via script:

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/onboarding-revops/api.py clickup_setup "{COMPANY}" "{ONBOARDING_CONTENT_FILE}" "{date_DD/MM/YYYY}" "{TLDV_MEETING_URL}"
```

O script faz tudo em sequência:
1. Cria a pasta do cliente no Space "Tipo A - Clientes"
2. Cria lista Anúncios com `override_statuses: true` + statuses corretos
3. Cria lista Tarefas com statuses corretos
4. Cria view "Lista" com 5 colunas em ambas as listas
5. Cria Doc "Docs - {COMPANY}" com 6 guias (Onboarding com conteúdo, Acessos, Entregáveis com os 9 entregáveis, Benchmark, Tráfego Pago, ICP e Personas)
6. Cria Doc "Reuniões {COMPANY}" com hierarquia Reuniões > Ano > Mês > Data (conteúdo do onboarding)

Retorna JSON com todos os IDs criados.

---

## Passo 6 — Criar estrutura no Google Drive

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/onboarding-revops/api.py drive_setup "{COMPANY}"
```

O script cria:
- Pasta `{COMPANY}` dentro de `[WORK] - DVE Assessoria > 3. Operação > 1. Clientes`
- Subpastas: Anúncios, Documentos, Comercial, Identidade Visual, Fotos e Vídeos, Listas de Clientes, Planilhas, Contrato
- Dentro de Anúncios: RM 01 a RM 05, cada um com: Prontos, Revisão, Arquivos Brutos

Retorna JSON com os IDs das pastas criadas (incluindo `contrato_folder_id` e `drive_folder_url`).

---

## Passo 7 — Buscar contrato no ZapSign

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/onboarding-revops/api.py zapsign_find "{COMPANY}"
```

Busca o contrato do cliente no ZapSign varrendo todas as páginas. Retorna JSON com `name`, `token`, `status` e `zapsign_url` (link permanente).

Se não encontrar, informe o usuário e pergunte se quer pular essa etapa ou informar o token manualmente.

---

## Passo 8 — Criar guia Contrato no ClickUp

Com o `DOC1_ID` retornado no Passo 5, o `DRIVE_CONTRATO_URL` do Passo 6 e o `ZAPSIGN_URL` do Passo 7:

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/onboarding-revops/api.py clickup_contrato "{DOC1_ID}" "{DRIVE_CONTRATO_URL}" "{ZAPSIGN_URL}" "{date_DD/MM/YYYY}"
```

---

## Passo 9 — Criar tarefas de onboarding no ClickUp

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/onboarding-revops/api.py clickup_tarefas "{TAREFAS_LIST_ID}"
```

O script replica a estrutura completa da tarefa mãe de onboarding RevOps:
- **Onboarding RevOps** (mãe, status: backlog)
  - Fase 1 - Boas Vindas (8 subtarefas)
  - Fase 2 - Diagnóstico (10 subtarefas)
  - Fase 3 - Estruturação (3 subtarefas)
  - Fase 4 - Ativação (7 subtarefas)

---

## Passo 10 — Resumo final para o usuário

Apresente um resumo limpo do que foi criado:

```
✅ Onboarding {COMPANY} configurado!

ClickUp
• Pasta: {COMPANY} (Tipo A - Clientes)
• Listas: Anúncios e Tarefas (com colunas configuradas)
• Docs: Docs - {COMPANY} | Reuniões {COMPANY}
• Tarefas: Onboarding RevOps com 4 fases e 28 subtarefas

Google Drive
• Pasta: {COMPANY} com 8 subpastas
• Anúncios: 5 RMs (Prontos / Revisão / Arquivos Brutos)

Contrato
• ClickUp: guia Contrato criada com links
• ZapSign: {status do contrato}

Próximos passos manuais:
• Upload do PDF do contrato na pasta Contrato do Drive
• Verificar modelo de status da lista Anúncios no ClickUp (abrir "Editar status" > selecionar "Anúncios" > "Aplicar alterações")
```

---

## Regras gerais

- Uma etapa por vez. Não pular etapas sem avisar.
- Se qualquer passo falhar, reportar o erro com clareza e sugerir solução antes de continuar.
- Nunca usar travessão (—) em nenhum texto gerado.
- Após criar a lista Anúncios, **sempre** avisar o usuário para verificar o modelo de status na UI do ClickUp (limitação da API — o modelo "Anúncios" precisa ser aplicado manualmente em "Editar status" > dropdown > "Aplicar alterações").
