# TEMPLATE — Playbook de Vendas: Equipamentos

> Use este arquivo como base para gerar o playbook de um novo cliente.
> Substitua todas as variáveis `{{VARIAVEL}}` pelos dados reais do onboarding.
> Variáveis disponíveis no final deste arquivo.

---

# Introdução

**{{EMPRESA}}**

{{PRODUTOS}}

---

**PLAYBOOK DE VENDAS**

*Processos Comerciais • Qualificação • Roteiros • Objeções • CRM*

---

Elaborado por DVE Assessoria — {{MES_ANO}}

*Documento confidencial — uso exclusivo do time comercial {{EMPRESA}}*

---

**Como usar este Playbook?**

O playbook é o guia prático do time comercial da **{{EMPRESA}}**. Ele padroniza cada etapa do atendimento, do primeiro contato ao fechamento, e serve de base para a configuração do {{CRM}}.

Leia uma vez do início ao fim. Depois, use como consulta rápida durante os atendimentos.

| O que você vai encontrar | Números de referência |
|---|---|
| 1. Perfil do cliente ideal (ICP) | Ticket médio: {{TICKET_MEDIO}} |
| 2. Funil de vendas e etapas no {{CRM}} | Faixa: {{TICKET_MIN}} a {{TICKET_MAX}} |
| 3. Qualificação LS-NBT | Margem bruta: {{MARGEM}} |
| 4. Roteiros de abordagem (WhatsApp) | CAC alvo: {{CAC_ALVO}} / venda |
| 5. Diagnóstico de necessidades | Conversão atual: {{CONVERSAO_ATUAL}} |
| 6. Condução da proposta e negociação | Meta: {{META_MENSAL}} equipamentos / mês |
| 7. Follow-up estruturado | Região: {{REGIAO_PRINCIPAL}} ({{PERCENTUAL_REGIAO_PRINCIPAL}}%) + {{REGIAO_SECUNDARIA}} |
| 8. Mapeamento de objeções | |
| 9. Gatilhos de avanço no CRM | |

---

# ICP — Perfil do Cliente Ideal

Antes de qualificar qualquer lead, o vendedor precisa saber para quem a {{EMPRESA}} quer vender.

## Segmentos prioritários

| Segmento | Perfil típico | Produto |
|---|---|---|
{{TABELA_SEGMENTOS_ICP}}

## Sinais de lead qualificado vs. desqualificado

| Qualificado | Desqualificado |
|---|---|
| Tem obra ou projeto definido | Só está "pesquisando preço" |
| Decisor presente | Não tem poder de decisão |
| Localização: {{REGIAO_PRINCIPAL}} ou {{REGIAO_SECUNDARIA}} | Fora da área de atendimento |
| Orçamento compatível (≥ {{TICKET_MIN}}) | Quer produto abaixo de {{TICKET_MIN_DESCONTO}} |
| Engajou na conversa e gerou orçamento | Não respondeu e sumiu |

---

# Processo Comercial — Funil de Vendas

O funil define as etapas do pipeline no {{CRM}}. Cada etapa tem critério claro de entrada e saída.

| ETAPAS SDR — PRÉ-VENDAS | | |
|---|---|---|
| **Etapa** | **O que acontece** | **Ação do SDR** |
| 1. Novo Lead | Lead chegou (WhatsApp, Instagram, Google, indicação) | — |
| 2. BOT | Perguntas automáticas de qualificação pelo BOT | — |
| 3. Follow Up 1/2/3 | Lead não respondeu o BOT | Aguardar follow-up automático |
| 4. Atendimento SDR | Lead respondeu — aguardando contato humano | Ligar em até 5 minutos após resposta do BOT |
| 5. Aguardando Dados | Dados técnicos solicitados, pendentes de envio | Acompanhar até ter todos os dados para orçamento |
| 6. Follow Up 1/2/3 | Lead não enviou os dados | Aguardar follow-up automático |

