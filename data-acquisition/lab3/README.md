# Andmehõive: Labor 3 — Tilk ja katkestus

See fail on Labori 3 tööleht. Labori 3 füüsiline töö ei ole veel alanud ja kõik füüsilised tulemused jäävad kuni päris mõõtmiseni märgendiga **TODO**. Laborite 1 ja 2 väärtusi võib siia üle tuua ainult pärast nende kontrollimist vastavate laborite failidest.

**Töömaht:** 30 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 28.10.26 | **Tellimise kuupäev:** 06.11.26 | **Esimene kaitsmine:** 17.11.26, veebis

## Eesmärk

Sama pump doseerib nüüd ka vaiku läbi süstla. 3/2 solenoidklapp valib iminapa ja süstla haru vahel ning klappi juhib Atom. Laboris määratakse mõõtmiste põhjal doseerimisretsept ning tuvastatakse kinnine otsik ja tühi süstal. Keskmes on rõhu tuletis, müra ja filtreerimine ning kiire riistvarakatkestus.

## Laboritest 1 ja 2 vajalikud sisendid

Õppejõu ülesanne eeldab andurit koos Labori 2 astmega, ligikaudu 100 Hz logija kontseptsiooni, pumbajuhtimise riba ja pooliku haarde logisid. Meeskonna tegelik valmidus ning väärtused tuleb enne kasutamist allikatest kontrollida.

- Labori 2 lõplik konditsioneeritud anduriahel: **TODO: kontrollida Labori 2 tulemustest**.
- Labori 2 lõplik CSV-vorming: **TODO: kontrollida Labori 2 tulemustest**.
- Labori 2 pooliku haarde logid: **TODO: leida ja kontrollida päris failid**.
- Labori 2 lõplikud pumbajuhtimise väärtused: **TODO: kontrollida `../lab2/docs/pump_control.md` failist**.
- Tegelik kasutatav diskreetimissagedus: **TODO: mõõta ajatemplitest**.
- Vajalikud filtreeritud ja op-amp tulemused: **TODO: kontrollida Labori 2 analüüsist**.

## Nõutavad väljundid

- [`data/drops.csv`](data/drops.csv) ja iga tilga sama ID-ga rõhukõver failis `data/`.
- [`docs/recipe.md`](docs/recipe.md), [`docs/latency.csv`](docs/latency.csv), [`docs/bom.md`](docs/bom.md) ja uuendatud [`docs/pump_control.md`](docs/pump_control.md).
- Falstadi elav link, eksport ja ekraanipilt kaustas `docs/falstad/`.
- Ostsilloskoobi tõendid kaustas `docs/scope/`.
- Atomi püsivara ja arvuti logija kaustas `src/`.
- Korratav analüüs kaustas `notebooks/`.

## Kontrollnimekiri

- [ ] Klapp lülitab Atomi käsu peale; vooluta ohutu asend on iminapp ja see on füüsiliselt kontrollitud.
- [ ] Impulssi juhib riistvarataimer.
- [ ] Viis kästud impulsi pikkust on võrreldud ostsilloskoobiga mõõdetud pikkustega.
- [ ] UV LED-i juhib Atom ja LED kustub alati automaatselt.
- [ ] Anduri asukoht on valitud ja põhjendatud.
- [ ] Vähemalt viis impulsi pikkust × kümme tilka; iga tilk mõõdetud ja rõhukõver salvestatud.
- [ ] `data/drops.csv` on päris mõõtmistega täidetud.
- [ ] Teine muutuja — teine otsik või teine rõhk — on katsetatud kolme impulsi pikkusega.
- [ ] Retsept on mõõtmiste põhjal failis `docs/recipe.md`.
- [ ] Toores ja filtreeritud kalle on võrreldud.
- [ ] Signaali ja tuletise spektrid on võrreldud.
- [ ] Filter on valitud arvulise müra ja viivituse võrdluse põhjal.
- [ ] Sama kaldeanalüüs on tehtud Labori 2 pooliku haarde logil.
- [ ] Komparaator on Falstadis kontrollitud.
- [ ] Komparaator on maketeerimisplaadil kontrollitud.
- [ ] Atomi katkestus viib klapi ohutusse olekusse, lukustab alarmi ja väljastab sündmuse.
- [ ] Viivitus on mõõdetud kümme korda katkestusega ja kümme korda katkestuseta.
- [ ] Kinnine otsik on katsetatud 10 korda.
- [ ] Tühi süstal on katsetatud 10 korda.
- [ ] Tavalise tilga valehäireid on kontrollitud 30 katsel.
- [ ] Tellimus on dokumenteeritud failis `docs/bom.md` hiljemalt 06.11.26.
- [ ] Repo ja arenduspäevik on lõpetatud ning esitamisel on tag `data-acquisition-lab3`.

## 1. Klapp ja impulss

Ettevalmistatud tulevane töö:

1. Lugeda enne ühendamist klapi korpuselt nimipinge. **TODO: päris märgistus**.
2. Ühendada Atomi ja klapi vahele sobiv MOSFET-moodul; klapi toidet ja Atomi loogikatoidet mitte segi ajada.
3. Kontrollida kaitsedioodi olemasolu ja sobivust enne lülitamist.
4. Kontrollida füüsiliselt, et vooluta klapp jätab pumba iminapa harule, mitte süstlale.
5. Teostada klapi impulss riistvarataimeriga, mitte põhitsükli ajastusega.
6. Mõõta viis impulsi pikkust, igaühte kümme korda, ning arvutada keskmine ja kõikumine.
7. Mõõta rõhukõveralt klapi tegelik avanemisviivitus.
8. Valida anduri asukoht ja kirjeldada, mida selle valikuga võidetakse ning millest loobutakse.
9. Juhtida 405 nm LED-i draiveri kaudu ja tagada taimeriga automaatne väljalülitus.

- Klapi ühendusskeem pildina: **TODO: lisada pärast skeemi koostamist**.
- Süstlaharu rõhk, kui Atom on vooluta: **TODO: mõõta, väärtust mitte oletada**.
- Vooluta ohutu oleku tegelik mõõtetõend: **TODO: lisada pärast füüsilist kontrolli**.

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

## 2. Tilga suurus

- Hoida rõhk ühe katseseeria ajal konstantsena; väärtus **TODO: määrata päris mõõtmisega**.
- Alustada õppejõu soovitusel keskmisest otsikust; see ei ole veel meeskonna valik.
- Katsetada vähemalt viit impulsi pikkust ja teha iga pikkusega kümme tilka.
- Mõõta iga tilga läbimõõt millimeetrites.
- Mõõta mass milligrammides ainult siis, kui olemas on 0,01 g lahutusega kaal.
- Siduda iga tilga ID sama ID-ga rõhukõvera failiga.
- Hinnata eraldi, kas tilga suuruse ja impulsi kestuse seos on lineaarne; mittelineaarsuse korral määrata pärisandmetest, kus seos paindub ja miks.
- Arvutada suhteline kõikumine: `standardhälve / keskmine`.
- Hoida lineaarsuse hinnang eraldi sama impulsi korduskatsete varieeruvusest (`standardhälve / keskmine`).
- Kontrollida eraldi esimest tilka pärast pausi.
- Muuta teise muutujana kas otsikut või rõhku ja katsetada kolme impulsi pikkust.
- Teha lõplik katse päris klaasi ja vaiguga ning mõõta kõvenemist.
- Täita retsept alles pärast mõõtmisi ja päris katset.

Kõik tilkade mõõtmed, massid, rõhud, ajad ja otsused: **TODO: füüsiline töö**.

## 3. Filter ja tuletis

Õppejõu lähtevalem 100 Hz juhu jaoks:

```text
dP/dt = (P_now - P_previous) / 10 ms
```

`10 ms` eeldab kavandatud 100 Hz diskreetimist. Meeskonna pärisandmetes tuleb kasutada ja kontrollida tegelikku ajatemplite vahet, mitte oletada püsivat 10 ms sammu.

Analüüsi TODO-d:

- arvutada toores tuletis;
- koostada rõhusignaali ja tuletise spektrid;
- selgitada tuletise sagedusvõimendust teguriga `2πf`;
- katsetada libisevat keskmist;
- katsetada mediaanfiltrit;
- võrrelda filtreid tuletise müra arvulise näidu järgi;
- võrrelda filtreid viivituse arvulise näidu järgi;
- valida filter ainult nende arvude põhjal;
- rakendada valitud kalde tunnust Labori 2 päris pooliku haarde logile;
- võrrelda tavalist tilka, kinnist otsikut ja tühja süstalt;
- valida tuvastustunnus pärisandmetest.

Filtrit ega läve selles ettevalmistuses ei valita: **TODO: päris andmed**.

## 4. Katkestus

1. Koostada komparaator esmalt Falstadis.
2. Kasutada katsesisenditena tavalist tilka, kinnist otsikut ja müraga tavalist tilka.
3. Lisada hüsterees ehk Schmitti triger; läved ja takistid **TODO: arvutada pärisandmetest**.
4. Mõõta komparaatori väljund enne Atomi ühendamist ja kinnitada, et see ei ületa 3,3 V.
5. Hoida katkestusteenindus minimaalne: viia klapp kohe ohutusse olekusse ja seada alarmilipp.
6. Uuendada ekraani ning saata USB sündmus hiljem põhitsüklis.
7. Hoida alarm lukus kuni `clear` käsuni.
8. Võrrelda katkestuse ja põhitsükli küsitluse viivitust.
9. Korrata võrdlust koormatud põhitsükliga.
10. Teha lõplikud kinnise otsiku, tühja süstla ja tavalise tilga valehäirekatsed.

Tühja süstla tulevane loogika:

- normaalse tilga oodatav rõhuplatoo: **TODO: määrata päris normaalse tilga andmetest**;
- lubatud ajavahemik platooni jõudmiseks: **TODO: määrata pärisandmetest**;
- kui rõhk ei jõua lubatud aja jooksul oodatud platooni, lukustada tühja süstla alarm;
- läve ega aega ei määrata enne päris mõõtmisi.

Viivituse tulemused ja otsus:

- katkestuse keskmine viivitus: **TODO: ms**;
- katkestuse halvim viivitus: **TODO: ms**;
- polling'u keskmine viivitus: **TODO: ms**;
- polling'u halvim viivitus: **TODO: ms**;
- polling'u viivitus põhitsükli koormusega: **TODO: ms, keskmine ja halvim**;
- katkestuslahenduse arendusaeg: **TODO**;
- polling'u lahenduse arendusaeg: **TODO**;
- lõplik valitud meetod ja ühe lause põhjendus: **TODO: valida mõõtetulemuste põhjal**.

Kõik läved, komponendiväärtused, viivitused ja tabamismäärad: **TODO: simulatsioon ja päris mõõtmised**.

## Ohutus

- 405 nm LED-i töötamise ajal kannavad kõik laua ääres 405 nm kaitseprille; LED-i ei vaadata.
- UV lamp suunatakse laua poole ning LED on vooluta olekus väljas.
- Kõvenemata vaiguga töötamisel kasutatakse nitriilkindaid.
- Mahaläinud vaik puhastatakse isopropanooli ja paberiga; saastunud paber kõvendatakse enne jäätmesse panemist.
- Kõvenemata vaiku ei valata kunagi kraanikaussi.
- UV LED-i ei suunata otsikule.
- Kinnise otsikuga süstal on rõhu all suletud anum.
- Ummistuskatse ajal kinnitatakse süstal hoidikusse või statiivi.
- Kuni katkestuskaitse on kontrollitud, hoiab inimene ummistuskatse ajal kätt pumba lüliti juures.
- Enne süstla eemaldamist lastakse rõhk klapi kaudu välja.
- Otsikul on kork peal, kui ei doseerita.
- Klapi mähis vajab kaitsedioodi.
- Klapi toidet ja Atomi loogikatoidet ei tohi segi ajada.
- ADC- ja katkestusviigud ei talu 5 V.
- Komparaatori väljund mõõdetakse enne Atomi ühendamist.
- USB ja toide lülitatakse enne ümberjuhtmestamist välja.
- Pumbakast on 24 V.
- Lahtist +110 kPa voolikut ei suunata inimeste poole.
- MG400 töötamise ajal hoitakse käed laualt eemal; esimene uus liikumine tehakse aeglaselt, hädastopp käeulatuses.
- Esimesed tilgamõõtmised tehakse laual, mitte roboti otsas.
- Selles laboris ei joodeta.

## Hindamiskriteeriumid

| Kategooria | Punktid | Ettevalmistuse olek |
|---|---:|---|
| Tööfailid — Atomi püsivara, logija, `drops.csv`, rõhukõverad ja analüüsi märkmik | 5 | Struktuur valmis; **TODO: kood ja päris andmed** |
| Analüüs — impulss, tilga suurus, kalded, spektrid, filtri viivitus ning katkestuse võrdlus | 5 | **TODO: päris mõõtmised ja analüüs** |
| Prototüüp — ohutu klapp, toimiv retsept ning kinnise/tühja olukorra alarm | 5 | **TODO: füüsiline prototüüp ja katsed** |
| Dokumentatsioon — README, päevik, retsept, viivitus, Falstad, pumbajuhtimine, BOM ja AGENTS.md | 5 | Mallid valmis; **TODO: tulemused ja tõendid** |
| **Kokku** | **20** | **TODO: Labor 3 ei ole füüsiliselt alustatud** |

## Arenduspäevik

Lisa ainult tegeliku töösessiooni järel uus sissekanne; olemasolevaid sissekandeid hiljem ei muudeta.

**PP.KK.AA — osalejad**

- Tegime:
- Juhtus (numbrid ja ühikud):
- Otsustasime, ja miks:
- Failid:
- Lahti järgmiseks korraks:

## Väljundid ja tulemused

- Nutikad Lahendused L3: klapi ja LED-i käsud, seaded ning testnupud Atomi lehele; alarmisündmus, mille peale jaam peatab roboti.
- 3D printimine L3: klapi ja süstla vahel lubatud vooliku pikkus ning valitud anduri asukoht.
- Andmehõive L4: retsept ja rõhukõverad ning kolm märgistatud olukorda — tavaline, kinnine ja tühi.

- Git repo ja tag: **TODO: tag lisatakse alles esitamisel; `data-acquisition-lab3` ei ole veel loodud**.
- Lõplikud numbrid koos ühikutega: **TODO: päris mõõtmised**.
- Mida teeksime teisiti: **TODO: täita pärast füüsilist tööd**.
- Mida Labor 4 peab teadma: **TODO: täita kontrollitud Labor 3 tulemuste põhjal**.
