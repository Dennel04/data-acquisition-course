# Op-amp astme kavandamise ja arvutamise tööleht

See on projekteerimise ja hilisema kontrolli tööleht, mitte valmis astme tulemus. Allpool olevad võrrandid eeldavad määratud sisendvahemikku ning selles vahemikus lineaarset andurit ja astet. Labor 1 kinnitab anduri, ADC seadistuse ja raw-signaali teisenduse; tegelikud Labor 2 sisendi otspunktid ning füüsilise astme tulemused: TODO: real measurement required.

Õppejõu MPX5700AP arvud on ainult ülesande näide. **Õppejõu MPX5700AP näide, mitte meie mõõtetulemus.** Labor 1 kinnitab, et meeskond kasutas sama MPX5700AP andurit otse AtomS3R ADC-sse, kuid ei asenda Labor 2 otspunktide mõõtmist.

Esimese riistvarasessiooni mõõtmisjärjekord, mõõtepunktid ja tagastatav väärtuste mall on failis [`bench_session.md`](bench_session.md). Täida seal `V_sensor_supply`, `V_opamp_supply`, `Vin_atmosphere`, `Vin_full_suction`, `Vin_full_blowing`, op-ampi markeering ja olemas olevad takistid enne meeskonna astme lõplikku arvutust.

## Teadaolevad sisendsuurused

| Suurus | Sümbol | Väärtus | Allikas |
|---|---|---|---|
| Kasutatud andur | — | `MPX5700AP` | `data-acquisition/lab1/docs/sensor_choice.md` |
| Anduri toitepinge | `V_sensor` | Laboris 1 mõõdetud `5,00 V`; Labor 2: TODO: real measurement required | `data-acquisition/lab1/docs/sensor_choice.md`; mõõta uuesti multimeetriga |
| Minimaalne anduripinge | `V_in,min` | TODO: real measurement required | Mõõta Labor 2 tegelikus alumises tööpunktis |
| Maksimaalne anduripinge | `V_in,max` | TODO: real measurement required | Mõõta Labor 2 tegelikus ülemises tööpunktis |
| Vastavad rõhud | `P_min`, `P_max` | Ülesande töövahemik `−70…+110 kPa` suhtelist rõhku; tegelikud mõõtepunktid: TODO: real measurement required | Labor 2 ametlik ülesanne |
| Anduri tundlikkus | `S_P` | Labori 1 `5,00 V` toite korral andmelehe valemist arvutatud `6,429 mV/kPa`; Labor 2 toitega arvutada uuesti | `V_sensor · 0,0012858`; `data-acquisition/lab1/src/firmware/include/sensor.h` |
| ADC bitisügavus | `N` | `12 bit` (`0…4095`) | `data-acquisition/lab1/src/firmware/src/sensor.cpp`, `include/sensor.h` |
| ADC seadistus ja kasutatav sisendvahemik | `V_ADC,min`, `V_ADC,max` | AtomS3R G5, `ADC_11db`, kaheksa lugemi keskmine; Labori 1 koodist pingeks tegur `3,70 V / 4095`; tegelik kasulik sisendvahemik: TODO: real measurement required | `data-acquisition/lab1/src/firmware/src/sensor.cpp`, `include/sensor.h`, `docs/sensor_choice.md` |
| Op-ampi tegelik toitepinge | `V_OP,meas` | TODO: real measurement required | Mõõta astme toiteviikudel tööolukorras |

## Nõutav anduripinge vahemik

`ΔV_in = V_in,max − V_in,min > 0`.

Sümbolid `min` ja `max` tähistavad **pinget**, mitte tingimata rõhu suunda. Kui anduri pinge rõhuga väheneb, tuleb rõhu ja pinge otspunktid eraldi siduda. Kui `ΔV_in = 0`, ei saa kahest otspunktist võimendust määrata.

