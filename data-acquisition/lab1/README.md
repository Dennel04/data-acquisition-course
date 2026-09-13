## Andmehõive: Labor 1 — Andur, ja kompressor, mis ise seisma jääb

**Töömaht:** 32 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 12.09.26 | **Tellimise kuupäev:** 22.09.26 | **Esimene kaitsmine:** 06.10.26, veebis

### Kuidas see dokument töötab

* Kopeeri see fail esimesel päeval oma repo laborikausta `README.md`-ks ja täida seal, töö käigus.
* KAARDISTA ise on puudu, sest vastust ei tea veel keegi. Sina ise mõõdad ja kirjutad numbri ja põhjuse siia.
* Midagi ei kustutata. Vale number jääb, kuupäevaga, parandus tuleb tema alla.
* Kirjuta nii, et meeskonnakaaslane, kes sel päeval ruumis ei olnud, saab aru: päris failinimed, päris numbrid, ühikud.
* Skeemid ja simulatsioonid lähevad dokumenti pildina, pildi juurde link elavale failile, et teine saaks selle lahti teha ja edasi muuta. Näited: osas 2 Falstadi simulatsioon, osas 3 draw.io skeem. Tee enda omad samade tööriistadega.
* Tähtaeg ei ole tähtis. Tähtis on, et asi saab tehtud ja sa saad aru. Ei tulnud esimesel korral välja, tule homme tagasi ja proovi uuesti. Kaitsta saab nii mitu korda, kui vaja.

### Eesmärk

Laboris on viis MG400 ja viis pumbakasti. Üks neist on tark: mõõdab rõhku ja laseb pumbal seista, kui rõhk on käes. Neli ülejäänut töötavad nii kaua, kui DO liin on üleval, ükskõik, mis torus toimub. Kõik viis peavad käituma nagu tark. Selleks läheb igasse väljundtorusse oma andur, AtomS3 ekraanile rõhk ja otsus, ja arvutisse Python, mis loeb Atomit UART-USB kaudu ja lülitab pumba MG400 DO liini kaudu. Aasta lõpuks on see loogika tööriista trükkplaadil. Praegu on ta maketeerimisplaadil, kus viga maksab ühe juhtme. Sama meeskond teeb kõiki kolme ainet: sama Atom saadab ka tähe, mille robot joonistab. Kolm ainet, üks demo: **vajuta tähte, robot joonistab selle.**

Selles laboris on kolm asja:

1. **Andur.** Pumbakast teeb −70 … +110 kPa. Vali andur, mis näeb mõlemat märki, ja ütle numbritega, miks just see. Esimesel päeval on MPX5700AP vanade asjade kastist.
2. **Tark kast.** Logi tehase tark kast enne, kui ise midagi disainid. Kaks lülituspunkti ja tsükli aeg.
3. **Sinu kast.** Atom otsustab, ekraan näitab, arvuti lülitab. Pump jääb ise seisma imemisel ja puhumisel, ja robot võtab sellega klaasi.

Esimene asi on tellimus. Esimesel päeval uusi osi ei ole: mõtle välja, mida see labor üldse vajab ja mis riiulil puudu on, ja kirjuta see tellimuseks, mis läheb välja 22.09. Tellitu jõuab kohale selle labori ajal. Seni ehita sellest, mis riiulil on.

*See on elav dokument. Uuenda eesmärke, kui need töö käigus muutuvad — uued teadmised teevad vanad eesmärgid vahel mõttetuks. Mõte on hoida meeskond kogu aeg sihil, et ei eksitaks detailide metsa ja põhiprobleem ei jääks lahendamata.*

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

### Kontrollnimekiri

**Peab olema tehtud**

- [x] Tellimus 22.09: mis selle labori jaoks riiulil puudu on, anduri valik numbritega.
  - 13.09.26: osa 1 võrdlustabel valmis (`docs/sensor_choice.md`) — MPX5700AP vs MPX4250AP (absoluutne, 20-250 kPa) vs MPX5100GP+MPXV6115V (kaks manomeetrilist) päris andmelehtede numbritega (mV/kPa, Pa/samm, skaala %, väljundpinge meie -70…+110 kPa akna peal). Otsus: jääme MPX5700AP juurde — kõik kolm alternatiivi annavad küll parema lahutuse, aga nende väljund meie vahemikus ületab 3,3V (vajaks jagurit/OP-ampi, mida osa 2 veel ei luba). `docs/bom.md` loodud: kontrollisime riiulit, kõik selle labori jaoks vajalik oli juba olemas — tellimust ei läinud vaja (null-tulemus, põhjendatud).
