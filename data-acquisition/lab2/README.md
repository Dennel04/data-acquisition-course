# Andmehõive: Labor 2 — Op-amp, lihtne aga keeruline

See fail on Labori 2 tööleht ja arenduspäevik. Labori 1 kinnitatud lähteandmed on allpool koos allikatega. Labori 2 füüsiliste katsete ja komponentide saadavuse väljad täidetakse alles kontrollitud tõendite põhjal.

**Esimene kaitsmine: 29.10.2026, veebis.** Kuupäeva allikas: [õppejõu ametlik Labor 2 ülesanne](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLab%202%5D%20EST.md).

## Jagatud AtomS3R ja logija

Andmehõive ja Smart Solutions laborid kasutavad ühte füüsilist AtomS3R-i. Seadmes töötab korraga üks põhipüsivara: Andmehõive mõõtmis-püsivara teenib ADC lugemist ja CSV kogumist arvuti logijaga; Smart Solutions `NORMAL` teenib post-office/station tööd. Nende vahel liikumine nõuab kontrollitud üleslaadimist, varukoopia ja taastamisvõimaluse säilitamist ning ühendatud elektroonika kontrolli enne käivitamist.

XIAO ESP32S3 Sense on eraldi plaat oma kaamera-püsivaraga; see ei konkureeri Atomi püsivara kohaga.

