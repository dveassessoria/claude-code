# TEMPLATE — Playbook de Vendas: Manutenção

> Use este arquivo como base para gerar o playbook de um novo cliente que vende manutenção preventiva/corretiva.
> Substitua todas as variáveis `{{VARIAVEL}}` pelos dados reais do onboarding.
> Variáveis disponíveis no final deste arquivo.

---

# Introdução

**{{EMPRESA}}**

{{SERVICOS_MANUTENCAO}}

---

**PLAYBOOK DE VENDAS**

*Processos Comerciais • Qualificação • Roteiros • Objeções • CRM*

---

Elaborado por DVE Assessoria — {{MES_ANO}}

*Documento confidencial — uso exclusivo do time comercial {{EMPRESA}}*

---

**Como usar este Playbook?**

O playbook é o guia prático do time comercial da **{{EMPRESA}}**. Ele padroniza cada etapa do atendimento, da prospecção ao fechamento do contrato, e serve de base para a configuração do {{CRM}}.

Leia uma vez do início ao fim. Depois, use como consulta rápida durante os atendimentos.

| O que você vai encontrar | Números de referência |
|---|---|
| 1. Perfil do cliente ideal (ICP) | Ticket médio mensal: {{TICKET_MEDIO_MENSAL}} |
| 2. Funil de vendas e etapas no {{CRM}} | Faixa: {{TICKET_MIN_MENSAL}} a {{TICKET_MAX_MENSAL}} / mês |
| 3. Qualificação LS-NBT | Contrato mínimo: {{PRAZO_MINIMO_CONTRATO}} |
| 4. Roteiros de abordagem (WhatsApp) | CAC alvo: {{CAC_ALVO}} / contrato |
| 5. Diagnóstico de necessidades | Conversão atual: {{CONVERSAO_ATUAL}} |
| 6. Condução da proposta e negociação | Meta: {{META_CONTRATOS}} novos contratos / mês |
| 7. Follow-up estruturado | Região: {{REGIAO_PRINCIPAL}} + {{REGIAO_SECUNDARIA}} |
| 8. Mapeamento de objeções | |
| 9. Gatilhos de avanço no CRM | |

---

# ICP — Perfil do Cliente Ideal

Na manutenção, o decisor não é quem comprou o elevador — é quem paga a conta de manter o prédio funcionando. Antes de qualificar, o vendedor precisa saber exatamente quem é esse decisor e em que contexto ele aparece.

## Segmentos prioritários

| Segmento | Decisor típico | Dor principal |
|---|---|---|
| **Condomínios residenciais** | Síndico profissional ou morador eleito | Elevador parado gera reclamação dos moradores e risco de autuação |
| **Condomínios comerciais** | Síndico / administradora | Elevador parado paralisa o prédio e gera responsabilidade legal |
| **Prédios corporativos** | Gestor de facilities / proprietário | SLA de disponibilidade e risco de multa contratual com inquilinos |
| **Hospitais e clínicas** | Gerente de facilities / diretor administrativo | Elevador parado é risco operacional crítico |
| **Shoppings e centros comerciais** | Gerente de operações | Acessibilidade é obrigação legal e impacta experiência do cliente |
| **Escolas e igrejas** | Diretor / pastor administrativo | Adequação às normas de acessibilidade ABNT |
{{SEGMENTOS_ADICIONAIS_ICP}}

## Sinais de lead qualificado vs. desqualificado

| Qualificado | Desqualificado |
|---|---|
| 2+ elevadores no local | 1 elevador residencial unifamiliar |
| Equipamento com 3+ anos sem contrato estruturado | Contrato novo assinado há menos de 6 meses |
| Contrato atual vencendo nos próximos 90 dias | Vínculo exclusivo com o fabricante (difícil de romper) |
| Insatisfação com o prestador atual | Fora da área de atendimento |
| Localização: {{REGIAO_PRINCIPAL}} ou {{REGIAO_SECUNDARIA}} | Sem poder de decisão sobre o contrato |
| Decisor presente ou acessível | Orçamento incompatível com {{TICKET_MIN_MENSAL}}/mês |

---

