# Labor 3 andmed

[Ülesanne](../assignment-EST.md) nõuab kaamerapõhist mõõtmist. [drops.csv](drops.csv), [placement.csv](placement.csv) ja [latency.csv](../docs/latency.csv) on praegu ainult päistega; mõõtmata ridu ei lisata. CSV eraldaja on koma, kümnendmärk punkt. Puuduv tulemus jääb tühjaks koos põhjusega märkuses, mitte nulliks.

## drops.csv

Üks rida ühe päriselt mõõdetud tilga kohta:

| Väljad | Sisu ja ühikud |
|---|---|
| drop_id | Üheselt määratud tilga ID, sama rõhukõveral ja fotol |
| plate_id, grid_row, grid_column | Tilgaplaat ja koht 5 × 5 võrgus; rida = impulsi pikkus, veerg = kordus; seos kahe plaadi vahel dokumenteerida |
| nozzle, pressure_kpa, pulse_ms | Otsiku tunnus, mõõdetud suhteline rõhk kPa, kästud impulss ms |
| area_px, mm_per_pixel | Kontrollitud segmendi pindala pikslites ja seansi mõõtkava mm/pixel |
| area_mm2 | `area_px × mm_per_pixel²`, mm² |
| layer_height_mm | Füüsiliselt mõõdetud vahetükkide tekitatud kihi kõrgus, mm |
| volume_ul | `area_mm2 × layer_height_mm`, µL; 1 mm³ = 1 µL |
| image_file, contour_image_file, scale_image_file | Algfoto, kontrollkontuuriga pilt ja sama seansi mõõtkavapilt |
| curve_file | Selle sama tilga algne rõhukõver |
| measurement_uncertainty_pct | Piiripiksli ja skaala põhjal hinnatud mõõtemääramatus protsentides |
| pause_before_s, note | Paus enne tilka sekundites ja katseseadistuse/täitumise/vea märkus |

## placement.csv

Üks rida prinditud ekraanipoole mudelil tehtud päris klaasikatse kohta. `model_id` seob rea mõõdetud mudeli/CAD-versiooniga, `drop_id` tilga ja tema rõhukõveraga, `pulse_ms` käsuga. `spot_area_mm2` on laigu pindala klaasi all; `offset_x_mm` ja `offset_y_mm` laigu keskme nihe ekraani keskpunktist mm. Telgede suund ning keskpunkti määramine kirjeldada `measurement_method` väljas. `reached_edge` väärtus on pärast vaatlust `yes` või `no`; seni tühi. `mm_per_pixel`, `image_file`, `contour_image_file` ja `scale_image_file` tagavad mõõtmise taastatavuse; `note` säilitab piirangud ja ebaõnnestumised.

## Rõhukõverad ja fotod

Repo soovituslik konventsioon (näited, mitte olemasolevad mõõtefailid):

```text
curve_drop_0001.csv
image_drop_0001.jpg
contour_drop_0001.png
```

Failiväljade teed on `data/` suhtes. Lisa tee alles pärast faili loomist; iga tilga foto ja `curve_file` peavad vastama samale `drop_id`-le. Mitme tilgaga algfoto korral peab võrgu/segmendi seos olema tuvastatav. Ära kirjuta algpilte ega toorproove üle.

Rõhukõvera lõplik CSV-skeem, kalibratsioon ja ajasammu kontroll: **TODO pärast Lab 2 kinnitamist**. Säilita algsed ADC-proovid ja ajatemplid; kalibreerimata kPa ei esitata mõõdetud rõhuna. Töökõrgus, fookus, valgus, kaamera nihe, vahetüki kõrguse mõõtemeetod ja seansi skaala dokumenteeritakse [mõõtelehel](../docs/bench_session.md). Pildista pärast kõvendamist, UV väljas.

Plaadi, vahetükkide ja ekraanipoole mudeli CAD-lähtefailid ning STL-id: **TODO**; neid ega fotode kohatäitefaile selles ettevalmistuses ei looda.
