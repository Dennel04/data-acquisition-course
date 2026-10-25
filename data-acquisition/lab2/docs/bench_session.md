# Labor 2 esimese elektroonikasessiooni tööleht

Täida see leht mõõtepingi juures enne Atomi ADC ühendamist. Ära kasuta õppejõu näitearve mõõtetulemustena. Lülita toide välja enne juhtmete ümbertõstmist.

## 1. Riistvara tuvastamine

| Väli | Kontroll / märge |
|---|---|
| Op-ampi täpne markeering | `LM358N`, DIP-8; füüsiliselt korpuselt kinnitatud 04.10.26 |
| Anduri markeering | TODO: loe korpuselt; Labori 1 andur oli MPX5700AP |
| Maketeerimisplaat / toiteallikas | Üks suur MB-102 tüüpi jootmisvaba maketeerimisplaat; AtomS3R `5V` ja `G`/GND ühendati vastavalt punasele pluss- ja sinisele miinussiinile. Toitepinget ei mõõdetud. |
| Esimese versiooni jaoks füüsiliselt olemas olevad takistid | Nähtud nimiväärtused: `10 kΩ`, `20 kΩ`, `6,8 kΩ`, `47 kΩ`, `3,3 kΩ`. Kogused: TODO: count physically. Tegelikud takistused: TODO: real measurement required. |

Kontrolli op-ampi viigustik täpse korpusemarkeeringu andmelehelt enne toite ühendamist. Ära eelda, et riiulis olev detail on LM358 või et selle viigustik vastab teisele variandile.

### 04.10.26 ettevalmistuse seis

`LM358N` paiknes üle maketeerimisplaadi keskvahe ridadel 26–29. Korpuse täpi järgi vaadeldud suunas olid pin 1 poolel `e26`, pin 2 `e27`, pin 3 `e28`, pin 4 poolel `e29` ja pin 8 poolel `f26`. Maketeerimisplaadi sama rea ühendusi kasutades ühendati pin 4 rida sinise miinussiiniga ning pin 8 rida punase plussiiniga. AtomS3R päise algne ebaselge või vale ühenduskoht parandati enne toite ühendamist. Sessiooni andmed ei kinnita, et op-ampi ahelat pingestati. **Toide ja väljund ei olnud veel mõõtmisega kinnitatud.**

Labor 1 anduriahel jäeti terveks. Multimeeter seati alalispinge mõõtmiseks valmis; pingestamata ahela juures nähtud `0,000 V` ei ole mõõtetulemus. Ostsilloskoop oli klassis olemas, kuid seda ei kasutatud salvestatud Labor 2 mõõtmiseks.

### 11.10.26 diagnostika

Nikita ja Maksim kasutasid UNI-T UT139C multimeetrit ning toitsid AtomS3R-i USB kaudu. B5K potentsiomeeter mõõdeti ligikaudu `4,9 kΩ` ja B100K ligikaudu `94,8 kΩ`. Katses kasutati ajutise reguleeritava sisendina ainult B5K potentsiomeetrit; kumbki potentsiomeeter ei ole valitud lõpliku astme komponendiks.

Maketeerimisplaadil ühenduvad ühe rea pesad A–E omavahel ja F–J omavahel; keskvahe eraldab pooled. Katse eeldatud LM358N paigutus oli pin 1 = E26, pin 2 = E27, pin 3 = E28, pin 4 = E29 ning pin 8 rea 26 vastaspoole F–J rühmas. Enne järgmist pingestatud ülesehitust tuleb korpuse suund ja viigud uuesti kontrollida.

Ajutise katse ühendused:

- AtomS3R `5V` → G26;
- AtomS3R `G` → E29;
- B5K viigud → A21, A23 ja A25;
- B21 → C29;
- B25 → H26;
- C23 → D28;
- D26 → D27.

USB eemaldamise järel ei andnud `+5V` ja GND vaheline pidevuskontroll helisignaali, seega ei leitud ilmset tugevat lühist. Lühistatud multimeetri mõõteotsad andsid helisignaali ning kinnitasid pidevusrežiimi töö. Pidevus C26 ja C27 vahel andis lõpuks helisignaali. LM358 toiteviikude pidevus kinnitati.