# Processo Comercial — Funil de Vendas

A venda de manutenção tem uma etapa extra que a de equipamentos não tem: a **vistoria técnica gratuita**. Ela é a chave do processo — o técnico vê o estado real do equipamento e o vendedor tem argumentos concretos para a proposta.

| ETAPAS SDR — PRÉ-VENDAS | | |
|---|---|---|
| **Etapa** | **O que acontece** | **Ação do SDR** |
| 1. Novo Lead | Lead chegou (WhatsApp, indicação, prospecção ativa, Google) | — |
| 2. BOT | Perguntas automáticas de qualificação | — |
| 3. Follow Up 1/2/3 | Lead não respondeu o BOT | Aguardar follow-up automático |
| 4. Atendimento SDR | Lead qualificado — aguardando contato humano | Ligar em até 5 minutos. Objetivo: agendar vistoria técnica gratuita |
| 5. Vistoria Agendada | Vistoria confirmada com data e horário | Confirmar vistoria no dia anterior e no dia |
| 6. Follow Up 1/2/3 | Lead não confirmou a vistoria | Follow-up para reagendar |

| ETAPAS VENDEDOR — VENDAS | | |
|---|---|---|
| **Etapa** | **O que acontece** | **Ação do Vendedor** |
| 7. Vistoria Realizada | Técnico foi ao local e gerou laudo | Vendedor usa o laudo para montar a proposta |
| 8. Proposta em Elaboração | Proposta sendo montada com base no laudo | Elaborar em até {{PRAZO_ELABORACAO_PROPOSTA}} após a vistoria |
| 9. Proposta Enviada | Proposta enviada — lead ainda não assinou | Follow-up por ligação e WhatsApp |
| 10. Follow Up 1/2/3 | Lead não assinou | Follow-up escalonado |
| 11. Contrato Ganho | Contrato assinado | Passar para onboarding técnico e CS |
| 12. Contrato Perdido | Negociação encerrada sem fechamento | Registrar motivo da perda |
| 13. Nutrição | Lead sem resposta há mais de 14 dias | Contato mensal de reengajamento |

> **Importante:** a vistoria técnica gratuita é o diferencial que transforma uma proposta genérica em uma proposta personalizada e difícil de comparar com concorrentes.

---

# Qualificação de Leads — LS-NBT

Aplique assim que o lead entrar em contato. Objetivo: confirmar que vale a pena fazer a vistoria gratuita.

**Fluxo:** L (Localização) → S (Situação) → N (Necessidade) → B (Budget) → T (Timeline)

## L — Localização

> Filtro geográfico. Leads fora de {{REGIAO_PRINCIPAL}} e {{REGIAO_SECUNDARIA}} são desqualificados.

**Pergunta do BOT:** "Antes de iniciar seu atendimento, me confirma: qual a cidade e o estado onde os elevadores estão instalados?"

## S — Situação: Qual é o contexto atual?

**Pergunta do BOT:** "Quantos elevadores você possui no local?"

**Pergunta do BOT:** "Qual a marca/fabricante dos seus elevadores? (Se souber)"

**Pergunta do BOT:** "Você já possui contrato de manutenção ativo hoje?
- Sim, tenho contrato
- Não tenho contrato
- Tenho, mas estou insatisfeito"

## N — Necessidade: Qual é a dor?

**Pergunta do BOT:** "O que te motivou a buscar uma nova empresa de manutenção agora?"

> O vendedor usa essa resposta para personalizar a abordagem — lead sem contrato tem dor diferente de lead insatisfeito com o prestador atual.

## B — Budget

**Pergunta do BOT:** "Hoje você investe em manutenção de elevadores?
- Sim, pago [X] por mês
- Sim, mas não sei o valor exato
- Não invisto em manutenção regular"

> Se o lead pagar abaixo de {{TICKET_MIN_MENSAL}}/mês, não desqualificar ainda — pode estar subestimando o serviço ou o contrato atual ser deficiente.

## T — Timeline

**Pergunta do BOT:** "Quando você gostaria de iniciar o novo contrato de manutenção?
- O mais rápido possível
- Quando o contrato atual vencer (quando vence?)
- Ainda estou pesquisando"