Meeskonna tegelik `ΔV_in`: TODO: real measurement required. Õppejõu andmelehe-põhine näide `1,16 V` jääb allpool eraldi näitena.

## ADC vahemik

- Ideaalse ühtlase ADC mudeli ligikaudne pingesamm: `q_V ≈ (V_ADC,max − V_ADC,min) / 2^N`.
- Toore signaali kasutatud ADC vahemiku osa: `η_raw = ΔV_in / (V_ADC,max − V_ADC,min) · 100%`.
- Kui `S_P = |dV_in/dP|` ühikus V/Pa, siis `q_P,raw ≈ q_V / S_P` ühikus Pa/kood. Astme järel ideaaljuhul `q_P,opamp ≈ q_V / (|A| · S_P)`.

Need on **ideaalse kvantimise** valemid. Labori 1 empiirilise teisendusteguri korral oli tarkvara pingesamm `3,70 V / 4095 ≈ 0,9035 mV/kood`. MPX5700AP andmelehe tundlikkusega `6,429 mV/kPa` arvutati `q_P,raw ≈ 0,1405 kPa/kood = 141 Pa/kood`. See on Labori 1 kalibreeringu ja andmelehe valemi põhine arvutus, mitte ADC füüsilise sisendvahemiku mõõtmine.

Labor 2 peab sama raw-teisenduse uuesti kontrollima ja mõõtma op-amp konfiguratsiooni `q_P,opamp`: TODO: real measurement required.

## Väljundi sihtvahemik

| Suurus | Sümbol | Meeskonna väärtus |
|---|---|---|
| Esimese versiooni alumine siht | `V_out,min,1` | TODO: real measurement required |
| Esimese versiooni ülemine siht | `V_out,max,1` | TODO: real measurement required |
| Esimese versiooni väljundi ulatus | `ΔV_out,1` | `V_out,max,1 − V_out,min,1` |
| Parandatud alumine siht | `V_out,min,2` | TODO: real measurement required |
| Parandatud ülemine siht | `V_out,max,2` | TODO: real measurement required |

**Õppejõu MPX5700AP näide, mitte meie mõõtetulemus.** Näites on `V_in,min = 0,40 V` ja `V_in,max = 1,56 V`; esimese versiooni näidissiht on `0,2…3,3 V` ja parandatud näidissiht `0,3…3,0 V`. Labor 1 kinnitab sama andurit, 12-bitist ADC-d ja `ADC_11db` seadistust. Meeskond ei ole siiski mõõtnud oma `V_in,min`, `V_in,max`, Labor 2 op-ampi toidet ega ADC kasulikku lineaarset vahemikku. Seetõttu jäävad näitearvud näidiseks, kuni Labor 2 mõõtmised kinnitavad projekteerimise lähtepunktid.

## Võimenduse arvutus

Seame `V_in,min → V_out,min` ja `V_in,max → V_out,max`. Üldine afiinne teisendus on

`V_out = A · V_in + B`.

Kahe otspunkti võrrandid on `V_out,min = A · V_in,min + B` ning `V_out,max = A · V_in,max + B`. Lahutades saame

`A = (V_out,max − V_out,min) / (V_in,max − V_in,min) = ΔV_out / ΔV_in`.

Asendades alumise otspunkti võrrandisse saame

`B = V_out,min − A · V_in,min = (V_in,max · V_out,min − V_in,min · V_out,max) / ΔV_in`.

`A` on ühikuta võimendus ja `B` on voltides nihe. Mõlema otspunkti asendamine tagasi avaldisse on kohustuslik kontroll. Allpool kirjeldatud diferentsiaalaste eeldab `A > 0`; teistsugune anduri suund või eesmärk nõuab topoloogia uut valikut.

Meeskonna tulemus: TODO: real measurement required.

## Viite- ehk nihkepinge

Kui valitud aste realiseerib kuju `V_out = A · (V_in − V_ref)`, siis `B = −A · V_ref` ning

