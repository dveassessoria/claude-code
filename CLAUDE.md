# DVE Assessoria — Claude Code OS

## O que é esse workspace

Workspace de operações da DVE Assessoria. Aqui ficam todos os clientes, entregas, propostas e materiais de produção da agência.

**Estrutura de pastas:**
- `.contexto/` — memória do sistema (não apagar)
- `clientes/` — um subdiretório por cliente com briefing e histórico
- `briefings/` — briefings recebidos de clientes
- `propostas/` — propostas em andamento e enviadas
- `conteudo/` — produção de conteúdo (copy, roteiros, posts)
- `dados/` — arquivos para análise (CSV, PDF, relatórios)
- `marca/` — identidade visual e guia de design
- `templates/skills/` — templates de skills prontos para personalizar com /mapear
- `templates/ferramentas/catalogo.md` — APIs e ferramentas disponíveis para usar em skills
- `tarefas.md` — lista de tarefas corrente

## Sobre o negócio

A DVE Assessoria é uma agência de marketing digital que oferece gestão de tráfego pago (Meta Ads e Google Ads), produção de copy, criação de funis de marketing e playbooks comerciais e operacionais.
Atendemos clientes externos e também desenvolvemos o crescimento interno da própria DVE.

## O que mais produzimos aqui

- Copy para anúncios, landing pages, WhatsApp e atendimento comercial
- Gestão de tráfego pago (Meta Ads e Google Ads)
- Registros e transcrições de reuniões com clientes
- Benchmark e pesquisa de mercado
- Funis de marketing
- Playbooks de vendas, comercial e gestão
- Propostas comerciais
- Roteiros de vídeo para conteúdo da DVE e clientes

## Time

- **Danilo Santana** — Diretor Operacional e sócio-fundador (50%). Lidera operações, define estratégias, gerencia tráfego pago, treina o time e mantém a base de conhecimento.
- **Rafael Machado** — Diretor Comercial e sócio-fundador (50%). Responsável pelo comercial, reuniões de vendas e treinamento da pré-vendas.
- **Cristiane** — BDR (pré-vendas). Prospecção, qualificação de leads e agendamento de reuniões.
- **Davi Vinicius** — Gestor de Projetos e Customer Success. Gestão de clientes, relatórios e acompanhamento de resultados.
- **Ariana** — Copywriter e Social Media. Copy, conteúdo, planejamento editorial e documentos estratégicos.
- **Wesley** — Designer e Webdesigner. Identidade visual, landing pages, sites e peças gráficas.

## Tom de voz

Escrever de forma humanizada, natural e fluida. Textos que criam conexão real com a audiência.
Roteiros de vídeo devem soar como diálogo genuíno — naturais para leitura no teleprompter, sem artificialidade.

Evitar: textos genéricos, superficiais, robotizados ou sem profundidade. Frases vazias, introduções desnecessárias, entusiasmo exagerado típico de IA.

## Regras do sistema

- Propostas salvar em `propostas/`
- Clientes novos: criar pasta em `clientes/[nome-cliente]/` com `briefing.md` dentro
- Conteúdo produzido salvar em `conteudo/`
- Arquivos para análise jogar em `dados/`

## Ferramentas conectadas

- [ ] Gmail
- [ ] Google Calendar
- [ ] Google Drive
- [ ] Meta Ads (meta-ads-ratos)
- [ ] Google Ads (google-ads-ratos)

*(Marcar conforme for instalando os MCPs)*

---

## Contexto do negócio

No início de toda conversa, ler os seguintes arquivos (se existirem e estiverem configurados):

1. `.contexto/empresa.md` — quem é o usuário, o que faz, como funciona o negócio
2. `.contexto/preferencias.md` — tom de voz, estilo de escrita, o que evitar
3. `.contexto/estrategia.md` — foco atual, prioridades, o que pode esperar

Usar essas informações como base pra qualquer resposta ou decisão. Ao sugerir prioridades, formatos ou abordagens, considerar o foco atual descrito em `estrategia.md`.

Para qualquer tarefa visual (carrossel, proposta, slide, landing page), consultar `marca/design-guide.md` como referência de estilo.

Não é necessário listar o que foi lido nem confirmar a leitura. Apenas usar o contexto naturalmente.

---

## Fluxo de trabalho

Antes de executar qualquer tarefa, verificar se existe uma skill relevante em `.claude/skills/` ou `.claude/commands/`.
Se encontrar, seguir as instruções da skill.
Se não encontrar, executar a tarefa normalmente.

Ao concluir uma tarefa que não tinha skill mas parece repetível (o usuário provavelmente vai pedir de novo no futuro), perguntar:

> "Isso pode virar uma skill pra próxima vez. Quer que eu crie?"

Não perguntar pra tarefas pontuais ou perguntas simples. Só quando o padrão de repetição for claro.

---

## Aprender com correções

Quando o usuário corrigir algo, melhorar uma resposta ou dar uma instrução que parece permanente (frases como "na verdade é assim", "não faça mais isso", "prefiro assim", "sempre que...", "evita...", "da próxima vez..."), perguntar:

> "Quer que eu salve isso pra não precisar repetir?"

Se sim, identificar onde faz mais sentido salvar:

- **Sobre o negócio** → `.contexto/empresa.md`
- **Sobre preferências e estilo** → `.contexto/preferencias.md`
- **Sobre prioridades e foco atual** → `.contexto/estrategia.md`
- **Regra de comportamento nessa pasta** → `CLAUDE.md`

Salvar com uma linha nova clara, sem reformatar o arquivo inteiro. Confirmar o que foi salvo mostrando a linha adicionada.

---

## Manter contexto atualizado

Ao terminar uma tarefa que mudou algo relevante no projeto (novo cliente, nova skill, mudança de foco, novo processo, ferramenta instalada, estrutura de pastas alterada), perguntar:

> "Isso mudou algo no teu contexto. Quer que eu atualize os arquivos de memória?"

Se sim, identificar o que precisa atualizar:

- **Novo cliente, serviço, ferramenta, equipe** → `.contexto/empresa.md`
- **Mudança de prioridade ou foco** → `.contexto/estrategia.md`
- **Correção de tom ou estilo** → `.contexto/preferencias.md`
- **Nova pasta, regra de organização, skill criada** → `CLAUDE.md`
- **Mudança visual (cores, fontes, logo)** → `marca/design-guide.md`

**Dica:** se não sabe se algo mudou, rode `/atualizar` pra uma varredura completa.

---

## Criação de skills

Quando o usuário pedir pra criar uma nova skill:

1. Verificar se existe um template relevante em `templates/skills/`. Se existir, usar como base e adaptar pro contexto do usuário
2. Perguntar: "Essa skill é específica pra esse projeto ou vai ser útil em qualquer projeto?"
   - Específica desse negócio → salvar em `.claude/skills/nome-da-skill/SKILL.md` (local)
   - Útil em qualquer projeto → salvar em `~/.claude/skills/nome-da-skill/SKILL.md` (global)
3. Ler `.contexto/empresa.md` e `.contexto/preferencias.md` pra calibrar o conteúdo da skill ao contexto do negócio
4. Se a skill precisar de arquivos de apoio (templates, referências, exemplos), criar dentro da pasta da skill
5. Seguir o fluxo da skill-creator nativa do Claude Code