| ETAPAS VENDEDOR — VENDAS | | |
|---|---|---|
| **Etapa** | **O que acontece** | **Ação do Vendedor** |
| 7. Fazer/enviar orçamento | Dados coletados — montar e enviar orçamento | Ligar para apresentar orçamento pessoalmente |
| 8. Orçamento Enviado | Orçamento enviado, sem resposta ainda | Follow-up por ligação e WhatsApp |
| 9. Follow Up 1/2/3 | Lead não fechou | Aguardar follow-up automático |
| 10. Venda Ganha | Venda realizada | Passar para pós-venda |
| 11. Venda Perdida | Venda não realizada | Registrar motivo da perda |
| 12. Nutrição | Lead sem resposta há mais de 14 dias | Contato mensal de reengajamento |

> **Importante:** caso não seja possível dividir o time em pré-vendas e vendas, o mesmo vendedor conduz o lead do início ao fim.

---

# Qualificação de Leads — LS-NBT

Aplique assim que o lead entrar em contato, preferencialmente ainda no WhatsApp, antes de agendar visita.

**Fluxo:** L (Localização) → S (Situação) → N (Necessidade) → B (Budget) → T (Timeline)

> **Regra de ouro:** antes de ligar para o lead que respondeu o BOT, verifique as respostas e confirme se são verdadeiras.

## L — Localização

> Filtro geográfico. Leads fora de {{REGIAO_PRINCIPAL}} e {{REGIAO_SECUNDARIA}} são desqualificados.

**Pergunta do BOT:** "Antes de iniciar seu atendimento, me confirma: qual será o local (cidade e estado) de instalação do equipamento?"

## S — Situação: Qual é o tipo de projeto?

**Pergunta do BOT:** "Qual o tipo de equipamento que você está buscando? [{{OPCOES_EQUIPAMENTO}}]"

**Pergunta do BOT:** "Para eu te ajudar melhor: o equipamento é para qual tipo de projeto? [Residencial / Comercial / Industrial / Modernização]"

## N — Necessidade: Qual é a dor?

**Pergunta do BOT:** "O que motivou você a buscar {{PRODUTO_SINGULAR}} agora?"

> O vendedor usa essa resposta para personalizar a abordagem por telefone.

## B — Budget

**Pergunta do BOT:** "Nossos equipamentos estão a partir de {{TICKET_MIN}}. Esse valor de investimento faz sentido para você?"

## T — Timeline

**Pergunta do BOT:** "Qual é o prazo que você precisa ter o equipamento instalado?"

---

# Atendimento Inicial — WhatsApp e Ligação

> **Regra de ouro:** entrar em contato com o lead em no máximo 5 minutos. Esse tempo de resposta pode aumentar 21x a chance de fechar negócio.

## Dados técnicos necessários para orçamento

{{TABELA_DADOS_TECNICOS}}

> Orçamento sem dados técnicos completos é estimativa — e estimativa pode gerar orçamentos equivocados que prejudicam a margem.

## Script WhatsApp — SDR (até 5 min após BOT)

Leia TODAS as respostas do BOT antes de escrever a mensagem.

| Bloco | Objetivo |
|---|---|
| 1. Apresentação | Se apresentar (nome e empresa) |
| 2. Confirmação BOT | Confirmar o que o lead respondeu |
| 3. Solução | Mostrar que a {{EMPRESA}} tem solução para o perfil do lead |
| 4. CTA para ligação | Criar expectativa e obter confirmação de disponibilidade |

**Mensagem base:**

> Olá, [NOME DO LEAD]! Tudo bem?
>
> Sou o [NOME DO SDR], da equipe {{EMPRESA}}. Tentei te ligar agora porém não obtive retorno.
>
> Recebi suas respostas aqui e já vi que você está buscando [TIPO DE EQUIPAMENTO] para [RESUMO DA NECESSIDADE].
>
> Aqui na {{EMPRESA}} trabalhamos exatamente com esse tipo de projeto e temos soluções sob medida para [SEGMENTO].
>
> Para te apresentar as melhores opções e montar um orçamento personalizado, gostaria de te ligar rapidamente. Você tem disponibilidade agora ou prefere [SUGESTÃO DE HORÁRIO]?

## Variações por perfil de lead

