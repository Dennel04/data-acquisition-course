# Tilgaplaadi printimine / Печать капельной пластины

## Seis 14.11.2026

- **Laud 1: valmis.** Prinditi esimene valge V2 ja kuus valget AtomS3R maketti. Kasutaja mõõtis üht plaati ja üht maketti. V2: 167,5 × 167,5 mm, jalgadega umbes 9 mm; kolm klaasituge 0,6 mm igaüks. Plaat istus Gridfinity ruudustikus stabiilselt. Makett: 24 × 24 × 12,9 mm, ekraanisüvend umbes 1,2 mm; istus stabiilselt. Maketi parandatud kõrgus on 12,9 mm, CAD-is 12,8 mm (vahe +0,1 mm). [Mõõtmised](measurements.md) · [Fotod](photos/README.md).
- **Laud 2: valmis.** Teine valge V2 on prinditud. Kasutaja mõõtis klaasitoe kõrguseks 0,6 mm. 167,5 × 167,5 mm, Gridfinity paigutus stabiilne. Klaas liigub nurgatihvtide vahel vabalt; tihvtide vahe ja foto on TODO.
- **Varasem oranž V1:** 80 × 80 × 2,4 mm, oranž PLA, klaasitugedeta ja Gridfinity liideseta. [V1 algfailid, kirjeldus ja fotod](v1/README.md).
- Tilga-, kaamera-, UV- ja robotikatsed on TODO. Tabeli ajad ja massid on slaiseri prognoosid.

## Varasem seis 13.11.2026

**Seis 13.11.2026:** laud 1 (plaat + 6 AtomS3 mudelit) prindib (Denys). **Laud 2 (teine plaat) on printimata** — selle võib printida igaüks meeskonnast.

**Состояние 13.11.2026:** стол 1 (пластина + 6 макетов AtomS3) печатается (Denys). **Стол 2 (вторая пластина) ещё не напечатан** — его может напечатать любой из команды.

| Laud / Стол | Fail / Файл | Aeg / Время | PLA |
|---|---|---|---|
| 1 | [`bgcode/tilgaplaat-1-atoms3-mudel_0.4n_0.2mm_PLA_COREONE_3h9m.bgcode`](bgcode/tilgaplaat-1-atoms3-mudel_0.4n_0.2mm_PLA_COREONE_3h9m.bgcode) | 3 h 9 min | 115 g |
| **2** | [`bgcode/tilgaplaat-2_0.4n_0.2mm_PLA_COREONE_2h38m.bgcode`](bgcode/tilgaplaat-2_0.4n_0.2mm_PLA_COREONE_2h38m.bgcode) | 2 h 38 min | 97 g |

## Juhend (laud 2)

1. Printer: **Prusa CORE One, otsik HF0.4**. Plastik: **hele PLA — valge või kollane** (mitte oranž ega must: kaamera peab halli vaiku plaadil nägema).
2. Laadi fail alla: GitHubis ava ülaltoodud `.bgcode` link → nupp **Download raw file**. (Või `git pull` ja võta fail kaustast `data-acquisition/lab3/tilgaplaat/bgcode/`.)
3. Kopeeri fail **PRUSA USB-mälupulgale** (juurkausta), pane pulk printerisse.
4. Printeris: kontrolli, et alusplaat on puhas ja filament on hele PLA → vali fail → **Print**. Tugesid ega muid seadeid muuta ei ole vaja: kõik on failis (0.20mm SPEED, Prusament PLA 230/60 °C, täide 15 %, tugedeta).
5. Vaata esimene kiht ära (16 Gridfinity jalga peavad kinni jääma). Siis võib minna.
6. Pärast printi: võta plaat jahtunult maha, mõõda nihikuga 2–3 padjandi kõrgus (peab olema ~0,6 mm) ja kirjuta tulemus `README.md`-sse. Täida graveeritud ristid musta markeriga.

## Инструкция (стол 2)

1. Принтер: **Prusa CORE One, сопло HF0.4**. Пластик: **светлый PLA — белый или жёлтый** (не оранжевый и не чёрный: камера должна видеть серую смолу на пластине).
2. Скачай файл: на GitHub открой ссылку `.bgcode` выше → кнопка **Download raw file**. (Или `git pull` и взять файл из `data-acquisition/lab3/tilgaplaat/bgcode/`.)
3. Скопируй файл на **флешку PRUSA** (в корень), вставь флешку в принтер.
4. На принтере: проверь, что стол чистый и заправлен светлый PLA → выбери файл → **Print**. Поддержки и настройки менять не нужно: всё уже в файле (0.20mm SPEED, Prusament PLA 230/60 °C, заполнение 15 %, без поддержек).
5. Посмотри первый слой (16 ножек Gridfinity должны прилипнуть). Дальше можно уходить.
6. После печати: сними остывшую пластину, штангенциркулем измерь высоту 2–3 выступов (должно быть ~0,6 мм) и запиши в `README.md`. Крестики-желобки затри чёрным маркером.

Lähtefail ja parameetrid / исходник и параметры: [`src/da-lab3-tilgaplaat-atoms3-mudel.f3d`](src/da-lab3-tilgaplaat-atoms3-mudel.f3d); kirjeldus lab 3 [`README.md`](../README.md).
