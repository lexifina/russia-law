# Russia: law history in git

The law of Russia as a git history: one file per provision, one commit per edition on the day it took effect, and the decree or law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to an article; picking a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `ru/`. The texts are in Russian, the official language.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `konstitutsiya/` | Конституция Российской Федерации (the Constitution) | 21 | From adoption by referendum (12 December 1993) to the amendments of 4 October 2022, through every decree and law that changed the text (the latest, 8-FKZ, effective 5 October 2022) |

The Constitution and 135 current-text federal instruments are covered.

## Dates

- Each commit is dated at noon, Europe/Moscow, on the day the edition took effect, as the portal dates it.
- Editions from 1996 to 2005 are credited to the Presidential decrees that changed the list of the Federation's subjects (article 65); later ones to federal constitutional laws and the 2008, 2014 and 2020 amendments.
- Several editions share a day when more than one law took effect together (30 December 2008, 5 October 2022); they are commits on the same day in the portal's own order.

## How it is checked

- The newest edition was compared word by word with the portal's current text; it matches.
- Every edition is read back from git on the day it took effect and the day before; both match `corpus.json` (results in `REPRODUCE.md`).
- Committer dates preserve append order; author dates and In-force trailers record legal effect.
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


## Federal laws signed 2000–2009

130 additional current-text acts, each as one complete file including the source annotations. Earlier versions are not included for these acts.