---

# Atendimento Inicial — WhatsApp e Ligação

> **Regra de ouro:** entrar em contato com o lead em no máximo 5 minutos. O objetivo desta ligação não é fechar — é **agendar a vistoria técnica gratuita**.

## Dados necessários antes da vistoria

| # | Dado | Como perguntar |
|---|---|---|
| 1 | Endereço completo | "Qual o endereço completo do local para agendarmos a vistoria?" |
| 2 | Número de elevadores | "Quantos elevadores existem no local?" |
| 3 | Marca e modelo (se souber) | "Você sabe a marca dos elevadores? Ou tem alguma plaquinha de identificação no equipamento?" |
| 4 | Número de paradas | "Quantos andares o elevador atende?" |
| 5 | Contato no local | "Tem um zelador, porteiro ou responsável que pode receber o nosso técnico?" |
| 6 | Horário de acesso | "Qual o horário de funcionamento do prédio para a visita técnica?" |
| 7 | Contrato atual | "Vocês têm contrato de manutenção ativo hoje? Com quem?" |
| 8 | Vencimento do contrato | "Quando vence o contrato atual?" |

> Orçamento sem vistoria é estimativa — e estimativa gera proposta sem credibilidade técnica.

## Script WhatsApp — SDR (até 5 min após BOT)

Leia TODAS as respostas do BOT antes de escrever a mensagem.

**Mensagem base:**

> Olá, [NOME DO LEAD]! Tudo bem?
>
> Sou o [NOME DO SDR], da equipe {{EMPRESA}}. Tentei te ligar agora porém não obtive retorno.
>
> Recebi suas informações aqui e vi que você está buscando manutenção para [N] elevadores em [CIDADE].
>
> Aqui na {{EMPRESA}} oferecemos {{SERVICO_PRINCIPAL}} com [diferencial chave].
>
> Para montar uma proposta real para o seu caso, nosso técnico faz uma **vistoria gratuita** nos seus equipamentos — sem compromisso. Você tem disponibilidade para receber o nosso técnico agora ou prefere [SUGESTÃO DE HORÁRIO]?

## Variações por perfil de lead

| Situação (BOT) | Mensagem âncora |
|---|---|
| Sem contrato atual | "{{MSG_ANCORA_SEM_CONTRATO}}" |
| Insatisfeito com prestador | "{{MSG_ANCORA_INSATISFEITO}}" |
| Contrato vencendo | "{{MSG_ANCORA_VENCENDO}}" |
| Pesquisando / sem urgência | "{{MSG_ANCORA_PESQUISANDO}}" |

## Script de Ligação — SDR / Vendedor

**Estrutura:**
1. Abertura — apresentação + confirmar disponibilidade
2. Confirmação das respostas do BOT
3. Coleta de dados adicionais
4. Agendamento da vistoria técnica gratuita

**Abertura:**
> "Olá, [NOME]! Aqui é o [NOME DO SDR] da {{EMPRESA}}. Recebi seus dados e vi que você tem [N] elevadores em [CIDADE] e está buscando manutenção. Você tem 5 minutinhos para a gente conversar?"

**Confirmação:**
> "Antes de tudo, quero confirmar o que você nos informou. Você tem [N] elevadores, [com/sem] contrato de manutenção ativo. Isso está correto? Tem alguma informação que queira complementar?"

**Proposta da vistoria:**
> "[NOME], para montar uma proposta que realmente faz sentido para o seu caso, nosso técnico vai até o local para ver os equipamentos gratuitamente. Essa vistoria é sem compromisso — você recebe um laudo técnico detalhado do estado dos seus elevadores independentemente de fechar conosco. Qual o melhor dia e horário para a gente enviar o técnico?"

**Se o lead hesitar na vistoria:**
> "Entendo, [NOME]. Quer que eu te explique o que acontece na vistoria para você decidir? São 30 minutos, o técnico vai, olha os equipamentos, anota o que precisa e você já sai sabendo o estado real dos seus elevadores — mesmo que não feche com a gente. Não tem custo nenhum."

---

# Negociação — Condução do Contrato

