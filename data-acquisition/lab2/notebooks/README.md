# Labor 2 analüüsi töövoog

Notebook'id luuakse pärast päris `raw` ja `opamp` CSV-failide kogumist. Praegu andmeid ega tulemusi ei looda.

Kavandatud töövoog:

1. Laadi `raw` ja `opamp` read ning kontrolli kohustuslikke veerge, ühikuid ja `config` väärtusi.
2. Arvuta ajatemplite vahedest tegelik diskreetimissagedus. Ametliku sisendi siht on `100 Hz`; Labori 1 kontroll oli `1002` rida `10010 ms` jooksul ehk ligikaudu `100,1 Hz`. Labor 2 tegelik sagedus: TODO: real measurement required.
3. Vali võrreldavad, sama protokolliga pumbaimpulsid mõlemas konfiguratsioonis.
4. Teisenda raw-andmed Labori 1 kontrollitud lähtepunktist: MPX5700AP, 12-bitine `ADC_11db`, empiiriline teisendus `3,70 V / 4095` ja andmelehe ülekandefunktsioon. See andis arvutuslikult `0,1405 kPa/kood = 141 Pa/kood`. Kontrolli teisendus Labor 2 riistvaral ning määra op-amp teisendus: TODO: real measurement required.
5. Arvuta spektrid sama meetodi, akna, telgede, sagedusvahemiku ja ühikutega.
6. Arvuta signaalitase: platoo keskmine miinus baasjoone keskmine.
7. Arvuta platoo müra standardhälve samaväärses stabiilses ajavahemikus.
8. Arvuta `SNR_dB = 20 · log10(|signal| / noise_std)`.
9. Arvuta Pa ühe ADC sammu kohta enne ja pärast astet kontrollitud ülekandefunktsioonidest. Võrdle tulemust Labori 1 raw-lähtejoonega `141 Pa/kood`; ära käsitle seda Labor 2 mõõdetud väärtusena.
10. Koosta `raw` ja `opamp` võrdlus samade telgede, ühikute, intervallide ja kokkuvõtlike tabelitega.

Labori 1 CSV lähteveergude skeem: `t_ms,adc,p_kpa,pump`. Labor 2 fail lisab veeru `config`.

Labor 2 andmefailid: TODO: real measurement required.

Analüüsitulemused: TODO: real measurement required.
