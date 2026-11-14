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

- 14.11.26 parandus: hiljem samal päeval mõõtis Raimo anduri üksi uuel plaadil (ehitussamm 2): täis imemisel `0,32 V`, atmosfääril `0,831 V`, täis puhumisel `2,40 V`. Mõõtmisviis (multimeeter või G5-mõõtja) ja anduri toite täpne pinge jäid kirja panemata: TODO. Vt [punkt 6](#6-1411-hilisem-täpsustus-mõõdetud-vahemik-ja-muudetud-plaan).

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

- 14.11.26 parandus: allolev plaan (20 kΩ + B5K, `Rref` 6,8 kΩ + 2 kΩ, siht õppejõu näite järgi) asendati samal päeval mõõdetud vahemiku põhjal. Kehtiv plaan ja tegelikud pesad on [punktis 6](#6-1411-hilisem-täpsustus-mõõdetud-vahemik-ja-muudetud-plaan). Allolev tabel jääb esialgse plaanina alles.


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
  - 14.11.26 parandus: mõõdetud, `0,32 / 0,831 / 2,40 V` (punkt 6).
- Uue plaadi ehitus ja sammude 0–8 mõõtmised.
- Takistite lahtiselt mõõdetud väärtused.
- `DA2_MEASURE_V1` tagasi panemine enne CSV logimist.

## 6. 14.11 hilisem täpsustus: mõõdetud vahemik ja muudetud plaan

Raimo mõõtis anduri üksi ja vaatas üle tegeliku plaadi. Siin on sellest
tulenev plaan. Arvutused on **hinnang** kuni ehituse ja mõõtmiseni (sammud 4–7).

| Anduri väljund | Pinge |
|---|---|
| Täis imemine | `0,32 V` |
| Atmosfäär | `0,831 V` |
| Täis puhumine | `2,40 V` |

Vahemik `2,08 V` on õppejõu näitest (`1,16 V`) peaaegu kaks korda laiem, seega
on vaja väiksemat võimendust.

| Osa | Esialgne plaan (punkt 4) | Muudetud plaan |
|---|---|---|
| Potentsiomeeter | B5K + 20 kΩ | **B100K** (plaadil olemas), liugur → 47 kΩ → sõlm X (rida 32) → 10 kΩ → GND; X → pin 5. Reguleerimine 0…~0,88 V |
| `Rref` | 6,8 kΩ + 2 kΩ | 6,8 kΩ + **47 kΩ** = 53,8 kΩ |
| Võimendus `A` | ~2,15 | `1 + 10/53,8 ≈ 1,19` |
| `Vref` | ~0,49 V | `(1,186 × 0,32 − 0,30)/0,186 ≈ 0,43 V` |
| `Vout` imemine / atmosfäär / puhumine | – | ~`0,30` / ~`0,91` / ~`2,77 V` |
| G5 filter | puudus | 0,1 µF G5 sõlmest GND-sse; koos 3,3 kΩ-ga piirsagedus ~480 Hz, 100 Hz signaal ~98 % |
| Puhvri allatõmbetakisti | 2 kΩ | jääb 2 kΩ. Suurema `Rref`-iga on tagasivool täis puhumisel vaid ~`(2,40 − 0,43)/53,8 kΩ ≈ 37 µA` |

Tegelikud pesad uuel plaadil. Siinipaarid on prinditud järjekorras + ja −, nii
et A-poolel on + välimine ja J-poolel sisemine joon:

| Ühendus | Pesad |
|---|---|
| MPX5700AP | plaadil J1–J6 (pin 1 sälgu juures J1-s). I1 → C22 (`Vin`), I2 → J-poole −, I3 → J-poole + |
| AtomS3R | plaadil: 5V D62, GND D63, G5 H60, G8 H63. A62 → A-poole +, A63 → A-poole − |
| Siinide sillad | J+ → A+ reas 46, J− → A− reas 48 |
| LM358N | read 20–23 (enne umbes ridadel 25–29, tuleb ümber tõsta). J20 → J-poole +, A23 → A-poole − |
| B100K | J34 (üla), J36 (liugur), J38 (ala). I34 → J-poole +, I38 → J-poole − |
| Nõrgendi | 47 kΩ I36 → I32; 10 kΩ G32 → G38; hüppaja H32 → H23 (pin 5) |
| Puhver | H22 → H21; 2 kΩ I21 → J-poole − |
| `Rref` | 6,8 kΩ B21 → B27; 47 kΩ D27 → G27; hüppaja J27 → J21 |
| `Rf` | 10 kΩ A21 → A15; hüppaja B15 → B20 |
| Väljund | 3,3 kΩ C20 → C12; 0,1 µF E12 → A-poole −; hüppaja A12 → J60 (G5 rida) |

Seis: anduri vahemik mõõdetud (samm 2). Sammud 3–8 on veel tegemata.
