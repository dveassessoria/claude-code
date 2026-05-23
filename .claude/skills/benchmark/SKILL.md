---
name: benchmark
description: >
  Faz benchmark competitivo de um nicho ou cliente. Mapeia concorrentes relevantes,
  busca anúncios ativos na Meta Ad Library, analisa landing pages e estrutura de funil,
  e gera um documento de análise completo salvo em clientes/[nome]/benchmark-[data].md.
  Use quando o usuário mencionar "benchmark", "pesquisa de concorrentes", "análise competitiva",
  "o que os concorrentes estão fazendo", "pesquisa de mercado" ou pedir análise de um nicho.
---

# /benchmark — Benchmark Competitivo

## Dependências

- **Contexto do negócio:** `_contexto/empresa.md` (se existir)
- **Tom de voz:** `_contexto/preferencias.md` (se existir)
- **Variáveis no `.env`:**
  - `META_ACCESS_TOKEN` — token de acesso (gerado uma vez, dura 60 dias)
  - `META_APP_ID` — ID do app Facebook (necessário para renovar token)
  - `META_APP_SECRET` — segredo do app Facebook (necessário para renovar token)

---

## Workflow

### Passo 0 — Verificar token Meta

Antes de qualquer coisa, verificar o estado do token.

#### 0.1 — Checar se o token existe

Ler o arquivo `.env` na raiz do projeto. Se `META_ACCESS_TOKEN` não existir ou estiver vazio, ir para **Setup inicial** abaixo.

#### 0.2 — Validar o token

Fazer uma chamada de teste:

```
GET https://graph.facebook.com/me?access_token={META_ACCESS_TOKEN}
```

- Resposta com `id` → token válido. Prosseguir para o Passo 1.
- Erro código `190` ou similar → token expirado. Ir para **Renovar token** abaixo.

---

#### Setup inicial (primeira vez)

Informar o usuário:
> "Não encontrei o token Meta configurado. Vou precisar de três coisas do seu app no Facebook. Não se preocupa — é uma vez só e leva uns 5 minutos."

Pedir em sequência:

**1. App ID e App Secret:**
> "Acesse developers.facebook.com > seu app > Configurações > Básico. Me passe o **App ID** e o **App Secret**."

Salvar no `.env`:
```
META_APP_ID=valor_informado
META_APP_SECRET=valor_informado
```

**2. Token curto (short-lived):**
> "Agora vá em Ferramentas > Graph API Explorer. Selecione seu app, clique em 'Gerar token de acesso' e adicione a permissão `ads_read`. Me passe o token gerado."

Depois de receber o token curto, ir para **Trocar por token longo** abaixo.

---

#### Renovar token (token expirado)

Verificar se `META_APP_ID` e `META_APP_SECRET` existem no `.env`.

**Se existem:** informar e pedir apenas o token curto:
> "Seu token Meta expirou. É rápido renovar — acesse developers.facebook.com > Ferramentas > Graph API Explorer, selecione seu app e gere um novo token com permissão `ads_read`. Me passe o token gerado."

**Se não existem:** seguir o fluxo de Setup inicial completo.

---

#### Trocar por token longo (válido por 60 dias)

Com o token curto em mãos, fazer a troca automaticamente:

```
GET https://graph.facebook.com/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id={META_APP_ID}
  &client_secret={META_APP_SECRET}
  &fb_exchange_token={token_curto_informado}
```

A resposta retorna `access_token` com validade de ~60 dias.

Salvar o novo token no `.env`:
```
META_ACCESS_TOKEN=novo_token_longo
```

Confirmar para o usuário:
> "Token renovado e salvo. Válido por ~60 dias. Quando expirar, é só me dar o novo token curto do Graph API Explorer que eu faço a troca automática."

Prosseguir para o Passo 1.

---

### Passo 1 — Briefing inicial

Perguntar ao usuário:

1. "Qual cliente ou nicho vamos fazer o benchmark?" (ex: academia de crossfit, escritório de advocacia tributária, agência de viagens)
2. "Você já tem algum concorrente específico em mente, ou quer que eu mapeie do zero?"
3. "Focamos no Brasil ou tem mercado de outro país relevante?"

Se o usuário fornecer essas informações de forma livre antes de ser perguntado, extrair e seguir sem repetir as perguntas.

### Passo 2 — Mapear e filtrar concorrentes

Se o usuário não trouxer nomes específicos, executar as duas buscas abaixo em paralelo e depois cruzar os resultados.

#### Fase 2.1 — Busca por keywords na Meta Ad Library (fonte principal)

