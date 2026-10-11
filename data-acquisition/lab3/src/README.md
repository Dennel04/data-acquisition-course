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
- käivituda ohutus vaikeolekus: klapp iminapa harule, UV väljas, doseerimine keelatud alarmi ajal;
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
- Klapi, MOSFET-i, LED-draiveri ja komparaatori ühendused: **TODO: päris riistvara**.
- Atomi viigud ja nende pingepiirid: **TODO: kinnitada andmelehtedest ja stendilt**.
- Tuvastustunnus, filter ja läved: **TODO: valida ainult pärisandmetest**.
