# REVIEW pilots R4 → maakdag 9 jul (geschreven 8 jul, avond)

> **Doel van dit document:** morgen hoeft er alleen GEMAAKT te worden.
> Elke scène hieronder heeft (1) een eerlijke stand, (2) wat je NIET mag
> slopen, (3) een genummerde fixlijst in volgorde van impact, concreet
> genoeg om direct uit te voeren. Onderaan: 2 nieuwe sceneplannen voor de
> opgegeven scènes (apart: `PLAN_pilot_magnolia_VIJVERTUIN.md` en
> `PLAN_pilot_roosmarijn_KAMPVUUR.md`).
>
> Beoordeeld op de nieuwste previews: `*_R4_PREVIEW.png` (8 jul) per map in
> `pilots\`. Roosmarijn-zentuin = Beike zelf, NIET aanraken.
> Proces blijft: fix → headless diag → review-site (:8767) → pas finale
> 2560×1440 na Beikes akkoord. AgX Medium High Contrast. Geen commits.

## Scorebord (R4-stand)

| # | Scène | Score | Grootste hefboom |
|---|-------|-------|------------------|
| 1 | dahlia_leeshoek | **7** | bijna klaar: pad + gloed + gras |
| 2 | camelia_wijnterras | **6,5** | snoer AAN + terras aankleden |
| 3 | jasmijn_familietuin | **6,5** | reuzenschep + grounding |
| 4 | magnolia_wintertuin | **6,5** | winterkeuze + gloed sterker |
| 5 | zonnebloem_zomeravond | **6,5** | snoer AAN + zonnebloemen! |
| 6 | zonnebloem_ochtendhoek | **6** | pad + compositie-lucht |
| 7 | lavendel_lavendelveld | **6** | veld uitbreiden + pad |
| 8 | camelia_buitenbad | **5,5** | bad open + gele vlek weg |
| 9 | jasmijn_theehuis | **5,5** | grind echt maken + gloed |
| 10 | lelie_avondkubus | **5,5** | bay verlichten + heg-blokkade |
| 11 | lelie_ochtendnevel | **5,5** | pad gronden + rots verplaatsen |
| 12 | lavendel_pluktuin | **5,5** | LICHT (overcast → gouden) |
| 13 | dahlia_tuinkantoor | **5** | bureau zichtbaar = het verhaal |
| — | magnolia_groene_long | vervallen | → PLAN vijvertuin |
| — | roosmarijn_kruidenterras | vervallen | → PLAN kampvuur |

---

# DEEL 1 — Vijf systemische fixes (eerst bouwen, dan uitrollen)

Dezelfde handvol problemen zit in bijna alle 13. Bouw/patch deze één keer
en draai ze per scène; daarna is het per-scène werk klein.

### S1. Gras-mix (12 van 13 scènes)
Het gras is overal een uniform borstel-tapijt: elke spriet even hoog,
even groen, recht omhoog. Dit is hét CG-signaal in de hele lijn.
**Fix in `scripts/grass_lib.py`** (één patch, overal herdraaien):
- meng 2-3 clump-varianten, random scale 0.6–1.4, tilt tot ~30°, random Z;
- ColorRamp op noise/instance-index: 3 groentinten + 5-8% geel/droog;
- density-noise voor kale plekjes + zachte fade aan de scene-randen;
- alles instanced houden (VRAM); roughness hoog (geen "natte plas").
Let op de R4-les: mask-cell 0.22 en Mist_Rig tijdens raycasts verbergen
(zit in apply_r4.py). Draai daarna elke scène opnieuw door apply_r4.

### S2. Practicals AAN (6 scènes)
Alle lichtsnoeren en lantaarns staan uit (witte plastic bolletjes):
wijnterras, zomeravond, buitenbad (lantaarn), leeshoek (wandlantaarn),
avondkubus (bay), ochtendhoek. **Fix:** één emissie-preset — bollen
emission 2200K sterkte 2-4 (dag: 2, schemer: 4), lantaarns idem + kleine
warme point (radius 0.05) erin. Overkapping-scènes: zwakke warme area
(10-20 W, use_shadow=False) onder elk afdak zodat het interieur nooit
een zwart gat is. Dit is exact het overkappingen-recept (sb.emissie_mat
+ Fill_LED uit scene_b_spa.py — kopieer dat).

### S3. Paden die ergens heengaan (9 scènes)
Regel: een pad BEGINT in de voorgrond-onderhoek en EINDIGT bij de deur
(of bij de zitplek), ligt IN het maaiveld (1-2 cm verzonken, gras-mask
eromheen, geen sprieten erdoor) en heeft een vuil/AO-randje. Nu: tegels
en planken zweven op de grastoppen (ochtendnevel, familietuin,
ochtendhoek, theehuis, wintertuin-dekrand) of lopen het beeld uit
(buitenbad, pluktuin, tuinkantoor).

### S4. Zonrichting in de dawn-scènes (6 scènes)
Tuinkantoor, leeshoek, theehuis, ochtendnevel, ochtendhoek, pluktuin
hebben allemaal dezelfde vlakke roze-paarse waas zonder schaduwrichting.
**Referentie die bewijst dat het kan: jasmijn_familietuin R4** (echte
zon, tak-schaduwen op de wand, blauwe lucht). Per scène: zon elev 8-15°,
3500-4500K, energy 3-5, azimut zó dat één gevel oplicht en één in
schaduw valt + slagschaduw over het gras naar de camera toe. Waar mist
hoort (ochtendnevel, lavendelveld): BEGRENSDE volume-cube, density
0.002-0.005 — nooit World Volume Scatter.

### S5. Horizon-gaten dichtzetten (5 scènes)
Boven de heg is vaak een lege lucht/veld-strook (wijnterras rechts,
familietuin rechts, theehuis, kubus, ochtendnevel-banden). **Fix:** 1-2
extra ringen bomen (GLTF-berk/dennen, linked copies) achter de heg met
hoogtevariatie, of de camera 2-3° lager richten. Ochtendnevel heeft
daarnaast een echte banden-fout (zie scène 11).

---

# DEEL 2 — Per scène (volgorde = aanbevolen werkvolgorde morgen)

## 1. dahlia_leeshoek (scandi) — 7/10, dichtst bij klaar
`pilots\Dahlia-250x250-300-zijwand\style-scandi` · lavendel-border ✓,
leesstoel + boek + kop ✓, houtstapel ✓, lantaarn ✓, dawn met bergen ✓.
**Behouden:** de complete voorgrond-border, stoelopstelling, kleurpalet.
**Fixes:**
1. Lantaarn aan de overkapping ECHT laten branden (S2) + zwakke warme
   area onder het afdak — de achterwand is nu een leeg grijs vlak.
2. Tegelpad linksvoor doortrekken naar de linker-onderhoek (S3, nu
   eindigt het in het niets) en de tegels 1 cm laten zakken.
3. Zon laag rechtsachter (S4) zodat de vlonder-voorkant een warme rand
   krijgt en de stoel een slagschaduw werpt — nu is alles even licht.
4. Gras-mix (S1); de kale aarde tussen de lavendel mag blijven (leest
   als border) maar geef 'm een donkerder humus-kleur (nu grijzig).
5. Mini: plaid over de stoelleuning (blanket uit props, override-les),
   boek open laten liggen. Klaar voor final.

## 2. camelia_wijnterras (mediterraan) — 6,5/10
`pilots\Camelia-250x300-300-zijwand\style-mediterraan` · warm vurenhout
✓, bistroset + wijn ✓, terracotta terras ✓, heg dicht ✓.
**Behouden:** wandtextuur (vuren-rene), terrasvorm, bistroset-verhaal.
**Fixes:**
1. Lichtsnoer AAN (S2). Het snoer eindigt rechts in een kale dode boom —
   anker het aan een paal of haal de laatste meter weg.
2. Bistroset staat half op het gras: alle vier poten ÓP de tegels
   (verschuif set ~0.4 m naar links-voor), grounding-check.
3. Het terras is 60% leeg: olijfboompje in kuip + 2-3 lavendel/rozemarijn
   in terracotta bij de open zijde, kruik of vaas bij de deur. Onder het
   afdak: niets → wandrek of tweede stoel + zwakke warme fill (S2).
4. Namiddag-goud versterken: zon naar elev ~15°, 3800K, lange schaduwen
   over het terras (S4-waarden; er ís al richting, hij mag dieper).
5. Dode boom rechtsachter vervangen door een volle den/olijf-silhouet
   (S5) — hij leest nu als vergeten asset.
6. Gras-mix (S1) + droger/warmer gras rond het terras (mediterraan).

## 3. jasmijn_familietuin (klassiek) — 6,5/10, beste licht van de lijn
`pilots\Jasmijn-300x250-300-zijwand\style-klassiek-familie` · echte zon
+ tak-schaduwen ✓, picknicktafel ✓, zandbak ✓, vogelbad ✓, borders ✓.
**Behouden:** HET LICHT (referentie voor S4), bloemen-borders, opstelling.
**Fixes:**
1. De tuinschep in de zandbak is ~1 m lang (bekend restpunt) — schaal
   naar 0.35-0.4 m en leg hem LIGGEND half in het zand; nu prikt er een
   reuzenspade boven de rand uit.
2. Zandbak-grounding: randen zweven op grastoppen → 2 cm laten zakken,
   gras-mask eromheen, wat zand-morseling op het gras.
3. Tegel-eiland onder de picknicktafel: verbind het met een smal
   tegelpad naar de deur-stoep (S3) zodat het niet los in het gazon ligt;
   tegels 1 cm verzinken.
4. Vogelbad: staat droog — waterschijfje (glas-shader, roughness 0.05)
   erin + iets verzinken.
5. Overkapping-interieur: leeg blank vlak → speelgoedkist + bal of
   loopfiets tegen de achterwand (familietuin-verhaal), zwakke fill.
6. Gras-mix (S1) + horizonstrook rechts dichtzetten (S5).

## 4. magnolia_wintertuin (scandi) — 6,5/10
`pilots\Magnolia-300x200\style-scandi` · tak-schaduwen op de wand ✓,
blauwe lucht ✓, dek + bistroset + houtstapel + lantaarn ✓, witte
spikkels in het gras (rijp/bloei) ✓ deurgloed aanwezig ✓.
**Behouden:** compositie, dek-dressing, wand-schaduwspel.
**Beslissing eerst:** "winter" of "vroege lente"? De bomen/heg zijn vol
groen — als dit wintertuin blijft heten:
1. Ontkleur het gazon licht (droge winterkleur via ColorRamp-shift), maak
   de witte spikkels rijp-achtiger (kleiner, dichter bij de grond) en
   zet een dunne koele haze-cube (S4-mist) voor winterochtend-adem.
2. Deurgloed 2× sterker (warm toevluchtsoord = het verkoopverhaal) +
   lantaarn op het dek AAN (S2).
3. De vetplant (aloë) op het dek kan niet buiten in de winter → vervang
   door skimmia/heide in dezelfde pot.
4. Dek-rand zweeft boven het gras → 2 cm zakken + gras tegen de rand.
5. Bistrotafel leeg → twee mokken + plaid over een stoel (warme-choco).
6. Gras-mix (S1). Kies je "vroege lente": alleen 2, 4, 5, 6.

## 5. zonnebloem_zomeravond (boerderij) — 6,5/10
`pilots\Zonnebloem-300x300-300-zijwand\style-boerderij` · vuren-rene ✓,
dinerset + wijn ✓, rozen/hortensia's ✓, zachte avondlucht ✓.
**Behouden:** dinerset-verhaal, borders, wandtextuur.
**Fixes:**
1. ZONNEBLOEMEN. De scène heet zonnebloem-boerderij en er staat geen
   enkele zonnebloem — zet een rij van 5-7 (BlenderKit "sunflower",
   hoogte 1.6-2.2 m, linked copies, variatie in rotatie/hoogte) langs de
   rechterheg of achter de borders links. Dit is het concept-signaal.
2. Lichtsnoer AAN (S2) — het hangt er prominent maar dood bij; bij
   zomeravond is dit het sfeer-anker.
3. Overkapping: zwart gat achter de stoelen → warme fill + lantaarn op
   tafel; wijnflessen-schaal checken (ogen ~1.2×, schaal naar 0.30 m).
4. Stapstenen linksvoor gronden en laten beginnen bij de border (S3).
5. Zon dieper goud (elev ~8°, 3200K) voor lange schaduwen (S4).
6. Gras-mix (S1).

## 6. zonnebloem_ochtendhoek (scandi) — 6/10
`pilots\Zonnebloem-300x300-300-zijwand\style-scandi` · loungestoelen +
koffie ✓, lavendel ✓, nette staat.
**Behouden:** stoelen-hoek, lavendel-accenten.
**Fixes:**
1. De grijze stoep voor de deur ligt los in het gras → tegelpad van de
   stoep naar de rechter-onderhoek (S3), verzonken, langs de stoelen —
   geeft meteen de ontbrekende leading line.
2. Koffie-verhaal versterken: thermoskan + tweede kop op het tafeltje,
   plaid over een stoelleuning.
3. Zon laag rechts (S4): strijklicht over het gras naar de stoelen, de
   linkerwand in schaduw — nu is alles even roze-vlak.
4. Overkapping-interieur donker → zwakke warme fill + het raampje-luik
   checken (donkere rechthoek rechts leest als gat).
5. Cabin staat dood-centraal met een lege grasvoorgrond van 50% —
   camera 0.5 m naar links + 2° omlaag zodat het nieuwe pad de
   voorgrond vult (geen herbouw, alleen camera).
6. Gras-mix (S1).

## 7. lavendel_lavendelveld (mediterraan) — 6/10
`pilots\Lavendel-400x300-400-zijwand\style-mediterraan` · warme mist
rechts ✓ (dichtst bij de doel-look!), douglas warm ✓, lavendelrijen ✓.
**Behouden:** het mist-licht rechts, de rij-structuur, houtkleur.
**Fixes:**
1. Het "veld" is een hoekje: trek de lavendelrijen door tot in de
   rechter-voorgrond (2 extra rijen, linked copies, richting camera) en
   laat 1 rij links van het pad beginnen — de rijen zijn de leading line.
2. Tussen de rijen: droge aarde/grind-stroken i.p.v. fel gazon
   (mediterraan veld, S1-kleurshift naar droger).
3. Pad naar de deur ontbreekt → smal grindpad tussen twee rijen door
   naar de stoep (S3).
4. De 3 potten+bolboompjes voor de deur blokkeren de entree → 1 pot
   naast de deur, rest naar de overkapping-zijde.
5. Overkapping: bistroset verloren in een leeg vlak → kleedje +
   lavendel-bos op tafel + kruik; zwakke warme fill (S2).
6. Zon-mist iets breder trekken (volume-cube tot over het veld) zodat
   de godray-look ook links leeft (S4).

## 8. camelia_buitenbad (hot-tub premium) — 5,5/10
`pilots\Camelia-250x300-300-zijwand\style-hot-tub-premium` · avond,
deurgloed ✓, hottub + gloed ✓, handdoek ✓, stapstenen ✓.
**Behouden:** avondconcept, tub-positie, deurgloed.
**Fixes:**
1. De gele lichtvlek/flare linksachter in de bomen (HDRI-vlek) —
   HDRI 20-30° draaien of de vlek wegroteren achter de treeline; hij
   leest nu als brand.
2. Het bad is DICHT (deksel) — premium-verhaal = open bad: deksel eraf
   of half opengeklapt, donker watervlak (roughness 0.05) + dunne
   stoompluim (begrensde volume-cube boven het water, density 0.15).
3. De linker beeldhelft is leeg gras → verplaats 1 potplant + een
   lantaarn (AAN, S2) naar linksvoor langs de stapstenen, of camera
   0.5 m naar rechts zodat de tub-zone het frame draagt.
4. Stapstenen: beginnen bij de deur maar sterven rechts — doortrekken
   naar de voorgrond-onderhoek (S3, verzonken).
5. Overkapping-interieur (houtstapel) is pikzwart → zwakke warme fill.
6. Gras-mix (S1); avond-variant iets donkerder en matter.

## 9. jasmijn_theehuis (japandi) — 5,5/10
`pilots\Jasmijn-300x250-300-zijwand\style-japandi` · theeset-lantaarn ✓,
rots ✓, bolstruiken ✓, bank + dienblad onder het afdak ✓.
**Behouden:** zwart+blank palet, rots, bolstruiken, theeset op de bank.
**Fixes:**
1. Het "grind" is een glad egaal betonvlak — dit blijft de kern-kritiek:
   echte grind-look via pebble-textuur mét normal/displacement of een
   dunne kiezel-scatter (instanced, 1-2 cm) + donkerder voegen langs de
   randen. Zonder dit blijft het een betonplaat.
2. De bronzen theepot-lantaarn staat los midden op het terras → naast
   de bank onder het afdak (waar het ritueel is) en AAN (S2).
3. Warme gloed onder het afdak (S2): de bank + theeset zijn nu bijna
   onleesbaar donker; een zwakke 2700K-fill maakt het verhaal zichtbaar.
4. Zon laag links-achter (S4) met lange schaduwen over het grind; de
   roze waas mag blijven maar moet richting krijgen.
5. Stapstenen-lijn (3-4 platte stenen) van de voorgrond naar het
   terras (S3) — zen-signaal én leading line in één.
6. Gras-mix (S1) + mos-rand rond het grindveld.

## 10. lelie_avondkubus (modern) — 5,5/10
`pilots\Lelie-400x250-300-zijwand\style-modern` · deurgloed ✓ (eindelijk),
bollards + pools of light ✓, strakke hagen ✓.
**Behouden:** deurgloed, bollard-pad-idee, zwart palet.
**Fixes:**
1. De heg-blok VOOR de deur blokkeert nog steeds de route: het
   bollard-pad buigt erachter langs. Schuif dat heg-blok 1.5 m naar
   links of maak hem half zo breed — de zichtlijn pad→deur moet open.
2. De rechter bay (overkapping) is een pikzwart gat: 2 warme spots of
   een area onder het afdak + iets om te zien (loungestoel, plant,
   wandlamp). "Verlichte kubus" = beide volumes lichten.
3. Gele HDRI-vlek linksboven in de bomen (bekend restpunt) — HDRI
   draaien of de vlek maskeren met een extra boom.
4. Stapstenen gronden (zweven licht) en de laatste 2 richting camera
   doortrekken (S3).
5. Lucht is grijzig-groen met ruis → schonere blue-hour HDRI of
   world-strength iets omhoog + denoise-check.
6. Gras-mix (S1), avond-variant.

## 11. lelie_ochtendnevel (forest) — 5,5/10
`pilots\Lelie-400x250-300-zijwand\style-forest-wilderness` · klaprozen ✓,
rots-asset ✓, plankenpad-idee ✓, boslagen met mist ✓.
**Behouden:** klaprozen, bos-mist links, plankenpad-concept.
**Fixes:**
1. De achtergrond RECHTS heeft harde horizontale banden (groen veld /
   paarse berg / witte lucht) — dat is een backdrop-fout: zet 1-2 extra
   boomringen rechts zodat de banden geoccludeerd worden (S5), of trek
   de mist-cube door over die zone.
2. Het plankenpad zweeft op de grastoppen en wordt rechtsonder een
   kris-kras stapel → elke plank 1-2 cm het maaiveld in, gras-mask
   eronder, en de onderste 3 planken netjes richten (S3).
3. De rots staat dood-centraal vóór de deur en blokkeert de looproute →
   1.5 m naar links, half in de klaprozen; het pad krijgt vrij zicht op
   de deur.
4. Zonstralen: de nevel is overal even dik — zon laag rechtsachter
   (S4) + mist-cube dichter bij de bomen zodat er echte godrays door de
   stammen vallen (de Lelie-referentielook uit het lichtplan).
5. Deurglas is melkachtig-dicht → glas-shader check (de avondkubus-les:
   Transmission 1, of frosted mét gloed erachter).
6. Overkapping donker leeg → zwakke warme fill + houtstapel of bijl-blok
   (wilderness-verhaal).

## 12. lavendel_pluktuin (boerderij) — 5,5/10 (met licht-fix → 7)
`pilots\Lavendel-400x300-400-zijwand\style-boerderij` · Beikes eigen
boog-edit ✓, borders + rozenboog ✓, tafel onder de kap ✓.
**Behouden:** ALLES qua opstelling (door Beike goedgekeurde ronde) —
alleen licht en grond aanpakken.
**Fixes:**
1. HET LICHT: volledig grijs overcast, de bloemen knallen niet. Warme
   zon elev 10-12° van links (3800K, energy 4) + heldere ochtend-HDRI
   i.p.v. grijze lucht — dit ene punt tilt de scène 1,5 punt.
2. De grijze kale-aarde-vlekken tussen de borders lezen als beton →
   donkere humus-kleur + gras-mask strakker (S1-patch).
3. Pad loopt naar rechtsachter weg → stapsteen-aftakking naar de
   voorgrond-onderhoek (S3).
4. Warme fill onder de kap; de plukmand op de tafel mag een tint
   kleurrijker (bloemen erin = pluktuin-verhaal).
5. Gras-mix (S1).

## 13. dahlia_tuinkantoor (modern-urban) — 5/10
`pilots\Dahlia-250x250-300-zijwand\style-modern-urban-cottage` ·
raamgloed ✓, bakken + bolboompjes ✓, dek ✓, treeline dicht ✓.
**Behouden:** cabin-positie, dek, raamgloed.
**Fixes (het verhaal ontbreekt nog steeds):**
1. HET BUREAU MOET ZICHTBAAR. Restpunt was "bureau valt achter topiary;
   camera bewust niet aangeraakt" — dat compromis verkoopt het concept
   niet. Kies: camera 10-15° naar rechts (dek als voorgrond, kijklijn
   ONDER de overkapping in) óf schuif de bureau-opstelling 0.8 m naar
   de open zijde. Zichtbaar moeten zijn: bureau + stoel + laptop +
   vloerkleed + staande lamp (AAN, warme pool).
2. Het lage ronde tafel-object rechts op het dek leest als zwevend
   niet-ding → vervang door loungestoel + bijzettafel (pauze-plek) of
   weg ermee.
3. De twee identieke bakken+bollen zijn symmetrisch CG → één vervangen
   door siergras-bak of de maten 20% variëren.
4. Zon laag (S4): warme ochtendzon van rechts over het dek; de dawn-waas
   mag blijven maar moet een richting krijgen.
5. Pad: dek → voorgrond ontbreekt (S3), nu zweeft het dek in het gazon.
6. Gras-mix (S1) + horizon rechts iets dichter (S5).

---

# DEEL 3 — Vervangers voor de opgegeven scènes

Twee volwaardige nieuwe plannen staan in aparte bestanden (zelfde map):

1. **`PLAN_pilot_magnolia_VIJVERTUIN.md`** — vervangt magnolia_groene_long.
   Magnolia 300×200 als vijverhuisje aan een natuurlijke tuinvijver met
   vlonder — het waterelement dat bij het zwembad zo goed werkte, in
   eco-vorm (groendak + regenton blijven het product-verhaal dragen).
2. **`PLAN_pilot_roosmarijn_KAMPVUUR.md`** — vervangt
   roosmarijn_kruidenterras. Roosmarijn 200×300+400-kap als basecamp
   rond een vuurkuil met boomstambanken bij schemering — de overkapping
   wordt houtopslag + zitplek, de tuin vertelt het verhaal.

# DEEL 4 — Aanbevolen dagvolgorde (9 jul)

1. **S1 gras-patch** in grass_lib + testrender op leeshoek (30 min werk,
   grootste winst van de dag) → daarna batch-herdraai via apply_r4-loop.
2. **S2 practicals-preset** (kopieer emissie_mat + Fill-recept uit
   `overkappingen-website\scene_b_spa.py`) → wijnterras, zomeravond,
   buitenbad, leeshoek, kubus, ochtendhoek.
3. Scènes 1-6 uit het scorebord afwerken (bijna-klaar-groep) → diags →
   review-site.
4. Scènes 7-13 (meer werk per stuk; tuinkantoor en theehuis als laatste
   want die vragen camera/terrein-beslissingen).
5. Nieuwe scènes bouwen volgens de 2 plannen (anker eerst! kaal + vloer
   + licht → akkoord → dan pas dressing, conform WERKWIJZE_REVIEWLOOP).
6. Alles op :8767 → Telegram naar Beike → feedbackloop → finals pas na
   expliciet akkoord.