## Apresentação da proposta

> [Vendedor — WhatsApp]
> "Oi, [Nome]! Tudo bem? Aqui é o [Nome Vendedor] da {{EMPRESA}}. Nosso técnico já realizou a vistoria nos seus equipamentos e preparei a proposta com base no laudo. Posso te ligar agora para apresentar?"

**Como apresentar o investimento:**
> "Com base na vistoria dos [N] elevadores em [endereço], o investimento para o contrato de manutenção preventiva é de {{TICKET_MEDIO_MENSAL}}/mês. Isso inclui [{{ITENS_CONTRATO}}]. Além da manutenção preventiva mensal, qualquer chamado corretivo tem prioridade de atendimento em até {{SLA_ATENDIMENTO}} horas. Fechando hoje, já consigo incluir [{{BONUS_FECHAMENTO}}]. Qual o melhor e-mail para encaminhar o contrato?"

## Diferenciais para fechamento

{{LISTA_DIFERENCIAIS_MANUTENCAO}}

## Quando o lead pede desconto

| Estratégia | Como usar |
|---|---|
| Âncora de valor | "Esse valor já contempla [X visitas preventivas/mês], [peças de desgaste], [chamados corretivos com SLA de X horas] e laudo mensal. Separado, isso custaria facilmente [valor]." |
| Contrapartida | "Consigo reduzir para [valor] se você fechar por [12 ou 24 meses]. Contratos mais longos permitem que eu reduza a margem." |
| Comparação com o custo do problema | "Uma parada de emergência com técnico fora do contrato custa em média [valor] só a mão de obra, sem contar as peças. O contrato preventivo evita exatamente isso." |
| Contrato por fases | Para múltiplos elevadores: "Podemos iniciar com [N] elevadores agora e incluir os outros na renovação em [X meses]." |

---

# Follow-Up Estruturado

Mensagens organizadas em 4 blocos:
1. Follow-up do BOT
2. Follow-up de Agendamento de Vistoria
3. Follow-up Pós Proposta
4. Nutrição

## Follow-Up BOT — Lead não respondeu o atendimento automático

| FU | Quando dispara | Mensagem automática |
|---|---|---|
| FU 1 | 10 min sem resposta | "Oi, [Nome]! Vi que você entrou em contato com a {{EMPRESA}}. Consigo te ligar agora para dar sequência no seu atendimento?" |
| FU 2 | 3h sem resposta | "[Nome]! Para te ajudar com a manutenção dos seus elevadores, preciso de alguns dados. {{MSG_FU2_BOT_MANUTENCAO}}" |
| FU 3 | 24h sem resposta | "Olá, aqui é [vendedor] da {{EMPRESA}}. {{MSG_FU3_BOT_MANUTENCAO}} Quando consigo te ligar?" |

## Follow-Up Vistoria — Lead não confirmou o agendamento

| FU | Quando dispara | Mensagem SDR |
|---|---|---|
| FU 1 | 4h após proposta de vistoria | "Oi, [Nome]! Só confirmando a disponibilidade do nosso técnico para ir até [endereço]. Qual o melhor horário?" |
| FU 2 | Dia seguinte | "[Nome], quero garantir que você tenha o laudo técnico gratuito dos seus equipamentos antes de qualquer decisão. Quando o técnico pode ir?" |
| FU 3 | 3 dias após proposta | **SDR ligar:** "Oi, [Nome]! Nosso técnico tem disponibilidade [dia e horário]. A vistoria é gratuita e leva 30 minutos — você recebe o laudo dos seus elevadores independentemente de fechar conosco. Consegue receber?" |

## Follow-Up Pós Proposta — Lead recebeu e parou de responder

| FU | Quando dispara | Ação |
|---|---|---|
| FU 1 | 24h após envio | **Ligar:** "[Nome], bom demais? Aqui é o [Vendedor] da {{EMPRESA}}. Você teve a chance de analisar a proposta com [síndico/diretoria]?" |
| FU 2 | 3 dias após envio | **Ligar:** "Abrindo o jogo, as condições que coloquei na proposta são válidas até [data]. Depois disso preciso rever pelo volume de demanda que estamos tendo. Sendo direto: o que está impedindo de fecharmos?" |
| FU 3 | 7 dias após envio | **WhatsApp:** "[Nome]! Um dos nossos clientes em [cidade] tinha uma situação parecida com a sua — [breve case]. Hoje o contrato já completou [X meses] e [resultado]. [Enviar foto/depoimento se disponível] Quer que eu te conte como foi?" |