Quem aparece aqui tem budget ativo no Meta — sinal direto de escala.

Se `META_ACCESS_TOKEN` disponível, buscar via API com palavras-chave do nicho:

```
GET https://graph.facebook.com/v21.0/ads_archive
  ?access_token={META_ACCESS_TOKEN}
  &ad_reached_countries=["BR"]
  &search_terms={palavras_chave_do_nicho}
  &ad_active_status=ACTIVE
  &fields=page_name,page_id,ad_creative_bodies,ad_creative_link_titles,ad_delivery_start_time
  &limit=50
```

Usar 2 a 3 variações de keywords do nicho para ampliar a cobertura. Exemplos:
- Para advocacia tributária: `"advogado tributário"`, `"planejamento tributário"`, `"reduzir impostos empresa"`
- Para agência de viagens: `"pacote de viagem"`, `"viagem internacional"`, `"cruzeiro promoção"`

Para cada anunciante encontrado, calcular já nessa etapa:
- **Quantidade de anúncios ativos**
- **Longevidade** = hoje menos `ad_delivery_start_time` do anúncio mais antigo ainda ativo (em dias)
- **Variações de criativo** = contar ângulos ou ofertas distintos entre os anúncios ativos (mensagens claramente diferentes = split test ativo)

Se token não disponível, pular para Fase 2.2 e anotar que a triagem por Meta será manual.

#### Fase 2.2 — Busca complementar no Google (fonte secundária)

Captura marcas estabelecidas que podem usar copy muito diferente nos anúncios e não aparecer na busca por keyword.

Queries:
- `[nicho] Brasil referência OR líder OR especialista`
- `melhores [nicho] Brasil [ano]`
- `[nicho] "casos de sucesso" OR "resultados" OR depoimentos`

#### Fase 2.3 — Triagem, score e ranqueamento

Cruzar os candidatos das duas fontes. Descartar quem não tem anúncios ativos e não tem site identificável.

Para cada candidato que passa na triagem, calcular o **Score de Relevância (0 a 15 pontos)**:

| Critério | Pontuação |
|----------|-----------|
| **Longevidade** — anúncio mais antigo ativo há 60+ dias | 3 pts |
| **Longevidade** — anúncio mais antigo ativo há 30-59 dias | 2 pts |
| **Longevidade** — anúncios com menos de 30 dias | 1 pt |
| **Volume** — 10+ anúncios ativos no Meta | 3 pts |
| **Volume** — 5-9 anúncios ativos | 2 pts |
| **Volume** — 1-4 anúncios ativos | 1 pt |
| **Multi-canal** — confirmado no Meta E no Google Ads | 2 pts |
| **Multi-canal** — confirmado em apenas um canal | 1 pt |
| **Variações** — 3+ ângulos de criativo distintos rodando | 2 pts |
| **Variações** — 1-2 ângulos | 1 pt |
| **Tráfego do site** — 50k+ visitas/mês (SimilarWeb) | 2 pts |
| **Tráfego do site** — 10k-50k visitas/mês | 1 pt |
| **Funil maduro** — thank you page + pixel + CTA de fechamento | 3 pts |
| **Funil parcial** — landing page com formulário mas sem profundidade | 1 pt |

**Interpretação:**
- 12-15 pts → concorrente de referência, altamente relevante para modelar
- 8-11 pts → relevante, vale analisar com atenção
- 4-7 pts → incluir só se precisar completar a lista
- Abaixo de 4 pts → descartar

Apresentar lista final de **3 a 6 concorrentes** ordenados pelo score, mostrando:
- Nome / página
- Score total (X/15) com classificação
- Nº de anúncios ativos no Meta + longevidade do mais antigo
- Site identificado
- Handle do Instagram (se encontrado)

Pedir confirmação antes de continuar a análise detalhada.

### Passo 3 — Análise detalhada de anúncios Meta (automático)

Para cada concorrente confirmado, buscar os anúncios por nome de página (mais preciso que por keyword):

```
GET https://graph.facebook.com/v21.0/ads_archive
  ?access_token={META_ACCESS_TOKEN}
  &ad_reached_countries=["BR"]
  &search_page_names={nome_exato_da_página}
  &ad_active_status=ACTIVE
  &fields=page_name,ad_creative_bodies,ad_creative_link_captions,ad_creative_link_descriptions,ad_creative_link_titles,ad_delivery_start_time,ad_snapshot_url
  &limit=20
```

