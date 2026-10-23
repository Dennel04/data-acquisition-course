# Labor 2 mõõtmistarkvara

Esimene etapp kogub ainult ADC toorandmeid. Püsivara ja logija on tarkvaraliselt kontrollitud. Kasutaja kinnitas USB-only üleslaadimise, LCD töö ja `measure_stop` käsu `stopped` vastuse (Serial Monitor `--eol LF`). Elektriline sobivus, tegelik sagedus ja rõhukalibratsioon vajavad mõõtmist. Labor 1 lähtekood jääb muutmata. Võrguühenduseta CSV analüüs: [notebooks/README.md](../notebooks/README.md).

## Mõõtmisrežiim

`firmware/` on AtomS3R PlatformIO projekt (`atoms3r`, ühilduv board `m5stack-atoms3`). GPIO G5 on sisend: 12 bitti, `ADC_11db`, kaheksa lugemi täisarvuline keskmine. Siht on üks proov iga 10 ms järel. Hilinenud ajavahemikud loendatakse, mitte ei täideta väljamõeldud proovidega. LCD näitab režiimi ja ADC koodi; käivitamisel oodatakse USB käsku.

Wi-Fi, võrk, pumbajuhtimine, robot ja salvestatud seadete laadimine puuduvad. NVS-i algatamine ja namespace'ide avamine on linker-guardidega blokeeritud, et Arduino automaatne taastamine ega M5 teegid ei muudaks olemasolevaid seadeid. See ei taga kogu flash'i muutumatust: SDK panic/coredump ja OTA metadata jäävad eraldi riskiks. Ärge kasutage `erase_flash`, `uploadfs` ega tehase lähtestamist. Enne eraldi lubatud üleslaadimist kontrollige olemasoleva püsivara taastamise võimalust ja privaatset backup'i.

