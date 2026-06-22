---
name: playbook-vendas
description: Gera o Playbook de Vendas personalizado para um cliente do nicho de elevadores. Adapta o template base (equipamentos ou manutenção) com os dados reais do onboarding do cliente. Dispara com /playbook-vendas, "criar playbook de vendas", "gerar playbook", "playbook para [cliente]".
---

## O que essa skill faz

Gera o Playbook de Vendas completo, personalizado para um cliente do nicho de elevadores, com base nos dados coletados na reunião de onboarding.

Suporta dois tipos de playbook:
- **Equipamentos** — para clientes que vendem elevadores, plataformas hidráulicas e similares
- **Manutenção** — para clientes que vendem contratos de manutenção preventiva e/ou corretiva

**Raiz do projeto:** `/Users/macbookairm4/Documents/DVE Assessoria/Claude Code`

---

## Passo 1 — Identificar cliente e tipo

Se o usuário não informou, perguntar:

> "Para qual cliente vou gerar o playbook? E qual o tipo de venda: **equipamentos** (elevadores/plataformas) ou **manutenção** (preventiva/corretiva)?"

Se o cliente já foi mencionado na conversa, usar esse contexto sem perguntar de novo.

---

## Passo 2 — Ler dados do cliente

Ler em paralelo todos os arquivos disponíveis na pasta do cliente:

```bash
cat "clientes/[nome-cliente]/briefing.md"
cat "clientes/[nome-cliente]/base-conhecimento-onboarding.md"
```

Se existirem outros arquivos relevantes (público-alvo, entregáveis, reuniões), lê-los também.

**Extrair do onboarding:**
- Nome da empresa e produtos/serviços
- Região de atuação (cidade principal + secundárias)
- Ticket médio, faixa de valores, margem
- CAC alvo (se calculado ou mencionado)
- Meta mensal (vendas ou contratos)
- Conversão atual (se informada)
- Segmentos do ICP (quem são os clientes ideais)
- Diferenciais competitivos da empresa
- Estrutura do time comercial (quantos vendedores, SDR, etc.)
- CRM que vai ser usado (padrão: Kommo)
- Marca dos equipamentos (ex: Daiken)
- Problemas identificados no processo comercial atual

---

## Passo 3 — Carregar template base

Para **equipamentos** → ler:
```bash
cat "nichos/elevadores/playbook-template-equipamentos.md"
```

Para **manutenção** → ler:
```bash
cat "nichos/elevadores/playbook-template-manutencao.md"
```

---

## Passo 4 — Gerar o playbook personalizado

Usando o template como estrutura e os dados do onboarding como conteúdo, gerar o playbook completo.

**Regras de geração:**

1. **Manter a mesma estrutura de 9 seções do template** — não remover, reordenar ou fundir seções

2. **Substituir todas as variáveis `{{}}` pelos dados reais do cliente** — se o dado não foi informado no onboarding, usar `[A DEFINIR]` e não inventar números

3. **Adaptar os scripts de WhatsApp e ligação** com o nome real da empresa, produto/serviço e contexto do cliente

4. **Personalizar os exemplos de objeções** com os diferenciais competitivos reais e argumentos específicos do segmento do cliente

5. **Adaptar a tabela de dados técnicos** ao produto do cliente — se ele vende só plataformas, remover a tabela de elevadores; se vende manutenção, usar a lista de dados da vistoria

6. **Inserir casos e provas sociais reais** quando disponíveis nos arquivos do cliente — nunca inventar cases

7. **Ajustar os segmentos do ICP** com base no que o cliente relatou como público-alvo no onboarding

8. **Se o cliente tem time comercial pequeno** (sem divisão SDR/vendedor), adaptar o funil para que um único vendedor conduza todas as etapas — indicar isso no playbook com uma nota

9. **Nunca usar travessão (—)** no conteúdo gerado. Substituir por vírgula, dois-pontos ou reescrever a frase

10. **Tom direto e prático** — o playbook será lido por vendedores, não por gestores. Scripts devem soar naturais na fala, não robotizados

**Variáveis prioritárias a preencher:**

| Variável | Fonte de dados |
|---|---|
| `{{EMPRESA}}` | briefing.md ou onboarding |
| `{{PRODUTOS}}` / `{{SERVICOS_MANUTENCAO}}` | briefing.md |
| `{{TICKET_MEDIO}}` / `{{TICKET_MEDIO_MENSAL}}` | onboarding — seção de ticket médio |
| `{{MARGEM}}` | onboarding — seção de margem |
| `{{CAC_ALVO}}` | onboarding — cálculo de CAC ou estimativa |
| `{{META_MENSAL}}` / `{{META_CONTRATOS}}` | onboarding — metas definidas |
| `{{REGIAO_PRINCIPAL}}` | onboarding — região de atuação |
| `{{LISTA_DIFERENCIAIS}}` | onboarding — seção de diferenciais competitivos |
| `{{TABELA_SEGMENTOS_ICP}}` | onboarding — seção de público-alvo |
| `{{CRM}}` | onboarding ou briefing — padrão: Kommo |

---

## Passo 5 — Salvar o playbook

Salvar o playbook gerado em:

```
clientes/[nome-cliente]/playbook-vendas.md
```

Confirmar ao usuário:

> "Playbook de [tipo] gerado para [EMPRESA] e salvo em `clientes/[nome-cliente]/playbook-vendas.md`."

---

## Notas para edge cases

**Se o cliente vende equipamentos E manutenção:**
Gerar dois arquivos separados:
- `clientes/[nome-cliente]/playbook-vendas-equipamentos.md`
- `clientes/[nome-cliente]/playbook-vendas-manutencao.md`

**Se o onboarding está incompleto ou não existe:**
Informar o usuário sobre quais dados estão faltando antes de gerar o playbook. Não gerar com lacunas que comprometam a qualidade do documento.

**Se o cliente não usa CRM:**
Manter as referências a CRM no funil, mas adicionar uma nota no início do documento: "O CRM será configurado em breve. Até lá, registre as informações de cada lead em planilha ou caderno seguindo as mesmas etapas."