| Situação (BOT) | Mensagem âncora |
|---|---|
| Residencial | "{{MSG_ANCORA_RESIDENCIAL}}" |
| Comercial / Construtora | "{{MSG_ANCORA_COMERCIAL}}" |
| Industrial | "{{MSG_ANCORA_INDUSTRIAL}}" |
| Modernização | "{{MSG_ANCORA_MODERNIZACAO}}" |

## Script de Ligação — Vendedor

**Estrutura:**
1. Abertura — apresentação + confirmar disponibilidade
2. Confirmação — validar respostas do BOT
3. Coleta de dados técnicos
4. Próximos passos e comprometimento

**Abertura:**
> "Olá, [NOME]! Aqui é o [NOME DO VENDEDOR] da {{EMPRESA}}. Recebi seus dados e vi que você tem interesse em nosso equipamento. Você tem 10 minutos para a gente conversar e eu entender qual o tipo de equipamento você precisa?"

**Confirmação:**
> "Antes de tudo, quero confirmar o que você nos informou. Você mencionou que o projeto é [TIPO], localizado em [CIDADE], e que está buscando [EQUIPAMENTO] por conta de [NECESSIDADE]. Isso está correto? Tem alguma informação que queira complementar?"

**Encerramento:**
> "Perfeito, [NOME], já tenho o que preciso para montar um orçamento personalizado para você. Vou preparar tudo e te ligo [PRAZO]. Só preciso que você me envie [DADO PENDENTE] ainda hoje pelo WhatsApp. Consegue fazer isso?"

**Mensagem pós-ligação:**
> "[NOME], foi um prazer conversar! Conforme combinamos, vou preparar o seu orçamento até [DATA]. Só preciso que você me envie [DADO PENDENTE] aqui pelo WhatsApp."

---

# Negociação — Condução da Proposta

## Apresentação da proposta

> [Vendedor — WhatsApp]
> "Oi, [Nome]! Tudo bem? Aqui é o [Nome Vendedor] da {{EMPRESA}}. Preparei sua proposta com base no que você me contou sobre [resumo do projeto]. Estou com ela em mãos, consigo te ligar agora?"

**Como apresentar o preço:**
> "O investimento para esse projeto [contexto e especificações] é de [Valor]. Isso inclui equipamento, instalação, [X] meses de garantia com suporte técnico da {{EMPRESA}}. E para fechar o negócio te dou o frete grátis para [endereço]. Fechando hoje, consigo priorizar o seu projeto e entregar no prazo [X]. Qual o melhor e-mail para encaminhar o contrato agora?"

> **Importante:** incluir o valor do frete no orçamento e ofertar como Frete Grátis. Avaliar possibilidade de oferecer {{MESES_MANUTENCAO_GRATIS}} meses de manutenção preventiva grátis como argumento de negociação.

## Diferenciais para fechamento

{{LISTA_DIFERENCIAIS}}

## Quando o lead pede desconto

Regra: nunca conceda desconto sem contrapartida.

| Estratégia | Como usar |
|---|---|
| Âncora de valor | Reforce o que está incluído: "Esse valor já contempla instalação, equipamento, documentação, frete e garantia." |
| Contrapartida | "Consigo um desconto de [valor] se você fizer o pagamento à vista." / "Te dou desconto se fechar [X] anos de manutenção." |
| Alternativa de produto | Ofereça um produto de entrada se o orçamento for realmente restritivo. |
| Divisão do projeto | Para projetos grandes: "Podemos instalar a plataforma agora e o elevador na segunda fase." |

---

# Follow-Up Estruturado

Mensagens organizadas em 4 blocos:
1. Follow-up do BOT
2. Follow-up de Dados
3. Follow-up Pós Orçamento
4. Nutrição

## Follow-Up BOT — Lead não respondeu o atendimento automático

| FU | Quando dispara | Mensagem automática |
|---|---|---|
| FU 1 | 10 min sem resposta | "Oi, [Nome]! Vi que você entrou em contato com a {{EMPRESA}}. Consigo te ligar agora para dar sequência no seu atendimento?" |
| FU 2 | 3h sem resposta | "[Nome]! Não quero perder a chance de te ajudar. {{MSG_FU2_BOT}} Segue o nosso portfólio [Enviar portfólio]" |
| FU 3 | 24h sem resposta | "Olá, aqui é o [vendedor] da {{EMPRESA}}. {{MSG_FU3_BOT}} Quando consigo te ligar?" |