Para cada anúncio, extrair:
- Texto da copy (headline + corpo)
- URL de destino
- Data de início + dias rodando até hoje
- Link do snapshot

Depois de coletar todos os anúncios do concorrente, identificar:

**Longevidade:** qual é o anúncio mais antigo ainda ativo? Quantos dias está rodando? Um anúncio com 30+ dias ativo é quase certamente lucrativo — anotar como "anúncio provado".

**Variações de criativo:** agrupar os anúncios por ângulo ou oferta. Exemplos de ângulos distintos:
- Dor/problema ("você está perdendo dinheiro com impostos")
- Transformação ("como saí de X para Y")
- Prova social ("mais de X clientes")
- Oferta direta ("consulta grátis hoje")
- Autoridade ("especialista com X anos")

Identificar quantos ângulos distintos estão rodando simultaneamente — isso revela a sofisticação do anunciante e quais mensagens ele está priorizando.

**Se token não disponível:** orientar:
> "Não encontrei o token da Meta. Para buscar automaticamente, siga o Pré-requisito no topo dessa skill. Por enquanto, acesse facebook.com/ads/library, pesquise por [nome do concorrente] e me cole os anúncios que encontrar — eu estruturo tudo."

### Passo 4 — Análise de landing page, tráfego e profundidade de funil (automático)

#### Fase 4.1 — Ler a landing page

Para cada URL de destino encontrada nos anúncios, usar **WebFetch via Jina Reader**:

`https://r.jina.ai/{URL_da_landing_page}`

Se Jina falhar, tentar WebFetch direto na URL original.

Extrair:
- Headline principal (promessa)
- Proposta de valor resumida
- Seções identificadas na estrutura da página
- CTA principal (o que pedem: clique, mensagem WhatsApp, formulário, agendamento)
- Prova social (depoimentos, números, logos de clientes)
- O que o formulário pede (nome, email, WhatsApp, etc.)

Verificar também na resposta HTML se há sinais de pixel instalado (strings como `fbq(`, `gtag(`, `_ga`, Google Tag Manager) — presença de pixel indica que estão otimizando para conversão.

#### Fase 4.2 — Estimar tráfego via SimilarWeb

Para cada domínio identificado, tentar acessar a página pública do SimilarWeb via Jina Reader:

`https://r.jina.ai/https://www.similarweb.com/website/{dominio}/`

Extrair se disponível:
- Visitas mensais estimadas
- Principais fontes de tráfego (orgânico, pago, direto, social, referência)
- Países de origem
- Taxa de rejeição (se disponível)

Se SimilarWeb não retornar dados úteis (site muito pequeno ou bloqueado), registrar como `[tráfego não disponível]` e seguir.

#### Fase 4.3 — Verificar profundidade do funil

Depois de ler a landing page, tentar seguir o funil ativamente:

1. **Página de obrigada:** se houver formulário ou botão de CTA, verificar se há uma URL de redirecionamento pós-conversão mencionada no HTML (ex: `/obrigado`, `/confirmacao`, `/thank-you`). Tentar acessar essa URL via Jina Reader.

2. **Botão WhatsApp:** verificar se há link `wa.me/` na página — indica que o fechamento é feito por WhatsApp.

3. **Chat ou bot:** verificar presença de scripts de chat (Intercom, Chatwoot, ManyChat, etc.) no HTML.

4. **Upsell ou próximo passo:** se houver página de obrigada, verificar se ela contém nova oferta, agendamento ou próximo passo claro.

Classificar o funil encontrado:
- **Maduro:** landing page profissional + página de obrigada + CTA de fechamento claro (WhatsApp, agendamento ou redirecionamento com próximo passo)
- **Básico:** landing page com formulário, mas sem página de obrigada identificável ou próximo passo claro
- **Mínimo:** apenas link para Instagram, WhatsApp direto ou página genérica

### Passo 5 — Anúncios Google + Instagram (manual guiado)

Para essas etapas não há API pública confiável. Orientar a coleta com campos estruturados:

**Google Ads — pedir ao usuário:**
> "Agora acesse adstransparency.google.com e pesquise por '[nome do concorrente]'. Me passa:
> - Quantos anúncios ativos encontrou?
> - Qual é a headline e descrição dos principais anúncios?
> - Para qual URL ou tipo de destino apontam?"

**Instagram — pedir ao usuário:**
> "Acesse o perfil @[handle ou URL] e me informa:
> - Número de seguidores
> - Quantos posts por semana (aproximadamente)
> - Formato predominante: Reels, carrossel ou foto estática
> - Que tipo de conteúdo publica: educativo, bastidor, depoimento, oferta direta
> - Engajamento médio nos posts (curtidas + comentários)"

