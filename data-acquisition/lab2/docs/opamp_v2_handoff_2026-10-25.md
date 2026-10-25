# Op-amp astme 2. versioon ja üleandmine 25.10.2026

Raimo andis maketeerimisplaadi ja töö seisu üle Maksimile. Siin on kirjas,
mis 25.10 pärast [Maksimi jaguriga mõõtmisi](../README.md#arenduspäevik)
plaadil muudeti, mis on mõõdetud ja mis on veel tegemata. Arvud on Raimo
teatatud multimeetri näidud; **hinnang** tähistab arvutust, mitte mõõtmist.
Päevikukanne jääb meeskonna kirjutada.

## 1. Mida jaguriga CSV-d näitasid

Allikad: [`opamp_pump_off_test.csv`](../data/opamp_pump_off_test.csv),
[`opamp_vacum_test.csv`](../data/opamp_vacum_test.csv),
[`opamp_pressure_test.csv`](../data/opamp_pressure_test.csv). G5 sai
`10 kΩ / 10 kΩ` jaguri kaudu poole LM358N väljundist.

| Tähelepanek | Alus |
|---|---|
| ADC ja multimeeter on kooskõlas | Pump väljas: E35 `0,592 V` multimeetriga, ADC keskmine `657,6` koodi → `0,90 mV/kood`; Labori 1 tegur oli `3,70 V / 4095 = 0,9035 mV/kood` |
| Vaakum on alumises piiris kinni (küllastus) | Vaakumi platool ADC `14…21` koodi, standardhälve `1,23` koodi; atmosfääril `2,90` koodi. Väiksem müra näitab, et väljund on vastu alumist piiri, mitte ei järgi signaali |
| ADC vahemikust on kasutusel väike osa | Kogu salvestus `14…1175` koodi `4095`-st |
| `adc_clipped` jääb `0` | Lipp ei märka põrandat ~17 koodi juures |
| Metaandmed on vanad | Kõigis kolmes `dmm_reference_v = 0.19`, `condition = test_signal`, `trial = 1` (24.10 potentsiomeetrikatsest); `pump` on tühi |

**Hinnang:** jaguriga oli netovõimendus `2,542 × 0,5 ≈ 1,27`. Jagur kaitses
G5-t, kuid kaotas poole signaalist ja suurem osa op-ampi kasust läks kaduma.

## 2. Plaadil tehtud muudatused (2. versioon)

Lähtepaigutus: [`lm358n_wiring_2026-10-22.md`](lm358n_wiring_2026-10-22.md).

| Muudatus | Seis |
|---|---|
| B5K eemaldatud | Tehtud. Rida 22 kuulub nüüd `Rref` ahelasse |
| Juhe J42 → A22, sealt kaks `1 kΩ` jadamisi kuni A− sõlmeni (rida 18 / B18) | Tehtud. Täpsed vaheread: TODO, kontrolli plaadilt |
| Vana juhe J42 → A27 | Foto järgi eemaldatud; kontrolli |
| `Rref` ahela takistus J33 → A27 | `7,93 kΩ` mõõdetuna **ahelas** (rööpteed läbi `Rf` ja op-ampi); eraldi lahti ühendatuna mõõtmata. Nimiväärtuse järgi `6,51 + 2 × 1 = 8,51 kΩ` |
| Jaguri alumine `10 kΩ` (E35 → B29) eemaldatud | Raimo: "arvatavasti tehtud"; foto järgi eemaldatud |
| Jaguri ülemine takisti → jadatakisti G5 ette | Väärtus (kas `10 kΩ` jäi või vahetati `3,3 kΩ` vastu): TODO |
| `4,7 kΩ` allatõmbetakisti puhvri väljundist (pin 7 rida) GND-sse | Lisatud. Täpne pesa: TODO |
| Pidevuskontroll | Raimo teatel korras |

Ühenduste täistabel koos sõlmede kontrolliga on töös arutatud; plaadi täpsed
uued read tuleb selle dokumendi tabelisse lisada.

## 3. Viitepinge ja LM358 väljundi neeldevool

| Olukord | J27 miinimum (B100K madalaimas asendis) |
|---|---|
| Enne allatõmbetakistit | `0,675 V` |
| Pärast `4,7 kΩ` lisamist | `0,35 V` |

**Põhjus (hinnang):** anduri sisendiga atmosfääril on A− ligikaudu `0,85 V`.
Kui `Vref` on sellest madalam, peab puhvri väljund voolu **neelama**. LM358
väljund suudab maa lähedal neelata vaid umbes `12…50 µA` ([TI LM358
andmeleht](https://www.ti.com/lit/ds/symlink/lm358.pdf), output sink current
at VO = 200 mV). Allatõmbetakisti laseb op-ampil voolu anda, mitte neelata.
Jäänud `0,35 V` on ahela ja allatõmbetakisti tasakaalupunkt. See ei sega,
kui vajalik `Vref` on sellest kõrgemal. 22.10 ja 24.10 potentsiomeetrikatses
seda ei ilmnenud, sest sisend `0,40 V` oli `Vref`-ist madalam.

**Kontrollimata risk:** täis puhumisel (Vin ~`1,56 V`, andmelehe näide)
läheb ahelast J27 sisse rohkem voolu, kui `4,7 kΩ` ära juhib. `Vref` võib
siis tõusta. Kui J27 muutub täis puhumisel rohkem kui `2…3 mV`, pane
`3,3 kΩ` rööbiti `4,7 kΩ`-ga (~`1,9 kΩ`) ja sea `Vref` uuesti.

## 4. Abiarvutus (andmelehe näide, mitte meeskonna lõplik arvutus)

Aste: `Vout = A × Vin − (A − 1) × Vref`, kus `A = 1 + Rf/Rref`.

- Nimiväärtustega `A = 1 + 10,04/8,51 ≈ 2,18`. Kasuta lõplikus arvutuses lahti
  ühendatult mõõdetud `Rref`-i.
- Õppejõu MPX5700AP näite sisendiga `0,40…1,56 V` ja alumise sihiga `0,30 V`:
  `Vref = (2,18 × 0,40 − 0,30)/1,18 ≈ 0,48 V`; ülemine ots siis ~`2,9 V`.
- Tegelik `Vref` tuleb arvutada meeskonna **mõõdetud** `Vin` otspunktidest.

## 5. Järgmised sammud (Maksim)

G5 hoida lahti kuni sammuni 5. Must mõõteots D29-l.

1. Toide sisse; H26 pinge kirja.
2. Kontrolli täis puhumisel J27 püsivust (punkt 3); vajadusel tugevam allatõmbetakisti.
3. Mõõda atmosfääril, täis imemisel ja täis puhumisel korraga C28 (`Vin`),
   J27 (`Vref`) ja C26 (`Vout`). Võrdle `Vout` valemiga. Täis imemisel ei tohi
   `Vout` olla kinni ~0 V juures, täis puhumisel peab see jääma alla ~`3,1 V`.
4. Mõõda `Rref` ahel lahti ühendatult ja jadatakisti väärtus; lisa read sellesse dokumenti.
5. USB välja, ühenda E35 → G5, USB sisse. Logi kolm jooksu õigete
   metaandmetega, näiteks:

   ```powershell
   .\.venv\Scripts\python.exe src/python/logger.py --port COM3 --config opamp --csv data/opamp_v2.csv --condition atmosphere --trial 1 --duration 10 --dmm-v <E35 näit> --electrical-check-confirmed
   .\.venv\Scripts\python.exe src/python/logger.py --port COM3 --config opamp --csv data/opamp_v2.csv --condition full_suction --trial 2 --duration 10 --append --electrical-check-confirmed
   .\.venv\Scripts\python.exe src/python/logger.py --port COM3 --config opamp --csv data/opamp_v2.csv --condition full_blowing --trial 3 --duration 10 --append --electrical-check-confirmed
   ```

6. Kanna parandatud astme tulemused faili [`opamp_design.md`](opamp_design.md)
   ("Parandatud versiooni kolme punkti mõõtmine") ja lisa päevikukanne.
   Jaguriga mõõtmised jäävad esimese versiooni tulemustena alles.