## Follow-Up Dados — Lead não enviou informações para orçamento

| FU | Quando dispara | Mensagem SDR |
|---|---|---|
| FU 1 | 4h após solicitação | "Oi, [Nome]! Nossa equipe só está esperando os dados para finalizar sua proposta. [Enviar foto de exemplo]" |
| FU 2 | Dia seguinte | "Olá, [Nome]! Para montar uma proposta certeira para o seu projeto, preciso dos [dados pendentes]. Você consegue me passar isso hoje?" |
| FU 3 | 3 dias após solicitação | **SDR ligar:** "Oi, [Nome]! [Rapport inicial]. Para finalizar o seu orçamento eu preciso dos [dados pendentes]. Se preferir, pode me passar o contato do [arquiteto/responsável] que eu solicito diretamente." |

## Follow-Up Pós Orçamento — Lead recebeu e parou de responder

| FU | Quando dispara | Ação |
|---|---|---|
| FU 1 | 24h após envio | **Ligar:** "[Nome], bom demais? Aqui é o [Vendedor] da {{EMPRESA}}. Você analisou a proposta com [pessoa envolvida]?" |
| FU 2 | 3 dias após envio | **Ligar:** "Abrindo o jogo pra você, não consigo manter o [prazo] se a gente não fechar essa semana. Nossa agenda de instalações para [mês] está quase encerrada. Sendo sincero, o que está impedindo de fechar negócio?" |
| FU 3 | 7 dias após envio | **WhatsApp:** "[Nome]! A sua proposta contém o [equipamento X]. Queria te mostrar [equipamento X] que acabamos de entregar para um cliente. [Enviar foto] Faz sentido deixar reservado para você ou posso passar para frente?" |

## Nutrição — Lead sem resposta há mais de 14 dias

Frequência: 1 mensagem por mês.

| Mês / Tema | Mensagem |
|---|---|
| Mês 1 — Ativação | "{{MSG_NUTRICAO_1}}" |
| Mês 2 — Autoridade | "{{MSG_NUTRICAO_2}}" |
| Mês 3 — Prova social | "{{MSG_NUTRICAO_3}}" |

---

# Objeções

## A lógica antes dos scripts

A objeção que o lead declara raramente é o problema real. É uma proteção. O trabalho do vendedor não é argumentar contra a objeção declarada — é diagnosticar o que está por trás dela.

## Framework VIRE

| Etapa | Nome | O que fazer |
|---|---|---|
| V | Validar | Acolher sem resistência. Nunca discorde de imediato. |
| I | Isolar | Confirmar se é a única barreira ou se há outra por trás. |
| R | Resolver | Contornar a objeção com a resposta certa para o problema certo. |
| E | Encaminhar | Conduzir para o fechamento. Objeção resolvida sem CTA = perdeu a venda. |

**Regras de ouro:**
- Nunca contradiga uma objeção diretamente
- Nunca responda sem fazer pelo menos uma pergunta de diagnóstico
- O silêncio depois da pergunta é seu aliado — espere o lead falar
- Objeção resolvida sem próximo passo não é objeção resolvida

## Objeções mapeadas

### O1 — "Está caro."

| Etapa | Script |
|---|---|
| V | "Entendo, [NOME]. Preço é uma das coisas mais importantes em uma decisão dessa." |
| I | "Posso te fazer uma pergunta antes? Além do valor, tem mais alguma coisa impedindo de fechar negócio?" |
| R | "Quando você diz que está caro, está comparando com outro orçamento, com o valor que tinha em mente ou com o orçamento disponível?" [Se comparação com concorrente → O3] [Se limitação de orçamento → argumento de custo do retrofit] [Se percepção de valor → detalhar item por item] |
| E | "Quer que eu detalhe item por item o que está incluído? Assim você consegue comparar com as outras propostas. Levo 5 minutos." |

### O2 — "Vou pensar e te dou um retorno."

