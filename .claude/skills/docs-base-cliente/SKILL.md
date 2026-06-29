---
name: docs-base-cliente
description: Gera o documento base completo de um cliente de MarketingOps. Consolida dados do onboarding (workspace local + ClickUp), analisa presença digital (Instagram, Google Meu Negócio, Site) e produz um .docx com identidade visual do cliente. Dispara com /docs-base-cliente, "criar docs base", "gerar documento base do cliente", "docs base [cliente]".
---

## O que essa skill faz

Produz o documento estratégico base do projeto para clientes de MarketingOps. É o entregável da tarefa "Analisar Presença Digital" da Fase 2 - Diagnóstico do onboarding.

**Seções geradas:**
1. Diferencial Competitivo e Oferta
2. Público, ICP e Personas
3. Jornada de Compra
4. Funil de Marketing
5. Análise do Instagram (perfil + feed)
6. Análise do Google Meu Negócio
7. Análise do Site

**Arquivos de apoio:**
- `helpers.py` — funções de formatação .docx reutilizáveis (importar no script do cliente)
- `api.py` da skill minuta — TLDV e ClickUp
- Script gerado por cliente: `clientes/{slug}/gerar_docs_base.py`

**Raiz do projeto:** `/Users/macbookairm4/Documents/DVE Assessoria/Claude Code`

Todos os comandos Bash com:
```
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code"
```

---

## Passo 1 — Identificar o cliente

Perguntar ao usuário o nome do cliente (se não estiver claro no contexto).

Definir o `SLUG` do cliente: nome em minúsculas, sem acentos, espaços viram hífens.
Exemplo: "Smart Kon Elevadores" → `smart-kon-elevadores`

Verificar se existe a pasta do cliente:
```bash
ls "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code/clientes/{SLUG}/"
```

Ler o arquivo de base de conhecimento local:
```bash
cat "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code/clientes/{SLUG}/base-conhecimento-onboarding.md"
```

Se o arquivo não existir, avisar o usuário e perguntar se quer continuar só com os dados do ClickUp.

---

## Passo 2 — Double check no ClickUp

Buscar o doc "Docs - {COMPANY}" no ClickUp e ler o conteúdo da página de onboarding para cruzar com o arquivo local.

```python
import sys, os, json, requests

# Carregar credenciais do .env
def load_env():
    d = '/Users/macbookairm4/Documents/DVE Assessoria/Claude Code'
    candidate = os.path.join(d, '.env')
    env = {}
    if os.path.exists(candidate):
        with open(candidate) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    return env

_env = load_env()
CLICKUP_TOKEN = _env.get('CLICKUP_API_TOKEN', '')
WORKSPACE_ID  = '9011393934'
HEADERS = {'Authorization': CLICKUP_TOKEN, 'Content-Type': 'application/json'}

# Buscar todos os docs do workspace
r = requests.get(f'https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs?limit=100', headers=HEADERS)
docs = r.json().get('docs', [])

# Encontrar "Docs - {COMPANY}" (busca por substring)
company_query = '{COMPANY}'.lower()
target = next((d for d in docs if company_query in d['name'].lower() and 'docs' in d['name'].lower()), None)

if not target:
    print(json.dumps({'error': f'Doc não encontrado para {COMPANY}'}))
else:
    doc_id = target['id']
    # Pegar tree de páginas
    r2 = requests.get(
        f'https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs/{doc_id}/pages?content_format=text/md',
        headers=HEADERS
    )
    pages = r2.json() if isinstance(r2.json(), list) else r2.json().get('pages', [])

    # Encontrar página de onboarding
    onboarding_page = next(
        (p for p in pages if 'onboarding' in (p.get('name') or '').lower()),
        pages[0] if pages else None
    )

    if onboarding_page:
        page_id = onboarding_page['id']
        r3 = requests.get(
            f'https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs/{doc_id}/pages/{page_id}?content_format=text/md',
            headers=HEADERS
        )
        content = r3.json().get('content', '')
        print(content[:3000])  # primeiros 3000 chars
    else:
        print(json.dumps({'error': 'Página de onboarding não encontrada no doc'}))
```

**O que fazer com o double check:**
- Comparar os dois textos (local vs ClickUp)
- Se houver divergência, usar o mais completo/recente
- Anotar internamente qualquer informação que aparece num e não no outro para incluir no documento

