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
6. Gera mensagem de WhatsApp com os próximos passos para enviar ao grupo do cliente

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

O script replica a estrutura completa abaixo. Criar em ordem (pai antes dos filhos). Todas as tarefas com `status: backlog`.

**Hierarquia completa:**

```
Onboarding RevOps  [tarefa mãe]

  Fase 1 - Boas Vindas
  DESC: Alinhar expectativas, organizar o ambiente e garantir todos os acessos necessários para execução.

    Enviar mensagem de boas vindas no grupo de WhatsApp
    DESC: Todos os membros do squad devem mandar uma mensagem de boas vindas no WhatsApp se apresentando de forma profissional a equipe do novo cliente.
    Definição de pronto: Todos os membros do squad enviaram a mensagem no grupo.
    Responsável: Todos os membros do squad

    Realizar reunião de onboarding com o cliente
    DESC: Fazer a reunião de onboarding para alinhar objetivos, escopo, expectativas e forma de trabalho do projeto RevOps. Devemos gravar essa reunião com o TLDV e seguir o escopo do documento da reunião de onboarding.
    Definição de pronto: Reunião realizada e principais decisões registradas no documento de onboarding.
    Responsável: Customer Success

    Criar documento de onboarding do cliente
    DESC: Pegar gravação no TLDV e criar documento de onboarding com informações estratégicas, acessos, decisões e visão geral do projeto. Esse documento deve ser criado na parte "Documentos" que fica dentro da pasta do cliente no ClickUp.
    Definição de pronto: Documento criado e salvo no Google Drive e ClickUp do cliente.
    Responsável: Customer Success

    Criar ClickUp
    DESC: Criar pasta do cliente dentro do ClickUp com as seguintes sessões: Anúncios (lista), Tarefas (lista), Documentos (docs).
    Definição de pronto: ClickUp criado com as 3 sessões com os status da tarefa configurados corretamente.
    Responsável: Customer Success

    Criar Google Drive
    DESC: Criar e organizar as pastas do projeto do cliente para centralizar todos os arquivos no Google Drive. Pastas: Anúncios, Fotos e Vídeos, Identidade Visual, Planilhas, Marketing, Comercial, CS, Planejamento RevOps.
    Definição de pronto: Google Drive criado com estrutura padrão e compartilhado no grupo do cliente.
    Responsável: Customer Success

    Coletar Acessos Necessários
    DESC: Solicitar e validar todos os acessos essenciais para execução do projeto: Acesso Wordpress, Domínio, Hospedagem, CRM, Playbook de Vendas, Meta Ads, Google Ads.
    Definição de pronto: Todos os acessos recebidos, testados e funcionando.
    Responsável: Customer Success

    Solicitar Fotos, Vídeos, ID Visual e outros
    DESC: Precisamos que o cliente faça o upload de fotos, vídeos, ID Visual (Logo, PDF, Tipografia, etc) e outros materiais relevantes para o projeto como planilhas e documentos.
    Solicitar: Fotos do Serviço/Produto, Vídeos do Serviço/Produto, Identidade Visual (Logo, PDF, Tipografia, Paleta de Cor), Planilhas, Documentos, Proposta Comercial.
    Definição de pronto: Cliente fez o upload de todos os materiais solicitados na pasta correta do Drive.
    Responsável: Customer Success

    Definir as Reuniões do Google Agenda
    DESC: Alinhar com o cliente qual será a frequência, dia e horários das nossas reuniões quinzenais de alinhamento.
    Definição de pronto: Reuniões criadas no Google Agenda (da DVE), adicionado o e-mail de todos os participantes e comunicado no grupo.
    Responsável: Customer Success

  Fase 2 - Diagnóstico

    Realizar Benchmark
    DESC: Analisar concorrentes diretos e referências do mercado para identificar padrões e oportunidades. Realizar pesquisa com pelo menos 5 empresas do segmento analisando: canais de aquisição, funil de marketing, anúncios, oferta escalada, diferencial competitivo, posicionamento, provas sociais, processo comercial e follow up.
    Definição de pronto: Benchmark documentado no Google Docs, adicionado ao Drive, link no ClickUp, aprovado internamente e pelo cliente.
    Responsável: Analista

    Analisar Campanhas de Tráfego
    DESC: Analisar o histórico das campanhas de tráfego pago e mapear os criativos e públicos vencedores.
    Definição de pronto: Análise do desempenho das campanhas documentado em Planilha e/ou Google Docs.
    Responsável: Danilo

    Analisar Presença Digital
    DESC: Analisar como o cliente se posiciona hoje no digital em todos os canais ativos, mapeando gargalos, alavancas de crescimento e próximos passos.
    Definição de pronto: Análise registrada em Google Docs com pontos fortes, pontos fracos e oportunidades.
    Responsável: Davi

    Analisar e Criar Oferta
    DESC: Analisar se a oferta do cliente realmente é boa. Ver a gravação no TLDV na parte que fala sobre a oferta e também o site.
    Definição de pronto: Oferta atual analisada e documentada com ajustes sugeridos.
    Responsável: Danilo

    Analisar diferencial competitivo
    DESC: Ver a reunião de onboarding no TLDV e analisar a parte que o cliente fala sobre o diferencial competitivo. Verificar se o diferencial realmente é relevante para o mercado e ICP. Caso não for relevante, comunicar com o cliente para criar um.
    Definição de pronto: Diferencial competitivo analisado e documentado.
    Responsável: Danilo

    Analisar e Criar ICP e Personas
    DESC: Definir o perfil de cliente ideal e as personas que o funil deve atrair.
    Definição de pronto: ICP e personas documentados e aprovados.
    Responsável: Líder de Receita

    Analisar e Mapear Jornada de Compra
    DESC: Mapear o caminho do cliente desde o primeiro contato até a venda.
    Definição de pronto: Jornada documentada com etapas claras.
    Responsável: Líder de Receita

    Analisar e Definir Funil de Captação
    DESC: Definir a estrutura do funil (topo, meio e fundo) alinhada ao ICP e à jornada de compra do cliente.
    Definição de pronto: Funil analisado e documentado.
    Responsável: Líder de Receita

    Criar Planejamento RevOps
    DESC: Consolidar todas as decisões da fase de diagnóstico em um plano único de ação.
    Definição de pronto: Planejamento RevOps documentado e validado internamente.
    Responsável: Líder de Receita

    Realizar Reunião de Apresentação do Planejamento
    DESC: Apresentar o diagnóstico e alinhar expectativas antes da implementação.
    Definição de pronto: Planejamento aprovado pelo cliente.
    Responsável: Líder de Receita

  Fase 3 - Estruturação

    Marketing  [sub-pai]

      Configurar tracking e eventos
      DESC: Configurar todas as ferramentas de tracking necessárias para mensurar leads, conversões e desempenho das campanhas.
      Definição de pronto: Eventos configurados, testados e disparando corretamente.
      Responsável: Gestor de Tráfego

      Configurar contas de anúncios
      DESC: Configurar contas de anúncios que serão usadas na operação.
      Definição de pronto: Conta(s) configurada(s) e pronta(s) para criação de campanhas.
      Responsável: Gestor de Tráfego

      Criar planilha de tráfego
      DESC: Criar planilha para controle de investimentos, métricas e decisões de tráfego.
      Definição de pronto: Planilha criada, estruturada e salva no Drive do cliente.
      Responsável: Gestor de Tráfego

      Criar planilha de leads - Landing Page
      DESC: Criar planilha para registrar todos os leads cadastrados na Landing Page.
      Definição de pronto: Planilha criada e integrada ao Wordpress.
      Responsável: Webdesigner

      Escrever copy da landing page
      DESC: Escrever toda a copy da landing page com base no ICP, oferta e diferencial competitivo definidos.
      Definição de pronto: Copy finalizada, revisada e aprovada internamente.
      Responsável: Copywriter

      Criar design da landing page
      DESC: Criar o design visual da landing page seguindo o wireframe e a identidade do cliente.
      Checklist: Design responsivo (desktop/mobile), identidade visual respeitada, CTA destacado visualmente, layout focado em conversão.
      Definição de pronto: Design final aprovado internamente.

      Implementar Landing Page no Wordpress

      Integrar landing page ao tracking e fluxo de leads

      Revisar landing page antes da ativação
      DESC: Revisão final da landing page para evitar erros antes de iniciar campanhas.
      Definição de pronto: Landing page revisada e liberada para tráfego.
      Responsável: Líder de Receita

      Definir estratégia de campanhas de tráfego

      Criar Copy | RM 01

    Comercial  [sub-pai]

      Definir processos comerciais

      Implementar CRM

      Integrar leads ao CRM

      Criar playbook de vendas

      Criar Copy PDF Comercial

      Criar Design PDF Comercial

      Criar Planilha RevOps

      Testar Processo Comercial antes da ativação

    Sucesso do Cliente  [sub-pai]

      Definir modelo de acompanhamento do cliente

      Definir métricas de sucesso do cliente

      Criar pesquisa de satisfação / NPS

      Definir momentos de aplicação da pesquisa

      Criar rotina de feedback com o cliente

      Definir processo de tratamento de insatisfação

      Criar registro de histórico do cliente

      Validar estrutura de CS antes da ativação

  Fase 4 - Ativação

    Subir Campanhas de Tráfego

    Validar Jornada de Compra

    Analisar métricas iniciais da operação

    Brainstorm interno após ativação

    Definir rotina de acompanhamento recorrente

    Formalizar encerramento do onboarding

    Registrar lições aprendidas do onboarding
```

