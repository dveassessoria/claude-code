#!/usr/bin/env python3
"""
Minuta API — TLDV + ClickUp integration
Commands:
  tldv_list                              list 5 most recent meetings
  tldv_transcript <meeting_id>           get transcript as formatted text
  tldv_info <meeting_id>                 get meeting metadata as JSON
  clickup_docs                           list all Reuniões docs
  clickup_find <client_name>             find best matching Reuniões doc (returns JSON)
  clickup_save <doc_id> <DD/MM/YYYY> <content_file>  save minuta with year/month/day hierarchy
"""

import sys, os, json, re, requests
from datetime import datetime, timezone, timedelta
from difflib import SequenceMatcher

# ── Config ────────────────────────────────────────────────────────────────────

def find_env_file():
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        candidate = os.path.join(d, '.env')
        if os.path.exists(candidate):
            return candidate
        d = os.path.dirname(d)
    return None

def load_env():
    path = find_env_file()
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

_env = load_env()
TLDV_KEY       = _env.get('TLDV_API_KEY', '')
CLICKUP_TOKEN  = _env.get('CLICKUP_API_TOKEN', '')
WORKSPACE_ID   = '9011393934'
TLDV_BASE      = 'https://pasta.tldv.io/v1alpha1'
CLICKUP_BASE   = 'https://api.clickup.com/api/v3'
MEETINGS_CACHE = '/tmp/tldv_meetings_dve.json'

DVE_EMAILS = {
    'dvemarketingadm@gmail.com',
    'santanadaniloads@gmail.com',
    'daviniciusmkt@gmail.com',
    'contatorafamachadoc@icloud.com',
    'aricriativa.br@gmail.com',
    'contatokauanalvess@gmail.com',
}

MONTHS_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio',    6: 'Junho',     7: 'Julho',  8: 'Agosto',
    9: 'Setembro',10: 'Outubro', 11: 'Novembro',12: 'Dezembro',
}

BRT = timezone(timedelta(hours=-3))

def parse_tldv_date(s):
    """Parse TLDV date string to BRT datetime."""
    s = re.sub(r'\s*\(.*?\)', '', s).strip()
    for fmt in ('%a %b %d %Y %H:%M:%S GMT%z', '%a %b %d %Y %H:%M:%S %z'):
        try:
            return datetime.strptime(s, fmt).astimezone(BRT)
        except ValueError:
            continue
    return datetime.now(BRT)

def tldv_headers():
    return {'x-api-key': TLDV_KEY}

def clickup_headers():
    return {'Authorization': CLICKUP_TOKEN, 'Content-Type': 'application/json'}

# ── TLDV ──────────────────────────────────────────────────────────────────────

def tldv_list():
    r = requests.get(f'{TLDV_BASE}/meetings/?limit=10', headers=tldv_headers())
    r.raise_for_status()
    meetings = r.json()['results'][:5]
    with open(MEETINGS_CACHE, 'w') as f:
        json.dump(meetings, f, ensure_ascii=False)
    for i, m in enumerate(meetings, 1):
        dt = parse_tldv_date(m['happenedAt'])
        date_fmt = dt.strftime('%d/%m/%Y %H:%M')
        mins = int(m['duration'] / 60)
        print(f"{i}. {m['name']}  |  {date_fmt}  |  {mins} min  |  ID: {m['id']}")

def tldv_transcript(meeting_id):
    r = requests.get(f'{TLDV_BASE}/meetings/{meeting_id}/transcript', headers=tldv_headers())
    r.raise_for_status()
    segments = r.json().get('data', [])

    lines = []
    current_speaker = None
    buffer = []

    for seg in segments:
        sp  = seg.get('speaker', 'Desconhecido').strip()
        txt = seg.get('text', '').strip()
        if not txt:
            continue
        if sp != current_speaker:
            if current_speaker is not None and buffer:
                lines.append(f"**{current_speaker}:** {' '.join(buffer)}")
            current_speaker = sp
            buffer = [txt]
        else:
            buffer.append(txt)

    if current_speaker and buffer:
        lines.append(f"**{current_speaker}:** {' '.join(buffer)}")

    print('\n\n'.join(lines))

def tldv_info(meeting_id):
    """Return meeting metadata as JSON (reads from cache or re-fetches)."""
    meetings = []
    try:
        with open(MEETINGS_CACHE) as f:
            meetings = json.load(f)
    except Exception:
        r = requests.get(f'{TLDV_BASE}/meetings/?limit=10', headers=tldv_headers())
        meetings = r.json().get('results', [])

    m = next((x for x in meetings if x['id'] == meeting_id), None)
    if not m:
        print(json.dumps({'error': f'Meeting {meeting_id} not found. Run tldv_list first.'}))
        return

    dt = parse_tldv_date(m['happenedAt'])

    client_invitees = [
        inv for inv in m.get('invitees', [])
        if inv.get('email', '').lower() not in DVE_EMAILS and inv.get('name', '').strip()
    ]
    client_contact = client_invitees[0]['name'].strip() if client_invitees else ''

    # Company name = first segment of meeting title (before " - ")
    company = m['name'].split(' - ')[0].strip()

    print(json.dumps({
        'name':          m['name'],
        'company':       company,
        'client_contact': client_contact,
        'date':          dt.strftime('%d/%m/%Y'),
        'year':          str(dt.year),
        'month':         MONTHS_PT[dt.month],
        'day_page':      dt.strftime('%d/%m/%y'),
        'duration_min':  int(m['duration'] / 60),
        'invitees':      m.get('invitees', []),
    }, ensure_ascii=False))

# ── ClickUp ───────────────────────────────────────────────────────────────────

def _all_docs():
    r = requests.get(
        f'{CLICKUP_BASE}/workspaces/{WORKSPACE_ID}/docs?limit=100',
        headers=clickup_headers()
    )
    r.raise_for_status()
    return r.json().get('docs', [])

def clickup_docs():
    reunioes = [d for d in _all_docs() if 'reuni' in d['name'].lower()]
    for d in reunioes:
        print(f"{d['id']}  |  {d['name']}")

def clickup_find(client_query):
    reunioes = [d for d in _all_docs() if 'reuni' in d['name'].lower()]
    best, best_score = None, 0.0

    for d in reunioes:
        # Strip "Reuniões" prefix for a cleaner comparison
        doc_client = re.sub(r'^reuni[oõ]es\s*[-–]?\s*', '', d['name'], flags=re.IGNORECASE).strip()
        score = SequenceMatcher(None, client_query.lower(), doc_client.lower()).ratio()
        # Bonus: substring match
        if client_query.lower() in doc_client.lower() or doc_client.lower() in client_query.lower():
            score = max(score, 0.75)
        if score > best_score:
            best_score, best = score, d

    if best:
        print(json.dumps({'id': best['id'], 'name': best['name'], 'score': round(best_score, 2)},
                         ensure_ascii=False))
    else:
        print(json.dumps({'error': 'No matching doc found'}))

def _get_page_tree(doc_id):
    """Return full nested page tree (ClickUp nests children in 'pages' key)."""
    r = requests.get(
        f'{CLICKUP_BASE}/workspaces/{WORKSPACE_ID}/docs/{doc_id}/pages?content_format=text/md',
        headers=clickup_headers()
    )
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, list) else data.get('pages', [])

def _create_page(doc_id, name, content='', parent_page_id=None):
    body = {'name': name, 'content': content, 'content_format': 'text/md'}
    if parent_page_id:
        body['parent_page_id'] = parent_page_id
    r = requests.post(
        f'{CLICKUP_BASE}/workspaces/{WORKSPACE_ID}/docs/{doc_id}/pages',
        headers=clickup_headers(),
        json=body
    )
    r.raise_for_status()
    return r.json()

def _find_child(page, name):
    """Find a direct child page by name within a page's 'pages' list."""
    for child in page.get('pages', []):
        if child.get('name', '').strip() == name:
            return child
    return None

