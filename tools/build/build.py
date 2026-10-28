"""Build the Russian law repository from the cache of the state legal information system (ips.pravo.gov.ru).

    python scripts/russia-law/build.py ~/Documents/russia-law --today YYYY-MM-DD [--only TYPES] [--workers 4]

Steps:
1. Parse every cached edition text (parse_text.py), cached as .cache/parsed/<nd>/<rdk>.json.
2. For each act (Constitution, federal constitutional laws, codes, federal laws that are not purely amending), take
   its editions (`redactions` on its card) in order. Each edition has the date it applies from and names the act
   that made it (`refadoption`). Editions the system lists without a text of its own (`completed: false`) carry
   no text; their changes reach the record through the next edition that has one.
3. Each edition's text is compared with the one before, unit by unit (article, appendix, title). A changed unit is
   credited to the edition's act, unless the change newly cites (in the unit's own history notes, `(В редакции
   Федерального закона от 30.12.2012 № 302-ФЗ)`) one of the acts whose editions have no text of their own, or one
   of those acts' edition lists the article (`comment`: `ст. 64`); then to the latest such act. `Evidence:` says
   which. An edition that names no act (`с учетом уточнений`, with corrections) is a publisher commit.
4. Commits: one per amending act per in-force date, across every act it touched, at noon Moscow time (zone rules
   hard-coded below). Dates before 1970 are clamped to 1970-01-01 one second apart, the real date in `In-force:`.
   Editions that apply after --today go on the branch `future`, never on main. Written with one git fast-import,
   so the same cache gives the same hashes.
"""
import argparse
import gzip
import json
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
CACHE = HERE / '.cache'
CARDS = CACHE / 'cards'
TEXT = CACHE / 'text'
PARSED = CACHE / 'parsed'
PARSER_VERSION = '2'

COMMITTER = 'Lexifina <russia-law@lexifina.com>'
PUBLISHER = ('Законодательство России (pravo.gov.ru)', 'ips@pravo.gov.invalid')
TYPE_DIR = {'Конституция': 'constitution', 'Федеральный конституционный закон': 'fkz', 'Кодекс': 'code',
            'Федеральный закон': 'fz'}
TYPE_NAME = {'Конституция': 'Constitution', 'Федеральный конституционный закон': 'Federal constitutional law',
             'Кодекс': 'Code', 'Федеральный закон': 'Federal law'}
TYPE_ORDER = {'Конституция': 0, 'Федеральный конституционный закон': 1, 'Кодекс': 2, 'Федеральный закон': 3}
LATIN = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
                 ['a', 'b', 'v', 'g', 'd', 'e', 'e', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't',
                  'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']))
ACT = re.compile(r'^(.*?)\s+от\s+(\d\d)\.(\d\d)\.(\d{4})(?:\s*г\.)?\s+№\s*(\S+)\s*$')
CITE = re.compile(r'от\s+(\d\d)\.(\d\d)\.(\d{4})(?:\s*г\.)?\s*№\s*([0-9]+[0-9A-Za-zА-Яа-яЁё/-]*)')


# ---------------------------------------------------------------------------------------------------- dates

def last_sunday(y: int, m: int) -> date:
    d = (date(y, m + 1, 1) if m < 12 else date(y + 1, 1, 1)) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() + 1) % 7)