## Nutrição — Lead sem resposta há mais de 14 dias

Frequência: 1 mensagem por mês.

| Mês / Tema | Mensagem |
|---|---|
| Mês 1 — Ativação | "{{MSG_NUTRICAO_MANUTENCAO_1}}" |
| Mês 2 — Autoridade | "{{MSG_NUTRICAO_MANUTENCAO_2}}" |
| Mês 3 — Urgência normativa | "{{MSG_NUTRICAO_MANUTENCAO_3}}" |

---

# Objeções

## A lógica antes dos scripts

Na manutenção, as objeções têm uma particularidade: quase sempre existe um fornecedor atual. O lead não está comprando de zero — está trocando alguém. O trabalho do vendedor é entender por que ele está avaliando mudança e usar isso a seu favor.

## Framework VIRE

| Etapa | Nome | O que fazer |
|---|---|---|
| V | Validar | Acolher sem resistência |
| I | Isolar | Confirmar se é a única barreira |
| R | Resolver | Resposta certa para o problema certo |
| E | Encaminhar | Conduzir para o fechamento com CTA |

## Objeções mapeadas

### O1 — "Já tenho contrato com o fabricante."

Objeção mais comum. O lead acredita que o fabricante é a melhor opção — geralmente por falta de comparação ou por inércia.

| Etapa | Script |
|---|---|
| V | "Faz sentido, [NOME]. Muitos dos nossos clientes também vieram do contrato com o fabricante." |
| I | "Posso te fazer uma pergunta? O que te fez estar avaliando alternativas agora? Alguma insatisfação específica ou você está comparando preços?" |
| R | "Entendo. O que costuma acontecer com contratos de fabricante é que o preço sobe a cada renovação e o tempo de resposta em chamados de emergência tende a ser mais lento — eles atendem toda a base, não só a sua região. [Inserir diferencial específico da {{EMPRESA}}] Nossa proposta inclui [SLA de X horas], [técnico dedicado à região], [transparência no laudo mensal]. Posso te mostrar isso na prática com uma vistoria gratuita?" |
| E | "Que tal a gente fazer a vistoria gratuita primeiro? Você recebe o laudo, compara com o que tem hoje e decide com informação real na mão." |

### O2 — "Está funcionando bem, não preciso de manutenção."

Objeção de necessidade — o lead não percebe o risco de não ter manutenção estruturada.

| Etapa | Script |
|---|---|
| V | "Ótimo, [NOME]. Equipamento funcionando bem é exatamente o resultado que a manutenção preventiva garante." |
| I | "Posso te perguntar: quando foi a última vez que um técnico fez uma inspeção completa nos equipamentos?" |
| R | "Equipamento 'funcionando bem' sem manutenção preventiva é um risco silencioso. Os componentes de desgaste — correntes, guias, sistema hidráulico — se degradam antes de apresentar falha visível. Quando param, a parada é abrupta e o custo de manutenção corretiva costuma ser 3x a 5x maior que o preventivo. Além disso, a Norma {{NORMA_MANUTENCAO}} exige manutenção periódica — sem isso, o condomínio/empresa fica exposto a autuação e responsabilidade civil em caso de acidente." |
| E | "Quer que o nosso técnico faça uma vistoria diagnóstica gratuita? Você fica sabendo o estado real dos seus equipamentos sem compromisso." |

### O3 — "Está caro."

