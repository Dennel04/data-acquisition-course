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
| Potentsiomeetrid | Vähemalt 1 B5K ja 1 B100K | Ajutine reguleeritav diagnostikasisend | B5K mõõdeti ligikaudu `4,9 kΩ`; B100K ligikaudu `94,8 kΩ` | Jah, mõlemad mõõdeti 11.10.26 | TODO: final circuit decision | B5K kasutati ajutise testallikana; B100K aktiivses katses ei kasutatud. Kumbagi ei ole valitud lõpliku astme komponendiks. |
| Kondensaatorid | TODO: physical inventory required | Ainult arvutuse või skeemi põhjendatud vajaduse korral | TODO: circuit design required | TODO: physical inventory required | TODO: physical inventory required | Lisada ainult põhjendatud vajaduse korral |
| Maketeerimisplaat | 1 tk kasutati Labor 2 jaoks | `raw` ja `opamp` ahelate samaaegne säilitamine | Suur MB-102 tüüpi jootmisvaba maketeerimisplaat | Jah, kasutati 04.10.26 | TODO: confirm final setup needs | Labor 1 anduriahel jäeti terveks; Labor 2 jaoks kasutati eraldi plaati |
| Ühendusjuhtmed | Kogus: TODO: count physically | Maketeerimisplaadi ühendused | Jumper-juhtmed; sobivus ja vajalik kogus kontrollida lõpliku skeemi järgi | Jah, kasutati 04.10.26 | TODO: confirm final setup needs | AtomS3R `5V` ja GND ühendati maketeerimisplaadi toitesiinidele; pinget ei mõõdetud |
| Muu | TODO: physical inventory required | TODO: circuit design required | TODO: circuit design required | TODO: physical inventory required | TODO: physical inventory required | TODO: physical inventory required |


## 22.10.2026 — Katses kasutatud komponendid (Maksim)

Paigutus ja ühendused: [LM358N koostamisjuhend](lm358n_wiring_2026-10-22.md).
Algallikas: [Maksimi muutmata Word](sources/lab2-sborka-2026-10-22.docx).
Allikas ei lisa uut inventuuri ega kinnita varuosade või tellimisvajaduse seisu.

Järgmised komponendid olid kasutusel LM358N katseskeemi koostamisel ja mõõtmisel.

| Komponent | Kogus | Kasutus |
|---|---:|---|
| LM358N DIP-8 | 1 | Võimendusaste ja viitepinge puhver |
| 10 kΩ takisti | 1 | Tagasiside, mõõdetud 10,04 kΩ |
| 2 kΩ takisti | 3 | Jadaühendus, mõõdetud kogutakistus 6,51 kΩ |
| 1 kΩ takisti | 1 | Potentsiomeetrite toiteahelas |
| B5K potentsiomeeter | 1 | Reguleeritav testsisend |
| B100K potentsiomeeter | 1 | Reguleeritav viitepinge |
| Maketeerimisplaat | 1 | Skeemi koostamine |
| AtomS3R | 1 | Toide, GND ja ADC sisend G5 |
| Ühendusjuhtmed | Mitu | Skeemi ühendused |

**Märkus:** B100K potentsiomeeter oli selles katses kasutusel viitepinge seadmiseks. MPX5700AP andurit selle mõõtesessiooni ajal katseskeemi sisendina ei kasutatud.

Komponentide loend kirjeldab katses kasutatud lahendust, mitte veel lõplikult kinnitatud andmehõivesüsteemi.


## 15.11.2026 — ehitatud astme komponendid (uus plaat 14.11)

