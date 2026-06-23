# Skill: Relatório Meta Ads 90 dias

## Quando usar

Quando o usuário pedir um relatório de Meta Ads dos últimos 90 dias, auditoria de campanha, ou análise de desempenho de anúncios para um cliente.

Palavras que disparam: "relatório meta ads", "auditoria meta ads", "análise de campanha", "fazer relatório do [cliente]", "relatório 90 dias".

---

## O que essa skill faz

Gera um relatório completo de Meta Ads em HTML (versão PT e versão ES) com:
- KPI principal: custo por conversa iniciada
- Métricas da campanha: impressões, CPM, cliques no link, CPC, CTR, conversas, custo/conversa
- Desempenho por anúncio com frequência
- Perfil do público: gênero, faixa etária, posicionamento
- Análise geral da conta
- Próximos passos
- Estratégia de criativos

Identidade visual padrão: Chatflux (fundo `#10131c`, verde `#19e65a`). Adaptar conforme o cliente.

---

## Passo a passo

### 1. Identificar o cliente e a campanha

Perguntar ao usuário:
- Qual cliente?
- Qual campanha analisar? (nome ou ID)
- O relatório vai com a identidade de qual empresa? (DVE, Chatflux ou outra)

Consultar `~/.claude/skills/meta-ads-ratos/contas.yaml` para pegar o `conta_anuncio` do cliente.

### 2. Definir o período

Período padrão: últimos 90 dias a partir de hoje.
Calcular `since` (hoje - 90 dias) e `until` (hoje).
Formato: `{"since":"AAAA-MM-DD","until":"AAAA-MM-DD"}`

### 3. Puxar dados da API — executar esses comandos em sequência

**Métricas do ad set (campanha):**
```bash
python3 ~/.claude/skills/meta-ads-ratos/scripts/insights.py adset \
  --id [ADSET_ID] \
  --time-range '{"since":"AAAA-MM-DD","until":"AAAA-MM-DD"}' \
  --fields "impressions,clicks,spend,cpc,cpm,ctr,actions,cost_per_action_type,reach"
```

Extrair:
- `impressions` → Impressões
- `spend` → Investimento total
- `cpm` → CPM
- `reach` → Alcance
- `ctr` → CTR (link clicks / impressions × 100)
- Action `link_click` → Cliques no link
- Cost per `link_click` → CPC
- Action `messaging_conversation_started_7d` → Conversas iniciadas
- Cost per `messaging_conversation_started_7d` → Custo por conversa
- Frequência = impressions / reach

**Breakdown por idade e gênero:**
```bash
python3 ~/.claude/skills/meta-ads-ratos/scripts/insights.py adset \
  --id [ADSET_ID] \
  --time-range '{"since":"AAAA-MM-DD","until":"AAAA-MM-DD"}' \
  --fields "impressions,spend,actions" \
  --breakdown "age,gender"
```

Somar `messaging_conversation_started_7d` por gênero e por faixa etária.
Calcular percentuais sobre o total de conversas.

**Breakdown por posicionamento:**
```bash
python3 ~/.claude/skills/meta-ads-ratos/scripts/insights.py adset \
  --id [ADSET_ID] \
  --time-range '{"since":"AAAA-MM-DD","until":"AAAA-MM-DD"}' \
  --fields "impressions,spend,actions" \
  --breakdown "publisher_platform,platform_position"
```

Para cada posicionamento: conversas, % do total, custo por conversa (spend / conversas).

**Métricas por anúncio** (repetir para cada ad_id):
```bash
python3 ~/.claude/skills/meta-ads-ratos/scripts/insights.py ad \
  --id [AD_ID] \
  --time-range '{"since":"AAAA-MM-DD","until":"AAAA-MM-DD"}' \
  --fields "impressions,clicks,spend,cpc,cpm,ctr,actions,cost_per_action_type,reach"
```

Para listar os anúncios ativos da campanha:
```bash
python3 ~/.claude/skills/meta-ads-ratos/scripts/read.py ads-by-adset --id [ADSET_ID]
```

Calcular por anúncio: investimento, % budget, frequência (impressions/reach), conversas, custo/conv.

### 4. Calcular os dados antes de escrever o HTML

Organizar em uma tabela mental antes de começar:

| Dado | Valor |
|---|---|
| Período | DD/MM/AAAA – DD/MM/AAAA (X dias) |
| Investimento | $ X,XX [moeda] |
| Impressões | X.XXX |
| Alcance | X.XXX |
| Frequência média | X,XX |
| CPM | $ X,XX |
| Cliques no link | XXX |
| CPC | $ X,XX |
| CTR | X,XX% |
| Conversas iniciadas | XXX |
| Custo por conversa | $ X,XX |
| Gênero dominante | X% mulheres |
| Faixa etária top 2 | XX-XX anos (X%) e XX-XX anos (X%) |
| Posicionamento mais barato | [nome] a $ X,XX |

### 5. Gerar o HTML

Usar o template em `~/.claude/skills/relatorio-meta-ads-90d/template-es.html` como base para a versão em espanhol e `template-pt.html` para a versão em português.

Substituir todos os placeholders `{{...}}` com os dados reais.

Verificar:
- Sem travessões (—) em nenhum texto
- Valores numéricos com vírgula como separador decimal (padrão brasileiro/espanhol)
- Moeda correta (MXN, BRL, etc.)

### 6. Salvar os arquivos

**Clientes brasileiros (padrão — maioria dos casos):**
Gerar apenas a versão em português.
Salvar em `clientes/[nome-cliente]/`:
- `relatorio-meta-ads-[mes][ano]-pt.html`

```bash
open clientes/[nome-cliente]/relatorio-meta-ads-[mes][ano]-pt.html
```

**Clientes hispanófonos (ex: Dr. Héctor Durán — México):**
Gerar as duas versões.
Salvar em `clientes/[nome-cliente]/`:
- `relatorio-meta-ads-[mes][ano]-es.html` (espanhol — para o cliente)
- `relatorio-meta-ads-[mes][ano]-pt.html` (português — uso interno DVE)

```bash
open clientes/[nome-cliente]/relatorio-meta-ads-[mes][ano]-es.html
open clientes/[nome-cliente]/relatorio-meta-ads-[mes][ano]-pt.html
```

### 7. Alertas automáticos a verificar

Após calcular os dados, avaliar:
- Frequência > 3,5 → alerta laranja na análise
- CTR < 0,5% → mencionar como ponto de melhoria
- Um anúncio com > 80% do budget → mencionar concentração de risco
- Sem conversas em algum anúncio → mencionar falta de dados para avaliação
- Posicionamento com custo/conv. > 40% acima da média → mencionar como ineficiente

---

## Estrutura do relatório (seções em ordem)

1. Header (logo + dados do cliente + data)
2. Hero (título + subtítulo + fonte)
3. Hero metric (custo por conversa em destaque + 3 métricas secundárias)
4. Métricas da campanha (7 cards: impressões, CPM, cliques, CPC, CTR, conversas, custo/conv.)
5. Desempenho por anúncio (tabela com: anúncio, investimento, % budget, frequência, conversas, custo/conv.)
6. Perfil do público (gênero + faixa etária + posicionamento por custo/conv.)
7. Análise geral da conta (diagnóstico + texto de 3 parágrafos)
8. Próximos passos (cards de ação)
9. Estratégia de criativos (aviso de política Meta + 5 formatos)
10. Footer

---

## Identidade visual padrão

- Background: `#10131c`
- Accent: `#19e65a`
- Text: `#d5dbe6`
- Card: `#16191f`
- Orange (alerta): `#ffa040`
- Font: Inter (Google Fonts)

Para adaptar para outra identidade, trocar as variáveis CSS no `:root`.

---

## Observações importantes

- `messaging_conversation_started_7d` é a métrica confiável para conversas — janela de 7 dias pós-visualização
- Métricas de profundidade (depth_2, depth_3, depth_5) têm inconsistências matemáticas entre si — NÃO usar no relatório
- `messaging_first_reply` pode divergir de `messaging_conversation_started_7d` sem indicar erro — janelas de atribuição diferentes
- Todos os valores monetários vêm na moeda da conta (verificar `moeda` no contas.yaml)
- O símbolo `$` no gerenciador da Meta pode ser USD ou MXN dependendo da conta — sempre confirmar pela moeda configurada
