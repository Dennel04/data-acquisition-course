# Andmehõive · Labor 4 — Masin, mis mõõdab ise

**Maht** 30 tundi · **Meeskond** 3 tudengit · **Hindamine** 20 punkti · **Ülesandel märgitud väljastamine** 18.11.2026 · **Tellimine** 27.11.2026 · **Esimene kaitsmine** 10.12.2026 veebis

Robot doseerib vaiku tilgaplaadile. Programm mõõdab tilga pildilt ja salvestab iga tsükli andmed koos rõhukõvera, foto, märgendi ja märgendi päritoluga. Mudel pakub sihtpindalale sobiva impulsi ning tagasiside korrigeerib impulssi järgmisel tsüklil. Kolme olukorraga andmestik läheb edasi Laborisse 5.

[Õppejõu täielik ülesanne](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLab%204%5D%20EST.md) · [Ametlik kokkuvõte](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLabor%204%20kokkuv%C3%B5te%5D%20EST.md)

15.11.2026 kontrollitud GitHubi `main` failide blob SHA-d on vastavalt `0c34e4df5b4536c23afba305cd6cf912676fe417` ja `449c6f6cad3bfc179c92bb8fade10e05bb43e3a0`. Kokkuvõtte viis tööosa, tähtajad ja hindamine kattuvad täistekstiga. Täistekst täpsustab ohutust, kontrollkatseid ja esitatavaid mõõtarve.

## Seis 15.11.2026

Valmis on katse- ja teostusplaanid, skeemi kavand ning päiserida. Kirje kuju on kooskõlastamisel. Lab 4 püsivara, automaatne doseerimine ja mõõtmine, mudeli sobitamine, riistvarakatsed ning andmebaasi ülekanne on ootel. [Tsükliandmete mall](data/cycles.csv) · [Teostusplaan](src/README.md)

