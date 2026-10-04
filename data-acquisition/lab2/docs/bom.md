# Labor 2 BOM-i ja tellimuse tööleht

Komponentide saadavus kontrollitakse füüsiliselt. Ükski allolev rida ei kinnita, et osa on riiulis või tellitud.

See on eraldi Labor 2 tellimisleht. Labor 1 `docs/bom.md` jääb ajalooliseks Labor 1 dokumendiks; selle sisu ei kopeerita ega muudeta siin. Meeskond peab Labor 2 komponentide saadavust uuesti füüsiliselt kontrollima.

## Füüsilise inventuuri kontrollnimekiri

- [ ] Loe op-ampi kogu markeering korpuselt ja kontrolli selle variandi viigustik andmelehelt.
- [ ] Loe anduri markeering korpuselt.
- [ ] Kirjelda kasutatav maketeerimisplaat ja toiteallikas.
- [ ] Sorteeri esimese versiooni jaoks kaalutavad takistid; kirjuta iga nimiväärtuse juurde kogus.
- [ ] Mõõda kasutatavad takistid multimeetriga ja kirjuta tegelikud väärtused `docs/bench_session.md` faili.
- [ ] Kontrolli multimeetri, mõõtejuhtmete ja ühise maa ühenduse korrasolekut.
- [ ] Märgi iga BOM-i rea juures `Riiulis olemas?` ja `Tellida?` alles pärast füüsilist kontrolli.

| Osa | Kogus | Otstarve | Vajalik väärtus / spetsifikatsioon | Riiulis olemas? | Tellida? | Põhjus |
|---|---:|---|---|---|---|---|
| Op-amp | TODO: physical inventory required | Signaali nihutamine ja skaleerimine | Õppejõu lähtekomponent on LM358N; täpne olemas olev variant ja selle väljundulatus tegelikul toitepingel: TODO: physical inventory required; TODO: real measurement required | TODO: physical inventory required | TODO: physical inventory required | Kontrollida markeeringut, viigustikku ja väljundulatust |
| Takistid | TODO: physical inventory required | Võimenduse ja viitepinge määramine | TODO: circuit design required pärast tegelike `Vin` otspunktide mõõtmist | TODO: physical inventory required | TODO: physical inventory required | Vajalikud suhtarvud selguvad mõõdetud sisendvahemikust |
| Kondensaatorid | TODO: physical inventory required | Ainult arvutuse või skeemi põhjendatud vajaduse korral | TODO: circuit design required | TODO: physical inventory required | TODO: physical inventory required | Lisada ainult põhjendatud vajaduse korral |
| Maketeerimisplaat | TODO: real measurement required | `raw` ja `opamp` ahelate samaaegne säilitamine | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required |
| Ühendusjuhtmed | TODO: real measurement required | Maketeerimisplaadi ühendused | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required | TODO: real measurement required |
| Muu | TODO: physical inventory required | TODO: circuit design required | TODO: circuit design required | TODO: physical inventory required | TODO: physical inventory required | TODO: physical inventory required |