`V_ref = −B/A = V_in,min − V_out,min/A = V_in,max − V_out,max/A`.

Seega ei võrdu `V_ref` üldjuhul anduri alumise pingega. Selle topoloogia puhul peavad `A ≠ 0` ja saadud `V_ref` olema valitud toitega teostatavad.

Kontrollida tuleb mõlemat otspunkti:

- `A · (V_in,min − V_ref) = V_out,min`;
- `A · (V_in,max − V_ref) = V_out,max`.

Meeskonna `V_ref`: TODO: real measurement required.

## Takistite valik

Kandidaat `A > 0` korral on ühe op-ampiga sobitatud diferentsiaalaste. Ühenda `R_1` viitest `V_ref` inverteerivasse sisendisse ja `R_2` väljundist samasse sisendisse. Ühenda `R_3` andurist `V_in` mitteinverteerivasse sisendisse ja `R_4` sellest sisendist ühisesse maasse. Ideaalse op-ampi ja koormamata allikate korral:

`V_+ = V_in · R_4/(R_3 + R_4)`;

`V_out = (1 + R_2/R_1) · V_+ − (R_2/R_1) · V_ref`.

Kui `R_2/R_1 = R_4/R_3 = A`, lihtsustub see kujule `V_out = A · (V_in − V_ref)`. Sobitatud **suhtarvud**, mitte üksnes nimiväärtused, määravad ühismüra mahasurumise. Viitepinget ei tohi käsitleda ideaalse allikana, kui pingejagur koormuse all muutub.

Kui viitepinge tehakse op-ampi toitepingest pingejaguriga, on selle koormamata väärtus `V_ref,0 = V_OP · R_bottom/(R_top + R_bottom)`. Lihtsat pingejagurit ei saa automaatselt käsitleda ideaalse `V_ref` allikana, sest diferentsiaalastme takistivõrk koormab jagurit. Jagur tuleb arvutada koos selle koormusega või tuleb `V_ref` puhverdada. Tegelik `V_ref` tuleb hiljem valmis ahelas mõõta. Valitud lõplik topoloogia ja takistite väärtused: TODO: real measurement required.

Valikukäik:

1. vali sobiv takistite suurusjärk pärast op-ampi ja allika koormuse kontrolli;
2. arvuta vajalik suhtarv `R_2/R_1 = R_4/R_3 = A`;
3. vali reaalsed standardväärtused või mõõdetud kombinatsioon;
4. arvuta tegelikud suhtarvud ja nende võimalik lahknevus tolerantside tõttu;
5. arvuta tegelike väärtuste ja koormatud `V_ref` abil mõlemad otspunktid uuesti ning kontrolli sisendite ühispinget, väljundi koormust ja ADC lubatud sisendit.

Lõplikud takistid, tolerantsid ja viiteallikas: TODO: real measurement required. Need väärtused ei ole selles töölehes meeskonna tulemusena määratud.

## Esimese versiooni arvutus

Meeskonna esimese versiooni sihid `V_out,min,1` ja `V_out,max,1` valitakse alles pärast sisendvahemiku ja ADC piiride kinnitamist. Tingimused: `V_out,min,1 > V_ADC,min` ja `V_out,max,1 < V_ADC,max` koos põhjendatud varuga; lisaks peab väljund mahtuma op-ampi lineaarse väljundulatuse sisse.

1. Sisendi ulatus: `ΔV_in = V_in,max − V_in,min`.
2. Väljundi ulatus: `ΔV_out,1 = V_out,max,1 − V_out,min,1`.
3. Vajalik võimendus: `A_1 = ΔV_out,1 / ΔV_in`.
4. Vajalik nihe: `B_1 = V_out,min,1 − A_1 · V_in,min`.
5. Valitud diferentsiaalastme viide: `V_ref,1 = −B_1/A_1 = V_in,min − V_out,min,1/A_1`.
6. Takistite nõutud suhtarvud: `R_2/R_1 = R_4/R_3 = A_1`.
7. Otspunktide kontroll: `A_1 · V_in,min + B_1 = V_out,min,1` ja `A_1 · V_in,max + B_1 = V_out,max,1`.

