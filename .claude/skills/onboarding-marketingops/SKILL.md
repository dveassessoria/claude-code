---
name: onboarding-marketingops
description: Executa o onboarding completo de um novo cliente de MarketingOps (a oferta downsell da DVE, sem CRM/estruturação comercial completa/CS). Busca a reunião de onboarding no TLDV, gera o documento de base de conhecimento, cria toda a estrutura no ClickUp (pasta, listas, docs, tarefas) e no Google Drive. Dispara com /onboarding-marketingops, "onboarding MarketingOps", "novo cliente MarketingOps", "configurar cliente MarketingOps".
---

## O que essa skill faz

Processo completo de onboarding de um novo cliente de MarketingOps (oferta downsell da DVE, indicada quando o cliente não tem budget para o RevOps completo):
1. Busca a reunião de onboarding no TLDV
2. Gera documento de base de conhecimento a partir da transcrição
3. Cria estrutura completa no ClickUp (pasta, listas Anúncios e Tarefas, docs, tarefas de onboarding)
4. Cria estrutura completa no Google Drive (pasta do cliente com subpastas)
5. Busca o contrato no ZapSign e cria guia no ClickUp com os links
6. Gera mensagem de WhatsApp com os próximos passos para enviar ao grupo do cliente

**Antes de rodar esta skill, confirmar que o serviço vendido é mesmo MarketingOps.** Se for RevOps, usar a skill `onboarding-revops`. As duas divergem nos entregáveis e na estrutura de tarefas (MarketingOps não inclui CRM, estruturação de processo comercial completo, nem a fase de Sucesso do Cliente/LTV). Ver `.contexto/empresa.md` para a lista de entregáveis de cada oferta.

**Script helper:** `.claude/skills/onboarding-marketingops/api.py`
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

Com a transcrição completa, gere o documento de onboarding. Use a habilidade de um CS senior especialista em documentar reuniões de onboarding de MarketingOps.

### Regras de geração

- Extraia APENAS o que foi explicitamente dito na reunião. Nunca invente informações.
- Se a transcrição estiver incompleta, avise antes de continuar.
- Tom direto e profissional. É base de conhecimento interna.
- Nunca usar travessão (—) em nenhuma parte do documento.

### Formato obrigatório

```markdown
# Base de Conhecimento — {COMPANY}

**Data do onboarding:** {date}
**Serviço contratado:** MarketingOps
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
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/onboarding-marketingops/api.py clickup_setup "{COMPANY}" "{ONBOARDING_CONTENT_FILE}" "{date_DD/MM/YYYY}" "{TLDV_MEETING_URL}"
```

O script faz tudo em sequência (9 etapas internas, ~25–30s no total):
1. Cria a pasta do cliente no Space "Tipo A - Clientes"
2. Cria lista Anúncios com `override_statuses: true` + statuses corretos
3. Cria lista Tarefas com statuses corretos
4. Cria view "Lista" com 5 colunas em ambas as listas
5. Cria Doc "Docs - {COMPANY}" com 6 guias (Onboarding com conteúdo, Acessos, Entregáveis com os 8 entregáveis de MarketingOps, Benchmark, Tráfego Pago, ICP e Personas)
6. Cria Doc "Reuniões {COMPANY}" com hierarquia Reuniões > Ano > Mês > Data (conteúdo do onboarding)
7. Cria toda a hierarquia de 47 tarefas de onboarding na lista Tarefas (com 0.3s de intervalo entre chamadas para respeitar o rate limit do ClickUp)

Retorna JSON com: `folder_id`, `anuncios_list_id`, `tarefas_list_id`, `doc1_id`, `doc2_id`, `mae_task_id`.

---

## Passo 6 — Criar estrutura no Google Drive

O Google Drive usa o MCP `mcp__claude_ai_Google_Drive__create_file` com autenticação OAuth da conta DVE. Não pode rodar em script Python independente.

Execute via MCP na seguinte ordem:

**6a.** Buscar a pasta pai "1. Clientes":
```
mcp__claude_ai_Google_Drive__search_files
query: "name = '1. Clientes'"
```

**6b.** Criar a pasta raiz do cliente:
```
mcp__claude_ai_Google_Drive__create_file
name: "{COMPANY}"
mimeType: application/vnd.google-apps.folder
parents: ["{ID_1_CLIENTES}"]
```

**6c.** Criar as 8 subpastas dentro da pasta do cliente (em paralelo):
- Anúncios
- Documentos
- Comercial
- Identidade Visual
- Fotos e Vídeos
- Listas de Clientes
- Planilhas
- Contrato

**6d.** Criar dentro de Anúncios as pastas RM 01, RM 02, RM 03, RM 04, RM 05.

**6e.** Dentro de cada RM, criar: Prontos, Revisão, Arquivos Brutos.

Guardar:
- `DRIVE_FOLDER_URL` = link da pasta raiz do cliente
- `DRIVE_CONTRATO_URL` = link da pasta Contrato
- `DRIVE_FOTOS_URL` = link da pasta Fotos e Vídeos (usar na mensagem de WhatsApp)