| Etapa | Script |
|---|---|
| V | "Claro, [NOME], faz todo sentido. Uma decisão dessas precisa de análise." |
| I | "Só para eu entender melhor: o que você ainda precisa resolver antes de tomar a decisão?" |
| R | [Precisa consultar sócio/esposa] → "Posso apresentar o projeto para [sócio/esposa] também, assim tiro todas as dúvidas de uma vez." [Quer comparar orçamentos] → "As condições que te ofereci agora são para fechamento neste momento. Nossos prazos variam pelo volume de clientes." [Resposta vaga] → "Há algo na proposta que não ficou claro ou gerou dúvida?" |
| E | "Vou te enviar a proposta organizada pelo WhatsApp. Você analisa com calma e te ligo [PRAZO] para tirar qualquer dúvida. Fechado?" |

### O3 — "Recebi um orçamento mais barato."

| Etapa | Script |
|---|---|
| V | "Faz todo sentido comparar, você está fazendo certo, [NOME]." |
| I | "Além do preço, tem mais alguma coisa pesando na sua decisão?" |
| R | "Me conta sobre o outro orçamento — o que estava incluso? Era o mesmo tipo de equipamento, mesma capacidade e paradas?" [Diferenciar as propostas e realçar os diferenciais da {{EMPRESA}}] "O que costuma diferenciar muito no setor é: quem fabrica, o que cobre a garantia, quem faz a manutenção e se a documentação técnica está incluída." |
| E | "Você tem o outro orçamento aqui? Posso analisar com você agora mesmo, levo menos de 10 minutos." |

### O4 — "Preciso de aprovação da diretoria / arquiteto / sócio."

| Etapa | Script |
|---|---|
| V | "Totalmente compreensível, [NOME]. Decisão desse porte com mais de uma pessoa é a forma mais responsável." |
| I | "Fora a aprovação, tem mais alguma coisa em aberto?" |
| R | "O que a diretoria/arquiteto/sócio vai querer saber antes de aprovar? Posso preparar um dossiê técnico e comercial com exatamente essas informações." |
| E | "Quando é essa reunião de aprovação? Quero garantir que você tenha o material antes." |

### O5 — "Ainda não tenho o projeto definido."

| Etapa | Script |
|---|---|
| V | "Entendo, [NOME]. Projeto em maturação é completamente normal." |
| I | "Em que fase está o projeto agora? Tem alguma data de referência — início de obra, entrega, prazo de regularização?" |
| R | "Vamos fazer uma análise preliminar gratuita com o que você já tem. Sem compromisso. Isso te dá uma estimativa real para incluir no planejamento, sem surpresa de última hora." |
| E | "Me passa o que você tem agora — pode ser uma planta preliminar, foto do espaço ou medidas aproximadas. Já consigo te dar uma referência." |

### O6 — "Nunca ouvi falar da {{EMPRESA}}."

| Etapa | Script |
|---|---|
| V | "Faz todo sentido, [NOME]. Você está colocando um equipamento de longa duração em um imóvel importante." |
| I | "O que te daria mais segurança para conhecer a {{EMPRESA}} melhor? Visita técnica, projetos anteriores, conversar com clientes?" |
| R | "{{ARGUMENTO_AUTORIDADE_LOCAL}}" / "Posso te colocar em contato com um cliente nosso que passou por um projeto parecido com o seu." |
| E | "Qual dessas opções te deixaria mais confortável: ver os casos pelo WhatsApp agora ou agendar uma visita técnica sem compromisso?" |

### O7 — "Não quero fechar agora."

| Etapa | Script |
|---|---|
| V | "Sem problema, [NOME]. Não quero que você feche antes de estar seguro." |
| I | "Tem algo na proposta que não te convenceu — produto, prazo, preço ou empresa?" |
| R | Escute. Se não revelar: "O que faria você se sentir pronto para avançar?" |
| E | "Vou registrar aqui e entro em contato em [DATA]. Se antes disso surgir qualquer dúvida, pode me chamar. Posso contar com isso?" |

### O8 — "Qual é o prazo de entrega?"

