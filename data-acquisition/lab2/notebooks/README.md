# Labor 2 analüüsi töövoog

Minimaalne korratav analüüs asub failis `../src/python/analyze.py`. Päris CSV-sid pole veel saadud; ettevalmistus ei anna Labor 2 mõõtetulemusi. Eraldi notebook'i pole käivitamiseks vaja.

Kavandatud töövoog:

1. Laadi `raw` ja `opamp` read ning kontrolli kohustuslikke veerge, ühikuid ja `config` väärtusi.
2. Arvuta ajatemplite vahedest tegelik diskreetimissagedus. Ametliku sisendi siht on `100 Hz`; Labori 1 kontroll oli `1002` rida `10010 ms` jooksul ehk ligikaudu `100,1 Hz`. Labor 2 tegelik sagedus: TODO: real measurement required.
3. Vali võrreldavad, sama protokolliga pumbaimpulsid mõlemas konfiguratsioonis.
4. Kinnita kummagi konfiguratsiooni Labor 2 kalibratsioon enne rõhuks teisendamist. Labori 1 ajalooline lähtepunkt oli MPX5700AP, 12-bitine `ADC_11db`, empiiriline teisendus `3,70 V / 4095` ja andmelehe ülekandefunktsioon; see andis arvutuslikult `0,1405 kPa/kood = 141 Pa/kood`. Analüüs ei rakenda seda tegurit Labor 2 andmetele automaatselt. Mõlema Labor 2 teisenduse kontroll: TODO: real measurement required.
5. Arvuta spektrid sama meetodi, akna, telgede, sagedusvahemiku ja ühikutega.
6. Arvuta signaalitase: platoo keskmine miinus baasjoone keskmine.
7. Arvuta platoo müra standardhälve samaväärses stabiilses ajavahemikus.
8. Arvuta `SNR_dB = 20 · log10(|signal| / noise_std)`.
9. Arvuta Pa ühe ADC sammu kohta enne ja pärast astet kontrollitud ülekandefunktsioonidest. Võrdle tulemust Labori 1 raw-lähtejoonega `141 Pa/kood`; ära käsitle seda Labor 2 mõõdetud väärtusena.
10. Koosta `raw` ja `opamp` võrdlus samade telgede, ühikute, intervallide ja kokkuvõtlike tabelitega.

Labori 1 CSV lähteveergude skeem: `t_ms,adc,p_kpa,pump`. Praeguse Labor 2 logija täpne skeem:

```text
t_ms,adc,p_kpa,pump,config,run_id,seq,missed,voltage_v,dmm_reference_v,dmm_recorded_utc,condition,trial,adc_clipped
```

`t_ms` on seadme 32-bitine `millis()`, mitte arvuti kell. `seq` algab iga jooksu puhul nullist. Analüüs arvestab `millis()` ületäitumist ja alustab iga `run_id` aega nullist. `adc` on kaheksa 12-bitise lugemi täisarvuline keskmine; tarkvaraline keskmistamine mõjutab müra ja spektrit. `config` on `raw` või `opamp`, mitte automaatne elektrilise ühenduse tuvastus.

`p_kpa`, `voltage_v` ja `pump` on praegusel logijal tühjad. `dmm_reference_v` on käsitsi sisestatud püsipinge võrdlusnäit, mitte iga proovi pinge ega rõhukalibratsioon. `dmm_recorded_utc` on näidu logijasse sisestamise aeg. Analüüs ei asenda puuduvaid väärtusi nullidega ega Labor 1 teisendusteguriga.

Labor 2 andmefailid: TODO: real measurement required.

Analüüsitulemused: TODO: real measurement required.

## 25.10.2026 — tegelike mõõteandmete esmane analüüs

25.10.2026 salvestati MPX5700AP rõhuanduri, LM358N võimendusastme ja AtomS3R G5 ADC abil kolm mõõteseeriat. Võimendi väljundi ja ADC sisendi vahel kasutati kahest `10 kΩ` takistist koosnevat pingejagurit.

