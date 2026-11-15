# Regressioon ja tagasiside

## Mudeli sobitamine ja kontroll

Mudelda mõõdetud tilga pindala mm² impulsi `u` (ms), rõhu `p` (kPa) ja otsiku tüübi või läbimõõdu järgi. Kasuta [Lab 3 tilgatabelit](../../lab3/data/drops.csv), kui võrdlusandmed on kontrollitud, ning Lab 4 juhuslikustatud seeria sobiva seadistusega päris `normal`-tsükleid. Ummistus, tühi süstal ja mõõtmisvead jäävad Labori 5 andmestikku. Normaalse doseerimise regressioonis dokumenteeri nende välistus.

1. Sobita vähimruutudega lineaarne lähtekuju `A = a·u + b` otsiku ja rõhutaseme kaupa või kasuta mitme tunnusega lineaarset mudelit. Teise kujuna lisa näiteks `u²`.
2. Jaga andmed enne sobitamist seansside või süstlaplokkide järgi õppe- ja kontrollosaks. Kasuta sama jaotust ja versioonipiire kõigil võrdlusmudelitel. Väldi ühe süstla tihedalt seotud kaalude ja tsüklite jagamist üle piiri. Mudeli ja tunnuste valikuks võrdle valideerimisviga õppeosa sees. Lõplikule kontrollosale rakenda valitud variant pärast valikut ning näita ka eelnevalt fikseeritud võrdlusvariantide kontrollvead.
3. Proovi samu mudeleid süstla täidetusega ja ilma. Selgita, kuidas fikseeritud koostisega massist saadakse täidetus. Kasuta prognoosis vaid selleks hetkeks olemas olnud kaalumist või põhjendatud hinnangut. Säilita iga 25 tsükli järel saadud tegelik kaal eraldi. Kirjuta üles, kuidas puuduvad kaalud, taara ja süstlavahetus analüüsis käsitleti.
4. Lisa iga kuju kordajad, kasutatud seansid, andmejaotus, veamõõdik protsentides, valiku põhjus ja kasutusvahemik. Positiivse mõõdetud pindala korral sobib näiteks keskmine absoluutne protsentuaalne viga. Märgi võrdluse nimetaja ja hinnatud juhtude arv.
5. Pööra valitud mudel sisendiks `A_siht`, väljundiks algimpulss. Mittelineaarse kuju puhul luba üksnes valideeritud vahemiku üheselt määratud lahend. Lahendita juhtum vajab ohutut katkestust või eelnevalt kinnitatud retsepti.

## Tagasiside ja impulsi piirid

Õppejõu P-parandus kasutab eelmise tsükli mõõtmist. `e = A_siht − A_mõõdetud`, `u_järgmine = clip(u_praegune + k·e, u_min, u_max)`. Kui pindala ühik on mm² ja impulss ms, siis `k` ühik on ms/mm². Proovi vähemalt mitut `k` väärtust ja dokumenteeri reaktsiooniaeg, ülereguleerimine ning kõikumine. Piirid määratakse mõõdetud klapi ja doseerimise vahemiku ning ohutuse järgi. Tarkvara tuvastab piiri saabumise ja logib selle. Klapi taimer ja Lab 3 katkestus ning lukustuv alarm piiravad teostust ka jaama vea korral.

Vigane või laiguta mõõtmine jätab paranduse arvutamata. Ummistus, tühi süstal või muu käitustõrge peatab doseerimise ning käivitab [ohutu seisu](pump_control.md#katkestus-ja-ohutu-seis). Tõrke järel jätkab ainult kohapeal kinnitatud töövoog.

## Kolme juhtimisviisi võrdlus

| Viis | 100 tilga tingimus |
| --- | --- |
| Ainult retsept | Lab 3 mõõdetud retsepti fikseeritud impulss. |
| Ainult tagasiside | Algimpulss samast retseptist ja edaspidi P-parandus. |
| Mudel ja tagasiside | Algimpulss mudelist ja edaspidi P-parandus. |

Tee kolm 100 tilga plokki järjest sama süstlaga. Fikseeri plokkide järjekord, kaalud, rõhk, otsik, temperatuur, siht ja tööriistaversioon. Arvesta, et sama süstla täidetus muutub järjest. Joonista igal viisil pindala tilga järjekorranumbri järgi samas skaalas koos siht- ja tolerantsiribaga. Esita puuduva mõõtmise arv, sihivahe ja kõikumine protsentides, näiteks `100 × standardhälve / keskmine`, koos valimi ja nimetajaga.

Tee eraldi süstlavahetuse võrdlus ainult tagasisidega ning mudeli ja tagasisidega. Lepi enne katset kokku sihiriba ja sinna jõudmise kriteerium (vajadusel järjestikuste tilkade arv). Võrdle samadel tingimustel tsüklite arvu sihini. Kui sihti ei saavutata, märgi katse pikkus ja põhjus. Kordajad, `k`, impulsi piirid, tolerants ja tulemused on ootel. [Jupyteri analüüsiplaan](../notebooks/README.md)