Allikad: [pesade tabel](opamp_rebuild_2026-11-14.md#6-1411-hilisem-täpsustus-mõõdetud-vahemik-ja-muudetud-plaan),
[plaadi foto 15.11](breadboard_final_2026-11-15.jpg), [Falstadi mudel](falstad_team_stage_2026-11-15.txt) ja 15.11 multimeetri näidud.
Kogused on loetud pesade tabelist, mitte füüsilisest inventuurist. Kõik osad on plaadil olemas ja aste töötab
(14.11 kordustest PASS, 15.11 G5 0,865 V atmosfääril). Varuosi ja riiuli seisu ei loendatud.

| Osa | Kogus | Kus / otstarve | Väärtus | Mõõdetud | Tellida? |
|---|---:|---|---|---|---|
| LM358N DIP-8 | 1 | read 20–23; pool 1 võimendusaste, pool 2 `Vref` puhver (follower) | — | — | Ei, ehitatud |
| MPX5700AP | 1 | J1–J6, väljund pin 1 → C22 (`Vin`, LM358N pin 3) | 5 V toide | toide 5 V; väljund 0,837 V atmosfääril (15.11) | Ei |
| AtomS3R | 1 | 5V D62, GND D63, G5 H60; DA2_MEASURE_V1 | — | — | Ei |
| Takisti 10 kΩ | 2 | `Rf` (A21 → A15) ja nõrgendi alumine haru (G32 → G38) | 10 kΩ | 22.10 tagasiside 10,04 kΩ (vana plaat, sama osa ei ole kinnitatud) | Ei |
| Takisti 47 kΩ | 2 | nõrgendi ülemine haru (I36 → I32) ja `Rref` osa (D27 → G27) | 47 kΩ | `Rref` kokku ~54 kΩ (pin 2–pin 7, 15.11) | Ei |
| Takisti 6,8 kΩ | 1 | `Rref` osa (B21 → B27) | 6,8 kΩ | vt `Rref` kokku | Ei |
| Takisti 2 kΩ | 1 | puhvri väljundi allatõmme (I21 → GND) | 2 kΩ | — | Ei |
| Takisti 3,3 kΩ | 1 | väljundi jadatakisti G5 suunas (C20 → C12) | 3,3 kΩ | — | Ei |
| Kondensaator 0,1 µF | 1 | G5 sõlmest GND-sse (E12 → GND), koos 3,3 kΩ-ga ~482 Hz | 0,1 µF (100 nF) | — | Ei |
| Potentsiomeeter B100K | 1 | `Vref` seadmine (J34/J36/J38) | 100 kΩ | 11.10: ~94,8 kΩ; `Vref` ≈ 0,69 V (15.11 arvutus) | Ei |
| Maketeerimisplaat MB-102 | 1 | uus plaat 14.11 (vana plaat oli vigaste kontaktidega) | — | — | Ei |
| Ühendusjuhtmed / hüppajad | mitu | siinide sillad, puhvri hüppaja H22 → H21, `Vref` hüppaja H32 → H23, `Rf` B15 → B20, `Rref` J27 → J21, G5 A12 → J60 | — | — | Ei |
| B5K potentsiomeeter | 0 | lõplikus astmes ei kasutata (14.11 eemaldatud) | — | 11.10: ~4,9 kΩ | Ei |

`raw` võrdluskatseks lisandub ainult üks hüppaja (A22 → J60 A12 → J60 asemel), uusi osi ei vaja.

Lahti (füüsiline kontroll, ainult meeskond saab teha): varuosade kogused riiulis, iga takisti eraldi mõõdetud väärtus
ning ülaltoodud inventuuri kontrollnimekirja punktid.

- 15.11.26 kontroll: [plaadi fotol](breadboard_final_2026-11-15.jpg) on näha 6 takistit ja kollane keraamiline kondensaator (0,1 µF);
  seitsmes takisti (47 kΩ liugurist sõlme X) on tõenäoliselt B100K korpuse all. Ümberehituse juhendi (14.11 artifact) osade loend
  „10 kΩ ×2, 6,8 kΩ, 2 kΩ, 47 kΩ ×2, 3,3 kΩ, 0,1 µF, hüppajad“ langeb ülaltoodud tabeliga kokku. Takistite värvikoode fotolt ei loetud.