---

## Passo 7 — Buscar contrato no ZapSign

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/onboarding-marketingops/api.py zapsign_find "{COMPANY}"
```

Busca o contrato do cliente no ZapSign varrendo todas as páginas. Retorna JSON com `name`, `token`, `status` e `zapsign_url` (link permanente).

Se não encontrar, informe o usuário e pergunte se quer pular essa etapa ou informar o token manualmente.

---

## Passo 8 — Criar guia Contrato no ClickUp

Com o `DOC1_ID` retornado no Passo 5, o `DRIVE_CONTRATO_URL` do Passo 6 e o `ZAPSIGN_URL` do Passo 7:

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/onboarding-marketingops/api.py clickup_contrato "{DOC1_ID}" "{DRIVE_CONTRATO_URL}" "{ZAPSIGN_URL}" "{date_DD/MM/YYYY}"
```

---

## Passo 9 — Tarefas (criadas automaticamente no Passo 5)

As tarefas são criadas automaticamente pelo `clickup_setup`. Este passo existe apenas como **fallback**: se as tarefas falharem no meio do processo ou precisarem ser recriadas em uma lista existente, execute:

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 .claude/skills/onboarding-marketingops/api.py clickup_tarefas "{TAREFAS_LIST_ID}"
```

O script cria a estrutura completa abaixo. Todas as tarefas com `status: backlog`.

**Hierarquia completa (47 tarefas):**

```
Onboarding MarketingOps  [tarefa mãe]

  Fase 1 - Boas Vindas
    Enviar mensagem de boas vindas no grupo de WhatsApp
    Realizar reunião de onboarding com o cliente
    Criar documento de onboarding do cliente
    Criar ClickUp
    Criar Google Drive
    Coletar Acessos Necessários
    Solicitar Fotos, Vídeos, ID Visual e outros
    Definir as Reuniões do Google Agenda

  Fase 2 - Diagnóstico
    Realizar Benchmark
    Analisar Campanhas de Tráfego
    Analisar Presença Digital
    Analisar e Criar Oferta
    Analisar diferencial competitivo
    Analisar e Criar ICP e Personas
    Analisar e Mapear Jornada de Compra
    Analisar e Definir Funil de Captação
    Criar Planejamento MarketingOps
    Realizar Reunião de Apresentação do Planejamento

  Fase 3 - Estruturação
    Marketing  [sub-pai]
      Configurar tracking e eventos
      Configurar contas de anúncios
      Criar planilha de tráfego
      Criar planilha de leads - Landing Page
      Escrever copy da landing page
      Criar design da landing page
      Implementar Landing Page no Wordpress
      Integrar landing page ao tracking e fluxo de leads
      Revisar landing page antes da ativação
      Definir estratégia de campanhas de tráfego
      Criar Copy | RM 01

    Comercial  [sub-pai]
      Criar playbook de vendas
      Criar Copy PDF Comercial
      Criar Design PDF Comercial
      Criar Planilha de Acompanhamento

  Fase 4 - Ativação
    Subir Campanhas de Tráfego
    Validar Jornada de Compra
    Analisar métricas iniciais da operação
    Brainstorm interno após ativação
    Definir rotina de acompanhamento recorrente
    Formalizar encerramento do onboarding
    Registrar lições aprendidas do onboarding