- [x] MPX5700AP maketeerimisplaadil, Atom näitab kPa, logija kirjutab CSV 100 Hz.
  - 12.09.26: andur maketeerimisplaadil, juhtmestik parandatud (vale/hõljuv kontakt GND-rööpal; andur oli algul valepidi paigaldatud — mõlemad leitud multimeetriga). Stage A (`firmware_stageA_sanity/`) prošitud, töötab: toores ADC → Serial. Vout = 0,85 V (multimeeter, vastab README ootusele), ADC naiivse valemiga 0,758 V — ~11% lahknevus, seletatud ja üles kirjutatud failis `docs/sensor_choice.md`. Sellest tuletatud tegelik V_ref ≈ 3,70 V on juba sisse viidud `firmware/src/sensor.cpp` faili.
  - 12.09.26 (hiljem samal päeval): täisfirmware (`firmware/`) prošitud, ekraan näitab kPa (ekraani virvendus kõrvaldatud M5Canvas topeltpuhverdusega). `python/logger.py` testitud päris andmetega (`data/lab1_smartbox_acu2b_12.09.26.csv`) — 35800 rida 358.0 s peale, ~100 Hz kinnitatud.
  - 13.09.26: 2%-kontroll tehtud (0,5% lahknevus, vt `docs/sensor_choice.md`), 10s logi kontroll tehtud (1002 rida), LSB-müra pump väljas/sees mõõdetud, Falstad-skeem müraallikaga tehtud ja lingitud.
  - 13.09.26: ostsilloskoop (GW Instek GDS-1072A-U) saadud ja proovitud spektri jaoks — täielikult ei õnnestunud (skaala "libises" sessiooni jooksul, vt `docs/sensor_choice.md` täielik lugu). Kvalitatiivselt kinnitatud: pumba käivitamisel toores CH1 signaal muutub nähtavalt aktiivsemaks (amplituud kasvab), välja lülitades rahuneb — allikas-kinnitus olemas, aga konkreetset Hz-sagedust nimeliselt kinnitada ei õnnestunud. See osa jääb osaliselt lahtiseks, kui rohkem aega tekib enne kaitsmist.
  - Lahti: spektri tipud nimeliselt (mootor/MG400/USB/50Hz) formaalselt kinnitamata, vt oskilloskoobi katse ülal.
- [x] Targa kasti logi olemas, kaks lülituspunkti teada.
  - 12.09.26: ACU2-B logitud 5.97 min, tulemused failis `docs/pump_control.md`. Üks lülituspunkt kindel (väljalülitus ≈ -91,5 kPa), teine (sisselülitus) ei vallandunud selle akna jooksul — napp klaasil pidas nii hästi, et leket/teist tsüklit ei tekkinud. Loetakse kehtivaks tulemuseks, mitte veaks.
