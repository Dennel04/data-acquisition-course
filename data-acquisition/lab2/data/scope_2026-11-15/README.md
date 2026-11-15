# Ostsilloskoobi fotod 15.11.2026 (GW Instek GDS-1072A-U)

CH1 (kollane) = G5 sõlm (astme väljund pärast 3,3 kΩ / 0,1 µF), CH2 (tsüaan) = MPX5700AP pin 1 (anduri väljund),
maa = ühine GND. Mõlemad kanalid **1 V/div DC**, ajaskaala **1 s/div ROLL**, mõlema kanali 0 V keskteljel (`1▸` marker).
Rõhk tekitati kompressoriga. Pildid on telefonifotod ekraanist, mitte skoobi salvestatud failid.
Mõõtmise ajal oli Atomil DA2_MEASURE_V1 püsivara (taastatud samal hommikul).

| Fail | Mida näha on (kirjeldus pildi järgi, tingimus kirja panemata) |
|---|---|
| [`photo1_media.jpg`](photo1_media.jpg) | Hoitud ülerõhk: G5 tõuseb 2 s jooksul ~2,15 → ~2,40 V, andur ~1,06 → ~1,13 V |
| [`photo2_media_1.jpg`](photo2_media_1.jpg) | Langus: G5 ~0,86 → ~0,10 V, andur ~0,51 → ~0,20 V |
| [`photo3_media_2.jpg`](photo3_media_2.jpg) | Vabastus ja seis: G5 ~0,71–0,77 V, andur ~0,40–0,47 V, mõlemad aeglaselt langemas |

Tasemed on loetud piksli värvi järgi skriptiga [`scope_photo_fit.py`](scope_photo_fit.py) (iga jälg kümneks
ajalõiguks, lõigu mediaan). Fotolt lugemise täpsus on umbes ±0,05 V. Skoobi numbrilisi mõõtmisi (Mean/Max)
ega CSV-faili ei salvestatud.

## Tulemus

29 ajalõigu sobitus kolmelt fotolt:

**`G5 = 2,43 × andur − 0,37 V`**, `r = 0,998`, jääkhälve 0,06 V.

Kalle ei sõltu sellest, kus kanalite 0 V marker täpselt on, ainult mõlema kanali 1 V/div skaalast.

| | Väärtus |
|---|---|
| Disaini võimendus (`Rref` = 6,8 kΩ + 47 kΩ) | `1 + 10/53,8 = 1,186` |
| 14.11 Atomi kordustesti „tuletatud võimendus“ | `1,168` (eeldas anduri vahemikku 0,32–2,40 V, andurit ei mõõdetud samal ajal) |
| **Skoobi fotodelt (andur ja G5 samal ajal)** | **`2,43`** |
| Võimendus, kui `Rref` oleks ainult 6,8 kΩ | `1 + 10/6,8 = 2,471` |
| Sobitusest tulenev `Vref` | `0,37 / 1,43 ≈ 0,26 V` (B100K + nõrgendi lubab 0…~0,88 V) |

Andur oli plaadil puhkeolekus ~0,40–0,51 V. 14.11 eraldi mõõdetuna oli atmosfääril 0,831 V.

## Tõlgendus (kinnitamata)

1. **Võimendus on tõenäoliselt ~2,4, mitte ~1,19.** Kalle 2,43 on väga lähedal väärtusele 2,47, mis tekib, kui
   `Rref` 47 kΩ osa on vahelt ära või lühistatud. Kõik kolm fotot sobivad selle ühe sirgega.
   Atomi 14.11 test seda näha ei saanud, sest see mõõtis ainult G5 ja eeldas anduri vahemikku.
   Selgitab ka foto 1 aeglast G5 tõusu: andur tõuseb samal ajal ~0,07 V ja ×2,4 annab G5-l ~0,2 V.
2. **Andur annab plaadil ~60 % oodatust.** 0,831 × 3,3/5 = 0,55 V ja 0,32 × 3,3/5 = 0,21 V on lähedal
   mõõdetud 0,40–0,51 V ja 0,20 V väärtustele. Võimalik põhjus: anduri toide on 3,3 V või muul moel alla 5 V.
   See on oletus.
3. **Ohutus:** kui mõlemad punktid kehtivad, võib tugev puhumine viia G5 üle 3,0 V
   (nt andur 1,58 V × 2,43 − 0,37 ≈ 3,5 V). Kuni kontrollini ära puhu täisjõuga, kui G5 on ühendatud.

## Kontroll (multimeeter, paar minutit)

- Toide väljas: takistus LM358N pin 2 ja pin 7 vahel. Disain ~53,8 kΩ, ~6,8 kΩ tähendab, et 47 kΩ on möödas.
- Toide sees: pinge MPX5700AP pin 3 (Vs) ja pin 2 (GND) vahel. Peab olema ~5,0 V.

- 15.11.26 tulemus (multimeeter, Raimo): pin 2–pin 7 takistus **~54 kΩ**, anduri toide **5 V**. Mõlemad vastavad
  disainile. Seega tõlgendus 1 (47 kΩ möödas) ja 2 (anduri toide alla 5 V) **ei kehti** ning ka ohutushoiatus
  nende põhjal langeb ära. Fotode kalle 2,43 tuleb siis tõenäoliselt CH2 näidust: andur loeti ~1,6–2× liiga madalaks
  ja/või CH2 0 V asukoht ei olnud keskteljel. Põhjust ei leitud. CH1 (G5) puhkenäit ~0,86 V langeb kokku Atomi 0,858 V-ga,
  seega G5 näit on usaldusväärsem. Võimendust nendelt fotodelt ei järeldata.
- 15.11.26 multimeeter atmosfääril: anduri pin 1 0,837 V (fotolt CH2 ~0,45 V), G5 0,865 V (fotolt CH1 ~0,86 V). Kinnitab, et fotodel oli vale CH2 näit.

## Enne seda proovitud

Sama päeva hommikul proovitud FNIRSI 1013D näitas kalibreerimata nihkega väärtusi (nt −16,4 V atmosfääril).
Neid pilte ei kasutata ega lisata.
