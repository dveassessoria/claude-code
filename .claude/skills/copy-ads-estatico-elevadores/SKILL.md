---
name: copy-ads-estatico-elevadores
description: >
  Gera copy para 5 anúncios estáticos (IMG) de empresas de elevadores.
  Cada ad cobre um ângulo diferente (localização, oferta, prova social, dor/urgência, multidiferencial).
  Lê contexto do cliente (ICP, personas, diferencial, oferta) nos .md da pasta do cliente.
  Salva em clientes/[nome-cliente]/anuncios/RM [nº]/Estáticos/.
  Use quando o usuário pedir "copy de anúncio de elevador", "ads estáticos elevador",
  "criar anúncios para [cliente de elevador]", ou /copy-ads-estatico-elevadores.
---

# /copy-ads-estatico-elevadores — Copy de Anúncios Estáticos para Elevadores

## Uso

```
/copy-ads-estatico-elevadores [nome-cliente] [número da remessa]
```

**Exemplos:**
- `/copy-ads-estatico-elevadores t2-elevadores 07`
- `/copy-ads-estatico-elevadores altitude 03`

---

## Workflow

### Passo 1 — Coletar inputs

Se o usuário não forneceu nome do cliente e número da remessa junto ao comando, perguntar:

> "Para qual cliente e qual remessa? Ex: T2 Elevadores, RM 07"

Não avançar sem esses dois dados.

### Passo 2 — Ler contexto do cliente

Varrer **todos os arquivos .md** dentro de `clientes/[nome-cliente]/` (recursivo).

Extrair e consolidar:
- **ICP e Personas** — quem são os tomadores de decisão (síndico, administradora, proprietário, construtora etc.)
- **Diferencial Competitivo** — o que diferencia essa empresa das concorrentes
- **Oferta atual** — qual promoção ou entrada está ativa (ex: 1º mês grátis, vistoria gratuita)
- **Prova social** — números concretos (contratos ativos, anos de mercado, NPS, cidades atendidas)
- **Localização** — cidade(s) e estado(s) de atuação
- **Serviços** — manutenção preventiva, corretiva, modernização, instalação etc.

Se algum desses dados não for encontrado nos arquivos, avisar o usuário antes de continuar:

> "Não encontrei [dado] nos arquivos do cliente. Pode me passar ou quer que eu escreva sem essa informação?"

### Passo 3 — Gerar os 5 ads

Gerar sempre 5 anúncios, cada um com um ângulo principal diferente, na seguinte ordem:

| AD | Ângulo Principal | O que priorizar |
|---|---|---|
| 01 | **Localização** | Cidade/região + serviço. Mostrar presença local e disponibilidade |
| 02 | **Oferta** | Promoção de entrada (1º mês grátis, vistoria grátis). Baixar a barreira de experimentação |
| 03 | **Prova Social** | Números concretos: contratos, NPS, anos de mercado, depoimento implícito |
| 04 | **Dor/Urgência** | O que acontece quando o elevador falha: condomínio sem serviço, fiscalização, risco de acidente |
| 05 | **Multidiferencial** | Une localização + oferta + prova social num único ad de consolidação |

---

### Estrutura de cada AD

Cada ad deve seguir exatamente este formato:

```
---

**AD [nº] - IMG - RM [nº da remessa]**

---

**PERSONA:** [persona(s) extraída(s) do briefing]

| Campo | Conteúdo |
|---|---|
| **HEADLINE** | [título principal — específico, direto, sem adjetivo vazio] |
| **SUBHEADLINE** | [subtítulo complementar — opcional, usar só se agregar; omitir se não houver] |
| **Bullet Points** | [2 a 3 diferenciais curtos — opcional, usar só em ads que comportam lista] |
| **CTA** | [chamada para ação] |

---

**TÍTULOS PARA META ADS:**

1. [título 1 — variação com foco em localização ou serviço]
2. [título 2 — variação com foco em tempo de mercado ou credencial]
3. [título 3 — variação com foco em diferencial ou benefício]

---

**LEGENDA:**

[Parágrafo 1: gancho que ativa a dor ou o contexto do problema. 1-2 frases.]

[Parágrafo 2: apresentar a empresa + serviço principal. 1-2 frases.]

[Parágrafo 3: ampliar os diferenciais (multimarcas, suporte 24h, equipe própria etc.). 1-2 frases.]

[Parágrafo 4: CTA para ação. Terminar com emoji de dedo apontando + instrução direta.]
```

---

### Regras de escrita obrigatórias

**Proibido em qualquer elemento, sem exceção:**
- Travessão (—): nunca usar. Substituir por vírgula, dois-pontos ou reescrever a frase
- Estrutura "Isso não é X. Isso é Y." em qualquer variação
- Frases genéricas: "transforme seu condomínio", "eleve a experiência dos moradores"
- Adjetivos inflados sem prova: "o melhor", "o único", "revolucionário"
- Entusiasmo artificial: "Incrível!", "Você não vai acreditar..."

**O que funciona para elevadores:**
- Especificidade: número de contratos, anos de mercado, cidade, tempo de resposta
- Linguagem do síndico/administrador: praticidade, responsabilidade, segurança, regularidade
- Urgência real: irregularidade, risco de acidente, elevador parado prejudica todos
- Oferta como porta de entrada: vistoria gratuita, primeiro mês grátis reduzem a resistência

**CTAs aprovados (usar variações):**
- "Agendar no WhatsApp"
- "Agendar Vistoria no WhatsApp"
- "Conversar no WhatsApp"
- "Solicitar Vistoria Gratuita"

**TÍTULOS PARA META ADS:**
- Cada ad deve ter 3 títulos únicos, variando ângulo
- Não repetir os mesmos títulos entre os 5 ads
- Máximo ~40 caracteres por título
- Evitar títulos genéricos — incluir cidade, diferencial ou dado concreto sempre que possível

**LEGENDA:**
- Variar entre os 5 ads — nunca repetir o mesmo texto
- Manter estrutura de 4 parágrafos curtos
- Último parágrafo sempre com CTA + emoji (👇 ou similar)
- Tom: direto, confiável, sem exagero

---

### Passo 4 — Gerar o arquivo .docx e salvar

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

2. **Linha separadora** (borda inferior do parágrafo ou linha horizontal)

3. **PERSONA** — `PERSONA: [valor]`
   - Negrito no label "PERSONA:", normal no valor

4. **Tabela de copy** com 2 colunas:
   - Coluna esquerda: fundo azul escuro (#1B2A4A), texto branco, negrito (HEADLINE, SUBHEADLINE, Bullet Points, CTA)
   - Coluna direita: fundo branco, texto preto, conteúdo do campo
   - Borda da tabela: cinza claro
   - Omitir linhas de SUBHEADLINE e Bullet Points quando o campo estiver vazio

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

# Usar Montserrat em todos os elementos
FONT_NAME = "Montserrat"
DARK_BLUE = RGBColor(0x1B, 0x2A, 0x4A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
```

Adaptar o script com o conteúdo real de cada AD gerado no Passo 3.

---

Após gerar e salvar o .docx, exibir na conversa o conteúdo de todos os ads em texto (para revisão rápida).

Ao final, perguntar: "Quer ajustar o ângulo de algum ad ou gerar variações de headline?"