---

## Passo 3 — Coletar dados da presença digital

Solicitar ao usuário as seguintes informações. Pedir tudo de uma vez:

```
Para gerar o documento completo, preciso analisar a presença digital de [COMPANY]. Pode me enviar:

1. INSTAGRAM
   - Screenshot do perfil completo (foto, nome, username, bio, link na bio, destaques)
   - Screenshot do feed (os primeiros 9-12 posts visíveis)
   - Username do Instagram (para eu tentar buscar também via web)

2. GOOGLE MEU NEGÓCIO
   - Screenshot do painel que aparece no Google ao buscar o nome da empresa
   (nota, avaliações, endereço, horário, fotos visíveis)

3. SITE
   - URL do site da empresa

Pode mandar tudo junto, vou analisar na ordem.
```

Aguardar o usuário enviar os materiais antes de continuar.

---

## Passo 4 — Analisar presença digital

### 4a. Instagram — Perfil

Analisar cada elemento com base nos screenshots:

| Elemento | O que avaliar |
|---|---|
| Foto de perfil | Logo vs. foto pessoal. Legibilidade no formato circular. |
| Username | Clareza, sem caracteres especiais, fácil de digitar. |
| Nome da conta | Indexado na busca. Tem palavra-chave de serviço + cidade? |
| Bio | Fala com a dor do cliente ou descreve a empresa? Tem CTA? Tem social proof? Maiúsculas em excesso? |
| Link na bio | Linktree vs. link direto. Ordem dos links prioriza conversão? WhatsApp é o 1º? |
| Destaques | Cobrem vistoria gratuita, prova social, quem somos, serviços, contato? "Comandos" ou nomes não intuitivos? |

### 4b. Instagram — Feed

Avaliar os primeiros 9-12 posts:

| Dimensão | O que avaliar |
|---|---|
| Mix de conteúdo | % técnico, % pessoal, % genérico, % datas comemorativas |
| Identidade visual | Paleta consistente? Ou templates aleatórios? |
| Persona ativada | Fala com o decisor (síndico, gestor) ou com o usuário final? |
| CTAs | Algum post direciona para a oferta de entrada (vistoria gratuita)? |
| Frequência aparente | Posts recentes? Abandono visível? |
| Social proof | Depoimentos, resultados, equipe em campo? |

### 4c. Google Meu Negócio

| Elemento | O que avaliar |
|---|---|
| Nota e volume | Nota alta é ótimo. Volume baixo para o tempo de empresa é crítico. |
| Foto de capa | Atrai o síndico? Ou é técnica/genérica? |
| Categoria | Específica o suficiente para as buscas do ICP? |
| Descrição | Preenchida? Menciona diferenciais, vistoria gratuita, experiência? |
| Endereço | Coworking/escritório compartilhado exposto? |
| Google Posts / Q&A | Utilizados? |

### 4d. Site

Buscar via WebFetch:
```
WebFetch: {URL_DO_SITE}
Prompt: "Extraia todos os textos exatos da página: headlines, subtítulos, parágrafos, textos de botões, serviços, depoimentos, números, textos do rodapé."
```

| Elemento | O que avaliar |
|---|---|
| Headline | Fala com a dor do cliente ou descreve a empresa? |
| Proposta de valor | Diferenciais reais aparecem? Ou texto genérico? |
| CTA principal | "Contrate-nos" genérico ou CTA com oferta clara? |
| Provas sociais | Depoimentos, avaliações, anos de mercado, clientes? |
| Serviços | Descritos do ponto de vista do cliente ou da empresa? |
| Atualização | Copyright ano. Site abandonado? |

---

## Passo 5 — Coletar identidade visual do cliente

Perguntar ao usuário:

```
Para aplicar a identidade visual do cliente no documento, preciso de:

1. Cor primária da marca (hex ou nome) — ex: #C81010 (vermelho)
2. Cor secundária (hex ou nome) — ex: #2E2E2E (cinza escuro)
3. Alguma cor de destaque adicional? (opcional)
4. Qual é o segmento/nicho do cliente? (ex: manutenção de elevadores, odontologia, advocacia)

Se não tiver os hexadecimais, pode me mandar o logo que eu extraio as cores.
```