| Etapa | Script |
|---|---|
| V | "Boa pergunta, [nome]. É super importante para o planejamento da obra." |
| I | "Qual é a data que você precisa ter o equipamento instalado? Assim te digo com precisão se é viável." |
| R | "O prazo médio após aprovação do pedido é: {{PRAZO_EQUIPAMENTOS}}. Isso já inclui fabricação, frete e instalação." [Se prazo atender] → "Posso garantir essa data se confirmarmos o pedido até [DATA LIMITE]." |
| E | "Posso te enviar a proposta já com a data de instalação prevista para você avaliar?" |

### O9 — "Vou esperar a obra terminar para instalar."

| Etapa | Script |
|---|---|
| V | "Entendo, [NOME]. Muitos dos nossos clientes chegam a essa conclusão." |
| I | "Essa decisão é por orçamento disponível agora, pelo planejamento da obra ou tem outro motivo?" |
| R | "Instalar o equipamento durante a obra custa em média 30% a 50% menos do que após a obra pronta. Após a obra, a instalação exige quebra de parede, adaptação de laje e reforma posterior. {{ARGUMENTO_RETROFIT}}" |
| E | "Quer que eu te envie uma estimativa comparativa? Instalação em obra vs. instalação pós-obra para o seu projeto?" |

### Mapa rápido — Objeção declarada vs. real

| O lead diz... | O que pode ser na verdade... | Pergunta de diagnóstico |
|---|---|---|
| "Está caro" | Não viu valor / comparando / sem verba / precisa justificar | "Em relação a quê você está comparando?" |
| "Vou pensar" | Dúvida não verbalizada / quer comparar concorrentes | "O que você ainda precisa resolver antes de decidir?" |
| "Recebi mais barato" | Não entendeu o que está incluso / quer desconto | "O que estava incluso no outro orçamento?" |
| "Preciso de aprovação" | Não é o decisor / quer mais tempo | "O que a diretoria vai querer saber antes de aprovar?" |
| "Projeto não definido" | Sem verba / fase de pesquisa / prazo longo | "Em que fase está o projeto? Tem alguma data de referência?" |
| "Não conheço a empresa" | Falta de confiança / risco percebido alto | "O que te daria mais segurança para conhecer a gente melhor?" |
| "Não quero fechar agora" | Objeção anterior não resolvida / pressão percebida | "Tem algo na proposta que não te convenceu?" |
| "Vou esperar a obra" | Não sabe o custo do retrofit / fluxo de caixa | "Essa decisão é por orçamento agora ou por planejamento de obra?" |

---

# Gatilhos de Avanço — {{CRM}}

O lead só muda de etapa quando o critério abaixo for cumprido.

| De → Para | Critério de avanço |
|---|---|
| Novo Lead → Atendimento SDR | Lead respondeu o BOT com informação mínima sobre a necessidade |
| Atendimento SDR → Aguardando Dados | SDR entra em contato e coleta dados técnicos do projeto |
| Aguardando Dados → Fazer/enviar orçamento | Dados coletados e orçamento em montagem |
| Fazer/enviar orçamento → Orçamento Enviado | Orçamento enviado e follow-up iniciado |
| Orçamento Enviado → Venda Ganha | Lead fecha o pedido |

**Campos obrigatórios no {{CRM}}:** Origem do lead | Tipo de Equipamento | Vendedor responsável

---

# Regras de Ouro do Time Comercial

1. Responda em até 5 minutos durante o horário comercial.
2. Toda informação vai para o {{CRM}} — se não está registrado, não existe.
3. Nunca envie proposta sem conversa prévia.
4. Qualifique antes de gastar tempo.
5. Follow-up é responsabilidade do vendedor, não do lead.
6. Não dê desconto sem contrapartida.
7. Registre o motivo de toda perda — é o dado mais valioso para melhorar o processo.
8. Mantenha o {{CRM}} sempre atualizado.
9. Utilize o calendário de tarefas do {{CRM}} para organizar o time por vendedor.
10. Peça indicação após cada venda concluída — a melhor hora é quando o cliente está animado.

---

> *"O objetivo não é vender um equipamento. É transformar uma operação reativa em uma máquina previsível de vendas."* — DVE Assessoria