Registrar as respostas como vieram — sem inventar dados.

### Passo 6 — Gerar o documento

Com todos os dados coletados (automáticos e manuais), gerar o documento completo em Markdown.

**Estrutura do documento:**

```markdown
# Benchmark Competitivo — [Nicho/Cliente]

**Data:** [data]
**Preparado por:** DVE Assessoria
**Concorrentes analisados:** [N]

---

## Resumo Executivo

[3-5 linhas com os padrões dominantes do mercado, o que está funcionando e onde estão as oportunidades]

---

## Concorrentes Analisados

| # | Nome | Score | Anúncios Meta | Tráfego/mês | Site | Instagram |
|---|------|-------|--------------|-------------|------|-----------|
| 1 | | /15 | | | | |
| 2 | | /15 | | | | |

---

## [Nome do Concorrente 1]

**Score de Relevância: X/15** — [classificação: referência / relevante / complementar]

### Anúncios Meta
- **Anúncios ativos:** X
- **Anúncio mais antigo:** X dias rodando → [provado / recente]
- **Variações de criativo:** X ângulos distintos identificados
  - Ângulo 1: [descrição]
  - Ângulo 2: [descrição]
  - ...
- **Copy de destaque (anúncio mais antigo ativo):**
  > "[headline/copy do anúncio provado]"
- **CTA dos anúncios:** [clique no link / mensagem / formulário]

### Anúncios Google
- **Anúncios ativos:** X
- **Headlines principais:** [exemplos]
- **Destino:** [tipo de página]

### Landing Page
- **URL:** [link]
- **Headline:** [promessa principal]
- **Proposta de valor:** [resumo em 1-2 linhas]
- **Estrutura da página:**
  1. [seção 1]
  2. [seção 2]
  3. ...
- **Prova social:** [depoimentos / números / logos]
- **CTA / Formulário:** [o que pedem]
- **Pixel instalado:** [Sim (Meta/Google) / Não detectado]
- **Estimativa de tráfego:** [X visitas/mês — fonte: SimilarWeb] ou [não disponível]
- **Principais fontes de tráfego:** [pago / orgânico / direto / social]

### Funil Completo

**Classificação do funil:** [Maduro / Básico / Mínimo]

| Etapa | O que encontramos |
|-------|-------------------|
| Anúncio | |
| Landing Page | |
| Pixel de rastreamento | |
| Página de Obrigada | |
| Formulário/CTA | |
| WhatsApp / Chat / Bot | |
| Próximo passo | |

### Instagram
- **Seguidores:** X
- **Frequência:** X posts/semana
- **Formato predominante:** [Reels / Carrossel / Foto]
- **Tipo de conteúdo:** [padrão observado]
- **Engajamento médio:** [curtidas + comentários por post]

---

[Repetir bloco para cada concorrente]

---

## Análise Comparativa

### O que todos estão fazendo
[Padrões comuns — ângulos de copy, formatos de anúncio, estrutura de funil]

### O que se destaca (melhores práticas)
[O que está funcionando bem em pelo menos um concorrente]

### Oportunidades identificadas
[O que ninguém está fazendo, ou está fazendo mal — ângulos inexplorados, funis fracos, copy genérica]

### Recomendações para [Cliente]
1. [recomendação 1]
2. [recomendação 2]
3. [recomendação 3]
```

### Passo 7 — Salvar

Verificar se existe a pasta `clientes/[nome-cliente]/`. Se não existir, criar antes de salvar.

Salvar o documento em: `clientes/[nome-cliente]/benchmark-[YYYY-MM-DD].md`

Confirmar onde foi salvo e perguntar:
> "Quer que eu converta esse documento pra .docx agora? É só chamar `/docx` passando o caminho do arquivo que gerei."

---

## Regras

- Apresentar a lista de concorrentes mapeados e aguardar confirmação antes de analisar
- Nunca inventar dados — se uma informação não foi encontrada, registrar como `[coletar manualmente]`
- Se uma landing page não carregar via Jina, tentar WebFetch direto e informar o usuário
- Se o token Meta não estiver configurado, não travar — seguir com orientação manual para essa etapa
- O documento final precisa ter pelo menos 2 concorrentes analisados para ter valor comparativo
- Campos não preenchidos ficam marcados como `[coletar manualmente]` — nunca em branco silencioso
- Ao final, sempre mostrar o caminho onde o arquivo foi salvo