| Suurus | Meeskonna väärtus | Allikas / kontroll |
|---|---|---|
| `V_in,min`, `V_in,max` | TODO: real measurement required | Andur ja pumba tegelik töövahemik |
| `V_out,min,1`, `V_out,max,1` | TODO: real measurement required | ADC ning op-ampi kontrollitud lineaarne töövahemik |
| `ΔV_in`, `ΔV_out,1` | TODO: real measurement required | Ülaltoodud lahutamised |
| `A_1`, `B_1`, `V_ref,1` | TODO: real measurement required | Ülaltoodud võrrandid |
| `R_1`, `R_2`, `R_3`, `R_4` | TODO: real measurement required | Tegelikud osad ja tolerantsid kontrollida enne katset |

**Õppejõu MPX5700AP näide, mitte meie mõõtetulemus.** Näite sisendulatus on `1,56 − 0,40 = 1,16 V` ja esimese versiooni näite sihtulatus `3,3 − 0,2 = 3,1 V`; seega `A_1 = 3,1/1,16 ≈ 2,7`. See aritmeetika ei määra meeskonna takisteid ega kinnita, et näite ülemine siht tegelikul toitel saavutatav on.

### Õppejõu MPX5700AP näite Falstadi esimene versioon

**Õppejõu MPX5700AP näide, mitte meie mõõtetulemus.** Siinsed pinged, takistid ja müra on ainult kontrollitava simulatsiooni sisendid. See skeem ei ole meeskonna kinnitatud Labor 2 riistvaralahendus. Meeskonna väärtused ülaltoodud tabelites jäävad TODO-deks.

Õppejõu näite tingimused: `V_in,min = 0,40 V`, `V_in,max = 1,56 V`, `V_out,min = 0,20 V` ja `V_out,max = 3,30 V`. Eelmise jaotise võrranditest:

| Näite suurus | Arvutus | Tulemus |
|---|---|---:|
| `ΔV_in` | `1,56 − 0,40` | `1,16 V` |
| `ΔV_out` | `3,30 − 0,20` | `3,10 V` |
| `A` | `ΔV_out/ΔV_in = 3,10/1,16` | `155/58 ≈ 2,672413793` |
| `B` | `0,20 − A · 0,40` | `−126/145 V ≈ −0,868965517 V` |
| `V_ref` | `−B/A = 0,40 − 0,20/A` | `252/775 V ≈ 0,325161290 V` |

Falstadi näites on `R_1 = R_3 = 10 kΩ` ja `R_2 = R_4 = 27 kΩ`. Need on standardsed **näite simulatsioonitakistid**, mitte meeskonna lõplikud takistid ega väide nende saadavuse kohta. Mõlemad tegelikud suhtarvud on `27 kΩ / 10 kΩ = 2,7`; erinevus vajalikust `A`-st on `2,7 − 155/58 ≈ 0,027586207`. Ideaalse sobitatud diferentsiaalastme arvutus valitud takistite ja täpse näite `V_ref`-ga on `V_out,ratio = 2,7 · (V_in − 252/775 V)`.

| Näite `V_in` | Siht täpse `A` korral | Arvutus suhtega `2,7` | Takistisuhtest tekkiv viga sihi suhtes | Falstadi `V_out` | Falstadi ja suhtearvutuse vahe |
|---:|---:|---:|---:|---:|---:|
| `0,40 V` | `0,200000 V` | `0,202065 V` | `+2,065 mV` | ligikaudu `0,20215 V` | ligikaudu `+0,09 mV` |
| `0,98 V` | `1,750000 V` | `1,768065 V` | `+18,065 mV` | `1,768 V` | alla kuvatava `1 mV` täpsuse |
| `1,56 V` | `3,300000 V` | `3,334065 V` | `+34,065 mV` | `3,334 V` | alla kuvatava `1 mV` täpsuse |

