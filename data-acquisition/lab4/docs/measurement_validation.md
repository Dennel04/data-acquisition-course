# Automaatne tilgamõõtmine ja valideerimine

## Pildilt pindalaks ja ruumalaks

Kinnita iga kasutatava seadistuse kaamera kõrgus, vaatenurk, fookus, valgus ja tööpind. Pildista samal tasapinnal mõõteskaala. Märgi kaadri mõõtkava mm/px ja vajadusel moonutuse parandus. Säilita algpilt, kalibratsiooni viide, töötluse seaded/versioon ja automaatselt eraldatud kontuur. Ala `A = A_px × (mm/px)²` annab mm². Mõõdetud kihi kõrgusega `h` annab kaetult ühtlase kihi eeldusel `V = A × h` mahu µL. Plaadilt mõõdetud kolm 0,6 mm tuge on geomeetriline lähtekoht. Valideeritava plaadi tegelik vahe ja ühtlus tuleb mõõta koos klaasi ning toestusega. Kui automaatne töövoog kasutab teist pildistusgeomeetriat, valideeri pindala ja ruumala seos selles geomeetrias. [Lab 3 plaadimõõdud](../../lab3/tilgaplaat/measurements.md) · [CAD-i ja kaamera muudatused](integration.md#cad-i-vahetus-ja-kalibratsioon)

Segmenteeri laik heledast taustast ja kontrolli säritust, teravust, piirkonda, peegeldusi ja oodatavat komponentide arvu. Liiga hele/tume kaader, liitunud laigud või vigane kontuur annavad `not_measured` koos põhjusega. Kasutuskõlblik kinnitatud laiguta kaader annab `no_drop`. Hoia mõõtmise staatus eraldi olukorra märgendist ja ära uuenda vigase või laiguta kaadri järel impulssi. [Väljad ja päritolu](record.md)

## Võrdlus Lab 3 üle vaadatud piltidega

Fikseeri Lab 3 võrdluskomplekt algpiltide, käsitsi üle vaadatud kontuuride, pindalade, skaala ja versiooniga. Käivita uus töötlus ilma käsitsi korrigeerimata. Pane kõrvuti sama pildi vana ning uus pindala (mm²) ja arvuta `100 × (uus − vana) / vana` mittenullise lähtepindala korral. Näita ka absoluutset protsentuaalset erinevust ja nulljuhtumite absoluutset viga mm². Raporteeri piltide arv, keskmine ja suurim absoluutne erinevus ning põhjenda lahknevusi. Praegune [Lab 3 tilgatabel](../../lab3/data/drops.csv) on päisega. Võrdluskomplekti loomine on ootel.

## Sõltumatu kaalumine

Kaalu sama tilgaplaadi koost enne ja pärast valideerimise tilgaseeriat 0,01 g sammuga kaalul. Hoia klaasid ja muud kaalutavad osad mõlemal kaalumisel samad ning väldi kadusid, õhumulle ja erinevat kõvenemisastet. Talleta alg- ja lõppmass g, vahe `Δm` g, tilkade arv `n`, kaalu eraldusvõime ning vaigu tihedus `ρ` g/mL tootja andmelehelt. Kaalu ruumala tilga kohta on `1000 × Δm / (n × ρ)` µL. Võrdle samade tilkade kaameramahtude keskmisega ning arvuta erinevus protsentides kaaluga saadud mahu suhtes.

0,01 g samm peab jääma alla 2 % kogumassist. Seega on vaja `Δm > 0,50 g`. Kui piloodis hinnatud keskmine mass on `m` g tilga kohta, on minimaalne kavandatav arv `floor(0,50 / m) + 1`. Kontrolli piiri tegeliku massivahega ja arvesta kahe kaalumise määramatust eraldi. Kui selleks on vaja mitut plaati, kaalu iga plaadi koost enne/pärast ning koonda massivahed koos vastavate kaameramahtudega. Võrdluspiir lepitakse kokku kasutuse ja mõõtemääramatuse järgi.

## Veajuhtumid

Säilita vähemalt kolm tegelikku eksimuse pilti. Lisa igaühe juurde algfail, kontuur, mõõtarv või puudumise põhjus ning paranduse või tõrke käsitlus. Jälgi eraldi hägust serva, peegeldust, lähestikku laike ja laiguta kaadrit. Näita kaitsmisel üks näide koos sellega, mida programm selle põhjal tegi. Mõlemad võrdlused ja pildinäited ootavad päriskatset.