- [ ] Sinu kast jääb ise seisma imemisel ja puhumisel. USB välja, pump välja.
  - 12.09.26: kõik kolm holding-stsenaariumi mõõdetud (osa 4, täistabel `docs/pump_control.md`): napp klaasil (max -83,06 kPa, taastumine 310,7 s), napp õhus (max ainult -12…-15 kPa, taastumine 17,0 s), voolik korgiga (max -83,34 kPa, peaaegu kadudeta ~30s, siis üks järsk aste -58 kPa peale, stabiilne ≥240s).
  - 13.09.26: riba valitud otse CSV-de pealt arvutades (`docs/pump_control.md`): off=-75kPa, on=-40kPa, seisuaeg-alampiir=15s, käivitusi/min-ülempiir=4. Väljalülitus (-75) on napp õhus'ele füüsiliselt saavutamatu (seal max ainult -15,46kPa) — see iseenesest väldib lühitsüklit selles stsenaariumis, ilma et seisuaeg seda tööd peaks tegema. Klaasil taaskäivitub alles +102s pärast tippu — palju alla 4/min piiri. Lahtine (üle selle, mida ülesanne otseselt küsib): napp õhus ei jõua kunagi väljalülitusrõhuni, st jääks tööle lõputult, mitte lühitsükliteks — soovitus lisada eraldi max-tööaja turvapiir, veel realiseerimata.
  - 13.09.26: leiti ja parandati reaalne puudujääk — `logger.py` ei saatnud kunagi `min-off-ms`/`max-cycles-per-min` prošivile, ja `main.cpp` ei kutsunud kunagi `setSafetyLimits()`. Lisati protokolli uus käsk `{"cmd":"limits",...}`, prošivi kompileeritud ja üles laetud uuesti (COM6).
  - 13.09.26: **`logger.py` käivitatud ilma `--dry-run`-ta** — Atom otsustab ise, arvuti ainult vahendab MG400 DO liinidesse. 143.6s, 8 tsüklit: tööaeg ~1.5-1.6s, seisuaeg täpselt 15000ms (min-off-time töötab), väljalülitus stabiilselt -75...-76kPa (sihtmärk tabatud), 3.34 tsüklit/min (alla 4/min piiri). Aus leid: reaalne kokkupandud süsteem (koos roboti haaratsi haruga) kaotab vaakumi -75-lt peaaegu atmosfäärini alla 15 sekundiga — kordades kiiremini kui osa 4 võrdluskõveral (102s), tõenäoliselt lisaleke haaratsi haru juures. Andmed: `data/lab1_autonomous_run_13.09.26.csv`, täisanalüüs `docs/pump_control.md`.
  - 13.09.26: kontrollitud otse — klaas tõsteti iminapaga õhku (mitte lauale surutud) ja vaakum hoidis stabiilselt -76…-79kPa terve 30s vaatlusakna — varasem "leke" oli katsemeetodi (klaas laual) artefakt, mitte päris süsteemi (torud/haarats) probleem. Riba jääb samaks.
  - Aus reservatsioon: 30s ei ole veel võrreldav ACU2-B 6-minutilise testiga (osa 3) — piisab, et ümber lükata "leke torudes" hüpotees, aga mitte, et väita "hoiab sama kaua kui tark kast". Järgmine samm: korrata sama testi (klaas õhus) mitme minuti vältel.
  - Puudu: kümme võtmistsüklit robotiga (pumba töötsükkel) veel mõõtmata.
- [ ] Täht: nupp valib tähe, Atom saadab selle jaama.
- [ ] Repo ja arenduspäevik täidetud, tag `data-acquisition-lab1`.
  - 12.09.26: arenduspäevik käivitatud (vt allpool). Tag ja repo lõplik koristus jäävad kaitsmise eelseks sammuks.

### Sisendid