| Folder | Act | Versions | Text |
| --- | --- | ---: | --- |
| `fz/2000-1-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Ванкорском газонефтяном месторождении) | 1 | Current text from 2000-01-06; oldest version available |
| `fz/2000-29-fz/` | О качестве и безопасности пищевых продуктов | 1 | Current text from 2025-09-01; oldest version available |
| `fz/2000-37-fz/` | О народных заседателях федеральных судов общей юрисдикции в Российской Федерации | 1 | Current text from 2002-11-20; oldest version available |
| `fz/2000-60-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Северо-Астраханском перспективном участке) | 1 | Current text from 2000-05-06; oldest version available |
| `fz/2000-72-fz/` | О Договоре о всеобъемлющем запрещении ядерных испытаний | 1 | Current text from 2023-11-02; oldest version available |
| `fz/2000-73-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Штокмановском газоконденсатном месторождении) | 1 | Current text from 2000-05-30; oldest version available |
| `fz/2000-79-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Тасеевском месторождении золота) | 1 | Current text from 2000-05-30; oldest version available |
| `fz/2000-82-fz/` | О минимальном размере оплаты труда | 1 | Current text from 2025-12-09; oldest version available |
| `fz/2000-98-fz/` | О коэффициентах деноминации для месяцев, входящих в период с 1 марта по 31 декабря 1991 года | 1 | Current text from 2000-07-18; oldest version available |
| `fz/2000-101-fz/` | О создании суда Таймырского (Долгано-Ненецкого) автономного округа | 1 | Current text from 2001-01-01; oldest version available |
| `fz/2000-104-fz/` | Об общих принципах организации общин коренных малочисленных народов Севера, Сибири и Дальнего Востока Российской Федерации | 1 | Current text from 2022-10-31; oldest version available |
| `fz/2000-129-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Харампурском нефтегазоконденсатном месторождении) | 1 | Current text from 2000-10-10; oldest version available |
| `fz/2000-130-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Комсомольском нефтегазоконденсатном месторождении) | 1 | Current text from 2000-10-10; oldest version available |
| `fz/2000-131-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Тянском нефтяном месторождении) | 1 | Current text from 2000-10-10; oldest version available |
| `fz/2000-1-fkz/` | О Государственном флаге Российской Федерации | 1 | Current text from 2026-06-26; oldest version available |
| `fz/2000-2-fkz/` | О Государственном гербе Российской Федерации | 1 | Current text from 2025-12-29; oldest version available |
| `fz/2000-3-fkz/` | О Государственном гимне Российской Федерации | 1 | Current text from 2025-07-31; oldest version available |
| `fz/2000-149-fz/` | О присвоении столице Республики Ингушетия наименования - Магас | 1 | Current text from 2000-12-29; oldest version available |
| `fz/2001-12-fz/` | О гарантиях Президенту Российской Федерации, прекратившему исполнение своих полномочий, и членам его семьи | 1 | Current text from 2021-01-02; oldest version available |
| `fz/2001-13-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Ковыктинском газоконденсатном месторождении) | 1 | Current text from 2001-02-15; oldest version available |
| `fz/2001-49-fz/` | О территориях традиционного природопользования коренных малочисленных народов Севера, Сибири и Дальнего Востока Российской Федерации | 1 | Current text from 2020-12-08; oldest version available |
| `fz/2001-61-fz/` | Об увеличении штатной численности судей и работников аппаратов арбитражных судов в Российской Федерации | 1 | Current text from 2001-05-31; oldest version available |
| `fz/2001-3-fkz/` | О чрезвычайном положении | 1 | Current text from 2023-11-02; oldest version available |
| `fz/2001-73-fz/` | О государственной судебно-экспертной деятельности в Российской Федерации | 1 | Current text from 2024-08-02; oldest version available |
| `fz/2001-77-fz/` | О предупреждении распространения туберкулеза в Российской Федерации | 1 | Current text from 2023-01-01; oldest version available |
| `fz/2001-92-fz/` | О специальных экологических программах реабилитации радиационно загрязненных участков территории | 1 | Current text from 2012-06-25; oldest version available |
| `fz/2001-95-fz/` | О политических партиях | 1 | Current text from 2026-03-03; oldest version available |
| `fz/2001-106-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Нежданинском золоторудном месторождении) | 1 | Current text from 2001-08-09; oldest version available |
| `fz/2001-129-fz/` | О государственной регистрации юридических лиц и индивидуальных предпринимателей | 1 | Current text from 2026-08-04; oldest version available |
| `fz/2001-137-fz/` | О введении в действие Земельного кодекса Российской Федерации | 1 | Current text from 2026-08-04; oldest version available |
| `fz/2001-163-fz/` | Об индексации ставок земельного налога | 1 | Current text from 2001-12-20; oldest version available |
| `fz/2001-6-fkz/` | О порядке принятия в Российскую Федерацию и образования в ее составе нового субъекта Российской Федерации | 1 | Current text from 2005-11-03; oldest version available |
| `fz/2001-173-fz/` | О трудовых пенсиях в Российской Федерации | 1 | Current text from 2020-12-08; oldest version available |
| `fz/2001-174-fz/` | Уголовно-процессуальный кодекс Российской Федерации | 1 | Current text from 2026-08-06; oldest version available |
| `fz/2001-184-fz/` | О страховых тарифах на обязательное социальное страхование от несчастных случаев на производстве и профессиональных заболеваний на 2002 год | 1 | Current text from 2001-12-30; oldest version available |
| `fz/2001-196-fz/` | О введении в действие Кодекса Российской Федерации об административных правонарушениях | 1 | Current text from 2025-07-01; oldest version available |
| `fz/2001-197-fz/` | Трудовой кодекс Российской Федерации | 1 | Current text from 2026-09-01; oldest version available |
| `fz/2002-6-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Майском месторождении золота) | 1 | Current text from 2002-01-12; oldest version available |
| `fz/2002-1-fkz/` | О военном положении | 1 | Current text from 2024-12-13; oldest version available |
| `fz/2002-21-fz/` | О дополнительном ежемесячном материальном обеспечении граждан Российской Федерации за выдающиеся достижения и особые заслуги перед Российской Федерацией | 1 | Current text from 2026-01-01; oldest version available |
| `fz/2002-30-fz/` | Об органах судейского сообщества в Российской Федерации | 1 | Current text from 2026-05-02; oldest version available |
| `fz/2002-31-fz/` | О приведении законодательных актов в соответствие с Федеральным законом "О государственной регистрации юридических лиц" | 1 | Current text from 2026-03-03; oldest version available |
| `fz/2002-37-fz/` | О передаче Федеративной Республике Германия витражей из церкви Святой Марии (Мариенкирхе) в городе Франкфурте-на-Одере, перемещенных в Союз ССР в результате Второй мировой войны и хранящихся в Государственном Эрмитаже | 1 | Current text from 2002-05-21; oldest version available |
| `fz/2002-54-fz/` | О временном запрете на клонирование человека | 1 | Current text from 2010-04-13; oldest version available |
| `fz/2002-79-fz/` | Об Ирбитском районном суде Свердловской области | 1 | Current text from 2002-07-13; oldest version available |
| `fz/2002-83-fz/` | О финансовом оздоровлении сельскохозяйственных товаропроизводителей | 1 | Current text from 2014-07-22; oldest version available |
| `fz/2002-96-fz/` | О введении в действие Арбитражного процессуального кодекса Российской Федерации | 1 | Current text from 2022-01-01; oldest version available |
| `fz/2002-102-fz/` | О третейских судах в Российской Федерации | 1 | Current text from 2020-12-08; oldest version available |
| `fz/2002-113-fz/` | Об альтернативной гражданской службе | 1 | Current text from 2026-08-04; oldest version available |
| `fz/2002-114-fz/` | О противодействии экстремистской деятельности | 1 | Current text from 2025-11-07; oldest version available |
| `fz/2002-118-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Яламо-Самурском и Центральном перспективных участках) | 1 | Current text from 2002-07-30; oldest version available |
| `fz/2002-121-fz/` | О создании Грозненского гарнизонного военного суда и упразднении Норильского гарнизонного военного суда | 1 | Current text from 2021-01-01; oldest version available |
| `fz/2002-137-fz/` | О введении в действие Гражданского процессуального кодекса Российской Федерации | 1 | Current text from 2022-01-01; oldest version available |
| `fz/2002-138-fz/` | Гражданский процессуальный кодекс Российской Федерации | 1 | Current text from 2026-09-01; oldest version available |
| `fz/2002-161-fz/` | О государственных и муниципальных унитарных предприятиях | 1 | Current text from 2026-01-01; oldest version available |
| `fz/2002-156-fz/` | Об объединениях работодателей | 1 | Current text from 2015-12-09; oldest version available |
| `fz/2002-183-fz/` | О страховых тарифах на обязательное социальное страхование от несчастных случаев на производстве и профессиональных заболеваний на 2003 год | 1 | Current text from 2003-01-01; oldest version available |
| `fz/2002-184-fz/` | О техническом регулировании | 1 | Current text from 2026-09-01; oldest version available |
| `fz/2003-21-fz/` | О временных мерах по обеспечению представительства коренных малочисленных народов Российской Федерации в законодательных (представительных) органах государственной власти субъектов Российской Федерации | 1 | Current text from 2003-02-11; oldest version available |
| `fz/2003-29-fz/` | Об особенностях управления и распоряжения имуществом железнодорожного транспорта | 1 | Current text from 2026-06-05; oldest version available |
| `fz/2003-34-fz/` | О запрете производства и оборота этилированного автомобильного бензина в Российской Федерации | 1 | Current text from 2003-07-01; oldest version available |
| `fz/2003-58-fz/` | О системе государственной службы Российской Федерации | 1 | Current text from 2025-09-29; oldest version available |
| `fz/2003-63-fz/` | Об участках недр, право пользования которыми может быть предоставлено на условиях раздела продукции (Наталкинском золоторудном месторождении) | 1 | Current text from 2003-06-03; oldest version available |
| `fz/2003-74-fz/` | О крестьянском (фермерском) хозяйстве | 1 | Current text from 2025-08-11; oldest version available |
| `fz/2003-152-fz/` | Об ипотечных ценных бумагах | 1 | Current text from 2026-08-04; oldest version available |
| `fz/2003-165-fz/` | О специальных защитных, антидемпинговых и компенсационных мерах при импорте товаров | 1 | Current text from 2020-12-08; oldest version available |
| `fz/2003-167-fz/` | О страховых тарифах на обязательное социальное страхование от несчастных случаев на производстве и профессиональных заболеваний на 2004 год | 1 | Current text from 2004-01-01; oldest version available |
| `fz/2003-174-fz/` | О государственной регистрации выпусков акций, размещенных до вступления в силу Федерального закона "О рынке ценных бумаг" без государственной регистрации | 1 | Current text from 2003-12-17; oldest version available |
| `fz/2004-1-fkz/` | Об образовании в составе Российской Федерации нового субъекта Российской Федерации в результате объединения Пермской области и Коми-Пермяцкого автономного округа | 1 | Current text from 2006-04-14; oldest version available |
| `fz/2004-54-fz/` | О собраниях, митингах, демонстрациях, шествиях и пикетированиях | 1 | Current text from 2022-12-05; oldest version available |
| `fz/2004-59-fz/` | О создании и упразднении некоторых гарнизонных военных судов | 1 | Current text from 2021-01-01; oldest version available |
| `fz/2004-75-fz/` | О Ханты-Мансийском районном суде Ханты-Мансийского автономного округа - Югры | 1 | Current text from 2004-07-29; oldest version available |
| `fz/2004-82-fz/` | О потребительской корзине в целом по Российской Федерации в 2004 году | 1 | Current text from 2004-07-31; oldest version available |
| `fz/2004-92-fz/` | О продолжении эксперимента по налогообложению недвижимости в городах Великом Новгороде и Твери и внесении изменений в Федеральный закон "О проведении эксперимента по налогообложению недвижимости в городах Великом Новгороде и Твери" | 1 | Current text from 2004-07-31; oldest version available |
| `fz/2004-96-fz/` | О выплатах Банка России по вкладам физических лиц в признанных банкротами банках, не участвующих в системе обязательного страхования вкладов в банках Российской Федерации | 1 | Current text from 2019-01-01; oldest version available |
| `fz/2004-117-fz/` | О накопительно-ипотечной системе жилищного обеспечения военнослужащих | 1 | Current text from 2026-06-05; oldest version available |
| `fz/2004-119-fz/` | О государственной защите потерпевших, свидетелей и иных участников уголовного судопроизводства | 1 | Current text from 2026-01-01; oldest version available |
| `fz/2004-125-fz/` | Об архивном деле в Российской Федерации | 1 | Current text from 2024-12-24; oldest version available |
| `fz/2004-166-fz/` | О рыболовстве и сохранении водных биологических ресурсов | 1 | Current text from 2026-09-01; oldest version available |
| `fz/2004-172-fz/` | О переводе земель или земельных участков из одной категории в другую | 1 | Current text from 2026-03-01; oldest version available |
| `fz/2004-189-fz/` | О введении в действие Жилищного кодекса Российской Федерации | 1 | Current text from 2026-08-04; oldest version available |
| `fz/2004-191-fz/` | О введении в действие Градостроительного кодекса Российской Федерации | 1 | Current text from 2026-08-04; oldest version available |
| `fz/2004-209-fz/` | О снятии оговорки Российской Федерации к статьям 16 и 18 Договора о Таможенном союзе и Едином экономическом пространстве | 1 | Current text from 2005-01-01; oldest version available |
| `fz/2005-32-fz/` | Об Общественной палате Российской Федерации | 1 | Current text from 2026-06-26; oldest version available |
| `fz/2005-53-fz/` | О государственном языке Российской Федерации | 1 | Current text from 2025-01-01; oldest version available |
| `fz/2005-108-fz/` | О Всероссийской сельскохозяйственной переписи | 1 | Current text from 2026-09-01; oldest version available |
| `fz/2005-116-fz/` | Об особых экономических зонах в Российской Федерации | 1 | Current text from 2026-03-01; oldest version available |
| `fz/2005-6-fkz/` | Об образовании в составе Российской Федерации нового субъекта Российской Федерации в результате объединения Красноярского края, Таймырского (Долгано-Ненецкого) автономного округа и Эвенкийского автономного округа | 1 | Current text from 2005-10-19; oldest version available |
| `fz/2005-180-fz/` | Об отдельных вопросах исчисления и выплаты пособий по временной нетрудоспособности, по беременности и родам и размерах страхового обеспечения по обязательному социальному страхованию от несчастных случаев на производстве и профессиональных заболеваний в 2006 году | 1 | Current text from 2006-01-01; oldest version available |
| `fz/2005-196-fz/` | О парламентском расследовании Федерального Собрания Российской Федерации | 1 | Current text from 2023-04-03; oldest version available |
| `fz/2006-35-fz/` | О противодействии терроризму | 1 | Current text from 2026-05-25; oldest version available |
| `fz/2006-59-fz/` | О порядке рассмотрения обращений граждан Российской Федерации | 1 | Current text from 2025-03-30; oldest version available |
| `fz/2006-2-fkz/` | Об образовании в составе Российской Федерации нового субъекта Российской Федерации в результате объединения Камчатской области и Корякского автономного округа | 1 | Current text from 2006-07-15; oldest version available |
| `fz/2006-117-fz/` | Об экспорте газа | 1 | Current text from 2023-11-13; oldest version available |
| `fz/2006-174-fz/` | Об автономных учреждениях | 1 | Current text from 2026-08-06; oldest version available |
| `fz/2006-201-fz/` | О введении в действие Лесного кодекса Российской Федерации | 1 | Current text from 2025-09-01; oldest version available |
| `fz/2006-231-fz/` | О введении в действие части четвертой Гражданского кодекса Российской Федерации | 1 | Current text from 2026-03-23; oldest version available |
| `fz/2006-235-fz/` | О страховых тарифах на обязательное социальное страхование от несчастных случаев на производстве и профессиональных заболеваний на 2007 год | 1 | Current text from 2007-01-01; oldest version available |
| `fz/2006-6-fkz/` | Об образовании в составе Российской Федерации нового субъекта Российской Федерации в результате объединения Иркутской области и Усть-Ордынского Бурятского автономного округа | 1 | Current text from 2007-06-06; oldest version available |
| `fz/2006-269-fz/` | Об упрощенном порядке декларирования доходов физическими лицами | 1 | Current text from 2007-03-01; oldest version available |
| `fz/2006-284-fz/` | О социальных гарантиях и компенсациях военнослужащим, проходящим военную службу в воинских формированиях Российской Федерации, дислоцированных на территориях Республики Белоруссия, Республики Казахстан и Киргизской Республики, а также лицам, работающим в этих формированиях | 1 | Current text from 2026-01-01; oldest version available |
| `fz/2007-25-fz/` | О муниципальной службе в Российской Федерации | 1 | Current text from 2026-01-01; oldest version available |
| `fz/2007-139-fz/` | О Российской корпорации нанотехнологий | 1 | Current text from 2010-06-02; oldest version available |
| `fz/2007-144-fz/` | Об упразднении и создании некоторых районных судов Саратовской области | 1 | Current text from 2022-12-30; oldest version available |
| `fz/2007-196-fz/` | О ломбардах | 1 | Current text from 2025-06-01; oldest version available |
| `fz/2007-5-fkz/` | Об образовании в составе Российской Федерации нового субъекта Российской Федерации в результате объединения Читинской области и Агинского Бурятского автономного округа | 1 | Current text from 2007-07-26; oldest version available |
| `fz/2007-186-fz/` | О страховых тарифах на обязательное социальное страхование от несчастных случаев на производстве и профессиональных заболеваний на 2008 год и на плановый период 2009 и 2010 годов | 1 | Current text from 2008-01-01; oldest version available |
| `fz/2007-270-fz/` | О Государственной корпорации по содействию разработке, производству и экспорту высокотехнологичной промышленной продукции "Ростех" | 1 | Current text from 2026-03-03; oldest version available |
| `fz/2007-310-fz/` | Об организации и о проведении XXII Олимпийских зимних игр и XI Паралимпийских зимних игр 2014 года в городе Сочи, развитии города Сочи как горноклиматического курорта и внесении изменений в отдельные законодательные акты Российской Федерации | 1 | Current text from 2014-06-30; oldest version available |
| `fz/2008-48-fz/` | Об опеке и попечительстве | 1 | Current text from 2025-09-29; oldest version available |
| `fz/2008-76-fz/` | Об общественном контроле за обеспечением прав человека в местах принудительного содержания и о содействии лицам, находящимся в местах принудительного содержания | 1 | Current text from 2026-01-01; oldest version available |
| `fz/2008-89-fz/` | О создании Новочеркасского гарнизонного военного суда и упразднении 6-го гарнизонного военного суда | 1 | Current text from 2021-01-01; oldest version available |
| `fz/2008-130-fz/` | О принятии Поправки к Конвенции о физической защите ядерного материала | 1 | Current text from 2008-07-30; oldest version available |
| `fz/2008-207-fz/` | О мерах по организации местного самоуправления в Республике Ингушетия и Чеченской Республике | 1 | Current text from 2008-11-26; oldest version available |
| `fz/2008-217-fz/` | О страховых тарифах на обязательное социальное страхование от несчастных случаев на производстве и профессиональных заболеваний на 2009 год и на плановый период 2010 и 2011 годов | 1 | Current text from 2009-01-01; oldest version available |
| `fz/2008-262-fz/` | Об обеспечении доступа к информации о деятельности судов в Российской Федерации | 1 | Current text from 2023-01-01; oldest version available |
| `fz/2008-273-fz/` | О противодействии коррупции | 1 | Current text from 2026-09-01; oldest version available |
| `fz/2008-307-fz/` | Об аудиторской деятельности | 1 | Current text from 2026-08-15; oldest version available |
| `fz/2009-8-fz/` | Об обеспечении доступа к информации о деятельности государственных органов и органов местного самоуправления | 1 | Current text from 2026-03-01; oldest version available |
| `fz/2009-17-fz/` | О порядке применения статей 132 и 139 Бюджетного кодекса Российской Федерации | 1 | Current text from 2009-02-11; oldest version available |
| `fz/2009-22-fz/` | О навигационной деятельности | 1 | Current text from 2024-07-22; oldest version available |
| `fz/2009-103-fz/` | О деятельности по приему платежей физических лиц, осуществляемой платежными агентами | 1 | Current text from 2026-04-09; oldest version available |
| `fz/2009-109-fz/` | О создании и упразднении некоторых районных (городских) судов Калужской области и образовании постоянных судебных присутствий в составе некоторых районных судов Калужской области | 1 | Current text from 2018-02-05; oldest version available |
| `fz/2009-143-fz/` | Об особенностях предоставления финансовой поддержки субъектам Российской Федерации и муниципальным образованиям за счет средств государственной корпорации - Фонда содействия реформированию жилищно-коммунального хозяйства в 2009 году | 1 | Current text from 2009-07-02; oldest version available |
| `fz/2009-172-fz/` | Об антикоррупционной экспертизе нормативных правовых актов и проектов нормативных правовых актов | 1 | Current text from 2024-09-30; oldest version available |
| `fz/2009-190-fz/` | О кредитной кооперации | 1 | Current text from 2026-04-09; oldest version available |
| `fz/2009-200-fz/` | О выкупе чеков "Урожай-90", выплатах сдатчикам сельскохозяйственной продукции урожая 1991 года и внесении изменений в Федеральный закон "О государственных долговых товарных обязательствах" | 1 | Current text from 2009-07-24; oldest version available |
| `fz/2009-297-fz/` | О страховых тарифах на обязательное социальное страхование от несчастных случаев на производстве и профессиональных заболеваний на 2010 год и на плановый период 2011 и 2012 годов | 1 | Current text from 2010-01-01; oldest version available |
| `fz/2009-298-fz/` | О нормативе финансовых затрат в месяц на одного гражданина, получающего государственную социальную помощь в виде социальной услуги по обеспечению лекарственными средствами, изделиями медицинского назначения, а также специализированными продуктами лечебного питания для детей-инвалидов | 1 | Current text from 2010-01-01; oldest version available |
| `fz/2009-345-fz/` | О территориальной юрисдикции окружных (флотских) военных судов | 1 | Current text from 2023-11-27; oldest version available |