Kõik kolm katset tehti `opamp` konfiguratsioonis. Iga mõõteseeria kestis ligikaudu 10 sekundit ja sisaldas umbes 1000 ADC lugemit.

### Mõõtefailid

| Katse | CSV-fail | Kirjeldus |
|---|---|---|
| Pump välja lülitatud | [opamp_pump_off_test.csv](../data/opamp_pump_off_test.csv) | Baastaseme ja ADC näidu kõikumise kontroll |
| Vaakum | [opamp_vacum_test.csv](../data/opamp_vacum_test.csv) | Vaakumi tekitamine ja pumba väljalülitamine |
| Ülerõhk | [opamp_pressure_test.csv](../data/opamp_pressure_test.csv) | Rõhu tõus ja sellele järgnev vähenemine |

### ADC statistika

| Katse | Minimaalne ADC | Maksimaalne ADC | Keskmine ADC | Standardhälve |
|---|---:|---:|---:|---:|
| Pump välja lülitatud | 642 | 667 | 657,62 | 2,90 |
| Vaakum | 14 | 837 | 511,54 | 306,76 |
| Ülerõhk | 641 | 1175 | 804,60 | 185,60 |

Väljalülitatud pumba katses oli ADC näit suhteliselt stabiilne. Standardhälve oli ligikaudu `2,90` ADC koodi.

Vaakumi ja ülerõhu katsetes sisaldab standardhälve ka rõhu muutumisest põhjustatud signaali kõikumist. Seetõttu ei saa nende katsete kogu mõõteseeria standardhälvet käsitleda ainult mürana.

### Täheldatud üleminekud

Vaakumkatses täheldati pumba väljalülitamise järel lühiajalist ADC näidu tõusu ligikaudu `805` koodini. Üheks võimalikuks selgituseks on rõhu ajutine muutus pumba või ventiili ümberlülitamisel, kuid põhjus ei ole veel kinnitatud.

Ülerõhukatses vähenes ADC näit ligikaudu `1126 → 940 → 860` koodini, millele järgnes järsk langus. Võimalikeks põhjusteks on aeglane rõhukadu ja sellele järgnenud rõhu vabastamine. Selle kinnitamiseks on vaja täiendavaid katseid.

### Analüüsi piirangud

- Kõik kolm mõõtefaili kuuluvad `opamp` konfiguratsiooni. Võrreldavat Labor 2 `raw` mõõteseeriat veel ei ole.
- Rõhu kalibratsioon `kPa` ühikutesse ei ole lõpetatud.
- CSV-failides puuduvad proovipõhised rõhu- ja pingeväärtused.
- Pumba olekut ei saa CSV `pump` veeru põhjal automaatselt tuvastada; katsete nimetused lähtuvad laborimärkmetest.
- SNR-i, Pa/ADC sammu ja `raw`/`opamp` spektrivõrdlust ei saa nende kolme faili põhjal veel usaldusväärselt arvutada.

Need andmed kinnitavad, et ADC salvestas rõhu muutustega seotud signaalimuutusi, kuid ei tõenda veel võimendusastme lõplikku täpsust ega eeliseid võrreldes toorsignaaliga.

## Käivitamine

Repo juurkataloogist, pärast päris failide saamist:

```sh
python3 -m venv data-acquisition/lab2/.venv
data-acquisition/lab2/.venv/bin/pip install -r data-acquisition/lab2/notebooks/requirements.txt
data-acquisition/lab2/.venv/bin/python data-acquisition/lab2/src/python/analyze.py \
  data-acquisition/lab2/data/measurements.csv \
  --out data-acquisition/lab2/notebooks/results-first
```

