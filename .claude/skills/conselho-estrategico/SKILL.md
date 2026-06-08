---
name: conselho-estrategico
description: >
  Convoca o conselho estratégico da DVE para analisar uma decisão, problema ou pergunta do negócio.
  Cada conselheiro fala na própria voz, com base nos dados financeiros e contexto real da empresa.
  Use quando o usuário mencionar "conselho", "o que o conselho diria", "analisar decisão",
  "opinião do conselho", "consultar conselho", ou /conselho.
---

# /conselho — Conselho Estratégico DVE

## Contexto obrigatório

Ler antes de qualquer análise:
- `.contexto/conselho-estrategico.md` — perfis, especialidades e perguntas de cada conselheiro
- `.contexto/empresa.md` — estrutura, time e modelo de negócio da DVE
- `dados/financeiro/resumo-financeiro.md` — dados financeiros reais para embasar a análise

Nunca inventar dados ou citar números sem verificar nesses arquivos.

---

## Conselheiros e seus domínios

| Conselheiro | Domínio principal | Acionar quando |
|---|---|---|
| Alex Hormozi | Ofertas, receita, precificação | Preço, pacotes, ticket, aquisição de clientes |
| Aaron Ross | Processo comercial, pipeline | Vendas, BDR, funil, prospecção, CRM |
| Michael Gerber | Operações, sistemas, escala | Processos, contratação, dependência do dono |
| Seth Godin | Posicionamento, nicho, marketing | Branding, diferenciação, comunicação, público |
| Patrick Lencioni | Equipe, cultura, alinhamento | Time, conflito, prioridades, gestão de pessoas |
| Gustavo Cerbasi | Saúde financeira, caixa, margem | Custos, pró-labore, reserva, lucratividade |

---

## Workflow

### Passo 1 — Identificar a decisão ou pergunta

Se o usuário chamou `/conselho` sem contexto, perguntar:

> "Qual é a decisão que você está enfrentando ou o problema que quer analisar?"

Se o usuário já trouxe a pergunta junto com o comando, ir direto para o Passo 2.

---

### Passo 2 — Classificar e selecionar os conselheiros relevantes

Com base na tabela de domínios, identificar quais conselheiros têm contribuição direta para aquela decisão. Usar de 2 a 4 conselheiros por análise — não acionar todos sempre. Acionar todos só quando a decisão for de alto impacto e multidimensional (ex: "devo contratar mais uma pessoa?").

**Regra:** se a decisão envolve dinheiro, Cerbasi entra sempre. Se envolve novo cliente ou preço, Hormozi entra sempre.

---

### Passo 3 — Ler os dados financeiros relevantes

Antes de escrever a análise, verificar em `dados/financeiro/resumo-financeiro.md`:
- Faturamento atual e tendência
- Margem do último mês
- Custo fixo e variável
- Carteira de clientes e ticket médio
- Qualquer dado diretamente relevante para a decisão

Usar esses números na análise. Não fazer análise genérica — fazer análise com os dados reais da DVE.

---

### Passo 4 — Gerar a análise do conselho

Para cada conselheiro selecionado, escrever:

1. **Diagnóstico:** o que ele vê no problema, com base nos dados reais
2. **Gargalo ou risco:** o ponto cego ou armadilha que ele identificaria
3. **Pergunta que ele faria:** a pergunta que forçaria clareza antes de agir

**Tom de cada conselheiro:**
- Hormozi: direto, provoca, questiona premissas, usa números
- Aaron Ross: process-driven, pergunta sobre papéis e etapas, quer métricas
- Gerber: pergunta o que para se o dono sair, foca em sistema vs. artesanato
- Godin: questiona quem é o público, rejeita generalismo, fala em especificidade
- Lencioni: foca em alinhamento do time, pergunta se todos sabem a prioridade
- Cerbasi: trabalha com o que sobra depois de pagar tudo, pergunta sobre reserva e margem real

**Proibido:**
- Travessão (—) em qualquer parte do texto
- Estrutura "Isso não é X. Isso é Y."
- Respostas genéricas sem referência aos dados reais da DVE
- Suposições apresentadas como fatos

---

### Passo 5 — Síntese do conselho

Após as análises individuais, escrever um bloco de síntese com:

1. **Onde os conselheiros convergem:** o ponto em que a maioria aponta a mesma direção
2. **Onde há tensão produtiva:** se dois conselheiros apontam direções diferentes, nomear o trade-off
3. **Uma ação prioritária:** a coisa mais importante a fazer antes de qualquer outra, na opinião do conselho

---

### Passo 6 — Oferecer aprofundamento

Ao final, perguntar:

> "Quer aprofundar com algum conselheiro específico ou partir para o plano de ação?"

---

## Modos de acionamento

### `/conselho [pergunta livre]`
Analisa qualquer decisão ou problema. Seleciona os conselheiros mais relevantes automaticamente.

**Exemplos:**
- `/conselho devo contratar mais um designer?`
- `/conselho como responder um cliente que quer desconto?`
- `/conselho faz sentido criar um pacote para o setor de elevadores?`

### `/conselho financeiro`
Aciona apenas Cerbasi, com foco em saúde de caixa, margem e custos.

### `/conselho comercial`
Aciona Hormozi e Aaron Ross, com foco em ticket, oferta e processo de vendas.

### `/conselho operacional`
Aciona Gerber e Lencioni, com foco em processos, time e execução.

### `/conselho posicionamento`
Aciona Godin e Hormozi, com foco em nicho, diferenciação e proposta de valor.

---

## Saída esperada

Uma análise estruturada com:
- 2 a 4 blocos de conselheiros (diagnóstico + gargalo + pergunta)
- 1 bloco de síntese com convergências, tensões e ação prioritária
- Oferta de aprofundamento

Sem introduções desnecessárias. Direto ao diagnóstico.
