#!/usr/bin/env python3
"""
onboarding-revops/api.py

Commands:
  clickup_setup    <company> <onboarding_file> <date_DD/MM/YYYY> <tldv_url>
  zapsign_find     <company>
  clickup_contrato <doc1_id> <drive_contrato_url> <zapsign_url> <date_DD/MM/YYYY>
  clickup_tarefas  <tarefas_list_id>

Note: Drive setup uses Claude's Google Drive MCP (OAuth via claude.ai) and
cannot run from a standalone script. See SKILL.md Passo 6 for MCP instructions.
"""

import sys, os, json, requests
from difflib import SequenceMatcher

# ── Config ────────────────────────────────────────────────────────────────────

def _find_env():
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        c = os.path.join(d, '.env')
        if os.path.exists(c):
            return c
        d = os.path.dirname(d)
    return None

def _load_env():
    path = _find_env()
    env = {}
    if not path:
        return env
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env

_env          = _load_env()
CLICKUP_TOKEN = _env.get('CLICKUP_API_TOKEN', '')
ZAPSIGN_TOKEN = _env.get('ZAPSIGN_API_TOKEN', '')
WORKSPACE_ID  = '9011393934'
SPACE_ID      = '90113761810'   # Tipo A - Clientes
CU2           = 'https://api.clickup.com/api/v2'
CU3           = 'https://api.clickup.com/api/v3'
ZS_BASE       = 'https://api.zapsign.com.br'

MONTHS_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março',    4: 'Abril',
    5: 'Maio',    6: 'Junho',     7: 'Julho',     8: 'Agosto',
    9: 'Setembro',10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
}

def _cu():
    return {'Authorization': CLICKUP_TOKEN, 'Content-Type': 'application/json'}

def _zs():
    return {'Authorization': f'Bearer {ZAPSIGN_TOKEN}'}

# ── ClickUp low-level helpers ─────────────────────────────────────────────────

def _create_folder(name):
    r = requests.post(f'{CU2}/space/{SPACE_ID}/folder', headers=_cu(), json={'name': name})
    r.raise_for_status()
    return r.json()

ANUNCIOS_STATUSES = [
    {'status': 'brain',                'color': '#656f7d', 'type': 'open'},
    {'status': 'backlog',              'color': '#4466ff'},
    {'status': 'edicao video / design','color': '#b660e0'},
    {'status': 'revisão interna',      'color': '#d10108'},
    {'status': 'correção',             'color': '#e16b16'},
    {'status': 'aprovado',             'color': '#3db88b'},
    {'status': 'subir na planilha',    'color': '#23f6ef'},
    {'status': 'pronto p/ tráfego',    'color': '#35ff00'},
    {'status': 'testado',              'color': '#3444ea'},
    {'status': 'finalizado',           'color': '#008844', 'type': 'closed'},
]

LIST_COLUMNS = [
    {'field': 'priority',  'hidden': False, 'width': 60},
    {'field': 'assignee',  'hidden': False, 'width': 120},
    {'field': 'startDate', 'hidden': False, 'width': 120},
    {'field': 'dueDate',   'hidden': False, 'width': 120},
    {'field': 'dateDone',  'hidden': False, 'width': 120},
]

def _create_list(folder_id, name, override=False, statuses=None):
    body = {'name': name}
    if override and statuses:
        body['override_statuses'] = True
        body['statuses'] = statuses
    r = requests.post(f'{CU2}/folder/{folder_id}/list', headers=_cu(), json=body)
    r.raise_for_status()
    return r.json()

def _create_view(list_id):
    body = {
        'name': 'Lista', 'type': 'list',
        'columns': {'hidden': False, 'fields': LIST_COLUMNS},
    }
    r = requests.post(f'{CU2}/list/{list_id}/view', headers=_cu(), json=body)
    r.raise_for_status()
    return r.json()