Mõõdetud LM358 pin 8 ja pin 4 vaheline pinge oli ligikaudu `5 V`. Kontroll D29 ja H26 vahel andis ühe korra vastuolulise `0,027 V`, kordusmõõtmine andis `5,2 V`. Neid näite ei ühendata üheks keskmiseks ega peideta; järgmine ülesehitus peab leidma erinevuse põhjuse.

B5K liugur muutus ligikaudu vahemikus `0…5,2 V` ja seati väärtusele `0,401 V`. Pingejärgija esimene väljund C26 ja D29 vahel oli `0 V`, kuigi ligikaudu `0,4 V` sisendi korral oodati sama suurusjärku. Sisend C28 ja D29 vahel näitas eri hetkedel ligikaudu `3,9 V`, `5,222 V` ja `0,4 V`. Väljund C26 ja D29 vahel oli hiljem ligikaudu `3,9 V` ka pärast sisendi tagasiseadmist ligikaudu `0,4 V` juurde. **Pingejärgija ei töötanud õigesti ja vea põhjus jäi leidmata.**

ADC-d ei ühendatud. `3,9 V` ega `5,2 V` ei ole ADC ohutuse tõend. LM358 sisend ligikaudu `3,9…5,2 V` võib 5 V toite korral jääda lubatud ühispingevahemikust välja, seega tuleb järgmine katse teha pärast paigutuse kontrolli ligikaudu `0,4 V` sisendiga. MPX5700AP mõõtmised atmosfääril, täis imemisel ja täis puhumisel jäävad TODO.

Ühenduste täielik taastamisloend ja veaolek: [`diagnostic_2026-10-11.md`](diagnostic_2026-10-11.md).

## 2. Toite mõõtmised

Mõõda alalispinget. Ühenda multimeetri must juhe enne punast juhet.

| Mõõtmine | Must mõõteots | Punane mõõteots | Toetatud suurusjärk | Mõõdetud väärtus |
|---|---|---|---|---|
| Anduri toitepinge, V | Anduri GND viik või sama kinnitatud ühine maa | Anduri Vcc viik | Laboris 1 mõõdeti `5,00 V`; mõõda selle sessiooni väärtus uuesti | TODO: `V` |
| LM358 toitepinge otse toiteviikude vahel, V | Täpse variandi andmelehe järgi op-ampi negatiivne toiteviik `V−` / GND | Täpse variandi andmelehe järgi op-ampi positiivne toiteviik `V+` | Ülesanne kasutab `5 V` eeldust; tegelik väärtus on teadmata | TODO: `V` |

## 3. Raw-anduri mõõtmised

Mõõda anduri `Vin` enne op-ampi ehitamist. Hoia must mõõteots anduri GND viigul või samal kinnitatud ühisel maal. Pane punane mõõteots anduri `Vout` viigule. Ära mõõda rõhku oletuse järgi: kirjelda, kuidas voolik ja pump iga punkti ajal olid ühendatud.

| Tööpunkt | Rõhuolukorra kirjeldus | Must mõõteots | Punane mõõteots | Toetatud suurusjärk | Mõõdetud `Vin` |
|---|---|---|---|---|---|
| Atmosfäär | TODO: toru avatud atmosfääri, pump väljas; kinnita tegelik olukord | Anduri GND / kinnitatud ühine maa | Anduri `Vout` | Laboris 1 mõõdeti atmosfääril `0,85 V` | TODO: `V` |
| Täis imemine | TODO: kirjelda ühendus ja saavutatud rõhuolukord | Anduri GND / kinnitatud ühine maa | Anduri `Vout` | Õppejõu MPX5700AP näites umbes `0,40 V`; see ei ole meeskonna mõõtetulemus | TODO: `V` |
| Täis puhumine | TODO: kirjelda ühendus ja saavutatud rõhuolukord | Anduri GND / kinnitatud ühine maa | Anduri `Vout` | Õppejõu MPX5700AP näites umbes `1,56 V`; see ei ole meeskonna mõõtetulemus | TODO: `V` |

Märgi iga punkti juurde ka multimeetri vahemik ja näidu stabiilsus, kui näit kõigub. Ära kasuta ühe punkti hetkelist äärmust otspunktina ilma seda kirja panemata.

## 4. Ohutu tööjärjekord

A. Lülita toide välja enne juhtmete muutmist.

B. Mõõda kõigepealt anduri väljund atmosfääril, täis imemisel ja täis puhumisel.

C. Arvuta op-ampi aste mõõdetud `Vin` otspunktidest enne Atomi ADC ühendamist.

