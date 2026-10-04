# Pumbajuhtimise võrdluse tööleht

See fail täidetakse sama katseprotokolli järgi kogutud `raw` ja `opamp` andmetega. Allpool olev Labori 1 ajalooline lähtejoon pärineb kontrollitud repoallikatest; Labor 2 võrdlustabelitesse lähevad uued sama protokolli mõõtmised.

See on Labor 2 võrdlusmall ega asenda ega muuda Labor 1 ajaloolist `docs/pump_control.md` faili. Ametlik ülesanne nõuab uute tulemuste lisamist vanade väärtuste alla, kuid kursuse repositoorium eraldab laborite failid kataloogidesse `lab1/` ja `lab2/`.

TODO: enne rakendamist otsustada õppejõuga, kas Labor 2 lõplikud tulemused jäävad siia koos viitega Labor 1 ajaloole või tuleb need lisada ka ajaloolisse Labor 1 faili. Kuni otsus puudub, Labor 1 faili ei muudeta.

## Labor 1 ajalooline raw-lähtejoon

Allikas: `data-acquisition/lab1/docs/pump_control.md`. Need arvud kirjeldavad Labori 1 otseühendatud MPX5700AP süsteemi ega ole Labor 2 op-amp tulemused.

| Näitaja | Labor 1 kinnitatud väärtus | Piirang / allikas |
|---|---:|---|
| Väljalülitusrõhk | `−60 kPa` | Lõplik seadistus; varasem `−75 kPa` oli sellel stendil saavutamatu |
| Sisselülitusrõhk | `−40 kPa` | Lõplik seadistus |
| Minimaalne väljalülitusaeg | `15 s` | Kehtib automaatsetele taaskäivitustele |
| Käivituste ülempiir | `4/min` | Kehtib automaatsetele taaskäivitustele; see ei ole iga katse tegelik käivitussagedus |
| Klaas õhus, hoidmine | `0` automaatset taaskäivitust `120 s` jooksul | `lab1_ownbox_hold_air_02.10.26.csv`, rõhk `−77 → −44 kPa` |
| Klaas õhus, teine hoidmine | `0` automaatset taaskäivitust `60 s` jooksul | `lab1_ownbox_hold_air_fw2_02.10.26.csv`, rõhk `−81 → −57 kPa`, `100,0 Hz` |
| Pumba töötsükkel kümne võtmise ajal | `45,2%` | Tavavõtmine; `lab1_pick10_fw3_02.10.26.csv` |
| Pumba töötsükkel kümne lähenemisega võtmise ajal | `29,2%` | `lab1_approach_pick10_02.10.26.csv` |

Labori 1 eraldi anduritestis oli raw-müra atmosfääril `4,84 LSB` ja passiivselt hoitud vaakumil `3,68 LSB`. Teises aknas pump enam ei töötanud, seega ei kirjelda see aktiivse mootori müra. Allikas: `data-acquisition/lab1/docs/sensor_choice.md`. Neid väärtusi ei kasutata Labor 2 SNR-ina.

## Mõõtekonfiguratsioonid

| Väli | Raw | Opamp |
|---|---|---|
| CSV fail | Labori 1 ajalooliste failide skeem `t_ms,adc,p_kpa,pump`; Labor 2 raw: TODO: real measurement required | TODO: real measurement required |
| `config` väärtus | `raw` | `opamp` |
| Diskreetimissagedus (Hz) | Labor 1: `1002` rida / `10010 ms` ≈ `100,1 Hz`; Labor 2: TODO: real measurement required | TODO: real measurement required |
| Anduri ja ADC konfiguratsioon | Labor 1: MPX5700AP otse AtomS3R G5-le, 12 bit, `ADC_11db`, kaheksa lugemi keskmine | MPX5700AP + op-amp; tegelik Labor 2 konfiguratsioon: TODO: real measurement required |
| Katseprotokoll | TODO: real measurement required | TODO: real measurement required |

## Olukordade võrdlus

| Olukord | Konfiguratsioon | Kontrollriba (kPa) | Minimaalne väljalülitusaeg (s) | Käivitused minutis | Märkused |
|---|---|---:|---:|---:|---|
| Napp klaasil | raw | Labor 1 ajalooline `on −40 / off −60`; Labor 2 kordus: TODO: real measurement required | Labor 1 ajalooline `15`; Labor 2 kordus: TODO: real measurement required | Labor 1 hoidmiskatses `0/min` `120 s` jooksul; Labor 2 kordus: TODO: real measurement required | Klaas oli õhus |
| Napp klaasil | opamp | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | |
| Napp õhus | raw | Labor 1 ajalooline `on −40 / off −60`; Labor 2 kordus: TODO: real measurement required | Labor 1 ajalooline `15`; Labor 2 kordus: TODO: real measurement required | TODO: real measurement required | Labor 1 varasem katse ei kasutanud lõplikku Labor 2 protokolli |
| Napp õhus | opamp | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | |
| Voolik korgiga | raw | Labor 1 ajalooline `on −40 / off −60`; Labor 2 kordus: TODO: real measurement required | Labor 1 ajalooline `15`; Labor 2 kordus: TODO: real measurement required | TODO: real measurement required | Labor 1 varasem katse ei kasutanud lõplikku Labor 2 protokolli |
| Voolik korgiga | opamp | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | |
| Poolik haare | raw | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | |
| Poolik haare | opamp | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | |

## Lahutusvõime ja signaali kvaliteet

| Näitaja | Raw | Opamp | Arvutus / allikas |
|---|---:|---:|---|
| Pa ühe ADC sammu kohta | Labor 1 arvutus `0,1405 kPa/kood = 141 Pa/kood`; Labor 2 kontroll: TODO: real measurement required | TODO: real measurement required | `q_P = q_V / S_P` koos vastava astme võimendusega |
| Signaalitase (kPa) | TODO: real measurement required | TODO: real measurement required | sama Labor 2 impulsi platoo keskmine − baasjoone keskmine |
| Platoo müra standardhälve (kPa) | TODO: real measurement required | TODO: real measurement required | sama ajavahemik ja ühikud; Labor 1 LSB-vaatlus ei asenda seda |
| SNR (dB) | TODO: real measurement required | TODO: real measurement required | `20 · log10(|signal| / noise_std)` |

## Pooliku haarde eristamine

Laboris 1 poolikut haaret ei mõõdetud. Eristamise kriteerium ja läviväärtus: TODO: real measurement required.

| Konfiguratsioon | Eristamise aeg (s) | Algushetke määratlus | Meetod |
|---|---:|---|---|
| Raw | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required |
| Opamp | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required |

## Järeldus

- Kas kontrollriba muutus: TODO: real measurement required.
- Kas käivituste arv muutus: TODO: real measurement required.
- Kas lahutusvõime või SNR paranes: TODO: real measurement required.
- Kas poolik haare eristus varem: TODO: real measurement required.
- Kas aste oli põhjendatud: TODO: real measurement required.