def moscow_offset(day: str) -> int:
    """Hours east of UTC at noon in Moscow on `day` (no tzdata on the build machine, so the rules are here).
    1981-1983 summer time 1 Apr - 1 Oct; 1984-1990 last Sunday of March - last Sunday of September (+4, else +3);
    31.03.1991 - 29.09.1991 +3 and then +2 (Moscow kept summer time but dropped standard time); from 19.01.1992 +3
    again with summer time +4 to the last Sunday of September (1992-1995) or of October (1996-2010); 27.03.2011 -
    26.10.2014 +4 all year; +3 all year since 26.10.2014."""
    d = date.fromisoformat(day)
    if d >= date(2014, 10, 26):
        return 3
    if d >= date(2011, 3, 27):
        return 4
    if d >= date(1992, 1, 19):
        end = last_sunday(d.year, 9 if d.year <= 1995 else 10)
        return 4 if last_sunday(d.year, 3) <= d < end else 3
    if d >= date(1991, 9, 29):
        return 2
    if d >= date(1991, 3, 31):
        return 3
    if 1984 <= d.year <= 1990:
        return 4 if last_sunday(d.year, 3) <= d < last_sunday(d.year, 9) else 3
    if 1981 <= d.year <= 1983:
        return 4 if date(d.year, 4, 1) <= d < date(d.year, 10, 1) else 3
    return 3


def git_date(day: str, seq: int) -> str:
    off = moscow_offset(day)
    d = datetime.strptime(day, '%Y-%m-%d').replace(hour=12 - off, tzinfo=timezone.utc)
    ts = int(d.timestamp()) if d.year >= 1970 else seq
    return f'{ts} +{off:02d}00'


def dmy(s: str | None) -> str | None:
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', s or '')
    return f'{m.group(3)}-{m.group(2)}-{m.group(1)}' if m else None


def ddmmyyyy(d: str) -> str:
    return f'{d[8:10]}.{d[5:7]}.{d[:4]}' if d else ''


# ---------------------------------------------------------------------------------------------------- acts

def translit(s: str) -> str:
    out = ''.join(LATIN.get(c, c) for c in s.lower())
    return re.sub(r'[^a-z0-9]+', '-', out).strip('-')


def parse_act(s: str | None, nd: str | None = None) -> dict | None:
    """'Федеральный закон от 30.12.2012 № 302-ФЗ' -> {'kind', 'date', 'number', 'nd', 'label'}."""
    if not s:
        return None
    m = ACT.match(s.strip())
    if not m:
        return {'kind': s.strip(), 'date': None, 'number': '', 'nd': nd, 'label': s.strip()}
    return {'kind': m.group(1), 'date': f'{m.group(4)}-{m.group(3)}-{m.group(2)}', 'number': m.group(5), 'nd': nd,
            'label': s.strip()}


def act_key(a: dict | None) -> str:
    if a is None:
        return 'publisher'
    return f"nd{a['nd']}" if a.get('nd') else f"{a.get('date')}|{a.get('number')}|{a.get('kind')}"


def act_cite(a: dict) -> tuple:
    return (a.get('date'), a.get('number'))


KIND_SHORT = [('Постановление Конституционного Суда', 'ks'), ('Указ Президента', 'ukaz'),
              ('о поправке к Конституции', 'popravka'), ('Федеральный конституционный закон', 'fkz'),
              ('Федеральный закон', 'fz'), ('Кодекс', 'kodeks'), ('Закон', 'zakon')]


def act_ident(a: dict) -> tuple[str, str]:
    """Author name and an address that cannot exist: `302-ФЗ (30.12.2012) <302-fz-20121230@pravo.gov.invalid>`."""
    d = a.get('date') or ''
    num = a.get('number') or ''
    short = next((v for k, v in KIND_SHORT if k in a.get('kind', '')), 'act')
    if num and not re.search(r'[А-Яа-я]', num):
        num_name = f'{num}' if short in ('fz', 'fkz') else f'№ {num}'
    else:
        num_name = num
    if short == 'ukaz':
        num_name = f'Указ № {num}'
    elif short == 'ks':
        num_name = f'Постановление КС № {num}'
    name = f'{num_name} ({ddmmyyyy(d)})' if num and d else a.get('label', 'act')
    local = translit(num) if num else ''
    if short not in ('fz', 'fkz', 'popravka') or not local.endswith(('fz', 'fkz')):
        local = f'{short}-{local}' if local else short
    email = f"{local}-{d.replace('-', '')}@pravo.gov.invalid" if d else f"act-{a.get('nd') or 'x'}@pravo.gov.invalid"
    return name, email


