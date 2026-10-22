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

## 22.10.2026 — LM358N katseskeemi mõõtmised (Maksim)

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