---

## Variáveis deste template

| Variável | Descrição | Exemplo (Primmus) |
|---|---|---|
| `{{EMPRESA}}` | Nome da empresa | Primmus Elevadores |
| `{{PRODUTOS}}` | Linha de produtos | Plataformas de Acessibilidade & Elevadores Hidráulicos |
| `{{PRODUTO_SINGULAR}}` | Nome do produto no singular | um elevador |
| `{{MES_ANO}}` | Mês e ano de elaboração | Abril de 2026 |
| `{{TICKET_MEDIO}}` | Ticket médio | R$ 50.000 |
| `{{TICKET_MIN}}` | Ticket mínimo | R$ 25.000 |
| `{{TICKET_MAX}}` | Ticket máximo | R$ 100.000 |
| `{{TICKET_MIN_DESCONTO}}` | Valor abaixo do qual é desqualificado | R$ 20.000 |
| `{{MARGEM}}` | Margem bruta | ~20% |
| `{{CAC_ALVO}}` | CAC alvo por venda | R$ 2.000 |
| `{{CONVERSAO_ATUAL}}` | Taxa de conversão atual | ~15% |
| `{{META_MENSAL}}` | Meta de vendas por mês | 20+ |
| `{{REGIAO_PRINCIPAL}}` | Cidade/região principal | Curitiba |
| `{{PERCENTUAL_REGIAO_PRINCIPAL}}` | % das vendas na região principal | 85 |
| `{{REGIAO_SECUNDARIA}}` | Região secundária | Santa Catarina |
| `{{MARCA_EQUIPAMENTO}}` | Marca dos equipamentos | Daiken |
| `{{CRM}}` | CRM utilizado | Kommo |
| `{{TABELA_SEGMENTOS_ICP}}` | Tabela de segmentos (linhas markdown) | Construtoras / Indústrias / Escolas / Residencial alto padrão |
| `{{OPCOES_EQUIPAMENTO}}` | Opções de equipamento para o BOT | Elevador / Plataforma Hidráulica |
| `{{TABELA_DADOS_TECNICOS}}` | Tabela de dados técnicos para orçamento | (ver seção Primmus) |
| `{{LISTA_DIFERENCIAIS}}` | Lista de diferenciais competitivos | Representante Daiken / Ciclo completo / Conformidade ABNT |
| `{{PRAZO_EQUIPAMENTOS}}` | Prazo médio de entrega e instalação | X semanas para plataformas / Y semanas para elevadores |
| `{{MESES_MANUTENCAO_GRATIS}}` | Meses de manutenção grátis (negociação) | 6 |
| `{{ARGUMENTO_AUTORIDADE_LOCAL}}` | Argumento de autoridade e casos locais | (inserir referências reais da empresa) |
| `{{ARGUMENTO_RETROFIT}}` | Argumento custo retrofit pós-obra | (inserir dado técnico real) |
| `{{MSG_ANCORA_RESIDENCIAL}}` | Mensagem âncora para leads residenciais | (inserir texto da empresa) |
| `{{MSG_ANCORA_COMERCIAL}}` | Mensagem âncora para leads comerciais | (inserir texto da empresa) |
| `{{MSG_ANCORA_INDUSTRIAL}}` | Mensagem âncora para leads industriais | (inserir texto da empresa) |
| `{{MSG_ANCORA_MODERNIZACAO}}` | Mensagem âncora para modernização | (inserir texto da empresa) |
| `{{MSG_FU2_BOT}}` | Mensagem de autoridade no FU2 do BOT | (inserir texto da empresa) |
| `{{MSG_FU3_BOT}}` | Mensagem de prova social no FU3 do BOT | (inserir link/vídeo real) |
| `{{MSG_NUTRICAO_1}}` | Mensagem de nutrição mês 1 (ativação) | (inserir texto) |
| `{{MSG_NUTRICAO_2}}` | Mensagem de nutrição mês 2 (autoridade) | (inserir texto + link) |
| `{{MSG_NUTRICAO_3}}` | Mensagem de nutrição mês 3 (prova social) | (inserir texto + link) |
