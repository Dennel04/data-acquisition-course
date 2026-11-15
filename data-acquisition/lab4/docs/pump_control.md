# Labor 4 pumbajuhtimine ja süstlaharu

`pump → Y1 → iminapp / 3/2 klapp → süstal`. Iminapp jääb otse pumba Y-harusse. Voolu all ühendab klapp pumba süstlaga. Vooluta peab klapp pumba süstlast lahutama ning süstla atmosfääri avama. Labor 4 asendab süstlaklapi relee MOSFET-iga. Pumba digitaalväljund, klapi MOSFET ja UV-väljund on eraldi ülesannetega. [Lab 3 pneumaatika](../../lab3/docs/pump_control.md#süstlaharu-ohutu-olek-ja-y-pneumaatika) · [MOSFET](mosfet.md)

Lab 1 füüsilise katse −60/−40 kPa piirid kirjeldavad vaakumhaaret. Lab 4 doseerimisrõhk, võimaliku nõelventiili mõju, pumba piirid mõlema haru koormusel ja minimaalne väljasolekuaeg tuleb päris ahelal kinnitada. Säilita pumba katsetes anduri asukoht, rõhu märk, lahtise napa tingimus ning algsed ja kalibreeritud mõõtmised. Lab 2 küllastunud ADC ala jäta kalibratsioonist välja ja kontrolli G5 siirdeid enne sellele kanalile toetumist. [Lab 1 pumbaproov](../../lab1/docs/pump_control.md) · [Lab 2 võrdlus](../../lab2/docs/pump_control.md)

## Katkestus ja ohutu seis

| Juhtum | Nõutud käitumine ja tõend |
| --- | --- |
| Käivitus, taaskäivitus või klapi toite kadu | Klapp vooluta, süstlaharu õhutatud, UV väljas. Mõõda süstlaharu rõhu käik ja mähise pinge. |
| Komparaatori IRQ, ummistus, tühi süstal või lubatud aja ületus | Peata doseerimine ja lukusta alarm kuni kohaliku kontrolli ning kinnitamiseni. Mõõda IRQ-st mähise väljalülitumiseni ja rõhu vabanemiseni. Kirjuta tsüklivõti, sündmus, põhjus ja rõhukõver. |
| Käsuühenduse kadu või hädastopp | Kinnita kohapeal pumba, klapi, UV ja roboti käitumine ning uue käivituse tingimused. Puudulik tsükkel jääb logisse. |
| Ainult mõõteandmete tunnel maas | Kohalik puhver hoiab lõpetatud kirjed. Uue tsükli lubamine sõltub kohalikust ohutusseisust, töövoost ja vabast puhvrist. |

Märgi stendiprotokolli kuupäev, osalejad, anduri ja vooliku paigutus, kontrollitud pumba seaded, väljalülituse jäljed ning muudatuse põhjus. Alarmipiirid ning `raw` ja `opamp` sobivus vajavad mõõtmist. [Katseplaan](experiment_plan.md) · [Püsivara ja jaama tööjaotus](../src/README.md)