def _create_doc(name, folder_id):
    body = {'name': name, 'parent': {'id': folder_id, 'type': 5}}
    r = requests.post(f'{CU3}/workspaces/{WORKSPACE_ID}/docs', headers=_cu(), json=body)
    r.raise_for_status()
    d = r.json()
    return d.get('id') or d.get('doc', {}).get('id', '')

def _create_page(doc_id, name, content='', parent_page_id=None):
    body = {'name': name, 'content': content, 'content_format': 'text/md'}
    if parent_page_id:
        body['parent_page_id'] = parent_page_id
    r = requests.post(f'{CU3}/workspaces/{WORKSPACE_ID}/docs/{doc_id}/pages',
                      headers=_cu(), json=body)
    r.raise_for_status()
    return r.json()

ENTREGAVEIS = """\
# Entregáveis RevOps

1. Estratégia Completa para gerar demanda
2. Gestão de Tráfego Pago (Google e Meta)
3. Criação de Anúncios (Copy + Edição de Vídeo + Design)
4. Estruturação do Processo Comercial
5. Implementação do CRM de Vendas
6. Playbook de Vendas + Scripts de Atendimento Comercial
7. Estratégias de Sucesso do Cliente e LTV
8. Reunião On-line a cada 15 dias
9. Atendimento diário no grupo de WhatsApp
"""

# ── clickup_setup ─────────────────────────────────────────────────────────────

def clickup_setup(company, onboarding_file, date_str, tldv_url):
    """
    Creates full ClickUp structure for a new RevOps client.
    Returns JSON with all IDs.
    """
    day, month_num, year = date_str.split('/')
    month_name = MONTHS_PT[int(month_num)]
    day_label  = f'{day}/{month_num}/{year[2:]}'

    with open(onboarding_file, encoding='utf-8') as f:
        content = f.read()
    content_with_link = f'[Abrir gravação no TLDV]({tldv_url})\n\n---\n\n{content}'

    _log(f'[1/8] Criando pasta "{company}"...')
    folder    = _create_folder(company)
    folder_id = folder['id']

    _log('[2/8] Criando lista Anúncios...')
    anuncios    = _create_list(folder_id, 'Anúncios', override=True, statuses=ANUNCIOS_STATUSES)
    anuncios_id = anuncios['id']

    _log('[3/8] Criando lista Tarefas...')
    tarefas    = _create_list(folder_id, 'Tarefas')
    tarefas_id = tarefas['id']

    _log('[4/8] Criando views Lista...')
    _create_view(anuncios_id)
    _create_view(tarefas_id)

    _log('[5/8] Criando Doc Docs...')
    doc1_id = _create_doc(f'Docs - {company}', folder_id)

    _log('[6/8] Criando guias em Docs...')
    _create_page(doc1_id, 'Onboarding', content_with_link)
    _create_page(doc1_id, 'Acessos')
    _create_page(doc1_id, 'Entregáveis', ENTREGAVEIS)
    _create_page(doc1_id, 'Benchmark')
    _create_page(doc1_id, 'Tráfego Pago')
    _create_page(doc1_id, 'ICP e Personas')

    _log('[7/8] Criando Doc Reuniões...')
    doc2_id = _create_doc(f'Reuniões {company}', folder_id)

    _log('[8/8] Criando hierarquia de reunião...')
    root  = _create_page(doc2_id, 'Reuniões')
    root_id = root.get('id', '')
    year_p  = _create_page(doc2_id, year, parent_page_id=root_id)
    year_id = year_p.get('id', '')
    month_p = _create_page(doc2_id, month_name, parent_page_id=year_id)
    month_id = month_p.get('id', '')
    _create_page(doc2_id, day_label, content_with_link, parent_page_id=month_id)

    print(json.dumps({
        'folder_id':       folder_id,
        'anuncios_list_id': anuncios_id,
        'tarefas_list_id':  tarefas_id,
        'doc1_id':          doc1_id,
        'doc2_id':          doc2_id,
        'note': 'Verificar modelo de status da lista Anúncios: Editar status > selecionar "Anúncios" > Aplicar alterações',
    }, ensure_ascii=False, indent=2))

# ── zapsign_find ──────────────────────────────────────────────────────────────

