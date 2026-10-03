# Pumbajuhtimise võrdluse tööleht

See fail täidetakse sama katseprotokolli järgi kogutud `raw` ja `opamp` andmetega. Labori 1 väärtusi ei kopeerita ega tuletata ilma kontrollita.

See on Labor 2 võrdlusmall ega asenda ega muuda Labor 1 ajaloolist `docs/pump_control.md` faili. Ametlik ülesanne nõuab uute tulemuste lisamist vanade väärtuste alla, kuid kursuse repositoorium eraldab laborite failid kataloogidesse `lab1/` ja `lab2/`.

TODO: enne rakendamist otsustada õppejõuga, kas Labor 2 lõplikud tulemused jäävad siia koos viitega Labor 1 ajaloole või tuleb need lisada ka ajaloolisse Labor 1 faili. Kuni otsus puudub, Labor 1 faili ei muudeta ega selle väärtusi siia kopeerita.

## Mõõtekonfiguratsioonid

| Väli | Raw | Opamp |
|---|---|---|
| CSV fail | TODO: real measurement required | TODO: real measurement required |
| `config` väärtus | `raw` | `opamp` |
| Diskreetimissagedus (Hz) | TODO: real measurement required | TODO: real measurement required |
| Anduri ja ADC konfiguratsioon | TODO: Lab 1 data required | TODO: Lab 1 data required; TODO: real measurement required |
| Katseprotokoll | TODO: real measurement required | TODO: real measurement required |

## Olukordade võrdlus

| Olukord | Konfiguratsioon | Kontrollriba (kPa) | Minimaalne väljalülitusaeg (s) | Käivitused minutis | Märkused |
|---|---|---:|---:|---:|---|
| Napp klaasil | raw | TODO: Lab 1 data required | TODO: Lab 1 data required | TODO: Lab 1 data required | |
| Napp klaasil | opamp | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | |
| Napp õhus | raw | TODO: Lab 1 data required | TODO: Lab 1 data required | TODO: Lab 1 data required | |
| Napp õhus | opamp | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | |
| Voolik korgiga | raw | TODO: Lab 1 data required | TODO: Lab 1 data required | TODO: Lab 1 data required | |
| Voolik korgiga | opamp | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | |
| Poolik haare | raw | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | |
| Poolik haare | opamp | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | |

## Lahutusvõime ja signaali kvaliteet

| Näitaja | Raw | Opamp | Arvutus / allikas |
|---|---:|---:|---|
| Pa ühe ADC sammu kohta | TODO: Lab 1 data required | TODO: Lab 1 data required; TODO: real measurement required | `q_P = q_V / S_P` koos vastava astme võimendusega |
| Signaalitase (kPa) | TODO: Lab 1 data required | TODO: real measurement required | platoo keskmine − baasjoone keskmine |
| Platoo müra standardhälve (kPa) | TODO: Lab 1 data required | TODO: real measurement required | sama ajavahemik ja ühikud |
| SNR (dB) | TODO: Lab 1 data required | TODO: real measurement required | `20 · log10(|signal| / noise_std)` |

## Pooliku haarde eristamine

Eristamise kriteerium: TODO: Lab 1 data required; TODO: real measurement required.

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
