# Структура · Structure

```
конституция/                                   Конституция: статья-<n>.md, преамбула.md, раздел-2.md, структура.md
кодексы/<кодекс>/                              каждый кодекс во всех редакциях, по файлу на статью
    гражданский-кодекс/часть-1 … часть-4/
    налоговый-кодекс/часть-1, часть-2/
    кодекс-об-административных-правонарушениях/глава-<n>/   (не более 1 000 файлов в папке)
    заголовок.md      название, даты принятия и одобрения
    оглавление.md     части, разделы, главы, названия статей
    статья-<n>.md     «# Статья <n>. <название>», затем абзацы; статья-19.1.md = статья 19¹
    подписание.md     подпись, место, дата, номер
федеральные-конституционные-законы/<год>/<номер>-ФКЗ/
федеральные-законы/<год>/<номер>-ФЗ/           с 2018 года: статья-<n>.md (или text.md без статей); до 2018: text.md
data/  tools/  laws.csv  vulnerabilities/  visualisations/
```

Folder names are Russian, as searchers write them. A year folder holds at most a few hundred acts.

## Commits

- One commit per edition (редакция) of an act, author date noon Europe/Moscow on the day it took effect.
- The first commit of a code or law is the act as it took effect (`Kind: enactment`), dated by the commencement law's
  article 1 or the act's own clause, checked against the text; a law with no clause by Federal Law 5-FZ of 14.06.1994,
  art. 6 (ten days after official publication). `In-force-basis:` quotes the evidence.
- Each later commit is an IPS edition "на <дата>" (`Kind: amendment`), credited to the act that made it (`Amended-by:`);
  editions the portal lists without text are named in the next commit's `Also-amended-by:` trailers.
- `Edition:` and `Source:` identify the official response, `Source-sha256:` its hash.
- The portal's notes ("(В редакции ...)") are left out of the text; a note that a provision lost force is kept.
- Corrections are new commits (`Kind: correction`); history is never rewritten.