Registrar:
- `COR_PRIMARIA` = hex convertido para RGBColor(0xRR, 0xGG, 0xBB)
- `COR_SECUNDARIA` = idem

---

## Passo 6 — Gerar o script Python do cliente

Com todos os dados coletados, gerar o arquivo:
```
clientes/{SLUG}/gerar_docs_base.py
```

### Estrutura obrigatória do script

```python
import sys
sys.path.insert(0, '/Users/macbookairm4/Documents/DVE Assessoria/Claude Code/.claude/skills/docs-base-cliente')
from helpers import *

# ── Configuração do cliente ───────────────────────────────────────────────────
COMPANY  = '{COMPANY}'
SLUG     = '{SLUG}'
OUTPUT   = '/Users/macbookairm4/Documents/DVE Assessoria/Claude Code/clientes/{SLUG}/{COMPANY} - Docs Base.docx'

# Identidade visual (sobrescreve os defaults do helpers.py)
COR_PRIMARIA   = RGBColor(0xRR, 0xGG, 0xBB)  # cor primária do cliente
COR_SECUNDARIA = RGBColor(0xRR, 0xGG, 0xBB)  # cor secundária

# ── Seções ────────────────────────────────────────────────────────────────────

def section_diferencial(doc):
    heading1(doc, 'Diferencial Competitivo e Oferta')
    divider(doc)
    # ... conteúdo real do cliente ...

def section_publico(doc):
    heading1(doc, 'Público, ICP e Personas')
    divider(doc)
    # ... conteúdo real do cliente ...

def section_jornada(doc):
    heading1(doc, 'Jornada de Compra')
    divider(doc)
    # ... conteúdo real do cliente ...

def section_funil(doc):
    heading1(doc, 'Funil de Marketing')
    divider(doc)
    # ... conteúdo real do cliente ...

def section_instagram(doc):
    heading1(doc, 'Análise do Instagram')
    divider(doc)
    # ... análise real baseada nos screenshots ...

def section_gmn(doc):
    heading1(doc, 'Análise do Google Meu Negócio')
    divider(doc)
    # ... análise real baseada no screenshot ...

def section_site(doc):
    heading1(doc, 'Análise do Site')
    divider(doc)
    # ... análise real baseada no WebFetch ...

def main():
    doc = new_doc()
    cover_page(
        doc,
        company_name=COMPANY,
        subtitle='[segmento do cliente]',
        sections_summary='Diferencial Competitivo  •  Público e ICP/Personas  •  Jornada de Compra  •  Funil de Marketing  •  Instagram  •  Google Meu Negócio  •  Site',
        date_str='[Mês de Ano]'
    )
    section_diferencial(doc)
    section_publico(doc)
    section_jornada(doc)
    section_funil(doc)
    section_instagram(doc)
    section_gmn(doc)
    section_site(doc)
    doc.save(OUTPUT)
    print(f'Documento salvo em: {OUTPUT}')

if __name__ == '__main__':
    main()
```

---

## Padrões obrigatórios de qualidade por seção

### Diferencial Competitivo e Oferta
- Listar APENAS diferenciais mencionados explicitamente no onboarding ou verificáveis
- Cada diferencial tem: nome em negrito, descrição de 2-3 linhas explicando POR QUE importa para o cliente
- Oferta: tabela com planos disponíveis, ticket de referência, diferencial de entrada
- Provas disponíveis para anúncios (números verificados, nunca inventados)

### Público, ICP e Personas
- Público alvo: tabela com faixa etária, gênero, localização, tipo de relação com o produto/serviço
- ICP: tipo de cliente ideal, perfil do decisor, situação atual, gatilho de busca, o que valoriza, o que NÃO é cliente ideal
- Mínimo 2 personas, idealmente 3
- Cada persona: nome fictício, idade, cargo, rotina, frustrações com o mercado, como a oferta resolve, ângulo de ataque do anúncio, gatilho de contato, como qualificar o lead
- **Regra de ouro das personas:** A dor deve ser conectada ao papel do decisor, não ao produto. Ex: síndico não tem dor com elevador — tem dor com responsabilidade sem conhecimento.