COMMENT_TOKEN = re.compile(r'(ст|гл|п|разд|прил|ч|наим|абз)\.?|(\d+(?:-\d+)*)')


def comment_articles(comment: str | None) -> set[str]:
    """`ст. 8-1, 64, 94, наим. гл. 7, ст. 125` -> {'8-1', '64', '94', '125'}: article numbers an edition lists."""
    out, kind = set(), None
    for m in COMMENT_TOKEN.finditer(comment or ''):
        if m.group(1):
            kind = m.group(1)
        elif kind == 'ст':
            out.add(m.group(2))
    return out


# ---------------------------------------------------------------------------------------------------- parsing

def parsed_path(nd: str, rdk: int) -> Path:
    return PARSED / nd / f'{rdk}.json'


def parse_one(key: tuple[str, int]) -> None:
    nd, rdk = key
    out = parsed_path(nd, rdk)
    if out.exists():
        try:
            if json.loads(out.read_text('utf-8')).get('parser') == PARSER_VERSION:
                return
        except json.JSONDecodeError:
            pass
    import parse_text
    try:
        d = parse_text.parse(gzip.decompress((TEXT / nd / f'{rdk}.html.gz').read_bytes()).decode('utf-8'))
    except Exception as e:  # noqa: BLE001 - recorded, the edition is skipped
        d = {'error': f'{type(e).__name__}: {e}', 'front': [], 'units': []}
    d['parser'] = PARSER_VERSION
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(d, ensure_ascii=False), 'utf-8')


def load_parsed(nd: str, rdk: int) -> dict | None:
    p = parsed_path(nd, rdk)
    if not p.exists():
        return None
    return json.loads(p.read_text('utf-8'))


# ---------------------------------------------------------------------------------------------------- files

def norm(s: str) -> str:
    s = s.replace('­', '')
    return re.sub(r'\s+', ' ', s).strip()


def squash(s: str) -> str:
    return re.sub(r'\s+', '', s)


def cites(lines: list[str]) -> set[tuple]:
    out = set()
    for l in lines:
        for d, m, y, num in CITE.findall(l):
            out.add((f'{y}-{m}-{d}', num))
    return out


def unit_text(u: dict) -> str:
    lines = [f'## {norm(h)}' for h in u['heading'] if norm(h)]
    lines.append(f"# {norm(u['title'])} {norm(u.get('name') or '')}".rstrip())
    lines.extend(norm(l) for l in u['lines'] if norm(l))
    return '\n'.join(lines) + '\n'


def version_files(law: dict, parsed: dict) -> dict[str, tuple[str, set]]:
    files: dict[str, tuple[str, set]] = {}
    d = law['dir']
    if parsed.get('front'):
        files[f'{d}/title.md'] = ('\n'.join(norm(l) for l in parsed['front'] if norm(l)) + '\n', cites(parsed['front']))
    for u in parsed['units']:
        files[f"{d}/{u['id']}.md"] = (unit_text(u), cites(u['lines'] + [u.get('name') or '']))
    return files


# ---------------------------------------------------------------------------------------------------- history

def law_dir(row: dict, used: set) -> str:
    t = TYPE_DIR[row['type']]
    if t == 'constitution':
        return 'constitution'
    a = parse_act(row['adoption'])
    if a and a['date'] and a['number']:
        name = f"{a['date'][:4]}-{translit(a['number'])}"
    else:
        name = f"nd-{row['nd']}"
    d = f'{t}/{name}'
    if d in used:
        d = f'{t}/{name}-nd{row["nd"]}'
    used.add(d)
    return d


