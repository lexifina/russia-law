# How this repository was made (Russia)

This file is written by the build on 2026-10-29, the day the source data was retrieved. Everything below is enough to rebuild this repository hash for hash.

## Sources

| Source | Address | Retrieved | Requests | Licence |
| --- | --- | --- | ---: | --- |
| Официальный интернет-портал правовой информации, ИПС «Законодательство России» (actual.pravo.gov.ru API) | <http://actual.pravo.gov.ru/> | 2026-10-29 | 1080 | Official texts are not copyright objects (ГК РФ ст. 1259 п. 6) |

Every response is cached by the sha256 of its URL, and the table above lists every source with its retrieval date. Lexifina keeps its fetch scripts privately; `tools/parse.py` reads only the cache and writes `corpus.json`, so the same cache always gives the same corpus.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `konstitutsiya` | Конституция Российской Федерации | 21 | 1993-12-12 to 2022-10-05 |

The build made 21 commits:

| Commits | Kind |
| ---: | --- |
| 1 | first version of an act |
| 20 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `budushchee`: laws not yet in force on 2026-10-29.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 21 laws in the record.
- 38 tags.

## Dates

Each commit is dated at noon (Europe/Moscow) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Federal Law 5-FZ of 14.06.1994, art. 6: federal laws enter into force throughout the Russian Federation 10 days after official publication unless they set another date; here every edition uses the portal's own edition date. http://pravo.gov.ru/

## Commands, in order

```sh
# fill the cache from the sources listed above (network; Lexifina's fetch scripts are kept privately)
python -X utf8 tools/parse.py                  # cache -> corpus.json (no network)
python -X utf8 tools/build.py <folder> --repo <empty folder> --docs-date 2026-10-29
python -X utf8 tools/check_repo.py <repo> --corpus <folder>/corpus.json --write
python -X utf8 tools/build.py <folder> --repo <another empty folder> --docs-date 2026-10-29 --compare <repo>
```

In the main Lexifina repository these files live as follows:
- `fetch.py`, `parse.py` and `repo/`: in `scripts/russia-law/`.
- `build.py`, `check_repo.py` (`check.py` there) and `on.py`: in `scripts/gitlaw_common/`, with the corpus format in `SCHEMA.md`.

## Exact inputs

- `corpus.json` sha256 `956eae0160fc7c44a86848662b57df64cd4d587bb3a2d2a8b92adf135fceb3ef` (3706586 bytes)
- Script blob hashes (`git hash-object`):

| Script | Blob |
| --- | --- |
| build.py | `2bfc4ac9df193a7be844556d7f69cdb9d93ec3f2` |
| check.py | `cd346c7ff9996d450240e3bab52bcae03b2bc865` |
| on.py | `644a6c0857fbcc72562032b58d57aa113fee0641` |
| fetch.py | `a4b59c6c0a245168963479b5a91e24fb87ce57de` |
| parse.py | `5408882b923f772057135e4befccf82c5e75ba7e` |

- Tools:
  - Python 3.14.0
  - git version 2.52.0.windows.1
  - curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP

## Checks

21 versions of 1 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

Not yet run for this build.

These results are from the check run on the build before this one, from the same corpus.

## Decisions made by hand

- Each version's date is the portal's own edition date (reddate, 'на DD.MM.YYYY'), taken as the in-force date of that edition.
- Every unit that differs from the previous edition is credited to the single act the portal names for that edition (reddocrefid, resolved with card/).
- Editorial notes ('(В редакции ...)', class P paragraphs) are kept out of the provision text; superscripts are written as Unicode superscript digits.
- Section and chapter headings are collected in the unit 'struktura'; Section Two (final and transitional provisions) is one unit 'razdel-2'.
- Same-day editions (2008-12-30, 2022-10-05) are kept as separate same_day versions in the portal's order.

## What AI did and did not do

The fetch, parse and check scripts were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above, through code that anyone can rerun.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none: no model wrote or transformed any text; Claude Code (claude-opus-5-5) wrote fetch.py and parse.py.