* Riiulilt: AtomS3, MPX5700AP, maketeerimisplaat, passiivkomplekt, multimeeter, ostsilloskoop, 4 mm voolik, T-liitmik, vooliku kork, iminapp, polükarbonaatklaas.
* Õppejõult: MG400 koos oma pumbakastiga, tehase tark kast kordamööda, MG400 baaspakett Pythonis, kus on DO sisse ja välja: [KKallas/mg400-base](https://github.com/KKallas/mg400-base).
* Nutikad Lahendused L1: kanal tähe jaoks, lepitakse kokku esimesel nädalal.

### Vahendid

1. AtomS3 ×2, USB-C kaablid
2. MPX5700AP; sinu valitud andur, kui tellimus kohale jõuab
3. Maketeerimisplaat, juhtmed, takistite ja kondensaatorite komplekt, multimeeter
4. Ostsilloskoop FFT funktsiooniga
5. 4 mm voolik, T-liitmik, vooliku kork, iminapp φ13 või φ16, 24 × 24 mm klaas
6. MG400 koos pumbakasti ja baaspaketiga
7. Arduino IDE või PlatformIO ESP32 jaoks; Python 3, pyserial, Jupyter Lab, numpy, pandas, scipy, matplotlib
8. Falstad skeemisimulaator, draw.io skeemide jaoks
9. Git, üks repo meeskonna kohta, `AGENTS.md` juurkaustas

*Kui plaan muutub, uuenda ka vahendeid, või tee draw.io skeem, mis näitab, kuidas asjad omavahel töötavad.*

**KAARDISTA ISE — mida sa päriselt kasutasid.**

### Taustainfo

* **AtomS3**: viigud, ADC viigud, ekraan, nupp
  [https://docs.m5stack.com/en/core/AtomS3](https://docs.m5stack.com/en/core/AtomS3)
* **ESP32 ADC ja UART Arduinos**
  [https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/](https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/)
  [https://randomnerdtutorials.com/esp32-uart-communication-serial-arduino/](https://randomnerdtutorials.com/esp32-uart-communication-serial-arduino/)
* **pyserial**, arvuti pool
  [https://pyserial.readthedocs.io/](https://pyserial.readthedocs.io/)
* **Andurid**
  MPX5700AP: [https://www.nxp.com/docs/en/data-sheet/MPX5700.pdf](https://www.nxp.com/docs/en/data-sheet/MPX5700.pdf)
  MPX5100DP: [https://www.nxp.com/docs/en/data-sheet/MPX5100.pdf](https://www.nxp.com/docs/en/data-sheet/MPX5100.pdf)
  NXP MPX pere tähed: AP absoluutne, GP manomeetriline, DP diferentsiaalne, V vaakum. Absoluutandur näeb mõlemat märki, manomeetriline ainult ühte.
* **Pumbakast**: otsi fraasi "Dobot MG400 vacuum pump box IO control". Kaks DO liini; klemmid juhendist.
* **Kuidas rõhulüliti kompressoril töötab**: otsi fraasi "compressor pressure switch cut-in cut-out hysteresis short cycling".
* **Falstad**: [https://www.falstad.com/circuit/circuitjs.html](https://www.falstad.com/circuit/circuitjs.html)
* **Fourier**: [https://docs.scipy.org/doc/scipy/reference/fft.html](https://docs.scipy.org/doc/scipy/reference/fft.html) ja `scipy.signal.welch`

*Lisa siia oma allikaid ja kasulikku infot, mis aitaks sul projektist aru saada ka aastaid hiljem, kui selle uuesti lahti teed.*

**KAARDISTA ISE — sinu allikad.**

### Osad

#### 1. Mida tellida

See tuleb enne ehitamist. Käi labor paberil läbi ja mõtle välja, mida üldse tellida vaja on. Iga osa kohta: mis asju see küsib, mis on riiulil, mis on puudu. Puuduv läheb tellimusse.

Suurim küsimus on andur. Kandidaadid: üks absoluutandur, mille skaala katab 30–210 kPa; kaks manomeetrilist andurit, üks plussile ja üks vaakumile; või jääbki MPX5700AP. Iga kandidaadi kohta andmelehelt samad numbrid: tundlikkus mV/kPa, Pa ühe ADC sammu kohta, skaala kasutus protsentides, väljund 3,3 V vastu. Null-tulemus on ka tulemus: kui MPX5700AP on selle töö jaoks piisav, kirjuta see numbritega.

Kui osas 2 on müra mõõdetud ja osas 4 riba teada, lisa tabelisse riba jagatud müraga. Riba peab olema müra kohal kordades, mitte protsentides. Kui valik selle peale muutub, kirjuta see kuupäevaga vana otsuse alla.

Kirjuta üles: tabel ja otsus faili `docs/sensor_choice.md`; tellimus Mouseri tootekoodidena faili `docs/bom.md` 22.09-ks, iga rea juures üks lause, milline osa või number seda küsib.

#### 2. Andur ja esimene signaal

MPX5700AP maketeerimisplaadil: 5 V, GND, Vout → ADC viik. Andur otse ADC-sse, vahel ei ole midagi: ei jagurit, ei op-ampi, ei filtrit. See on meelega. Labor 2 paneb vahele kõigepealt jaguri, siis op-ampi, ja võrdleb nelja spektrit. Võrdlus on olemas ainult siis, kui toores signaal on siin mõõdetud ja alles. Multimeeter enne, kui Atom külge läheb: toide 5 V, Vout atmosfääril umbes 0,85 V. Atomil iga 10 ms: loe ADC → kPa → ekraan → üks rida UART-i. Arvutis Python, mis kirjutab CSV veergudega `t_ms, adc, p_kpa, pump`. Kontroll: 10 s logi on 1000 ± 5 rida, ja ADC on multimeetriga 2 % piires nõus.

MPX5700AP on vale skaalaga, aga absoluutne, ja atmosfäär on tema skaala sees: −70 kPa on 31 kPa absoluutset, +110 kPa on 211 kPa, väljund 0,40–1,56 V. Kogu pumba ulatus on 26 % tema skaalast, umbes 125 Pa ühe ADC sammu kohta. Ülekandefunktsioon: `Vout = 5 · (0.0012858 · P + 0.04)`, P kPa absoluutne.

Kirjuta üles: Pa ühe ADC sammu kohta, müra LSB-des pump väljas ja pump sees, spektri tipud nimedega (pumba mootor, MG400 servod, USB toide, 50 Hz), vähemalt kaks neist kontrollitud allika väljalülitamisega. Falstadi skeem andur → ADC koos müraallikaga, simuleeritud müra mõõdetu vastu.

Falstadi algus: andur on vahelduvpingeallikas 0,2–5 V, ADC sisend on modelleeritud järgurina, mis lõikab 0 ja 3,3 V vahele. See on ADC mudel, mitte signaaliaste. Skoop ADC viigul näitab, kus signaal ära lõigatakse. Lisa sellele oma müraallikas. [Ava simulatsioon (müraallikaga, 4.4mV 50Hz — vt `docs/sensor_choice.md`, sagedus on oletus, ostsilloskoopi polnud)](https://www.falstad.com/circuit/circuitjs.html?ctz=DwYwlgTgBAZgvAIgAwKgFwM6KQOiUgRlTBEQNwCZ8KB2GgZiQA4KA2ATnZtRACNEArCigAHfgiGoAbhEGoAtpkEBTALQEiAPgBQUKMClQAHmVZIojACxQCZmzVap4yVAHdnRWLISf5AQyMpRAocS1ReMD8sBBDHAHodPWAAc2NTcysbO3p6R1hsBATdfT80hEzbc0t8LOFnJgU-RHocegUwAqhkpp98PsLE-VcyistrCoIKJwKipOGTcqRrDQooavMV6ZdZobL1m0m1msqtlB3gecR9yrX2VlrTgeLgAHk9u9qoATGH-J9UDCkbaDYBGPbmCg-DT3SHcP7CDAdHxTdDKRAAQQAdgATACu0CQABoKIBkAgEUAAak8kmCFhQPhQqGtbFBGW14QCkZNUGg0Qh0QARADCUHkuNxOPxUCQJPohPolOp+lpVw+BA+31W6vYjygiLIKN5GOFUCkYDAAGslQYyuqtQ5WdV7HkPHl3GQnN5JKKAkFkHglmFzpcfOx7fcbgQHI9g2VIRsHRVoxzzgB7KDKTGIOEYESmLZGFF5lyDJIiU2dQFyHZljOdP0IoECa1xVMg9OZ7MA4u2AtFj2l-TlhsApsttvaYBxcAQHRAA)

![Falstad: andur 0,2–5 V → ADC mudel 0–3,3 V, 4.4mV 50Hz müraallikaga](lab1_falstad_adc.png)

#### 3. Tark kast

T-liitmik tehase targa kasti väljundtorusse, napp otsas, napp klaasi peal. Pump imemisele baaspaketi CLI-st. Logi viis minutit.

Kirjuta üles: väljalülitusrõhk, sisselülitusrõhk, pumba tööaeg, seisuaeg, käivitusi minutis. Need viis numbrit on sinu kasti sihtmärk.

Kuidas asjad omavahel töötavad: arvuti, robot, pumbakast, andur, Atom ja haarats. [Ava draw.io skeem](https://drive.google.com/file/d/1YczRgRYat7b16Y7tdC8Wtg52FTfknlgd/view?usp=sharing)

![draw.io: arvuti, MG400, pumbakast, andur, AtomS3, haarats](lab1_drawio_tark_kast.png)

#### 4. Sinu kast

Sama T sinu meeskonna tavalise kasti torusse. Atom saab arvutist režiimi ja riba, otsustab ise ja näitab ekraanil rõhu, režiimi ja otsuse. Arvuti kirjutab iga rea CSV-sse ja tõmbab DO liini otsuse järgi. Kui 500 ms jooksul rida ei tule, DO maha. Ohutu olek on lihtne: kui midagi on valesti, pump seisab.

```
Atom → arvuti:  {"t":123456,"adc":2011,"p":-52.3,"mode":"suction","pump":1}
arvuti → Atom:  {"cmd":"mode","mode":"suction"}   {"cmd":"band","on":-40,"off":-60}   {"cmd":"stop"}
```
```
iga 10 ms: loe ADC → kPa → ekraan → rida UART-i
imemine:  kui p on sisselülitusrõhust nõrgem ja seisuaeg ≥ alampiir → pump 1
          kui p on väljalülitusrõhust tugevam → pump 0
puhumine: sama, teise märgiga
off, lugem skaalast väljas, käivitusi minutis üle piiri → pump 0, ekraanil põhjus
```

Hoidmine: pump välja väljalülitusrõhul, logi langemist kuni sisselülitusrõhuni. Kolm olukorda: napp klaasil, napp õhus, voolik korgiga. Sealt tuleb riba laius, seisuaja alampiir ja käivituste ülempiir. Napp õhus ei tohi lühitsüklitesse minna: kast, mis iga sekund käivitub, ei ole tark, ta on katki.

Võtmine: robot viib napi klaasile, imemine, tõst, koht, puhumine, lahti. Kümme korda.

Kirjuta üles: riba, seisuaja alampiir, käivitusi minutis kolmes olukorras, rõhk napp klaasil ja napp õhus, pumba töötsükkel kümne võtmise ajal. Kõik koos loogikaga faili `docs/pump_control.md`. Jaam võtab need üle nii, nagu nad on.

#### 5. Täht

Lühike vajutus käib tähestikku läbi, pikk vajutus saadab `{"letter":"A"}` Nutikate Lahendustega kokkulepitud kanalisse. Jaam loeb, robot joonistab.

**KAARDISTA ISE — vastused.** Iga osa kohta: numbrid, ühikud, kus fail on. Tegemata asja kohta üks rida, miks.

### Ohutus

* USB ja 5 V välja, enne kui juhet liigutad. Viigud andmelehelt. ADC viik ei kannata 5 V; andur, mille väljund käib 4,7 V-ni, ei lähe täisskaalal otse viiku.
* Pumbakast on 24 V. DO liinid ühendatakse siis, kui robot on keelatud ja kast vooluvõrgust väljas.
* Pumba mootor ei ole tehtud iga sekund käivituma. Seisuaja alampiir enne, kui riba kitsaks lähed. Kui kast on soojem kui käsi, riba laiemaks.
* Lahtine voolik +110 kPa juures lendab; ära suuna kellegi poole. Napp −70 kPa juures ei lähe nahale.
* Robot: käed ei ole laual, kui robot on sisse lülitatud. Esimene jooks aeglaselt, hädastopp käeulatuses.
* Selles laboris ei joodeta.

### Komponendid selle labori jaoks

Tellimus läheb välja 22.09.26 ja jõuab kohale enne kaitsmist. Valmis nimekirja ei ole: meeskond paneb tellimuse ise kokku osa 1 põhjal. Mõtle näiteks, kas MPX5700AP jääb või tuleb uus andur ja kas ka varuks, ja kas voolikuliitmikke ja korke jätkub.

### Hindamiskriteeriumid

| Kategooria | Punktid |
| :--- | :--- |
| Tööfailid — Atomi püsivara, Pythoni logija ja pumba juhtimine, CSV failid | 5 p |
| Analüüs — Pa ühe ADC sammu kohta, spektrid nimedega, targa kasti numbrid, hoidmiskõverad, anduri valik | 5 p |
| Prototüüp — sinu kast jääb ise seisma imemisel ja puhumisel, USB välja = pump välja, robot võtab klaasi, täht jõuab jaama | 5 p |
| Dokumentatsioon — README, arenduspäevik, `pump_control.md`, `sensor_choice.md`, `bom.md`, AGENTS.md | 5 p |
| **Kokku** | **20 p** |

### Kaitsmine

Link git repole, tag `data-acquisition-lab1`.

Kaitsmine on lihtne suuline 15 minuti jutuajamine. Näitad, kuidas sinu kast ise seisma jääb ja uuesti käivitub, kui nappi kergitad, ja avad oma arenduspäeviku. Õppejõud küsib umbes viis küsimust selle kohta, kuidas sa selle tegid. Kui esimesel korral ei õnnestu, tuled uuesti.

Repos on kaustas `data-acquisition/lab1/`: `src/` püsivara ja logijaga, `data/` CSV failidega, `notebooks/` spektritega, `docs/` skeemi foto, ostsilloskoobi pildi, Falstadi ekspordi ja kolme md-failiga, see fail kui `README.md`, ja `AGENTS.md` uuendatud.

### Arenduspäevik

**KAARDISTA ISE — päevik.** Üks sissekanne iga töösessiooni kohta, kirjutatud iseendale, nii et inimene, kes seal ei olnud, saab aru. Sissekandeid lisatakse, mitte ei muudeta.

**12.09.26 — Denys, Raimo**
* Tegime: Panime kokku MPX5700AP + AtomS3R skeemi maketeerimisplaadil (Vout → G5, GND ja Vcc plaadi rööbaste kaudu, ilma jaguri/op-ampita, vastavalt osale 2). Raimo uuris skeeme ja ühendusi, Denys kogus kõik vajalikud detailid kokku. Kontrollisime AtomS3 andmelehte/manuaali viikude jaoks, testisime ühendust multimeetriga, kirjutasime Stage A püsivara (toores ADC → Serial) koos Claude'iga. Teel leidsime kaks reaalset viga ja parandasime need käsitsi.
* Juhtus (numbrid): Enne parandust Vout ~0,47 V ega reageerinud survele üldse (viga: GND-rööbas hõljus/OL, andur oli valepidi paigas). Pärast GND-rööpa parandamist (~0,2–0,3 Ω) ja anduri ümberpööramist: Vout = 0,85 V atmosfääril (multimeeter) — vastab README ootusele täpselt. Stage A ADC (naiivne valem `raw × 3,3/4095`, 8x keskmistatud) andis ~0,758 V — ~11% lahknevus multimeetrist, korduv kahel sõltumatul mõõtepunktil (nii enne kui pärast andurit ümber pööramist). Tagasi arvutatud tegelik ADC opinguvool: V_ref ≈ 3,3 × (0,85/0,758) ≈ 3,70 V.
* Otsustasime, ja miks: lahknevus on süstemaatiline (kordub kahel sõltumatul mõõtmisel samas suhtes), mitte müra ega halb kontakt — seega vahetame koodis ADC nominaalse 3,3 V eelduse mõõdetud 3,70 V vastu (`firmware/src/sensor.cpp`, `adcReferenceVolts()`). Täielik lugu ja tabel on failis `docs/sensor_choice.md`.
* Lahti järgmiseks korraks: täisfirmware (`firmware/`) prošimine koos kPa väljundi, JSON-protokolli ja 10 ms tsükliga; `python/logger.py` testimine (kõigepealt `--dry-run`, ilma MG400-ta); kontrollida, et uue V_ref'iga jõuab ADC vs multimeeter 2% piiresse (osa 2 nõue). Osa 1 (anduri valiku võrdlustabel) ja `docs/bom.md` on veel puutumata.

**12.09.26 (2. seanss) — Denys, Raimo**
* Tegime: Prošisime täisfirmware (`firmware/`) COM6 peale. Ekraan virvendas tugevalt (`fillScreen()`+`printf()` otse paneelile 100 Hz) — parandasime M5Canvas topeltpuhverdusega (kogu kaader joonistatakse mällu, üks `pushSprite()` tõmbab tervikuna ekraanile) ja lahutasime ekraani värskenduse (150 ms) 10 ms anduri/JSON tsüklist. Kirjatüüpi suurendasime (1 → 1,5). Seejärel läksime osa 3 juurde: T-liitmik ACU2-B (tehase "tark" imikäpa juhtplokk) väljundtorusse, napp käsitsi klaasi peale, üks `suck`-käsk CLI kaudu, edasi käsi eemal, `python/logger.py --mode off --dry-run` logis 5,97 minutit.
* Juhtus (numbrid): Log: 35800 rida, 358,0 s, ~100 Hz kinnitatud. Rõhk langes stardist (-4,23 kPa) väljalülituseni (-91,51 kPa) 4,15 sekundiga, seejärel jäi täiesti lauge kõveraks ülejäänud ~353 sekundiks — teist tsüklit ei tulnud. Täisanalüüs ja tabel: `docs/pump_control.md`.
* Otsustasime, ja miks: loeme selle kehtivaks tulemuseks, mitte veaks — napp pidas klaasil nii hästi, et leket polnud piisavalt, et sisselülitusrõhk selle akna jooksul vallanduks. Väljalülitusrõhk (-91,5 kPa) ja tööaeg (4,2 s) on kindlad numbrid; sisselülitusrõhk ja käivituste sagedus jäävad "≥"-hinnanguks, kuni pikem logi või tahtlik väike leke (osa 4 "napp õhus" stsenaarium) annab teise tsükli.
* Lahti järgmiseks korraks: osa 1 (anduri võrdlustabel, tellimus 22.09-ks), osa 4 kolm holding-stsenaariumi (napp klaasil / napp õhus / voolik korgiga) päris meeskonna enda MG400-kastiga, `docs/bom.md` alustamata.

**12.09.26 (3. seanss) — Denys, Raimo**
* Tegime: Seadistasime `mg400-base` veebilehe (`mg400 serve`, Brave brauseris) päris MG400 roboti juhtimiseks (robot juba varem ENABLED, IP 192.168.1.6 ping'itav). Leidsime ja lahendasime vea: "Sync sliders to robot" tundus katki, aga tegelik põhjus oli, et keegi polnud lehel `Enable` vajutanud — ilma selleta `servo_active` jääb `false` ja käsk `/api/move` ei liiguta kätt kuigi vastab 200 OK. Pump (vaakum/blow) töötas kogu aeg, kuna see on eraldi alamsüsteem. Pärast probleemi mõistmist alustasime osa 4 esimest holding-stsenaariumi: T-liitmik meeskonna enda (mitte ACU2-B) pumbakasti torusse, napp käsitsi klaasil, vaakum sisse kuni maksimumini, siis käsitsi välja täpselt tipus, ja logisime passiivset lekke-kõverat kuni atmosfäärini.
* Juhtus (numbrid): Log 39829 rida, 398,3 s, ~100 Hz kinnitatud. Vaakum jõudis maksimumini -83,06 kPa (~12-16 s tööaeg), misjärel rõhk taastus iseenesest atmosfäärini (≥ -2 kPa) **310,7 sekundiga (~5,18 min)**. Erinevalt ACU2-B testist (kus leket ei tekkinud 6 minuti jooksul) taastus see täielikult — seega selle napi/klaasi kombo leke on selgelt suurem kui ACU2-B omal.
* Otsustasime, ja miks: see on esimene täielik lekke-kõver (mitte ainult alumine piir nagu ACU2-B puhul) — sellest saab juba valida reaalse riba (on/off kPa) ja seisuaja alampiiri osa 4 jaoks, kui ka teised kaks stsenaariumi (napp õhus, voolik korgiga) on mõõdetud.
* Lahti järgmiseks korraks: stsenaarium 2 (napp õhus) ja 3 (voolik korgiga) sama meetodiga; seejärel reaalsete numbritega `logger.py` käivitamine ilma `--dry-run`-ta, et Atomi enda otsus (mitte käsitsi CLI) juhiks pumpa; osa 1 ja `docs/bom.md` endiselt puutumata.

**12.09.26 (4. seanss) — Denys, Raimo**
* Tegime: Lõpetasime osa 4 holding-stsenaariumid 2 ja 3 sama meetodiga (käsitsi suck kuni maksimumini, käsitsi off tipus, passiivne logimine). Stsenaarium 2: napp vabas õhus, ei puuduta midagi. Stsenaarium 3: napp asendatud vooliku korgiga.
* Juhtus (numbrid): Stsenaarium 2 (napp õhus, 9376 rida, 93,75 s): pump suutis tõmmata ainult -12…-15 kPa platoole (avatud otsa vastu ei jõua sügavamale), taastumine atmosfäärini 17,0 sekundiga. Stsenaarium 3 (voolik korgiga, 31193 rida, 311,9 s): maksimum -83,34 kPa (peaaegu sama, mis klaasiga!), esimesed ~30s peaaegu kadudeta, siis üks järsk aste (~5s jooksul -81,2 → -59,6 kPa — meeskond kinnitas, et midagi tahtlikult ei puudutatud, tõenäoliselt väike juhuslik nihe), edasi stabiilne uus platoo ≥240 sekundit ilma edasise triivita.
* Otsustasime, ja miks: kõik kolm stsenaariumit koos annavad selge pildi — leke süsteemis tuleb peaaegu täielikult napi-pinna kontaktist, mitte pumbast/klappidest endist (puhas pneumaatika korgiga hoiab peaaegu sama hästi kui klaas, avatud õhk on ainuke, mis reaalselt "lekib" kiiresti). Täisvõrdlustabel ja järeldus: `docs/pump_control.md`.
* Lahti järgmiseks korraks: nende kolme kõvera põhjal valida päris on/off kPa riba ja seisuaja alampiir; käivitada `logger.py` ilma `--dry-run`-ta, et Atomi enda prošivi (mitte käsitsi CLI/veebileht) otsustaks pumba üle ise; kontrollida USB-välja-tähendab-pump-välja nõuet; osa 1 (anduri valik) ja `docs/bom.md` (tähtaeg 22.09) endiselt puutumata.

### Väljundid ja tulemused

**Väljundid**
* Nutikad Lahendused L1: täht jaama; pumba juhtimise loogika ja lülituspunktid failis `docs/pump_control.md`.
* Andmehõive L2: maketeerimisplaat, 100 Hz logija, CSV formaat, esimesed spektrid toore signaaliga, mille vastu jagur ja op-amp võrreldakse.
* Andmehõive L3: sama loogika, mis kolib tööriistaplaadile.

**KAARDISTA ISE, lõpus.**
* Git repo ja tag:
* Numbrid, mille see labor andis, ühikutega:
* Mida me teeksime teisiti:
* Mida järgmine labor peaks enne alustamist teadma:

### Tagasiside