Asenda CSV tee saadud failiga. Võid anda mitu CSV-d; dubleeritud read / jooksud ei ole lubatud. `--out` peab olema uus kataloog, olemasolevat analüüsi ei kirjutata üle. Ilma CSV-ta või puuduva/tühja CSV korral väljub programm koodiga 2 ja tulemusi ei loo. Väljundid on `summary.json` ja `adc_time.png`; algfaile programm ei muuda.

Analüüs kontrollib skeemi, ADC piire, metaandmete püsivust, järjestust ja ajavahesid. Raportis on iga jooksu sagedus, kõrvalekalle 100 Hz sihist protsentides, min/max ajavahe ning logijaga sama ajastuskriteerium: null vahelejäänud intervalli ja iga ajavahe 9–11 ms. Terviklikkuse kontroll kasutab CSV kõrvalfaili `<CSV>.runs.jsonl`. Puuduv või poolik kõrvalfail ei takista ADC graafikut, kuid SNR ja spektrivõrdlus vajavad lõpetatud jooksu tõendit. Tarkvaraline kontroll ei tõenda elektrilist ohutust.

ADC statistika sisaldab keskmist, valimi standardhälvet (`ddof=1`), min/max, tippude vahet, keskmisest eemaldatud RMS-i ja äärmuslike koodide arvu. Kogu impulsi standardhälve sisaldab signaali muutust; seda ei tohi nimetada platoo müraks. Graafik eraldab `raw` ja `opamp`, kumbki jooks säilitab oma ajatelje.

## Kalibratsioon, SNR ja spektrid

Need arvutused on valikulised. Lisa `--plan TEGELIK_PLAAN.json` alles pärast andmete ja katsemärkmete kontrolli. Plaani struktuur (sümbolid tuleb asendada kontrollitud arvude ja päris jooksu ID-dega; see pole käivitatav kalibratsioon):

```text
{
  "calibration": {
    "RAW_RUN_ID": {
      "config": "raw", "source": "mõõteprotokolli tee ja meetod",
      "pa_per_code": K_RAW, "offset_pa": B_RAW,
      "adc_range": [MÕÕDETUD_ALUMINE_KOOD, MÕÕDETUD_ÜLEMINE_KOOD]
    },
    "OPAMP_RUN_ID": {
      "config": "opamp", "source": "mõõteprotokolli tee ja meetod",
      "pa_per_code": K_OPAMP, "offset_pa": B_OPAMP,
      "adc_range": [MÕÕDETUD_ALUMINE_KOOD, MÕÕDETUD_ÜLEMINE_KOOD]
    }
  },
  "windows": {
    "RAW_RUN_ID": {"baseline_s": [ALGUS, LÕPP], "plateau_s": [ALGUS, LÕPP]},
    "OPAMP_RUN_ID": {"baseline_s": [ALGUS, LÕPP], "plateau_s": [ALGUS, LÕPP]}
  },
  "spectrum_pairs": [{
    "raw_run": "RAW_RUN_ID", "opamp_run": "OPAMP_RUN_ID",
    "raw_s": [ALGUS, LÕPP], "opamp_s": [ALGUS, LÕPP],
    "protocol": "sama päeva sama impulsi protokoll ja valiku põhjendus"
  }]
}
```

Kalibratsioon kirjeldab lineaarset seost `P_Pa = K · adc + B`. `Pa/ADC step = |K|`. Kinnitatud ADC pinge-/koodisammu ja anduri tundlikkuse korral `K_raw = q_V/S_P`, `K_opamp = q_V/(A·S_P)`, kus `S_P` ühik on V/Pa ning `A` on kontrollitud astme võimendus. Mõõda ka nihe ja kontrolli lineaarsust kogu kasutatavas vahemikus. Üks multimeetri näit ei määra kogu teisendust; õppejõu näidis ega Labor 1 ajalooline tegur ei kinnita selle seadme Labor 2 kalibratsiooni. Märgi, kas rõhuseos põhineb referentsrõhul või andmelehe mudelil, koos toitepingega. Programm nõuab allikaviidet ja kontrollitud ADC vahemikku, kuid kalibratsiooni õigsust peab inimene tõendite järgi hindama.

