---
name: relatorio-trafego
description: Gera relatório mensal de tráfego pago em HTML com dados reais do Meta Ads e Google Ads, seguindo a identidade visual da DVE Assessoria. Salva em relatorios/[cliente]/ pronto para upload no cPanel.
metadata:
  type: skill
---

# Skill: Relatório de Tráfego Pago

Gera um arquivo HTML completo com dados reais das plataformas, identidade visual da DVE, e pronto para subir no cPanel.

## Passo 1 — Coletar informações

Perguntar ao usuário:
1. **Qual cliente?** (verificar se existe briefing em `clientes/[nome]/briefing.md` e ler)
2. **Qual período?** (mês e ano — ex: maio/2026)
3. **Quais plataformas?** Meta Ads, Google Ads, ou ambas

Se o cliente não estiver claro, listar as pastas em `clientes/` para ajudar.

## Passo 2 — Puxar dados das plataformas

### Meta Ads

Rodar em sequência:

```bash
# Insights gerais da conta no período
python3 ~/.claude/skills/meta-ads-ratos/scripts/insights.py account \
  --account ACT_ID \
  --since YYYY-MM-01 \
  --until YYYY-MM-31 \
  --fields spend,impressions,reach,clicks,ctr,cpm,cpc,actions,cost_per_action_type

# Desempenho por campanha
python3 ~/.claude/skills/meta-ads-ratos/scripts/insights.py campaign \
  --account ACT_ID \
  --since YYYY-MM-01 \
  --until YYYY-MM-31 \
  --fields campaign_name,spend,impressions,clicks,ctr,actions,cost_per_action_type \
  --limit 10
```

Extrair:
- Investimento total (spend)
- Impressões, alcance (reach), cliques (link clicks)
- CTR, CPM, CPC médio
- Conversões (actions onde action_type = lead ou purchase) e custo por conversão
- Top 5 campanhas por conversão ou por spend

### Google Ads

```bash
# Insights gerais da conta
python3 ~/.claude/skills/google-ads-ratos/scripts/insights.py account \
  --customer-id CUSTOMER_ID \
  --start-date YYYY-MM-01 \
  --end-date YYYY-MM-31

# Desempenho por campanha
python3 ~/.claude/skills/google-ads-ratos/scripts/insights.py campaign \
  --customer-id CUSTOMER_ID \
  --start-date YYYY-MM-01 \
  --end-date YYYY-MM-31

# Top keywords
python3 ~/.claude/skills/google-ads-ratos/scripts/insights.py keyword \
  --customer-id CUSTOMER_ID \
  --start-date YYYY-MM-01 \
  --end-date YYYY-MM-31
```

Extrair:
- Investimento total, impressões, cliques, CTR
- CPC médio
- Conversões e custo por conversão
- Top 5 campanhas por conversão
- Top 5 keywords por conversão

Para obter os IDs de conta, consultar `~/.claude/skills/meta-ads-ratos/contas.yaml` (Meta) e `~/.claude/skills/google-ads-ratos/.env` (Google). Se o cliente não estiver mapeado, perguntar o ID.

## Passo 3 — Calcular consolidados

Com os dados de ambas as plataformas:
- **Investimento total** = Meta spend + Google spend
- **Total de conversões/leads** = Meta conversões + Google conversões
- **CPL médio** = Investimento total / Total de conversões
- Calcular variação vs. mês anterior se o usuário tiver esse dado

## Passo 4 — Gerar o HTML

Gerar um único arquivo HTML completo e autocontido (sem dependências locais — apenas CDNs).

### Identidade visual obrigatória

```css
/* Cores */
--bg-primary: #0F2A33;
--bg-card: #1E2328;
--accent: #01FF96;
--text: #F4F3EE;
--text-muted: rgba(244, 243, 238, 0.6);
--border: rgba(244, 243, 238, 0.1);

/* Fontes via Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Plus+Jakarta+Sans:wght@300;400;500&display=swap');

/* Títulos: Montserrat Bold */
/* Corpo: Plus Jakarta Sans Regular */
/* Subtítulos: Plus Jakarta Sans Light */
```

### Estrutura do relatório

