# How this repository was made (Russia)

This file is written by the build on 2026-10-29, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Официальный интернет-портал правовой информации, ИПС «Законодательство России» (actual.pravo.gov.ru API) | <http://actual.pravo.gov.ru/> | 2026-10-29 | Official texts are not copyright objects (ГК РФ ст. 1259 п. 6) |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

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

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `4131e69e0b67c31cb8924282cbe8186fad8f4d91edadce6488ac84927747dc6a` (3706493 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Each version's date is the portal's own edition date (reddate, 'на DD.MM.YYYY'), taken as the in-force date of that edition.
- Every unit that differs from the previous edition is credited to the single act the portal names for that edition (reddocrefid, resolved with card/).
- Editorial notes ('(В редакции ...)', class P paragraphs) are kept out of the provision text; superscripts are written as Unicode superscript digits.
- Section and chapter headings are collected in the unit 'struktura'; Section Two (final and transitional provisions) is one unit 'razdel-2'.
- Same-day editions (2008-12-30, 2022-10-05) are kept as separate same_day versions in the portal's order.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none: no model wrote or transformed any text; Claude Code (claude-opus-5-5) wrote Lexifina's code.
