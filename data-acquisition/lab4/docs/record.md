# Ühise tsüklikande ettepanek

**ETTEPANEK · OOTAB KOKKULEPET.** Andmehõive, Nutikate Lahenduste ja teiste osalevate meeskondade kinnitus on vajalik enne esimese päristsükli salvestamist. Lukusta kinnitatud kuju pärast kaitsmist Labori 5 jaoks. Õppejõu näite väljad moodustavad tabeli esimesed 13 rida. Järgmised väljad on meeskondadele arutamiseks.

## Väljad CSV päise järjekorras

| Väli | Tüüp või ühik | Päritolu ja tähendus |
| --- | --- | --- |
| `cycle` | positiivne täisarv | Jaam eraldab järgmise numbri püsivalt enne tsükli käivitamist. |
| `team` | tunnus | Meeskonnale antud püsitunnus, kontrollitakse saatja õiguse vastu. |
| `t` | ISO 8601, UTC `Z` | Tsükli algusaeg jaama kellalt. Vastuvõtu aeg jääb eraldi andmebaasi metaandmetesse. |
| `tip` | mm | Otsiku nimiläbimõõt tootja märgistusest. Seansi seadistuslogi seob täpse tüübi ja tunnuse tsükliga. |
| `pressure_kpa` | kPa, atmosfääri suhtes | Kalibreeritud anduri keskmine doseerimiseelse seadehetke kokkulepitud aknas. Seanss talletab akna, anduri asukoha, märgikonventsiooni ja kalibratsiooni. |
| `pulse_ms` | ms | Atomile selleks tsükliks antud doseerimisimpulsi käsk. Tegeliku mähise impulsi tõend säilib eraldi mõõtefailis. |
| `drop_area_mm2` | mm², tühi mõõtmisvea korral | Kaamera segmendi pindala seansi mõõtkavas. Null on lubatud kontrollitud laiguta pildil, kui kaader läbib kvaliteedikontrolli. |
| `drop_target_mm2` | mm² | Katseplaanis seatud sihtpindala, ka püsiretseptiga võrdlusseerias. |
| `label` | `normal`, `blocked`, `empty` | Kinnitatud tegelik olukord. Lahtise või katkestatud tsükli puhul võib väli olla tühi kuni olukorra kinnitamiseni. |
| `label_source` | `human`, `image`, `scale` | Olukorra tuvastamise peamine viis. Tõend ja vastuolud lähevad väljale `label_ref` või `note`. |
| `syringe_g` | g, tühi kaalumata tsüklil | Vahetult pärast tsüklit kaalutud süstla mass fikseeritud koostisega. Kaalumise aeg ning süstla koostis säilivad seansi tõendis. |
| `curve` | suhteline failitee | Jaama salvestatud toorproovid ja kalibreeritud rõhk, kui kalibratsioon kehtib. |
| `image` | suhteline failitee | Algne tööriistakaamera fail või kaadri manifest. |
| `schema_version` | tunnus | Osapoolte kinnitatud kirjekuju versioon. |
| `station_id` | tunnus | Andmeid salvestava jaama püsitunnus. |
| `run_id` | tunnus | Katseseanss, seob retsepti, seadete plaani ja kalibratsioonid. |
| `run_cycle` | positiivne täisarv | Tsükli järjekorranumber seerias. Kaalumise samm tuleb katseplaanist, mitte üle seansside kasvavast tsüklivõtmest. |
| `series` | `pilot`, `dataset`, `comparison`, `recovery`, `verification` | Katseplaani põhiseeria. |
| `mode` | `recipe`, `feedback`, `model_feedback`, tühi | Jaama aktiivne juhtimisviis. Juhuslikustatud avatud juhtimise katsel jäta väli tühjaks ja loe seaded katseplaanist. |
| `pressure_setpoint_kpa` | kPa, atmosfääri suhtes | Katseseadistus või juhtimise siht. Mõõdetud rõhk jääb oma väljale. |
| `measurement_status` | `measured`, `no_drop`, `not_measured` | Pilditöötluse väljund. `no_drop` eeldab kasutuskõlblikku kaadrit ja lisakontrolli. `not_measured` nõuab põhjust. |
| `label_ref` | tõendiviide | Viide kontrollpildile, vaatlusele või kaalumise kirjele koos olukorra tuvastamise alusega. |
| `cad_config_id` | tunnus | Seansi metaandmed seovad jaama detailiversiooni, paigutuse, tööriista, kaamera ja kalibratsiooni. |
| `workflow_version` | tunnus | Nutikate Lahenduste salvestatud töövoo versioon või commit. |
| `cycle_status` | `completed`, `aborted` | Jaama töövoo lõppseis katse protokolli järgi. Kavandatud veakatse võib lõppeda kontrollitud väljalülitusega. Katkenud tsüklile jääb püsiv võti ja katkestuse põhjus. |
| `duration_s` | s | Aeg algusest töövoo lõpuni või katkestuseni, jaama monotoonse kella järgi. |
| `note` | tekst, vajadusel tühi | Puuduva väärtuse põhjus, katkestus, ebatavaline sündmus või tõendite vastuolu. |

