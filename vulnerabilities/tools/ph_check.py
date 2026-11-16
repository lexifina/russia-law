"""Hand-check helper: for each reference to a repealed article (findings/run/placeholder_ref.jsonl), the citing article's
heading, and whether that article is one on entry into force (it says when the act or parts of it take effect), so that
the references in force texts can be read one by one.
    python -X utf8 ph_check.py <scripts dir>      (reads sources/corpus/<repo>.git at the pinned commit)"""
import collections, json, re, subprocess, sys
from pathlib import Path

S = Path(sys.argv[1])
sys.path.insert(0, str(S / "detectors")); sys.path.insert(0, str(S / "ingest"))
import refscan  # noqa: E402
refscan._LANG["v"] = "ru"
import placeholder_ref as pr  # noqa: E402

pin = json.load(open(S / "pins.json", encoding="utf-8"))["corpora"][0]
M = S / "sources" / "corpus" / (pin["repo"] + ".git")
J = [json.loads(l) for l in open(S / "findings" / "run" / "placeholder_ref.jsonl", encoding="utf-8")]
cache = {}


def chunks(path):
    if path not in cache:
        t = subprocess.run(["git", "-C", str(M), "show", f"{pin['sha']}:{path}"], capture_output=True).stdout.decode("utf-8")
        cache[path] = pr.ru_split({path: t}) if path.endswith("text.md") else {path: t}
    return cache[path]


COMM = re.compile(r"(?i)вступа\w*\s+в\s+силу|вводится\s+в\s+действие|вводятся\s+в\s+действие|применя\w*\s+с\s+\d|не\s+применя")
groups = collections.OrderedDict()
for r in J:
    groups.setdefault((r["path"], r["from"]), []).append(r)
kinds = collections.Counter()
for (p, f), rs in groups.items():
    ch = chunks(p).get(f"{p}#{f}" if f else p, "")
    head = ch.strip().splitlines()[0][:90] if ch.strip() else "?"
    comm = bool(COMM.search(ch))
    kinds["entry into force" if comm else "other"] += len(rs)
    print(len(rs), p, f, "->", sorted({r["ref"] for r in rs}), "| entry into force" if comm else "| --", "|", head)
print(dict(kinds))
