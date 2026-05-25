---
name: copy-ads
description: >
  Cria copy para anúncios de tráfego pago (Meta Ads e Google Ads).
  Gera textos para diferentes formatos: vídeo (hook + roteiro), estático/carrossel
  (primary text + headline), e anúncios de pesquisa Google (headlines + descriptions).
  Use quando o usuário pedir "copy de anúncio", "texto de anúncio", "copy pra meta",
  "copy pra google", "hook", "roteiro de anúncio", "headline", "texto do ad".
---

# /copy-ads — Copy para Anúncios

## Dependências

- **Tom de voz:** `.contexto/preferencias.md`
- **Briefing do cliente:** `clientes/[nome-cliente]/briefing.md` (ler sempre que existir)
- **Contexto de nicho:** `nichos/[nicho]/README.md` (se existir)

---

## Workflow

### Passo 1 — Coletar o briefing

Ler o briefing do cliente se existir. Se já tiver o contexto suficiente, pular as perguntas já respondidas.

Perguntar apenas o que estiver faltando:

1. "Para qual cliente e produto/serviço é o anúncio?"
2. "Qual o objetivo do anúncio? (gerar leads, vender diretamente, aquecer audiência, remarketing)"
3. "Para qual plataforma? (Meta Ads, Google Ads ou ambas)"
4. "Qual formato? (vídeo, imagem estática, carrossel, pesquisa Google)"
5. "Qual a principal dor ou desejo da audiência que esse anúncio precisa ativar?"
6. "Tem algum CTA definido? (WhatsApp, formulário, landing page, loja)"

Se o usuário já tiver dado contexto suficiente no briefing ou na conversa, não repetir as perguntas. Extrair e confirmar em uma linha antes de começar.

### Passo 2 — Identificar o ângulo

Com base na dor/desejo informado, escolher o melhor ângulo para o anúncio:

- **Dor direta:** nomear o problema de forma visceral, sem rodeios
- **Resultado desejado:** mostrar o estado depois, o que o cliente quer alcançar
- **Prova social:** depoimento, caso de sucesso, número concreto
- **Curiosidade:** abrir uma pergunta ou dado surpreendente que puxa o clique
- **Objeção reversa:** nomear a desculpa que impede a compra e virar ela

Quando não houver ângulo óbvio, gerar 2 opções com ângulos diferentes e deixar o usuário escolher.

### Passo 3 — Gerar a copy

#### Formato: Vídeo (Meta Ads)

Gerar um roteiro estruturado:

**Hook (0-3 segundos):** frase de abertura que para o scroll. Deve ser específica, inesperada ou provocar identificação imediata. Gerar 3 opções de hook para o usuário escolher.

**Corpo (3-30 segundos):** desenvolvimento do problema ou resultado. Direto, em ritmo de fala. Parágrafos curtos. Sem transições artificiais.

**CTA (últimos 5 segundos):** instrução clara e única. Sem múltiplas opções de ação.

---

#### Formato: Imagem Estática ou Carrossel (Meta Ads)

**Primary Text (o texto acima da imagem):**
- Versão curta (até 125 caracteres, ideal para mobile sem "ver mais")
- Versão longa (até 500 caracteres, quando a dor precisa de mais contexto)

**Headline (negrito abaixo da imagem):**
- 3 opções, até 40 caracteres cada
- Deve completar o sentido da primary text ou reforçar o benefício

**Description (texto menor abaixo do headline):**
- 1 opção, até 30 caracteres
- Reforço do CTA ou do diferencial

Para carrossel: gerar headline específico para cada slide se o usuário fornecer o tema de cada um.

---

#### Formato: Pesquisa Google (Google Ads)

**Headlines:** gerar 10-15 opções variadas (até 30 caracteres cada)
- Variações com: problema, solução, localização, prazo, diferencial, prova social, pergunta
- Misturar estilos para o sistema do Google testar combinações

**Descriptions:** gerar 4-6 opções (até 90 caracteres cada)
- Cada uma com ângulo diferente: benefício principal, urgência, prova, objeção

---

### Passo 4 — Salvar e entregar

Salvar o arquivo em `conteudo/[nome-cliente]-copy-ads-[data].md`

Mostrar a copy formatada na conversa também, para o usuário já visualizar.

Perguntar: "Quer mais variações de algum elemento ou ajustar o ângulo?"

---

## Regras de escrita

**Proibido em qualquer copy, sem exceção:**
- Travessão (—): nunca usar. Substituir por vírgula, ponto, dois-pontos ou reescrever a frase
- Estrutura "Isso não é X. Isso é Y." em qualquer variação — virou clichê
- Frases de impacto vazias: "transforme sua vida", "eleve seus resultados", "leve seu negócio ao próximo nível"
- Entusiasmo artificial: "Incrível!", "Surpreendente!", "Você não vai acreditar..."
- Adjetivos inflados sem prova: "o melhor", "o único", "revolucionário"

**O que funciona:**
- Especificidade: número, prazo, nome do nicho, situação concreta
- Linguagem do cliente: usar as palavras que a audiência usaria, não jargões do marketing
- Ritmo de fala em vídeos: frases que respiram, pontuação que guia a pausa
- Começar pelo problema ou pelo resultado — nunca pela empresa ou pelo produto

**Tom geral:**
- Direto, sem rodeios
- Informal o suficiente para não parecer corporativo
- Profundo o suficiente para gerar identificação real
- Humanizado — soa como alguém que entende o problema, não como propaganda