D. Ehita op-ampi ahel kontrollitud viigustiku ja arvutatud takistitega.

E. Lülita ahelale toide. Kui komponent kuumeneb, lõhnab või voolutarve on ootamatu, lülita toide välja.

F. Mõõda op-ampi väljund multimeetriga kõigis kolmes rõhupunktis. Hoia must mõõteots ühisel maal ja punane mõõteots op-ampi `Vout` sõlmel.

G. Kui `Vout` võib ületada ADC jaoks kontrollitud ohutu sisendpinge, ära ühenda Atomit.

H. Ühenda ADC alles pärast seda, kui mõõdetud väljund jääb kogu töövahemikus kontrollitud ohutusse piirkonda.

Ühenda või muuda 24 V pumbakasti DO-liine ainult siis, kui robot on keelatud ja pumbakast vooluta. Ära suuna avatud survevoolikut inimese poole.

Ülesande esimese versiooni siht `0,2…3,3 V` ja parandatud versiooni näidissiht `0,3…3,0 V` on projekteerimissihid. `3,3 V` ei ole selle töölehe põhjal mõõdetud ega kinnitatud AtomS3R ADC ohutuspiir. Kontrolli kasutatud viigu, sumbuvuse ja kiibi lubatud sisendpinge ametlikust dokumentatsioonist ning mõõda valmis astme väljund enne ühendamist.

## 5. Op-ampi väljundi kontroll enne ADC-d

| Tööpunkt | Must mõõteots | Punane mõõteots | Arvutatud `Vout`, V | Mõõdetud `Vout`, V | ADC-ga ühendamine lubatud? |
|---|---|---|---:|---:|---|
| Atmosfäär | Ühine maa | Op-ampi `Vout` | TODO: calculate after raw measurements | TODO | TODO: verify safe range |
| Täis imemine | Ühine maa | Op-ampi `Vout` | TODO: calculate after raw measurements | TODO | TODO: verify safe range |
| Täis puhumine | Ühine maa | Op-ampi `Vout` | TODO: calculate after raw measurements | TODO | TODO: verify safe range |

## Send these numbers back for calculation

```text
OPAMP marking = LM358N, DIP-8 (physically confirmed 04.10.26)
V_sensor_supply =
V_opamp_supply =
Vin_atmosphere =
Vin_full_suction =
Vin_full_blowing =
Available resistors = 10 kΩ, 20 kΩ, 6.8 kΩ, 47 kΩ, 3.3 kΩ nominal; quantities not counted; resistance not measured
```

Lisa ühik voltides iga pinge juurde. Takistite puhul lisa ühik, kogus ja võimaluse korral multimeetriga mõõdetud väärtus.

## 6. Mõõtmisprogrammi kasutuselevõtt

See on katseplaan, mitte läbiviidud mõõtmine. Tarkvara juhend ja CSV skeem: [src/README.md](../src/README.md).

### Elektriline kontroll enne G5 ühendamist

1. Jäta G5 lahti. Lülita kõik toited välja. Kontrolli tegeliku LM358 korpuse suunda, tootja viigustikku, tagasisideahelat, ühise maa pidevust, katkestatud toitesiine ja lühiste puudumist. Ära järelda õiget viiku ainult vanast breadboard'i koordinaadist.
2. Pingesta ainult kontrollitav anduri/op-ampi ahel. Mõõda ja kirjuta üles anduri toide, LM358 toide, `V_ref`, anduri väljund ning astme väljund ühise maa suhtes. Korda atmosfääril, imemisel ja puhumisel; lisa meetod, aeg, mõõteriist ja ühikud. Kontrolli LM358 sisendi ühispinge- ja väljundulatust kasutatud toitel.
3. Kontrolli väljundit ka toite sisse-/väljalülitamisel ning üleminekutel, võimalusel ostsilloskoobiga. Üks `3,009 V` näit 22.10 ei kinnita kogu ahela ohutust, lineaarsust ega transientide puudumist. Varasemad vastuolulised LM358 näidud vajavad endiselt selgitamist.
4. MPX5700AP 5 V toitega andmelehe väljund võib ulatuda ligikaudu 4,7 V-ni. Ka 5 V LM358 väljund ei ole iseenesest ADC-kindel. `ADC_11db` ei muuda G5 viiku 5 V taluvaks; ESP32-S3 selle sumbuvuse mõõtevahemik on kuni ligikaudu 3,1 V, mitte piiramatu ohutusvahemik. Vajadusel arvuta ja kontrolli sobiv piiramine/jagur õpetajaga, ära vali kaitsetakisteid oletuse järgi.
5. Kui väljund on negatiivne, üle kontrollitud lubatud piiri, ebastabiilne, küllastuses või komponent kuumeneb, katkesta katse. Ära ühenda G5. Ainult multimeeter ei välista lühikesi ülepingepiike.
6. Ühenda G5 ainult pärast kogu töövahemiku ja üleminekute kontrolli ning õpetajaga kinnitatud sobivust; ühenda juhtmed väljalülitatud toitega. Tee sama kontroll eraldi `raw` ja `opamp` ühendusele. Logija `--electrical-check-confirmed` on kasutaja kinnitus, mitte elektriline kaitse.

