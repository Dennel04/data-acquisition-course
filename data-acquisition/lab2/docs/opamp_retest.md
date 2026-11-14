# Op-amp astme kordustest (pärast 14.11.2026 ümberehitust)

Test kontrollib uuel plaadil ehitatud astet
([skeem ja pesad](opamp_rebuild_2026-11-14.md#6-1411-hilisem-täpsustus-mõõdetud-vahemik-ja-muudetud-plaan)):
B5K-d enam ei ole, `Vref` tuleb B100K-st läbi 47 kΩ / 10 kΩ nõrgendi.

## Quick start (English)

1. Plug the AtomS3R (on the op-amp board, G5 connected) into your computer with a USB-C data cable.
2. Double-click **`run_opamp_retest.bat`** (Windows) or **`run_opamp_retest.command`** (macOS) in `data-acquisition/lab2`.
   The first run sets up Python by itself. Python 3 must be installed.
3. Answer `y` to the safety question, then follow the screen: hold atmosphere, full suction and
   full blowing for 8 seconds each and press Enter when each one is steady. The multimeter question is optional.
4. The result (PASS / WARN / FAIL) is printed and saved in `lab2/data/opamp_retest_<date>/`.
   Send or commit that folder.

## Mida test teeb

- Leiab Atomi pordi ise (Espressif USB VID `303A`). Mitme Atomi korral küsib numbrit.
- Tunneb püsivara ise ära:
  - `DA2_MEASURE_V1` või AUTO: 100 Hz jooksud [`logger.py`](../src/python/logger.py) kaudu, ametlikus
    CSV-skeemis (`config=opamp`, `condition`, `trial`) koos `.runs.jsonl` failiga;
  - [G5-mõõtja](../src/firmware_g5meter/src/main.cpp): ~5 lugemit sekundis, varuvariant.
- Salvestab kolm hoidmist ja hindab:

| Kontroll | Tulemus |
|---|---|
| Väljund järgib rõhku (imemine < atmosfäär < puhumine, vahe ≥ 0,2 V) | FAIL, kui ei |
| Ulatus täis imemisest täis puhumiseni ≥ 1,5 V (disain 2,47 V) | FAIL, kui ei |
| Täis imemisel ei ole väljund alumises piiris kinni (min ≥ 0,054 V, keskmine ≥ 0,10 V) | FAIL, kui on |
| Täis puhumisel ≤ 3,0 V ja ei ole koodi 4095 | FAIL, kui üle |
| Müra atmosfääril ≤ 10 ADC koodi | WARN |
| Iga punkt disainist ±0,25 V piires (0,30 / 0,91 / 2,77 V) | WARN |
| Tuletatud võimendus ±15 % disainist (1,19) | WARN |
| 100 Hz ajastus (ainult DA2) | WARN |

Disaini arvud on faili [`opamp_retest.py`](../src/python/opamp_retest.py) alguses (`RF_K`, `RREF_K`,
`SENSOR_V`, `TARGET_LOW_V`). Plaadi muutumisel muuda neid seal.

Pinge kasutab Labor 1 kalibreerimata tegurit `3,70 V / 4095`; rõhku test ei arvuta. Test ei juhi pumpa.
Tarkvaratestid: `python -m unittest tests.test_opamp_retest` (sünteetilised andmed, seadet ei kasutata).
