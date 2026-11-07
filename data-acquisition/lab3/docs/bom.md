# Labor 3 inventuur ja tellimuse tööleht

Tellimise tähtaeg oli **06.11.2026**. [Ühine tellimistabel](https://docs.google.com/spreadsheets/d/11Wf7WONugjfL77vNTto1eWfUyokqos01xseWcNSE6f4/edit?gid=0#gid=0). Siinne dokumentatsioon ei ole ostukinnitus.

Allikas on [ametlik ülesanne](../assignment-EST.md). „Õppejõult” tähendab ülesandes lubatud varustust, mitte meeskonna kinnitatud inventuuri. Füüsiline olemasolu ja inventuuri kuupäev on veel TODO. UV-komponentide dokumenteeritud valik ja tellimisolek on allpool.

| Komponent | Allikas / vastutus | Otstarve ja nõutav kontroll | Füüsiliselt olemas? | Tellida? | Põhjus | Kontrollitud kuupäev |
|---|---|---|---|---|---|---|
| 3/2 solenoidklapp | Õppejõult | Ainult süstal; vooluta atmosfääri; nimipinge/vool mõõta/lugeda | TODO | TODO | Ohutu doseerimine | TODO |
| M5Stack Mini 3A Relay Unit | Õppejõult | COM/ON/OFF tegelik NO/NC, DC induktiivkoormus ja loogika sobivus | TODO | TODO | Lab 3 nõutud klapijuhtimine | TODO |
| Kaks 4 mm Y-kiirliitmikku | Õppejõult | Y1 napale, teine rõhuandurile | TODO | TODO | Ametlik õhuskeem | TODO |
| Metcal 910-B 10 cc must süstal, kolb | Õppejõult, täidab õppejõud | Märgistus, ühendus ja survekindlus kontrollida | TODO | TODO | Üks ülesandes määratud süstlasuurus | TODO |
| Otsikud kolmes suuruses ja korgid | Õppejõult | Kogus ja sobivus kontrollida | TODO | TODO | Põhisari ning teine muutuja | TODO |
| Anycubic Standard Resin | Õppejõult | Tegelik märgistus, ohutusinfo ja 405 nm sobivus | TODO | TODO | Minimaalselt 50 tilga põhisari ja korduskatsed | TODO |
| Kaitseprillid 405 nm, nitriilkindad, IPA, paber | Õppejõu varustus / inventuur | Sobivus ning kogused kontrollida | TODO | TODO | UV ja vaigu ohutus | TODO |
| LM358N | Olemasolu kontroll laboris | Teine pool komparaatoriks pärast Lab 2 puhvriülesande lahendamist; väljund enne Atomit mõõta | TODO | TODO | IRQ lävi ja hüsterees | TODO |
| Kaitsediood | Inventuur; vajadusel lisatellimus | Mähisega rööbiti, polaarsus ning pinge/vool kontrollida | TODO | TODO | Kontakti ja ahela kaitse | TODO |
| Takistid ja kondensaatorid | Riiul / inventuur | Väärtused pärast pärisandmeid, Falstadi ja pinge sobituse arvutust | TODO | TODO | Hüsterees ja vajaduspõhine sobitus/filter | TODO |
| Maketeerimisplaat ja juhtmed | Riiul / inventuur | Ilma jootmiseta, ühenduste kontroll | TODO | TODO | Analoog- ja loogikaahela prototüüp | TODO |
| Ostsilloskoop ja multimeeter | Riiul / inventuur | Kaks kanalit, sobivad sondid ja mõõteulatus | TODO | TODO | GPIO/mähis, NO/NC ja pinged | TODO |
| Nihik | Riiul / inventuur | AtomS3, raami ja vahetükkide füüsilised mõõdud | TODO | TODO | Mudel ning kihi kõrgus; tilgad mõõdetakse kaameraga | TODO |
| XIAO ESP32S3 Sense tööriistakaamera | 3D L2/L3, füüsiline kontroll | Fookus, kõrgus, mm/pixel ja kaamera nihe | TODO | TODO | Pildilt pindala ning paigutus | TODO |
| Hele PLA ja vahetükkide materjal | Inventuur; vajadusel lisatellimus | Mõõtkavaga plaat ja mõõdetud kihi kõrgus | TODO | TODO | Kaamerapõhine tilgamõõtmine | TODO |
| Ekraanipoole mudeli ja musta UV-katte materjal | Koos 3D L3-ga / inventuur | Mudel päris mõõtudest, katte valguslekke kontroll | TODO | TODO | Atomit säästev klaasikatse ja UV-kaitse | TODO |
| 405 nm LED | Meeskonna valik; õppejõud ostab Mouserist | New Energy LST1-01G01-UV04-00; jahutus kontrollida | TODO | `submitted`; ost kinnitamata | Sama valik 3D L3-ga | TODO |
| LED-draiver | Meeskonna valik; õppejõud ostab Mouserist | RECOM RCD-24-0.35/W/X3; toite ja juhtimise sobivus ning auto-off kontrollida | TODO | `submitted`; ost kinnitamata | Kavandatud kõvendamine | TODO |
| LED-i jahutusradiaator | 3D L3 BOM | Würth Elektronik 40905112092424; jahutus kontrollida | TODO | `submitted`; ost kinnitamata | LED-i jahutus | TODO |
| Nõelventiil napi harusse | Tingimuslik lisatellimus | Ainult mõõdetud õhukao/rõhupuuduse korral; kontrollida mõju imemisele | TODO | TODO | Mõõtmisega põhjendatav valik | TODO |
| Lisaotsikud, korgid, voolik ja tihendid | Tingimuslik pärast inventuuri | Tegelikud puudujäägid ja kogused TODO | TODO | TODO | Kordused ja üks märgistatud ummistusotsik | TODO |

Üks meelega kinnine otsik valmistatakse tulevikus meeskonna poolt eraldi süstlast lahti, katte all ja märgistusega; see pole juba olemasolev testitulemus. Ülejäänud osade andmelehed, valiku põhjendused, kogused ja füüsilise inventuuri kuupäevad: **TODO**.

## UV-komponentide valik ja tellimisolek

Allikas: [3D printimise Lab 3 avaldatud BOM, 07.11.2026](https://github.com/Dennel04/3d-printing-course/blob/9cf6bf179b39b055f85b1e05a061bb8c26b49af6/3d-print/lab3/docs/bom.md#uv-komponentide-valik-ja-tellimisolek). `selected` tähendab kinnitatud mudelivalikut, `submitted` rea kandmist ühisesse tellimistabelisse.

| Komponent | Mudel | Mouseri kood | `selected` | `submitted` | `ordered` | `received` | `physically tested` |
|---|---|---|---|---|---|---|---|
| 405 nm LED (rida 10) | New Energy LST1-01G01-UV04-00 | 416-LST101G01UV04 | Jah | Jah, 1 tk | Kinnitamata | Kinnitamata | TODO |
| LED-draiver (rida 11) | RECOM RCD-24-0.35/W/X3 | 919-RCD-24-0.35/W/X3 | Jah | Jah, 1 tk | Kinnitamata | Kinnitamata | TODO |
| Jahutusradiaator (rida 14) | Würth Elektronik 40905112092424 | Siin kinnitamata | Jah | Jah, 1 tk | Kinnitamata | Kinnitamata | TODO |

LED-i andmelehe võrdlustingimus on **500 mA**. Draiveri nimiväljund on **350 mA**; tegelikku LED-i voolu pole mõõdetud. Ühise tabeli rida 15 käsitleb UV-toite lisareleed, mitte Andmehõive klapireleed. 3D BOM-is viidatud M5Stack U023 **3 A / 30 V DC** on kontaktide nimikoormus, mitte LED-i ega draiveri töövool.

**TODO:** kontrollida LED-i päripinget ja jahutust 350 mA juures, draiveri pingevaru 12 V toitega ning UV-toite relee sobivust draiveri püsi- ja käivitusvoolule. Klapirelee kontaktid, induktiivkoormuse sobivus ja elektriline kaitse, sh kaitsediood, vajavad kontrolli. UV sõltumatu ohutu väljalülituse lahendus ning selle toimimine tavaseiskamisel ja juhtsignaali kadumisel on füüsiliselt kontrollimata.