Allikad: [MPX5700 andmeleht](https://www.nxp.com/docs/en/data-sheet/MPX5700.pdf), [LM358 tootja dokumentatsioon](https://www.ti.com/product/LM358), [ESP32-S3 ADC dokumentatsioon](https://docs.espressif.com/projects/esp-idf/en/v4.4.7/esp32s3/api-reference/peripherals/adc.html).

### Andmete kogumise järjekord

1. Pärast eraldi lubatud üleslaadimist kontrolli kõigepealt ainult USB-ga LCD ja logija käivituskinnitust. Lahtise G5 näit on ujuva sisendi vaatlus, mitte rõhumõõtmine; hoia see eraldi smoke-test failis. Püsivara peab ootama `measure_start` käsku.
2. Pärast elektrilist kontrolli kogu ühendatud `raw` signaalist 10 s püsipunkti jooks. Võrdle ajatemplite sagedust 100 Hz sihiga; 10 s jooks annab ligikaudu 1000 proovi, täpne arv tuleb logi järgi. Kirjuta sama stabiilse sõlme multimeetrinäit `--dmm-v` abil ning töölehele.
3. Kogu mitu kontrollitud pingepunkti kummagi konfiguratsiooni jaoks. Ära rakenda vana Atomi `3,70 V / 4095` tegurit uuele seadmele kinnitatud kalibratsioonina. Alles päris kalibratsiooni ja rõhureferentsi järel saab tuletada pinge/kPa ning teha kPa-põhist SNR analüüsi; esialgses CSV-s jäävad need väljad tühjaks.
4. Kogu sama määratletud pumbaimpulss vähemalt 30 korda `raw` ja vähemalt 30 korda `opamp` konfiguratsioonis, nagu nõuab [ametlik ülesanne](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLab%202%5D%20EST.md). Ühine CSV, erinevad `config/run_id/trial`, samad tingimused ja kestus. Säilita ebaõnnestunud jooksud ning põhjendus, ära kirjuta neid üle.
5. Pumpa selles etapis tarkvara ei juhi. Impulsi tekitamine, vooliku ühendus ja ohutu käsitsi juhtimine tuleb laboris eraldi kokku leppida. DO-liinid ühenda ainult keelatud roboti ja vooluta pumbakastiga; automaatne pump ja MG400 liikumine ei kuulu siia etappi.
6. Märgi katsetingimus (`atmosphere`, `pulse`, `calibration` jne), tegelik ühendus, toide ja multimeetri mõõteaeg töölehele. Hilisemad spektrid, SNR, pooliku haarde test ja pumbajuhtimise võrdlus jäävad TODO, kuni andmed ning kalibratsioon on olemas.

## 22.10.2026 — LM358N katseskeemi mõõtmised (Maksim)

Allikas: Maksimi [muutmata Word](sources/lab2-sborka-2026-10-22.docx).
Viigustik, komponentide koordinaadid ja juhtmete täielik loend on
[eraldi koostamisjuhendis](lm358n_wiring_2026-10-22.md). Järgnev mõõtetabel
säilitab juba avaldatud väärtused; see ei ole uus mõõtesessioon.

Koostasime LM358N-põhise katseskeemi maketeerimisplaadil. Esimese kanali sisendpinge määrati B5K potentsiomeetriga. Teise kanali abil puhverdati B100K potentsiomeetriga seatud viitepinge.

Kõik pinged mõõdeti ühise maa suhtes.

| Mõõtepunkt | Kirjeldus | Tulemus |
|---|---|---|
| H26 | LM358N toitepinge | 5,00 V |
| C28 | Mitteinverteeriv sisend (+) | 0,402 V |
| C27 | Inverteeriv sisend (−) | 0,403 V |
| J27 | Puhverdatud viitepinge | 0,520 V |
| C26 | Võimendi väljund | 0,205 V |

### Takistuste mõõtmised

| Komponent | Mõõdetud väärtus |
|---|---|
| Tagasisidetakisti | 10,04 kΩ |
| Kolm järjestikku ühendatud takistit | 6,51 kΩ |

### Väljundi reguleerimine

B5K potentsiomeetri reguleerimisel mõõtsime võimendi väljundis 3,009 V.

See väärtus näitab ühte saavutatud tööpunkti, mitte kogu väljundpinge vahemikku.

Pärast mõõtmist ühendasime LM358N väljundi AtomS3R ADC sisendiga G5. Ühendamine toimus väljalülitatud USB-toitega.

### Veel tegemata

- MPX5700AP anduri tegelike väljundpingete mõõtmine.
- Kolme rõhupunkti mõõtmine.
- Ostsilloskoobiga signaali kontrollimine.
- ADC programmi käivitamine.
- Mõõteandmete salvestamine CSV-faili.
- Müra ja signaali-müra suhte analüüs.

**Märkus:** selles katses kasutati anduri asemel reguleeritavat testpinget. Rõhuanduri mõõtmistulemusi veel ei ole.

## 24.10.2026 — LM358N katseskeemi ja AtomS3R ADC kontroll (Maksim)

Jätkasime LM358N katseskeemi mõõtmist. B5K potentsiomeeter tekitas sisendpinge ning B100K potentsiomeeter viitepinge. LM358N väljund oli ühendatud AtomS3R GPIO5 ADC sisendiga.

### Multimeetri mõõtmised

| Mõõtepunkt | Tulemus |
|---|---:|
| Sisendpinge `Vin` | 0,402 V |
| Viitepinge `Vref` | 0,526 V |
| Võimendi väljund `Vout` | 0,190 V |

### ADC mõõtmine

Kasutasime AtomS3R-i USB-ühenduse kaudu ADC väärtuste lugemiseks.

| Näitaja | Tulemus |
|---|---:|
| Mõõtmiste arv | 1001 |
| Kestus | ligikaudu 10 s |
| Diskreetimissagedus | ligikaudu 100 Hz |
| ADC keskmine | 188,43 koodi |
| ADC miinimum | 182 koodi |
| ADC maksimum | 196 koodi |

### Järeldus

Katseskeemi väljundpinget oli võimalik mõõta multimeetriga ja ADC väärtusi lugeda AtomS3R abil. Kasutati potentsiomeetritega tekitatud testpinget, mitte MPX5700AP rõhuandurit.

Rõhu kalibratsioon, kolme rõhupunkti mõõtmised, ostsilloskoobipildid ning `raw` ja `opamp` signaalide võrdlus on veel tegemata.

## 25.10.2026 — MPX5700AP rõhuanduri, LM358N võimendusastme ja AtomS3R ADC mõõtmised (Maksim)

### Katse eesmärk

Kontrollida MPX5700AP rõhuanduri signaali lugemist LM358N võimendusastme ja AtomS3R G5 ADC kaudu ning salvestada kolm mõõteseeriat: väljalülitatud pump, vaakum ja ülerõhk.

### Katseskeemi ühendused

Kasutati MPX5700AP rõhuandurit, LM358N operatsioonvõimendit, B100K potentsiomeetrit viitepinge seadmiseks, kahte `10 kΩ` takistit pingejagurina ning AtomS3R mikrokontrollerit.

Toite- ja signaaliühendused:

| Komponent | Ühendus |
|---|---|
| AtomS3R `5V` | Maketeerimisplaadi H26, +5 V toitesõlm |
| AtomS3R GND | Maketeerimisplaadi D29, ühine maa |
| MPX5700AP viik 1 (`Vout`) | C28, LM358N viigu 3 sisendsõlm |
| MPX5700AP viik 2 (`GND`) | B29, ühine maa |
| MPX5700AP viik 3 (+5 V) | I26, +5 V toitesõlm |
| LM358N viik 1 (väljund) | E26, väljundsõlm |
| LM358N viik 2 (inverteeriv sisend) | E27 |
| LM358N viik 3 (mitteinverteeriv sisend) | E28 |
| LM358N viik 4 (GND) | E29 |
| LM358N viik 8 (+5 V) | F26 |
| Esimene `10 kΩ` pingejaguri takisti | B26 → A35 |
| Teine `10 kΩ` pingejaguri takisti | D35 → C29 (GND) |
| AtomS3R G5 ADC | E35, pingejaguri keskpunkt |

Maketeerimisplaadi A35–E35 pesad kuuluvad samasse elektrilisse sõlme. Seetõttu on G5 ühendatud kahe `10 kΩ` takisti keskpunkti, mitte otse LM358N väljundisse.

Tagasisideahelas kasutati mõõdetud takistusi `10,04 kΩ` ja `6,51 kΩ`. B100K potentsiomeetriga seatud viitepinge oli ligikaudu `0,633 V`. Takistite ja potentsiomeetri kõiki täpseid maketeerimisplaadi pesakohti ei ole selles protokollis kinnitatud.

### Pingemõõtmised

AtomS3R G5 sisendsõlmes täheldati järgmisi multimeetri näite:

| Tingimus | G5 pinge |
|---|---:|
| Pump välja lülitatud | 0,592 V |
| Pumba töötamise ajal täheldatud maksimaalne väärtus | 0,952 V |

Need on eraldi multimeetri vaatlused, mitte iga ADC proovi juurde salvestatud pingeväärtused.

### ADC mõõteseeriad

Salvestati kolm ligikaudu 10 sekundi pikkust mõõteseeriat, igaühes ligikaudu 1000 ADC lugemit. Kasutati `opamp` konfiguratsiooni.

| Katse | CSV-fail | Min ADC | Max ADC | Keskmine ADC | Standardhälve |
|---|---|---:|---:|---:|---:|
| Pump välja lülitatud | [opamp_pump_off_test.csv](../data/opamp_pump_off_test.csv) | 642 | 667 | 657,62 | 2,90 |
| Vaakum | [opamp_vacum_test.csv](../data/opamp_vacum_test.csv) | 14 | 837 | 511,54 | 306,76 |
| Ülerõhk | [opamp_pressure_test.csv](../data/opamp_pressure_test.csv) | 641 | 1175 | 804,60 | 185,60 |

Väljalülitatud pumba mõõteseerias oli ADC näidu kõikumine väike. Vaakumi ja ülerõhu mõõteseeriate standardhälbed sisaldavad ka signaali tegelikke muutusi ning neid ei saa käsitleda üksnes mürana.

### Katsete käigus täheldatud muutused

**Vaakumkatse.** Pärast vaakumi vähendamist või pumba väljalülitamist tõusis ADC näit lühiajaliselt ligikaudu `805` koodini ja püsis kõrgenenud umbes kaks sekundit. Võimalik selgitus on ajutine rõhumuutus pumba või ventiili ümberlülitamisel. Seda põhjust ei ole eraldi mõõtmisega kinnitatud.

**Ülerõhukatse.** ADC näit vähenes ligikaudu `1126 → 940 → 860` koodini, millele järgnes järsk langus. Üks võimalik selgitus on aeglane rõhukadu ja sellele järgnev rõhu vabastamine. Täpne põhjus vajab kontrollimist.

### Järeldus ja piirangud

MPX5700AP, LM358N ja AtomS3R G5 kaudu oli võimalik salvestada pumba tööga seotud ADC signaalimuutusi.

Samas ei ole rõhk veel kalibreeritud `kPa` ühikutesse. CSV-failide `p_kpa`, `voltage_v` ja `pump` väljad ei sisalda proovipõhiseid mõõteväärtusi. Pumba töörežiimid on määratud katsemärkmete ja failide nimetuste, mitte CSV `pump` veeru põhjal.

Kolm mõõteseeriat ei võimalda veel teha nõutavat sama protokolli `raw` ja `opamp` võrdlust, määrata Pa/ADC sammu ega arvutada kinnitatud SNR-i.

### Järgmised tegevused

- Mõõta anduri sisendpinge ja võimendi väljundpinge kontrollitud rõhupunktides.
- Kontrollida G5 pinget kogu töövahemikus, sealhulgas üleminekute ajal.
- Korrata katseid võrreldavas `raw` konfiguratsioonis.
- Kalibreerida ADC näit rõhuks.
- Teha võrreldavate mõõteseeriate müra-, spektri- ja SNR-analüüs.
