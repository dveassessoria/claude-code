---
name: copy-ads-estatico-venda-elevadores
description: >
  Gera copy para 5 anúncios estáticos (IMG) de empresas que vendem equipamentos de elevadores
  (residencial, hidráulico, plataforma elevatória, comercial).
  Cada ad cobre um ângulo diferente (produto, valorização patrimonial, tecnologia, personalização, acessibilidade).
  Lê contexto do cliente (ICP, personas, diferencial, produtos) nos .md da pasta do cliente.
  Salva em clientes/[nome-cliente]/anuncios/RM [nº]/Estáticos/.
  Use quando o usuário pedir "copy de anúncio de venda de elevador", "ads estáticos elevador equipamento",
  "criar anúncios para vender elevadores", ou /copy-ads-estatico-venda-elevadores.
---

# /copy-ads-estatico-venda-elevadores — Copy de Anúncios Estáticos para Venda de Elevadores

## Uso

```
/copy-ads-estatico-venda-elevadores [nome-cliente] [número da remessa]
```

**Exemplos:**
- `/copy-ads-estatico-venda-elevadores altitude-elevadores 07`
- `/copy-ads-estatico-venda-elevadores primmus-elevadores 03`

---

## Workflow

### Passo 1 — Coletar inputs

Se o usuário não forneceu nome do cliente e número da remessa junto ao comando, perguntar:

> "Para qual cliente e qual remessa? Ex: Altitude Elevadores, RM 07"

Não avançar sem esses dois dados.

### Passo 2 — Ler contexto do cliente

Varrer **todos os arquivos .md** dentro de `clientes/[nome-cliente]/` (recursivo).

Extrair e consolidar:
- **ICP e Personas** — quem compra (proprietário de imóvel de alto padrão, fazendeiro, empresário, construtora, pessoa com mobilidade reduzida, engenheiro, arquiteto)
- **Produtos vendidos** — quais equipamentos o cliente comercializa (residencial, hidráulico, plataforma elevatória, predial/comercial)
- **Diferencial Competitivo** — o que distingue essa empresa das concorrentes (tecnologia, personalização, equipe própria, garantia)
- **Diferenciais técnicos** — inovações específicas (app, resgate remoto, monitoramento por IA, Alexa, tela touch, sob medida, redundâncias de segurança)
- **Prova social** — projetos entregues, anos de mercado, garantia oferecida, depoimentos
- **Localização/área de entrega** — estados e regiões atendidos
- **Ticket médio** — faixa de preço dos equipamentos (impacta o tom da copy)

Se algum dado crítico não for encontrado, avisar antes de continuar:

> "Não encontrei [dado] nos arquivos do cliente. Pode me passar ou quer que eu escreva sem essa informação?"

### Passo 3 — Verificar portfólio de produtos

Antes de gerar, identificar se o cliente vende **plataforma elevatória**. Esse dado define o AD 05:

- **Vende plataforma:** AD 05 usa ângulo de Acessibilidade (persona: família com mobilidade reduzida)
- **Não vende plataforma:** AD 05 usa ângulo de Confiança/Credencial (garantia, equipe própria, anos de mercado)

### Passo 4 — Gerar os 5 ads

Gerar sempre 5 anúncios, cada um com um ângulo principal diferente, na seguinte ordem:

| AD | Ângulo Principal | O que priorizar |
|---|---|---|
| 01 | **Produto** | Nomear o tipo de elevador (residencial, hidráulico, plataforma). Mostrar o equipamento como solução concreta para o imóvel do cliente |
| 02 | **Valorização Patrimonial** | ROI do elevador: valoriza o imóvel em % concreto. Reposicionar o elevador de "custo" para "investimento" |
| 03 | **Tecnologia e Inovação** | Diferenciais técnicos exclusivos do produto (app, IA, resgate remoto, quadro próprio, Alexa). Para quem decide por tecnologia, não preço |
| 04 | **Personalização e Qualidade** | Fabricação sob medida, equipe de instalação própria, não competição por preço. Para quem quer o melhor, não o mais barato |
| 05 | **Acessibilidade** (se vende plataforma) ou **Credencial** (se não vende) | Acessibilidade: plataforma elevatória para mobilidade reduzida, conforto familiar. Credencial: anos de mercado, garantia, projetos entregues |

---

### Estrutura de cada AD

Cada ad deve seguir exatamente este formato:

```
---

**AD [nº] - IMG - RM [nº da remessa]**

---

**PERSONA:** [persona(s) extraída(s) do briefing — específica para o ângulo do ad]

| Campo | Conteúdo |
|---|---|
| **HEADLINE** | [título principal — específico, direto. Para alto ticket: construir valor, não reduzir preço] |
| **SUBHEADLINE** | [subtítulo complementar — opcional, usar só se agregar; omitir se não houver] |
| **Bullet Points** | [2 a 3 diferenciais técnicos ou benefícios concretos — opcional] |
| **Texto (acima do CTA)** | [frase de reforço antes do botão — opcional] |
| **CTA** | [chamada para ação] |

---

**TÍTULOS PARA META ADS:**

1. [título 1 — variação com foco no produto ou tipo de elevador]
2. [título 2 — variação com foco em tecnologia, garantia ou diferencial]
3. [título 3 — variação com foco em resultado (valorização, segurança, conforto)]

---

**LEGENDA:**

[Parágrafo 1: gancho que ativa o desejo ou a situação do cliente. 1-2 frases. Para alto ticket: começar pelo resultado ou pela identidade do comprador, não pelo problema.]

[Parágrafo 2: apresentar a empresa + produto. 1-2 frases.]

[Parágrafo 3: ampliar os diferenciais técnicos ou de serviço. 1-2 frases.]

[Parágrafo 4: CTA para ação. Terminar com emoji de dedo apontando + instrução direta.]
```

