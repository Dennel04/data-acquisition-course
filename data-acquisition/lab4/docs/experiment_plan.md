# Füüsiline katse ja andmekogumine

## Eeltingimused ja piloot

1. Kinnita [kirje kuju](record.md) enne esimest päristsüklit. Tuvasta kohapeal olemasolevad osad ja pane puudujääk kirja [BOM-is](bom.md).
2. Kontrolli Lab 2 anduri pingeulatust ja kalibratsiooni. Lõpeta Lab 3 relee ajastus, lühima tilga katse, kaamera referentspildid, retsept ja ohutu katkestus. Kontrolli ummistatud otsikut Lab 3 tõendi järgi.
3. Kinnita [MOSFET-i ahel ja ohutu õhutus](mosfet.md), [CAD-i paigutus ja kalibratsioon](integration.md#cad-i-vahetus-ja-kalibratsioon) ning kohalik operaatorilukk. Määra pärismõõtmiste põhjal rõhu- ja impulsi piirid. Kontrolli viie klaasi asukohta ja hoidikute mõlemasuunalist töövoogu.
4. Tee kohapeal piloot ja [kaks mõõtmise valideerimist](measurement_validation.md). Uus jada läbib esimese jooksu 20 % kiirusel. Kogu piloodiga tsükli ajad, mittetöötavad juhtumid ja kaalumise lähteandmed.

## Automaatne tsükkel

| Samm | Jaama ja tööriista tegevus |
| --- | --- |
| 1. Alusta | Kontrolli kohalikku operaatorilukku, hädastopi valmisolekut, alarmi, plaadi vaba pesa, hoidikute seisu ja töövoo versiooni. Leia vaba puhver, salvesta unikaalne võti ja algusaeg. |
| 2. Doseeri | Tõsta logimine valmis, saada piiratud impulsi käsk, kogu rõhu toorproovid ja Atomi sündmused. Tilk läheb plaadile. |
| 3. Pildista ja mõõda | Seo algkaader tsükliga, arvuta pindala ja kvaliteedi staatus. Eraldi katsekorraldus annab olukorra ja selle tõendi. |
| 4. Teisalda klaas | Klaas liigub sisendist väljundisse ilma liimita. Viis klaasi ringlevad. Kui sisend tühjeneb, vahetab töövoog tarkvaras hoidikute rollid. |
| 5. Salvesta | Seo rõhukõver, pilt, märgend ja päritolu. Pane kirje kohalikku püsipuhvrisse ning saada andmebaasi. Järgmise impulsi arvutus kasutab ainult kehtivat mõõtmist ja kontrollitud olekut. |

Ühe rutiinse tsükli jooksul ei tee inimene doseerimise, pildi ega mõõtmise samme. Kohalik inimene viibib hädastopi juures kogu jooksu ajal. Plaadi vahetus, otsiku seadmine ja kaalumised toimuvad kavandatud pausidel. Mõõda iga sammu kestus sekundites ja kogu tsükli aeg sama kella järgi. Raporteeri pikim samm ja käsitsi tehtud pausid eraldi.

## Labori 5 andmeseeria

- Kogu vähemalt **300 lõpetatud, tõenditega päristsüklit**. Kavanda igast olukorrast mitmeid kordusi. `normal` on kinnitatud tavadoos, `blocked` kontrollitud ummistunud otsikuga katse ning `empty` kinnitatud tühja süstlaga katse. Ummistuskatse ajal on rõhu all olev süstal tööriistas. Veakatse lõpu tingimus võib olla kavandatud ohutu väljalülitus, mille järel säilivad rõhukõver, pilt ja sõltumatu märgendi tõend. Plaaniväline katkestus jääb eraldi. Kinnita enne alustamist minimaalne korduste arv olukorra kohta, jaota katsed seanssidele ning salvesta tegelik jaotus.
- Koosta enne katset ohutute impulsi, rõhu ja otsikutüüpide kombinatsioonid ning juhuslikusta nende järjekord fikseeritud seemnega. Kui seadevahetus nõuab ohutut peatust, jaga katse ette märgitud plokkideks, juhuslikusta lubatud plokkide järjekord ja seaded plokkides ning märgi piirangud ja tegelik järjekord. Nii saab Labor 5 eristada seadete mõju tühjenemisest ja ajast sõltuvatest muutustest.
- Kaalu süstalt enne seeriat, **iga 25 tsükli järel** ja vahetuse ajal. Säilita kaalumise aeg, `run_id`, `run_cycle`, süstla ID, koostis, taara või võrdlusmass ja tegelik mass g. Katkenud katse säilitab sündmuse ja tsüklivõtme. Märgi ka plaaniväline kaalumine ja põhjus.
- Õppejõu ülesanne nõuab [kolme 100 tilga võrdlusplokki](model_and_feedback.md#kolme-juhtimisviisi-võrdlus) ja vähemalt 300 tsükliga andmestikku. Samu tsükleid saab mõlemas arvestada, kui katse täidab mõlema osa tingimused. Juhtimisviiside võrdluses peab olema 100 tilka iga viisi kohta samast süstlast järjest ning süstlavahetuse järel tuleb mõõta sihini jõudmist. Kogu andmestik peab endiselt katma seadete juhuslikustatud järjekorra, kõigi kolme olukorra kordused, tõendatud märgendid, kaalumise iga 25 tsükli järel, rõhukõverad, pildid ja andmebaasikirjed. Täitmata tingimuste jaoks kogu lisatsükleid. Enne kattuvusega arvestamist küsi õppejõult, kas kavandatud katsekorraldus ja arvestus sobivad.
- Märgi `series` abil iga tsükli põhiseeria. Kui katseplaan lubab kattuvust, lisa aruandesse andmestikku arvatud võrdlustsüklite võtmed. Andmestiku koguarvus loe iga võti üks kord.
- Iga detaili või olulise seadistuse vahetus lõpetab vana konfiguratsiooni seeria. Märgi vana viimane ja uue esimene kasutatav tsükkel. Erista vahepealsed kontrollid ja katkestused. [Vahetuse üleandmine](integration.md#cad-i-vahetus-ja-kalibratsioon)

## Aruandeks

Raporteeri tsüklite koguarv ja arv olukordade ning seeriate kaupa, seadete jaotus ning järjekord, kaalud, mõõtmisvigade ja katkestuste arv ning märgendite päritolu. Võrdle jaama CSV võtmeid andmebaasi võtmetega. Esita saatmise, korduste, vastuolude, andmebaasi unikaalsete kirjete ning puuduolevate kirjete arv. Lisa lõik andmestiku piirangutest, näiteks vaigu, otsikute ja tööriista versioonide ulatusest ning sellest, millised juhud jäid mõõtmata. [CSV](../data/cycles.csv) · [Rõhukõverad](../data/curves/) · [Kaadrid](../data/images/) · [Kirje](record.md)