def zapsign_find(company):
    """Search ZapSign for a document matching company name."""
    best, best_score = None, 0.0
    page = 1
    while page <= 20:
        r = requests.get(f'{ZS_BASE}/api/v1/docs/?page={page}', headers=_zs())
        r.raise_for_status()
        data = r.json()
        for doc in data.get('results', []):
            name  = doc.get('name', '')
            score = SequenceMatcher(None, company.lower(), name.lower()).ratio()
            if company.lower() in name.lower() or name.lower() in company.lower():
                score = max(score, 0.7)
            if score > best_score:
                best_score, best = score, doc
        if not data.get('next'):
            break
        page += 1

    if best and best_score >= 0.4:
        token = best.get('token', '')
        print(json.dumps({
            'name':        best.get('name'),
            'token':       token,
            'status':      best.get('status'),
            'zapsign_url': f'https://app.zapsign.com.br/validar/{token}',
            'score':       round(best_score, 2),
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            'error': f'Contrato não encontrado para "{company}". Informe o token manualmente.',
        }))

# ── clickup_contrato ──────────────────────────────────────────────────────────

def clickup_contrato(doc1_id, drive_url, zapsign_url, date_str):
    """Add 'Contrato' page to Docs doc with Drive and ZapSign links."""
    content = f"""\
# Contrato

**Data:** {date_str}

## Links

**Pasta no Google Drive:**
[Abrir pasta Contrato no Drive]({drive_url})

**Contrato assinado (ZapSign):**
[Visualizar contrato assinado]({zapsign_url})
"""
    page    = _create_page(doc1_id, 'Contrato', content)
    page_id = page.get('id', '')
    url     = f'https://app.clickup.com/{WORKSPACE_ID}/docs/{doc1_id}/{page_id}'
    print(json.dumps({'page_id': page_id, 'url': url}, ensure_ascii=False))

# ── clickup_tarefas ───────────────────────────────────────────────────────────

