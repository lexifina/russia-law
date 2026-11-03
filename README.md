# Russia: law history in git

The law of Russia as a git history: one file per provision, one commit per edition on the day it took effect, and the decree or law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to an article; picking a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `ru/`. The texts are in Russian, the official language.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `konstitutsiya/` | Конституция Российской Федерации (the Constitution) | 21 | From adoption by referendum (12 December 1993) to the amendments of 4 October 2022, through every decree and law that changed the text (the latest, 8-FKZ, effective 5 October 2022) |

The Constitution and five current-text federal laws are covered.

## Dates

- Each commit is dated at noon, Europe/Moscow, on the day the edition took effect, as the portal dates it.
- Editions from 1996 to 2005 are credited to the Presidential decrees that changed the list of the Federation's subjects (article 65); later ones to federal constitutional laws and the 2008, 2014 and 2020 amendments.
- Several editions share a day when more than one law took effect together (30 December 2008, 5 October 2022); they are commits on the same day in the portal's own order.

## How it is checked

- The newest edition was compared word by word with the portal's current text; it matches.
- Every edition is read back from git on the day it took effect and the day before; both match `corpus.json` (results in `REPRODUCE.md`).
- No merge commits, no dates going backwards, none in the future, and every commit's trailers parse.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the decree or law that made the change, with an e-mail address that cannot exist, so `git blame` and `git log --author` name them. The committer is always Lexifina.

---

# Россия: история права в git

Право России как история git: один файл на положение, один коммит на редакцию в день вступления в силу, а автор коммита - указ или закон, внёсший изменение. `git blame` называет акт, стоящий за каждым абзацем; `git log` показывает все изменения статьи; по дате можно получить текст, действовавший в этот день.

Тексты на русском языке, государственном языке Российской Федерации.

**Что есть сейчас**

| Папка | Акт | Редакций | История |
| --- | --- | ---: | --- |
| `konstitutsiya/` | Конституция Российской Федерации | 21 | С принятия на референдуме (12 декабря 1993 г.) по поправки 4 октября 2022 г., через все указы и законы, изменявшие текст (последний - 8-ФКЗ, действует с 5 октября 2022 г.) |

Включены Конституция и пять федеральных законов в действующих редакциях. Кодексы ещё не добавлены.

**Источник.** Официальный интернет-портал правовой информации (pravo.gov.ru), ИПС «Законодательство России». Официальные тексты законов не являются объектами авторского права (ГК РФ, ст. 1259, п. 6). Самая новая редакция сверена с текущим текстом портала дословно.

## Current-text additions (signed 1991–1999)

These five federal acts each have one current official edition. Earlier editions are not yet recorded. The In-force trailer uses the date stated on that edition.

| Folder | Act | Current edition applies from |
| --- | --- | --- |
| `fz/1994-5-fz/` | О порядке опубликования и вступления в силу федеральных конституционных законов, федеральных законов, актов палат Федерального Собрания | 2019-05-01 |
| `fz/1995-82-fz/` | Об общественных объединениях | 2026-03-03 |
| `fz/1995-181-fz/` | О социальной защите инвалидов в Российской Федерации | 2026-09-01 |
| `fz/1996-7-fz/` | О некоммерческих организациях | 2026-09-01 |
| `fz/1999-92-fz/` | О Российской трехсторонней комиссии по регулированию социально-трудовых отношений | 2017-01-09 |
