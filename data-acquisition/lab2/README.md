# Andmehõive: Labor 2 — Op-amp, lihtne aga keeruline

## Ülevaade

MPX5700AP rõhuandur muudab rõhu pingeks. AtomS3R-i analoog-digitaalmuundur (ADC) loeb pinget G5 viigult ja annab selle kohta ADC koodi. Arvutis salvestab Python-logija koodi koos ajatempli ja valitud ühendusega CSV-faili.

`raw` tähistab otse andurilt loetud signaali, `opamp` LM358N astme kaudu loetud signaali. Võimendus aitab rõhumuutusel kasutada rohkem ADC koode. Viitepinge abil nihutatakse väljundivahemikku, et signaal mahuks ADC kasulikku ossa. Kui aste jõuab oma väljundipiirini, kaob osa rõhumuutuse infost. Võimendus tõstab ka sisendmüra, mistõttu tuleb mõlemat ühendust katsetada sama pumbaimpulsiga.

**Esimene kaitsmine oli ülesandes määratud 29.10.2026 veebis.** [Õppejõu ametlik Labor 2 ülesanne](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLab%202%5D%20EST.md).

## Praegune seis (13.11.2026)

| Valdkond | Seis |
|---|---|
| Füüsilised katsed | Maksimi 22. ja 24.10 potentsiomeetrikatsed ning 25.10 kolm MPX5700AP mõõteseeriat on dokumenteeritud. [Tõendid ja tulemused](#tõendid-ja-tulemused). |
| Tarkvara | 45 kohalikku testi läbisid kontrolli, sh AUTO loogika imiteeritud ADC/LCD/USB-ga, logija ja CSV analüüs. `atoms3r` ehitus õnnestus 07.11 dokumenteeritud kontrollis. [Tarkvarakontroll](src/README.md#tarkvarakontroll). |
| Kontrollimata riistvara | Raimo andis pärast 25.10 katseid Maksimile muudetud katseskeemi. Selle ühendused, kolm rõhupunkti ja G5 pingeulatus koos siiretega vajavad kontrolli. [Üleandmine](docs/opamp_v2_handoff_2026-10-25.md). |
| Kontrollimata püsivara | Varasemal versioonil töötasid ainult USB-ga ühendatud Atomi LCD ja `measure_stop` → `stopped`. Uuema AUTO-versiooni üleslaadimine, töö päris seadmel ja 100 Hz ajastus vajavad eraldi kinnitust. [AUTO kasutus](src/README.md#adc-vaatamine-ilma-logijata). |
| Lahtised tulemused | Rõhukalibratsioon, võrreldavad `raw`/`opamp` jooksud, ostsillogrammid, Pa/ADC samm, spektrid, signaali-müra suhe (SNR) ja pumbajuhtimise võrdlus. [Järgmised sammud](#puuduvad-katsed-ja-järgmised-sammud). |

## Tõendid ja tulemused

| Kuupäev | Maksimi katse | Mõõdetud tulemus | Tõend |
|---|---|---|---|
| 22.10.2026 | LM358N elektriline kontroll potentsiomeetritega | Katseskeemi toide **5,00 V**, `Vin = 0,402 V`, `Vref = 0,520 V`, `Vout = 0,205 V`. Sisendit muutes mõõdeti ka `Vout = 3,009 V`. | [Mõõtetabel](docs/bench_session.md#22102026--lm358n-katseskeemi-mõõtmised-maksim) · [Ühendused ja arvutus](docs/lm358n_wiring_2026-10-22.md#6-mõõtmine-ja-arvutuse-kontroll) |
| 24.10.2026 | LM358N ja G5 kontroll potentsiomeetritega | `Vin = 0,402 V`, `Vref = 0,526 V`, `Vout = 0,190 V`. Umbes 10 sekundiga 1001 lugemit, keskmine 188,43 ja vahemik 182–196 ADC koodi. | [Mõõteprotokoll](docs/bench_session.md#24102026--lm358n-katseskeemi-ja-atoms3r-adc-kontroll-maksim) |
| 25.10.2026 | MPX5700AP, LM358N ja 10 kΩ / 10 kΩ jagur | Kolm `opamp` seeriat enne skeemi ümberehitust. G5 multimeetrinäit seiskunud pumbaga 0,592 V ja suurim täheldatud näit töötava pumbaga 0,952 V. | [Mõõteprotokoll](docs/bench_session.md#25102026--mpx5700ap-rõhuanduri-lm358n-võimendusastme-ja-atoms3r-adc-mõõtmised-maksim) · [Hilisem üleandmine](docs/opamp_v2_handoff_2026-10-25.md) |

22.10 toite- ja väljundnäidud kehtivad tolle katseskeemi mõõdetud tööpunktidele. 25.10 G5 multimeetrinäidud on eraldi vaatlused. Lõpliku astme toite ja G5 kogu pingeulatuse, kaasa arvatud siirded, peab mõõtma valmis skeemil.

| 25.10 katse ja algne CSV | Lugemeid | Keskmine (ADC koodi) | Min–max (ADC koodi) | Valimi standardhälve (ADC koodi) |
|---|---:|---:|---:|---:|
| [Pump väljas](data/opamp_pump_off_test.csv) | 1001 | 657,6234 | 642–667 | 2,90 |
| [Vaakum](data/opamp_vacum_test.csv) | 1001 | 511,5405 | 14–837 | 306,76 |
| [Ülerõhk](data/opamp_pressure_test.csv) | 1001 | 804,5984 | 641–1175 | 185,60 |

Kõigis kolmes failis on salvestatud ajatemplite vahe 10 ms (100 Hz) ja esimese ning viimase lugemi vahe 10,000 s. See kirjeldab 25.10 salvestatud seeriaid. Uuema AUTO-püsivara füüsilist ajastust tuleb mõõta eraldi.

Vaakumikatse graafikul püsib signaal alumisel platool **14–21 ADC koodi**. See näitab varasema analoogastme alumise otsa küllastust. `adc_clipped=0` ütleb ainult, et ADC kood ei olnud 0 ega 4095. Platool on väike hajuvus, sest aste ei järgi seal sisendi muutust. Vaakumi ja ülerõhu terve seeria standardhälve sisaldab ka signaali muutusi. Seisva pumba 2,90 koodi kirjeldab selle seeria kõikumist. [Küllastuse käsitlus](docs/opamp_v2_handoff_2026-10-25.md#1-mida-jaguriga-csv-d-näitasid).

`p_kpa`, `voltage_v` ja `pump` on CSV-des tühjad. `dmm_reference_v = 0.19`, `condition = test_signal` ja `trial = 1` jäid 24.10 katsest. Tingimused tuleb lugeda [25.10 protokollist](docs/bench_session.md#adc-mõõteseeriad) ja failinimedest. Failidel puuduvad logija `.runs.jsonl` kõrvalfailid. Olemasolevad seeriad sobivad ADC koodide kirjeldamiseks ja ajagraafikuks. Kalibreeritud rõhu, SNR-i ja võrdluse jaoks on vaja täiendavaid mõõtmisi.

## Süsteemi arhitektuur

25.10 kasutatud mõõteahel ja andmete tee arvutis:

```text
MPX5700AP → LM358N võimendusaste → 10 kΩ / 10 kΩ jagur → AtomS3R G5 (ADC)
                                                       → USB → logger.py → CSV → analyze.py
```

- **Labor 1 (`raw`).** Andur läks otse G5-le. Atmosfääril mõõdeti anduri toiteks 5,00 V ja väljundiks 0,85 V. Empiirilise `3,70 V / 4095` teisendusteguri ning andmelehe valemi põhjal saadi ligikaudu **141 Pa/ADC kood**. See on Labori 1 arvutuslik lähtejoon. Labori 1 logis oli 1002 rida 10,010 s jooksul ehk ligikaudu 100,1 Hz. Labori 2 lahutus ja ohutu G5 pingeulatus vajavad oma mõõtmisi. [Labori 1 andurimõõtmised ja arvutus](../lab1/docs/sensor_choice.md).
- **25.10 (`opamp`).** LM358N üks kanal võimendas ja nihutas signaali, teine puhverdas viitepinget. G5 luges kahe 10 kΩ takisti keskpunkti. [Ühendused ja mõõtepunktid](docs/bench_session.md#katseskeemi-ühendused).
- **Muudetud teine versioon.** Varasema testsisendi B5K eemaldati, `Rref` ahelat pikendati ja puhvri väljundile lisati 4,7 kΩ allatõmbetakisti. Jaguri alumise haru seis ja G5 jadatakisti väärtus vajavad kontrolli. [Üleandmise märkmed](docs/opamp_v2_handoff_2026-10-25.md#2-plaadil-tehtud-muudatused-2-versioon).
  - 14.11.26 märkus: andur töötab, kuid vana plaadi ühendused olid vigased (anduri väljund plaadil ~0,5 V, rõhuga ei muutunud). Aste ehitatakse uuele plaadile ümber. [Tõrkeotsing ja uus paigutus](docs/opamp_rebuild_2026-11-14.md).

Püsivara seadistab G5 sisendiks, kasutab 12-bitist ADC-d, `ADC_11db` sumbuvust ja kaheksa lugemi keskmist. Siht on 100 Hz. AUTO kuvab kalibreerimata ADC koodi LCD-l ja USB eelvaates kuni neli korda sekundis. Logija valib hallatud jooksule `raw` või `opamp` sildi füüsilise ühenduse järgi. Mõõtmisprogramm ei juhi pumpa ega MG400 robotit. Logija toetab Windowsi kohalikke `COM` porte ja macOS-i `/dev/cu.*` porte. Windowsi pordikäsitlus on tarkvaras testitud, füüsiline Windowsi USB-katse vajab kinnitust. [Püsivara ja logija](src/README.md) · [Windowsi ja macOS-i käsud](src/README.md#logija-windowsis-ja-macos-is).

Andmehõive ja Smart Solutions kasutavad sama AtomS3R-i. Korraga töötab üks põhipüsivara. Andmehõive versioon on ADC ja CSV kogumiseks, Smart Solutions `NORMAL` postkontori ja jaama tööks. Püsivara vaheta kontrollitud üleslaadimisega, säilitades varukoopia ja taastamisvõimaluse ning kontrollides ühendatud elektroonikat. XIAO ESP32S3 Sense on eraldi kaameraplaat oma püsivaraga.

## Kiirstart ilma riistvarata

Käivita repo juurkaustast macOS-i või Linuxi terminalis. Vajad Python 3 ja analüüsi sõltuvusi. Paigaldus vajab pakiallikat või kohalikku paketivahemälu. Kui sobiv Python-keskkond on juba olemas, kasuta selle Pythonit. Analüüs ja testid töötavad võrguühenduseta.

```sh
lab2_tmp=$(mktemp -d)
python3 -m venv "$lab2_tmp/venv"
"$lab2_tmp/venv/bin/python" -m pip install -r data-acquisition/lab2/notebooks/requirements.txt
export MPLCONFIGDIR="$lab2_tmp/mpl"

"$lab2_tmp/venv/bin/python" -B data-acquisition/lab2/src/python/analyze.py \
  data-acquisition/lab2/data/opamp_pump_off_test.csv \
  data-acquisition/lab2/data/opamp_vacum_test.csv \
  data-acquisition/lab2/data/opamp_pressure_test.csv \
  --out "$lab2_tmp/results"
ls "$lab2_tmp/results"
```

Ava ajutisest väljundkaustast `adc_time.png` ja `summary.json`. Graafiku y-telg on ADC kood, x-telg sekundites jooksu algusest. `raw` paneel on tühi, sest kõik sisendid on `opamp` seeriad. Kalibratsiooni ja võrdlusplaanita jäävad rõhk, SNR ja spektrid arvutamata. [Analüüsijuhend](notebooks/README.md).

Käivita samas terminalis kõik tarkvaratestid. Täiskomplekt vajab ka `c++` kompilaatorit ja PlatformIO ehitusega laaditud ArduinoJsoni päiseid. [Eeltingimused ja ehituskäsk](src/README.md#tarkvarakontroll).

```sh
"$lab2_tmp/venv/bin/python" -B -m unittest discover -s data-acquisition/lab2/tests -v
```

## Kaitsmise juhend

Valmista [kiirstardi](#kiirstart-ilma-riistvarata) abil ette graafik ja kokkuvõte. Ava ka arvutus, mõõteprotokoll ja päevik. Allolev 7-minutiline demonstratsioon töötab ilma riistvarata. Ametlik 15-minutiline kaitsmine nõuab lisaks sisendi ja väljundi samaaegset ostsilloskoobivaadet, esimese astme vea selgitust ning pumba seiskamise näitamist uue signaaliga. [Õppejõu kaitsmisjuhend](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLab%202%5D%20EST.md#kaitsmine).

| Aeg | Mida näidata | Mida selgitada |
|---|---|---|
| 0:00–1:00 | [Mõõteahel](#süsteemi-arhitektuur) | Mida andur, võimendi, pingejagur, ADC ja logija teevad. Kuidas erinevad `raw` ja `opamp`. |
| 1:00–2:30 | [Võimenduse arvutus](docs/opamp_design.md#võimenduse-arvutus), [22.10 katseskeemi arvutus](docs/opamp_design.md#väljundpinge-arvutamine) ja [Falstadi näide](docs/opamp_design.md#õppejõu-mpx5700ap-näite-falstadi-esimene-versioon) | Kuidas võimendus määrab ulatuse ja viitepinge nihke. Millised arvud on mõõdetud ja millised pärinevad õppejõu näite simulatsioonist. |
| 2:30–3:45 | [Mõõtmiste tabel](#tõendid-ja-tulemused) ja üks algne CSV | Millal kasutati potentsiomeetrit, millal andurit. Kuidas 1001 lugemist annab 1000 ajavahet. Miks CSV metaandmeid tuleb lugeda koos protokolliga. |
| 3:45–5:30 | `adc_time.png` ja `summary.json` | Osuta seisva pumba kõikumisele ja vaakumi lamedale osale 14–21 koodi juures. Selgita, miks `adc_clipped=0` ei tuvasta analoogastme küllastust ja miks kPa või SNR veel puuduvad. |
| 5:30–7:00 | [Üleandmise märkmed](docs/opamp_v2_handoff_2026-10-25.md), [kontrollnimekiri](#kontrollnimekiri) ja [arenduspäevik](#arenduspäevik) | Mis muutus pärast CSV katseid, milline kontroll lubab G5 ühendada ja millised tõendid on veel vaja koguda. |

## Puuduvad katsed ja järgmised sammud

### Kodus, olemasolevate failidega

1. Tee kolme CSV ajagraafik ja märgi kaitsmiseks vaakumi alumine platoo. Valmista ette sama päeva `raw`/`opamp` katseplaan koos `condition`, `trial`, baasjoone ja platoo akende märkimisega. [Analüüs ja vajalikud failid](notebooks/README.md#maksimilt-vajalikud-failid-ja-mõõtmised).
2. Valmista ette tööleht toite-, sisend-, viite- ja väljundpingete ning otspunktivigade kirjapanekuks. Õppejõu Falstadi näidise eksport ja veebilingid on olemas. Meeskonna skeem, ühismüra ja ühe sisendi müra kontroll ning skeemipilt jäävad teha lõplike lähteandmetega. [Arvutused ja Falstad](docs/opamp_design.md) · [BOM ja tellimus](docs/bom.md).

### Laboris, päris mõõtmistega

1. **Kontrolli skeemi ja G5 ohutust.** Tuvasta muudetud skeemi juhtmed, jagur ja takistid. Mõõda tegelik anduri ning LM358N toide, `Vin`, `Vref` ja `Vout` atmosfääril, täis imemisel ja täis puhumisel. Kontrolli ADC-sse minevat pinget kogu ulatuses, sh siiretel, enne G5 ühendamist. Kontrolli füüsiliselt komponendid ja tellimisvajadus. [Pingitöö ja ohutu järjekord](docs/bench_session.md#4-ohutu-tööjärjekord).
2. **Mõõda ja paranda aste.** Pane kirja esimese astme kolm punkti ja mõlema otspunkti vead. Põhjenda mõõtmiste alusel parandatud vahemik ja takistid ning korda kolme punkti kontrolli. Salvesta skeemifoto ja kahe kanaliga ostsillogramm samast impulsist anduri ja astme väljundis. Lisa meeskonna Falstadi skeem koos ekspordi, pildi ja muudetava lingiga. [Otspunktivead](docs/opamp_design.md#otspunktide-vead) · [Parandatud astme mõõtetabel](docs/opamp_design.md#parandatud-versiooni-kolme-punkti-mõõtmine).
3. **Kalibreeri ja kogu võrdlus.** Pärast elektrilist kontrolli kinnita ADC ajastus ja kalibratsioon mõlemas ühenduses. Salvesta samal päeval sama protokolliga ühte CSV-sse vähemalt 30 impulssi kummaski konfiguratsioonis, koos logija kõrvalfailiga. Arvuta kontrollitud kalibratsioonist Pa/ADC samm ja võrreldavatest akendest SNR dB-des enne ja pärast astet. Kõrvuta spektreid Labori 1 omadega samadel telgedel, rõhk kPa-des. [Kalibratsioon, SNR ja spektrid](notebooks/README.md#kalibratsioon-snr-ja-spektrid).
4. **Võrdle pumbajuhtimist.** Mõõda klaasil, õhus ja korgiga voolikuga juhtimisriba, minimaalne väljalülitusaeg ning käivitused minutis. Mõõda pooliku haarde eristamise aeg sekundites mõlema signaaliga. Võrdle Labori 1 lähtejoonega (välja −60 kPa, sisse −40 kPa, vähemalt 15 s seisu ja kuni 4 käivitust/min), põhjenda järeldust ja näita pumba seiskumist. [Labori 1 pumbajuhtimine](../lab1/docs/pump_control.md) · [Labori 2 võrdlustabel](docs/pump_control.md).

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

## Ohutus

- Lülita USB ja 5 V välja enne juhtmete muutmist.
- Mõõda astme väljund multimeetriga enne ADC-ga ühendamist ja pärast iga komponendimuudatust; ADC viik ei talu 5 V.
- Ühenda 24 V pumbakasti DO-liinid ainult siis, kui robot on keelatud ja kast vooluta.
- Jälgi pumba käivitusi minutis ja minimaalset väljalülitusaega; soojeneva kasti korral katkesta katse.
- Ära suuna lahtist survevoolikut kellegi poole.
- Katseta poolikut haaret laual, ilma käeta klaasi all.
- Hoia käed laualt eemal, kui MG400 on sisse lülitatud; esimene jooks aeglaselt ja hädastopp käeulatuses.
- Selles laboris ei joodeta.

**Enne G5 ühendamist** kontrolli ühine maa ning mõõda tegeliku anduri toide, LM358N toide viikudel ja ADC-sse minev signaal kogu kasutusalas. Kontrolli ostsilloskoobiga ka pumba lülitamise ja rõhu muutuse siirdeid. Ära ühenda kontrollimata 5 V analoogsignaali otse G5-le. `3,3 V` projekteerimissiht ega tarkvaratestid ei kinnita viigu elektrilist sobivust. [G5 elektriline kontroll](docs/bench_session.md#elektriline-kontroll-enne-g5-ühendamist).

## Hindamiskriteeriumid

| Kategooria | Punktid | Ettevalmistuse olek |
|---|---:|---|
| Tööfailid — mõlemad konfiguratsioonid, `config` veerg ja CSV-d | 5 | TODO: real measurement required |
| Analüüs — Pa/samm, spektrid, SNR ja pumbajuhtimise võrdlus | 5 | Labori 1 raw-lähtejoon olemas; TODO: real measurement required |
| Prototüüp — esimene ja parandatud aste mõõdetud ning uus juhtimine töötab | 5 | TODO: real measurement required |
| Dokumentatsioon — README, päevik, Falstad, `pump_control.md`, `bom.md`, AGENTS.md | 5 | ettevalmistamisel |
| **Kokku** | **20** | |

## Labori ajalugu

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

- Tegime: toitsime AtomS3R-i USB kaudu ja kasutasime UNI-T UT139C multimeetrit. Mõõtsime B5K ja B100K potentsiomeetrite takistuse. Ühendasime B5K ajutiseks reguleeritavaks sisendiks ning proovisime LM358N esimest kanalit pingejärgija. Kontrollisime maketeerimisplaadi ridade ühendusi, toiteviikude pidevust ja ilmset lühist enne pingestamist. AtomS3R ADC-d ei ühendatud.
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
* Lahti järgmiseks korraks: tudeng kinnitab osalejad ja kirje; eraldi luba üleslaadimiseks; LM358 ja MPX5700AP kogu väljundulatuse ning transientide elektriline kontroll enne G5 ühendamist; tegelik ajastus, kalibratsioon ja vähemalt 30 impulssi kummagi konfiguratsiooniga. Füüsiline tulemused, SNR ja pumbavõrdlus jäävad TODO.

**22.10.26 katse allikaviide — lisatud 23.10.26 (Maksim)**

* Tegime: sidusime olemasoleva 22.10 katsekande Maksimi Word-allika ja [eestikeelse koostamisjuhendiga](docs/lm358n_wiring_2026-10-22.md). Juhend sisaldab viigustikku, ühendusi ja arvutuse kontrolli; varasemad mõõteväärtused ja päevikukanded jäävad muutmata.
* Juhtus (numbrid): allikas kinnitab varem kirjapandud ühe tööpunkti tulemused ning B5K reguleerimisel saadud väljundnäidu. Uusi füüsiline mõõtmisi selle dokumenteerimise käigus ei tehtud.
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

**07.11.2026. Täpsustus tööjaotuse kohta**

[Mõõteprotokollid](docs/bench_session.md#22102026--lm358n-katseskeemi-mõõtmised-maksim) kinnitavad Maksimi mõõtmised 22., 24. ja 25.10. [Raimo üleandmine](docs/opamp_v2_handoff_2026-10-25.md) toimus pärast Maksimi 25.10 jaguriga katseid. [23.10 tarkvaratöö](#arenduspäevik) ei olnud füüsiline katse. Tarkvaratöö tegijad vajavad meeskonna kinnitust.

## Väljundid ja tulemused

Esitamisel koonda kinnitatud tulemused koos ühikute ja failiviidetega. [Mõõtetulemused](#tõendid-ja-tulemused) · [Lõpetamata katsed](#puuduvad-katsed-ja-järgmised-sammud).

**KAARDISTA ISE, lõpus.**

- Repo ja tag `data-acquisition-lab2`: lisada tag alles esitamisel.
- Mida teeksime teisiti: sõnasta pärast parandatud astme mõõtmist ja võrdluskatseid.
- Järgmisele laborile: anna üle kontrollitud skeem, kalibratsioon, proovivõtu ajastus ja pooliku haarde logid. Labori 3 komparaatori jaoks tuleb eraldi lahendada LM358N viitepuhvri ülesanne. Smart Solutions Atomi rõhuväljad vajavad kinnitatud kalibratsiooni. [Labor 3 lähteandmed](../lab3/README.md).