def clickup_save(doc_id, date_str, content_file, meeting_url=''):
    """
    Save minuta navigating the existing hierarchy:
    root_page → year (e.g. "2026") → month (e.g. "Maio") → day (e.g. "27/05/26")
    Prepends a clickable TLDV link if meeting_url is provided.
    """
    day, month_num, year = date_str.split('/')
    month_name = MONTHS_PT[int(month_num)]
    year_str   = year                              # e.g. "2026"
    day_label  = f'{day}/{month_num}/{year[2:]}'   # e.g. "27/05/26"

    with open(content_file, encoding='utf-8') as f:
        content = f.read()

    # Prepend TLDV link if provided
    if meeting_url:
        content = f'[Abrir gravacao no TLDV]({meeting_url})\n\n---\n\n' + content

    # Get full page tree
    tree = _get_page_tree(doc_id)
    if not tree:
        raise RuntimeError('No pages found in this doc.')

    # Root page = first page in the doc (e.g. "Reuniões 2026" or "Reuniões")
    root_page = tree[0]
    root_id   = root_page['id']

    # Year page = direct child of root named e.g. "2026"
    year_page = _find_child(root_page, year_str)
    if not year_page:
        year_page = _create_page(doc_id, year_str, '', root_id)
        tree = _get_page_tree(doc_id)
        root_page = tree[0]
        year_page = _find_child(root_page, year_str) or year_page
    year_id = year_page['id']

    # Month page = direct child of year
    month_page = _find_child(year_page, month_name)
    if not month_page:
        month_page = _create_page(doc_id, month_name, '', year_id)
        tree = _get_page_tree(doc_id)
        root_page = tree[0]
        year_page  = _find_child(root_page, year_str) or year_page
        month_page = _find_child(year_page, month_name) or month_page
    month_id = month_page['id']

    # Day page = new child of month
    day_page = _create_page(doc_id, day_label, content, month_id)
    page_id  = day_page.get('id', '')

    url = f'https://app.clickup.com/{WORKSPACE_ID}/docs/{doc_id}/{page_id}'
    print(json.dumps({'page_id': page_id, 'url': url, 'name': day_label}, ensure_ascii=False))

# ── Task creation ─────────────────────────────────────────────────────────────

CLIENT_SPACES = ['90113761810', '90114165992']  # Tipo A, Tipo B

def _all_client_folders():
    """Return all folders from both client spaces."""
    folders = []
    for space_id in CLIENT_SPACES:
        r = requests.get(
            f'https://api.clickup.com/api/v2/space/{space_id}/folder?archived=false',
            headers=clickup_headers()
        )
        r.raise_for_status()
        folders.extend(r.json().get('folders', []))
    return folders

def clickup_find_list(client_query):
    """Find the 'Tarefas' list in the best-matching client folder."""
    folders = _all_client_folders()
    best, best_score = None, 0.0

    for f in folders:
        score = SequenceMatcher(None, client_query.lower(), f['name'].lower()).ratio()
        if client_query.lower() in f['name'].lower() or f['name'].lower() in client_query.lower():
            score = max(score, 0.75)
        if score > best_score:
            best_score, best = score, f

    if not best:
        print(json.dumps({'error': 'No matching client folder found'}))
        return

    tarefas = next(
        (l for l in best.get('lists', []) if 'tarefa' in l['name'].lower()),
        None
    )
    if not tarefas:
        print(json.dumps({'error': f"No 'Tarefas' list in folder '{best['name']}'"}))
        return

    print(json.dumps({
        'list_id':     tarefas['id'],
        'list_name':   tarefas['name'],
        'folder_name': best['name'],
        'score':       round(best_score, 2),
    }, ensure_ascii=False))

def clickup_create_tasks(list_id, tasks_file):
    """
    Create tasks from a JSON file (array of strings) in the given list.
    Status: backlog. No assignee.
    """
    with open(tasks_file, encoding='utf-8') as f:
        tasks = json.load(f)

    created = []
    for name in tasks:
        r = requests.post(
            f'https://api.clickup.com/api/v2/list/{list_id}/task',
            headers=clickup_headers(),
            json={'name': name, 'status': 'backlog'}
        )
        r.raise_for_status()
        t = r.json()
        created.append({'id': t['id'], 'name': t['name'], 'url': t.get('url', '')})

    print(json.dumps({'created': len(created), 'tasks': created}, ensure_ascii=False))

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd  = sys.argv[1]
    args = sys.argv[2:]

    try:
        if   cmd == 'tldv_list':             tldv_list()
        elif cmd == 'tldv_transcript':       tldv_transcript(args[0])
        elif cmd == 'tldv_info':             tldv_info(args[0])
        elif cmd == 'clickup_docs':          clickup_docs()
        elif cmd == 'clickup_find':          clickup_find(args[0])
        elif cmd == 'clickup_save':          clickup_save(args[0], args[1], args[2], args[3] if len(args) > 3 else '')
        elif cmd == 'clickup_find_list':     clickup_find_list(args[0])
        elif cmd == 'clickup_create_tasks':  clickup_create_tasks(args[0], args[1])
        else:
            print(f'Comando desconhecido: {cmd}')
            print(__doc__)
            sys.exit(1)
    except Exception as e:
        import traceback
        print(json.dumps({'error': str(e), 'trace': traceback.format_exc()}), file=sys.stderr)
        sys.exit(1)
