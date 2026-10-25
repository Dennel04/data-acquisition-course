# Andmehõive: Labor 3 — Tilk ja IRQ

See on meeskonna Labori 3 tööleht. Füüsilisi Lab 3 tulemusi pole siia veel dokumenteeritud; kõik mõõtmised, riistvara saadavus, valikud ja katsed jäävad TODO kuni kontrollitud tõendini.

**Töömaht:** 30 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 28.10.26 | **Tellimise kuupäev:** 06.11.2026 | **Esimene kaitsmine:** 19.11.2026, veebis

## Allikad ja tõendite piirid

[Ametliku ülesande täpne koopia](assignment-EST.md) on muutmata etalon, mitte meeskonna tulemuste register. Kontrollitud 25.10.2026: Git blob SHA `3b8089eb54e7587946d42ffa25a071f35e174396`, sama kui kontrollversioon. [Õppejõu algallikas](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLab%203%5D%20EST.md) on varasemate plaanide suhtes ülimuslik; [ametlik kokkuvõte](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLabor%203%20kokkuv%C3%B5te%5D%20EST.md) on abiallikas.

- **Dokumenteeritud varasem tulemus:** [Lab 1 andur](../lab1/docs/sensor_choice.md) ja [pumbajuhtimine](../lab1/docs/pump_control.md) kirjeldavad oma toonast stendi; nende väärtusi ei võeta automaatselt Lab 3 seadeteks.
- **Lab 2 elektriline katse:** [22.–24.10 mõõteleht](https://github.com/Dennel04/data-acquisition-course/blob/bcb899ccd64a2471693dd93075a9fe5c2450e4fc/data-acquisition/lab2/docs/bench_session.md) ning [arvutused ja kontrollmõõtmised](https://github.com/Dennel04/data-acquisition-course/blob/bcb899ccd64a2471693dd93075a9fe5c2450e4fc/data-acquisition/lab2/docs/opamp_design.md) on kinnitatud repoallikad. Katsed kasutasid B5K/B100K potentsiomeetreid; 24.10 ADC kontrollis dokumenteeriti 1001 lugemit ligikaudu 10 s jooksul. See ei kinnita MPX5700AP rõhukalibratsiooni, kogu ADC sisendulatuse ohutust, lõplikku anduriastet ega Lab 3 filtrit, releed või doseerimist.
- **Oluline ühenduste piirang:** Lab 2 katses puhverdab LM358N teine pool viitepinget. Selle ümberkasutamine komparaatoriks nõuab Lab 2 lõpliku skeemi kontrolli; olemasolevat puhvrit ei loeta vabaks kanaliks.
- **CAD ja tööplaan:** [3D printimise L3 README](https://github.com/Dennel04/3d-printing-course/blob/6068053f90d09fa301889ee4476e139a78dd82ad/3d-print/lab3/README.md) kirjeldab Y-pneumaatikat, nelja nihet ja tühja kuivtsükli plaani. See, Lab 2 tulemused ja simulatsioonid ei kinnita Andmehõive L3 füüsilist valmimist.
- **TODO:** lõplik Labori 2 anduriahel, CSV-vorming, kalibratsioon, tegelik kasutatav ajasamm, filtreeritud/op-amp tulemused, pooliku haarde logid ning pumbajuhtimise väärtused tuleb kontrollida [Lab 2 dokumentidest](../lab2/README.md) ja [pumbavõrdlusest](../lab2/docs/pump_control.md).
- **Arvutused ja valikud:** filtrit, lävesid, takisteid, releekontakti, GPIO-d, mähise pinget ega taimeri seadistust ei määrata oletuse järgi.

## Eesmärk ja pneumaatika

Tööjärjekord: **doseerimine → klaasi tõstmine → kõvendamine → väljund**. Üks pump ei ime ja puhu korraga.

Õppejõu nõutav skeem: **pump → Y1 → iminapp / 3/2 klapp → süstal**. Napp on otse pumba harus, mitte klapi järel. Klapp juhib ainult süstalt: voolu all ühendab pumba süstlaga; vooluta lahutab pumba ja ühendab süstla atmosfääriga. Teine 4 mm Y-liitmik ühendab rõhuanduri. Anduri koht enne klappi või klapi ja süstla vahel on **TODO: põhjendatud insenerivalik**. Võimalik nõelventiil napi harus lisatakse ainult siis, kui päris mõõtmine näitab, et lahtise napa õhukadu takistab rõhu hoidmist; mõju imemisele mõõdetakse eraldi.

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

TODO: täita tegelike otsuste ja mõõtmiste järel.

## Kontrollnimekiri

Järgmised 16 punkti on ametlikust ülesandest sõna-sõnalt ja samas järjekorras. Dokumentatsiooni sünkroonimine ei täida füüsilisi kriteeriume.

- [ ] Klapp lülitab Atomi käsu peale. Vooluta on süstal õhu peal ja pumbast lahti. Mõõdetud, mitte oletatud.
- [ ] Impulsi pikkust loeb riistvarataimer. Käsk ja ostsilloskoobilt klapi mähisel mõõdetud pikkus kõrvuti viie pikkuse kohta.
- [ ] UV LED lülitab Atomi käsu peale ja kustub alati ise.
- [ ] Anduri koht voolikus valitud ja põhjendatud.
- [ ] Tilgad: vähemalt viis impulsi pikkust, kümme tilka igaühega, iga tilk mõõdetud pildilt tilgaplaadil ja iga tilga rõhukõver salvestatud. Fail `data/drops.csv`.
- [ ] Teine muutuja läbi proovitud: teine otsik või teine rõhk, kolme impulsi pikkusega.
- [ ] Atomi ekraanipoole mudelid prinditud päris AtomS3 mõõtude järgi. Tilk ja klaas mudeli peal, laigu suurus ja koht mõõdetud tööriista kaamera pildilt. Tulemused ja pildid failis `data/placement.csv`.
- [ ] Retsept kirjas failis `docs/recipe.md`: otsik, rõhk, impulss, kõvendamise aeg, ja klaas selle tilga peal läbi proovitud.
- [ ] Toores ja filtreeritud muutumise kiirus kõrvuti samal kõveral, spektrid kõrvuti. Filter valitud numbritega.
- [ ] Sama muutumise kiirus Labori 2 pooliku haarde logil: kas "vaakum püsib" on nüüd otsus.
- [ ] Komparaator Falstadis: lülitub kinnise otsiku peale, ei lülitu tavalise tilga ega müra peale.
- [ ] Komparaator plaadil, katkestus (IRQ) Atomis: klapp tagasi, alarm lukus, sündmus välja.
- [ ] Reageerimise aeg ostsilloskoobilt, kümme korda, katkestusega ja ilma. Fail `docs/latency.csv`.
- [ ] Kinnine otsik kümme korda ja tühi süstal kümme korda: mitu korda tabas. Tavaline tilk kolmkümmend korda: mitu valehäiret.
- [ ] Tellimus 06.11 failis `docs/bom.md`.
- [ ] Repo ja arenduspäevik täidetud, tag `data-acquisition-lab3`.

**KAARDISTA ISE — kuupäevad ja sinu enda sammud.**

TODO: täita päris töö käigus.

## Nõutavad väljundid

- [Tilgamõõtmised](data/drops.csv), iga tilga algne rõhukõver, foto, mõõtkavapilt ja kontrollitud kontuuridega pilt; [paigutusmõõtmised](data/placement.csv).
- [Andmeskeem ja ühikud](data/README.md), [analüüsiplaan](notebooks/README.md) ja [püsivara/logija plaan](src/README.md).
- [Retsept](docs/recipe.md), [viivitused](docs/latency.csv), [BOM](docs/bom.md), [pumbajuhtimine](docs/pump_control.md) ja [füüsilise töö kontrollleht](docs/bench_session.md).
- [Falstadi elav link, eksport ja skeemipilt](docs/falstad/README.md), [ostsilloskoobitõendid](docs/scope/README.md), elektriline skeem pildina ning füüsilise ahela foto: **TODO**.
- Tilgaplaadi, vahetükkide ja ekraanipoole mudeli CAD-lähtefailid ning STL-id: **TODO pärast füüsilisi mõõtmisi ja eraldi modelleerimist**. Faile ei looda selles dokumentatsioonitöös.

## 1. Klapp, relee ja impulss

1. Kasutada ülesande järgi **M5Stack Mini 3A Relay Unit** moodulit. Lugeda päris klapi nimipinge ja vool ning relee täpne markeering; kontrollida induktiivse DC-koormuse sobivust andmelehelt.
2. Hoida klapi jõuahel ja Atomi loogikaahel eraldi. Mõõta pingestamata COM/ON/OFF kontaktide tegelik NO/NC olek multimeetriga; märgistusest üksi ei järeldata ohutut kontakti. GPIO ja ühendused: **TODO: kontrollitud riistvara ja lähtekood**.
3. Kaitsediood klapi mähisega rööbiti: katood ehk triip plussi poole. Kontrollida polaarsus ja pinge-/voolutaluvus enne ühendamist.
4. Kontrollida füüsiliselt, et Atomilt/toitelt voolu kadumisel klapp lahutab pumba ja tühjendab süstla atmosfääri. Mõõta süstlaharu rõhk ja säilitada ohutu oleku tõend.
5. Ajastada impulss riistvarataimeriga. Mõõta kahe kanaliga Atomi GPIO signaal ja **klapi mähise pinge**: viis pikkust × kümme mõõtmist. Võrrelda käsku, GPIO-impulssi ja mähise impulssi, keskmist ning hajuvust.
6. Mõõta relee sisse-/väljalülitusviivitus ja kontaktipõrge; võrrelda andmelehega. Hinnata elektriline kontaktide eluiga lülitustes ja päevades tegeliku kavandatud tilkade arvu järgi, arvestades induktiivset koormust. Releega kiiret PWM-i ei tehta. Piirid jäävad võrdluseks hilisema labori MOSFET-lahendusele.
7. Mõõta rõhukõveralt eraldi klapi mehaaniline avanemisviivitus. Valida anduri koht ning dokumenteerida kompromiss.
8. UV LED läbi sobiva draiveri, taimeriga automaatne väljalülitus ja must kaitsekate. Kuni LED/draiver puuduvad, on tulevane taimerikatse ostsilloskoobiga Atomi viigul.

Tõendid [mõõtelehel](docs/bench_session.md): ühendusskeem pildina, füüsilise ahela foto, süstlaharu rõhk vooluta, relee andmeleht ning ajastustabelid — kõik **TODO**. Ilma dioodita väljalülitustipu mõõtmine on lubatud ainult pärast ohutu protseduuri kooskõlastamist õppejõuga; seda pole tehtud.

Õppejõu liidese näited, mitte meeskonna teostatud tulemus:

Arvuti → Atom:

```json
{"cmd":"dispense","ms":200}
{"cmd":"uv","ms":5000}
{"cmd":"clear"}
```

Atom → arvuti:

```json
{"ev":"dispense_start","t":123456}
{"ev":"dispense_end","t":123660}
```

## 2. Tilga suurus ja ekraanipoole mudel

- Mõõta rõhk lahtise napaga ja kontrollida, kas pumba riba jõuab väljalülituseni. Doseerimisrõhk, süstla täituvus ja vooliku pikkus: **TODO**.
- Õppejõu lähte-soovitus on **kõige peenem otsik, madal rõhk ja üle 100 ms impulss**; need pole meeskonna valitud retsept ega mõõtetulemused.
- Valmistada hele PLA tilgaplaat prinditud mõõtkavaga. Paigutus 5 × 5: read on impulsi pikkused, veerud kordused; vähemalt viis pikkust × kümme kordust ehk vähemalt 50 tilka (kaks plaati põhisarjaks). Tilkade vahe valida esimesest katsest suurem kui suurim laik.
- Klaas asetada mõõdetud kõrgusega prinditud vahetükkidele. Salvestada kõrgus ja mõõtemeetod; CAD/STL ning tegelik sobivus on TODO. Tilgad teha järjest, kõvendada plaat ja alles siis pildistada.
- Kasutada tööriista **XIAO ESP32S3 Sense** kaamerat. Hoida stabiilne töökõrgus, kaamera risti plaadiga, fookus ja hajus/külgvalgus; UV on pildistamisel väljas. Kaamera flantsinihe tuleb [3D L3 nelja nihke dokumendist](https://github.com/Dennel04/3d-printing-course/blob/6068053f90d09fa301889ee4476e139a78dd82ad/3d-print/lab3/docs/tool_offsets.md), mitte vanast oletusest.
- Leida terav töökõrgus katseliselt; igal seansil mõõtkavapilt, `mm/pixel` ning väikseima tilga läbimõõt pikslites. Segmenteerida laik ja joonistada leitud kontuur fotole tagasi kontrollimiseks.
- Arvutada pindala `area_px × mm_per_pixel²` ühikus mm² ja ruumala `area_mm2 × layer_height_mm` ühikus µL (1 mm³ = 1 µL). Hinnata ühe piiripiksli mõju pindalale protsentides; mõõteviga peab olema uuritavast hajuvusest väiksem.
- Iga `drop_id` siduda foto, kontuuripildi, mõõtkavapildi ning algse rõhukõveraga [drops.csv-s](data/drops.csv). Iga tilga nihikuga mõõtmine ei ole uus meetod.
- Hinnata lineaarsust: kus suuruse ja impulsi seos paindub ja miks; eraldi arvutada `CV = standardhälve / keskmine` ning protsentides `100 × CV`.
- Kontrollida esimest impulssi pärast pausi. Teine muutuja on teine otsik **või** rõhk, kolme impulsi pikkusega. Võrrelda rõhuplatoo ja kõvera pindala seost tilga suurusega.

**Päris AtomS3 peale vaiku ei katsetata.** Mõõta nihikuga päris korpuse välismõõt, ekraani ava suurus/asukoht, raam ja ekraani sügavus raamist. Nende järgi kavandada õhuke prinditav ekraanipoole koopia, kontrastne ekraaniala ja sobivus hoidikusse; CAD-lähtefail ning STL: **TODO**. Katsetada vaiku, klaasi ja kõvendamist prinditud mudelil, mõõta kaamerapildilt laigu pindala ja nihe ekraani keskpunktist x/y millimeetrites ning servani jõudmine [placement.csv-s](data/placement.csv). Retsept [recipe.md-s](docs/recipe.md) kehtib alles päris katse järel.

**KAARDISTA ISE — mida sa päriselt kasutasid.**

TODO: füüsilised mõõdud, töövahendid, failid ja tõendid.

## 3. Filter ja tuletis

Õppejõu 100 Hz lähtevalem: `dP/dt = (P_now - P_previous) / 10 ms`. Enne arvutamist kontrollida päris CSV ajatemplite vahet; kPa/s saamiseks kasutada ajasammu sekundites. Kavandatud 100 Hz ei tõenda tegelikku ajastust.

Järjekord: päris rõhuandmed → toores dP/dt → rõhu ja tuletise spektrid → libisev keskmine ning mediaan **enne tuletist** → kummagi müra ja viivituse arvuline võrdlus → põhjendatud valik. Selgitada sagedusvõimendust `2πf`.

Seejärel rakendada valitud meetodit kontrollitud Lab 2 pooliku haarde logile pärast pumba väljalülitumist ning määrata eristamise lävi ja aeg otsuseni. Kui päris logi puudub, jääb töö TODO. Võrrelda normal / clogged / empty rõhukõveraid: tõusukiirus, platoo ja langus pärast ventileerimist. Tunnus, filter, läved ning ajapiirid: **TODO: ainult pärisandmetest**.

## 4. Katkestus (IRQ)

1. Falstad esmalt: valitud rõhu- või tuletisesignaal, komparaator ja hüsterees. Tavaline ning müraga tavaline tilk ei tohi lülitada, kinnine otsik peab lülitama. Takistid ja läved: **TODO**.
2. Füüsiline ahel kasutab ülesande järgi **LM358N teist poolt**. Enne ümberühendamist lahendada Lab 2 viitepinge puhvri vajadus. Mõõta väljundi madal/kõrge pinge ja üleminekud **enne Atomi ühendamist**; kõrge tase ei tohi ületada 3,3 V ega konkreetse viigu kontrollitud lubatud piiri. Vajadusel arvutada ja mõõta sobiv jagur; LM358N toide ei tõenda väljundi sobivust.
3. ISR-is ainult käsk klapi viivitamatuks vooluta viimiseks ja lipp. Relee/klapi mehaaniline vabastus pole sama kui GPIO muutus. Põhitsüklis ekraan, USB alarmisündmus ning alarmi lukustus; järgmist doseerimist ei lubata kuni `clear` käsuni.
4. Tühja süstla jaoks määrata normaalse tilga pärisandmetest oodatud platoo ja lubatud aeg. Kui rõhk selle ajaga platooni ei jõua, lukustada `empty` alarm. Väärtused **TODO**.
5. Mõõta ostsilloskoobiga rõhu läve ületusest **mähise pinge** vabastuseni kümme korda IRQ-ga ja kümme korda polling'uga; korrata koormatud põhitsükliga. Tulemused [latency.csv-s](docs/latency.csv).
6. Kinnine otsik ×10 ja tühi süstal ×10: tabamised; tavaline tilk ×30: valehäired. Kõik tulemused **TODO**.

Viivituse tulemused ja otsus:

- katkestuse keskmine viivitus: **TODO: ms**;
- katkestuse halvim viivitus: **TODO: ms**;
- polling'u keskmine viivitus: **TODO: ms**;
- polling'u halvim viivitus: **TODO: ms**;
- polling'u viivitus põhitsükli koormusega: **TODO: ms, keskmine ja halvim**;
- katkestuslahenduse arendusaeg: **TODO**;
- polling'u lahenduse arendusaeg: **TODO**;
- lõplik valitud meetod ja ühe lause põhjendus: **TODO: valida mõõtetulemuste põhjal**.

## Ohutus

- UV valgustamine musta katte all, valgus ei paista välja. Kõigil laua ääres 405 nm kaitseprillid, kui LED on draiveriga ühendatud. LED-i ei vaadata; lamp laua poole, taimeriga auto-off ja vooluta väljas.
- Süstlad täidab õppejõud; täidetud süstlal otsikukork ja tagumine kolb. Lahtise süstlaga nitriilkindad. Vaik koristada IPA/paberiga, saastunud paber kõvendada enne jäätmesse panemist; kõvenemata vaiku ei valata kraanikaussi.
- Lampi ei suunata tavapärasele otsikule. Tulevase ummistuskatse üks otsik valmistatakse eraldi süstlast lahti, vaiguga täidetult ja katte all kõvendades; märgistada. See pole veel tehtud.
- Kinnine süstal on rõhu all suletud anum: hoidikus/statiivis, mitte käes. Enne eemaldamist klapp vooluta ja süstlaharu rõhu vabanemine füüsiliselt kinnitatud. Kuni IRQ-kaitse on kontrollitud, inimese käsi pumba lüliti juures.
- Klapi mähisel kaitsediood; dioodita mõõtekatse ainult õppejõuga kooskõlastatud ohutu protseduuriga ja sobiva sondi/ulatusega. Klapi jõuahelat ei ühendata Atomi loogikapoolega; võrgupinget releega ei lülitata.
- ADC ja IRQ ei talu 5 V. Kontrollida väljundpinge enne Atomi ühendamist. USB ja toide välja enne juhtmete muutmist.
- Pumbakast 24 V; DO-liinid ühendada ainult keelatud roboti ja vooluta kastiga. Lahtist +110 kPa voolikut ei suunata inimeste poole.
- Käed lauast eemal, kui MG400 on sisse lülitatud; esimene jooks aeglaselt, hädastopp käeulatuses. Esmased tilgakatsed laual; hilisem robotiga pildistamine alles ohutu seadistuse järel.
- Otsikule kork, kui ei doseerita. Selles laboris ei joodeta.

## Hindamiskriteeriumid

| Kategooria | Punktid | Ettevalmistuse olek |
|---|---:|---|
| Tööfailid — püsivara taimeri/IRQ/alarmiga, logija, drops.csv, kõverad ja analüüs | 5 | Mallid; **TODO: kood ja päris andmed** |
| Analüüs — käsk/GPIO/mähis, kaameraga tilga suurus ja hajuvus, spektrid, filter ja viivitus | 5 | **TODO: mõõtmised ja analüüs** |
| Prototüüp — vooluta süstal atmosfääri, retsept mudelil hoiab klaasi ega ulatu servani, õiged alarmid | 5 | **TODO: füüsilised katsed** |
| Dokumentatsioon — README, päevik, retsept, latency.csv, Falstad, pump_control.md, BOM, AGENTS.md | 5 | Mallid; **TODO: tulemused ja tõendid** |
| **Kokku** | **20** | **TODO** |

## Arenduspäevik

Lisa ainult tegeliku töösessiooni järel uus sissekanne; olemasolevaid sissekandeid hiljem ei muudeta.

**PP.KK.AA — osalejad**

- Tegime:
- Juhtus (numbrid ja ühikud):
- Otsustasime, ja miks:
- Failid:
- Lahti järgmiseks korraks:

**25.10.2026 — dokumentatsiooni sünkroonimine; osalejad teadmata**

- Tegime: võrdlesime ametlikku ülesannet ja kokkuvõtet, säilitasime täpse ülesandekoopia ning uuendasime ainult Lab 3 dokumente ja tühje andmemalle.
- Juhtus (numbrid ja ühikud): ülesande blob SHA `3b8089eb54e7587946d42ffa25a071f35e174396`; 16 ametlikku kontrollpunkti kopeeriti sõna-sõnalt. Füüsilist sessiooni, mõõtmisi ega katseid ei toimunud.
- Otsustasime, ja miks: kehtiv alus on releega juhitud süstlaharu, vooluta atmosfääri tühjendus ja kaamerapõhine tilgamõõtmine; varasem plaan on asendatud ametliku redaktsiooni järgi.
- Failid: `assignment-EST.md`, `README.md`, `data/README.md`, `data/drops.csv`, `data/placement.csv`, `docs/bom.md`, `docs/bench_session.md`, `docs/pump_control.md`, `docs/recipe.md`, `docs/scope/README.md`, `docs/falstad/README.md`, `notebooks/README.md`, `src/README.md`.
- Lahti järgmiseks korraks: inventuur, Lab 2 lõpliku skeemi ja kalibratsiooni kontroll, mõõdetud relee-/klapiühendus, kaamera skaala ning plaadi, vahetükkide ja ekraanipoole mudeli füüsilised mõõdud. Kõik füüsilised Lab 3 tulemused jäävad TODO.

## Väljundid ja tulemused

- Nutikad Lahendused L3: klapi ja LED-i käsud, seaded/testnupud Atomi lehele ning alarmisündmus, mille peale jaam peatab roboti — **TODO**.
- 3D printimine L3: lubatud voolikupikkus klapi ja süstla vahel, põhjendatud anduri asukoht ning kaamera flantsinihke kontroll — **TODO**.
- Andmehõive L4: retsept ja kõverad, märgistatud normal / clogged / empty juhud, pildilt mõõdetud laigu suurused ja kohad `placement.csv-s` ning relee viivitus, põrge ja eluiga hilisemaks võrdluseks — **TODO**.

**KAARDISTA ISE, lõpus.**

- Git repo ja tag: **TODO: tag alles esitamisel; selles töös tag'i ei looda**.
- Lõplikud numbrid koos ühikutega: **TODO: päris mõõtmised**.
- Mida teeksime teisiti: **TODO: täita pärast füüsilist tööd**.
- Mida Labor 4 peab teadma: **TODO: täita kontrollitud Labor 3 tulemuste põhjal**.