**Importante sobre níveis:** A Fase 3 tem 3 camadas: Onboarding RevOps > Fase 3 - Estruturação > Marketing/Comercial/CS > subtarefas de cada área. Criar cada nível com o `parent` apontando para o ID do pai imediato criado na chamada anterior.

---

## Passo 10 — Gerar mensagem de WhatsApp para o grupo do cliente

Com base nas informações do documento de onboarding (acessos necessários, data/hora da próxima reunião, próximos passos do cliente), gere a mensagem de boas-vindas e orientação para enviar no grupo do WhatsApp.

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
• Tarefas: Onboarding RevOps com 4 fases (56 subtarefas no total)

Google Drive
• Pasta: {COMPANY} com 8 subpastas
• Anúncios: 5 RMs (Prontos / Revisão / Arquivos Brutos)

Contrato
• ClickUp: guia Contrato criada com links
• ZapSign: {status do contrato}

Próximos passos manuais:
• Upload do PDF do contrato na pasta Contrato do Drive
• Verificar modelo de status da lista Anúncios no ClickUp (abrir "Editar status" > selecionar "Anúncios" > "Aplicar alterações")
• Enviar a mensagem de WhatsApp acima no grupo do cliente
```

---

## Regras gerais

- Uma etapa por vez. Não pular etapas sem avisar.
- Se qualquer passo falhar, reportar o erro com clareza e sugerir solução antes de continuar.
- Nunca usar travessão (—) em nenhum texto gerado.
- Após criar a lista Anúncios, **sempre** avisar o usuário para verificar o modelo de status na UI do ClickUp (limitação da API — o modelo "Anúncios" precisa ser aplicado manualmente em "Editar status" > dropdown > "Aplicar alterações").
