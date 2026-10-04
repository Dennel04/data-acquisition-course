# Labor 2 tulevased tarkvaramuudatused

Selles ettevalmistusetapis püsivara ega Pythoni koodi ei rakendata.

## AtomS3 püsivara

- Toetada kahte selgelt valitavat konfiguratsiooni: `raw` ja `opamp`.
- Hoida konfiguratsiooniga seotud ADC ja teisenduse seaded eraldi ning jälgitavad.
- Võtta raw-konfiguratsiooni lähtepunktiks Labori 1 MPX5700AP ülekandefunktsioon `Vout = Vcc · (0,0012858 · P_abs + 0,04)`, 12-bitine ADC, `ADC_11db`, kaheksa lugemi keskmine ja empiiriline koodist pingeks tegur `3,70 V / 4095`. Allikad: `data-acquisition/lab1/src/firmware/include/sensor.h`, `data-acquisition/lab1/src/firmware/src/sensor.cpp` ja `data-acquisition/lab1/docs/sensor_choice.md`. Kontrollida tegur Labor 2 riistvaral uuesti: TODO: real measurement required.
- Säilitada ametliku Labor 2 sisendi diskreetimise siht `100 Hz`. Laboris 1 mõõdeti `1002` rida `10010 ms` jooksul ehk ligikaudu `100,1 Hz`; Labor 2 tegelik sagedus: TODO: real measurement required.
- Kuvada konfiguratsioon nii, et logi ja ekraani olek ei läheks segamini.

## Python logger

- Lisada Labori 1 CSV-skeemile `t_ms,adc,p_kpa,pump` veerg `config`, mille lubatud väärtused on `raw` ja `opamp`.
- Säilitada ajatempel, ADC toorväärtus, suhteline rõhk kilopaskalites ja pumba olek.
- Kontrollida tegelikku diskreetimissagedust ajatemplite järgi. TODO: real measurement required.
- Tagada, et mõlema konfiguratsiooni andmeid saab võrrelda sama skeemi ja ühikutega.

## Pumbajuhtimine

Pumbajuhtimise ühendamine tuleb pärast astme ehitamist, elektrilist kontrolli ja `raw/opamp` võrdlusandmete kogumist. Labori 1 ajalooline lähtejoon oli `off −60 kPa`, `on −40 kPa`, automaatsete taaskäivituste minimaalne väljalülitusaeg `15 s` ja ülempiir `4 käivitust/min` (`data-acquisition/lab1/docs/pump_control.md`). Labor 2 väärtused määratakse uute mõõtmiste põhjal: TODO: real measurement required.