def load_laws(only: set | None) -> list[dict]:
    cat = [r for r in json.loads((CACHE / 'catalogue.json').read_text('utf-8')) if not r['amending']]
    cat.sort(key=lambda r: (TYPE_ORDER[r['type']], dmy(r.get('docdate')) or '', r['nd']))
    laws, used = [], set()
    for r in cat:
        if only and r['type'] not in only and r['nd'] not in only:
            continue
        p = CARDS / f"{r['nd']}.json"
        if not p.exists():
            continue
        card = json.loads(p.read_text('utf-8'))
        eds = []
        for red in sorted(card.get('redactions') or [], key=lambda x: int(x['id'])):
            eds.append({'rdk': int(red['id']), 'date': dmy(red['date']), 'act': parse_act(red.get('refadoption'),
                                                                                         red.get('refnd')),
                        'comment': red.get('comment') or '', 'reason': red.get('redreason') or '',
                        'has_text': (TEXT / r['nd'] / f"{int(red['id'])}.html.gz").exists(),
                        'official': red.get('official')})
        a = parse_act(r['adoption'])
        laws.append({'nd': r['nd'], 'type': r['type'], 'title': card.get('name') or r['name'],
                     'adoption': r['adoption'], 'enacted': a['date'] if a else None,
                     'number': a['number'] if a else '', 'state': card.get('state') or r.get('state') or '',
                     'hash': card.get('hash'), 'editions': eds, 'dir': law_dir(r, used)})
    return laws


def plan(laws: list[dict], today: str):
    events, issues, missing = [], [], []
    for law in laws:
        prev_files = None
        skipped: list[dict] = []
        for ed in law['editions']:
            if not ed['date']:
                issues.append({'nd': law['nd'], 'rdk': ed['rdk'], 'issue': 'edition has no date'})
                continue
            parsed = load_parsed(law['nd'], ed['rdk']) if ed['has_text'] else None
            if parsed is None or parsed.get('error') or not (parsed['units'] or parsed['front']):
                if parsed is not None:
                    issues.append({'nd': law['nd'], 'rdk': ed['rdk'], 'issue': parsed.get('error') or 'no text'})
                if ed['rdk'] > 0 or prev_files is not None:
                    skipped.append(ed)
                    if ed['act']:
                        missing.append({'nd': law['nd'], 'rdk': ed['rdk'], 'date': ed['date'],
                                        'act': ed['act']['label']})
                continue
            files = version_files(law, parsed)
            future = ed['date'] > today
            if prev_files is not None:
                for p in files:
                    if p in prev_files and squash(files[p][0]) == squash(prev_files[p][0]):
                        files[p] = prev_files[p]
            if prev_files is None:
                kind = 'original' if ed['rdk'] == 0 else 'first-text'
                events.append({'date': ed['date'], 'kind': kind, 'law': law, 'ed': ed, 'act': None,
                               'changes': {p: t for p, (t, _) in files.items()}, 'evidence': {}, 'future': future,
                               'skipped': skipped})
            else:
                changed = sorted(p for p in files if p not in prev_files or files[p][0] != prev_files[p][0])
                removed = sorted(p for p in prev_files if p not in files)
                buckets: dict[str, dict] = {}
                for p in sorted(set(changed) | set(removed)):
                    new = (files[p][1] if p in files else set()) - (prev_files[p][1] if p in prev_files else set())
                    art = p.rsplit('/', 1)[1][:-3]
                    who, ev = ed['act'], 'edition' if ed['act'] else 'edition (no act named)'
                    if ed['act'] and act_cite(ed['act']) in new:
                        ev = 'note'
                    elif skipped:
                        by_note = [s for s in skipped if s['act'] and act_cite(s['act']) in new]
                        by_comment = [s for s in skipped if s['act'] and art in comment_articles(s['comment'])]
                        if by_note:
                            who, ev = by_note[-1]['act'], 'note (edition without text)'
                        elif by_comment:
                            who, ev = by_comment[-1]['act'], 'edition list (edition without text)'
                    b = buckets.setdefault(act_key(who), {'act': who, 'changes': {}, 'evidence': {}})
                    b['changes'][p] = files[p][0] if p in files else None
                    b['evidence'][p] = ev
                for k in sorted(buckets):
                    b = buckets[k]
                    events.append({'date': ed['date'], 'kind': 'amendment' if b['act'] else 'editorial',
                                   'law': law, 'ed': ed, 'act': b['act'], 'changes': b['changes'],
                                   'evidence': b['evidence'], 'future': future, 'skipped': skipped})
            prev_files = files
            skipped = []
    return events, issues, missing


