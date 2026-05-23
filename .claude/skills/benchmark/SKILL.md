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
- **Token Meta Ad Library:** variável `META_ACCESS_TOKEN` no arquivo `.env` do projeto

---

## Pré-requisito: Token Meta Ad Library

Para buscar anúncios automaticamente, você precisa de um access token do Facebook:

1. Acesse developers.facebook.com e faça login
2. Vá em "Minhas Apps" > crie um app do tipo "Outro > Business"
3. Vá em "Ferramentas > Graph API Explorer"
4. Selecione seu app, clique em "Gerar token de acesso" e adicione a permissão `ads_read`
5. Copie o token gerado
6. Crie (ou edite) o arquivo `.env` na raiz do projeto e adicione: `META_ACCESS_TOKEN=seu_token_aqui`

Se não tiver o token configurado, a skill segue o fluxo com orientação manual para essa etapa.

---

## Workflow

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

Agrupar os resultados por `page_name` e contar quantos anúncios ativos cada anunciante tem. Ordenar do maior para o menor — mais anúncios = mais investimento = mais escala.

Usar 2 a 3 variações de keywords do nicho para ampliar a cobertura. Exemplos:
- Para advocacia tributária: `"advogado tributário"`, `"planejamento tributário"`, `"reduzir impostos empresa"`
- Para agência de viagens: `"pacote de viagem"`, `"viagem internacional"`, `"cruzeiro promoção"`

Se token não disponível, pular para Fase 2.2 e anotar que a triagem por Meta será manual.

#### Fase 2.2 — Busca complementar no Google (fonte secundária)

Captura marcas estabelecidas que podem não aparecer na busca por keyword (ex: usam copy muito diferente nos anúncios).

Queries:
- `[nicho] Brasil site confiável OR referência OR líder`
- `melhores [nicho] Brasil [ano]`
- `[nicho] depoimentos OR "casos de sucesso" OR "resultados"`

#### Fase 2.3 — Triagem e ranqueamento

Cruzar os candidatos das duas buscas. Para cada nome encontrado, verificar rapidamente:

1. **Tem anúncios ativos no Meta?** (confirmado via API na Fase 2.1, ou anotar para checar manualmente)
2. **Tem site ou landing page?** (URL aparece no resultado de busca ou nos anúncios)
3. **Tem presença no Instagram?** (handle identificável via Google ou nos anúncios)

Descartar candidatos sem anúncios ativos e sem site identificável.

Apresentar lista final de **3 a 6 concorrentes** ranqueados por volume de anúncios ativos no Meta (do maior para o menor). Para cada um, mostrar:
- Nome / página
- Nº de anúncios ativos no Meta (se disponível)
- Site identificado
- Handle do Instagram (se encontrado)

Pedir confirmação antes de continuar a análise.

### Passo 3 — Anúncios Meta Ad Library (automático)

Para cada concorrente confirmado, verificar se `META_ACCESS_TOKEN` está disponível no `.env`.

**Se token disponível:** buscar via API:

```
GET https://graph.facebook.com/v21.0/ads_archive
  ?access_token={META_ACCESS_TOKEN}
  &ad_reached_countries=["BR"]
  &search_page_names={nome_exato_da_página}
  &ad_active_status=ACTIVE
  &fields=page_name,ad_creative_bodies,ad_creative_link_captions,ad_creative_link_descriptions,ad_creative_link_titles,ad_delivery_start_time,ad_snapshot_url
  &limit=10
```

Extrair de cada anúncio:
- Texto da copy (headline + corpo)
- URL de destino
- Data de início
- Link do snapshot

**Se token não disponível:** orientar:
> "Não encontrei o token da Meta. Para buscar automaticamente, siga o Pré-requisito no topo dessa skill. Por enquanto, acesse facebook.com/ads/library, pesquise por [nome do concorrente] e me cole os anúncios que encontrar — eu estruturo tudo."

### Passo 4 — Analisar landing pages (automático)

Para cada URL de destino encontrada nos anúncios, usar **WebFetch via Jina Reader** para extrair o conteúdo:

URL de acesso: `https://r.jina.ai/{URL_da_landing_page}`

Se Jina falhar, tentar WebFetch direto na URL original.

Extrair:
- Headline principal (promessa)
- Proposta de valor resumida
- Seções identificadas na estrutura da página
- CTA principal (o que pedem: clique, mensagem WhatsApp, formulário, agendamento)
- Prova social (depoimentos, números, logos de clientes)
- O que o formulário pede (nome, email, WhatsApp, etc.)

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

| # | Nome | Site | Instagram |
|---|------|------|-----------|
| 1 | | | |
| 2 | | | |

---

## [Nome do Concorrente 1]

### Anúncios Meta
- **Anúncios ativos:** X
- **Ângulo principal:** [o que a maioria dos anúncios comunica]
- **Copy de destaque:**
  > "[melhor exemplo de headline/copy encontrado]"
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

### Funil Completo

| Etapa | O que encontramos |
|-------|-------------------|
| Anúncio | |
| Landing Page | |
| Página de Obrigada | |
| Formulário/CTA | |
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