`raw` tähendab kontrollitud anduriväljundit, `opamp` kontrollitud astme väljundit. Silt ei muuda juhtmestikku ega kalibratsiooni. Mõlema elektriline sobivus tuleb eraldi kinnitada: [tööjärjekord](../docs/bench_session.md#6-mõõtmisprogrammi-kasutuselevõtt).

## USB protokoll

115200 baud, üks ASCII JSON-objekt real. Logija saadab ühe käivituskäsu koos juhusliku jooksu ID-ga:

```json
{"cmd":"measure_start","config":"raw","run":"0123456789abcdef"}
```

Püsivara kinnitab `event=started`, `firmware=DA2_MEASURE_V1`, sama `run` ja `config`, `period_ms=10`, `adc_pin=5`, `adc_bits=12`, `adc_samples=8`, `calibrated=false`. Seejärel väljastab:

```json
{"t":1234,"adc":123,"p":null,"pump":null,"config":"raw","run":"0123456789abcdef","seq":0,"missed":0}
```

Näide on sünteetiline, mitte mõõtmine. `t` on Atomi `millis()`, `seq` algab nullist, `missed` loendab vahele jäänud 10 ms intervalle. `{"cmd":"measure_stop"}` peatab ainult mõõtmise. Neid käske ei tohi asendada Labor 1 pumbakäskudega. Vigane käsk või serial-raam peatab jooksu. USB taasühendus ei taasta jooksu automaatselt.

## Logija MacBookis

Sulge Serial Monitor ja kõik teised sama porti kasutavad programmid. Kasuta tegelikult tuvastatud porti, mitte vana pordinumbrit. Järgmised käsud on tulevase füüsilise katse jaoks, mitte selle ettevalmistuse käigus tehtud katsed:

```sh
cd data-acquisition/lab2
python3 -m venv .venv
.venv/bin/pip install -r src/python/requirements.txt
.venv/bin/python src/python/logger.py --port /dev/cu.usbmodemXXXX \
  --config raw --csv data/measurements.csv --condition atmosphere \
  --trial 1 --duration 10 --electrical-check-confirmed
```

Püsivas tööpunktis lisa `--dmm-v TEGELIK_PINGE` (asenda mõõdetud arvuga). See on käsitsi sisestatud G5 sõlme võrdluspinge, mitte iga proovi mõõdetud pinge. `dmm_recorded_utc` on logijasse sisestamise aeg; tegelik multimeetri mõõtmisaeg ja meetod märgi töölehele. Ära lisa üht püsipinge näitu muutuva impulsi jooksule.

Järgmise jooksu lisamiseks samasse CSV-sse kasuta `--append`, uut `--trial` numbrit ning õiget `--config raw` või `--config opamp`. Olemasolevat faili ilma `--append` parameetrita ei kirjutata üle. Ühine CSV on lubatud ainult koos iga rea `config`, `run_id`, `condition` ja `trial` väljadega. Füüsiliselt vaheta ühendusi ainult väljalülitatud toitega.

CSV veerud:

```text
t_ms,adc,p_kpa,pump,config,run_id,seq,missed,voltage_v,dmm_reference_v,dmm_recorded_utc,condition,trial,adc_clipped
```

`p_kpa`, `voltage_v` ja `pump` jäävad tühjaks: puuduvad selle seadme ja kummagi konfiguratsiooni kinnitatud teisendus ning pumba tagasiside. Tühi pump ei tähenda `off`. `adc_clipped` märgib ainult koodi 0 või 4095, mitte diagnoosi ega elektrilist ohutust. Kõik jooksud saavad kõrvalfaili `.runs.jsonl`, kus on kestus, ridade arv, sagedus, min/max intervall ja vead. Poolik jooks säilib tõendina; ära kasuta seda vaikimisi kehtiva võrdlusena. Logija lõpetab vigase raami, vale konfiguratsiooni, puuduva proovi või 500 ms vaikuse korral; pumba olekut ta ei muuda. Väljumiskood 0 nõuab lõppenud jooksu, null vahelejäänud intervalli ning 9–11 ms proovivahesid. Tegelik USB läbilase ja 100 Hz tuleb riistvaral kontrollida.

## Tarkvarakontroll

```sh
python3 -m unittest discover -s data-acquisition/lab2/tests -v
cd data-acquisition/lab2/src/firmware
pio run -e atoms3r
```

Testid kasutavad sünteetilisi JSON-ridu, ajakella ja ajutisi CSV-faile; ühestki testist ei saa füüsilisi mõõtetulemusi. Hostil kompileeritakse ka tegelik C++ ajastusloogika. Üleslaadimine vajab eraldi luba.

## Labor 1 lähtejoon ja veel vajalik kalibratsioon

- Toetada kahte selgelt valitavat konfiguratsiooni: `raw` ja `opamp`.
- Hoida konfiguratsiooniga seotud ADC ja teisenduse seaded eraldi ning jälgitavad.
- Võtta raw-konfiguratsiooni lähtepunktiks Labori 1 MPX5700AP ülekandefunktsioon `Vout = Vcc · (0,0012858 · P_abs + 0,04)`, 12-bitine ADC, `ADC_11db`, kaheksa lugemi keskmine ja empiiriline koodist pingeks tegur `3,70 V / 4095`. Allikad: `data-acquisition/lab1/src/firmware/include/sensor.h`, `data-acquisition/lab1/src/firmware/src/sensor.cpp` ja `data-acquisition/lab1/docs/sensor_choice.md`. Kontrollida tegur Labor 2 riistvaral uuesti: TODO: real measurement required.
- Säilitada ametliku Labor 2 sisendi diskreetimise siht `100 Hz`. Laboris 1 mõõdeti `1002` rida `10010 ms` jooksul ehk ligikaudu `100,1 Hz`; Labor 2 tegelik sagedus: TODO: real measurement required.
- Kuvada konfiguratsioon nii, et logi ja ekraani olek ei läheks segamini.

## Python logger

- Lisada Labori 1 CSV-skeemile `t_ms,adc,p_kpa,pump` veerg `config`, mille lubatud väärtused on `raw` ja `opamp`.
- Säilitada ajatempel, ADC toorväärtus, suhteline rõhk kilopaskalites ja pumba olek.
- Kontrollida tegelikku diskreetimissagedust ajatemplite järgi. TODO: real measurement required.
- Tagada, et mõlema konfiguratsiooni andmeid saab võrrelda sama skeemi ja ühikutega.

## Pumbajuhtimine

Pumbajuhtimise ühendamine tuleb pärast astme ehitamist, elektrilist kontrolli ja `raw/opamp` võrdlusandmete kogumist. Labori 1 ajalooline lähtejoon oli `off −60 kPa`, `on −40 kPa`, automaatsete taaskäivituste minimaalne väljalülitusaeg `15 s` ja ülempiir `4 käivitust/min` (`data-acquisition/lab1/docs/pump_control.md`). Labor 2 väärtused määratakse uute mõõtmiste põhjal: TODO: real measurement required.
