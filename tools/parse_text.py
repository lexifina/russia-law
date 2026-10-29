"""Read one edition's HTML (the `doctext` of /api/ips/legislation/documenttext) into units.

    parse(html: str) -> {'front': [..], 'units': [{'id', 'kind', 'heading': [..], 'title', 'lines': [..]}]}

The publisher's HTML is a flat run of <p> elements, each one paragraph, with a class for its role: `H` and `T`
headings (Раздел, Глава, Статья ...), `C` centred lines, `Y` signatures, and so on. History notes are inline spans
(`<span class="mark">(В редакции Федерального закона от 30.12.2012 № 302-ФЗ)</span>`) and are kept as text, exactly
where the publisher prints them. Every <p> is one line, so `git blame` works paragraph by paragraph.

Units: `title` (everything before the first article: the act's name, its list of amending acts, the preamble), one
per article (`Статья 15.`, `Статья 15-1.`), and one per appendix (`Приложение N`) after the articles. Part,
chapter and section headings directly above an article go at the top of that article's file as `##` lines.
The <label>/<input> pair the site uses to fold the list of amending acts is interface, not text, and is dropped.
"""
import copy
import re

from lxml import html as lh

SPACE = re.compile(r'[\s\u00a0\u200b\ufeff]+')
SOFT = re.compile('\u00ad')
SUP = str.maketrans('0123456789', '\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079')
# `Статья 15.`, `Статья 15-1. Name`, `Статья 15.1. Name`, `Статья 67-1` (the Constitution prints no dot).
ARTICLE = re.compile(r'^(?:Статья|С т а т ь я)\s+(\d+(?:[-.]\d+)*(?:\u00b9|\u00b2|\u00b3|[\u2070-\u2079])*)(?:\.\s*|\s+|$)(.*)$')
ANNEX = re.compile(r'^(?:ПРИЛОЖЕНИЕ|Приложение)(?:\s+(?:N|№)?\s*(\d+(?:[-.]\d+)*))?\s*$')
HEADING_CLASSES = {'H', 'T'}
NOTE = re.compile(r'^\(.*\)$')
DIVISION = re.compile(r'^(?:РАЗДЕЛ|Раздел|ПОДРАЗДЕЛ|Подраздел|ГЛАВА|Глава|ЧАСТЬ|Часть|Параграф|ПАРАГРАФ|§)\s*(?:[IVXLC]+|[0-9]+(?:[-.][0-9]+)*|[\u00b9\u00b2\u00b3\u2070-\u2079]+|[А-ЯЁ]+(?:ЫЙ|ОЙ|ИЙ|АЯ|ЬЯ)|[а-яё]+(?:ый|ой|ий|ая|ья))\b[^а-яё]?')


def inline_text(el, keep_lines: bool = False) -> str:
    out: list[str] = []

    def walk(e, sup=False):
        if not isinstance(e.tag, str):
            if e.tail:
                out.append(e.tail.translate(SUP) if sup else e.tail)
            return
        tag = e.tag.lower()
        if tag in ('script', 'style', 'input', 'label'):
            if e.tail:
                out.append(e.tail.translate(SUP) if sup else e.tail)
            return
        # The publisher prints superscript article numbers (`Статья 8<span class="W9">1</span>`) as W9 spans.
        inner = sup or tag == 'sup' or (tag == 'span' and (e.get('class') or '') == 'W9')
        if tag == 'br':
            out.append(' ')
        if e.text:
            out.append(e.text.translate(SUP) if inner else e.text)
        for c in e:
            walk(c, inner)
        if e.tail:
            out.append(e.tail.translate(SUP) if sup else e.tail)

    if el.text:
        out.append(el.text)
    for c in el:
        walk(c)
    if keep_lines:
        return SOFT.sub('', ''.join(out))
    return SPACE.sub(' ', SOFT.sub('', ''.join(out))).strip()


def preformatted(raw: str):
    """Older texts are one <p class="M"> of fixed-width lines. A paragraph starts on an indented line (or after a
    blank line); a line that starts at the left margin continues the paragraph above. Article and division headings,
    and lines indented like centred text, are returned with a heading class."""
    paras: list[tuple[int, list[str]]] = []
    for line in raw.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
        if not line.strip():
            paras.append((-1, []))
            continue
        indent = len(line) - len(line.lstrip(' \u00a0\t'))
        prev = paras[-1] if paras else (-1, [])
        heading = prev[0] >= 0 and bool(ARTICLE.match(prev[1][0].strip()) or DIVISION.match(prev[1][0].strip()))
        if (indent == 0 and prev[0] >= 0) or (heading and indent >= 8):
            # A line at the margin continues the paragraph; an indented line right under a heading (no blank line
            # between) continues the heading's name.
            paras[-1][1].append(line)
        else:
            paras.append((indent, [line]))
    for indent, lines in paras:
        if indent < 0 or not lines:
            continue
        t = SPACE.sub(' ', ' '.join(lines)).strip()
        if not t:
            continue
        if ARTICLE.match(t) and len(t) < 600:
            yield t, 'H'
        elif DIVISION.match(t) or indent >= 8:
            yield t, 'C' if not DIVISION.match(t) else 'H'
        else:
            yield t, ''