```

**O que NÃO entra (exclusivo do RevOps, ver skill `onboarding-revops`):**
- Fase 3 > Comercial: "Definir processos comerciais", "Implementar CRM", "Integrar leads ao CRM", "Testar Processo Comercial antes da ativação" (MarketingOps não estrutura o processo comercial completo nem implementa CRM)
- Fase 3 > "Sucesso do Cliente" (fase inteira): MarketingOps não inclui estratégia de CS/LTV

**Importante sobre níveis:** A Fase 3 tem 3 camadas: Onboarding MarketingOps > Fase 3 - Estruturação > Marketing/Comercial > subtarefas de cada área. Criar cada nível com o `parent` apontando para o ID do pai imediato criado na chamada anterior.

---

## Passo 10 — Gerar resumo de "Próximos Passos" (slide + mensagem de WhatsApp)

O resumo de próximos passos existe em duas versões com o mesmo conteúdo: uma para o slide de encerramento da apresentação de onboarding (template em `conteudo/onboarding-marketing-ops-slides.docx`) e uma para a mensagem de WhatsApp do grupo do cliente. Gerar as duas.

### 10a. Conteúdo dos dois blocos de cards

**Bloco "Próximos Passos"** (7 cards, ordem fixa). Os itens 1, 2 e 3 vêm do que foi combinado na reunião do cliente (data real, checklist real). Os itens 4, 6 e 7 são o SLA operacional padrão da DVE para MarketingOps e **sempre entram, mesmo que não tenham sido citados na reunião daquele cliente específico**:

1. Agendamento da Reunião para Compartilhar os Acessos — {data e hora combinada com o cliente}
2. Verificar Checklist que será enviado no Grupo (fotos, logo, senhas) — {ajustar itens reais do checklist desse cliente}
3. Criação do Documento Base do Projeto
4. Revisão e Aprovação do Documento (72 horas) — **padrão fixo**
5. Ativação das Campanhas
6. Reunião de Kick-off (apresentamos tudo antes de ativar) — **padrão fixo**
7. Campanhas no Ar (7 dias úteis após compartilhamento dos acessos e materiais) — **padrão fixo**

**Bloco "O que precisamos de você"** (cards variáveis conforme o que o cliente já tem ou não). Base fixa, ajustar por cliente:

- Acesso ao Meta Business Manager
- Acesso ao Google Ads
- Acesso ao site, domínio e hospedagem (só incluir se o cliente não tiver site ou for criar um novo)
- Logo em alta resolução (PNG ou SVG)
- Fotos reais de instalações, equipe e escritório
- Depoimentos de clientes (texto ou vídeo), se houver
- Meta de leads mensais (validar orçamento) — usar o valor de investimento e meta de leads combinados na reunião

**Antes de preencher os dois blocos, sempre conferir a transcrição da reunião do cliente** para os itens 1, 2, 3 e o bloco "O que precisamos de você" — nunca inventar datas, valores ou acessos que não foram ditos. Os itens marcados como "padrão fixo" acima não precisam de confirmação na transcrição.

Ver `project_marketingops_sla_padrao` na memória para o racional desse SLA.

### 10b. Mensagem de WhatsApp para o grupo do cliente

Com base nos dois blocos acima, gere a mensagem de boas-vindas e orientação para enviar no grupo do WhatsApp.

### Regras da mensagem

- Tom humano, direto e profissional. Sem formalidade excessiva.
- Saudação baseada no horário atual (BRT): 05h–11h59 = "Bom dia", 12h–17h59 = "Boa tarde", 18h–04h59 = "Boa noite"
- Nunca usar travessão (—).
- Listar apenas os acessos que o cliente precisa providenciar (não os que a DVE vai configurar).
- Mencionar o Google Drive para envio de fotos e vídeos.
- Confirmar data e horário da próxima reunião.
- **Exibir a mensagem dentro de um bloco de código** (``` ```) para que o botão de copiar apareça.

### Formato obrigatório

```
{Bom dia/Boa tarde/Boa noite}, {nome do contato principal}! Tudo bem?

Ficamos muito felizes em dar início ao trabalho com a {COMPANY}. {data_reunião} às {hora_reunião} faremos a reunião técnica para configurar tudo. Para aproveitar ao máximo o tempo da reunião, precisamos que vocês cheguem preparados com alguns acessos.

*O que reunir até {data_reunião}:*

{lista numerada dos acessos que o cliente precisa providenciar, baseada na seção "Acessos necessários" do documento de onboarding}

Além disso, se possível, vão separando fotos e vídeos da empresa, da equipe e dos serviços. Já criamos uma pasta no Google Drive para vocês enviarem esses materiais:
{DRIVE_FOTOS_URL}

{se houver outros próximos passos do cliente no documento de onboarding, incluir aqui}

Qualquer dúvida, estou à disposição aqui no grupo. Até {data_reunião}!
```

---

## Passo 11 — Resumo final para o usuário

Apresente um resumo limpo do que foi criado:

```
✅ Onboarding {COMPANY} configurado!

ClickUp
• Pasta: {COMPANY} (Tipo A - Clientes)
• Listas: Anúncios e Tarefas (com colunas configuradas)
• Docs: Docs - {COMPANY} | Reuniões {COMPANY}
• Tarefas: Onboarding MarketingOps com 4 fases (47 subtarefas no total)

Google Drive
• Pasta: {COMPANY} com 8 subpastas
• Anúncios: 5 RMs (Prontos / Revisão / Arquivos Brutos)

Contrato
• ClickUp: guia Contrato criada com links
• ZapSign: {status do contrato}

Próximos passos manuais:
• Upload do PDF do contrato na pasta Contrato do Drive
• Verificar modelo de status da lista Anúncios no ClickUp (abrir "Editar status" > selecionar "Anúncios" > "Aplicar alterações")
• Rodar a skill docs-base-cliente após coletar Instagram/GMN/Site para gerar o entregável "Analisar Presença Digital" da Fase 2
• Enviar a mensagem de WhatsApp acima no grupo do cliente
```

---

## Regras gerais

- Uma etapa por vez. Não pular etapas sem avisar.
- Se qualquer passo falhar, reportar o erro com clareza e sugerir solução antes de continuar.
- Nunca usar travessão (—) em nenhum texto gerado.
- Após criar a lista Anúncios, **sempre** avisar o usuário para verificar o modelo de status na UI do ClickUp (limitação da API — o modelo "Anúncios" precisa ser aplicado manualmente em "Editar status" > dropdown > "Aplicar alterações").
- Depois do onboarding, a skill `docs-base-cliente` é o próximo passo natural para gerar o entregável de diagnóstico de presença digital.