| Etapa | Script |
|---|---|
| V | "Entendo, [NOME]. Custo é sempre um ponto importante em uma decisão de contrato." |
| I | "Você está comparando com o que paga hoje ou com algum outro orçamento que recebeu?" |
| R | [Se comparando com o atual] "O que está incluso no contrato atual pelo mesmo valor? Às vezes a diferença de preço reflete diferença de escopo — SLA de atendimento, cobertura de peças, número de visitas preventivas. Posso te mostrar item por item o que a nossa proposta inclui." [Se outro orçamento] "Me conta o que o outro orçamento previa — assim consigo comparar com precisão." [Se percepção de valor] "Uma parada de emergência não planejada custa em média {{CUSTO_EMERGENCIA_ESTIMADO}} só de chamado técnico urgente, sem contar as peças. O contrato preventivo elimina praticamente esse risco. Se dividirmos esse custo pelos meses, o preventivo é significativamente mais barato." |
| E | "Quer que eu detalhe item por item o que está na nossa proposta? Assim você consegue comparar tecnicamente com o que tem hoje." |

### O4 — "Preciso de aprovação do síndico / diretoria / administradora."

| Etapa | Script |
|---|---|
| V | "Totalmente compreensível, [NOME]. Decisão de contrato com terceiros normalmente passa por aprovação." |
| I | "Fora a aprovação, tem mais alguma coisa em aberto?" |
| R | "Posso preparar um material executivo com tudo que a administradora / síndico precisa saber para aprovar: laudo da vistoria, escopo do contrato, SLA, referências de outros condomínios que atendemos na região. Isso facilita muito a aprovação interna." |
| E | "Quando é a reunião de aprovação? Quero garantir que você tenha o material completo antes. Se for até [DATA], consigo enviar ainda hoje." |

### O5 — "Vou renovar com quem tenho."

Objeção de inércia — o lead não quer o atrito de mudar de fornecedor.

| Etapa | Script |
|---|---|
| V | "Faz sentido, [NOME]. Mudar de prestador tem um custo de tempo e adaptação." |
| I | "Posso te perguntar com sinceridade: você está renovando por satisfação com o serviço atual ou por conveniência mesmo?" |
| R | [Se satisfação genuína] "Entendo perfeitamente. O que te levou a pesquisar então? Às vezes existe uma dúvida pequena que vale a pena explorar antes de renovar." [Se inércia] "Entendo. Só para registrar: o que seria necessário para você considerar mudar? Preço menor? Tempo de resposta mais rápido? Transparência no serviço? Pergunto porque posso verificar se conseguimos atender exatamente esse ponto antes da renovação." |
| E | "Que tal a gente fazer a vistoria antes da renovação? Você vai ter um laudo independente dos seus equipamentos para embasar qualquer decisão — seja renovar com quem tem ou migrar para a gente." |

### O6 — "Nunca ouvi falar da {{EMPRESA}}."

| Etapa | Script |
|---|---|
| V | "Faz todo sentido, [NOME]. Para um contrato de longo prazo, confiar em quem vai cuidar dos seus equipamentos é o mínimo." |
| I | "O que te daria mais segurança para conhecer a {{EMPRESA}} melhor?" |
| R | "Atendemos [X] condomínios / prédios em {{REGIAO_PRINCIPAL}}. Posso te passar o contato de [referência local] que passa a experiência de quem já usa o nosso serviço. {{ARGUMENTO_AUTORIDADE_MANUTENCAO}}" |
| E | "Qual dessas opções te deixaria mais confortável: ver os clientes que atendemos na sua região ou agendar a vistoria gratuita para você nos conhecer pelo nosso trabalho técnico?" |

### O7 — "Vou esperar o contrato atual vencer."

| Etapa | Script |
|---|---|
| V | "Faz sentido, [NOME]. Quebrar um contrato antes do vencimento tem custo e burocracia." |
| I | "Quando vence o contrato atual?" |
| R | "Entendido. O que posso fazer agora é [duas opções]: 1) Deixar tudo preparado para que assim que vencer, a migração seja imediata sem nenhum período sem cobertura. 2) Analisar se existe alguma cláusula de saída antecipada no seu contrato — às vezes é mais simples do que parece." [Se prazo for curto — menos de 90 dias] "Considerando que vence em [data], vale a pena iniciar o processo agora. A vistoria leva [X dias], a proposta mais [X dias] e a aprovação interna mais [X]. Se esperarmos, pode ficar sem cobertura por alguns dias na transição." |
| E | "Posso reservar o slot da vistoria para a semana que antecede o vencimento? Assim você chega na renovação com a proposta pronta e uma decisão informada." |