def blocks(root):
    """Yield (text, class) for every paragraph, and one line per table row (cells joined by ` | `)."""
    for e in root.iter():
        if not isinstance(e.tag, str):
            continue
        tag = e.tag.lower()
        if tag == 'p':
            # A <p> inside a table cell is read with its row.
            anc = e.getparent()
            inside = False
            while anc is not None:
                if isinstance(anc.tag, str) and anc.tag.lower() == 'table':
                    inside = True
                    break
                anc = anc.getparent()
            if inside:
                continue
            if (e.get('class') or '') == 'M':
                yield from preformatted(inline_text(e, keep_lines=True))
                continue
            first = next((c for c in e if isinstance(c.tag, str)), None)
            if (first is not None and first.tag.lower() == 'span' and (first.get('class') or '') == 'W4'
                    and not (e.text or '').strip()):
                # A run-in article heading: `<p><span class="W4">Статья 1. </span>Text ...</p>`.
                head = inline_text(first)
                if ARTICLE.match(head):
                    rest_el = copy.deepcopy(e)
                    f = next(c for c in rest_el if isinstance(c.tag, str))
                    rest_el.text = (rest_el.text or '') + (f.tail or '')
                    f.tail = None
                    rest_el.remove(f)
                    yield head, 'H'
                    rest = inline_text(rest_el)
                    if rest:
                        yield rest, ''
                    continue
            t = inline_text(e)
            if t:
                yield t, (e.get('class') or '')
        elif tag == 'tr':
            cells = [inline_text(td) for td in e if isinstance(td.tag, str) and td.tag.lower() in ('td', 'th')]
            cells = [c for c in cells if c]
            if cells:
                yield ' | '.join(cells), 'row'


def file_id(num: str) -> str:
    n = num.strip().rstrip('.')
    n = re.sub(r'([\u2070\u00b9\u00b2\u00b3\u2074-\u2079]+)',
               lambda m: '-' + m.group(1).translate(str.maketrans('\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079', '0123456789')), n)
    return re.sub(r'[^0-9A-Za-z.-]', '-', n).strip('-.') or 'x'


def parse(page: str) -> dict:
    doc = lh.fromstring(page.encode('utf-8'), parser=lh.HTMLParser(encoding='utf-8'))
    body = doc.find('.//body')
    root = body if body is not None else doc
    units: list[dict] = []
    front: list[str] = []
    pending: list[str] = []
    cur: dict | None = None

    def new_unit(uid: str, kind: str, title: str, name: str = ''):
        nonlocal cur, pending
        base, n = uid, 1
        while any(u['id'] == uid for u in units):
            n += 1
            uid = f'{base}~{n}'
        cur = {'id': uid, 'kind': kind, 'heading': pending, 'title': title, 'name': name, 'lines': []}
        units.append(cur)
        pending = []

    for text, cls in blocks(root):
        if cls in HEADING_CLASSES:
            m = ARTICLE.match(text)
            if m and len(text) < 600:
                new_unit(file_id(m.group(1)), 'article', f'Статья {m.group(1)}.', m.group(2).strip())
                continue
        if cls in HEADING_CLASSES or cls == 'C':
            m = ANNEX.match(text)
            if m and cur is not None:
                new_unit('annex-' + file_id(m.group(1) or '1'), 'annex', text)
                continue
        if cur is not None and cur['kind'] == 'article' and (
                (cls in ('H', 'T', 'C') and DIVISION.match(text) and len(text) < 400)
                or (pending and (cls in ('H', 'T', 'C', 'I') or (NOTE.match(text) and len(text) < 1000)))):
            # Headings of the next part, chapter or section, the name lines under them and their history notes
            # wait for the next article.
            pending.append(text)
            continue
        if cur is None:
            front.append(text)
        else:
            if pending:
                if DIVISION.match(pending[0]) and cur['kind'] == 'article':
                    # A division with no article of its own (the Constitution's `РАЗДЕЛ ВТОРОЙ`, final and
                    # transitional provisions): its own file, named after the article it follows.
                    held = pending
                    new_unit('after-' + cur['id'].split('~')[0], 'section', held[0])
                    cur['heading'] = []
                    cur['lines'].extend(held[1:])
                else:
                    cur['lines'].extend(pending)
                pending = []
            cur['lines'].append(text)
    if pending:
        (cur['lines'] if cur is not None else front).extend(pending)
    return {'front': front, 'units': units}
