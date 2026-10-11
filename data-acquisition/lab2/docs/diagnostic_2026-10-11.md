# LM358N diagnostika 11.10.26

Osalejad: Nikita, Maksim.

See fail kirjeldab pooleli jäänud pingejärgija katset, et järgmine sessioon saaks ahela nullist taastada ja vea üles leida. Katse ei kinnitanud pingejärgija tööd ega ADC jaoks ohutut väljundit.

## Vahendid

- USB kaudu toidetud AtomS3R;
- `LM358N`, DIP-8, maketeerimisplaadil;
- UNI-T UT139C multimeeter;
- B5K potentsiomeeter, mõõdetud ligikaudu `4,9 kΩ`;
- B100K potentsiomeeter, mõõdetud ligikaudu `94,8 kΩ`; aktiivses katses ei kasutatud.

## Maketeerimisplaadi reegel ja eeldatud LM358N paigutus

Maketeerimisplaadil ühenduvad ühe rea pesad A–E omavahel ja F–J omavahel. Keskvahe eraldab need rühmad.

Katse ajal kasutati järgmist paigutuse tõlgendust:

| LM358N viik | Maketeerimisplaadi koht |
|---|---|
| pin 1 | E26 |
| pin 2 | E27 |
| pin 3 | E28 |
| pin 4 | E29 |
| pin 8 | rea 26 vastaspool, F–J rühm |

See paigutus ja korpuse suund vajavad enne järgmist pingestatud ülesehitust uut kontrolli.

## Katse ühendused

| Ühendus | Otstarve katse ajal |
|---|---|
| AtomS3R `5V` → G26 | LM358N ja B5K toitesiin |
| AtomS3R `G` → E29 | ühine maa / LM358N pin 4 |
| B5K viigud → A21, A23, A25 | ajutine reguleeritav sisend |
| B21 → C29 | B5K üks ots maale |
| B25 → H26 | B5K teine ots 5 V sõlme |
| C23 → D28 | B5K liugur LM358N sisendile |
| D26 → D27 | LM358N väljundi tagasiside inverteerivale sisendile |

ADC-d ei ühendatud.

## Pidevus- ja toitekontroll

- USB eemaldamise järel ei andnud `+5V` ja GND vaheline pidevuskontroll helisignaali. Kontroll ei leidnud ilmset tugevat lühist.
- Lühistatud multimeetri mõõteotsad andsid helisignaali ja kinnitasid UNI-T UT139C pidevusrežiimi töö.
- C26 ja C27 vaheline pidevus andis lõpuks helisignaali.
- Pidevus LM358N toiteviikude ühendusteni kinnitati.
- LM358 pin 8 ja pin 4 vahel mõõdeti ligikaudu `5 V`.
- D29 ja H26 vahel mõõdeti ühel korral `0,027 V`; kordusmõõtmine andis `5,2 V`. Näidud on vastuolus ning vea põhjus jäi lahtiseks.

## B5K sisend ja ebaõnnestunud pingejärgija katse

B5K liuguri pinge muutus ligikaudu vahemikus `0…5,2 V`. Katseks seati liugur väärtusele `0,401 V`.

| Mõõtekoht | Mõõdetud väärtus | Märkus |
|---|---:|---|
| C26 vs D29, esimene väljundmõõtmine | `0 V` | Sisend pidi olema ligikaudu `0,4 V`; väljund ei järginud sisendit |
| C28 vs D29, eri mõõtmised | `~3,9 V`, `5,222 V`, `~0,4 V` | Vastuolulised sisendnäidud eri hetkedel |
| C26 vs D29, hilisem väljundmõõtmine | `~3,9 V` | Näit püsis kõrge ka pärast sisendi tagasiseadmist ligikaudu `0,4 V` juurde |

Pingejärgija ei käitunud õigesti. Katse ei leidnud algpõhjust. Sisend `~3,9…5,2 V` võib 5 V toitega LM358 lubatud ühispingevahemikust välja jääda ning seda ei kasutata kehtiva pingejärgija katsepunktina.

## Ohutus ja järgmine kontroll

- Ära ühenda LM358 väljundit ega B5K liugurit AtomS3R ADC-ga enne ADC viigu, lubatud pingevahemiku ja väljundi kontrolli.
- Ära käsitle `3,9 V` või `5,2 V` näitu ohutu ADC taseme tõendina.
- Ehita pingejärgija järgmisel korral nullist uuesti.
- Kontrolli LM358N korpuse suund, iga viigu number ja maketeerimisplaadi kontaktid enne USB ühendamist.
- Alusta sisendiga ligikaudu `0,4 V`; mõõda sisend, väljund ja toide samast kinnitatud maapunktist.
- Selgita D29–H26 vastuolulised `0,027 V` ja `5,2 V` näidud enne ADC ühendamist.

MPX5700AP kolme rõhupunkti mõõtmised jäävad TODO: `Vin_atmosphere`, `Vin_full_suction`, `Vin_full_blowing`.