---

### Regras de escrita obrigatórias

**Proibido em qualquer elemento, sem exceção:**
- Travessão (—): nunca usar. Substituir por vírgula, dois-pontos ou reescrever a frase
- Estrutura "Isso não é X. Isso é Y." em qualquer variação
- Frases genéricas: "eleve sua experiência", "leve seu imóvel ao próximo nível", "qualidade incomparável"
- Adjetivos inflados sem prova: "o melhor", "o único", "revolucionário"
- Entusiasmo artificial: "Incrível!", "Você não vai acreditar..."
- Competição por preço: nunca mencionar "preço baixo", "mais barato", "custo acessível" — o produto é de alto ticket e compete por valor

**O que funciona para venda de elevadores (alto ticket):**
- Especificidade técnica com linguagem do comprador: "elevador hidráulico até 4 paradas", "instalação sob medida", "1 ano de garantia no equipamento"
- Valorização patrimonial com número concreto: "valoriza o imóvel em até 25%" (usar apenas se o cliente tiver esse dado ou se for dado de mercado — sinalizar se for estimativa)
- Identidade do comprador: "quem constrói com padrão não aceita compromisso na mobilidade"
- Tecnologia como status e segurança: app, IA, resgate remoto comunicam confiança e modernidade
- Personalização como diferencial de qualidade: sob medida, equipe própria, sem terceirização

**CTAs aprovados para venda (usar variações):**
- "Solicite seu Orçamento"
- "Solicite seu Orçamento Agora"
- "Solicitar Orçamento Hoje"
- "Fale com um Especialista"
- "Receba uma Proposta Personalizada"
- "Solicite uma Visita Técnica"

**TÍTULOS PARA META ADS:**
- Cada ad deve ter 3 títulos únicos, variando ângulo entre si
- Não repetir os mesmos títulos entre os 5 ads
- Máximo ~40 caracteres por título
- Incluir: tipo de produto, dado concreto (%, anos, garantia) ou localização quando relevante

**LEGENDA:**
- Variar entre os 5 ads — nunca repetir o mesmo texto
- Manter estrutura de 4 parágrafos curtos
- Tom: confiante, aspiracional e técnico. Não exagerado. Soa como especialista, não como vendedor
- Último parágrafo sempre com CTA + emoji (👇 ou similar)

**Personas por ângulo (referência):**
- AD 01 (Produto): Proprietário de Imóvel Residencial, Construtora, Incorporadora
- AD 02 (Valorização): Proprietário de Imóvel, Investidor Imobiliário
- AD 03 (Tecnologia): Proprietário de Alto Padrão, Engenheiro, Arquiteto
- AD 04 (Personalização): Proprietário de Casa de Alto Padrão, Construtora Premium
- AD 05 (Acessibilidade): Família com Mobilidade Reduzida, Proprietário de Imóvel com Idosos

---

### Passo 5 — Gerar o arquivo .docx e salvar

Gerar um script Python usando `python-docx` e executar para criar o arquivo `.docx`.

**Caminho de destino:**
```
clientes/[nome-cliente]/anuncios/RM [nº]/Estáticos/ads-estaticos-rm[nº].docx
```

Criar as pastas intermediárias se não existirem.

---

**Formatação obrigatória do .docx** (replicar o layout do Google Docs de referência):

**Fonte:** Montserrat em todos os elementos. Se não disponível no sistema, usar Arial como fallback.

**Para cada AD, a estrutura no documento deve ser:**

1. **Título do ad** — ex: `AD 01 - IMG - RM 07`
   - Centralizado, negrito, tamanho 16pt

2. **Linha separadora**

3. **PERSONA** — `PERSONA: [valor]`
   - Negrito no label "PERSONA:", normal no valor

4. **Tabela de copy** com 2 colunas:
   - Coluna esquerda: fundo azul escuro (#1B2A4A), texto branco, negrito (HEADLINE, SUBHEADLINE, Bullet Points, Texto, CTA)
   - Coluna direita: fundo branco, texto preto, conteúdo do campo
   - Borda da tabela: cinza claro
   - Omitir linhas de campos opcionais quando estiverem vazios

5. **TÍTULOS PARA META ADS:** — negrito, seguido da lista numerada

6. **Linha separadora**

7. **LEGENDA:** — negrito, seguido dos parágrafos da legenda

8. **Quebra de página** entre cada AD

---

**Código base para o script Python:**

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

FONT_NAME = "Montserrat"
DARK_BLUE = RGBColor(0x1B, 0x2A, 0x4A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
```

Adaptar o script com o conteúdo real de cada AD gerado no Passo 4.

---

Após gerar e salvar o .docx, exibir na conversa o conteúdo de todos os ads em texto (para revisão rápida).

Ao final, perguntar: "Quer ajustar o ângulo de algum ad ou gerar variações de headline?"