Falstadi väljundinäidud on ekraanilt loetud ja ümardatud; viimaste kahe punkti väiksemat erinevust ei saa selle kuvaga täpselt määrata. Simulatsioonis saavutab op-amp `3,30 V` sihi ja valitud suhte tõttu isegi umbes `3,334 V`. See näitab ainult kasutatud Falstadi mudeli käitumist. See ei tõenda, et päris LM358 sama toite ja koormusega selle pingeni jõuab.

Skeem kasutab Falstadi op-ampi väljundipiiridega `0…5 V` ja sisemise avatud ahela võimendusega `100000`. `+5 V` on õppejõu ülesande **simulatsioonieeldus**, mitte mõõdetud toitepinge. Selle mudeli toiterööpad on op-ampi omadustes ning skeemil tekstina nähtavad; mudelil ei ole eraldi toiteviike. `V_in` on muudetav alalispingeallikas, `V_ref` on ideaalne `0,325161290 V` allikas ning väljundil on mõõtesõlm. Ideaalse viite kasutamine eraldab ülekandefunktsiooni kontrolli pingejaguri koormusest. Päris viitevõrk tuleb hiljem koos koormusega arvutada või puhverdada ning valmis ahelas mõõta. TODO: real measurement required.

- Esimese versiooni [Falstadi eksport](falstad_first_version.txt) ja [muudetav veebiskeem](https://www.falstad.com/s.php?s=b1gefl). Faili importimiseks vali Falstadis **File → Import From Text**; `V_in` allika pinget saab muuta allikal paremklõpsuga.
- Ühismüra [eksport](falstad_noise_common.txt) ja [veebiskeem](https://www.falstad.com/s.php?s=2Gxo5B).
- Ühe sisendi müra [eksport](falstad_noise_single.txt) ja [veebiskeem](https://www.falstad.com/s.php?s=rpTgtj).
- Falstadi eraldi PNG skeemipilt: TODO: image export required. Veebisimulaatori pildieksport ei andnud siin kättesaadavat kohalikku faili; ülaltoodud tekstiekspordid ja lingid avavad päris skeemid.

**Õppejõu MPX5700AP näide, mitte meie mõõtetulemus.** Mürakatse ainus näitehäiring on siinus `10 mV` tippamplituudiga ja sagedusega `100 Hz`. Mõlema katse alalissisend on `V_in = 0,98 V` ja ideaalne viide `V_ref = 252/775 V`. Ühismüra skeemis on sama faasi ja amplituudiga allikas nii anduri kui ka viite harus; sobitatud suhtarvudega ei muuda see tahtlikult võimendi sisendite diferentsiaalpinget. Teises skeemis on sama allikas ainult anduri harus. Globaalse maa liigutamine muudaks ka viite- või toitesõlme tähendust ning oleks teine katse.

| Näite mürakatse | Sisendhäiring | Falstadi väljundmüra, tippude vahe | Järeldus selle mudeli kohta |
|---|---|---:|---|
| Sama häiring mõlemas harus | `10 mV` tipp, `100 Hz` | kuval `0 V` | Alla kuvatava täpsuse; ei väida päris ahelas ideaalset mahasurumist |
| Häiring ainult `V_in` harus | `10 mV` tipp, `100 Hz` | ligikaudu `53,998 mV` | Ligikaudu `26,999 mV` tipp; vastab `2,7 · 10 mV` arvutusele |

Väljundmürade vahe on kuvatud täpsusel ligikaudu `53,998 mV` tippude vahel. Nende jagatis ei ole sellest kuvast lõpliku arvuna määratav, sest ühismüra näit on `0 V`; ideaalses sobitatud mudelis on teoreetiline ühismüra väljund `0`. Need on **simulatsiooni näiteparameetrid ja mudeli näidud**, mitte mõõdetud andurimüra ega meeskonna SNR-i tulemus.

## Esimese versiooni kolme punkti mõõtmine

| Tööpunkt | Rõhk (kPa) | Sisend (V) | Arvutatud väljund (V) | Mõõdetud väljund (V) | Vahe (mV) |
|---|---:|---:|---:|---:|---:|
| Atmosfäär | TODO: real measurement required | TODO: real measurement required | TODO: circuit design required | TODO: real measurement required | TODO: real measurement required |
| Täis imemine | TODO: real measurement required | TODO: real measurement required | TODO: circuit design required | TODO: real measurement required | TODO: real measurement required |
| Täis puhumine | TODO: real measurement required | TODO: real measurement required | TODO: circuit design required | TODO: real measurement required | TODO: real measurement required |

## Otspunktide vead

`e_low = V_out,measured,low − V_out,calculated,low`

`e_high = V_out,measured,high − V_out,calculated,high`

Tabelis väljenda `e` millivoltides: `e_mV = 1000 · e_V`. Hoia märki alles. Võrdle sama mõõtmise ajal registreeritud tegelikku `V_in` arvutatud `V_out` väärtusega; ainult sihtväärtusega võrdlemine võib segada anduri ja astme vea.

| Otspunkt | Arvutatud (V) | Mõõdetud (V) | Viga (mV) | Täheldatud piirang / põhjus |
|---|---:|---:|---:|---|
| Alumine | TODO: circuit design required | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required |
| Ülemine | TODO: circuit design required | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required |

## Parandatud versiooni arvutus

Paranduse sihid määratakse esimese versiooni **mõõdetud** toitepinge, väljundi piiride, otspunktivigade ja ADC kontrollitud kasuliku vahemiku põhjal. Praegu on teine versioon ainult sümboolne arvutuskäik.

Vali `V_out,min,2 > V_out,min,1` ja `V_out,max,2 < V_out,max,1` ainult siis, kui mõõtmised kinnitavad, et just selline varu on vajalik. Mõlemad sihid peavad jääma korraga ADC kasulikku sisendvahemikku ja op-ampi lineaarse väljundulatuse sisse.

1. Parandatud väljundi ulatus: `ΔV_out,2 = V_out,max,2 − V_out,min,2`.
2. Parandatud võimendus: `A_2 = ΔV_out,2 / ΔV_in`.
3. Parandatud nihe: `B_2 = V_out,min,2 − A_2 · V_in,min`.
4. Parandatud viide: `V_ref,2 = −B_2/A_2 = V_in,min − V_out,min,2/A_2`.
5. Uued suhtarvud: `R_2,2/R_1,2 = R_4,2/R_3,2 = A_2`.
6. Kontroll: `A_2 · V_in,min + B_2 = V_out,min,2` ja `A_2 · V_in,max + B_2 = V_out,max,2`.

| Suurus | Parandatud väärtus | Põhjendus |
|---|---|---|
| `V_out,min,2` | TODO: real measurement required | Mõõdetud alumise piiri ja ADC varu järgi |
| `V_out,max,2` | TODO: real measurement required | Mõõdetud toite, ülemise piiri ja ADC varu järgi |
| `A_2`, `B_2` | TODO: real measurement required | Parandatud sihid ja `ΔV_in` |
| `V_ref,2` | TODO: real measurement required | `−B_2/A_2` |
| Parandatud takistid | TODO: real measurement required | Suhtarvud ja tegelikud komponendid |

**Õppejõu MPX5700AP näide, mitte meie mõõtetulemus.** Parandatud näidissiht on `0,3…3,0 V`; selle ulatus on `2,7 V` ja näite võimendus `A_2 = 2,7/1,16 ≈ 2,3`. Meeskonna paranduse sihid tuleb valida enda esimese versiooni mõõtmiste alusel.

## LM358 ja toitepinge piirangud

- LM358 ei ole rail-to-rail väljundiga. Õppejõu projekteerimisnäites jääb ülemine väljund ligikaudu `1,5 V` alla positiivse toiterööpa; see ei ole LM358 universaalne absoluutne piir. Tegelik väljundi ulatus sõltub täpsest LM358 variandist, koormusest ja toitepingest. Kontrolli piir valitud variandi andmelehe vastavate katsetingimuste järgi ning kinnita see hiljem riistvaramõõtmisega.
- Alumises otsas võib väljund jõuda küllastuses maa lähedale, kuid see ei taga lineaarset ülekannet kogu madala pinge piirkonnas. Kontrolli väikeste väljundpingete juures mitut sisendpunkti, mitte ainult nullilähedast näitu.
- Kontrolli ka LM358 sisendite lubatud ühispinget. Ülal kirjeldatud astmes on ideaalne `V_+ = V_in · A/(1 + A)`; tegelik lubatud vahemik tuleb andmelehelt ning sõltub toitest.
- USB ja juhtmete pingelangud võivad muuta astme tegelikku toidet. `5 V` on ülesande nimitingimus, mitte mõõdetud `V_OP,meas`. Mõõda pinge op-ampi toiteviikudel ja arvuta saavutatav ülemine väljundsiht selle järgi uuesti.
- Koormus, takistite tolerantsid, op-ampi sisendnihke pinge ja viiteallika koormumine võivad põhjustada lisavigu. Esimese versiooni hälvet ei saa omistada ühele põhjusele enne mõõtmist.

Allikad: [Labor 2 ametlik ülesanne](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLab%202%5D%20EST.md), [TI LM358 andmeleht](https://www.ti.com/lit/ds/symlink/lm358.pdf). Valitud konkreetse LM358 variandi ja koormuse andmelehe tingimused: TODO: real measurement required.

## ESP32 ADC otspunktid

ESP32 ADC ülekandefunktsioon ei ole ideaalne sirge kogu vahemikus. Äärmiste pingete juures võib koodi muutus pinge muutuse suhtes erineda keskmisest või küllastuda; sumbuvus ja kalibreerimine mõjutavad kasutatavat vahemikku. Seetõttu jätab parandatud siht nii alumisse kui ka ülemisse otsa varu. Näite `0,3…3,0 V` ei tõesta, et see on meeskonna valitud AtomS3 ADC seadistusega ohutu või lineaarne. Kontrolli konkreetset kiipi, viiku, sumbuvust, lubatud sisendpinget ja kalibreerimist enne ühendamist.

Allikas: [Espressifi ESP32-S3 ADC dokumentatsioon](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/adc/index.html). Meeskonna Labor 1 seadistus oli AtomS3R G5, 12 bit ja `ADC_11db`; tarkvara keskmistas kaheksa lugemit ning kasutas empiirilist teisendust `3,70 V / 4095`. Tegelik kasulik ja lineaarne sisendvahemik Labor 2 konfiguratsioonis: TODO: real measurement required.

## Parandatud versiooni kolme punkti mõõtmine

| Tööpunkt | Rõhk (kPa) | Sisend (V) | Arvutatud väljund (V) | Mõõdetud väljund (V) | Vahe (mV) |
|---|---:|---:|---:|---:|---:|
| Atmosfäär | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required |
| Täis imemine | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required |
| Täis puhumine | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required |

## Falstad

Järgnev katseplaan ja TODO-tabel käivad meeskonna tulevase kinnitatud anduri ning astme kohta. Õppejõu MPX5700AP näite käivitatud skeemid ja näidud on eraldi ülaltoodud alajaotuses.

Falstadi katseplaan pärast lähteandmete kinnitamist:

1. Esita andur muudetava pingeallikana `V_in`; märgi kontrollitud `V_in,min`, keskmine proovipunkt ja `V_in,max`. Ära kasuta õppejõu MPX5700AP väärtusi meeskonna sisendina.
2. Lisa eraldi `V_ref` allikas või arvutatud ja koormuse suhtes kontrollitud pingejagur. Ühenda op-amp ning takistid valitud topoloogia järgi; kasuta simulatsioonis toidet `V_OP,sim`, mille eeldus on kirjas.
3. Pane väljundile mõõtepunkt ja kontrolli `V_out` kõigis kolmes sisendpunktis. Võrdle esimese versiooni `A_1 · V_in + B_1` väärtustega.
4. Ühismüra katses rakenda sama häiring mõlemale võimendi sisendile sama amplituudi ja faasiga, ilma et sisendite diferentsiaalpinge `V_+ − V_−` tahtlikult muutuks. Ühe sisendi katses rakenda sama häiring ainult ühele sisendile. Pelgalt müraallika lisamine skeemi globaalsesse maasse võib nihutada ka `V_ref` või toite viitepunkte ning katsetada seetõttu teist nähtust. Märgi skeemil müraallika täpne ühendus ja võrdle väljundi müra mõlemas katses sama mõõtmisviisi ning ühikuga.
5. Salvesta mõlemas katses häiringu allikas ja asukoht, amplituud (V), sagedus (Hz), sisendite vahe (V), väljundi müra amplituud (V) ning nende suhe. Ilma simulatsioonita jäävad kõik tulemused TODO-väljadeks.
6. Salvesta elava skeemi link, Falstadi ekspordifail ja skeemipilt. Pildil peavad olema näha toiteallikad, `V_in`, `V_ref`, op-amp, takistid, väljundsond ja kasutatud müraallikas. Lisa sama katse kohta pilt ning link elavale failile.

| Tõend / suurus | Väärtus või fail |
|---|---|
| Elava skeemi link, ekspordifail ja skeemipilt | TODO: circuit design required |
| `V_OP,sim`, `V_ref`, takistite väärtused ja allikas | TODO: circuit design required |
| Kolme sisendpunkti arvutatud ja simuleeritud väljund (V) | TODO: circuit design required |
| Ühismüra katse seaded ja väljundi amplituud (V) | TODO: circuit design required |
| Ühe sisendi müra katse seaded ja väljundi amplituud (V) | TODO: circuit design required |
| Kahe mürajuhtumi amplituudide suhe | TODO: circuit design required |

Falstadi mudel ei tõenda konkreetse LM358 madala otsa lineaarsust, väljundi ülemist piiri ega tegelikku USB-toidet.

## Ostsilloskoop

- Kahe kanaliga pilt samast impulsist: TODO: real measurement required.
- Failitee: TODO: real measurement required.
- Kanali 1 ja kanali 2 tähendus ning ühikud: TODO: real measurement required.
- Tipu kuju ja võimaliku piirangu vaatlus: TODO: real measurement required.

## Mida ei saa lõpetada ilma Labor 2 riistvaramõõtmiseta

| Lahendamata küsimus | Vajalik tõend |
|---|---|
| Tegelikud `V_in,min` ja `V_in,max` kogu nõutud töövahemikus | TODO: real measurement required |
| Raw-signaali lähtejoon | Labori 1 arvutus `0,1405 kPa/kood = 141 Pa/kood`; kontrollida Labor 2 riistvaral |
| Lõpliku vahemiku põhjal valitud takistid ja nende tegelikud väärtused | TODO: real measurement required |
| Tegelik op-ampi toitepinge | TODO: real measurement required |
| Esimese ja parandatud astme kolme punkti mõõtmised | TODO: real measurement required |
| Mõlema otspunkti vead | TODO: real measurement required |
| Ostsilloskoobi sisendi ja väljundi tõend | TODO: real measurement required |
| Parandatud astme füüsiline kinnitus | TODO: real measurement required |
