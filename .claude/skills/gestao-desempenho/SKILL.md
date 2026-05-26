---
name: gestao-desempenho
description: >
  Conduz um diagnóstico estruturado de desempenho de colaborador e gera três documentos:
  roteiro de conversa de feedback, sistema de metas com KPIs e planilha CSV de acompanhamento.
  Usa frameworks reconhecidos internacionalmente: Gilbert BEM, SBI, Radical Candor, GROW e SMART.
  Use quando o usuário mencionar "queda de desempenho", "colaborador não está entregando",
  "conversa de feedback", "sistema de metas", "KPIs de time", "avaliar colaborador",
  "bônus por resultado", "desempenho do time" ou /gestao-desempenho.
---

# /gestao-desempenho — Diagnóstico e Gestão de Desempenho

## Contexto

Ler antes de iniciar:
- `.contexto/empresa.md` — estrutura do time e cargos
- `.contexto/preferencias.md` — tom de voz e estilo

---

## Frameworks utilizados

### 1. Gilbert's Behavior Engineering Model (BEM)
Desenvolvido por Thomas Gilbert (autor de *Human Competence*, 1978), referência em análise de performance.
Separa causas de desempenho em dois grupos:

**Ambiente (responsabilidade da organização):**
- Informação: o colaborador sabe o que se espera dele, como fazer e recebe feedback?
- Recursos: tem ferramentas, tempo e suporte suficientes?
- Incentivos: as consequências do bom desempenho são claras e justas?

**Indivíduo (responsabilidade do colaborador):**
- Conhecimento: tem o treinamento e a capacidade técnica necessária?
- Capacidade: tem aptidão física/cognitiva para a função?
- Motivação: está engajado e quer performar?

**Regra de ouro do BEM:** antes de concluir que é problema do colaborador, verificar se o ambiente está favorecendo o bom desempenho.

---

### 2. Modelo SBI — Situation, Behavior, Impact
Desenvolvido pelo Center for Creative Leadership (CCL), instituição com campus em Harvard, Greensboro e Bruxelas.
Estrutura o feedback de forma objetiva e não pessoal:
- **Situação:** quando e onde o comportamento ocorreu
- **Comportamento:** o que exatamente foi feito ou deixado de fazer (observável, não interpretação)
- **Impacto:** qual foi o efeito concreto no cliente, no time ou no negócio

---

### 3. Radical Candor (Kim Scott)
Framework de Kim Scott, ex-diretora do Google e Apple. Publicado em *Radical Candor* (2017).
Dois eixos para conduzir a conversa de feedback:
- **Care Personally:** demonstrar que se importa com a pessoa, não só com o resultado
- **Challenge Directly:** ser direto sobre o problema, sem suavizar ao ponto de perder clareza

Quadrante a evitar: *Ruinous Empathy* — feedback suavizado que não muda nada.

---

### 4. Modelo GROW (Goal, Reality, Options, Will)
Criado por Sir John Whitmore, base do coaching executivo moderno. Referenciado em programas da Harvard Business School e London Business School.
Usado na parte da conversa em que se busca comprometimento com a mudança:
- **Goal:** qual é o resultado esperado?
- **Reality:** qual é a situação atual com honestidade?
- **Options:** quais caminhos existem para melhorar?
- **Will:** qual é o compromisso concreto a partir de agora?

---

### 5. Metas SMART
Framework originado em 1981 por George Doran. Adotado por Harvard Business Review, McKinsey e praticamente todas as referências de gestão modernas.
Toda meta definida deve ser:
- **Specific** (Específica): sem ambiguidade
- **Measurable** (Mensurável): com número ou critério claro
- **Achievable** (Atingível): desafiadora mas possível
- **Relevant** (Relevante): conectada ao que importa para o negócio
- **Time-bound** (com prazo): data clara de avaliação

---

## Workflow

### Passo 1 — Coletar informações básicas

Verificar se existe `time/[nome]/perfil.md`. Se existir, usar como base e não perguntar o que já está documentado.

Se não existir, perguntar:

1. "Qual o nome do colaborador e qual é o cargo dele?"
2. "Quais são as funções definidas para ele? (pode listar ou colar)"
3. "Há quanto tempo ele está na empresa e nessa função?"

