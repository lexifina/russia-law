# Tools

The scripts behind this Russia-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/russia-law.git`, a blobless bare clone
of global-law at `sources/global-law.git`, and a `pins.json` that names only russia-law and its commit (language `ru`).
`build_vulns.py`, `flags_chart.py`, `late_ext_select.py`, `late_ext_rebut.py` and `config.json` sit two folders above the
scripts.

| Script | What it does |
| --- | --- |
| `run.sh` | Indexes the history and texts, maps paths to each act's folder (`map_moved.py`), adds this repository's history rows, and runs the detectors (`bash run.sh <shards>`) |
| `map_moved.py` | Rewrites the paths in the history table to each act's folder since the move of 10 November 2026 (`data/paths.json`, `fz/2001-197-fz/` to `fz/2001/197/`), so that an act's history is not split in two at the move; here it rewrote 6,519 paths of 1,791 folders |
| `add_root.py` | Builds the history rows from this repository's own commits (global-law replays it only up to an earlier commit), so the history detectors read every change; changed for this repository (below) |
| `run_triage.sh` | The model review: the 40 strongest flags per category, the 40 strongest lapsed time limits in law texts, and the empty periods (there were none here) |
| `late_ext_select.py` | Chooses the empty periods for global-law's review of that category (there were none here) |
| `late_ext_rebut.py` | Adds the second, arguing-against pass to the empty-period review, as `triage.py` does for the other categories |
| `build_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |
| `flags_chart.py` | Draws the chart at the top of the READMEs, in Russian and English, light and dark |
| `config.json` | The repository, the Russian category names and chart labels, and what is not law: `data/`, `tools/` and the root files (`README.md`, `README.en.md`, `REPRODUCE.md`, `LICENSE`, `laws.csv`, `jurisdiction.json`) |
| `apply_patches.py` | Applies the patches below to a copy of the scripts, each once, in a fixed order, and records them in `.kit_patches.json` (`python -X utf8 apply_patches.py <scripts dir>`); later patches edit text earlier ones inserted, so a patch is never run twice on the same copy. `patch_ru_fz.py` is last in its order |
| `patch_detectors.py` | Fixes blind spots found in runs on several country repositories in the copy of global-law's scripts |
| `patch_ru.py` | The Russian fixes made for kyrgyzstan-law: "не позднее" (not later than) before a date is read as a time limit; the cases of "статья" ("статье", "статью", "статьей", "статей" ...) are read; "статьи 5 Закона ..." (another act named after the number) is not the act's own article; only "исключен", "исключена", "исключено", "исключены" mark a deleted article, not "за исключением" (except). They apply to this repository's Russian too |
| `patch_detectors_vi.py`, `patch_es.py`, `patch_ca.py`, `patch_en.py`, `patch_de.py`, `patch_en_et.py`, `patch_co.py`, `patch_sv.py`, `patch_pt.py`, `patch_r18.py`, `patch_xk.py`, `patch_mo.py`, `patch_lu.py`, `patch_li.py`, `patch_mx.py`, `patch_mn.py`, `patch_mt.py`, `patch_np.py`, `patch_en_nr.py`, `patch_dv.py`, `patch_az.py`, `patch_ar.py`, `patch_en_nz.py`, `patch_nb.py`, `patch_mk.py`, `patch_pa.py`, `patch_py.py`, `patch_pe.py`, `patch_en_ph.py` | The same for the dates, references and currency names of other languages and jurisdictions; they change nothing in Russian text |
| `patch_ru_fz.py` | The fixes made for this repository, in the same form (`python -X utf8 patch_ru_fz.py <scripts dir>`; a fix already in place is skipped, each one found by a marker that survives later edits; see below) |
| `redo.py` | Runs `apply_patches.py`, then again only the scans and detectors the fixes change, the model review of lapsed time limits, references to deleted provisions and empty periods, and the build (`python -X utf8 redo.py <run folder> [--keep-reviews] [--full]`; `--full` runs every step again through `run.sh`, sends every category to the model and keeps every review already made; `EMBED_FONTS` names the script that embeds the chart's fonts); not needed here, as the fixes were in place before the review |
| `measure_missed.py` | Counts the places in the law texts where "до", "по" or "не позднее" comes before a past date, month or year, which of them the time-limit search reads, and the forms of those it misses (the numbers in the READMEs: 2,331 with a bare year, 5 with a month and no day) |
| `ph_check.py` | Hand-check helper: for each reference to a repealed article, the citing article's heading and whether it is an article on entry into force, so that the references in other articles can be read one by one |

The model review needs `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and `LLM_AUTH` set for an OpenAI-compatible Responses API.
It was run with a pattern of the files that are not law (`data/`, `tools/`, `vulnerabilities/`, and the root files named in
`config.json`); every law is under `constitution/`, `fkz/` or `fz/`, so the review of lapsed time limits in law texts drew the
same 40 flags as the review of all of them, and `build_vulns.py` keeps the later review of each flag.

Changes made for this repository:

- `add_root.py` already counted as law the kinds this repository gives the Constitution's 21 versions (`referendum`, `decree`
  and `law`), and a commit with no `Kind:` trailer (one documentation commit of 3 November 2026, which touches only
  `README.md`, `jurisdiction.json` and `laws.csv`): 22 rows. The current texts of the other acts keep their kind, so the
  history detectors do not read them as changes made on the day they were fetched: `baseline` (the 1,655 acts signed
  2010-2017) and `first-text` (the 135 signed 1994-2009), which `add_root.py` now reads as `baseline` too, so that the
  scans treat both alike.
- `patch_ru_fz.py`, references (`ingest/refscan.py`): an inserted article is written "статья 12<sup>1</sup>" (the portal's
  superscript), "статья 12.1" or "статья 9¹"; all were read as article 12 or 9, so a reference to a live article 12.1
  counted as one to a repealed article 12. They are now article 12.1 and 9.1; a heading at the start of a line ("Статья
  12.1. ...") is not a reference; "статьей 19.5 Кодекса ... об административных правонарушениях" is another act's article;
  in a list ("статьями 11, 13 - 16, 19.1, 22") 19.1 is one article; and the act cited is the first act named after the whole
  list, within its clause ("статью 21, пункт 1 статьи 25 и статью 29 Федерального закона от 8 мая 2010 года ..."), so
  such a list is not read as the citing act's own articles. The files of the five acts of 1994-1999 kept one file per
  article (`9-1.md` for "Статья 9¹") now have keys.
- `patch_ru_fz.py`, references to repealed placeholders (`detectors/placeholder_ref.py`): 1,785 of the 1,790 acts are kept
  as one file (`fkz/<year>/<number>/text.md`, `fz/<year>/<number>/text.md`) and were never split into articles, so a
  reference to an article that reads "(Статья утратила силу ...)" in the same act could not be seen: the first run raised
  5 flags. For Russian, such a file is now read article by article ("Статья N." headings at the start of a line); a heading
  out of sequence inside an amending article (a new article set out for another act) continues that article, and past
  repealed chapters the portal leaves out the numbering may jump ahead. An amending article ("Внести в Федеральный закон
  ... следующие изменения: ...", "изложить в следующей редакции", "следующего содержания") cites the amended act's
  articles, and "настоящего Федерального закона" in the wording it sets out is that act too, so its references are not
  read as the amending act's own. An article that declares other acts repealed ("О признании утратившими силу ...") is not
  itself a repeal placeholder. Reading by article raised the flags to 445; the fixes for references brought them to 102,
  all read by hand.
- `patch_ru_fz.py`, duplicate numbering (`detectors/dup_labels.py`): "§ 4<sup>1</sup>" (a section inserted after § 4) was
  read as a second "§ 4"; two flags in Federal Law No. 44-FZ of 5 April 2013 went with it, leaving 4.
- `config.json` counts the top-level files, `data/` and `tools/` as not law; the Constitution's `README.md` (its list of
  articles) is not scanned.
- `pins.json` already named the language (`ru`), and Russian month names in the genitive ("января" ... "декабря") were
  already in the time-limit search.