| Sisend | Mida saab kasutada ja mis vajab kinnitust |
| --- | --- |
| Lab 1 füüsilised mõõtmised | MPX5700AP väljund atmosfääril 0,85 V, ajaloolised pumba piirid −60 ja −40 kPa, tavavõtmine 10/10. Kasuta pumba ja logimise lähtejoonena. Doseerimisrõhk ja uue süsteemi väljalülitumine tuleb eraldi mõõta. [Mõõteprotokollid](../../README.md#labor-1--rõhu-mõõtmine-ja-pumbajuhtimine) · [Spektrimärkmik](../lab1/notebooks/lab1_spectra.ipynb) |
| Lab 2 füüsilised ADC näidud | 25.10 protokollis on kolm varasema LM358N astme seeriat, 1001 lugemit igas seerias ja 10 ms ajatemplisamm. Vaakumiplatoo 14–21 ADC koodi näitab analoogastme küllastust ka siis, kui `adc_clipped=0`. 14.11 lisatud failides on 707, 1001 ja 1001 ADC lugemit. Failide DMM-metaandmed viitavad 25.10-le. Nende seeriate täpne skeem ja katsetingimused vajavad kinnitust ning mõõdetud rõhu väljad on tühjad. 15.11 koguti ümberehitatud astmega 30 + 30 `raw/opamp` impulssi ja kasutati andmelehe mudelil põhinevat kalibratsiooni. Lab 4 mõõteahela töövahemik vajab kohapeal kontrolli. [Lab 2 protokoll](../lab2/README.md#tõendid-ja-tulemused) · [14.11 andmed](../../README.md#labor-2--lm358n-katse-rõhuanduriga) |
| Lab 3 CAD ja 14.11 füüsilised tõendid | V1 on prinditud oranž 80 × 80 × 2,4 mm prototüüp. Esimene valge V2 plaat on 167,5 × 167,5 mm ja jalgadega umbes 9 mm. Kolm mõõdetud klaasituge on 0,6 mm. Üks valge AtomS3R makett on 24 × 24 × 12,9 mm. Teine V2 on prinditud ja mõõdetud. Plaadil mõõdeti 167,5 × 167,5 mm ja klaasitoe kõrguseks 0,6 mm. Klaas liikus ridade vahel. V3 on CAD-i ja prindifailina ette valmistatud. CAD, 3MF ja BGCODE kirjeldavad kavandit ja prindi ettevalmistust. [Mõõdud ning fotod](../lab3/tilgaplaat/measurements.md) · [CAD ja print](../lab3/README.md#nõutavad-väljundid) |
| Lab 3 tarkvara ja lahtised katsed | Ühises Atomi projektis on klapi ja UV olekumudel ning sündmuste puhver koos native-testidega. Relee viivitus, lühim tilk ja mähise vool, IRQ füüsiline reaktsiooniaeg, kaamera mõõteskaala, üle vaadatud tilgapildid, rõhukõverad ning kinnitatud retsept on puudu. Tilga-, paigutus- ja viivitus-CSV-des on ainult päised. [Tarkvaramudel](../lab3/src/README.md#olemasolev-tarkvaramudel) · [Andmed](../lab3/data/README.md) · [Retsept](../lab3/docs/recipe.md) |
| CAD Lab 3 füüsilised mõõtmised 15.11 | Vaadeldud klapikoost 68,84 g, tühi süstlakorpus 6,33 g ja tööriistakaamera 4,05 g. Mähise klemmidel mõõdeti 589,6 Ω ning loeti märgistus DC 24 V, 1 W. Klappi mõõtmisel ei pingestatud. Süstla kuivsobitus jätab hermeetilisuse ja vahetamise korduvuse lahtiseks. [CAD mõõteprotokoll](https://github.com/Dennel04/3d-printing-course/blob/main/3d-print/lab3/docs/measurements.md#m%C3%B5%C3%B5tmised-15112026) · [Integratsioon](docs/integration.md) |

## Kontrollnimekiri

Iga rida vastab õppejõu täisteksti ühele kohustuslikule punktile. Lisa valmimisel kuupäev, mõõtarvud ja tõendiviide.

| Nr | Ametlik nõue | Dokumentatsioon ja praegune seis |
| --- | --- | --- |
| 1 | Klappi lülitab relee asemel MOSFET. Kaitsediood on paigas ja vooluta on süstal atmosfääri ühendatud. | [IRLZ34N, paisu- ja allatõmbetakisti, diood](docs/mosfet.md#skeemi-kavand) · [Pneumaatika](docs/pump_control.md). Kavand valmis, koostamine ja ohutu oleku füüsiline kontroll ootel. |
| 2 | MOSFET-i lülitusaeg, lühim tilk ja mähise vool on mõõdetud ja relee tulemustega kõrvutatud. | [Mõõteplaan ja võrdlustabel](docs/mosfet.md#relee-ja-mosfet-i-võrdlus). Mõlema lüliti võrdlusmõõtmised, servad, põrge ja PWM-i katsed ootel. |
| 3 | Kirje kuju on Nutikate Lahendustega kokku lepitud ja `docs/record.md`-s kirjas. | [Kirje ettepanek](docs/record.md). Osapoolte kinnitus ootel. |
| 4 | Üks tsükkel läbib automaatselt doseerimise, pildistamise, mõõtmise ja kirjete salvestamise. | [Tsükli sammud ja aeg](docs/experiment_plan.md#automaatne-tsükkel). Klaasiringluse kontroll ja tervikkatse ootel. |
| 5 | Automaatne kaameramõõtmine on võrreldud Lab 3 üle vaadatud piltide ja sõltumatu tilgaplaadi kaalumisega. Mõlemad erinevused on protsentides. | [Kaks valideerimist](docs/measurement_validation.md). Lab 3 võrdluspildid, kaalumised ja veanäited ootel. |
| 6 | Pindala mudel arvestab impulssi, rõhku ja otsikut. Proovitud on vähemalt kaks mudelikuju ja süstla täidetus. Viga kontrollandmetel on protsentides. | [Regressioon ja kontrollandmed](docs/model_and_feedback.md#mudeli-sobitamine-ja-kontroll). Mõõteandmed, sobitamine ja mudelivalik ootel. |
| 7 | Tagasiside muudab impulssi mõõdetud pindala ja sihi järgi ning järgib impulsi ülempiiri. | [P-regulaator ja piirid](docs/model_and_feedback.md#tagasiside-ja-impulsi-piirid). Piiride mõõtmine, `k` katsed ja teostus ootel. |
| 8 | Kolm juhtimisviisi kõrvuti, 100 tilka igaühes. Süstlavahetuse järel on mõõdetud tilkade arv sihini. | [Kolme viisi võrdlus](docs/model_and_feedback.md#kolme-juhtimisviisi-võrdlus). 3 × 100 tilka ja taastumiskatsed ootel. |
| 9 | Vähemalt 300 päristsüklit tähistega `normal`, `blocked` või `empty`. Süstalt kaalutakse iga 25 tsükli järel. | [Juhuslikustatud katseseeria](docs/experiment_plan.md#labori-5-andmeseeria). Tsüklid, kaalud ja märgendid ootel. |
| 10 | Andmestik asub `data/cycles.csv`, `data/curves/`, `data/images/` ja Nutikate Lahenduste andmebaasis. | [CSV päis](data/cycles.csv) · [Kõverad](data/curves/) · [Pildid](data/images/) · [MQTT ja andmebaas](docs/integration.md#andmetee-ja-kordussaatmine). Failides on 0 mõõterida. Andmeedastus ja vähemalt 300 kirje kontroll andmebaasis on ootel. |
| 11 | 27.11 tellimus on `docs/bom.md`-s. | [Inventuur ja tellimuse tööleht](docs/bom.md). Riiuliseis, kogused ja Moodle'i kanne ootel. |
| 12 | Täidetud repo ja arenduspäevik. Esitamisel tag `data-acquisition-lab4`. | [Arenduspäevik](#arenduspäevik) · [Kaitsmine](#hindamine-ja-kaitsmine). Dokumentatsioon alustatud. Töötavad väljundid, katsetulemused ja esitamise tag ootel. |

## Tööjärjekord

1. **Kodus.** Vaata üle [kirje ettepanek](docs/record.md) ja kooskõlasta Nutikate Lahenduste ning CAD-i meeskonnaga tsüklivõti, väljad ja detailivahetuse jälgimine. Koosta võrguühenduseta valideerimis- ja analüüsitöölehed ning vaata üle MOSFET-i skeemi kavand ja andmelehed. [Analüüsiplaan](notebooks/README.md)
2. **Esimene laboripäev.** Tee inventuur olemasolevate osadega. Tuvasta klapp, mähis ja kaitsediood. Kontrolli Lab 2 andurikanalit ning lõpeta Lab 3 võrdlusmõõtmised ja retsept. Märgi 27.11 tellimusse kinnitatud puudujääk. [BOM](docs/bom.md)
3. **Laboris.** Võrdle releed ja MOSFET-i, kinnita õhutus, katkestus ja kaamera skaala ning teosta üks terviktsükkel. Valideeri pildimõõtmine kahe sõltumatu võrdlusega. Kogu juhuslikustatud pärisandmed, katseta mudelit ja tagasisidet ning kontrolli kirjete kohalejõudmist. [Katseplaan](docs/experiment_plan.md)

**KAARDISTA ISE.** Lisa töö käigus eesmärk ning kuupäevad, kasutatud vahendid ja allikad, iga tööosa mõõtarvud ühikute ja failiviitega ning lahtise töö põhjus. Lõpus lisa kaitsmisel kasutatav repo ja tag, tulemused, õpitu ning Labori 5 sisend koos andmestiku piirangutega.

## Ohutus

- Katkesta toide enne juhtmete muutmist. Klapi toide ei tohi jõuda Atomi viigule. Kasuta mähisel kontrollitud kaitsedioodi, mõõda MOSFET-i temperatuuri kontaktita ja jäta jootmine sellest laborist välja.
- Hoia sisselülitatud roboti tööala kätest vaba. Käivita uut jada esimest korda 20 % kiirusel. Kogu jooksu vältel peab ruumis olema inimene, kes ulatub hädastopini.
- Hoia 405 nm valgus katte all. Ühendatud LED-draiveri korral kannavad kõik laua ääres 405 nm kaitseprille. Kasuta lahtise süstlaga nitriilkindaid, kõvenda vaiguga plaadid enne äraviskamist ja hoia kõvenemata vaik kanalisatsioonist eemal.
- Ummistuskatse ajal kinnita suletud rõhu all olev süstal tööriista. [Pneumaatika ja katkestused](docs/pump_control.md)

## Hindamine ja kaitsmine

| Kategooria | Punktid | Kaitsmiseks vajalik |
| --- | ---: | --- |
| Tööfailid | 5 | Atomi MOSFET-i/PWM-i püsivara, tsükli- ja mõõtmisprogramm, mudel, tagasiside, CSV koos kõverate ja piltidega |
| Analüüs | 5 | Relee ja MOSFET kõrvuti, kaamerakontroll piltide ja kaaluga, mudeli kontrollviga, kolme viisi graafikud, seadete jaotus ja märgendite päritolu |
| Prototüüp | 5 | MOSFET lülitab klappi, vooluta on süstal atmosfääris, tsükkel töötab, tilk püsib sihis ja andmebaasis on vähemalt 300 kirjet |
| Dokumentatsioon | 5 | README, arenduspäevik, kirje kokkulepe, skeem pildi ja muudetava lähtefailiga, ostsillogrammid, ajakohane pumbajuhtimine, BOM ja juurkausta AGENTS.md |

Esita Git-repo link ja tag `data-acquisition-lab4`. 15 minuti jooksul tee kümme tsüklit ja näita kirjete jõudmist andmebaasi, relee ja MOSFET-i servi ostsilloskoobil, kolme viisi graafikuid, mudeli kontrollviga ning üht pilti koos mõõtmisvea käsitlusega. Ava arenduspäevik. Tag luuakse esitamisel.

## Arenduspäevik

Lisa iga töösessiooni järel uus sissekanne. Märgi kuupäev ja osalejad, tehtud töö, arvud koos ühikute ja failiviidetega, otsuste põhjused ning järgmine samm.

**15.11.2026 · dokumentatsiooni ettevalmistus (Codex)**

- Võrdlesin õppejõu täisteksti ja kokkuvõtet, sidusin 12 kontrollpunkti tööfailidega ning kontrollisin varasemate laborite mõõteandmeid ja seotud kursuste materjale.
- Valmistasin ette kirje ettepaneku ja päisega CSV. Lab 4 mõõteridu on 0. Järgmisena kinnitavad meeskonnad kirje kuju ja teevad inventuuri ning katsed.