### Jornada de Compra
- Versão simplificada: fluxo em linha com ">"
- Versão detalhada: cada etapa numerada com O QUE acontece e QUAL É O OBJETIVO da etapa
- Tabela de objeções com como responder

### Funil de Marketing
- Canal atual (antes do tráfego pago)
- Funis por plataforma (Meta, Google)
- Tabela de estratégia de canais
- Observações sobre o perfil digital (pendências identificadas)

### Análise do Instagram
- Diagnóstico rápido: tabela semáforo (verde/amarelo/vermelho) por elemento
- Análise detalhada de cada elemento: status atual + recomendação específica
- Bio: reproduzir o texto atual e propor versão revisada
- Feed: o que parar imediatamente + o que manter + linha editorial recomendada (tabela com pilares)
- Destaques: estrutura recomendada (tabela)
- Link na Bio: ordem recomendada + alternativa de médio prazo

### Análise do Google Meu Negócio
- Diagnóstico rápido: tabela semáforo
- Análise de: avaliações (nota + volume), categoria, fotos, endereço, descrição, Posts/Q&A
- Proposta de texto para a descrição (dentro do limite de 750 caracteres)
- Tabela de ações com responsável e prazo

### Análise do Site
- Reproduzir os textos literais do site atual (headline, missão, serviços)
- Diagnóstico rápido: tabela semáforo
- Análise de: headline, proposta de valor, CTAs, provas sociais, serviços, atualização
- Recomendação de estrutura de landing page de conversão (tabela com seções)
- Nota sobre acesso ao painel/domínio se identificado como pendência

---

## Regras de geração de conteúdo

- Extrair APENAS o que foi explicitamente dito na transcrição ou verificado na análise. Nunca inventar.
- Se um campo não tem dado suficiente, indicar com "[A CONFIRMAR COM O CLIENTE]" em vez de inventar.
- Personas criadas com base no perfil real do decisor descrito no onboarding, não em personas genéricas do mercado.
- Números (anos de empresa, clientes ativos, cidades) sempre baseados no que o cliente disse — nunca arredondados ou aproximados sem indicar.
- Travessão (—) proibido em todo o documento. Usar vírgula ou dois-pontos.
- Sem introduções desnecessárias. Cada seção começa pelo conteúdo, não por "Nesta seção vamos analisar...".

---

## Passo 7 — Executar o script e verificar o output

```bash
cd "/Users/macbookairm4/Documents/DVE Assessoria/Claude Code" && python3 clientes/{SLUG}/gerar_docs_base.py
```

Se der erro de índice em tabela (IndexError: list index out of range), a causa é tabela criada com `rows=N` mas preenchida com N+1 linhas (header + dados). Corrigir: `rows = len(dados) + 1`.

Confirmar o caminho do arquivo gerado e informar ao usuário.

---

## Passo 8 — Criar guias no ClickUp com o conteúdo das seções

Com o conteúdo de todas as seções já gerado em memória (Passo 6), criar/atualizar páginas no doc "Docs - {COMPANY}" do ClickUp.

### 8a. Localizar o doc e listar páginas existentes

```python
import os, json, requests

def load_env():
    candidate = '/Users/macbookairm4/Documents/DVE Assessoria/Claude Code/.env'
    env = {}
    if os.path.exists(candidate):
        with open(candidate) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    return env

_env = load_env()
CLICKUP_TOKEN = _env.get('CLICKUP_API_TOKEN', '')
WORKSPACE_ID  = '9011393934'
HEADERS = {'Authorization': CLICKUP_TOKEN, 'Content-Type': 'application/json'}

# Buscar "Docs - {COMPANY}" se o DOC1_ID não estiver disponível
r = requests.get(f'https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs?limit=100', headers=HEADERS)
docs = r.json().get('docs', [])
target_doc = next((d for d in docs if '{company}'.lower() in d['name'].lower() and 'docs' in d['name'].lower()), None)
DOC1_ID = target_doc['id'] if target_doc else '{DOC1_ID}'

# Listar páginas existentes
r2 = requests.get(
    f'https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs/{DOC1_ID}/pages?content_format=text/md',
    headers=HEADERS
)
pages = r2.json() if isinstance(r2.json(), list) else r2.json().get('pages', [])
pages_by_name = {(p.get('name') or '').lower(): p['id'] for p in pages}
print(json.dumps(pages_by_name, indent=2))
```

