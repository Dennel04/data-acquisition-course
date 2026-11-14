# Andmehõive: Labor 3 — Tilk ja IRQ

**Töömaht:** 30 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 28.10.26 | **Tellimise kuupäev:** 06.11.2026 | **Esimene kaitsmine:** 19.11.2026, veebis

[Ülesanne](assignment-EST.md) · [Tõendid](#tõendid-ja-tulemused) · [Arhitektuur](#süsteemi-arhitektuur) · [Kontrollnimekiri](#kontrollnimekiri) · [Nõutavad väljundid](#nõutavad-väljundid) · [Tööplaan](#tööplaan) · [Kiirstart](#kiirstart-ilma-riistvarata) · [Kaitsmine](#kaitsmise-juhend)

## Ülevaade

Laboris 3 uurime, kuidas teha korduva suurusega vaigutilk ja peatada doseerimine, kui otsik ummistub või süstal tühjeneb. Pump surub vaigu süstlast välja. Klapi lahtioleku aeg määrab doseerimisimpulsi, rõhuandur näitab, mis selle ajal voolikus toimub, ja kaamerapildilt mõõdame tilga suurust.

Rõhuandur annab rõhule vastava pinge. AtomS3R loeb pinget arvuna ja logija seob proovid ajatemplitega. Filter vähendab müra, enne kui arvutame, kui kiiresti rõhk muutub. Kui mõõtmised annavad vea eristamiseks sobiva tunnuse, saab komparaator märgata selle läve ületamist ja tekitada protsessoris katkestuse (IRQ). Katkestus võimaldab reageerida põhitsükli järgmist lugemist ootamata. Tegelikku peatamisaega mõõdame klapi mähisel.

## Praegune seis (14.11.2026)

| Valdkond | Seis |
|---|---|
| Varasemad päriskatsed | Lab 1-s kontrollis meeskond rõhuandurit, pumbajuhtimist ja klaasi tõstmist. Lab 2-s mõõtis meeskond LM358N katseskeemi potentsiomeetritega ning 25.10 rõhuanduriga. Need on varasemate seadistuste tulemused. |
| Tarkvara | Nutikate Lahenduste ühises Atomi projektis on klapi ja UV olekumudel, sündmuste puhver ning native-testid. Lab 3 tilgalogija ja riistvaraliides on TODO. |
| Ettevalmistus | Olemas on [mõõteleht](docs/bench_session.md), [BOM](docs/bom.md), [analüüsiplaan](notebooks/README.md) ja [andmemallid](data/README.md). LED-i, draiveri ja radiaatori read on ühises tellimistabelis; ost ja kättesaamine vajavad kinnitust. |
| CAD ja printimise seis | Laud 1 on valmis: valge V2 ja kuus valget AtomS3R maketti. Kasutaja mõõtis üht V2 plaati ja üht maketti. Laud 2 (teine valge V2) on viimase teate järgi veel printimisel. [Printimisjuhend](tilgaplaat/PRINT.md) · [Mõõtmised](tilgaplaat/measurements.md). |
| Lab 3 füüsiline integratsioon | Tilga-, kaamera-, UV- ja robotikatsed on TODO. Klapi ja UV juhtimine, ohutu väljalülitus, doseerimine, kaamera mõõteskaala ja katkestuse viivitus ootavad päriskatseid. Teise V2 mõõdud ja sobivus on TODO. Kolmes Lab 3 CSV-s on ainult päised. |

## Tõendid ja tulemused

| Tõendi liik | Mida see näitab | Failid |
|---|---|---|
| Lab 1. Füüsiline mõõtmine | MPX5700AP väljund atmosfääril oli 0,85 V. Oma pumbakasti katses kasutas meeskond piire −60 ja −40 kPa; tavavõtmisel õnnestus 10/10 tõstmist. Need piirid ei ole Lab 3 doseerimisseaded. | [Andur ja arvutused](../lab1/docs/sensor_choice.md) · [Pumbakatse](../lab1/docs/pump_control.md) · [Tavavõtmise CSV](../lab1/data/lab1_pick10_fw3_02.10.26.csv) |
| Lab 2. Füüsiline mõõtmine | 22. ja 24.10 katsed kasutasid potentsiomeetreid. 25.10 mõõtis meeskond rõhuanduri signaali **varasema LM358N astme ja 10 kΩ / 10 kΩ jaguriga**. Igas seerias on 1001 lugemit 10 ms sammuga. Vaakumis jäi alumine platoo 14–21 ADC koodi vahele: analoogaste küllastus, kuigi `adc_clipped` oli null. | [Mõõteprotokoll](../lab2/docs/bench_session.md#adc-mõõteseeriad) · [Pump väljas](../lab2/data/opamp_pump_off_test.csv) · [Vaakum](../lab2/data/opamp_vacum_test.csv) · [Ülerõhk](../lab2/data/opamp_pressure_test.csv) |
| Arvutus ja simulatsioon | Võimenduse ja viitepinge arvutus ning Falstadi näide aitavad seletada ADC töövahemikku. Lab 3 komparaatori kohta on tööleht; Lab 2 näide ei tõenda Lab 3 skeemi. | [Lab 2 arvutused](../lab2/docs/opamp_design.md#võimenduse-arvutus) · [Falstadi näite eksport](../lab2/docs/falstad_first_version.txt) · [Lab 3 komparaatori plaan](docs/falstad/README.md) |
| Tarkvaratestid | Ühekordse taimeri käivitamine eelneb väljundi lubamisele. UV käivitamine ja alarmi vabastamine vajavad uut kohalikku kinnitust. Sündmuste puhver säilitab lühikese komparaatorihäire ning töötleb seda enne ootel taimeriteadet. Testid kasutavad loogilisi väljundeid ja simuleeritud sündmusi. | [C++ mudel](https://github.com/Dennel04/smart-solutions-course/blob/5fc4fbf76653ef1a0e92037cb38ebd10012faf00/smart-solutions/lab2/firmware/src/core/actuator_model.cpp) · [Puhver](https://github.com/Dennel04/smart-solutions-course/blob/5fc4fbf76653ef1a0e92037cb38ebd10012faf00/smart-solutions/lab2/firmware/include/actuator_events.h) · [Mudeli testid](https://github.com/Dennel04/smart-solutions-course/blob/5fc4fbf76653ef1a0e92037cb38ebd10012faf00/smart-solutions/lab2/firmware/test/test_actuator_model/test_main.cpp) · [Sündmuste testid](https://github.com/Dennel04/smart-solutions-course/blob/5fc4fbf76653ef1a0e92037cb38ebd10012faf00/smart-solutions/lab2/firmware/test/test_actuator_events/test_main.cpp) |
| Lab 3 CAD ja slaiss, 13.11 | Denys avaldas tilgaplaadi ja ekraanipoole mudeli CAD-i ning kahe laua prindifailid. Plaadi 0,6 mm padjandid on kavandatud mõõt; prinditud padjandite kõrgust tuleb mõõta. Mudeli mõõtude lähteandmed ei kinnita prinditud mudeli mõõte ega sobivust. | [CAD, STL ja 3MF](#nõutavad-väljundid) · [Laudade seis ja BGCODE](tilgaplaat/PRINT.md) |
| Lab 3 füüsilised mõõtmised, 14.11 | Oranž V1: 80 × 80 × 2,4 mm, klaasitugedeta ja Gridfinity liideseta. Esimene valge V2: 167,5 × 167,5 mm, jalgadega umbes 9 mm; kolm mõõdetud klaasituge 0,6 mm igaüks; Gridfinity paigutus stabiilne. Üks valge AtomS3R makett: 24 × 24 × 12,9 mm, ekraanisüvend umbes 1,2 mm; istub stabiilselt. Maketi mõõdetud kõrgus on CAD-ist 0,1 mm suurem (CAD: 12,8 mm). | [Mõõtmised](tilgaplaat/measurements.md) · [V1 ajalugu](tilgaplaat/v1/README.md) · [Originaalfotod](tilgaplaat/photos/README.md) |
| Katseplaan | `drops.csv` seob tilga, pildi ja rõhukõvera. `placement.csv` kirjeldab laigu asukohta ning `latency.csv` reaktsiooniaega. Praegu pole mallides mõõteridu. | [Tilgad](data/drops.csv) · [Paigutus](data/placement.csv) · [Viivitus](docs/latency.csv) · [Ühikud ja väljad](data/README.md) |

25.10 ADC seeriad pärinevad ümberehitusele eelnenud skeemist. CSV-des puudub kalibreeritud rõhk. [Üleandmisleht](../lab2/docs/opamp_v2_handoff_2026-10-25.md) kirjeldab hilisemat ümberehitust ja eristab multimeetri näite arvutuslikest hinnangutest. Muudetud astme kolm rõhupunkti, G5 pingeulatus koos siiretega ning rõhukalibratsioon vajavad eraldi kontrolli. [Lab 2 mõõteandmete selgitus](../lab2/README.md#tõendid-ja-tulemused).

## Allikad ja tõendite piirid

[Ametliku ülesande koopia](assignment-EST.md) on muutmata. 25.10.2026 kontrollitud Git blob SHA on `3b8089eb54e7587946d42ffa25a071f35e174396`. [Õppejõu algallikas](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLab%203%5D%20EST.md) määrab nõuded; [ametlik kokkuvõte](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLabor%203%20kokkuv%C3%B5te%5D%20EST.md) on abiallikas.

## Eesmärk ja pneumaatika

Tööjärjekord on **doseerimine → klaasi tõstmine → kõvendamine → väljund**. Kõigepealt paneme tilga mudelile, siis tõstame iminapaga klaasi tilgale. UV-lamp kõvendab vaigu katte all ja tööriist viib detaili väljundisse. Üks pump ei ime ja puhu korraga.

[Ühenduste plaan](#süsteemi-arhitektuur) näitab pumba harude ja süstlaklapi asetust.

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

TODO: täita tegelike otsuste ja mõõtmiste järel.

## Süsteemi arhitektuur

**Lab 3 ühenduste plaan:**

```text
Pump → Y1 ┬→ iminapp
          └→ 3/2 klapp → süstal → otsik → tilk
                └→ atmosfäär (süstla väljalase vooluta olekus)

Rõhuandur (Y2, asukoht valida) → mõõteaste → AtomS3R ADC → USB → tilgalogija
AtomS3R → relee → klapi mähis
AtomS3R → LED-draiver → 405 nm UV LED katte all
Komparaator → AtomS3R katkestussisend (IRQ)
```

- **Õhutee.** Iminapp on otse pumba harus. 3/2 klapp juhib ainult süstlaharu: voolu all ühendab klapp süstla pumbaga, vooluta lahutab süstla pumbast ja ühendab selle atmosfääriga. Rõhuanduri jaoks võrdleme teise Y-liitmiku asukohta enne klappi ja süstlaharus. Nõelventiili kaalume siis, kui lahtise iminapa õhukadu takistab rõhu hoidmist; mõõdame ka mõju imemisele. [Pumbajuhtimise plaan](docs/pump_control.md).
- **Mõõteahel.** Lab 1 andur läks otse G5-le; Lab 2 katseskeemis oli vahel LM358N aste ja jagur. Dokumenteeritud Lab 2 skeemis puhverdas **LM358N teine kanal viitepinget**. Enne selle kanali kasutamist komparaatorina tuleb lahendada puhvri ülesanne ja kontrollida lõplikku skeemi. [Lab 2 ühendused](../lab2/docs/bench_session.md#katseskeemi-ühendused) · [Viitepuhvri üleandmine](../lab2/docs/opamp_v2_handoff_2026-10-25.md).
- **Juhtimine.** AtomS3R loeb rõhusignaali ning peab juhtima klappi relee ja UV-lampi draiveri kaudu. Nutikate Lahenduste ühine Atomi projekt annab olekumudeli ja testid. Asjaosalised peavad kokku leppima käsud, lubatud kestused, GPIO tasemed ja alarmisündmuse vormingu. Mudel ja puhver vajavad eraldi riistvaraadapterit; puhver ei sobi otse ISR-i. UV ohutus vajab sõltumatut blokeeringut ja päris väljalülituse kontrolli. [Atomi liidese plaan](https://github.com/Dennel04/smart-solutions-course/blob/856fe7e86df09ce37abe7b29613425f90cbc6b96/smart-solutions/lab3/docs/atom_page.md) · [Püsivara ja logija plaan](src/README.md).
- **Tööriist.** 3D printimise meeskonnaga tuleb kokku leppida klapi asukoht, voolikupikkus ja juhtmete teekond. Uue tööriista jaoks mõõdame samast flantsi referentsist neli nihet: iminapp, süstla otsik, UV-laik ja kaamera keskpunkt. Enne roboti katset tuleb kinnitada sobivus, koormus ja uued tööpunktid. [Tööriista paigutus](https://github.com/Dennel04/3d-printing-course/blob/2cec9c8058282a3d7fa94cb977e4abd9002db7b0/3d-print/lab3/docs/tool_layout.md) · [Neli nihet](https://github.com/Dennel04/3d-printing-course/blob/2cec9c8058282a3d7fa94cb977e4abd9002db7b0/3d-print/lab3/docs/tool_offsets.md).

## Kontrollnimekiri

Järgmised 16 punkti on ametlikust ülesandest sõna-sõnalt ja samas järjekorras. Dokumentatsiooni sünkroonimine ei täida füüsilisi kriteeriume.

- [ ] Klapp lülitab Atomi käsu peale. Vooluta on süstal õhu peal ja pumbast lahti. Mõõdetud, mitte oletatud.
- [ ] Impulsi pikkust loeb riistvarataimer. Käsk ja ostsilloskoobilt klapi mähisel mõõdetud pikkus kõrvuti viie pikkuse kohta.
- [ ] UV LED lülitab Atomi käsu peale ja kustub alati ise.
- [ ] Anduri koht voolikus valitud ja põhjendatud.
- [ ] Tilgad: vähemalt viis impulsi pikkust, kümme tilka igaühega, iga tilk mõõdetud pildilt tilgaplaadil ja iga tilga rõhukõver salvestatud. Fail `data/drops.csv`.
- [ ] Teine muutuja läbi proovitud: teine otsik või teine rõhk, kolme impulsi pikkusega.
- [ ] Atomi ekraanipoole mudelid prinditud päris AtomS3 mõõtude järgi. Tilk ja klaas mudeli peal, laigu suurus ja koht mõõdetud tööriista kaamera pildilt. Tulemused ja pildid failis `data/placement.csv`.
- [ ] Retsept kirjas failis `docs/recipe.md`: otsik, rõhk, impulss, kõvendamise aeg, ja klaas selle tilga peal läbi proovitud.
- [ ] Toores ja filtreeritud muutumise kiirus kõrvuti samal kõveral, spektrid kõrvuti. Filter valitud numbritega.
- [ ] Sama muutumise kiirus Labori 2 pooliku haarde logil: kas "vaakum püsib" on nüüd otsus.
- [ ] Komparaator Falstadis: lülitub kinnise otsiku peale, ei lülitu tavalise tilga ega müra peale.
- [ ] Komparaator plaadil, katkestus (IRQ) Atomis: klapp tagasi, alarm lukus, sündmus välja.
- [ ] Reageerimise aeg ostsilloskoobilt, kümme korda, katkestusega ja ilma. Fail `docs/latency.csv`.
- [ ] Kinnine otsik kümme korda ja tühi süstal kümme korda: mitu korda tabas. Tavaline tilk kolmkümmend korda: mitu valehäiret.
- [ ] Tellimus 06.11 failis `docs/bom.md`.
- [ ] Repo ja arenduspäevik täidetud, tag `data-acquisition-lab3`.

**KAARDISTA ISE — kuupäevad ja sinu enda sammud.**

TODO: täita päris töö käigus.

## Nõutavad väljundid

- [Tilgamõõtmised](data/drops.csv), iga tilga algne rõhukõver, foto, mõõtkavapilt ja kontrollitud kontuuridega pilt; [paigutusmõõtmised](data/placement.csv).
- [Andmeskeem ja ühikud](data/README.md), [analüüsiplaan](notebooks/README.md) ja [püsivara/logija plaan](src/README.md).
- [Retsept](docs/recipe.md), [viivitused](docs/latency.csv), [BOM](docs/bom.md), [pumbajuhtimine](docs/pump_control.md) ja [füüsilise töö kontrollleht](docs/bench_session.md).
- [Falstadi elav link, eksport ja skeemipilt](docs/falstad/README.md), [ostsilloskoobitõendid](docs/scope/README.md), elektriline skeem pildina ning füüsilise ahela foto: **TODO**.
- **Valge V2 tilgaplaat ja AtomS3 ekraanipoole mudel (13.11.26, CAD + slaiss):** ühine Fusioni fail [`tilgaplaat/src/da-lab3-tilgaplaat-atoms3-mudel.f3d`](tilgaplaat/src/da-lab3-tilgaplaat-atoms3-mudel.f3d) (parameetrid `dp_*`, `at_*`), STL [`tilgaplaat/stl/tilgaplaat.stl`](tilgaplaat/stl/tilgaplaat.stl), [`atoms3-mudel/stl/atoms3-mudel.stl`](atoms3-mudel/stl/atoms3-mudel.stl), 3MF [`tilgaplaat/3mf/`](tilgaplaat/3mf/).
  - Tilgaplaat: 4 × 4 Gridfinity (167,5 mm, standardne jalg), 5 × 5 tilka sammuga 32,5 mm; iga tilga peale oma klaas 30 × 30 × 1,2 mm, mida hoiavad nurgatihvtid (0,3 mm lõtk külje kohta); vahetükid = neli 0,6 mm padjandit klaasi servade keskel (õhk pääseb nurkadest välja). Mõõtkava: graveeritud ristid ±11 mm tilga keskpunktist (22 mm vahe), 0,6 mm laiad, 0,4 mm sügavad (täita musta markeriga). Rea 1 / veeru 1 nurga tihvt on 3 mm kõrgem. Padjandite tegelik kõrgus tuleb iga plaadi juures mõõta.
  - AtomS3 ekraanipoole CAD-mudel: välismõõt 24 × 24 mm ja kõrgus 12,8 mm, nurga R 3 mm, ekraani ava 17,8 mm → 45° faas → 16,2 mm, ekraan raamist 1,2 mm madalamal. Lähteandmed: M5Stacki STL `C123_AtomS3` ning 13.11.26 nihikumõõdud. Mudel on alt lahti, et see mahuks akumooduli tihvtidele. Ekraaniala soon on 15 mm ja skaala samm 2 mm. Ühe valge AtomS3R maketi parandatud füüsiline kõrgus on 12,9 mm (CAD-ist +0,1 mm), vt [mõõteleht](tilgaplaat/measurements.md).
  - Print: Prusa CORE One HF0.4, `0.20mm SPEED`, hele PLA (valge/kollane), täide 15 %, tugedeta. Laud 1 = plaat + 6 mudelit, 3 h 9 min, 115 g; laud 2 = teine plaat, 2 h 38 min, 97 g.
  - Taust ja allikad (patendid US 5837892 jt: pindala × kalibreeritud vahe; prinditud vahe viga ±0,05 mm ≈ ±8 % mahust 0,6 mm juures): kokkuvõte meeskonna märkmetes.
  - [Printimisjuhend ja laudade seis](tilgaplaat/PRINT.md) · [Prusa BGCODE-failid](tilgaplaat/bgcode/). Ajad ja materjalikogused ülal on slaisseri hinnangud.

## Tööplaan

Numbrid viitavad [kontrollnimekirja](#kontrollnimekiri) punktidele nende algses järjekorras. A–F näitavad töö sõltuvusi; enne füüsilisi katseid vaata [ohutusjuhiseid](#ohutus).

### A. Inventuur ja elektriohutus

- **Eeldus ja alus (3, 15).** [BOM-is](docs/bom.md#uv-komponentide-valik-ja-tellimisolek) on 405 nm LED-i, draiveri ja radiaatori valik ning tabelisse kandmise olek. Varasem Lab 2 pingenäit käib oma katseskeemi kohta.
- **Puuduv töö.** Kinnita saadavus ja osade markeeringud. Kontrolli klapi nimipinget ja voolu, relee sobivust induktiivkoormusega, kaitsedioodi ning jõu- ja loogikaahela eraldust. Enne Atomi ühendamist mõõda tegelik pingeulatus. Kontrolli UV-ühilduvust ja jahutust, katte valgusleket, taimerit, sõltumatut väljalülitust ning vooluta olekut.
- **Tõend ja failid.** Lisa inventuur ja tellimise tõendid [BOM-i](docs/bom.md), mõõdetud pinged ja ühendused [mõõtelehele](docs/bench_session.md) ning UV automaatse kustumise katse [ostsilloskoobi tõenditesse](docs/scope/README.md).

### B. Pneumaatika, relee, klapp ja taimer

- **Eeldus ja alus (1, 2, 4).** Läbi A etapi kontrollid. Kasuta [Y-pneumaatika plaani](#süsteemi-arhitektuur) ja ülesandes nõutud M5Stack Mini 3A Relay Unit moodulit. Tarkvaramudeli taimer ei ole veel riistvarataimer.
- **Puuduv töö.** Tuvasta relee NO/NC kontaktid multimeetriga. Kinnita rõhumõõtmisega süstla tühjenemine atmosfääri toite kadumisel. Vali anduri koht ja mõõda rõhku lahtise iminapaga. Võrdle viie impulsi pikkuse juures, igaüht kümme korda, käsku, GPIO signaali ja mähise pinget. Hinda relee viivitust, kontaktipõrget ja elektrilist eluiga; mõõda rõhukõveralt eraldi klapi mehaaniline avanemisviivitus. Dioodita väljalülitustipu mõõtmine vajab õppejõuga kooskõlastatud ohutut protseduuri.
- **Tõend ja failid.** Lisa ühendusskeem, foto ja ohutu oleku rõhukõver [mõõtelehele](docs/bench_session.md). Salvesta kahe kanaliga [ostsillogrammid](docs/scope/README.md), ajastustabel ning anduri asukoha põhjendus [pumbajuhtimise töölehele](docs/pump_control.md).

### C. Doseerimine, fotod ja tilga suurus

- **Eeldus ja alus (5–7).** Kinnita klapi ja UV ohutu toimimine ning rõhu mõõtmise sobivus. [Kaamera- ja tilgamõõtmise plaan](notebooks/README.md#tilgad-ja-paigutus) kirjeldab pilti, kontuuri ja rõhukõverat. Õppejõu soovitus alustada peenest otsikust, madalast rõhust ja üle 100 ms impulsist on lähtekoht, mitte katsetatud retsept.
- **Puuduv töö.** Pärast teise V2 printimist mõõda selle klaasitoe kõrgus ning kontrolli plaadi mõõte ja sobivust. Kalibreeri XIAO kaamera pilt samalt kõrguselt iga seansi alguses; kontrolli fookust ja valgustust. Tee viis impulsi pikkust × kümme tilka ning proovi teist otsikut või rõhku kolme pikkusega. Mõõda pildilt pindala ja kasuta kihi kõrgust ruumala hindamiseks. Võrdle lineaarsust, korduste hajuvust (CV) ja esimest impulssi pärast pausi. Päris AtomS3 peale vaiku ei katsetata; mõõda [prinditud maketil](tilgaplaat/measurements.md) laigu pindala ja nihe.
- **Tõend ja failid.** Seo iga `drop_id` foto, mõõtkava, kontrollkontuuri ja algse rõhukõveraga failis [drops.csv](data/drops.csv). Lisa mudeli katse pildid ja tulemused faili [placement.csv](data/placement.csv). Viita olemasolevale Fusioni lähtefailile ja STL-idele ning lisa prinditud detailide mõõtmised. [Andmevorming](data/README.md).

### D. Filter, rõhutuletis ja poolik haare

- **Eeldus ja alus (9, 10).** Kasuta kalibreeritud rõhku ning kontrollitud ajatempleid. [Varasema Lab 2 ADC logid](#tõendid-ja-tulemused) näitavad ajastust ja küllastust; need ei sisalda tõendatud pooliku haarde rõhukõverat.
- **Puuduv töö.** Arvuta kahe proovi rõhuvahe jagatuna tegeliku ajavahega sekundites (kPa/s). Tuletis võimendab kõrgsageduslikku müra; ideaalse tuletise sagedustegur on `2πf`. Võrdle libisevat keskmist ja mediaanfiltrit **enne tuletist**, hinnates mõlema müra ja viivitust. Hinda kontrollitud Lab 2 pooliku haarde logil eristamise läve ja aega pärast pumba peatamist. Võrdle tavalise tilga, ummistuse ja tühja süstla tõusu, platood ning langust. Vali tunnus ja lävi pärisandmetest.
- **Tõend ja failid.** Lisa kõrvuti toore ja filtreeritud muutumiskiiruse graafikud, spektrid ning müra ja viivituse võrdlustabel. Lisa põhjendatud filtrivalik [analüüsi](notebooks/README.md#filter-tuletis-ja-otsus) ja pooliku haarde otsuse alus [pumbajuhtimise töölehele](docs/pump_control.md#pooliku-haarde-tuletise-otsus).

### E. Komparaator, IRQ, alarm ja reaktsiooniaeg

- **Eeldus ja alus (11–14).** Kasuta D etapi tunnust ja läve ning lahenda LM358N viitepuhvri ülesanne. [Falstadi tööleht](docs/falstad/README.md) ning [olekumudel ja sündmuste testid](#tõendid-ja-tulemused) annavad erinevad kontrollid: üks analoogahela käitumisele, teine tarkvarareeglitele.
- **Puuduv töö.** Katseta Falstadis läve ja hüstereesi tavalise, müraga tavalise ja ummistunud otsiku signaaliga. Ehita ahel ning mõõda madal ja kõrge väljund ning siirded enne Atomi ühendamist. Kõrge tase peab jääma nii 3,3 V kui ka valitud viigu lubatud piiri sisse. Kinnita klapi vooluta viimine, alarmi lukustumine ja jaamale saadetav sündmus. Katkestusrutiin hoiab ajakriitilise töö lühikesena; põhitsükkel tegeleb ekraani ja USB-teatega. Tühja süstla alarmi rõhuplatoo ja ajapiir tuleb valida tegelikest kõveratest. Ära luba uut doseerimist enne vea kõrvaldamist ja alarmi kinnitatud vabastamist.
- **Tõend ja failid.** Lisa Falstadi link, eksport ning skeemipilt. Mõõda läve ületamisest klapi mähise väljalülitumiseni kümme korda IRQ ja kümme korda põhitsüklis küsitlemisega (polling), ka koormuse all. Salvesta [ostsillogrammid](docs/scope/README.md) ja [latency.csv](docs/latency.csv). Esita keskmine ja halvim viivitus, arendusajad ja meetodi valiku põhjendus. Loenda tabamised kümnel ummistuse ja kümnel tühja süstla katsel ning valehäired 30 tavalisel tilgal.

### F. Retsept, integratsioon ja kaitsmine

- **Eeldus ja alus (8, 16).** Kasuta C etapi tilgaandmeid, E etapi ohutustõendeid ning kontrollitud tööriista ja nihete andmeid. [Retsept](docs/recipe.md) on täitmata mall. [Püsivaraplaan](src/README.md) kirjeldab tulevast liidest ja eraldi tilgalogijat.
- **Puuduv töö.** Proovi klaasi prinditud ekraanipoole mudelil. Kinnita, et kõvendatud tilk hoiab klaasi ega ulatu servani. Kooskõlasta klapi ja UV käsud ning alarmi käitumine jaamaga; [õppejõu JSON-näited](assignment-EST.md#1-klapp-ja-impulss) ei ole teostatud käsuleping. Kinnita tööriista sobivus ja katseta kogu tsüklit alles pärast eelnevaid ohutuskontrolle.
- **Tõend ja failid.** Lisa retsepti otsik, rõhk, impulss, kõvendusaeg ning viited piltidele ja kõveratele. Kogu mõõte- ja tarkvaratõendid, uuenda päevikut päris töö järel ja valmista ette [ametlik kaitsmine](assignment-EST.md#kaitsmine). Tag kuulub lõplikule esitamisele.

## 1. Klapp, relee ja impulss

1. Kasutada ülesande järgi **M5Stack Mini 3A Relay Unit** moodulit. Lugeda päris klapi nimipinge ja vool ning relee täpne markeering; kontrollida induktiivse DC-koormuse sobivust andmelehelt.
2. Hoida klapi jõuahel ja Atomi loogikaahel eraldi. Mõõta pingestamata COM/ON/OFF kontaktide tegelik NO/NC olek multimeetriga; märgistusest üksi ei järeldata ohutut kontakti. GPIO ja ühendused: **TODO: kontrollitud riistvara ja lähtekood**.
3. Kaitsediood klapi mähisega rööbiti: katood ehk triip plussi poole. Kontrollida polaarsus ja pinge-/voolutaluvus enne ühendamist.
4. Kontrollida füüsiliselt, et Atomilt/toitelt voolu kadumisel klapp lahutab pumba ja tühjendab süstla atmosfääri. Mõõta süstlaharu rõhk ja säilitada ohutu oleku tõend.
5. Ajastada impulss riistvarataimeriga. Mõõta kahe kanaliga Atomi GPIO signaal ja **klapi mähise pinge**: viis pikkust × kümme mõõtmist. Võrrelda käsku, GPIO-impulssi ja mähise impulssi, keskmist ning hajuvust.
6. Mõõta relee sisse-/väljalülitusviivitus ja kontaktipõrge; võrrelda andmelehega. Hinnata elektriline kontaktide eluiga lülitustes ja päevades tegeliku kavandatud tilkade arvu järgi, arvestades induktiivset koormust. Releega kiiret PWM-i ei tehta. Piirid jäävad võrdluseks hilisema labori MOSFET-lahendusele.
7. Mõõta rõhukõveralt eraldi klapi mehaaniline avanemisviivitus. Valida anduri koht ning dokumenteerida kompromiss.
8. UV LED läbi sobiva draiveri, taimeriga automaatne väljalülitus ja must kaitsekate. Kuni LED/draiver puuduvad, on tulevane taimerikatse ostsilloskoobiga Atomi viigul.

Tõendid [mõõtelehel](docs/bench_session.md): ühendusskeem pildina, füüsilise ahela foto, süstlaharu rõhk vooluta, relee andmeleht ning ajastustabelid — kõik **TODO**. Ilma dioodita väljalülitustipu mõõtmine on lubatud ainult pärast ohutu protseduuri kooskõlastamist õppejõuga; seda pole tehtud.

Õppejõu liidese näited, mitte meeskonna teostatud tulemus:

Arvuti → Atom:

```json
{"cmd":"dispense","ms":200}
{"cmd":"uv","ms":5000}
{"cmd":"clear"}
```

Atom → arvuti:

```json
{"ev":"dispense_start","t":123456}
{"ev":"dispense_end","t":123660}
```

## 2. Tilga suurus ja ekraanipoole mudel

- Mõõta rõhk lahtise napaga ja kontrollida, kas pumba riba jõuab väljalülituseni. Doseerimisrõhk, süstla täituvus ja vooliku pikkus: **TODO**.
- Õppejõu lähte-soovitus on **kõige peenem otsik, madal rõhk ja üle 100 ms impulss**; need pole meeskonna valitud retsept ega mõõtetulemused.
- Valmistada hele PLA tilgaplaat prinditud mõõtkavaga. Paigutus 5 × 5: read on impulsi pikkused, veerud kordused; vähemalt viis pikkust × kümme kordust ehk vähemalt 50 tilka (kaks plaati põhisarjaks). Tilkade vahe valida esimesest katsest suurem kui suurim laik.
- Klaas asetada mõõdetud kõrgusega prinditud vahetükkidele. Salvestada kõrgus ja mõõtemeetod; CAD/STL ning tegelik sobivus on TODO. Tilgad teha järjest, kõvendada plaat ja alles siis pildistada.
- Kasutada tööriista **XIAO ESP32S3 Sense** kaamerat. Hoida stabiilne töökõrgus, kaamera risti plaadiga, fookus ja hajus/külgvalgus; UV on pildistamisel väljas. Kaamera flantsinihe tuleb [3D L3 nelja nihke dokumendist](https://github.com/Dennel04/3d-printing-course/blob/6068053f90d09fa301889ee4476e139a78dd82ad/3d-print/lab3/docs/tool_offsets.md), mitte vanast oletusest.
- Leida terav töökõrgus katseliselt; igal seansil mõõtkavapilt, `mm/pixel` ning väikseima tilga läbimõõt pikslites. Segmenteerida laik ja joonistada leitud kontuur fotole tagasi kontrollimiseks.
- Arvutada pindala `area_px × mm_per_pixel²` ühikus mm² ja ruumala `area_mm2 × layer_height_mm` ühikus µL (1 mm³ = 1 µL). Hinnata ühe piiripiksli mõju pindalale protsentides; mõõteviga peab olema uuritavast hajuvusest väiksem.
- Iga `drop_id` siduda foto, kontuuripildi, mõõtkavapildi ning algse rõhukõveraga [drops.csv-s](data/drops.csv). Iga tilga nihikuga mõõtmine ei ole uus meetod.
- Hinnata lineaarsust: kus suuruse ja impulsi seos paindub ja miks; eraldi arvutada `CV = standardhälve / keskmine` ning protsentides `100 × CV`.
- Kontrollida esimest impulssi pärast pausi. Teine muutuja on teine otsik **või** rõhk, kolme impulsi pikkusega. Võrrelda rõhuplatoo ja kõvera pindala seost tilga suurusega.

**Päris AtomS3 peale vaiku ei katsetata.** Mõõta nihikuga päris korpuse välismõõt, ekraani ava suurus/asukoht, raam ja ekraani sügavus raamist. Nende järgi kavandada õhuke prinditav ekraanipoole koopia, kontrastne ekraaniala ja sobivus hoidikusse; CAD-lähtefail ning STL: **TODO**. Katsetada vaiku, klaasi ja kõvendamist prinditud mudelil, mõõta kaamerapildilt laigu pindala ja nihe ekraani keskpunktist x/y millimeetrites ning servani jõudmine [placement.csv-s](data/placement.csv). Retsept [recipe.md-s](docs/recipe.md) kehtib alles päris katse järel.

**KAARDISTA ISE — mida sa päriselt kasutasid.**

TODO: füüsilised mõõdud, töövahendid, failid ja tõendid.

## 3. Filter ja tuletis

Õppejõu 100 Hz lähtevalem: `dP/dt = (P_now - P_previous) / 10 ms`. Enne arvutamist kontrollida päris CSV ajatemplite vahet; kPa/s saamiseks kasutada ajasammu sekundites. Kavandatud 100 Hz ei tõenda tegelikku ajastust.

Järjekord: päris rõhuandmed → toores dP/dt → rõhu ja tuletise spektrid → libisev keskmine ning mediaan **enne tuletist** → kummagi müra ja viivituse arvuline võrdlus → põhjendatud valik. Selgitada sagedusvõimendust `2πf`.

Seejärel rakendada valitud meetodit kontrollitud Lab 2 pooliku haarde logile pärast pumba väljalülitumist ning määrata eristamise lävi ja aeg otsuseni. Kui päris logi puudub, jääb töö TODO. Võrrelda normal / clogged / empty rõhukõveraid: tõusukiirus, platoo ja langus pärast ventileerimist. Tunnus, filter, läved ning ajapiirid: **TODO: ainult pärisandmetest**.

## 4. Katkestus (IRQ)

1. Falstad esmalt: valitud rõhu- või tuletisesignaal, komparaator ja hüsterees. Tavaline ning müraga tavaline tilk ei tohi lülitada, kinnine otsik peab lülitama. Takistid ja läved: **TODO**.
2. Füüsiline ahel kasutab ülesande järgi **LM358N teist poolt**. Enne ümberühendamist lahendada Lab 2 viitepinge puhvri vajadus. Mõõta väljundi madal/kõrge pinge ja üleminekud **enne Atomi ühendamist**; kõrge tase ei tohi ületada 3,3 V ega konkreetse viigu kontrollitud lubatud piiri. Vajadusel arvutada ja mõõta sobiv jagur; LM358N toide ei tõenda väljundi sobivust.
3. ISR-is ainult käsk klapi viivitamatuks vooluta viimiseks ja lipp. Relee/klapi mehaaniline vabastus pole sama kui GPIO muutus. Põhitsüklis ekraan, USB alarmisündmus ning alarmi lukustus; järgmist doseerimist ei lubata kuni `clear` käsuni.
4. Tühja süstla jaoks määrata normaalse tilga pärisandmetest oodatud platoo ja lubatud aeg. Kui rõhk selle ajaga platooni ei jõua, lukustada `empty` alarm. Väärtused **TODO**.
5. Mõõta ostsilloskoobiga rõhu läve ületusest **mähise pinge** vabastuseni kümme korda IRQ-ga ja kümme korda polling'uga; korrata koormatud põhitsükliga. Tulemused [latency.csv-s](docs/latency.csv).
6. Kinnine otsik ×10 ja tühi süstal ×10: tabamised; tavaline tilk ×30: valehäired. Kõik tulemused **TODO**.

Viivituse tulemused ja otsus:

- katkestuse keskmine viivitus: **TODO: ms**;
- katkestuse halvim viivitus: **TODO: ms**;
- polling'u keskmine viivitus: **TODO: ms**;
- polling'u halvim viivitus: **TODO: ms**;
- polling'u viivitus põhitsükli koormusega: **TODO: ms, keskmine ja halvim**;
- katkestuslahenduse arendusaeg: **TODO**;
- polling'u lahenduse arendusaeg: **TODO**;
- lõplik valitud meetod ja ühe lause põhjendus: **TODO: valida mõõtetulemuste põhjal**.

## Kiirstart ilma riistvarata

Ava macOS-is või Linuxis terminal repo juurkaustas. Olemasolev Python 3 analüsaator loeb Lab 1 tavavõtmise CSV-d ja selle kõrval olevat sündmuslogi. See kasutab standardteeki; väljund läheb ajutisse kausta.

```sh
lab3_demo=$(mktemp -d) &&
python3 -B data-acquisition/lab1/src/python/analyze_run.py \
  data-acquisition/lab1/data/lab1_pick10_fw3_02.10.26.csv > "$lab3_demo/lab1-pump.txt" &&
cat "$lab3_demo/lab1-pump.txt"
```

Kokkuvõttes näed ligikaudu 100 Hz proovivõttu, pumba 45,2% tööaja osakaalu ja kümne võtmise sündmusi. Need on Lab 1 logi tulemused. Lab 2 jaoks ava [mõõtmiste tabel ja olemasolev analüüsijuhend](../lab2/README.md#kiirstart-ilma-riistvarata). Lab 3 kohta näita [mudeli ja sündmuste teste](#tõendid-ja-tulemused) ning tühje andmemalle; päris tilgaandmeid ega valminud Lab 3 tilgaanalüsaatorit siin veel ei ole.

## Kaitsmise juhend

Seitsme minutiga saad anda ülevaate ilma Atomi, pumba, roboti ja UV-lambita. Ava enne esitlust kiirstardi väljund, Lab 2 mõõteprotokoll ja mudeli testid. [Ametlik 15-minutiline kaitsmine](assignment-EST.md#kaitsmine) nõuab lisaks retsepti järgi doseerimist ja rõhukõverat, ummistuse reaktsiooni ostsilloskoobil ning alarmiluku näitamist: uut tilka ei tule enne alarmi vabastamist.

| Aeg | Mida näidata ja selgitada |
|---|---|
| 0:00–1:15 | [Arhitektuur](#süsteemi-arhitektuur). Jälgi õhu teed Y1-st iminapa ja süstlani. Selgita vooluta klapi olekut ja töötsükli järjekorda. |
| 1:15–2:45 | [Kiirstardi väljund](#kiirstart-ilma-riistvarata) ja [Lab 2 mõõtmised](#tõendid-ja-tulemused). Näita Lab 1 pumbalogi kokkuvõtet. Selgita, miks Lab 2 vaakumiplatoo kirjeldab vana astme küllastust ning miks sellest ei saa Lab 3 rõhku ega läve. |
| 2:45–4:15 | [Mudel ja testid](#tõendid-ja-tulemused). Näita, kuidas taimeri käivitamise nõue ja kohalik kinnitus piiravad väljundeid ning kuidas lühike häire jääb puhvris meelde. Nimeta päris ISR-i ja UV blokeeringu kontrollid. |
| 4:15–5:45 | [Andmemallid](data/README.md) ja [ostsilloskoobi plaan](docs/scope/README.md). Näita, kuidas tilga ID seob kõvera ja foto, mida võrrelda filtritel ning milliste sündmuste vahel mõõta reaktsiooniaega. |
| 5:45–7:00 | [Kontrollnimekiri](#kontrollnimekiri) ja [päevik](#arenduspäevik). Nimeta puuduv elektriline kontroll, tilga- ja kõvenduskatsed ning IRQ/polling võrdlus. Selgita, mida tuleb enne ametlikku kaitsmist laboris näidata. |

## Ohutus

- UV valgustamine musta katte all, valgus ei paista välja. Kõigil laua ääres 405 nm kaitseprillid, kui LED on draiveriga ühendatud. LED-i ei vaadata; lamp laua poole, taimeriga auto-off ja vooluta väljas.
- Süstlad täidab õppejõud; täidetud süstlal otsikukork ja tagumine kolb. Lahtise süstlaga nitriilkindad. Vaik koristada IPA/paberiga, saastunud paber kõvendada enne jäätmesse panemist; kõvenemata vaiku ei valata kraanikaussi.
- Lampi ei suunata tavapärasele otsikule. Tulevase ummistuskatse üks otsik valmistatakse eraldi süstlast lahti, vaiguga täidetult ja katte all kõvendades; märgistada. See pole veel tehtud.
- Kinnine süstal on rõhu all suletud anum: hoidikus/statiivis, mitte käes. Enne eemaldamist klapp vooluta ja süstlaharu rõhu vabanemine füüsiliselt kinnitatud. Kuni IRQ-kaitse on kontrollitud, inimese käsi pumba lüliti juures.
- Klapi mähisel kaitsediood; dioodita mõõtekatse ainult õppejõuga kooskõlastatud ohutu protseduuriga ja sobiva sondi/ulatusega. Klapi jõuahelat ei ühendata Atomi loogikapoolega; võrgupinget releega ei lülitata.
- ADC ja IRQ ei talu 5 V. Kontrollida väljundpinge enne Atomi ühendamist. USB ja toide välja enne juhtmete muutmist.
- Pumbakast 24 V; DO-liinid ühendada ainult keelatud roboti ja vooluta kastiga. Lahtist +110 kPa voolikut ei suunata inimeste poole.
- Käed lauast eemal, kui MG400 on sisse lülitatud; esimene jooks aeglaselt, hädastopp käeulatuses. Esmased tilgakatsed laual; hilisem robotiga pildistamine alles ohutu seadistuse järel.
- Otsikule kork, kui ei doseerita. Selles laboris ei joodeta.

## Hindamiskriteeriumid

| Kategooria | Punktid | Ettevalmistuse olek |
|---|---:|---|
| Tööfailid — püsivara taimeri/IRQ/alarmiga, logija, drops.csv, kõverad ja analüüs | 5 | Mallid; **TODO: kood ja päris andmed** |
| Analüüs — käsk/GPIO/mähis, kaameraga tilga suurus ja hajuvus, spektrid, filter ja viivitus | 5 | **TODO: mõõtmised ja analüüs** |
| Prototüüp — vooluta süstal atmosfääri, retsept mudelil hoiab klaasi ega ulatu servani, õiged alarmid | 5 | **TODO: füüsilised katsed** |
| Dokumentatsioon — README, päevik, retsept, latency.csv, Falstad, pump_control.md, BOM, AGENTS.md | 5 | Mallid; **TODO: tulemused ja tõendid** |
| **Kokku** | **20** | **TODO** |

## Arenduspäevik

Lisa ainult tegeliku töösessiooni järel uus sissekanne; olemasolevaid sissekandeid hiljem ei muudeta.

**PP.KK.AA — osalejad**

- Tegime:
- Juhtus (numbrid ja ühikud):
- Otsustasime, ja miks:
- Failid:
- Lahti järgmiseks korraks:

**25.10.2026 — dokumentatsiooni sünkroonimine; osalejad teadmata**

- Tegime: võrdlesime ametlikku ülesannet ja kokkuvõtet, säilitasime täpse ülesandekoopia ning uuendasime ainult Lab 3 dokumente ja tühje andmemalle.
- Juhtus (numbrid ja ühikud): ülesande blob SHA `3b8089eb54e7587946d42ffa25a071f35e174396`; 16 ametlikku kontrollpunkti kopeeriti sõna-sõnalt. Füüsilist sessiooni, mõõtmisi ega katseid ei toimunud.
- Otsustasime, ja miks: kehtiv alus on releega juhitud süstlaharu, vooluta atmosfääri tühjendus ja kaamerapõhine tilgamõõtmine; varasem plaan on asendatud ametliku redaktsiooni järgi.
- Failid: `assignment-EST.md`, `README.md`, `data/README.md`, `data/drops.csv`, `data/placement.csv`, `docs/bom.md`, `docs/bench_session.md`, `docs/pump_control.md`, `docs/recipe.md`, `docs/scope/README.md`, `docs/falstad/README.md`, `notebooks/README.md`, `src/README.md`.
- Lahti järgmiseks korraks: inventuur, Lab 2 lõpliku skeemi ja kalibratsiooni kontroll, mõõdetud relee-/klapiühendus, kaamera skaala ning plaadi, vahetükkide ja ekraanipoole mudeli füüsilised mõõdud. Kõik füüsilised Lab 3 tulemused jäävad TODO.

**07.11.2026 — dokumentatsiooni sünkroonimine (Codex)**

- Codex võrdles [3D printimise Lab 3 BOM-i](https://github.com/Dennel04/3d-printing-course/blob/9cf6bf179b39b055f85b1e05a061bb8c26b49af6/3d-print/lab3/docs/bom.md), [Nutikate Lahenduste Lab 3 päevikut](https://github.com/Dennel04/smart-solutions-course/blob/7bc372c7d90253701caf3b026c0a7f17c4528cf6/smart-solutions/lab3/README.md#arendusp%C3%A4evik) ning [ühise Atomi projekti C++ mudelit, sündmuste puhvrit ja native-teste](https://github.com/Dennel04/smart-solutions-course/commit/5fc4fbf76653ef1a0e92037cb38ebd10012faf00). Seotud GitHubi commit'ide autor on `Nikikikl`; muid osalejaid selles dokumentatsioonitöös ei ole kinnitatud.
- Uuendasin `README.md`, [`docs/bom.md`](docs/bom.md) ja [`src/README.md`](src/README.md). Kinnitatud on LED-i ja draiveri valik ning nende ja radiaatori kanded ühises tabelis. Ost ja kättesaamine on kinnitamata. Ühises Atomi projektis on olemas tarkvaramudel ja native-testid; siinse töö käigus teste ei korratud ega riistvara kasutatud.
- TODO: elektriline sobivus, jahutus, relee parameetrid, UV ohutu väljalülitumine, füüsiline ühendus ning GPIO/ISR-i kontroll, eraldi tilgalogija ja päris mõõteandmed.

**14.11.2026: tilgaplaadi ja maketi mõõtmised ning fotod**

- Kasutaja edastas mõõdud ja fotod. Codex lisas tõendid reposse. Füüsilise töö osalejaid arhiiv ei täpsusta.
- Oranž V1 mõõtis 80 × 80 × 2,4 mm. Oranžil PLA-prototüübil pole klaasitugesid ega Gridfinity liidest. [V1 kaustas](tilgaplaat/v1/README.md) on kasutaja arhiivist pärit Fusioni, OpenSCADi, STEPi, STL-i ja 3MF-i failid.
- Laud 1: valge V2 ja kuus maketti valmis. Esimese V2 mõõdud on 167,5 × 167,5 mm ja jalgadega umbes 9 mm. Kolm mõõdetud klaasituge olid 0,6 mm kõrgused, plaat istus ruudustikus stabiilselt. Üks valge AtomS3R makett mõõtis 24 × 24 × 12,9 mm, ekraanisüvend oli umbes 1,2 mm ja makett istus stabiilselt. Kasutaja parandas algse kõrgusnäidu 12,8 mm väärtuseks 12,9 mm. Vahe CAD-i kõrgusega (12,8 mm) on +0,1 mm.
- Lisatud: [mõõteleht](tilgaplaat/measurements.md), [V1 prototüübi kirjeldus ja fotod](tilgaplaat/v1/README.md), [V2 ja makettide originaalfotod](tilgaplaat/photos/README.md). [Printimisjuhendis](tilgaplaat/PRINT.md) on mõlema laua seis.
- Laud 2 on viimase teate järgi veel printimisel. Teise V2 mõõdud ja fotod ning tilga-, kaamera-, UV- ja robotikatsed on TODO.

## Väljundid ja tulemused

- Nutikad Lahendused L3: klapi ja LED-i käsud, seaded/testnupud Atomi lehele ning alarmisündmus, mille peale jaam peatab roboti — **TODO**.
- 3D printimine L3: lubatud voolikupikkus klapi ja süstla vahel, põhjendatud anduri asukoht ning kaamera flantsinihke kontroll — **TODO**.
- Andmehõive L4: retsept ja kõverad, märgistatud normal / clogged / empty juhud, pildilt mõõdetud laigu suurused ja kohad `placement.csv-s` ning relee viivitus, põrge ja eluiga hilisemaks võrdluseks — **TODO**.

**KAARDISTA ISE, lõpus.**

- Git repo ja tag: **TODO: tag alles esitamisel; selles töös tag'i ei looda**.
- Lõplikud numbrid koos ühikutega: **TODO: päris mõõtmised**.
- Mida teeksime teisiti: **TODO: täita pärast füüsilist tööd**.
- Mida Labor 4 peab teadma: **TODO: täita kontrollitud Labor 3 tulemuste põhjal**.
