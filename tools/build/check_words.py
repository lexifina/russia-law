"""Independent check: every edition's raw HTML against what git holds, as letters and digits.

The source side is the cached `doctext` (.cache/text/<nd>/<rdk>.html.gz) read with lxml's itertext() over <body>,
dropping only the site's fold control (<label>, <input>), scripts and styles; nothing from parse_text.py or build.py.
The git side is every file in the act's folder at the last commit whose `Edition:` trailer names that edition, read
with git cat-file. Both sides are reduced to their letters and digits (casefolded, superscripts as digits) and
compared as counts, so file order and whitespace do not matter.

    python scripts/russia-law/check_words.py ~/Documents/russia-law [--sample N] [--seed 1]

Exit status 1 if any edition differs.
"""
import argparse
import csv
import gzip
import random
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import lxml.html as lh

CACHE = Path(__file__).parent / '.cache' / 'text'
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')


def letters(s: str) -> Counter:
    return Counter(c for c in s.translate(SUP).casefold() if c.isalnum())


def source_letters(nd: str, rdk: str) -> Counter:
    raw = gzip.decompress((CACHE / nd / f'{rdk}.html.gz').read_bytes())
    doc = lh.fromstring(raw, parser=lh.HTMLParser(encoding='utf-8'))
    body = doc.find('.//body')
    root = body if body is not None else doc
    for el in root.xpath('.//script|.//style|.//label|.//input'):
        el.drop_tree()
    return letters(' '.join(root.itertext()).replace('­', ''))


def main() -> None:
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', type=Path)
    ap.add_argument('--sample', type=int, default=0, help='check N random editions (default: all)')
    ap.add_argument('--seed', type=int, default=1)
    args = ap.parse_args()
    repo = args.repo

    def git(*a: str) -> str:
        return subprocess.run(['git', '-c', 'core.quotepath=false', '-C', str(repo), *a], capture_output=True,
                              text=True, encoding='utf-8', check=True).stdout

    folders = {row['nd']: row['path'].rstrip('/') for row in csv.DictReader(open(repo / 'laws.csv', encoding='utf-8'))}
    last: dict[tuple[str, str], str] = {}
    log = git('log', '--reverse', 'main', '--format=%H%x1f%(trailers:key=Edition,valueonly,separator=%x1e)')
    for line in log.splitlines():
        h, _, eds = line.partition('\x1f')
        for e in eds.split('\x1e'):
            m = re.match(r'\s*(\d+) (\d+)\s*$', e)
            if m:
                last[(m.group(1), m.group(2))] = h  # --reverse: the last commit naming the edition wins
    keys = sorted(last)
    if args.sample:
        random.Random(args.seed).shuffle(keys)
        keys = sorted(keys[:args.sample])
    print(f'{len(last)} editions named by commits on main; checking {len(keys)}', flush=True)

    cat = subprocess.Popen(['git', '-C', str(repo), 'cat-file', '--batch'], stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)

    def blob(spec: str) -> bytes:
        cat.stdin.write(spec.encode('utf-8') + b'\n')
        cat.stdin.flush()
        header = cat.stdout.readline().split()
        if header[1] == b'missing':
            return b''
        data = cat.stdout.read(int(header[2]))
        cat.stdout.read(1)
        return data

    results = []
    for nd, rdk in keys:
        commit = last[(nd, rdk)]
        folder = folders.get(nd)
        if not folder or not (CACHE / nd / f'{rdk}.html.gz').exists():
            continue
        ours = Counter()
        for n in filter(None, git('ls-tree', '-r', '--name-only', commit, folder + '/').split('\n')):
            ours += letters(blob(f'{commit}:{n}').decode('utf-8'))
        src = source_letters(nd, rdk)
        missing, extra = src - ours, ours - src
        results.append((sum(missing.values()) + sum(extra.values()), nd, rdk, sum(src.values()),
                        sum(missing.values()), sum(extra.values()), missing.most_common(5), extra.most_common(5)))
    cat.stdin.close()
    results.sort(reverse=True)
    bad = [r for r in results if r[0]]
    total = sum(r[3] for r in results)
    print(f'checked {len(results)} editions, {total} source letters and digits: '
          f'{sum(r[4] for r in results)} missing, {sum(r[5] for r in results)} extra; {len(bad)} editions differ')
    for r in bad[:25]:
        print(f'  {r[1]} edition {r[2]}: missing {r[4]}/{r[3]}, extra {r[5]}; missing e.g. {r[6]}; extra e.g. {r[7]}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