Python logija toetab kohalikke Windowsi `COM1`, `COM3`, `COM10` jne porte ning macOS-i `/dev/cu.*` porte. Tarkvaratestid on olemas, kuid päris Windowsi riistvarakatse ei ole veel kinnitatud. See ei kinnita ADC ega rõhu mõõtetulemusi. Käivitamisjuhend: [Windows ja macOS](src/README.md#logija-windowsis-ja-macos-is).

## Eesmärk

Kavandada anduri ja ADC vahele analoogaste, mis nihutab ja skaleerib meeskonna tegeliku andurisignaali ADC jaoks sobivasse vahemikku. Seejärel võrrelda sama pumbaimpulssi toore (`raw`) ja astmega (`opamp`) signaaliga ning hinnata lahutusvõimet, müra, SNR-i ja pumbajuhtimist.

## Labor 1-st üle võetud kinnitatud lähteandmed

- Andur on `MPX5700AP`. Laboris 1 läks selle `Vout` otse AtomS3R viigule G5; vahel ei olnud jagurit, op-ampi ega filtrit. Allikad: `data-acquisition/lab1/docs/sensor_choice.md`, `data-acquisition/lab1/src/firmware/include/sensor.h`.
- ADC seadistus oli 12-bitine, `ADC_11db`, kaheksa lugemi keskmistamisega. Allikad: `data-acquisition/lab1/src/firmware/src/sensor.cpp`, `data-acquisition/lab1/src/firmware/include/sensor.h`.
- Labori 1 atmosfääripunktis mõõdeti anduri toiteks `5,00 V` ja väljundiks `0,85 V`. ADC keskmine oli `945,2` koodi; tarkvara teisendusteguriga `3,70 V / 4095` saadi `0,854 V`, mis erines multimeetrist ligikaudu `0,5%`. `3,70 V` on Labori 1 empiiriline koodist pingeks teisendamise tegur, mitte Labori 2 op-ampi mõõdetud toide ega ADC füüsilise sisendvahemiku piir. Allikas: `data-acquisition/lab1/docs/sensor_choice.md`.
- MPX5700AP andmelehe ülekandefunktsiooni ja Labori 1 teisendusteguri põhjal arvutati toore signaali lahutuseks ligikaudu `0,1405 kPa/kood` ehk `141 Pa/kood`. See on arvutatud väärtus, mitte eraldi rõhumõõtmine. Allikas: `data-acquisition/lab1/docs/sensor_choice.md`.
- Labori 1 logis mõõdeti `1002` telemeetriarida `10010 ms` jooksul ehk ligikaudu `100,1 Hz`. CSV veerud olid `t_ms,adc,p_kpa,pump`. Allikad: `data-acquisition/lab1/docs/sensor_choice.md`, `data-acquisition/lab1/src/python/logger.py`.
- Labori 1 lõplik pumbajuhtimise lähtejoon oli väljalülitus `−60 kPa`, sisselülitus `−40 kPa`, automaatsete taaskäivituste minimaalne väljalülitusaeg `15 s` ja ülempiir `4 käivitust/min`. Allikas: `data-acquisition/lab1/docs/pump_control.md`.
- Labori 1 ei mõõtnud Labor 2 jaoks vajalikku tegelikku `V_in,min` ja `V_in,max` paari kogu `−70…+110 kPa` vahemikus ega pooliku haarde eristamise aega. Need tuleb Laboris 2 mõõta.

## Nõutavad väljundid

- Arvutuskäik ja esimese ning parandatud astme mõõtetabelid: [`docs/opamp_design.md`](docs/opamp_design.md).
- Maksimi 22.10.26 potentsiomeetritega LM358N katseskeemi [paigutus ja ühendused](docs/lm358n_wiring_2026-10-22.md), koos muutmata Word-allikaga. See ei ole MPX5700AP rõhukalibratsioon ega G5 kogu sisendvahemiku ohutuskinnitus.
- Falstadi elav link, eksport ja skeemipilt: TODO: circuit design required.
- Kahe kanaliga ostsilloskoobipilt sisendist ja väljundist: TODO: real measurement required.
- 25.10 astme 2. versiooni muudatused, jaguriga CSV-de analüüs ja üleandmise seis: [`docs/opamp_v2_handoff_2026-10-25.md`](docs/opamp_v2_handoff_2026-10-25.md).
- Tellimuse tööleht: [`docs/bom.md`](docs/bom.md).
- Toore ja astmega pumbajuhtimise võrdlus: [`docs/pump_control.md`](docs/pump_control.md).
- `raw` ja `opamp` konfiguratsiooniga CSV-andmed: TODO: real measurement required.
- Võrdlev analüüs, spektrid, Pa/ADC samm ja SNR: toore signaali arvutuslik lähtejoon `141 Pa/kood`; op-amp võrdlus ja SNR: TODO: real measurement required.
- Mõõtmis-püsivara ja USB logija on ette valmistatud: [`src/README.md`](src/README.md). USB-only üleslaadimine, LCD ja `measure_stop` → `stopped` vastus on kinnitatud. G5, 12-bitine ADC, `raw/opamp` silt ning 100 Hz siht; tegelik ajastus ja kalibratsioon vajavad veel mõõtmist. CSV analüüsi juhend: [`notebooks/README.md`](notebooks/README.md). Pumba automaatjuhtimist ei ole.

## Kontrollnimekiri

- [ ] Labori 1 signaalist on arvutatud Pa ühe ADC sammu kohta (`141 Pa/kood`); tegelik sisendvahemik, kasutatud ADC vahemiku osa ja lõplikud astme nõuded: TODO: real measurement required.
- [ ] Falstadis on astme skeem, põhjendatud takistid ja müraallika katsed. Õppejõu näidisskeem on olemas; meeskonna skeem: TODO: real measurement required.
- [ ] Esimene aste on maketeerimisplaadil mõõdetud kolmes rõhupunktis. TODO: real measurement required.
- [ ] Sisend ja väljund on salvestatud korraga ostsilloskoobiga. TODO: real measurement required.
- [ ] Esimese versiooni mõlema otspunkti hälve on mõõdetud ja seletatud. TODO: real measurement required.
- [ ] Parandatud aste on uuesti arvutatud ja samades punktides mõõdetud. TODO: real measurement required.
- [ ] Sama pumbaimpulss on logitud konfiguratsioonides `raw` ja `opamp`. TODO: real measurement required.
- [ ] Spektrid on võrreldud samade telgede ja ühikutega. Labori 1 toores lähtefail on olemas; Labor 2 võrdlus: TODO: real measurement required.
- [ ] Pa ühe ADC sammu kohta ja SNR on arvutatud enne ning pärast astet. Raw-lähtejoon `141 Pa/kood`; op-amp ja SNR: TODO: real measurement required.
- [ ] Pumbajuhtimine on uue signaaliga mõõdetud ja võrreldud Labori 1 ajaloolise lähtejoonega. TODO: real measurement required.
- [ ] Pooliku haarde eristamise aeg on mõõdetud mõlema signaaliga. TODO: real measurement required.
- [ ] Füüsiline komponentide saadavus ja tellimisvajadus on kontrollitud failis `docs/bom.md`. TODO: real measurement required.
- [ ] Repo ja arenduspäevik on lõpetatud; esitamisel on lisatud tag `data-acquisition-lab2`.

## 1. Mis on puudu

Määrata meeskonna Labori 1 andmete põhjal:

- anduri tegelik sisendpinge vahemik: TODO: real measurement required;
- kasutatud ADC vahemiku osa: TODO: real measurement required;
- praegune arvutuslik lahutus: `141 Pa/kood` (`sensor_choice.md`; Labori 1 teisendustegur ja MPX5700AP andmelehe ülekandefunktsioon);
- lähtehüpotees: MPX5700AP otseühendatud signaal vajab nihutamist ja võimendamist; lõplik otsus kontrollitakse mõõdetud `V_in,min`, `V_in,max` ning ADC kasuliku vahemiku järgi;
- astme sihtvahemik ja vajalik võimendus: TODO: real measurement required.

Õppejõu MPX5700AP arvud `0,40…1,56 V` on andmelehe ja ülesande näide, mitte meeskonna mõõdetud otspunktid. Meeskond kasutas Laboris 1 sama andurit, kuid mõõdab Laboris 2 oma tegelikud otspunktid enne lõpliku astme valikut.

## 2. Aste, esimene versioon

1. Koostada sümboolne arvutus failis `docs/opamp_design.md`.
2. Valida topoloogia ja komponendid alles pärast tegeliku sisend- ning sihtvahemiku kinnitamist. TODO: real measurement required.
3. Koostada Falstadi simulatsioon koos eraldi ühismüra ja ühe sisendi müra katsega.
4. Kontrollida arvutatud väljundvahemikku simulatsioonis.
5. Ehitada aste maketeerimisplaadile ja mõõta tegelik toide ning kolm tööpunkti. TODO: real measurement required.
6. Salvestada kahe kanaliga ostsilloskoobipilt. TODO: real measurement required.

## 3. Parandus

- Arvutada mõlema otspunkti viga mõõdetud ja arvutatud pinge vahena. TODO: real measurement required.
- Kontrollida tegeliku toitepinge, op-ampi väljundulatuse ja ADC mittelineaarsuse mõju. TODO: real measurement required.
- Valida uus sihtvahemik ja arvutada võimendus, viitepinge ning takistid uuesti. TODO: real measurement required.
- Mõõta samad kolm punkti parandatud astmega ning hoida esimese versiooni tulemused kõrval. TODO: real measurement required.

## 4. Vahe

- Logida sama pumbaimpulss konfiguratsioonides `raw` ja `opamp` sama CSV-skeemiga. TODO: real measurement required.
- Võrrelda spektrit, signaalitaset, platoo müra standardhälvet, SNR-i ja Pa ühe ADC sammu kohta Labori 1 raw-lähtejoone ning Labor 2 sama protokolli andmetega. TODO: real measurement required.
- Võrrelda pumbajuhtimist olukordades `napp klaasil`, `napp õhus`, `voolik korgiga` ja `poolik haare`; ajalooline Labori 1 lähtejoon on failis `docs/pump_control.md`. Labor 2 kordus: TODO: real measurement required.
- Dokumenteerida kontrollriba, minimaalne väljalülitusaeg, käivitused minutis ja pooliku haarde eristamise aeg. TODO: real measurement required.
- Järeldus astme kasulikkuse kohta: TODO: real measurement required.

## Ohutus

- Lülita USB ja 5 V välja enne juhtmete muutmist.
- Mõõda astme väljund multimeetriga enne ADC-ga ühendamist ja pärast iga komponendimuudatust; ADC viik ei talu 5 V.
- Ühenda 24 V pumbakasti DO-liinid ainult siis, kui robot on keelatud ja kast vooluta.
- Jälgi pumba käivitusi minutis ja minimaalset väljalülitusaega; soojeneva kasti korral katkesta katse.
- Ära suuna lahtist survevoolikut kellegi poole.
- Katseta poolikut haaret laual, ilma käeta klaasi all.
- Hoia käed laualt eemal, kui MG400 on sisse lülitatud; esimene jooks aeglaselt ja hädastopp käeulatuses.
- Selles laboris ei joodeta.

## Hindamiskriteeriumid

| Kategooria | Punktid | Ettevalmistuse olek |
|---|---:|---|
| Tööfailid — mõlemad konfiguratsioonid, `config` veerg ja CSV-d | 5 | TODO: real measurement required |
| Analüüs — Pa/samm, spektrid, SNR ja pumbajuhtimise võrdlus | 5 | Labori 1 raw-lähtejoon olemas; TODO: real measurement required |
| Prototüüp — esimene ja parandatud aste mõõdetud ning uus juhtimine töötab | 5 | TODO: real measurement required |
| Dokumentatsioon — README, päevik, Falstad, `pump_control.md`, `bom.md`, AGENTS.md | 5 | ettevalmistamisel |
| **Kokku** | **20** | |

## Lõplikud repo väljundid

- `src/`: Atomi püsivara ja logija mõlema konfiguratsiooni jaoks.
- `data/`: kontrollitud `raw` ja `opamp` CSV-failid.
- `notebooks/`: spektrite, lahutusvõime ja SNR-i korratav analüüs.
- `docs/`: arvutused, Falstadi eksport ja pilt, skeemifoto, ostsilloskoobipilt, `pump_control.md` ja `bom.md`.
- `README.md`: kontrollnimekiri, otsused, tulemused ja arenduspäevik.

Kõik füüsilised väljundid: TODO: real measurement required.

### Arenduspäevik

**KAARDISTA ISE — päevik.** Üks sissekanne iga töösessiooni kohta, kirjutatud
iseendale, nii et inimene, kes seal ei olnud, saab aru. Sissekandeid lisatakse,
mitte ei muudeta.

**PP.KK.AA — kes olid kohal**
* Tegime:
* Juhtus (numbrid):
* Otsustasime, ja miks:
* Lahti järgmiseks korraks:
* Failid: (valikuline lisainfo)

**04.10.26 — Nikita**

- Tegime: valmistasime ette Labor 2 maketeerimisplaadi ja toitejuhtmed. Paigutasime füüsiliselt tuvastatud `LM358N` DIP-8 korpuse suure MB-102 tüüpi maketeerimisplaadi keskvahesse ridadele 26–29 ning kontrollisime korpuse täppi ja suunda. Ühendasime pin 4 rea sinise miinussiiniga ja pin 8 rea punase plussiiniga. Ühendasime AtomS3R `5V` plussiinile ning `G`/GND miinussiinile. Seadsime multimeetri alalispinge mõõtmiseks valmis. Ostsilloskoop oli klassis olemas, kuid me ei teinud sellega salvestatud Labor 2 mõõtmist.
- Juhtus (numbrid ja ühikud): vaadeldud suunas oli pin 1 poolel `e26`, pin 2 `e27`, pin 3 `e28`, pin 4 poolel `e29` ja pin 8 poolel `f26`. Nägime takistiribasid nimiväärtustega `10 kΩ`, `20 kΩ`, `6,8 kΩ`, `47 kΩ` ja `3,3 kΩ`; koguseid ei loendanud ning tegelikke takistusi ei mõõtnud. Algne ebaselge või vale AtomS3R päise ühenduskoht parandati enne toite ühendamist. Pärast parandust ei tehtud kinnitatud pingestatud mõõtmist ning sessiooni andmed ei kinnita, et op-ampi ahelat pingestati. Multimeetri näit `0,000 V` pingestamata ahela juures ei ole Labor 2 pingetulemus.
- Otsustasime, ja miks: jätsime Labor 1 anduriahela terveks, et `raw` konfiguratsioon säiliks hilisemaks kõrvutamiseks. Selle sessiooni tulemus on maketeerimisplaadi ja toitejuhtmete ettevalmistus; op-ampi ahela toidet ega väljundit ei loeta kontrollituks.
- Failid: `data-acquisition/lab2/README.md`, `data-acquisition/lab2/docs/bench_session.md`, `data-acquisition/lab2/docs/bom.md`.
- Lahti järgmiseks korraks: mõõta `V_sensor_supply` ja `V_opamp_supply`; mõõta `Vin` atmosfääril, täis imemisel ja täis puhumisel; mõõta kasutatavate takistite tegelikud väärtused; arvutada ja ehitada aste; mõõta `V_ref` ning `Vout` kolmes rõhupunktis enne AtomS3R ADC ühendamist.

**11.10.26 — Nikita, Maksim**

- Tegime: toitsime AtomS3R-i USB kaudu ja kasutasime UNI-T UT139C multimeetrit. Mõõtsime B5K ja B100K potentsiomeetrite takistuse. Ühendasime B5K ajutiseks reguleeritavaks sisendiks ning proovisime LM358N esimest kanalit pingejärgijana. Kontrollisime maketeerimisplaadi ridade ühendusi, toiteviikude pidevust ja ilmset lühist enne pingestamist. AtomS3R ADC-d ei ühendatud.
- Juhtus (numbrid ja ühikud): B5K takistus oli ligikaudu `4,9 kΩ` ja B100K takistus `94,8 kΩ`; B100K aktiivses katses ei kasutatud. LM358 pin 8 ja pin 4 vahel mõõtsime ligikaudu `5 V`. B5K liuguri pinge muutus ligikaudu `0…5,2 V` ning seadsime selle väärtusele `0,401 V`. Esimene väljundmõõtmine C26 ja D29 vahel andis `0 V`, kuigi ootasime ligikaudu `0,4 V`. Sisend C28 ja D29 vahel näitas eri hetkedel ligikaudu `3,9 V`, `5,222 V` ja `0,4 V`. Väljund C26 ja D29 vahel näitas hiljem ligikaudu `3,9 V` ka siis, kui sisend oli seatud tagasi ligikaudu `0,4 V`. Toite kontroll D29 ja H26 vahel andis ühe korra `0,027 V`, kordusmõõtmine `5,2 V`; mõlemad näidud jäävad dokumenti vastuoluna.
- Otsustasime, ja miks: pingejärgija ei käitunud õigesti ning vea põhjus jäi leidmata. `3,9 V` ja `5,2 V` ei tõenda ADC jaoks ohutut väljundit. Järgmine katse algab LM358 suuna, viigustiku ja kontaktide kontrollist ning ligikaudu `0,4 V` sisendi taastamisest. LM358 sisendit vahemikus `3,9…5,2 V` ei kasutata 5 V toitega kehtiva pingejärgija katsena, sest see võib jääda lubatud ühispingevahemikust välja.
- Failid: `data-acquisition/lab2/README.md`, `data-acquisition/lab2/docs/bench_session.md`, `data-acquisition/lab2/docs/bom.md`, `data-acquisition/lab2/docs/diagnostic_2026-10-11.md`.
- Lahti järgmiseks korraks: ehitada pingejärgija nullist uuesti, kinnitada korpuse suund ja kõik viigud, korrata `~0,4 V` sisendi ning väljundi mõõtmist ja leida vastuoluliste toitenäitude põhjus. MPX5700AP kolme rõhupunkti mõõtmised, ADC ühendamine ja Labor 2 astme kontroll jäävad TODO.

**22.10.26 — LM358N võimendusastme koostamine ja kontroll**

* **Tegime:** Koostasime maketeerimisplaadil LM358N operatsioonvõimendil põhineva katseskeemi. B5K potentsiomeetrit kasutasime reguleeritava sisendpinge tekitamiseks ning B100K potentsiomeetrit viitepinge seadmiseks. LM358N teine kanal töötas viitepinge puhvrina. Pärast väljundpinge kontrollimist ühendasime võimendi väljundi AtomS3R viiguga G5.
* **Juhtus (numbrid):** Toitepinge oli 5,00 V. Mõõdetud tagasisidetakistus oli 10,04 kΩ ning kolme järjestikuse takisti kogutakistus 6,51 kΩ. Ühes tööpunktis mõõtsime sisendpingeks 0,402 V, inverteerival sisendil 0,403 V, viitepingeks 0,520 V ja väljundpingeks 0,205 V. B5K reguleerimisel saime väljundpingeks 3,009 V.
* **Otsustasime, ja miks:** Jätkame katseskeemi kontrollimist enne tegeliku rõhuanduri ühendamist. Mõõdetud väljundpinge oli arvutatud väärtusele lähedane.
* **Lahti järgmiseks korraks:** MPX5700AP anduri mõõtmised, kolme rõhupunkti kontroll, ostsilloskoobimõõtmised, AtomS3R ADC programmi käivitamine ning CSV-andmete salvestamine.
* **Failid:** `README.md`, `docs/bench_session.md`, `docs/opamp_design.md`, `docs/bom.md`.

**23.10.26 — tarkvara ettevalmistuse mustand; osalejad kinnitab tudeng**

* Tegime: valmistasime ette eraldi Labor 2 mõõtmis-püsivara ja USB CSV-logija, kasutades Labor 1 ADC seadistust, kaheksa lugemi keskmist ja serial-pordi avamise võtet. Codex oli tarkvaraline abivahend, mitte füüsiliselt kohal olnud osaleja. Labor 1 lähtekoodi ega varasemaid päevikukirjeid ei muudetud.
* Juhtus (numbrid): kohalik build `SUCCESS`; RAM `22 804 / 327 680` baiti, flash `471 177 / 3 342 336` baiti. Sünteetilised tarkvaratestid `19/19`; tegelik 100 Hz, ADC, pinge ja rõhk ei ole selle tööga mõõdetud.
* Otsustasime, ja miks: iga jooks nõuab selget `raw/opamp` valikut; kalibreerimata pinge ja kPa jäävad CSV-s tühjaks. Multimeetri võrdlusnäit salvestatakse eraldi käsitsi sisestatud metaandmena. Võrku, pumpa ega robotit mõõtmisprogramm ei juhi.
* Lahti järgmiseks korraks: tudeng kinnitab osalejad ja kirje; eraldi luba üleslaadimiseks; LM358 ja MPX5700AP kogu väljundulatuse ning transientide elektriline kontroll enne G5 ühendamist; tegelik ajastus, kalibratsioon ja vähemalt 30 impulssi kummagi konfiguratsiooniga. Füüsilised tulemused, SNR ja pumbavõrdlus jäävad TODO.

**22.10.26 katse allikaviide — lisatud 23.10.26 (Maksim)**

* Tegime: sidusime olemasoleva 22.10 katsekande Maksimi Word-allika ja [eestikeelse koostamisjuhendiga](docs/lm358n_wiring_2026-10-22.md). Juhend sisaldab viigustikku, ühendusi ja arvutuse kontrolli; varasemad mõõteväärtused ja päevikukanded jäävad muutmata.
* Juhtus (numbrid): allikas kinnitab varem kirjapandud ühe tööpunkti tulemused ning B5K reguleerimisel saadud väljundnäidu. Uusi füüsilisi mõõtmisi selle dokumenteerimise käigus ei tehtud.
* Otsustasime, ja miks: säilitame Wordi muutmata algallikana. Põhijuhendisse ei kopeeri faili lõpus olevat vestlust. Potentsiomeetritega katse ei kinnita rõhku ega kogu väljundulatuse sobivust G5-le.
* Lahti järgmiseks korraks: MPX5700AP, elektriline vahemikukontroll, kalibratsioon, ostsillogrammid ja `raw/opamp` CSV-d. Kohalik AUTO-püsivara jääb eraldi, üles laadimata tööks.

**24.10.26 — LM358N katseskeemi ja ADC kontroll (Maksim)**

* Tegime: jätkasime LM358N katseskeemi kontrollimist. B5K potentsiomeeter tekitas reguleeritava sisendpinge ja B100K potentsiomeeter viitepinge. Mõõtsime multimeetriga sisend-, viite- ja väljundpinget. Kontrollisime AtomS3R GPIO5 ADC lugemist USB-ühenduse kaudu.
* Juhtus (numbrid): mõõtsime `Vin = 0,402 V`, `Vref = 0,526 V` ja `Vout = 0,190 V`. ADC testis saime 1001 lugemit ligikaudu 10 sekundi jooksul ehk umbes 100 Hz. ADC keskmine näit oli `188,43` koodi, minimaalne `182` ja maksimaalne `196`.
* Otsustasime, ja miks: katseskeem võimaldas mõõta väljundpinget ja lugeda ADC väärtusi. Tegemist oli potentsiomeetritega tehtud elektrilise testiga, mitte MPX5700AP rõhuanduri mõõtmisega. Rõhu kalibratsiooni, signaali-müra suhet ega võimendusastme lõplikku sobivust selle katse põhjal ei kinnita.
* Lahti järgmiseks korraks: ühendada MPX5700AP, mõõta kolm rõhupunkti, kontrollida väljundpinge ohutut vahemikku ning salvestada võrreldavad `raw` ja `opamp` CSV-andmed.

**25.10.2026 — MPX5700AP mõõtmised LM358N astmega Maksim**

Laboritöö käigus ühendasime rõhuanduri MPX5700AP operatsioonivõimendiga LM358N ning mõõtsime signaali AtomS3R-i ADC sisendi G5 kaudu. LM358N väljundi ja G5 sisendi vahel kasutasime kahest `10 kΩ` takistist koosnevat pingejagurit.

Salvestasime kolm mõõteseeriat, igaüks ligikaudu 10 sekundit ja 100 Hz sagedusega.

### CSV mõõtefailid

| Katse | Mõõtefail | Kirjeldus |
|---|---|---|
| Pump välja lülitatud | [opamp_pump_off_test.csv](data/opamp_pump_off_test.csv) | ADC näidu stabiilsuse kontroll |
| Vaakum | [opamp_vacum_test.csv](data/opamp_vacum_test.csv) | Vaakumi tekitamine ja pumba väljalülitamine |
| Ülerõhk | [opamp_pressure_test.csv](data/opamp_pressure_test.csv) | Rõhu tõus ja sellele järgnev vähenemine |

### Mõõtmistulemused

| Katse | Keskmine ADC | Minimaalne ADC | Maksimaalne ADC |
|---|---:|---:|---:|
| Pump välja lülitatud | 657,62 | 642 | 667 |
| Vaakum | 511,5 | 14 | 837 |
| Ülerõhk | 804,6 | 641 | 1175 |

Väljalülitatud pumba korral oli ADC näidu standardhälve ligikaudu `2,90` koodi. Vaakumkatses täheldasime pärast vaakumi vähenemist lühiajalist ADC näidu tõusu ligikaudu `805` koodini. Ülerõhukatses vähenes näit ligikaudu `1126 → 940 → 860` koodini, millele järgnes järsk langus.

Nende muutuste täpsed füüsikalised põhjused vajavad täiendavat kontrollimist.

**Piirangud:** rõhku ei ole veel kalibreeritud `kPa` ühikutesse. Samuti ei ole lõpetatud sama katse `raw` ja `opamp` signaalide võrdlust ega SNR-i arvutamist.


### Väljundid ja tulemused

**Väljundid**
* Lõplik op-amp aste koos arvutuse, skeemi ja kontrollitud komponentidega: TODO —
  real measurement required.
* Sama katse kontrollitud `raw` ja `opamp` andmestikud: TODO — real measurement
  required.
* Kalibratsioonikonstandid ja rõhuks teisendamine koos ühikutega: TODO — real
  measurement required.
* Toore ja op-amp signaaliga pumbajuhtimise võrdlus: TODO — real measurement
  required.
* Smart Solutions Lab 2 Atomi lehele vajalikud kalibratsiooni- ja rõhuväljad:
  TODO — real measurement required.

**KAARDISTA ISE, lõpus.**
* Git repo ja tag: TODO — lisada alles esitamisel.
* Numbrid, mille see labor andis, ühikutega: TODO — real measurement required.
* Mida me teeksime teisiti: TODO — complete after physical tests.
* Mida järgmine labor peaks enne alustamist teadma: TODO — complete after the
  op-amp, calibration and pump-control comparison are physically verified.





