# Labor 2 esimese elektroonikasessiooni tööleht

Täida see leht mõõtepingi juures enne Atomi ADC ühendamist. Ära kasuta õppejõu näitearve mõõtetulemustena. Lülita toide välja enne juhtmete ümbertõstmist.

## 1. Riistvara tuvastamine

| Väli | Kontroll / märge |
|---|---|
| Op-ampi täpne markeering | TODO: loe korpuselt kogu tähis |
| Anduri markeering | TODO: loe korpuselt; Labori 1 andur oli MPX5700AP |
| Maketeerimisplaat / toiteallikas | TODO: kirjelda plaat ja toiteallikas |
| Esimese versiooni jaoks füüsiliselt olemas olevad takistid | TODO: kirjuta nimiväärtus, mõõdetud väärtus ja kogus |

Kontrolli op-ampi viigustik täpse korpusemarkeeringu andmelehelt enne toite ühendamist. Ära eelda, et riiulis olev detail on LM358 või et selle viigustik vastab teisele variandile.

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
OPAMP marking =
V_sensor_supply =
V_opamp_supply =
Vin_atmosphere =
Vin_full_suction =
Vin_full_blowing =
Available resistors =
```

Lisa ühik voltides iga pinge juurde. Takistite puhul lisa ühik, kogus ja võimaluse korral multimeetriga mõõdetud väärtus.