### O8 — "O fabricante faz a manutenção — eles conhecem melhor o equipamento."

| Etapa | Script |
|---|---|
| V | "É um argumento que faz sentido à primeira vista, [NOME]." |
| I | "Você já teve alguma experiência negativa com a manutenção do fabricante ou está só pesquisando alternativas?" |
| R | "Sim, o fabricante conhece bem o equipamento de saída. Mas no dia a dia, o que importa é o tempo de resposta a chamados de emergência, o custo das peças e a transparência nos laudos. Fabricantes têm carteira nacional e o técnico que atende você hoje pode não ser o mesmo amanhã. [{{EMPRESA}}] tem [X] técnicos dedicados à região {{REGIAO_PRINCIPAL}}, com SLA de {{SLA_ATENDIMENTO}} horas e laudo técnico após cada visita." |
| E | "Que tal você comparar lado a lado? Nossa vistoria gratuita gera um laudo que você pode comparar com o relatório do fabricante. Aí decide com informação técnica real." |

### Mapa rápido — Objeção declarada vs. real

| O lead diz... | O que pode ser na verdade... | Pergunta de diagnóstico |
|---|---|---|
| "Já tenho contrato com o fabricante" | Inércia / nunca comparou / medo do atrito | "O que te fez avaliar alternativas agora?" |
| "Está funcionando bem" | Não percebe o risco / não sabe o que é manutenção preventiva | "Quando foi a última inspeção completa?" |
| "Está caro" | Comparando errado / não viu o custo do problema | "Você está comparando com o que paga hoje ou com outro orçamento?" |
| "Preciso de aprovação" | Não tem poder de decisão / quer material para justificar | "O que a diretoria vai precisar saber para aprovar?" |
| "Vou renovar com quem tenho" | Inércia / satisfação genuína / medo de mudança | "Você está renovando por satisfação ou por conveniência?" |
| "Nunca ouvi falar" | Falta de confiança / risco percebido alto | "O que te daria mais segurança para nos conhecer melhor?" |
| "Vou esperar vencer" | Custo de quebra de contrato / inércia | "Quando vence o contrato atual?" |
| "Fabricante conhece melhor" | Crença de que especialização = qualidade | "Você já teve alguma experiência negativa com eles?" |

---

# Gatilhos de Avanço — {{CRM}}

O lead só muda de etapa quando o critério abaixo for cumprido.

| De → Para | Critério de avanço |
|---|---|
| Novo Lead → Atendimento SDR | Lead respondeu o BOT com informação mínima |
| Atendimento SDR → Vistoria Agendada | Data e horário da vistoria confirmados com o responsável local |
| Vistoria Agendada → Vistoria Realizada | Técnico foi ao local e gerou laudo |
| Vistoria Realizada → Proposta Enviada | Proposta enviada por e-mail e WhatsApp |
| Proposta Enviada → Contrato Ganho | Contrato assinado |

**Campos obrigatórios no {{CRM}}:** Origem do lead | Nº de elevadores | Marca dos equipamentos | Vencimento do contrato atual | Vendedor responsável

---

# Regras de Ouro do Time Comercial

1. Responda em até 5 minutos durante o horário comercial.
2. A vistoria gratuita é o principal argumento de diferenciação — nunca a abandone como CTA.
3. Toda informação vai para o {{CRM}} — se não está registrado, não existe.
4. Nunca envie proposta sem vistoria prévia — proposta sem laudo não tem credibilidade técnica.
5. Follow-up é responsabilidade do vendedor, não do lead.
6. Não dê desconto sem contrapartida — sempre peça prazo maior de contrato em troca.
7. Registre o motivo de toda perda — é o dado mais valioso.
8. Cada síndico satisfeito é uma fonte de indicação para outros prédios da administradora.
9. Monitore os vencimentos da carteira de clientes ativos — renovação antecipada com benefício é mais fácil que renovação em cima da hora.
10. Peça indicação após cada contrato assinado — a melhor hora é quando o síndico está animado com o laudo da vistoria.

