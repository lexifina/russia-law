# Russian federal law, change by change

The federal law of the Russian Federation as a git repository: 1 Constitution, 29 federal constitutional laws, 32 codes, 2983 federal laws, from the state system of legal
information "Законодательство России" (ips.pravo.gov.ru), part of the Official Internet Portal of Legal Information
(pravo.gov.ru). Each article is its own file, with one paragraph per line. Every change is a commit credited to the
act that made it and dated the day the changed text took effect, at noon Moscow time. The text is the Russian
original.

On `main`, the record runs from 1991-04-25 to 2026-10-25 in 12882 commits, built from 20173 edition texts
(of 24373 editions the system lists). A further 155 commits apply after the build day and sit on the
`future` branch.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did article 65 of the Constitution say on 1 January 2010? | `python tools/in_force_on.py 2010-01-01 constitution 65` |
| The whole act on a date | `python tools/in_force_on.py 2010-01-01 constitution` |
| Which act last changed each paragraph of an article? | `git blame constitution/81.md` |
| Every change to an article, with the act behind it | `git log -p constitution/81.md` |
| The words that changed, not whole paragraphs | `git log -p --word-diff constitution/81.md` |
| Everything one act changed | `git log --author='1-ФКЗ (14.03.2020)' --stat` |
| What takes effect after today | `git log main..future` |
| The list of acts, with their sources | [`laws.csv`](laws.csv) |

Use `tools/in_force_on.py` for "on this date" questions rather than `git log --before`: it picks the text by the
`In-force:` trailer, so it is right in any time zone and for dates before 1970.

Folders: `constitution/`, `fkz/` (federal constitutional laws), `code/` and `fz/` (federal laws). Each act's folder
is named after its adoption year and official number (`code/1994-51-fz` is the Civil Code, part one, № 51-ФЗ of
30.11.1994). Inside it there is one file per article (`8-1.md` for article 8¹, the form the system's own edition
lists use), one per appendix (`annex-1.md`), and `title.md` for the text before the first article (the act's name,
the list of amending acts, the preamble). An article file starts with the part, section and chapter headings above
it (`##`), then its heading line (`# Статья 8-1. ...`), then one line per paragraph. The publisher's history notes,
such as `(В редакции Федерального закона от 30.12.2012 № 302-ФЗ)`, are kept where it prints them.

## The dates, and which one we use

The system keeps the editions (`редакции`) of each act, each "на <date>", the day from which that text applies,
together with the act that made it. **Commits are dated by that day.** The amending act's adoption date is in the
`Enacted:` trailer; in 19 commits the edition applies from a day before the act was adopted (retroactive
effect), and those keep the in-force date.

The first commit of each act is its original edition (`Kind: original`), dated by the system's date for it, which is
the act's date (adoption or signature), not its entry into force. Where the system has no text for the original
edition, the first commit is the earliest edition it does hold (`Kind: first-text`) and lists the editions before it.

**Git cannot store dates before 1970.** None of these acts is that old, but the rule is the same as in the other
corpora: such dates would be clamped to 1970-01-01 with the real date in `In-force:`.

**Editions that apply after the build day** are on the branch `future`, which starts at the tip of `main` and is
never merged into it.

## What "author" means

The author of a commit is the act that made the change, at an address that cannot exist, for example
`302-ФЗ (30.12.2012) <302-fz-20121230@pravo.gov.invalid>`. One commit holds everything one act changed on one day,
across every act it touched.

Each edition names the act it was made for, and that act is credited (`Evidence: edition`, or `note` where the
changed article's own history note newly cites it). The system lists some editions without making a text for them
(4200 here, in [`data/editions-without-text.csv`](data/editions-without-text.csv)). Their changes reach
the record in the next edition that has a text. A changed article is then credited to the edition-without-text act
that its history note newly cites (`Evidence: note (edition without text)`), or whose edition lists that article
(`Evidence: edition list (edition without text)`); otherwise to the act of the edition that has the text.
Editions that name no act (the system's "с учетом уточнений", with corrections) are credited to the publisher
(`Kind: editorial`).

- `edition`: 109024 changed files
- `edition list (edition without text)`: 4646 changed files
- `note`: 28777 changed files
- `note (edition without text)`: 1829 changed files

In all there are 3042 first commits, 9811 amendment commits by
7936 amending acts and 28 editorial commits.

## What it does not show

- Acts whose only purpose is to amend or repeal others (`О внесении изменений ...`): they are the authors of
  commits here, not files. Their transitional provisions are in each act at the `Source:` link.
- Laws of the RSFSR and Russian Federation from before 1993 that are not codes, presidential decrees, government
  resolutions and other acts below the level of federal law.
- Editions the system lists without a text, and texts we could not read (0, in
  [`data/unreadable.csv`](data/unreadable.csv)).
- Renumbering: an article that moves appears as one file removed and another added.

This repository is a research aid, not an official publication. The official publication of federal law is on
publication.pravo.gov.ru and in Собрание законодательства Российской Федерации and Российская газета.

## How it is checked

- An independent check compares the letters and digits of every edition's raw HTML with the files git holds at
  that edition's commit.
- `tools/in_force_on.py` is compared with the system's own text for several articles and dates.
- `main` has no merge commits, its commit dates never go backwards, and none is after the build day.
- Two builds from the same cache give the same commit hashes.

See [`REPRODUCE.md`](REPRODUCE.md) and [`SOURCES.md`](SOURCES.md).

## How it is built

`tools/build/fetch.py` finds every act of the four types through the system's search, reads each act's card (its
editions, with dates and amending acts) and downloads the text of every edition. `parse_text.py` splits each text
into articles and paragraphs. `build.py` compares each act's editions in order and credits each change as above, and
writes the whole history with one `git fast-import`. No AI model reads or writes any text, in the build or in the
checks. If you use raw git for dates, write the time in full: `git rev-list -1 --before="2010-01-01T23:59:59+03:00" main`.

## Licence

Under article 1259(6)(1) of the Civil Code of the Russian Federation, official documents of state bodies, including
laws and other normative acts, and their official translations, are not objects of copyright. The texts here were
split into files and arranged as commits; their wording was not changed. Lexifina's own contributions (the tools,
the arrangement and the commit messages) are CC0. See [`LICENSE`](LICENSE).