```
1. HEADER
   - Logo DVE (se existir em marca/logo.svg ou marca/logo.png, incluir como base64 ou usar texto "DVE Assessoria")
   - Nome do cliente + período
   - Badge de plataformas incluídas (Meta, Google, ou ambas)

2. RESUMO EXECUTIVO
   - 3 ou 4 cards de KPI: Investimento Total | Leads/Conversões | CPL Médio | [ROAS se tiver e-commerce]
   - Cards com fundo #1E2328, número em destaque na cor #01FF96, label em text-muted

3. SEÇÃO META ADS (se incluído)
   - Header da seção com ícone/badge "Meta Ads"
   - Cards de métricas: Investimento | Impressões | Alcance | Cliques | CTR | CPM | CPC | Conversões | CPL
   - Gráfico de barras horizontais: top campanhas por conversão (Chart.js)
   - Tabela: top 5 campanhas com colunas (Campanha | Investimento | Cliques | CTR | Conversões | CPL)

4. SEÇÃO GOOGLE ADS (se incluído)
   - Header da seção com badge "Google Ads"
   - Cards de métricas: Investimento | Impressões | Cliques | CTR | CPC | Conversões | CPL
   - Gráfico de barras horizontais: top campanhas (Chart.js)
   - Tabela: top 5 campanhas com colunas (Campanha | Investimento | Cliques | CTR | Conv. | CPL)
   - Tabela: top 5 keywords (Keyword | Cliques | CTR | Conv. | CPL)

5. RODAPÉ
   - "Relatório gerado por DVE Assessoria · dveassessoria.com.br"
   - Período de referência
   - Data de geração
```

### Regras de design HTML

- `background: #0F2A33` no body e html
- Cards com `background: #1E2328`, `border-radius: 10px`, `border: 1px solid rgba(244,243,238,0.1)`
- Números principais (KPIs) em `color: #01FF96`, `font-family: Montserrat`, `font-weight: 700`
- Labels e textos secundários em `color: rgba(244,243,238,0.6)`
- Tabelas com linhas separadas por `border-bottom: 1px solid rgba(244,243,238,0.08)`
- Sem sombras pesadas — profundidade por contraste
- Responsivo: grid de cards vira 1 coluna em mobile (max-width: 600px)
- Padding generoso: cards com `padding: 24px`, seções com `padding: 48px 0`

### Gráficos Chart.js

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

Configuração padrão dos gráficos:
```javascript
Chart.defaults.color = '#F4F3EE';
Chart.defaults.borderColor = 'rgba(244,243,238,0.1)';

// Barras horizontais: cor #01FF96 com opacidade 0.8
// backgroundColor: 'rgba(1, 255, 150, 0.8)'
// borderColor: '#01FF96'
```

### Formatação dos números

- Valores em R$: `R$ 1.250,00` (ponto para milhar, vírgula para decimal)
- Percentuais: `2,34%`
- Números grandes: `12.450` (com ponto para milhar)
- CPL, CPC: sempre 2 casas decimais

## Passo 5 — Salvar o arquivo

```
relatorios/[nome-cliente]/[mes]-[ano].html
```

Exemplos:
- `relatorios/altitude-elevadores/maio-2026.html`
- `relatorios/mm-medicina/maio-2026.html`

Se a pasta do cliente não existir dentro de `relatorios/`, criar automaticamente.

## Passo 6 — Publicar automaticamente no servidor

Carregar credenciais FTP:
```bash
source .claude/skills/relatorio-trafego/ftp.env
```

Criar pasta do cliente no servidor (se não existir):
```bash
curl -s --connect-timeout 10 \
  ftp://$FTP_HOST/ \
  --user "$FTP_USER:$FTP_PASS" \
  -Q "MKD $FTP_BASE_PATH/[nome-cliente]" 2>&1 || true
```

Fazer upload do arquivo:
```bash
curl -s --connect-timeout 30 \
  -T "relatorios/[nome-cliente]/[mes]-[ano].html" \
  ftp://$FTP_HOST/$FTP_BASE_PATH/[nome-cliente]/[mes]-[ano].html \
  --user "$FTP_USER:$FTP_PASS"
```

Se o upload funcionar (sem erro), informar ao usuário:

> Relatório publicado com sucesso.
> Link: `https://dveassessoria.com.br/relatorios/[nome-cliente]/[mes]-[ano].html`

Se der erro, informar a mensagem de erro e orientar a fazer o upload manual via File Manager no CyberPanel.

## Observações

- Se não houver conversões configuradas na plataforma, usar cliques como métrica principal e informar isso no relatório com uma nota discreta
- Se um cliente tiver só Meta ou só Google, omitir a seção da plataforma que não usa e ajustar o resumo executivo
- Não inventar dados — se um script retornar erro ou dado vazio, informar o usuário antes de gerar o relatório
- O arquivo gerado é autocontido: funciona offline após o carregamento inicial das fontes e do Chart.js via CDN