### 8b. Mapeamento de seções para páginas

| Seção do Docs Base | Página no ClickUp | Ação |
|---|---|---|
| Diferencial Competitivo e Oferta | Diferencial e Oferta | Criar (não existe) |
| Público, ICP e Personas | ICP e Personas | Atualizar (já existe) |
| Jornada de Compra | Jornada de Compra | Criar (não existe) |
| Funil de Marketing | Tráfego Pago | Atualizar (já existe) |
| Análise do Instagram | Instagram | Criar (não existe) |
| Análise do Google Meu Negócio | Google Meu Negócio | Criar (não existe) |
| Análise do Site | Site | Criar (não existe) |

### 8c. Para cada seção: criar ou atualizar a página

```python
def upsert_page(doc_id, name, content_md, existing_pages_by_name):
    page_id = existing_pages_by_name.get(name.lower())
    if page_id:
        # Atualizar página existente
        r = requests.patch(
            f'https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs/{doc_id}/pages/{page_id}',
            headers=HEADERS,
            json={'content': content_md, 'content_format': 'text/md'}
        )
    else:
        # Criar página nova
        r = requests.post(
            f'https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs/{doc_id}/pages',
            headers=HEADERS,
            json={'name': name, 'content': content_md, 'content_format': 'text/md'}
        )
    return r.status_code, r.json()
```

### 8d. Gerar o conteúdo markdown de cada seção

O conteúdo de cada página deve ser a **versão markdown** do mesmo conteúdo gerado para o .docx. Claude já tem esse conteúdo em memória após o Passo 6. Reexpressar cada seção no formato abaixo e chamar `upsert_page` para cada uma.

**Formato markdown das páginas:**

```markdown
# {Nome da Seção}

{conteúdo completo da seção em markdown}
{tabelas no formato GFM: | col | col |}
{listas com - ou 1. 2. 3.}
{negrito com **texto**}
```

**Regras:**
- Nunca usar travessão (—). Usar vírgula ou dois-pontos.
- Tabelas no formato GFM (pipes `|`).
- Títulos de subseção com `##`.
- Preservar toda a riqueza do conteúdo do .docx — não resumir.
- Se uma análise estava marcada como `[ANÁLISE PENDENTE]` no .docx, manter a mesma marcação.

### 8e. Executar tudo em sequência e reportar

Para cada seção (7 no total), chamar `upsert_page` e exibir o resultado:
```
✅ ICP e Personas — atualizada
✅ Tráfego Pago — atualizada
✅ Diferencial e Oferta — criada
✅ Jornada de Compra — criada
✅ Instagram — criada
✅ Google Meu Negócio — criada
✅ Site — criada
```

---

## Passo 9 — Resumo final para o usuário

Ao concluir, apresentar:

```
Docs Base — {COMPANY} gerado!

.docx
• Arquivo: clientes/{SLUG}/{COMPANY} - Docs Base.docx

ClickUp — Docs - {COMPANY}
• ICP e Personas — atualizada
• Tráfego Pago — atualizada
• Diferencial e Oferta — criada
• Jornada de Compra — criada
• Instagram — criada
• Google Meu Negócio — criada
• Site — criada

Seções incluídas:
• Diferencial Competitivo e Oferta
• Público, ICP e Personas (X personas)
• Jornada de Compra (X etapas)
• Funil de Marketing
• Análise do Instagram (perfil + feed)
• Análise do Google Meu Negócio
• Análise do Site

Pendências identificadas durante a análise:
[listar pendências reais encontradas — acesso ao site, avaliações GMN, etc.]
```

---

## Regras gerais

- Não pular etapas. Cada passo depende do anterior.
- Se qualquer análise estiver incompleta (screenshot não enviado, site fora do ar), registrar no documento com "[ANÁLISE PENDENTE — {motivo}]" e seguir.
- Nunca usar travessão (—) em nenhum texto gerado.
- Sempre que criar uma tabela Python com `doc.add_table(rows=N)`, conferir que N = len(dados) + 1 (header). Erros de índice são sempre dessa causa.
- O arquivo `helpers.py` deve ser importado, nunca copiado. Se o script precisar de funções novas, adicioná-las ao `helpers.py`.
