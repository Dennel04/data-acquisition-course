# Andmehõive (SVNC.00.325)

Tartu Ülikooli kursusel „Andmehõive“ mõõdame Dobot MG400 tööriista pneumaatikas rõhku. MPX5700AP muudab rõhu pingeks ja AtomS3R-i analoog-digitaalmuundur (ADC) teisendab pinge arvuliseks koodiks. Laboris 2 katsetame LM358N astet, et nihutada ja võimendada signaali ADC-le sobivasse vahemikku. Pythoni logija loeb proove USB kaudu ja kirjutab need CSV-faili, millest saab uurida ajastust, rõhukõveraid ja müra.

Laboris 1 otsustab AtomS3R rõhupiiride järgi, millal pump käivitada või peatada. Arvuti vahendab otsuse MG400-le, mille digitaalväljundid (DO) lülitavad pumbakasti. Sama AtomS3R saatis tähe ka Nutikate Lahenduste jaamale, kus MG400 joonistas selle 3D-prinditud pastakahoidikuga. [Jaama sündmuslogi](https://github.com/Dennel04/smart-solutions-course/blob/f15d7a9c06a186ed4386532c25adbccf967f748e/smart-solutions/lab1/data/letter_events.csv).

## Mõõdetud tulemused

### Labor 1 · rõhu mõõtmine ja pumbajuhtimine

| Katse | Tulemus ja tõend |
| --- | --- |
| MPX5700AP ja ADC kontroll | Atmosfääril mõõtis multimeeter **0,85 V**. ADC põhjal arvutatud **0,854 V** erines sellest ligikaudu **0,5 %**. Kümne sekundi sageduskontrollis salvestas logija **1002 rida** (ligikaudu **100 Hz**). [Mõõteprotokoll ja arvutused](data-acquisition/lab1/docs/sensor_choice.md). |
| Tehase tark kast ACU2-B | Pump lülitus välja ligikaudu **−91,5 kPa** juures. Ligikaudu kuue minuti logis korduskäivitust ei toimunud, mistõttu sisselülitusrõhku ei saadud määrata. [Mõõteprotokoll](data-acquisition/lab1/docs/pump_control.md) · [CSV](data-acquisition/lab1/data/lab1_smartbox_acu2b_12.09.26.csv). |
| Oma pumbakast, 02.10.2026 | Kasutasime väljalülituspiiri **−60 kPa** ja sisselülituspiiri **−40 kPa**. Katseprotokolli järgi kulus USB katkestamisel viimasest telemeetriareast DO väljalülituseni **29 ms**. [Katseprotokoll](data-acquisition/lab1/docs/pump_control.md) · [USB katse CSV](data-acquisition/lab1/data/lab1_usb_unplug_fw2_02.10.26.csv). |
| Klaasi tõstmine ja vabastamine | Mõlemas katseseerias õnnestus **10/10** võtmist. Pump töötas vastavalt **45,2 %** ja **29,2 %** katseajast. Klaas vabanes kõigil 20 puhumisimpulsil. [Katseprotokoll](data-acquisition/lab1/docs/pump_control.md) · [Tavavõtmise CSV](data-acquisition/lab1/data/lab1_pick10_fw3_02.10.26.csv) · [Lähenemisega võtmise CSV](data-acquisition/lab1/data/lab1_approach_pick10_02.10.26.csv). |

### Labor 2 · LM358N katse rõhuanduriga

25.10.2026 mõõtsime MPX5700AP signaali LM358N astme ja pingejaguri kaudu AtomS3R-i G5 sisendil. Igas seerias on **1001 lugemit**, ajavahe proovide vahel **10 ms**. [Ühendused ja mõõteprotokoll](data-acquisition/lab2/docs/bench_session.md#adc-mõõteseeriad).

| Katse ja algandmed | Keskmine (ADC koodi) | Vahemik (ADC koodi) |
| --- | ---: | ---: |
| [Pump väljas](data-acquisition/lab2/data/opamp_pump_off_test.csv) | 657,62 | 642–667 |
| [Vaakum](data-acquisition/lab2/data/opamp_vacum_test.csv) | 511,54 | 14–837 |
| [Ülerõhk](data-acquisition/lab2/data/opamp_pressure_test.csv) | 804,60 | 641–1175 |

Esimese astme väljund küllastus vaakumkatses alumises otsas. ADC näit jäi platool vahemikku **14–21 koodi**, kuigi `adc_clipped` jäi nulliks. Lipp märgib ADC äärmisi koode ja võib jätta analoogastme küllastuse tuvastamata. Pumba seisuaja valimi standardhälve oli **2,90 koodi**. [Analüüs ja teise versiooni üleandmine](data-acquisition/lab2/docs/opamp_v2_handoff_2026-10-25.md).

Kolm CSV-d pärinevad ümberehitusele eelnenud `opamp` skeemist. Muudetud astmel tuleb veel kontrollida kolm rõhupunkti ja G5 pingeulatust koos siiretega. Lahtised tööd on ka rõhukalibratsioon, sama pumbaimpulsi `raw/opamp` mõõtepaarid, kahe kanaliga ostsillogrammid, spektrite ja signaali-müra suhte (SNR) võrdlus ning pumbajuhtimise võrdlus koos pooliku haarde katsega. [Labori kontrollnimekiri](data-acquisition/lab2/README.md#kontrollnimekiri) · [Arvutused](data-acquisition/lab2/docs/opamp_design.md) · [Pumbavõrdluse tööleht](data-acquisition/lab2/docs/pump_control.md).

## Laborid 1–3

| Labor ja seis | Füüsiline töö | Simulatsioon ja tarkvara |
| --- | --- | --- |
| [1 · Andur ja iseseisev pumbakast](data-acquisition/lab1/README.md) · lõpetatud | MPX5700AP otse G5-l, ACU2-B logi, oma pumbakasti katsed ja tähe edastus USB kaudu jaamale. Esitamise tähis on `data-acquisition-lab1`. | Falstadi müramudel ja tegelike logide [spektrianalüüs](data-acquisition/lab1/notebooks/lab1_spectra.ipynb). |
| [2 · Operatsioonvõimendi](data-acquisition/lab2/README.md) · töös | Kolm mõõteseeriat esimese astmega. Muudetud aste ja võrdluskatsed vajavad füüsilist kontrolli. | Falstadi näidisskeemid ja CSV analüsaator. AUTO-püsivara ADC eelvaade läbis tarkvaratestid. Selle versiooni riistvarakinnitus on lahtine. [Püsivara ja logija](data-acquisition/lab2/src/README.md#tarkvarakontroll). |
| [3 · Tilk ja IRQ](data-acquisition/lab3/README.md) · ette valmistatud | Plaanis on releega juhitav süstlaklapp, vaigu doseerimine, tilga pildilt mõõtmine, rõhukõverad ja UV-kõvendus. Füüsilised mõõtmised on ootel. | Plaanis on võrrelda filtreid enne rõhutuletise arvutamist ning katsetada komparaatorit ja katkestust (IRQ) vea korral. Jagatud Atomi projektis on klapi ja UV tarkvaramudel ning testid. [Teostusplaan](data-acquisition/lab3/src/README.md). |

## Süsteemi arhitektuur

```text
Rõhk voolikus → MPX5700AP ┬─ otse (Lab 1, raw) ────────────┐
                          └─ LM358N + pingejagur (Lab 2) ──┤
                                                           ↓
                                                    AtomS3R ADC (G5)
                                                           ↓ USB
                                                      Pythoni logija
                                                 ┌─────────┴─────────┐
                                                 ↓                   ↓
                                           CSV → analüüs       Lab 1 pumbaotsus
                                                               → MG400 DO → pump
```

Lab 2 haru kujutab 25.10 mõõteskeemi. Lab 2 logija kogub mõõteandmeid, pumbajuhtimise haru kuulub Lab 1 lahendusse. [Lab 1 süsteemiskeem (SVG)](data-acquisition/lab1/docs/lab1_system.svg) · [Muudetav draw.io skeem](data-acquisition/lab1/docs/lab1_system.drawio).

## Kaustad

| Asukoht | Sisu |
| --- | --- |
| [`data-acquisition/`](data-acquisition/) | Laborid `lab1/`, `lab2/` ja `lab3/`. Iga labori README-s on kontrollnimekiri, tulemused ja arenduspäevik. |
| `src/` | Atomi püsivara ja Pythoni logijad. Lab 3 kaustas on teostusplaan. |
| `data/` | Algsed mõõte- ja sündmuslogid. Lab 3 CSV-d on päiseridadega mallid. |
| `notebooks/` | Lab 1 Jupyteri märkmik, Lab 2 analüüsijuhend ja Lab 3 analüüsiplaan. |
| `docs/` | Skeemid, mõõteprotokollid, arvutused, komponendiloendid ja katseplaanid. |
| [`study-ru/`](study-ru/README.md) | Ülesannete mitteametlikud venekeelsed tõlked ja õppemärkmed. |

## Kiirstart ilma riistvarata

Ava terminal repo juurkaustas. Python 3 abil saad lugeda olemasolevat Lab 1 logi ja arvutada pumba tööaja osakaalu. Kõrvalfailist loeb skript ka iga võtmise sündmused.

```sh
python3 -B data-acquisition/lab1/src/python/analyze_run.py data-acquisition/lab1/data/lab1_pick10_fw3_02.10.26.csv
```

Lab 2 graafiku jaoks paigalda analüüsi sõltuvused. Allolev näide töötab macOS-is ja Linuxis. Keskkond ja väljundid lähevad ajutisse kausta.

```sh
work_dir=$(mktemp -d)
python3 -m venv "$work_dir/venv"
"$work_dir/venv/bin/python" -m pip install -r data-acquisition/lab2/notebooks/requirements.txt
MPLCONFIGDIR="$work_dir/mpl" "$work_dir/venv/bin/python" -B data-acquisition/lab2/src/python/analyze.py \
  data-acquisition/lab2/data/opamp_pump_off_test.csv \
  data-acquisition/lab2/data/opamp_vacum_test.csv \
  data-acquisition/lab2/data/opamp_pressure_test.csv \
  --out "$work_dir/results"
ls "$work_dir/results"
```

Tulemuste kaustas `"$work_dir/results"` on graafik `adc_time.png` ja kokkuvõte `summary.json`. Graafiku ühik on ADC kood. [Analüüsijuhend](data-acquisition/lab2/notebooks/README.md).

Lab 2 tarkvaratestide käivitamiseks jätka samas terminalis. Täiskomplekt vajab `c++` kompilaatorit ja PlatformIO ehitusega laaditud ArduinoJsoni päiseid. [Eeltingimused ja ehituskäsk](data-acquisition/lab2/src/README.md#tarkvarakontroll).

```sh
MPLCONFIGDIR="$work_dir/mpl" "$work_dir/venv/bin/python" -B -m unittest discover -s data-acquisition/lab2/tests -v
```

## Kaitsmisel

1. **Labor 1.** Alusta süsteemiskeemist ja näita pumba lülituspiire koos katse CSV-ga. Anduri arvutused ja müra käsitlus on [anduri mõõteprotokollis](data-acquisition/lab1/docs/sensor_choice.md). Graafikud leiad [spektrimärkmikust](data-acquisition/lab1/notebooks/lab1_spectra.ipynb) ja ostsilloskoobi vaate [FFT fotolt](data-acquisition/lab1/docs/lab1_scope_fft_13.09.26.jpg).
2. **Labor 2.** Näita [LM358N ühendusi](data-acquisition/lab2/docs/lm358n_wiring_2026-10-22.md), [astme arvutusi ja Falstadi näiteid](data-acquisition/lab2/docs/opamp_design.md) ning ülal toodud CSV-dest loodud ADC graafikut. Osuta vaakumi platoole ja [lahtistele kontrollpunktidele](data-acquisition/lab2/README.md#kontrollnimekiri).
3. **Labor 3.** Kõrvuta [ametlikku ülesannet](data-acquisition/lab3/assignment-EST.md) [kontrollnimekirja](data-acquisition/lab3/README.md#kontrollnimekiri) ja [mõõteplaaniga](data-acquisition/lab3/docs/bench_session.md). Näita, kuhu lähevad [tilgaandmed](data-acquisition/lab3/data/README.md), [retsept](data-acquisition/lab3/docs/recipe.md), [komparaatori simulatsioon](data-acquisition/lab3/docs/falstad/README.md) ja [ostsilloskoobi tõendid](data-acquisition/lab3/docs/scope/README.md).

## Seotud kursuseprojektid

- MG400 tööriistad, detailihoidikud ning süstla ja UV-lambi paigutus. [3D printimine ja CAD](https://github.com/Dennel04/3d-printing-course).
- Atomi kasutajaliides, robotijaam ja tööriistakaamera. [Nutikad Lahendused (Smart Solutions)](https://github.com/Dennel04/smart-solutions-course).

## Ohutus ja piirangud

- Labori 1 **141 Pa/kood** on anduri ülekandefunktsioonist ja ühe tööpunkti pingevõrdlusest arvutatud lahutus. Labori 2 ADC koodide teisendamiseks tuleb rõhukalibratsioon füüsiliselt kinnitada. Labori 2 CSV-de `p_kpa`, `voltage_v` ja `pump` väljad on tühjad. Katsetingimuse leiad protokollist.
- Lülita toide välja enne juhtmete muutmist. G5 ei talu 5 V. Enne G5 ühendamist kontrolli konkreetse ahela pingeulatust ka siiretel. LM358N toitepinge ja tarkvaratestid üksi ei kinnita sisendi ohutust. [Lab 2 ohutus](data-acquisition/lab2/README.md#ohutus).
- Ühenda 24 V pumbakasti DO-liinid vooluta kastiga ja keelatud robotiga. Hoia sisselülitatud MG400 tööala vaba ja hädastopp käeulatuses. Järgi vaigu ja UV-ga töötamisel labori kaitsejuhiseid. [Lab 1 ohutus](data-acquisition/lab1/README.md#ohutus) · [Lab 3 ohutus](data-acquisition/lab3/README.md#ohutus).