## Identiteet, failid ja kvaliteet

- Võtme ettepanek on `(team, station_id, cycle)`. Jaam säilitab numeratsiooni üle taaskäivituste ja ei anna sama numbrit teisele tsüklile. Katkestus ja kordussaatmine säilitavad sama võtme. Kui jaam asendatakse või taastatakse varukoopiast, kontrolli enne uut tsüklit numeratsiooni või anna uus jaamatunnus.
- CSV on UTF-8, eraldaja koma ja kümnendmärk punkt. Tühjale väärtusele vastab JSON-is `null`. `curve` ja `image` lähtuvad `data/` kaustast, näiteks nimereegli `curves/<team>/<station_id>/<cycle>.csv` ja `images/<team>/<station_id>/<cycle>.jpg` järgi. Salvesta algfailid muutmata. Kirja lähevad olemasolevad failid või kinnitatud salvestusviited.
- Kõvera failis säilita vähemalt proovide järjekord, mõõtmise ajabaas (`t_ms` tsükli suhtes), ADC kood ja kalibreeritud `p_kpa` või tühi väli. Seansi metaandmed seovad anduri, kalibratsiooni, rõhu märgi ning kella ja annavad seose doseerimissündmusega. Surveproovide katkemine jääb nähtavaks.
- Tundmatu või kasutuskõlbmatu pilt jätab pindala tühjaks. Üks laiguta pilt üksi ei erista ummistust tühjast süstlast. Otsusta märgend sõltumatu seadeoleku, vaatluse või kaalumise abil. Kirjuta üles vastuolu ja välista lahendamata juhtum märgendatud põhiandmestiku loendusest.
- Hoia iga alustatud tsükli jälg alles, ka katkenud tsüklil. Kaitsmise 300 hulka loe tegelikud lõpetatud andmestikutsüklid, mille märgend ja tõend on kinnitatud ning mille nõutud failiviited lahenevad. Võrdlustsükleid arvesta [katseplaani kattuvuse tingimustel](experiment_plan.md#labori-5-andmeseeria). Sama võti loeb andmestikus ühe korra.
- Kinnita olukord enne andmekirje avaldamist, kui sõltumatu tõend on kättesaadav. Hilisem parandus vajab tõendiga paranduskannet ja kokkulepitud andmebaasitoimingut. Võtme korduv saatmine säilitab algse sisu.

**Enne esimest tsüklit kinnitada:** väljade nimed, ühikud ja tühjad väärtused, võti ja andmete ajatsoon, rõhu võrdlusaken, failide säilitus ja ligipääs, paranduste kord ning MQTT ja andmebaasi kinnituse kuju. Kirjuta kinnitajad, kuupäev ja ühise versiooni viide siia. [Integratsioon](integration.md)
