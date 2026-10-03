# Labor 2 tulevased tarkvaramuudatused

Selles ettevalmistusetapis püsivara ega Pythoni koodi ei rakendata.

## AtomS3 püsivara

- Toetada kahte selgelt valitavat konfiguratsiooni: `raw` ja `opamp`.
- Hoida konfiguratsiooniga seotud ADC ja teisenduse seaded eraldi ning jälgitavad.
- Kasutada ainult kontrollitud anduri- ja kalibratsioonikonstante. TODO: Lab 1 data required; TODO: real measurement required.
- Säilitada ametliku Labor 2 sisendi diskreetimise siht `100 Hz`. Selle saavutamine Laboris 2: TODO: real measurement required.
- Kuvada konfiguratsioon nii, et logi ja ekraani olek ei läheks segamini.

## Python logger

- Lisada igale CSV reale veerg `config`, mille lubatud väärtused on `raw` ja `opamp`.
- Säilitada ajatempel, ADC toorväärtus ja olemasolevad kontrollitud füüsikalised ühikud.
- Kontrollida tegelikku diskreetimissagedust ajatemplite järgi. TODO: real measurement required.
- Tagada, et mõlema konfiguratsiooni andmeid saab võrrelda sama skeemi ja ühikutega.

## Pumbajuhtimine

Pumbajuhtimise ühendamine tuleb pärast astme ehitamist, elektrilist kontrolli ja `raw/opamp` võrdlusandmete kogumist. Kontrollriba, minimaalne väljalülitusaeg ja muud juhtimisväärtused: TODO: Lab 1 data required; TODO: real measurement required.