ONBOARDING_TASKS = {
    'name': 'Onboarding RevOps',
    'description': '',
    'children': [
        {
            'name': 'Fase 1 - Boas Vindas',
            'description': 'Alinhar expectativas, organizar o ambiente e garantir todos os acessos necessários para execução.',
            'children': [
                {
                    'name': 'Enviar mensagem de boas vindas no grupo de WhatsApp',
                    'description': 'Todos os membros do squad devem mandar uma mensagem de boas vindas no WhatsApp se apresentando de forma profissional a equipe do novo cliente.\n\nDefinição de pronto: Todos os membros do squad enviaram a mensagem no grupo.\nResponsável: Todos os membros do squad',
                },
                {
                    'name': 'Realizar reunião de onboarding com o cliente',
                    'description': 'Fazer a reunião de onboarding para alinhar objetivos, escopo, expectativas e forma de trabalho do projeto RevOps. Devemos gravar essa reunião com o TLDV e seguir o escopo do documento da reunião de onboarding.\n\nDefinição de pronto: Reunião realizada e principais decisões registradas no documento de onboarding.\nResponsável: Customer Success',
                },
                {
                    'name': 'Criar documento de onboarding do cliente',
                    'description': "Pegar gravação no TLDV e criar documento de onboarding com informações estratégicas, acessos, decisões e visão geral do projeto. Esse documento deve ser criado na parte 'Documentos' que fica dentro da pasta do cliente no ClickUp.\n\nDefinição de pronto: Documento criado e salvo no Google Drive e ClickUp do cliente.\nResponsável: Customer Success",
                },
                {
                    'name': 'Criar ClickUp',
                    'description': 'Criar pasta do cliente dentro do ClickUp com as seguintes sessões: Anúncios (lista), Tarefas (lista), Documentos (docs).\n\nDefinição de pronto: ClickUp criado com as 3 sessões com os status da tarefa configurados corretamente.\nResponsável: Customer Success',
                },
                {
                    'name': 'Criar Google Drive',
                    'description': 'Criar e organizar as pastas do projeto do cliente para centralizar todos os arquivos no Google Drive. Pastas: Anúncios, Fotos e Vídeos, Identidade Visual, Planilhas, Marketing, Comercial, CS, Planejamento RevOps.\n\nDefinição de pronto: Google Drive criado com estrutura padrão e compartilhado no grupo do cliente.\nResponsável: Customer Success',
                },
                {
                    'name': 'Coletar Acessos Necessários',
                    'description': 'Solicitar e validar todos os acessos essenciais para execução do projeto: Acesso Wordpress, Domínio, Hospedagem, CRM, Playbook de Vendas, Meta Ads, Google Ads.\n\nDefinição de pronto: Todos os acessos recebidos, testados e funcionando.\nResponsável: Customer Success',
                },
                {
                    'name': 'Solicitar Fotos, Vídeos, ID Visual e outros',
                    'description': 'Precisamos que o cliente faça o upload de fotos, vídeos, ID Visual (Logo, PDF, Tipografia, etc) e outros materiais relevantes para o projeto como planilhas e documentos.\nSolicitar: Fotos do Serviço/Produto, Vídeos do Serviço/Produto, Identidade Visual (Logo, PDF, Tipografia, Paleta de Cor), Planilhas, Documentos, Proposta Comercial.\n\nDefinição de pronto: Cliente fez o upload de todos os materiais solicitados na pasta correta do Drive.\nResponsável: Customer Success',
                },
                {
                    'name': 'Definir as Reuniões do Google Agenda',
                    'description': 'Alinhar com o cliente qual será a frequência, dia e horários das nossas reuniões quinzenais de alinhamento.\n\nDefinição de pronto: Reuniões criadas no Google Agenda (da DVE), adicionado o e-mail de todos os participantes e comunicado no grupo.\nResponsável: Customer Success',
                },
            ],
        },
        {
            'name': 'Fase 2 - Diagnóstico',
            'description': '',
            'children': [
                {
                    'name': 'Realizar Benchmark',
                    'description': 'Analisar concorrentes diretos e referências do mercado para identificar padrões e oportunidades. Realizar pesquisa com pelo menos 5 empresas do segmento analisando: canais de aquisição, funil de marketing, anúncios, oferta escalada, diferencial competitivo, posicionamento, provas sociais, processo comercial e follow up.\n\nDefinição de pronto: Benchmark documentado no Google Docs, adicionado ao Drive, link no ClickUp, aprovado internamente e pelo cliente.\nResponsável: Analista',
                },
                {
                    'name': 'Analisar Campanhas de Tráfego',
                    'description': 'Analisar o histórico das campanhas de tráfego pago e mapear os criativos e públicos vencedores.\n\nDefinição de pronto: Análise do desempenho das campanhas documentado em Planilha e/ou Google Docs.\nResponsável: Danilo',
                },
                {
                    'name': 'Analisar Presença Digital',
                    'description': 'Analisar como o cliente se posiciona hoje no digital em todos os canais ativos, mapeando gargalos, alavancas de crescimento e próximos passos.\n\nDefinição de pronto: Análise registrada em Google Docs com pontos fortes, pontos fracos e oportunidades.\nResponsável: Davi',
                },
                {
                    'name': 'Analisar e Criar Oferta',
                    'description': 'Analisar se a oferta do cliente realmente é boa. Ver a gravação no TLDV na parte que fala sobre a oferta e também o site.\n\nDefinição de pronto: Oferta atual analisada e documentada com ajustes sugeridos.\nResponsável: Danilo',
                },
                {
                    'name': 'Analisar diferencial competitivo',
                    'description': 'Ver a reunião de onboarding no TLDV e analisar a parte que o cliente fala sobre o diferencial competitivo. Verificar se o diferencial realmente é relevante para o mercado e ICP. Caso não for relevante, comunicar com o cliente para criar um.\n\nDefinição de pronto: Diferencial competitivo analisado e documentado.\nResponsável: Danilo',
                },
                {
                    'name': 'Analisar e Criar ICP e Personas',
                    'description': 'Definir o perfil de cliente ideal e as personas que o funil deve atrair.\n\nDefinição de pronto: ICP e personas documentados e aprovados.\nResponsável: Líder de Receita',
                },
                {
                    'name': 'Analisar e Mapear Jornada de Compra',
                    'description': 'Mapear o caminho do cliente desde o primeiro contato até a venda.\n\nDefinição de pronto: Jornada documentada com etapas claras.\nResponsável: Líder de Receita',
                },
                {
                    'name': 'Analisar e Definir Funil de Captação',
                    'description': 'Definir a estrutura do funil (topo, meio e fundo) alinhada ao ICP e à jornada de compra do cliente.\n\nDefinição de pronto: Funil analisado e documentado.\nResponsável: Líder de Receita',
                },
                {
                    'name': 'Criar Planejamento RevOps',
                    'description': 'Consolidar todas as decisões da fase de diagnóstico em um plano único de ação.\n\nDefinição de pronto: Planejamento RevOps documentado e validado internamente.\nResponsável: Líder de Receita',
                },
                {
                    'name': 'Realizar Reunião de Apresentação do Planejamento',
                    'description': 'Apresentar o diagnóstico e alinhar expectativas antes da implementação.\n\nDefinição de pronto: Planejamento aprovado pelo cliente.\nResponsável: Líder de Receita',
                },
            ],
        },
        {
            'name': 'Fase 3 - Estruturação',
            'description': '',
            'children': [
                {
                    'name': 'Marketing',
                    'description': '',
                    'children': [
                        {
                            'name': 'Configurar tracking e eventos',
                            'description': 'Configurar todas as ferramentas de tracking necessárias para mensurar leads, conversões e desempenho das campanhas.\n\nDefinição de pronto: Eventos configurados, testados e disparando corretamente.\nResponsável: Gestor de Tráfego',
                        },
                        {
                            'name': 'Configurar contas de anúncios',
                            'description': 'Configurar contas de anúncios que serão usadas na operação.\n\nDefinição de pronto: Conta(s) configurada(s) e pronta(s) para criação de campanhas.\nResponsável: Gestor de Tráfego',
                        },
                        {
                            'name': 'Criar planilha de tráfego',
                            'description': 'Criar planilha para controle de investimentos, métricas e decisões de tráfego.\n\nDefinição de pronto: Planilha criada, estruturada e salva no Drive do cliente.\nResponsável: Gestor de Tráfego',
                        },
                        {
                            'name': 'Criar planilha de leads - Landing Page',
                            'description': 'Criar planilha para registrar todos os leads cadastrados na Landing Page.\n\nDefinição de pronto: Planilha criada e integrada ao Wordpress.\nResponsável: Webdesigner',
                        },
                        {
                            'name': 'Escrever copy da landing page',
                            'description': 'Escrever toda a copy da landing page com base no ICP, oferta e diferencial competitivo definidos.\n\nDefinição de pronto: Copy finalizada, revisada e aprovada internamente.\nResponsável: Copywriter',
                        },
                        {
                            'name': 'Criar design da landing page',
                            'description': 'Criar o design visual da landing page seguindo o wireframe e a identidade do cliente.\nChecklist: Design responsivo (desktop/mobile), identidade visual respeitada, CTA destacado visualmente, layout focado em conversão.\n\nDefinição de pronto: Design final aprovado internamente.',
                        },
                        {'name': 'Implementar Landing Page no Wordpress', 'description': ''},
                        {'name': 'Integrar landing page ao tracking e fluxo de leads', 'description': ''},
                        {
                            'name': 'Revisar landing page antes da ativação',
                            'description': 'Revisão final da landing page para evitar erros antes de iniciar campanhas.\n\nDefinição de pronto: Landing page revisada e liberada para tráfego.\nResponsável: Líder de Receita',
                        },
                        {'name': 'Definir estratégia de campanhas de tráfego', 'description': ''},
                        {'name': 'Criar Copy | RM 01', 'description': ''},
                    ],
                },
                {
                    'name': 'Comercial',
                    'description': '',
                    'children': [
                        {'name': 'Definir processos comerciais', 'description': ''},
                        {'name': 'Implementar CRM', 'description': ''},
                        {'name': 'Integrar leads ao CRM', 'description': ''},
                        {'name': 'Criar playbook de vendas', 'description': ''},
                        {'name': 'Criar Copy PDF Comercial', 'description': ''},
                        {'name': 'Criar Design PDF Comercial', 'description': ''},
                        {'name': 'Criar Planilha RevOps', 'description': ''},
                        {'name': 'Testar Processo Comercial antes da ativação', 'description': ''},
                    ],
                },
                {
                    'name': 'Sucesso do Cliente',
                    'description': '',
                    'children': [
                        {'name': 'Definir modelo de acompanhamento do cliente', 'description': ''},
                        {'name': 'Definir métricas de sucesso do cliente', 'description': ''},
                        {'name': 'Criar pesquisa de satisfação / NPS', 'description': ''},
                        {'name': 'Definir momentos de aplicação da pesquisa', 'description': ''},
                        {'name': 'Criar rotina de feedback com o cliente', 'description': ''},
                        {'name': 'Definir processo de tratamento de insatisfação', 'description': ''},
                        {'name': 'Criar registro de histórico do cliente', 'description': ''},
                        {'name': 'Validar estrutura de CS antes da ativação', 'description': ''},
                    ],
                },
            ],
        },
        {
            'name': 'Fase 4 - Ativação',
            'description': '',
            'children': [
                {'name': 'Subir Campanhas de Tráfego', 'description': ''},
                {'name': 'Validar Jornada de Compra', 'description': ''},
                {'name': 'Analisar métricas iniciais da operação', 'description': ''},
                {'name': 'Brainstorm interno após ativação', 'description': ''},
                {'name': 'Definir rotina de acompanhamento recorrente', 'description': ''},
                {'name': 'Formalizar encerramento do onboarding', 'description': ''},
                {'name': 'Registrar lições aprendidas do onboarding', 'description': ''},
            ],
        },
    ],
}

