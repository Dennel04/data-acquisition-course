# Andmehõive: Labor 2 — Op-amp, lihtne aga keeruline

See fail on Labori 2 tööleht ja arenduspäevik. Labori 1 kinnitatud lähteandmed on allpool koos allikatega. Labori 2 füüsiliste katsete ja komponentide saadavuse väljad täidetakse alles kontrollitud tõendite põhjal.

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
- Falstadi elav link, eksport ja skeemipilt: TODO: circuit design required.
- Kahe kanaliga ostsilloskoobipilt sisendist ja väljundist: TODO: real measurement required.
- Tellimuse tööleht: [`docs/bom.md`](docs/bom.md).
- Toore ja astmega pumbajuhtimise võrdlus: [`docs/pump_control.md`](docs/pump_control.md).
- `raw` ja `opamp` konfiguratsiooniga CSV-andmed: TODO: real measurement required.
- Võrdlev analüüs, spektrid, Pa/ADC samm ja SNR: toore signaali arvutuslik lähtejoon `141 Pa/kood`; op-amp võrdlus ja SNR: TODO: real measurement required.
- Atomi püsivara ja logija muudatused: kavandatud failis [`src/README.md`](src/README.md).

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

## Arenduspäevik

Lisa iga tegeliku töösessiooni kohta uus sissekanne. Ära kirjuta varasemaid sissekandeid ümber.

**PP.KK.AA — osalejad**

- Tegime:
- Juhtus (numbrid ja ühikud):
- Otsustasime, ja miks:
- Failid:
- Lahti järgmiseks korraks:
