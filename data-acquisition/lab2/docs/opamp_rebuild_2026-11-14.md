# Op-amp astme tõrkeotsing ja ümberehituse plaan 14.11.2026

Raimo kontrollis 14.11 [2. versiooni plaati](opamp_v2_handoff_2026-10-25.md).
Siin on kirjas tema mõõtmised, järeldus, Atomi püsivara muutus ja uue plaadi
paigutus. Arvud on Raimo teatatud multimeetri või G5 näidud. **Plaan**
tähistab veel ehitamata ja mõõtmata osa. Päevikukanne jääb meeskonna kirjutada.

## 1. Mõõtmised vanal plaadil

Must mõõteots GND-l. Andur ühendatud nagu
[25.10 tabelis](bench_session.md#katseskeemi-ühendused).

| Mõõtmine | Tulemus |
|---|---|
| C28 (anduri viik 1, `Vin`) ja B29 (GND) vahel | `0,468 V` |
| Rõhu muutmine süstlaga | Pinge ei muutunud |
| Anduri viik 3 | `5 V` |
| Anduri viik 2 | GND |
| Süstla tihendus anduri pordil | Kontrollitud, tihe |
| G5 (G5-mõõtja püsivara, vt punkt 3) lahtise juhtmega | ligikaudu `1,15 V` (ujuv sisend, mitte mõõtmine) |
| G5 ühendatud anduri väljundiga, andur endiselt plaadil | ligikaudu `0,5 V`, süstlaga ei muutunud |
| Andur plaadist lahti ühendatud | Andur töötab (Raimo kinnitus). Arvulised näidud jäid kirja panemata: TODO |

**Hinnang:** MPX5700AP on absoluutrõhuandur. 5 V toitel peaks atmosfääril
väljund olema ligikaudu `0,85 V` (Labor 1 mõõtis sama). `0,468 V` vastaks
valemi järgi ligikaudu 42 kPa absoluutrõhule. Anduri väljund annab
andmelehe järgi ainult umbes `0,1 mA` (output source current at full scale).
Plaadil koormas C28 sõlme miski, mis hoidis väljundit ligikaudu `0,5 V` juures,
viitepinge lähedal.

## 2. Järeldus

Andur töötab, vigased on vana maketeerimisplaadi ühendused. Täpset vigast
ühendust ei tuvastatud. Kahtlusalune oli vana B5K liuguri juhe `B22→C28`, sest
rida 22 kuulub 2. versioonis `Rref` ahelasse
([üleandmise punkt 2](opamp_v2_handoff_2026-10-25.md#2-plaadil-tehtud-muudatused-2-versioon)).
Seda ei kontrollitud. Raimo otsustas kõik komponendid tõsta uuele plaadile.

## 3. Atomi püsivara muutus

AtomS3R on Labor 2 ja Smart Solutionsi ühine seade.

| Samm | Tulemus |
|---|---|
| Varem seadmes olnud püsivara | `DA2_MEASURE_V1` (flash'i tekstiväljavõttes märk `# DA2_MEASURE_V1;no_network;no_actuators;nvs_blocked`). AUTO-versiooni seadmes ei olnud |
| Varukoopia enne üleslaadimist | Kogu 8 MB flash, `esptool read_flash 0 ALL`, port COM5. Fail on Raimo arvutis `Documents\atom-backups\atoms3r-before-g5meter-2026-11-14.bin`, SHA-256 `75815c7ea103845ea8d8c6d6a59621cbc14ca2f36ab8e7452047c5a0c2a5c0ed`. Repos seda ei ole: flash võib sisaldada salvestatud seadeid |
| Üles laaditud | [`src/firmware_g5meter`](../src/firmware_g5meter/src/main.cpp), build ja üleslaadimine `SUCCESS`, USB väljund kontrollitud |

G5-mõõtja näitab LCD-l G5 pinget ja MPX5700AP absoluutrõhku. Ekraani
puudutus seab hetke rõhu suhtelise rea nulliks. USB-le läheb CSV-rida
`t_ms,adc_raw,g5_volts,p_abs_kpa,p_rel_kpa` umbes 5 korda sekundis. Võrku,
pumpa, robotit ega NVS-i see ei kasuta (sama `nvs_guard.cpp` mis
`src/firmware`). Pinge teisendus kasutab Labor 1 tegurit `3,70 V / 4095`. Rõhk
eeldab 5,0 V toidet ja G5 otse anduri väljundil. Op-amp astme väljundil on
rõhurida vale, kehtib ainult pinge. Kalibreerimata.

**CSV logimiseks `logger.py`-ga** tuleb `DA2_MEASURE_V1` tagasi panna:

```powershell
python -m esptool --chip esp32s3 --port COM5 write_flash 0 atoms3r-before-g5meter-2026-11-14.bin
```

või ehitada ja üles laadida `src/firmware`. Smart Solutionsi töö jaoks tuleb
samuti õige püsivara tagasi panna.

## 4. Uue plaadi paigutus (plaan, ehitamata)

Vooluring jääb samaks: `Vout = A × Vin − (A − 1) × Vref`, `A = 1 + Rf/Rref`.
Muutused 2. versiooniga võrreldes:

| Osa | 2. versioon | Uus plaan | Põhjus |
|---|---|---|---|
| `Vref` jagur | 1 kΩ + B100K | 20 kΩ + B5K, reguleerimine 0…~1,0 V | ~3 korda täpsem seadmine ~0,5 V juures |
| `Rref` | 3 takistit (6,51 kΩ) + 2 × 1 kΩ | 6,8 kΩ + 2 kΩ | Vähem ühendusi |
| Puhvri allatõmbetakisti | 4,7 kΩ | 2 kΩ | **Hinnang:** täis puhumisel voolab `Rref` kaudu puhvrisse ~0,12 mA, 4,7 kΩ oli piiril |
| G5 jadatakisti | väärtus TODO | 3,3 kΩ | Piirab voolu, kui väljund tõuseb üle 3,3 V |
| Toide | juhtmed ridadesse 26/29 | toitesiinid mõlemal serval | Vähem hüppajaid |

Siht: täis imemisel `Vout ≈ 0,30 V`, täis puhumisel `≈ 2,80 V` (G5
`ADC_11db` lineaarses osas). Õppejõu näite sisendiga `0,40…1,56 V` annab see
`A ≈ 2,15` ja `Vref ≈ 0,49 V`. Tegelikud väärtused arvutatakse uuel plaadil
mõõdetud anduri otspunktidest (samm 2).

| Ühendus | Pesad |
|---|---|
| AtomS3R 5V / GND | J-poole + siin / − siin; sillad A-poole siinidele |
| LM358N | read 20–23, pin 1 = E20, pin 8 = F20 |
| Pin 8 / pin 4 | J20 → + siin / A23 → − siin |
| MPX5700AP 1 / 2 / 3 | C22 / A-poole − siin / A-poole + siin |
| Puhver | H22 → H21 (pin 6 → pin 7); 2 kΩ I21 → − siin |
| `Vref` jagur | 20 kΩ + siin → J30; B5K F30/F32/F34; J34 → − siin; liugur G32 → H23 (pin 5) |
| `Rref` | 6,8 kΩ B21 → B27; 2 kΩ D27 → G27; hüppaja J27 → J21 |
| `Rf` | 10 kΩ A21 → A15; hüppaja B15 → B20 |
| Väljund | 3,3 kΩ C20 → C12; G5 → A12 (alles viimases sammus) |

Ehitusjärjekord, iga samm kontrollitakse enne järgmist:

0. Tühja plaadi siinide pidevus (kas siin on keskelt katki), iga takisti
   lahtiselt mõõdetud väärtus.
1. Toitesiinid; mõlemal serval ~5 V.
2. Ainult andur, G5 ajutiselt A22-l: `Vin` atmosfääril, täis imemisel ja täis
   puhumisel. Nendest arvutatakse `Rref` ja `Vref`.
3. LM358N ja toide; pin 8 – pin 4 ~5 V.
4. Puhver: rida 21 F–J järgib liugurit (rida 32); seada arvutatud `Vref`.
5. `Rf` ja `Rref`; rida 22 A–E sisaldab ainult anduri juhet ja pin 3.
6. Ilma G5-ta: A− = `Vin` kõigil rõhkudel; seada `Vout` täis imemisel
   ~0,30 V; täis puhumisel ≤ 2,9 V; `Vref` püsib 2–3 mV piires.
7. 3,3 kΩ ja G5; G5 pinge = rida 20 ~10 mV piires.
8. Tulemused faili [`opamp_design.md`](opamp_design.md) ja päevikukanne.

## 5. Veel tegemata

- Plaadilt lahti ühendatud anduri arvulised näidud (atmosfäär, imemine, puhumine).
- Uue plaadi ehitus ja sammude 0–8 mõõtmised.
- Takistite lahtiselt mõõdetud väärtused.
- `DA2_MEASURE_V1` tagasi panemine enne CSV logimist.
