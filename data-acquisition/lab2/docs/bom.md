# Labor 2 BOM-i ja tellimuse tööleht

04.10.26 sessioonil füüsiliselt nähtud osad on allpool eraldi märgitud. Füüsiline olemasolu ei kinnita elektrilist korrasolekut, täpset kogust ega seda, et osa sobib lõplikku astmesse. Ühtegi tellimisotsust ei ole veel tehtud.

See on eraldi Labor 2 tellimisleht. Labor 1 `docs/bom.md` jääb ajalooliseks Labor 1 dokumendiks; selle sisu ei kopeerita ega muudeta siin. Meeskond peab Labor 2 komponentide saadavust uuesti füüsiliselt kontrollima.

## Füüsilise inventuuri kontrollnimekiri

- [ ] Kontrolli füüsiliselt tuvastatud `LM358N` DIP-8 variandi viigustik andmelehelt.
- [ ] Loe anduri markeering korpuselt.
- [ ] Kinnita maketeerimisplaadi täpne mudel ja mõõda toiteallika pinge; 04.10.26 kirjeldus on lisatud.
- [ ] Sorteeri esimese versiooni jaoks kaalutavad takistid; kirjuta iga nimiväärtuse juurde kogus.
- [ ] Mõõda kasutatavad takistid multimeetriga ja kirjuta tegelikud väärtused `docs/bench_session.md` faili.
- [ ] Kontrolli multimeetri, mõõtejuhtmete ja ühise maa ühenduse korrasolekut.
- [ ] Märgi iga BOM-i rea juures `Riiulis olemas?` ja `Tellida?` alles pärast füüsilist kontrolli.

| Osa | Kogus | Otstarve | Vajalik väärtus / spetsifikatsioon | Riiulis olemas? | Tellida? | Põhjus |
|---|---:|---|---|---|---|---|
| Op-amp | Vähemalt 1 tk; varueksemplare ei loendatud | Signaali nihutamine ja skaleerimine | `LM358N`, DIP-8, korpuselt kinnitatud; viigustik ja väljundulatus tegelikul toitepingel: TODO: datasheet check required; TODO: real measurement required | Jah, vähemalt 1 tk oli 04.10.26 füüsiliselt olemas | TODO: final design and spare requirement | Kontrollida viigustikku, väljundulatust ja varueksemplari vajadust |
| Takistid | Täpsed kogused: TODO: count physically | Võimenduse ja viitepinge määramine | Nähtud nimiväärtused `10 kΩ`, `20 kΩ`, `6,8 kΩ`, `47 kΩ`, `3,3 kΩ`; tegelikud takistused: TODO: real measurement required; lõplikud väärtused: TODO: circuit design required pärast tegelike `Vin` otspunktide mõõtmist | Jah, loetletud nimiväärtuste ribad olid 04.10.26 nähtaval; elektriliselt kontrollimata | TODO: final circuit values and quantities | Vajalikud suhtarvud selguvad mõõdetud sisendvahemikust; lõplikku tellimisvajadust ei saa veel otsustada |
| Kondensaatorid | TODO: physical inventory required | Ainult arvutuse või skeemi põhjendatud vajaduse korral | TODO: circuit design required | TODO: physical inventory required | TODO: physical inventory required | Lisada ainult põhjendatud vajaduse korral |
| Maketeerimisplaat | 1 tk kasutati Labor 2 jaoks | `raw` ja `opamp` ahelate samaaegne säilitamine | Suur MB-102 tüüpi jootmisvaba maketeerimisplaat | Jah, kasutati 04.10.26 | TODO: confirm final setup needs | Labor 1 anduriahel jäeti terveks; Labor 2 jaoks kasutati eraldi plaati |
| Ühendusjuhtmed | Kogus: TODO: count physically | Maketeerimisplaadi ühendused | Jumper-juhtmed; sobivus ja vajalik kogus kontrollida lõpliku skeemi järgi | Jah, kasutati 04.10.26 | TODO: confirm final setup needs | AtomS3R `5V` ja GND ühendati maketeerimisplaadi toitesiinidele; pinget ei mõõdetud |
| Muu | TODO: physical inventory required | TODO: circuit design required | TODO: circuit design required | TODO: physical inventory required | TODO: physical inventory required | TODO: physical inventory required |
