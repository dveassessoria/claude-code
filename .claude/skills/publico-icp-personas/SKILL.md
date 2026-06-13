---
name: publico-icp-personas
description: >
  Cria o documento de Público Alvo, ICP e Personas de um cliente da DVE.
  Aplica o framework do Conselho Estratégico: conecta a oferta real do cliente
  à dor específica de cada persona, define ângulo de ataque para cada anúncio
  e orienta a qualificação de leads. Dispara com /publico-icp-personas,
  "criar ICP e personas", "definir personas", "público alvo e personas",
  "fazer ICP", "montar personas do cliente".
---

# /publico-icp-personas — Público, ICP e Personas

## O que essa skill faz

Gera o documento completo de Público, ICP e Personas para um cliente da DVE,
seguindo o framework validado pelo Conselho Estratégico. O documento é feito
para ser usado diretamente pela copywriter na criação de anúncios de tráfego pago.

**Princípios do conselho que guiam cada etapa:**
- **Godin:** nada genérico. Cada persona precisa refletir o que é específico desse cliente, não serve para qualquer concorrente. Se o orçamento for limitado, a skill define uma persona prioritária.
- **Hormozi:** a oferta do cliente precisa aparecer conectada à dor de cada persona. Copywriter não escreve para "quem tem dor", escreve para "quem tem essa dor e pode ser resolvida por essa oferta específica."
- **Aaron Ross:** cada persona precisa de uma primeira pergunta de qualificação para o time comercial saber com quem está falando antes de oferecer qualquer coisa.

---

## Passo 1 — Identificar o cliente e ler o que já existe

Perguntar ou identificar na conversa: qual é o cliente?

Com o nome do cliente, verificar se existem esses arquivos:

```
clientes/[nome-cliente]/base-conhecimento-onboarding.md
clientes/[nome-cliente]/briefing.md
clientes/[nome-cliente]/publico-icp-personas.md  (já existe?)
```

Se o documento de personas já existir, perguntar:
> "Já existe um documento de personas para esse cliente. Quer revisar o existente ou criar do zero?"

---

## Passo 2 — Coletar as informações necessárias

Extrair as informações dos documentos existentes. Perguntar **apenas o que estiver faltando**, agrupando em uma única mensagem.

### Bloco A — Público Alvo
Necessário para preencher os 4 campos:
- Faixa etária
- Gênero
- Localização geográfica (cidades ou regiões onde o cliente atua)
- Tipo de relação com o produto/serviço (síndico, dono de clínica, gestor de TI, etc.)

### Bloco B — ICP
Necessário para definir o cliente ideal:
- Perfil do imóvel, empresa ou contexto ideal (porte, segmento, volume)
- Perfil do decisor (quem assina o contrato)
- Situação atual do ICP (o que ele está vivendo antes de procurar o cliente)
- O que ele valoriza na hora de contratar (não preço — o que realmente pesa)
- Gatilhos que fazem ele buscar ativamente uma solução
- O que **não é** cliente ideal (perfis que não convertem ou têm LTV ruim)

### Bloco C — A Oferta do Cliente
Este bloco é crítico. Sem ele, as personas ficam genéricas e a copy não converte.

Extrair ou perguntar:
- Qual é o produto ou serviço principal?
- O que está incluído no pacote de entrada? (o que o lead recebe antes ou ao fechar)
- Quais são os redutores de risco? (garantia, período grátis, sem fidelidade, sem multa)
- Quais são os diferenciais reais frente aos concorrentes diretos?
- Quais provas existem? (número de clientes, anos no mercado, casos de resultado, depoimentos)

### Bloco D — Personas
Para cada persona identificada:
- Nome, idade, cargo e contexto profissional
- Rotina do dia a dia
- Frustrações específicas com o mercado atual (não genéricas — o que esse mercado especificamente faz de errado)
- Gatilho que faz essa persona entrar em contato

Se o usuário já tiver as personas definidas, usar essas. Se não, sugerir de 2 a 3 personas com base no que foi coletado e confirmar antes de gerar.

---

## Passo 3 — Definir a persona prioritária

Com base no orçamento de mídia paga e nos canais definidos, indicar qual persona deve receber foco nos primeiros anúncios.

Critérios de priorização:
- Maior volume no mercado (mais pessoas nesse perfil)
- Maior dor emocional (mais urgência para agir)
- Melhor presença no canal principal (quem está no Instagram vs. Google)
- Menor fricção para converter (quem chega mais pronto para fechar)

Se o orçamento for inferior a R$ 3.000/mês em mídia, recomendar **uma persona exclusiva** para os primeiros anúncios. Dispersar orçamento baixo entre múltiplas personas dilui o aprendizado e aumenta o CPL.

---

## Passo 4 — Gerar o documento