---

> *"Manutenção preventiva não é custo — é o seguro que evita o custo real: a parada de emergência e a responsabilidade legal."* — DVE Assessoria

---

## Variáveis deste template

| Variável | Descrição | Exemplo |
|---|---|---|
| `{{EMPRESA}}` | Nome da empresa | Primmus Elevadores |
| `{{SERVICOS_MANUTENCAO}}` | Serviços (subtítulo) | Manutenção Preventiva & Corretiva de Elevadores |
| `{{SERVICO_PRINCIPAL}}` | Serviço principal (texto corrido) | manutenção preventiva e corretiva |
| `{{MES_ANO}}` | Mês e ano | Junho de 2026 |
| `{{TICKET_MEDIO_MENSAL}}` | Mensalidade média do contrato | R$ 800/mês por elevador |
| `{{TICKET_MIN_MENSAL}}` | Mensalidade mínima | R$ 500/mês |
| `{{TICKET_MAX_MENSAL}}` | Mensalidade máxima | R$ 2.000/mês |
| `{{PRAZO_MINIMO_CONTRATO}}` | Prazo mínimo do contrato | 12 meses |
| `{{CAC_ALVO}}` | CAC alvo por contrato novo | R$ 500 |
| `{{CONVERSAO_ATUAL}}` | Taxa de conversão atual | A definir |
| `{{META_CONTRATOS}}` | Meta de novos contratos/mês | 5 |
| `{{REGIAO_PRINCIPAL}}` | Cidade/região principal | Curitiba |
| `{{REGIAO_SECUNDARIA}}` | Região secundária | Santa Catarina |
| `{{CRM}}` | CRM utilizado | Kommo |
| `{{PRAZO_ELABORACAO_PROPOSTA}}` | Prazo para elaborar proposta após vistoria | 48 horas |
| `{{SLA_ATENDIMENTO}}` | SLA de atendimento a chamados | 4 horas |
| `{{ITENS_CONTRATO}}` | O que está incluído no contrato | X visitas preventivas/mês, peças de desgaste, laudos |
| `{{BONUS_FECHAMENTO}}` | Bônus de fechamento | 1 mês grátis / vistoria adicional |
| `{{NORMA_MANUTENCAO}}` | Norma técnica aplicável | ABNT NBR 16858 ou NR-12 |
| `{{CUSTO_EMERGENCIA_ESTIMADO}}` | Custo estimado de uma parada emergencial | R$ 1.500 a R$ 3.000 |
| `{{LISTA_DIFERENCIAIS_MANUTENCAO}}` | Lista de diferenciais da empresa | (inserir após onboarding) |
| `{{ARGUMENTO_AUTORIDADE_MANUTENCAO}}` | Argumento de autoridade local | (inserir referências e clientes) |
| `{{SEGMENTOS_ADICIONAIS_ICP}}` | Linhas adicionais da tabela de ICP | (inserir se aplicável) |
| `{{MSG_ANCORA_SEM_CONTRATO}}` | Âncora para leads sem contrato | (inserir texto) |
| `{{MSG_ANCORA_INSATISFEITO}}` | Âncora para leads insatisfeitos | (inserir texto) |
| `{{MSG_ANCORA_VENCENDO}}` | Âncora para contrato vencendo | (inserir texto) |
| `{{MSG_ANCORA_PESQUISANDO}}` | Âncora para leads pesquisando | (inserir texto) |
| `{{MSG_FU2_BOT_MANUTENCAO}}` | Mensagem FU2 do BOT | (inserir texto + prova social) |
| `{{MSG_FU3_BOT_MANUTENCAO}}` | Mensagem FU3 do BOT | (inserir texto + link) |
| `{{MSG_NUTRICAO_MANUTENCAO_1}}` | Nutrição mês 1 | (inserir texto) |
| `{{MSG_NUTRICAO_MANUTENCAO_2}}` | Nutrição mês 2 | (inserir texto + link autoridade) |
| `{{MSG_NUTRICAO_MANUTENCAO_3}}` | Nutrição mês 3 | (inserir texto sobre norma/risco) |
