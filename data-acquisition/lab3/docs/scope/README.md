# Labor 3 ostsilloskoobi tõendite kontrollnimekiri

Tulevased tõendid peavad sisaldama seadistust, telgede ühikuid, dioodi olekut ja seost mõõtetabeliga. Failiteed lisatakse pärast mõõtmist. GPIO näit üksi ei tõenda relee ega klapi ajastust.

- [ ] Klapi mähise väljalülitustipp dioodiga; dioodita ainult õppejõuga kooskõlastatud ohutu protseduuri järgi, sobiva sondi ja ulatusega.
- [ ] Kaks kanalit korraga: Atomi GPIO ja klapi mähise pinge; käsk/GPIO/mähis viie pikkuse kohta, igaüks kümme korda.
- [ ] Relee sisse- ja väljalülitusviivitus, kontaktipõrge; võrdlus täpse relee andmelehega.
- [ ] Rõhk ja klapi mähise pinge samal ajateljel; klapi mehaaniline avanemisviivitus.
- [ ] Kinnise otsiku rõhuläve ületus ja klapi mähise vabastus samal ajateljel.
- [ ] IRQ viivitus kümnel katsel.
- [ ] Polling'u viivitus kümnel katsel.
- [ ] Polling'u viivitus põhitsükli koormuse all; koormatud IRQ võrdlus.
- [ ] Komparaatori väljundi sobivus enne Atomi ühendamist, sh üleminekud.
- [ ] UV auto-off signaal; LED-i puudumisel eraldi märgitud taimeri GPIO-katse.

Failiteed ja mõõteriista seadistused: **TODO: lisada pärast päris mõõtmisi**. [latency.csv](../latency.csv) säilitab meetodi, koormuse ja viivituse ms. Relee mehaaniline lahtilaskmine kuulub viivitusse; õhu/klapi tegelik viivitus tuleb eraldi rõhukõveralt.