### Formato obrigatório

```markdown
# Público, ICP e Personas — {NOME DO CLIENTE}
*(Gerado em {data})*

---

## Público Alvo

| Campo | Dados |
|---|---|
| Faixa etária | {faixa} |
| Gênero | {gênero} |
| Localização geográfica | {cidades ou regiões} |
| Tipo de relação com o produto/serviço | {perfis: síndico, dono, gestor, etc.} |

---

## ICP — Cliente Ideal

**{Tipo de empresa/imóvel/contexto ideal}:** {descrição, prioridade de porte}

**Perfil do decisor:** {quem tem poder de contratar}

**Situação atual:** {o que ele está vivendo antes de buscar solução}

**Localização prioritária:** {onde focar}

**Gatilho de busca:** {o que faz ele ir atrás ativamente}

**O que valoriza:** {o que pesa na decisão, além de preço}

**O que não é cliente ideal:** {perfis que não convertem}

---

## A Oferta do {NOME DO CLIENTE} — Referência para a copywriter

Antes de escrever qualquer anúncio, entender o pacote de entrada do cliente.
Esses diferenciais precisam aparecer nos anúncios conectados à dor de cada persona,
não listados de forma genérica.

**O que está incluído:**
- {diferencial 1}
- {diferencial 2}
- {redutor de risco: garantia, mês grátis, sem fidelidade, etc.}

**Provas disponíveis:**
- {número de clientes, anos de mercado, casos de resultado, depoimentos}

---

## Personas

### Persona prioritária para os primeiros anúncios: {Nome da Persona Prioritária}

{Justificativa em 1-2 frases: por que essa é a primeira, qual é o critério de priorização}
{Se orçamento baixo: instrução de concentrar 100% nessa persona até validar CPL}

---

### Persona {N}: {Nome do Perfil}

**Nome fictício:** {nome}
**Idade:** {idade}
**Cargo/Perfil:** {função e contexto}

**Rotina:**
{2-3 frases sobre o dia a dia profissional e como o problema aparece na rotina}

**Frustrações com o mercado atual:**
- {frustração específica desse mercado, não genérica}
- {frustração 2}
- {frustração 3}

**Como a oferta do {CLIENTE} resolve a dor dela/dele:**
- {diferencial X → resolve a frustração Y especificamente}
- {diferencial Z → resolve o medo W}

**Ângulo de ataque do anúncio:**
{1 parágrafo: qual é a dor central, qual emoção ativar, por onde o anúncio deve entrar}

Exemplo de ângulo: *"{headline ou gancho de exemplo direto para essa persona}"*

**Gatilho para entrar em contato:**
{o que acontece que faz essa persona buscar o cliente agora, não amanhã}

**Como esse lead chega e como qualificá-lo:**
{como ele se apresenta no WhatsApp, e-mail ou formulário}
Pergunta de qualificação: "{primeira pergunta para identificar se é lead válido}"

---
```

Repetir o bloco de Persona para cada uma definida.

---

## Passo 5 — Salvar o documento

Salvar em:
```
clientes/[nome-cliente]/publico-icp-personas.md
```

Se já existir um arquivo anterior, salvar como:
```
clientes/[nome-cliente]/publico-icp-personas-v{N}.md
```
onde N é a próxima versão disponível.

---

## Passo 6 — Verificar se precisa atualizar o ClickUp

O onboarding RevOps cria automaticamente uma guia "ICP e Personas" no Doc do cliente no ClickUp.

Perguntar ao usuário:
> "Quer que eu atualize também a guia de ICP e Personas no ClickUp do cliente?"

Se sim, usar o MCP do ClickUp para localizar o Doc do cliente e atualizar a guia correspondente com o conteúdo gerado.

---

## Regras de escrita

- Nunca usar travessão (—) em nenhuma parte do documento
- Nenhuma persona pode ser genérica o suficiente para servir a qualquer concorrente do cliente
- O bloco "Como a oferta resolve a dor" deve conectar diferenciais reais do cliente a medos específicos dessa persona — nunca benefícios genéricos
- O "Ângulo de ataque" deve gerar pelo menos um exemplo concreto de headline ou gancho
- A pergunta de qualificação deve ser de resposta rápida (sim/não, número, tipo) — não pode ser uma pergunta aberta que demora para responder
- Se não tiver informação suficiente para escrever um bloco com especificidade real, perguntar ao usuário antes de preencher com suposições

---

## Quando usar essa skill

- Novos clientes: durante a fase de diagnóstico do RevOps (logo após o onboarding)
- Clientes antigos: quando o cliente mudar de nicho, produto ou público
- Antes de criar qualquer copy de anúncio para um cliente novo
- Quando a copywriter reportar que os anúncios estão atraindo leads desqualificados
