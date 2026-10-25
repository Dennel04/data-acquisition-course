# Labor 3 püsivara ja logija plaan

Selles ettevalmistuses püsivara ega logijat ei rakendata. Liidesed, viigud, riistvara ja Labori 2 korduskasutus tuleb enne koodi kontrollida.

## Tulevane Atomi püsivara

- vastu võtta `dispense` käsk;
- vastu võtta `uv` käsk;
- vastu võtta alarmi `clear` käsk;
- ajastada klapi impulss riistvarataimeriga;
- tagada UV LED-i riistvarataimeri või muu sõltumatu mehhanismiga automaatne väljalülitus;
- teenindada komparaatori katkestust;
- lukustada alarm kuni `clear` käsuni;
- teha ISR-is ainult klapi ohutusse olekusse viimine ja lipu seadmine;
- väljastada sündmus ning uuendada ekraani väljaspool ISR-i;
- käivituda ohutus vaikeolekus: klapp vooluta, süstal atmosfääri ja pumbast lahutatud, UV väljas, doseerimine keelatud alarmi ajal;
- logida rõhukõverad koos üheselt seotud `drop_id` väärtusega.

## Tulevane arvuti logija

- saata Atomi käsud;
- püüda ja säilitada sündmused;
- logida lähte- ja vastuvõtuajatemplid;
- siduda `drop_id` õige rõhukõveraga;
- säilitada toorproovid muutmata;
- eksportida selge skeemiga analüüsisõbralik CSV;
- kontrollida tegelikku diskreetimissagedust ajatemplite põhjal.

## Enne rakendamist

- Labori 2 lõplik püsivara ja CSV-skeem: **TODO: kontrollida**.
- Klapi, M5Stack Mini 3A Relay Unit mooduli, LED-draiveri ja LM358N komparaatori ühendused: **TODO: päris riistvara**.
- Atomi viigud ja nende pingepiirid: **TODO: kinnitada andmelehtedest ja stendilt**.
- Tuvastustunnus, filter ja läved: **TODO: valida ainult pärisandmetest**.

## Ajakohase ülesande piirid

See on [ametliku ülesande](../assignment-EST.md) teostusplaan. Klapp juhib ainult süstlaharu; iminapp on Y kaudu otse pumbaga ühendatud. GPIO, aktiivne signaalitase, releekontakt, mähise toide ja taimeri parameetrid jäävad TODO kuni riistvara ja kasutatava lähtekoodi kontrollini.

IRQ peab kohe andma releele käsu klapp vooluta viia ja seadma lipu; ülejäänud alarmi lukustus, ekraan ning USB-sündmus tehakse põhitsüklis, enne uut doseerimist. Oodatud platoo ja tühja süstla ajapiir määratakse pärisandmetest. Relee mehaaniline viivitus ei kao GPIO kiire lülitamisega.

Logija peab siduma drop_id ka foto ja [drops.csv](../data/drops.csv) rõhukõveraga; [placement.csv](../data/placement.csv) seob mudeli ja foto. Algproovid, ajatemplid ja algpildid säilitatakse; kaameratöötlus ning mm²/µL arvutus on tulevane analüüs, mitte selles sessioonis loodav juhtkood.
