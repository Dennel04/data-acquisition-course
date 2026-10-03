# Andmehõive: Labor 2 — Op-amp, lihtne aga keeruline

See fail on Labori 2 tööleht ja arenduspäevik. Füüsiliste katsete, Labori 1 lähteandmete ja komponentide saadavuse väljad täidetakse alles kontrollitud tõendite põhjal.

## Eesmärk

Kavandada anduri ja ADC vahele analoogaste, mis nihutab ja skaleerib meeskonna tegeliku andurisignaali ADC jaoks sobivasse vahemikku. Seejärel võrrelda sama pumbaimpulssi toore (`raw`) ja astmega (`opamp`) signaaliga ning hinnata lahutusvõimet, müra, SNR-i ja pumbajuhtimist.

## Nõutavad väljundid

- Arvutuskäik ja esimese ning parandatud astme mõõtetabelid: [`docs/opamp_design.md`](docs/opamp_design.md).
- Falstadi elav link, eksport ja skeemipilt: TODO: circuit design required.
- Kahe kanaliga ostsilloskoobipilt sisendist ja väljundist: TODO: real measurement required.
- Tellimuse tööleht: [`docs/bom.md`](docs/bom.md).
- Toore ja astmega pumbajuhtimise võrdlus: [`docs/pump_control.md`](docs/pump_control.md).
- `raw` ja `opamp` konfiguratsiooniga CSV-andmed: TODO: real measurement required.
- Võrdlev analüüs, spektrid, Pa/ADC samm ja SNR: TODO: Lab 1 data required; TODO: real measurement required.
- Atomi püsivara ja logija muudatused: kavandatud failis [`src/README.md`](src/README.md).

## Kontrollnimekiri

- [ ] Labori 1 signaalist on arvutatud Pa ühe ADC sammu kohta, kasutatud ADC vahemik ja astme nõuded. TODO: Lab 1 data required.
- [ ] Falstadis on astme skeem, põhjendatud takistid ja müraallika katsed. TODO: Lab 1 data required.
- [ ] Esimene aste on maketeerimisplaadil mõõdetud kolmes rõhupunktis. TODO: real measurement required.
- [ ] Sisend ja väljund on salvestatud korraga ostsilloskoobiga. TODO: real measurement required.
- [ ] Esimese versiooni mõlema otspunkti hälve on mõõdetud ja seletatud. TODO: real measurement required.
- [ ] Parandatud aste on uuesti arvutatud ja samades punktides mõõdetud. TODO: Lab 1 data required; TODO: real measurement required.
- [ ] Sama pumbaimpulss on logitud konfiguratsioonides `raw` ja `opamp`. TODO: real measurement required.
- [ ] Spektrid on võrreldud samade telgede ja ühikutega. TODO: Lab 1 data required; TODO: real measurement required.
- [ ] Pa ühe ADC sammu kohta ja SNR on arvutatud enne ning pärast astet. TODO: Lab 1 data required; TODO: real measurement required.
- [ ] Pumbajuhtimine on uue signaaliga mõõdetud ja võrreldud. TODO: Lab 1 data required; TODO: real measurement required.
- [ ] Pooliku haarde eristamise aeg on mõõdetud mõlema signaaliga. TODO: real measurement required.
- [ ] Füüsiline komponentide saadavus ja tellimisvajadus on kontrollitud failis `docs/bom.md`. TODO: real measurement required.
- [ ] Repo ja arenduspäevik on lõpetatud; esitamisel on lisatud tag `data-acquisition-lab2`.

## 1. Mis on puudu

Määrata meeskonna Labori 1 andmete põhjal:

- anduri tegelik sisendpinge vahemik: TODO: Lab 1 data required;
- kasutatud ADC vahemiku osa: TODO: Lab 1 data required;
- praegune Pa ühe ADC sammu kohta: TODO: Lab 1 data required;
- kas vaja on võimendust ja nihutamist või pingejagurit: TODO: Lab 1 data required;
- astme sihtvahemik ja vajalik võimendus: TODO: Lab 1 data required.

Õppejõu MPX5700AP arvud on näide, mitte meeskonna mõõtetulemus. Meeskonna arvutused tehakse kasutatud anduri, selle kontrollitud andmelehe ja Labori 1 andmete järgi.

## 2. Aste, esimene versioon

1. Koostada sümboolne arvutus failis `docs/opamp_design.md`.
2. Valida topoloogia ja komponendid alles pärast sisend- ning sihtvahemiku kinnitamist. TODO: Lab 1 data required.
3. Koostada Falstadi simulatsioon koos eraldi ühismüra ja ühe sisendi müra katsega.
4. Kontrollida arvutatud väljundvahemikku simulatsioonis.
5. Ehitada aste maketeerimisplaadile ja mõõta tegelik toide ning kolm tööpunkti. TODO: real measurement required.
6. Salvestada kahe kanaliga ostsilloskoobipilt. TODO: real measurement required.

## 3. Parandus

- Arvutada mõlema otspunkti viga mõõdetud ja arvutatud pinge vahena. TODO: real measurement required.
- Kontrollida tegeliku toitepinge, op-ampi väljundulatuse ja ADC mittelineaarsuse mõju. TODO: real measurement required.
- Valida uus sihtvahemik ja arvutada võimendus, viitepinge ning takistid uuesti. TODO: Lab 1 data required; TODO: real measurement required.
- Mõõta samad kolm punkti parandatud astmega ning hoida esimese versiooni tulemused kõrval. TODO: real measurement required.

## 4. Vahe

- Logida sama pumbaimpulss konfiguratsioonides `raw` ja `opamp` sama CSV-skeemiga. TODO: real measurement required.
- Võrrelda spektrit, signaalitaset, platoo müra standardhälvet, SNR-i ja Pa ühe ADC sammu kohta. TODO: Lab 1 data required; TODO: real measurement required.
- Võrrelda pumbajuhtimist olukordades `napp klaasil`, `napp õhus`, `voolik korgiga` ja `poolik haare`. TODO: Lab 1 data required; TODO: real measurement required.
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
| Analüüs — Pa/samm, spektrid, SNR ja pumbajuhtimise võrdlus | 5 | TODO: Lab 1 data required; TODO: real measurement required |
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
