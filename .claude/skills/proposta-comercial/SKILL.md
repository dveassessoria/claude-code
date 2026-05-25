---
name: proposta-comercial
description: >
  Gera uma proposta comercial profissional em HTML para a DVE Assessoria.
  Aplica a identidade visual da DVE (cores, fontes do design-guide.md).
  Use quando o usuário mencionar "proposta", "proposta comercial", "orçamento",
  "fechar contrato" ou pedir um documento de venda para um cliente.
---

# /proposta-comercial — Proposta Comercial DVE

## Dependências

- **Identidade visual:** `marca/design-guide.md`
- **Contexto do negócio:** `.contexto/empresa.md`
- **Tom de voz:** `.contexto/preferencias.md`
- **Briefing do cliente:** `clientes/[nome-cliente]/briefing.md` (se existir)

---

## Workflow

### Passo 1 — Coletar informações

Ler o briefing do cliente se existir na pasta `clientes/`. Se já existir, usar como base e não perguntar o que já está documentado.

Se não tiver briefing ou faltar informação, perguntar apenas o que estiver faltando:

1. "Qual o nome e empresa do cliente?"
2. "Qual o problema ou dor principal que ele relatou?"
3. "Qual oferta você quer propor? (RevOps, MarketingOps, SalesOps ou outra)"
4. "Tem algum contexto específico da reunião que eu deva considerar?"

Não perguntar sobre valor — usar os valores padrão das ofertas abaixo, a menos que o usuário indique algo diferente.

### Passo 2 — Identificar a oferta

Com base no que o cliente precisa, identificar qual oferta faz sentido:

**RevOps (oferta principal)** — R$ 2.500/mês + mídia a partir de R$ 1.500/mês + ferramentas a partir de R$ 300/mês
- Quando o cliente precisa integrar marketing, comercial e CS
- Inclui: estratégia, tráfego pago, criação de anúncios, estruturação comercial, CRM, playbook de vendas, CS/LTV, reunião quinzenal, atendimento diário no WhatsApp

**MarketingOps (downsell)** — R$ 1.500/mês + mídia R$ 1.500/mês + ferramentas a partir de R$ 300/mês
- Quando o cliente precisa de demanda mas não tem budget para o RevOps completo
- Inclui: estratégia de demanda, tráfego pago, criação de anúncios, reunião mensal, atendimento diário no WhatsApp

**SalesOps (produto único)** — R$ 6.000 pagamento único (projeto de 60 dias)
- Quando o problema é o processo comercial, sem necessidade de marketing
- Inclui: estruturação do processo comercial, playbook + scripts, CRM, videoaulas, suporte pós-implementação 30 dias, reuniões quinzenais, atendimento diário no WhatsApp

### Passo 3 — Gerar o HTML

Criar arquivo HTML completo com a identidade visual da DVE.

**Paleta de cores:**
- Fundo principal: `#0F2A33`
- Fundo secundário/cards: `#1E2328`
- Destaque/CTA: `#01FF96`
- Texto: `#F4F3EE`

**Tipografia:**
- Títulos: Montserrat, Bold 700 (Google Fonts fallback)
- Corpo: Plus Jakarta Sans, Regular (Google Fonts fallback)

**Estrutura da proposta:**

1. **Header** — "DVE Assessoria" em texto (Montserrat Bold, cor #01FF96) + data
2. **Destinatário** — "Proposta para [Nome do Cliente] — [Empresa]"
3. **O desafio** — o problema do cliente em 2-3 parágrafos, escrito na perspectiva dele. Usar as dores reais relatadas, não frases genéricas.
4. **A solução** — o que a DVE propõe e por que resolve especificamente o problema deste cliente
5. **O que está incluído** — lista clara dos entregáveis da oferta escolhida
6. **O que não está incluído** — quando relevante (evita conflito depois)
7. **Prazo** — cronograma ou expectativa de início
8. **Investimento** — valor mensal ou único em destaque visual, com contexto de ROI quando possível. Mencionar os casos de sucesso relevantes (MM Medicina 21,5x, Altitude Elevadores 23,5x, Dra. Marina Varela 3,1x)
9. **Próximos passos** — CTA claro: "Para avançar, responda esta proposta com a confirmação e agendaremos o início da implementação."
10. **Sobre a DVE** — 3-4 linhas: pioneiros em RevOps no Brasil, 1,5 anos, 20 clientes ativos, R$ 33k/mês de MRR, crescimento 100% via network.

**Estilo visual:**
- Fundo escuro (#0F2A33), texto claro (#F4F3EE)
- Cards com fundo #1E2328, border-radius 10px
- Valor em destaque: box com borda sutil #01FF96 e o número grande
- Botão CTA: fundo #01FF96, texto #0F2A33, bold
- Layout de uma coluna, responsivo, max-width 700px
- Seções com espaçamento generoso (padding 40px+)

### Passo 4 — Salvar

Salvar em `propostas/proposta-[nome-cliente]-[data].html`

Confirmar o caminho do arquivo salvo e perguntar: "Quer revisar alguma seção antes de enviar?"

---

## Regras de escrita

- Tom: profissional mas humano. Sem formalidade excessiva, sem marketing genérico.
- Nunca usar travessão (—)
- Nunca usar estrutura "Isso não é X. Isso é Y." em nenhuma variação
- Nunca inventar dores que o cliente não mencionou — se não tiver contexto suficiente, usar placeholder visível: `[INSERIR DOR ESPECÍFICA RELATADA NA REUNIÃO]`
- A proposta deve soar como veio de uma pessoa, não de um template
- Valor nunca escondido — apresentar cedo e com contexto de retorno