---

### Passo 2 — Diagnóstico pelo BEM

Perguntar sobre cada uma das seis dimensões do BEM. Não fazer todas de uma vez — conduzir como conversa:

**Dimensão Informação:**
> "Ele tem clareza do que se espera dele em cada função? Existe algum processo documentado ou é tácito?"

**Dimensão Recursos:**
> "Ele tem as ferramentas, o tempo e o suporte que precisa para entregar o que é esperado?"

**Dimensão Incentivos:**
> "As consequências de performar bem (ou mal) estão claras para ele? Existe algum sistema de reconhecimento?"

**Dimensão Conhecimento:**
> "Ele tem o treinamento e a capacidade técnica para fazer o que é esperado?"

**Dimensão Motivação:**
> "Como você percebe o engajamento dele? Ele demonstra iniciativa ou espera ser cobrado?"

Com base nas respostas, identificar se os problemas são predominantemente **ambientais** (processo, clareza, suporte) ou **individuais** (atitude, competência, motivação). Isso muda o tom da conversa de feedback.

---

### Passo 3 — Mapear os problemas específicos

> "Quais são os comportamentos ou entregas que estão abaixo do esperado? Pode ser específico — o que você está vendo que não deveria estar vendo?"

Para cada problema relatado, identificar:
- É observável e concreto ou é uma percepção/impressão?
- Tem prazo ou critério de comparação claro?
- Acontece com frequência ou foi pontual?

Organizar os problemas em tabela:

| Problema | Frequência | Impacto | Causa provável (BEM) |
|---|---|---|---|

---

### Passo 4 — Definir os KPIs

Com base nos problemas mapeados, propor de 3 a 5 KPIs SMART.

Cada KPI deve ter:
- O que mede
- Como mede (evidência verificável)
- Meta clara
- Peso em reais (se houver bônus)

Perguntar:
> "O bônus é tudo ou nada, proporcional por KPI ou dividido em blocos?"
> "Qual o valor do bônus disponível?"
> "Quantos clientes ou projetos ele gerencia ativamente?"

---

### Passo 5 — Gerar os documentos

Gerar três arquivos salvos em `time/[nome]/`:

**Arquivo 1:** `feedback-[data].md`
Roteiro completo da conversa de feedback estruturado no modelo SBI + Radical Candor + GROW:
- Enquadramento da conversa (abertura Radical Candor)
- Um bloco por problema: Situação → Comportamento → Impacto → Pergunta de escuta
- Bloco GROW: meta, realidade, opções, compromisso
- Lista de acordos a confirmar ao final
- Data de acompanhamento

**Arquivo 2:** `sistema-bonus.md`
Sistema de metas com KPIs SMART:
- Tabela de KPIs com peso, meta e critério de medição
- Tabela de cálculo do bônus
- Simulação de cenários (mês perfeito, bom, fraco, ruim)
- Regras gerais (como é medido, quem mede, quando paga)
- Texto de abertura para apresentar ao colaborador

**Arquivo 3:** `kpis-bonus.csv`
Planilha de acompanhamento mensal:
- Colunas: Mês, KPI, Peso Máximo (R$), Meta, Resultado Apurado, Valor Calculado, Observações
- Pré-preenchida com os KPIs definidos para os próximos 12 meses
- Com fórmulas para KPIs percentuais

---

### Passo 6 — Recomendar próximos passos

Ao final, apresentar:

1. **Classificação do caso** — com base no BEM, o problema é predominantemente ambiental, individual ou misto?
2. **Tom recomendado para a conversa** — corretivo (problema de atitude/motivação) ou construtivo (problema de processo/clareza)?
3. **Data de acompanhamento sugerida** — 30 dias para problemas leves, 15 dias para casos graves
4. **Sinal de alerta** — se o BEM indicar que a maior parte dos problemas é ambiental, alertar que a conversa de feedback isolada não resolve e sugerir ajuste de processo antes.

---

## Saída esperada

Três arquivos em `time/[nome]/`:
- `feedback-[DDMESANO].md`
- `sistema-bonus.md`
- `kpis-bonus.csv`

E um resumo final na conversa com:
- Classificação BEM do caso
- Tom recomendado para a conversa
- Data sugerida de acompanhamento