def _create_task(list_id, name, description, parent_id=None):
    body = {'name': name, 'status': 'backlog'}
    if description:
        body['description'] = description
    if parent_id:
        body['parent'] = parent_id
    r = requests.post(f'{CU2}/list/{list_id}/task', headers=_cu(), json=body)
    r.raise_for_status()
    return r.json()

def _build_tasks(list_id, task_def, parent_id=None, depth=0):
    _log('  ' * depth + f'+ {task_def["name"]}')
    t = _create_task(list_id, task_def['name'], task_def.get('description', ''), parent_id)
    for child in task_def.get('children', []):
        _build_tasks(list_id, child, t['id'], depth + 1)
    return t['id']

def clickup_tarefas(tarefas_list_id):
    """Create full onboarding task hierarchy in the given list."""
    _log('Criando hierarquia de tarefas de onboarding...')
    mae_id = _build_tasks(tarefas_list_id, ONBOARDING_TASKS)
    print(json.dumps({'mae_id': mae_id, 'list_id': tarefas_list_id}, ensure_ascii=False))

# ── Util ──────────────────────────────────────────────────────────────────────

def _log(msg):
    print(msg, file=sys.stderr)

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd  = sys.argv[1]
    args = sys.argv[2:]

    try:
        if   cmd == 'clickup_setup':    clickup_setup(args[0], args[1], args[2], args[3])
        elif cmd == 'zapsign_find':     zapsign_find(args[0])
        elif cmd == 'clickup_contrato': clickup_contrato(args[0], args[1], args[2], args[3])
        elif cmd == 'clickup_tarefas':  clickup_tarefas(args[0])
        else:
            print(f'Comando desconhecido: {cmd}')
            print(__doc__)
            sys.exit(1)
    except Exception as e:
        import traceback
        print(json.dumps({'error': str(e), 'trace': traceback.format_exc()}), file=sys.stderr)
        sys.exit(1)
