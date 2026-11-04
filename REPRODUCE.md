# Reproducibility record for the current-text additions

This section records the 130 acts signed 2000–2009 appended to published base `563ea3326fe58be5a224a57f80e49197c0c73b6f`. The immutable pre-fix data head is `3f831c9ced664f230ca8bdc62639d4fbc36118d6`. The documentation correction changes README.md and REPRODUCE.md only. The Constitution's original build record is preserved verbatim below and describes that historical build, including its original “not yet run” checks; it does not describe today's validation status.

## Source, snapshot and licence

| Source | Official address | Source snapshot | Licence |
| --- | --- | --- | --- |
| Official Internet Portal of Legal Information, current federal legislation | <http://actual.pravo.gov.ru/> | Official responses retained on 2026-11-03; unchanged responses revalidated on 2026-11-04 | Official legislative documents are not copyright objects: Civil Code article 1259(6) |

The edition identifiers and commencement evidence for each act are in `data/signed-2000-2009.json` and its law commit trailers. Each `edition_id` identifies the official response at `http://actual.pravo.gov.ru:8000/api/ebpi/redtext?bpa=ebpi&t=<edition_id>&ttl=3`. The 135 current-text federal instruments comprise five earlier additions and these 130 acts; their earlier versions are not recorded. The Constitution retains 21 historical versions. No coverage claim is made for excluded or unresolved acts.

## Inputs, builder identities and toolchain

- Constitution corpus SHA-256: `4131e69e0b67c31cb8924282cbe8186fad8f4d91edadce6488ac84927747dc6a` (3,706,493 bytes).
- Immutable 130-act append input (`draft-part.json`) SHA-256: `804f483cc009d6cd1008a0fc1a90c0c53d41a9ba0958b25f29c12005afd6f642`.
- Expanded official-source validation corpus SHA-256: `fb0d9310935fbeacad7e97e7819170260044f8de96feeb2af9e7f7bd0760aba1`; 131 acts / 151 versions. Its expected new texts were independently parsed from official responses, not copied from the append input.
- Own append builder SHA-256: `572977f019451c32e3b6a9331423ab4de5f33a2d11500fdf0bc954957b9ec7f6`; parser SHA-256: `35c8df7d9fdbd12390a7dd1f223dc6ef513f19b2aec70103539e1417b8c0cebf`. These identify the append handoff artifacts. They are not the tracked `tools/build.py`, which reproduces the historical Constitution build. Exact commit regeneration of these additions requires those immutable append artifacts and official-response inputs; the tracked Constitution builder alone does not regenerate them.
- Tracked Git tool blob IDs: `build.py` `3fa29d18e75f2ec35d37d87b5147fea1f2e4afdf`, `check_repo.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`, `SCHEMA.md` `8089ad749b50a7e0f5676e21763334abb05f4741`.
- Current validation toolchain: Python 3.12.10; git version 2.46.0.windows.1. The original historical toolchain is retained below.
- Original append committer epoch: `1793751507` plus the one-based law index; the original append documentation commit follows those laws. Author dates use Europe/Moscow and the source-based In-force date. This documentation correction's committer epoch is `1793754632`.

## Build and check instructions

Given the immutable offline official-response inputs, use the identified own append builder on `563ea3326fe58be5a224a57f80e49197c0c73b6f` with the identified 130-act input and recorded epoch; it creates one whole-act file per law plus exact official image assets. Two runs must produce the same pre-fix data head `3f831c9ced664f230ca8bdc62639d4fbc36118d6`. Append this documentation correction afterward; do not replace published commits or move tags.

Run the unmodified tracked check on a validation corpus with `python -X utf8 tools/check_repo.py <scratch-repository> --corpus <corpus.json>`. The historical Constitution corpus checks its 21 versions. To cover the additions, supply the expanded source-derived corpus identified above: all 130 new whole-act texts must be read independently from the official responses, including superscripts and in-place image references. Preserve the historical Constitution entries. The day-of-effect and preceding-day comparisons, trailer checks and repository health checks must all pass. The original own source checker requires matching official HTML inputs; an edition skipped because its input is absent is not a checked edition.

## Completed validation and remaining limits

- Unmodified tracked gate on published baseline and current candidate: 1 act / 21 versions, all six error counters zero. Against the expanded source-derived corpus: 131 acts / 151 versions, all six counters zero.
- Ordered official-source text comparison: 130 / 130 complete new texts match. Own character check: 6,957,161 source letters/digits; zero missing, extra or differing editions. The five inherited current-text instruments are outside this new-source character check, and their published Git identities remain unchanged.
- Independent source commencement and current-edition/latest-amendment provenance checks: 130 / 130 pass; no retrieval-day legal dates.
- Source images: 5 = referenced 5 + omitted 0; exact official bytes, SHA-256 filenames, source positions, native image validation and binary attributes verified. No included act has an unpreserved table grid.
- Two complete parse/filter runs and two append builds were identical. These establish determinism, not legal-text provenance. Publication-range privacy audits passed; no stalled full-history audit is claimed passed.

## Decisions and AI-use disclosure for the additions

- One current-text version per act, `first_law` null, labelled oldest version available; the entire official text and publisher annotations are preserved in one file. No earlier wording was reconstructed.
- Legal effect comes from the latest verified amendment's own commencement clause and official publication evidence, or the ten-complete-day rule in unchanged published 5-FZ/1994 article 6. A source signing or clarification link alone is insufficient to prove the latest amendment; unresolved provenance is held.
- There are 178 held whole acts. This includes the three clarification-linked dates rejected in the first review and nine acts needing preservation of 27 table grids. Provisional exclusions and other instrument types still need examination.
- Codex (GPT-6) wrote extraction, append, validation and documentation code under Lexifina's direction. No model wrote, translated, OCR-corrected or replaced legal text; no model runs in the builder. Every included legal word and image comes from the official source. The original historical build's separate AI-use disclosure is preserved below.

---

# Preserved original Constitution build record

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
