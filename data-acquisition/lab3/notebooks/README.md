# Labor 3 analüüsiplaan

Märkmikud luuakse pärast pärisandmete kogumist ja on korratavad algsetest CSV-dest ning fotodest. Need ei asenda füüsilisi mõõtmisi. [Ametlik järjestus](../assignment-EST.md) ja [andmeskeem](../data/README.md) on alus.

## Tilgad ja paigutus

- Seansi mõõtkava mm/pixel, stabiilse töökõrguse, fookuse ja valguse kontroll; väikseima tilga läbimõõt pikslites.
- Segmenteerimine, kontuuri tagasijoonistus ja visuaalne kontroll, pindala px → mm².
- Ruumala µL = pindala mm² × tegelikult mõõdetud vahetüki kõrgus mm; ühe piiripiksli ning skaala mõju mõõtemääramatusele protsentides.
- Vähemalt viis impulsi pikkust × kümme kordust, kaks 5 × 5 plaati põhisarjaks; sama drop_id foto ja rõhukõvera kontroll.
- Suuruse/ruumala ja impulsi kestuse lineaarsus, kõrvalekalde algus ning põhjus tegelike andmete põhjal; graafik hajuvuse/veapiiridega.
- CV = standardhälve / keskmine, protsentides 100 × CV, eraldi lineaarsuse hinnangust.
- Esimese impulsi mõju pärast pausi; teine otsik või rõhk kolme impulsi pikkusega.
- Rõhuplatoo / kõvera pindala seos tilga suuruse ja ruumalaga.
- placement.csv: laigu pindala klaasi all, keskme x/y nihe ekraani keskpunktist, servani jõudmine ja tõendipildid.

## Filter, tuletis ja otsus

1. Päris rõhu-CSV ning kalibratsiooni ja tegeliku ajatemplite vahe kontroll; toores dP/dt ühikus kPa/s.
2. Rõhu ja tuletise spektrid ning sagedusvõimenduse 2πf selgitus.
3. Libisev keskmine ja mediaan enne tuletist; numbriline müra/viivituse tabel ja põhjendatud valik.
4. Valitud meetod kontrollitud Lab 2 pooliku haarde logile pärast pumba väljalülitumist; eristamise lävi ja aeg otsuseni. Logi puudumisel TODO.
5. normal / clogged / empty rõhuplatoo, tõusu ja languse võrdlus; tunnus ning tühja süstla lubatud platooni jõudmise aeg ainult pärisandmetest.
6. IRQ ja polling'u viivitus: kümme mõõtmist kummagi meetodiga, lisaks põhitsükli koormus. Mõõte lõpp on klapi mähise vabastus, mitte ainult GPIO muutus.
7. Keskmine, halvim, arendusajad ja valiku põhjus; relee sisse-/väljalülitus, kontaktipõrge, eluiga andmelehe ning päevase tilgaarvu järgi.
8. clogged ×10, empty ×10 tabamised ja normal ×30 valehäired.

Kõik graafikud, filtrid, läved ja järeldused: **TODO: päris andmed**.