Vali graafikult statsionaarsed ja kattumatud baseline/platoo aknad. Ajad on sekundites jooksu esimesest proovist; aknad on `[algus, lõpp)`. Programm arvutab `signal = mean(plateau) − mean(baseline)`, `noise = std(plateau, ddof=1)`, `SNR_dB = 20·log10(|signal|/noise)`. Nullsignaali või nullmüra korral jääb SNR määramata. Kummagi konfiguratsiooni võrdluses peab inimene valima sama protokolli ja võrreldavad aknad; programm ei leia impulssi ega platoo piire ise.

Spektripaar peab nimetama sama `condition` ja `trial` väärtusega raw/opamp jooksud ning katseprotokolli. Analüüs nõuab kinnitatud kalibratsiooni, sama proovide arvu ja täpselt sama ühtlast prooviperioodi; jitteriga andmeid ei interpoleerita. Meetod: keskmise eemaldamine, Hann-aken, ühepoolne periodogramm tihedusühikus kPa²/Hz. Mõlemad kõverad asuvad samal graafikul ühiste telgedega (`spectra_1.png`, jne). Koodid 0/4095 või vigane ajastus blokeerivad SNR-i ja spektrid. See konservatiivne kontroll võib vajada hiljem eraldi põhjendatud ebaregulaarse diskreetimise meetodit.

Vähemalt 30 impulssi kummaski konfiguratsioonis, Labor 1 spektritega kõrvutamine ning katsete sobivuse hindamine jäävad päris andmete saabumiseni TODO. Programm ei väida, et üks spektripaar täidab kogu ülesande.

## Maksimilt vajalikud failid ja mõõtmised

- Saada logija algsed muutmata CSV-d mõlema konfiguratsiooni kohta ja iga CSV `<CSV>.runs.jsonl` kõrvalfail. Säilita ebaõnnestunud jooksud; märgi nende põhjus. Ära saada ainult ekraanipilti või ümber salvestatud Exceli faili.
- Kirjelda iga `run_id`, `condition` ja `trial`: raw/opamp ühendus, sama päeva impulsi protokoll, vähemalt 30 impulssi kummaski konfiguratsioonis, baasjoone/platoo ajad ning küllastuse või katkestuse vaatlus. Märgi rõhuviide (suhteline/absoluutne) ja ühikud.
- Lisa päris multimeetri näidud koos mõõtekohtade, mõõtmise aja ja rõhuolukorraga: anduri toide, LM358 toide otse viikudel, anduri väljund ning astme väljund atmosfääril, täis imemisel ja täis puhumisel; `V_ref`, kasutatud takistite mõõdetud väärtused ja skeem. Näitearve ära sisesta tulemusteks.
- ADC teisenduse kontrolliks saada stabiilsetes punktides G5 sõlme mõõdetud pinge koos sama jooksu ADC koodidega. Vähemalt mitu vahemikku katvat punkti on vajalikud kalde/nihke ja lineaarsuse kontrolliks. Impulsi ajal ei tohi üht multimeetri näitu käsitleda ajareana.
- Rõhuks teisenduseks lisa kontrollitud rõhureferents või põhjendatud andmelehe-põhine teisendus koos mõõdetud toite ja astme parameetritega. SNR jaoks märgi sama füüsilise impulsi võrreldavad baseline/platoo osad; pooliku haarde jaoks ka katse algushetk ja eristamise kriteerium.

## Tarkvaratestid

```sh
data-acquisition/lab2/.venv/bin/python -m unittest discover -s data-acquisition/lab2/tests -v
```

Testid kasutavad sünteetilisi andmeid mälus või ajutises kataloogis, mitte labori `data/` ega tulemuste kataloogis. Graafiku- ja spektritestid vajavad ülaltoodud analüüsisõltuvusi.