def group(events: list[dict]) -> list[dict]:
    """One commit per (date, act) across every act it touched. Within a day, commits follow the edition order
    of each law: a commit's place is the first edition (law order, rdk) it holds."""
    commits: dict[tuple, dict] = {}
    for i, e in enumerate(events):
        if e['kind'] in ('original', 'first-text'):
            k = (e['future'], e['date'], f"law{e['law']['nd']}")
        elif e['kind'] == 'editorial':
            k = (e['future'], e['date'], f"editorial{e['law']['nd']}|{e['ed']['rdk']}")
        else:
            k = (e['future'], e['date'], act_key(e['act']))
        c = commits.setdefault(k, {'date': e['date'], 'kind': e['kind'], 'act': e['act'], 'future': e['future'],
                                   'parts': [], 'order': (e['ed']['rdk'], i)})
        c['parts'].append(e)
    rank = {'original': 0, 'first-text': 0, 'amendment': 1, 'editorial': 1}
    return sorted(commits.values(), key=lambda c: (c['future'], c['date'], rank[c['kind']], c['order']))


def source(nd: str, rdk: int | None = None) -> str:
    """The system's own address for an edition's text (or, without rdk, for the act's card)."""
    api = 'http://ips.pravo.gov.ru/api/ips/legislation/'
    if rdk is None:
        return f'{api}document_card.json?nd={nd}&bpa=c000000000'
    return f'{api}documenttext?nd={nd}&rdk={rdk}&bpa=c000000000'


def law_label(law: dict) -> str:
    t = law['title']
    return t if len(t) <= 60 else t[:57].rstrip() + '...'


def message(c: dict) -> tuple[str, str]:
    parts = sorted(c['parts'], key=lambda p: p['law']['dir'])
    law0 = parts[0]['law']
    n = sum(len(p['changes']) for p in parts)
    if c['kind'] in ('original', 'first-text'):
        law = law0
        ed = parts[0]['ed']
        a = parse_act(law['adoption'])
        name, email = act_ident(a) if a and a['date'] else (law['title'][:60], f"act-{law['nd']}@pravo.gov.invalid")
        if c['kind'] == 'original':
            subject = f'{law_label(law)}: original text'
            body = [f"{law['adoption']}: {law['title']}, as adopted (the system's original edition).",
                    'Each later change is its own commit, credited to the act that made it.']
            ev = 'original edition'
        else:
            subject = f'{law_label(law)}: first text the system holds'
            body = [f"{law['adoption']}: {law['title']}, in edition {ed['rdk']}, the earliest edition the system "
                    f"holds a text for. It includes the changes of the earlier editions, which have no text:"]
            body += [f"- edition {s['rdk']} ({ddmmyyyy(s['date'])}): {s['act']['label'] if s['act'] else 'no act'}"
                     for s in parts[0]['skipped']] or ['- (none listed)']
            ev = 'first edition with a text'
        trailers = [f"Kind: {c['kind']}", f"In-force: {c['date']}"]
        if law['enacted']:
            trailers.append(f"Enacted: {law['enacted']}")
        trailers += [f'Evidence: {ev}', f"Edition: {law['nd']} {ed['rdk']}", f"Source: {source(law['nd'], ed['rdk'])}"]
        return f'{name} <{email}>', '\n'.join([subject, '', *body, '', *trailers]) + '\n'
    if c['kind'] == 'editorial':
        ed = parts[0]['ed']
        subject = f'{law_label(law0)}: publisher\'s edition of {ddmmyyyy(c["date"])}'
        body = [f"The system's edition {ed['rdk']} of {law0['title']} names no amending act"
                + (f" ({ed['reason']})." if ed['reason'] else '.'),
                'The change is credited to the publisher, not to a law.']
        trailers = ['Kind: editorial', f"In-force: {c['date']}", f"Evidence: edition {ed['rdk']} names no act",
                    f"Edition: {law0['nd']} {ed['rdk']}", f"Source: {source(law0['nd'], ed['rdk'])}"]
        return f'{PUBLISHER[0]} <{PUBLISHER[1]}>', '\n'.join([subject, '', *body, '', *trailers]) + '\n'
    act = c['act']
    name, email = act_ident(act)
    subject = f"{name}: {law_label(law0)}" + (f' and {len(parts) - 1} more' if len(parts) > 1 else '')
    body = [f"Changes by {act['label']} to {len(parts)} act(s), {n} unit(s), in force from {ddmmyyyy(c['date'])}.", '']
    body += [f"- {p['law']['title']}" for p in parts[:40]]
    if len(parts) > 40:
        body.append(f'- and {len(parts) - 40} more')
    trailers = ['Kind: amendment', f"In-force: {c['date']}"]
    if act.get('date'):
        trailers.append(f"Enacted: {act['date']}")
    if act.get('nd'):
        trailers.append(f"Source: {source(act['nd'])}")
    evid = sorted({ev for p in parts for ev in p['evidence'].values()})
    for ev in evid:
        trailers.append(f'Evidence: {ev}')
    for p in parts:
        trailers.append(f"Edition: {p['law']['nd']} {p['ed']['rdk']}")
        if p['ed']['act'] and act_key(p['ed']['act']) != act_key(act):
            trailers.append(f"Edition-made-for: {p['ed']['act']['label']}")
    return f'{name} <{email}>', '\n'.join([subject, '', *body, '', *trailers]) + '\n'


# ---------------------------------------------------------------------------------------------------- write

class Writer:
    def __init__(self, repo: Path):
        self.p = subprocess.Popen(['git', '-C', str(repo), 'fast-import', '--quiet', '--force', '--done'],
                                  stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.mark = 0
        self.last = {}

    def w(self, b: bytes) -> None:
        self.p.stdin.write(b)

    def commit(self, ref: str, author: str, when: str, msg: str, changes, parent: int | None = None) -> int:
        self.mark += 1
        m = msg.encode('utf-8')
        self.w(f'commit {ref}\nmark :{self.mark}\nauthor {author} {when}\ncommitter {COMMITTER} {when}\n'.encode('utf-8'))
        self.w(f'data {len(m)}\n'.encode() + m + b'\n')
        par = parent if parent is not None else self.last.get(ref)
        if par:
            self.w(f'from :{par}\n'.encode())
        for path, text in changes:
            if text is None:
                self.w(f'D {path}\n'.encode('utf-8'))
            else:
                t = text if isinstance(text, bytes) else text.encode('utf-8')
                self.w(f'M 100644 inline {path}\ndata {len(t)}\n'.encode('utf-8') + t + b'\n')
        self.w(b'\n')
        self.last[ref] = self.mark
        return self.mark

    def finish(self) -> None:
        self.w(b'done\n')
        self.p.stdin.close()
        err = self.p.stderr.read()
        if self.p.wait():
            sys.exit(err.decode('utf-8', 'replace')[-3000:])


def changes_of(c: dict):
    return [(p, t) for part in c['parts'] for p, t in sorted(part['changes'].items())]


def write(repo: Path, commits: list[dict], docs: dict[str, bytes], today: str) -> None:
    w = Writer(repo)
    seq = 0
    for c in (c for c in commits if not c['future']):
        seq += 1
        author, msg = message(c)
        w.commit('refs/heads/main', author, git_date(c['date'], seq), msg, changes_of(c))
    msg = (f'Documentation: README, REPRODUCE, SOURCES, tools and laws.csv\n\n'
           f'Built from the cache of ips.pravo.gov.ru retrieved on {today}.\n\nIn-force: {today}\n')
    base = w.commit('refs/heads/main', COMMITTER, git_date(today, seq + 1), msg, sorted(docs.items()))
    for c in (c for c in commits if c['future']):
        seq += 1
        author, msg = message(c)
        base = w.commit('refs/heads/future', author, git_date(c['date'], seq), msg, changes_of(c), parent=base)
    w.finish()


def main() -> None:
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', type=Path)
    ap.add_argument('--today', required=True, help='retrieval day of the cache; dates the documentation commit')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--only', help='comma-separated act types or nd numbers (default: everything cached)')
    ap.add_argument('--parse-only', action='store_true')
    args = ap.parse_args()
    only = set(args.only.split(',')) if args.only else None
    laws = load_laws(only)
    keys = [(l['nd'], e['rdk']) for l in laws for e in l['editions'] if e['has_text']]
    todo = []
    for k in keys:
        p = parsed_path(*k)
        try:
            if p.exists() and json.loads(p.read_text('utf-8')).get('parser') == PARSER_VERSION:
                continue
        except json.JSONDecodeError:
            pass
        todo.append(k)
    print(f'{len(laws)} acts, {len(keys)} edition texts; parsing {len(todo)}', flush=True)
    if todo:
        with ProcessPoolExecutor(args.workers) as pool:
            for i, _ in enumerate(pool.map(parse_one, todo, chunksize=4), 1):
                if i % 500 == 0:
                    print(f'  parsed {i}/{len(todo)}', flush=True)
    if args.parse_only:
        return
    events, issues, missing = plan(laws, args.today)
    commits = group(events)
    print(f'{len(commits)} commits from {len(events)} events; {len(issues)} editions unreadable, '
          f'{len(missing)} editions without text', flush=True)

    import docs as docmod
    docs = docmod.render(laws, commits, issues, missing, args.today)

    repo = args.repo
    repo.mkdir(parents=True, exist_ok=True)
    remote = None
    if (repo / '.git').exists():
        root = subprocess.run(['git', '-C', str(repo), 'log', '--format=%B', '--max-parents=0', 'main'],
                              capture_output=True, encoding='utf-8').stdout or ''
        ok = (not root.strip() or 'Kind: original' in root or 'Kind: first-text' in root
              or root.splitlines()[0].endswith('sources, before any law'))
        if not ok:
            sys.exit(f'{repo} holds something other than an earlier build; refusing to replace it')
        r = subprocess.run(['git', '-C', str(repo), 'remote', 'get-url', 'origin'], capture_output=True, text=True)
        remote = r.stdout.strip() or None
        import os
        import shutil
        import stat

        def onerr(func, path, _):
            os.chmod(path, stat.S_IWRITE)
            func(path)
        for child in repo.iterdir():
            shutil.rmtree(child, onerror=onerr) if child.is_dir() else child.unlink()
    elif any(repo.iterdir()):
        sys.exit(f'{repo} is not empty and not a git repository; refusing to build into it')
    subprocess.run(['git', 'init', '-q', '-b', 'main', str(repo)], check=True)
    subprocess.run(['git', '-C', str(repo), 'config', 'core.autocrlf', 'false'], check=True)
    subprocess.run(['git', '-C', str(repo), 'config', 'core.quotepath', 'false'], check=True)
    if remote:
        subprocess.run(['git', '-C', str(repo), 'remote', 'add', 'origin', remote], check=True)
    write(repo, commits, docs, args.today)
    subprocess.run(['git', '-C', str(repo), 'checkout', '-q', '-f', 'main'], check=True)
    head = subprocess.run(['git', '-C', str(repo), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    count = subprocess.run(['git', '-C', str(repo), 'rev-list', '--count', 'HEAD'], capture_output=True,
                           text=True).stdout.strip()
    print(f'built {repo}: {count} commits on main, head {head}', flush=True)


if __name__ == '__main__':
    main()
