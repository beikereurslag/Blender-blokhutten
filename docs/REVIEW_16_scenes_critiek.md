# Kritische feedback — 16 cabin-scenes (review 2026-07-01)

*Elke scene beoordeeld op de nieuwste R2-preview, afgerekend tegen de archviz-regels (compositie, licht, materiaal, scatter, grounding, scale, aankleding, anti-uncanny-valley). Gesorteerd van zwakste naar sterkste score.*

## Systemische problemen (over alle scenes)

### 1. "Licht-komt-erdoorheen"-signatuur ontbreekt overal (blocker in bijna elke scene)
Alle 16 scenes falen op Beike's kern-lichtdoel: vlak, richtingloos, schaduwarm licht in plaats van lage warme zon + volumetrische haze + AgX. Camelia Buitenbad/Wijnterras, beide Dahlia's, Jasmijn Theehuis/Familietuin, Lavendel Pluktuin/Lavendelveld, Lelie Ochtendnevel/Avondkubus, beide Magnolia's, Roosmarijn Zentuin/Kruidenterras, beide Zonnebloemen. Zonder richtingslicht leest elk beeld als 3D-viewport i.p.v. foto — dit is de grootste enkele reden dat de hele lijn "CG" oogt.
**Generieke fix (één keer bouwen):** een herbruikbare lighting-rig-functie in cabin_lib: Sun-object op lage hoek (5-15°) met per-scene azimut, warme blackbody (2800-4500K afhankelijk van moment), + World Volume Scatter (density ~0.002-0.005) + gegarandeerde AgX view transform. Één call per scene, per-moment-preset (golden hour / blue hour / overcast / ochtend). Lost meteen ook de ontbrekende slagschaduwen op.

### 2. CG-perfect / plastic gras (blocker-major in nagenoeg alle scenes)
Gras is overal het probleem: uniform egaal groen, gelijke spriethoogte, geen kleurvariatie, geen kale plekken, soms zichtbare tiling/naden of een zwevend grastapijt (Lavendel Pluktuin, Zonnebloem Zomeravond met glimmend "nat" gras). Genoemd in élke scene op één na. Het trekt de blik weg van de hero en is het duidelijkste uncanny-valley-signaal.
**Generieke fix:** één gedeelde GN-gazon-generator: 2-3 grasclumps gemengd, density-noise (kale plekken + platgelopen paden), random scale (0.6-1.4) + random tilt (tot 35°), 5-10% klaver/onkruid/gele sprieten, kleurvariatie via ColorRamp, uitfadende density naar de randen (geen naden), en gegrond op een gesubdivideerde ground-plane. Vervang alle huidige scatters hiermee.

### 3. Cabin plat-frontaal en dood-centraal, geen leading line (blocker in ~14 scenes)
Vrijwel elke scene zet de cabin frontaal in het midden met de gevel evenwijdig aan de camera en geen pad dat naar de deur leidt — leest als technische elevatie/productfoto i.p.v. hero. Waar wél een pad ligt, loopt het vaak wég van de deur (Camelia Buitenbad, Lelie Avondkubus, Magnolia Groene Long, Roosmarijn Kruidenterras).
**Generieke fix:** standaard camera-preset (3/4-hoek 20-35°, ooghoogte 1.6m, ~35mm, cabin op derde-lijn) + een verplichte cl.klinker_strip/pad-helper die van de voorgrond-onderhoek naar de deur loopt als leading line. Eén keer als "hero_camera + entry_path"-template.

### 4. Zwevende objecten / geen contact-AO (major, terugkerend in ~11 scenes)
Meubels, potten, terrasdekken, zandbakken, lantaarns, stapstenen en bloemclusters missen contactschaduw en "plakken" op het gras i.p.v. erin te zakken. Ook harde zwevende deck-/tegelranden (Camelia, Dahlia Leeshoek, Roosmarijn Kruidenterras). Ondermijnt realisme in bijna alle premium-props.
**Generieke fix:** een "ground & seat"-helperpass die alle props drop-to-ground zet (bbox Z-min = terreinhoogte), de scatter tot tegen de basis laat groeien, en contact-AO forceert. Voor terrasdekken/tegels: standaard randbalk/inzinking van 1-2cm + grind/aarde-overgang. Verhoog globaal de AO in render-settings.

### 5. Bleek/plastic-blank of gebroken houttextuur (blocker-major, ~10 scenes)
Cabinhout is óf knalwit-blank vurenhout (Camelia Wijnterras, Roosmarijn Kruidenterras), óf egaal grijs-plastic zonder nerf (Camelia Buitenbad, Lelie Ochtendnevel/Avondkubus, Magnolia's), óf gebroken/90°-box-geprojecteerd en vlekkerig (Dahlia Tuinkantoor zijwand, mogelijk Zonnebloem Ochtendhoek panelen). Nooit warm, geleefd hout.
**Generieke fix:** verplichte cl.uv_board_textures() (UV+FLAT, nerf mét de plank) op elke wand, plus een gedeeld warm-hout PBR-preset met per-plank kleurvariatie, roughness-breakup en dirt/AO in de naden + subtiele verwering aan de onderrand. Draai over álle cabins.

### 6. Ijle backdrop / "vliegend eiland" tussen heg en boomkroon (major, ~9 scenes)
Terugkerend: één dunne rij naaldbomen met veel lucht ertussen, of kale stammen zichtbaar tussen heg en kroon, of losse low-poly tree-cutouts (Camelia Buitenbad/Wijnterras, Jasmijn Theehuis, Magnolia's, Roosmarijn Zentuin/Kruidenterras, Zonnebloem Ochtendhoek). De sky wordt niet geoccludeerd.
**Generieke fix:** een standaard "backdrop_ringen"-helper: minimaal 2-3 ringen bomen met hoogte/soort-variatie + een tussenring lagere struiken tussen heg en dennen, en scripts/hide_bare_trees.py verplicht draaien om <50k-vert kale clusters te vervangen. Per klimaat een soort-set (mediterraan = olijf/cipres i.p.v. den).

### 7. Concept/dressing niet verteld — lege overkappingen en "showroom" (blocker-major, ~9 scenes)
De scene-titel wordt aangewezen door rekwisieten maar niet gevoeld: leeg tuinkantoor zonder bureau (Dahlia), theehuis zonder theeset (Jasmijn), familietuin zonder speelgoed/leven (Jasmijn), kruidenterras zonder kruiden/kookprops (Roosmarijn), avondkubus die niet gloeit (Lelie), lege overkappingen als donkere gaten (Camelia, Lavendel, Lavendelveld, Roosmarijn Zentuin).
**Generieke fix:** per-scene een verplichte concept-dressing-checklist (min. 3 verhaal-props uit assets/) + een gedeelde "overkapping mag nooit leeg/zwart zijn"-regel: altijd een zithoek/plant/lantaarn + zwakke warme fill-area-light onder elk afdak. Koppel dit aan het lichtplan (warme binnengloed door glas als default avond/schemer).

## Prioriteitenlijst / quick wins

1. **Bouw en pas de lighting-rig-preset toe** (issue 1) — één functie fixt richtingslicht + haze + AgX + slagschaduwen over alle 16 scenes; grootste sfeer- en realisme-sprong per uur werk. Lost meteen een deel van de grounding op (echte slagschaduwen).
2. **Vervang alle grass-scatters door de gedeelde GN-gazon-generator** (issue 2) — schakelt in één klap het meest opvallende CG-signaal uit; herbruikbaar, geen per-scene handwerk.
3. **Draai cl.uv_board_textures() + warm-hout-preset over alle cabins** (issue 5) — cheap, deterministisch, fixt de "plastic/witte/gebroken wand"-killer die in tien scenes voorkomt.
4. **Zet de hero-camera-preset + entry-path** (issue 3) — één camera-template + pad-helper haalt de "technische elevatie"-look weg; puur compositie, geen render-kosten.
5. **Verplichte overkapping-dressing + warme fill-light** (issue 7) — geen enkele overkapping meer als zwart gat; kleine ingreep, groot verschil in "bewoond/premium" gevoel, en verkoopt eindelijk het concept.

## Scores in één oogopslag

| Scene | Score | Oordeel |
|---|---|---|
| Dahlia — Tuinkantoor | 3.0 | Leeg |
| Magnolia — Wintertuin | 3.5 | Concept-mismatch |
| Camelia — Wijnterras | 4.0 | Bleek |
| Jasmijn — Theehuis | 4.0 | Doods |
| Lelie — Avondkubus | 4.0 | Onverlicht |
| Magnolia — Groene Long | 4.0 | Stro-dak |
| Zonnebloem — Zomeravond | 4.0 | Natte-plas |
| Camelia — Buitenbad | 4.5 | Catalogus-plat |
| Dahlia — Leeshoek | 4.5 | Levenloos |
| Jasmijn — Familietuin | 4.5 | Bloedeloos |
| Roosmarijn — Zentuin | 4.5 | Onrustig |
| Lelie — Ochtendnevel | 5.0 | Roze-waas |
| Lavendel — Pluktuin | 5.0 | Zwevend-tapijt |
| Zonnebloem — Ochtendhoek | 5.0 | Plastic-gras |
| Lavendel — Lavendelveld | 5.5 | Half-verteld |
| Roosmarijn — Kruidenterras | 5.5 | Blank-hout |

---

# Per scene (zwakste eerst)

## Dahlia — Tuinkantoor (modern-urban-cottage, ochtend) — **3/10**
*Een lege overkapping-doos op een kaal moddergazon onder een doods paars schemerlicht verkoopt geen thuiswerk-droom en al helemaal geen ochtend.*

**Concept/licht:** Nee. Het concept 'tuinkantoor / thuiswerken' is nergens te zien: de overkapping rechts is een volledig leeg houten hok — geen bureau, stoel, laptop, lamp of enig kantoor-signaal. Zonder die props leest het beeld als een standaard opbergblokhut met carport, niet als werkplek. Het lichtmoment 'ochtend' klopt evenmin: de lucht is paars/schemerig, de zon is niet als warme lage ochtendzon te herkennen, en de tuinpad-lampen branden (nachtmodus), wat ochtend direct tegenspreekt.

**Sterk:** De deur met dubbele glaspanelen en het RVS-deurbeslag ogen als een echt, geloofwaardig product op menselijke schaal · De twee topiary-bolletjes in plantenbakken zijn echte 3D-assets met volume, geen flat cards · De achtergrond-treeline sluit de lucht netjes af (geen 'zwevend eiland'), met een tweede rij bomen achter de haag voor diepte

**Problemen:**

- **🔴 BLOCKER · Dressing** — De overkapping/carport rechts (midden-rechts van het frame) is een volledig lege houten doos — nul kantoor-props terwijl het concept 'tuinkantoor/thuiswerken' is. Er is geen bureau, bureaustoel, laptop, monitor, boekenkast of lamp te zien.
  → *Fix:* Plaats in de overkapping een echt bureau + bureaustoel (Sketchfab/Polyhaven), een laptop/monitor op het bureau, een vloerkleed, en een staande lamp of wandplanken met boeken. Richt de opstelling naar de open zijde zodat de kijker het 'werken met uitzicht op de tuin' leest.
- **🔴 BLOCKER · Vegetation** — Het hele voorgrond-gazon (onderste helft van het frame) is schaarse losse graspolletjes op kale bruine modder — leest als een dood/verwaarloosd veld, niet als verzorgde kantoortuin. Extra uncanny door de zichtbare kale-grond-plekken tussen de plukken.
  → *Fix:* Verhoog de grass GN-scatter density fors en voeg een tweede, kortere ground-cover laag toe zodat de grond volledig gesloten is; meng 2-3 gras-varianten met kleurvariatie. Verwijder de kale modder-textuur eronder of vervang door een donkere humus die niet doorschijnt. Overweeg een strak modern gazon (lager, egaler) passend bij 'urban cottage'.
- **🟠 MAJOR · Lighting** — Het licht is vlak en somber-paars (schemer/dusk lucht boven de treeline), geen warme lage ochtendzon en geen volumetrische 'licht-komt-erdoorheen' haze. Schaduwen zijn zwak, het beeld mist de bedoelde ochtendsfeer volledig.
  → *Fix:* Zet een lage warme zon (Sun ~5-8° hoogte, kleurtemp ~3500-4000K) die van rechts door de bomen valt, voeg lichte volumetrische mist toe (World volume of een volume-cube) voor godrays, en gebruik AgX view transform. Vervang de paarse dusk-HDRI/lucht door een heldere ochtendlucht.
- **🟠 MAJOR · Materials** — De linker zijwand (links van het frame) is donker, vlekkerig en smeuïg met een glimmende veeg — leest als vies geschilderd metaal, niet als hout. De plankverdeling is nauwelijks zichtbaar en de vlekken ogen als een gebroken/verkeerd geprojecteerde textuur.
  → *Fix:* Controleer de wand-UV met cl.uv_board_textures() (UV+FLAT) zodat de houtnerf met de planken meeloopt; verlaag de specular/roughness zodat de glimmende veeg verdwijnt. Zorg dat dezelfde warme houtkleur als de voorgevel op de zijwand zit i.p.v. de donkere grijstint.
- **🟠 MAJOR · Composition** — De twee zwarte tuinlampen staan midden in het gazon vóór de cabin (een centraal-onder, een links ervan) i.p.v. langs een pad, blokkeren het zicht op de hero en zorgen voor een leeg, doelloos voorgrond zonder leading line naar de deur. De cabin staat bovendien vrij frontaal en gecentreerd.
  → *Fix:* Leg een echt terraspad/klinkerstrip van de voorgrond naar de deur en zet de bollard-lampen daar netjes langs (en zet ze UIT voor ochtend). Draai de camera iets meer 3/4 en plaats de cabin volgens rule-of-thirds zodat het pad als leading line naar de deur voert.
- **🟡 minor · Dressing** — Twee identieke topiary-bolletjes flankeren symmetrisch de deur (links en midden), wat CG-perfect/nep aanvoelt. De picknicktafel rechts op het terras is bovendien een vreemde keuze voor een kantoor.
  → *Fix:* Maak de twee bollen ongelijk (verschil in grootte/rotatie) of vervang er één door een andere plantsoort. Vervang de picknicktafel door een loungestoel of een klein bijzettafeltje dat past bij een tuinkantoor.
- **🟡 minor · Grounding** — De picknicktafel rechts op het terras (midden-rechts) heeft nauwelijks contactschaduw en lijkt licht op het dek te zweven; ook de plantenbakken missen een duidelijke AO-schaduw op de deckplanken.
  → *Fix:* Verhoog AO/contactschaduw of zak de objecten 1-2 cm in het dek; controleer dat de bodemvlakken de deckplanken raken zodat niets zweeft.


## Magnolia — Wintertuin (scandi) — **3.5/10**
*Dit is een productfoto-op-een-gazon, geen "wintertuin"-sfeerbeeld: de hut staat plat frontaal in het midden, het licht is vlak en het beloofde winter-verhaal ontbreekt volledig.*

**Concept/licht:** Nee. Het concept "Wintertuin" komt totaal niet over: het gras is helgroen zomers, de heg is vol en groen, de bomen hebben volle naaldkroon, en er is geen enkel winterelement (geen kale takken, geen rijp, geen koele lucht, geen warme binnenverlichting die door het glas gloeit). Het bedoelde lichtmoment "zacht daglicht" is deels aanwezig (bewolkte lucht, diffuus) maar slaat door naar VLAK en levenloos — geen richting, geen warmte, geen volumetrische haze/godrays die Beike overal wil. Als losse titel "Wintertuin" eronder staat, klopt het beeld niet met het verhaal.

**Sterk:** De deur (echte DD-glasdeur met kozijn, beslag, scharnieren) leest overtuigend en op menselijke schaal — goede referentie voor de hoogte. · Het scandi bistro-set (metaal/hout klaptafel + 2 stoelen) is een geloofwaardig, passend product rechts. · De heg leest als dichte 3D-foliage (geen platte leaf-cards) en occludeert netjes de onderrand van de lucht.

**Problemen:**

- **🔴 BLOCKER · Lighting** — Het licht is volledig vlak en richtingloos over de hele hut. De grijze linkerwand en de frontwand hebben nagenoeg dezelfde helderheid; er is geen duidelijke zonrichting, geen kernschaduw op een gevel, geen slagschaduw van de hut op het gras. Daardoor oogt alles als een 3D-viewport-render, niet als een foto.
  → *Fix:* Zet een lage warme zon (Sun, ~15-25° elevatie, 3500-4500K) onder een lichte hoek links-voor zodat de linkerwand in schaduw valt en de frontgevel warm oplicht. Voeg een subtiele slagschaduw van de hut naar rechts-achter toe. Behoud AgX. Overweeg lichte volumetrische haze (Volume Scatter in world of een dun mist-volume) voor de 'licht-komt-erdoorheen' look.
- **🔴 BLOCKER · Concept** — Niets in de scene zegt 'winter'. Gras is fel zomergroen, heg is vol groen, naaldbomen hebben volle kronen, lucht is een neutrale zomerse bewolking. Het beloofde verhaal ontbreekt compleet.
  → *Fix:* Kies richting: OFWEL echte winter (kale loofbomen-silhouetten in de backdrop, ontkleurd/geelbruin wintergras, koelere 6000-6500K daglicht, eventueel rijp op de heg-toppen, warme oranje gloed IN de hut zichtbaar door het glas), OFWEL hernoem de scene. Voeg minimaal warme binnenverlichting (Point light achter het glas) toe zodat het als een 'wintertuin'-toevluchtsoord leest.
- **🔴 BLOCKER · Composition** — De hut staat vrijwel dood-centraal en volledig frontaal (frontgevel recht naar de camera). Geen rule-of-thirds, geen leidende lijn naar de deur, geen aantrekkelijke 3/4-hoek. Het is een technisch productplaatje, geen wervend hero-beeld.
  → *Fix:* Draai de camera naar een 3/4-hoek zodat de frontgevel én een zijwand zichtbaar zijn (meer volume/diepte). Plaats de hut op een derde-lijn i.p.v. midden. Voeg een leidende lijn toe (klinkerpad/stapstenen die naar de deur leiden) en breng het bistro-set als voorgrondlaag mee de compositie in.
- **🟠 MAJOR · Grounding** — Meerdere objecten hangen/zweven zonder contactschaduw. De lantaarn middenvoor en het stapeltje haardhout links-onder hebben nauwelijks AO/contactschaduw en lijken op het gras te plakken i.p.v. erin te staan. Ook de bistro-stoelpoten rechts missen duidelijke contactschaduw in het gras.
  → *Fix:* Verlaag objecten tot ze echt in de graslaag zakken en voeg contact-AO toe (kortere shadow-terminator, evt. een klein negatief displacement onder de props). Controleer dat poten/objectbases onder de graspluk-toplaag zitten, niet erbovenop.
- **🟠 MAJOR · Dressing** — De props vertellen geen samenhangend verhaal en staan verspreid als losse assets: een enkele lantaarn dumpt midden-voor de deur (blokkeert de looproute), een los stapeltje haardhout links-onder zonder context, bistro-set geïsoleerd rechts. Leeg, ongebruikt gevoel — geen 'geleefde tuin'.
  → *Fix:* Cluster de dressing in geloofwaardige zones: haardhout netjes tegen de gevel of in een rek, lantaarn naast de deur of op de bistro-tafel (niet midden op het pad), voeg 1-2 potplanten/varens bij de deur voor een verwelkomende entree. Houd de looproute naar de deur vrij.
- **🟠 MAJOR · Vegetation** — Het gras is CG-perfect: uniform helgroen, gelijkmatig hoog, zonder kale plekken, mos, klaver, kleurvariatie of platgetreden zones. In combinatie met de vlakke belichting versterkt dit de uncanny/plastic look, vooral op de grote open voorgrond links.
  → *Fix:* Voeg kleur- en lengtevariatie toe aan de grass-scatter (2-3 groentinten, gele/bruine sprietjes, wat mos/klaver-clumps), en breng lichte hoogtevariatie/platgetreden paadjes aan. Overweeg een subtiele grond-textuur die doorschemert zodat het niet als een egaal groen tapijt leest.
- **🟡 minor · Backdrop** — De boom-backdrop is een dunne rij losse naaldbomen bovenop de heg met veel open lucht ertussen; het leest deels als een 'zwevende' cutout-rand i.p.v. een dieptevol bos. Rechts is een grote lege lucht/veld-zone die het beeld voelt leegtrekt.
  → *Fix:* Voeg 2-3 ringen bomen achter de heg toe met variatie in soort/hoogte zodat de treeline dichter wordt en de lucht meer occludeert (conform de dichte-bos-regel). Vul de rechter open zone met wat naar voren gehaalde beplanting of een boom om de compositie te balanceren.
- **🟡 minor · Materials** — De grijze wandbeplating oogt erg egaal en strak (weinig grain-variatie/verwering), en de zijwand-planknaden lopen correct horizontaal maar de textuur is bijna te schoon/uniform — draagt bij aan de te-perfecte look. Geen zichtbare 90°-projectiefout, maar wel weinig leven.
  → *Fix:* Voeg subtiele roughness-/kleurvariatie en lichte verwering (per-plank tint-variatie, fijne noesten, vuil onderaan de gevel) toe aan het wandmateriaal. Verhoog micro-roughness-breakup zodat het hout minder als egaal vlak leest.


## Camelia — Wijnterras (mediterraan, namiddag) — **4/10**
*De basiscompositie zit er, maar het beeld verkoopt geen mediterraan namiddag-wijnterras: het hout is bleek-wit CG, de lucht is koud-blauw, de beplanting is schaars en het gras oogt als plastic gel-strips — dit is nog een productplaatje, geen sfeerbeeld.*

**Concept/licht:** Nauwelijks. De props (bistrotafel, rieten stoelen, wijnfles + 2 glazen, lichtsnoer, terracotta-potten, tegelterras) wijzen wel naar "wijnterras", maar het LICHT verraadt alles: koele blauwe lucht en vlakke schaduwloze belichting = geen namiddag, geen warme mediterrane gloed. Er is geen lage warme zon, geen lange schaduwen, geen volumetrische haze. Het bleke onbehandelde vurenhout versterkt Noord-Europees-nieuwbouw i.p.v. zonovergoten zuiden. Het verhaal wordt aangewezen door rekwisieten maar niet gevóeld.

**Sterk:** Prop-keuze past thematisch: rieten bistrostoelen, ronde cafétafel met wijnfles en twee glazen, en het lichtsnoer onder het afdak vertellen samen wel degelijk een terras-verhaal · De overdekte zithoek (open zijde onder het afdak) is een sterk, realistisch verkoopargument van dit model en is helder in beeld gebracht · Het tegelterras heeft een duidelijke vorm en verbindt de zithoek met de deur; de terracotta-potten links geven een aanzet tot mediterrane kleuraccenten

**Problemen:**

- **🔴 BLOCKER · Lighting** — De lucht is koud staalblauw en de belichting is vlak en schaduwarm over de hele scene (geen richting, geen lange namiddag-schaduwen op het terras of van de cabin op het gras). Dit leest als kille ochtend/middag, niet als warme mediterrane namiddag. Beike's doellook (lage warme zon + volumetrische haze + AgX) ontbreekt volledig.
  → *Fix:* Zet de zon laag (elevation ~12-18 graden) en warm (color temp ~3500-4000K), azimuth zo dat de cabin lange schaduwen naar rechts-voor werpt over het terras. Vervang/roteer de HDRI naar een gouden namiddag-hemel. Voeg een dunne volumetrische wereld-mist toe (density ~0.002) zodat de zon 'erdoorheen' komt. Controleer dat AgX view transform actief is.
- **🔴 BLOCKER · Materials** — Het hout van de cabin (voorwand, deurpaneel, binnenwanden onder het afdak) is bijna wit en volkomen egaal — het leest als plastic/gips, niet als hout. Geen zichtbare nerf-variatie of warmte. Dit is de grootste realisme-killer en past totaal niet bij 'mediterraan'.
  → *Fix:* Wissel naar een warmere, verzadigde houttextuur (honing/amber tint) met echte nerf en per-plank kleurvariatie; verlaag base value zodat het niet uitblaast. Voeg subtiele roughness-variatie/bump toe. Controleer of het geen uitgeblazen highlight is door de belichting — zo nodig ook exposure temperen.
- **🟠 MAJOR · Vegetation** — Het gras rond het terras oogt als CG-gel: uniforme felgroene rechtopstaande sprietjes-clumps in een bijna regelmatig patroon, allemaal even hoog, geen variatie, geen droge/bruine halmen. Voor mediterraan (droger klimaat) is dit dubbel verkeerd en het schreeuwt 'procedureel'.
  → *Fix:* Vervang door een dichter, lager grass-scatter met lengte- en kleurvariatie (meng groen met vergeelde halmen), randomize rotation/scale, en laat het niet in nette clumps staan. Overweeg mediterrane grond (grind/kiezel of droger gras) rond het terras i.p.v. sappig gazon.
- **🟠 MAJOR · Backdrop** — Achter de cabin staat één rij donkere naaldbomen tegen een lege lucht met veel zichtbare hemel eronder en ertussen — 'vliegend eiland'-gevoel, de treeline occludeert de lucht niet en er is geen diepte-opbouw. Rechts staat een losse dunne boom half buiten beeld. Naaldbomen passen bovendien niet bij een mediterraan verhaal.
  → *Fix:* Voeg minimaal 2-3 ringen bomen toe achter de cabin zodat de skyline dichtloopt, met variatie in hoogte/soort. Ruil (een deel van) de naaldbomen voor mediterraan-passende soorten (olijf, cipres, pijnboom-silhouet). Verwijder of integreer de losse rechter boom die nu tangentieel aan de framerand kust.
- **🟠 MAJOR · Dressing** — De aankleding is te schaars en eenzijdig links geconcentreerd: alle beplanting (2 potten met een schriele struik + een groter bladplant) staat linksvoor, terwijl de hele rechterhelft en de overdekte zithoek kaal zijn. Onder het afdak staat geen enkele plant of accent, waardoor de dure overkapping leeg en onaf oogt.
  → *Fix:* Verdeel beplanting over de scene: plaats mediterrane potten (lavendel, olijfboompje, rozemarijn, citrus in pot) ook rechts bij de zithoek en naast het afdak. Voeg een groter kuipplant-accent toe bij de open zijde zodat de rechterhelft balans krijgt.
- **🟠 MAJOR · Lighting** — Het lichtsnoer onder het afdak en doorlopend naar rechts is niet aan/geeft geen licht — bij een namiddag/avond-terrasconcept is dat een gemiste kans en nu leest het als losse witte bolletjes-draad. De draad hangt bovendien deels los in de lege lucht rechts zonder duidelijk bevestigingspunt (rechterbol kust bijna de framerand).
  → *Fix:* Geef de bolletjes een warm emissive-materiaal (emission ~2-4, kleur ~2200K) zodat ze gloeien en de zithoek warmte geven — versterkt meteen het namiddag/schemer-terrasgevoel. Anker het snoer zichtbaar aan een paal/boom rechts en houd de laatste bol weg van de framerand.
- **🟡 minor · Grounding** — De rieten stoelen en de bistrotafel rechts staan deels op het gras net buiten de tegelrand en lijken licht te zweven / missen overtuigende contactschaduw; de rechterstoel staat half op gras half naast de tegels, wat rommelig oogt.
  → *Fix:* Zet tafel + beide stoelen netjes ÓP het tegelterras met de poten binnen de rand, en verifieer AO/contactschaduw onder elke poot (drop op ground, kleine ambient occlusion).
- **🟡 minor · Composition** — De cabin staat vrij frontaal/plat in beeld en beslaat samen met het afdak bijna de volledige breedte; er is weinig leading line — het tegelterras leidt het oog niet duidelijk naar de deur, en de bovenrand van het dak zit dicht tegen de bovenframe-rand.
  → *Fix:* Draai de camera iets meer three-quarter zodat de zijwand meer diepte geeft, laat wat meer lucht boven het dak, en vorm het terras/pad zo dat een lijn richting de dubbele deur loopt (hero = deur). Plaats de cabin iets uit dead-center richting linkerderde.


## Jasmijn — Theehuis (japandi, ochtend) — **4/10**
*De cabin en de zen-tuin-aanzet zijn er, maar het beeld voelt kaal, mistig-doods en onbewoond — het thee-ritueel wordt niet verteld en het ochtendlicht ontbreekt volledig.*

**Concept/licht:** Nee. Het "thee-ritueel / japandi rust"-verhaal komt niet over: er is geen theeset, geen kussen, geen mens-schaal die rust suggereert — alleen een lege bank onder de overkapping en een losse steen op een grindveld. Het bedoelde ochtendlicht is er ook niet: de scene is egaal, koel-paars en schaduwloos, meer bewolkte schemer dan warme ochtend. Japandi-materialen (warm hout + rust) worden deels gesuggereerd door de bank en het grind, maar de zwarte wand plus roze/zalm-deur botsen qua palet en verpesten de sereniteit.

**Sterk:** De deels-open overkapping met de houten bank rechts geeft een geloofwaardige japandi-luifel en zichtlijn naar binnen · Het losse rots-element op het grindveld is een echt 3D-asset met goede detaillering en past bij een zen-tuin · De bol-gesnoeide struiken (rechts, achter de heg) lezen als echte dichte foliage en ondersteunen het japandi-snoeimotief

**Problemen:**

- **🔴 BLOCKER · Lighting** — De hele scene is vlak, schaduwloos en koel-paars; er is geen enkele richtingsschaduw op het gras of onder de cabin, de lucht is een egale grijs-paarse waas. Dit leest als bewolkte schemer, niet als warme ochtend. Het bedoelde 'licht-komt-erdoorheen'-moment (volumetrische haze + lage warme zon + AgX) ontbreekt volledig.
  → *Fix:* Zet een lage warme zon (elevation ~8-12°, kleur ~4500K) links-achter zodat lange schaduwen over het grind en gras vallen en de deur/bank warm oplichten. Voeg lichte volumetrische mist toe (Volume Scatter, dichtheid laag) zodat de treeline zonlichtstralen vangt. Zet view transform op AgX met iets meer look-contrast.
- **🔴 BLOCKER · Concept** — Het thee-ritueel wordt nergens verteld: onder de overkapping staat alleen een lege bank, geen theeset/dienblad/kop, geen zitkussen, geen leven. Rechtsvoor het grind ligt slechts één losse steen. Het verhaal 'japandi thee-rust' is leeg.
  → *Fix:* Dress de bank en/of een laag tafeltje met een theeset (pot + 2 koppen), een gevouwen plaid en een zitkussen; leg 1-2 zafu-kussens op het houten dek. Voeg eventueel een dampend theelicht/lantaarn toe. Gebruik alleen realistische japandi-props uit assets/, geen procedurele boxjes.
- **🟠 MAJOR · Materials** — Het kleurpalet botst hard met japandi: de wanden zijn bijna zwart, terwijl de dubbele deur felroze/zalm oplicht — dit oogt als een verkeerd/oversaturated of onbelicht deurmateriaal, niet als warm naturel hout. De combinatie zwart+roze verpest de serene sfeer.
  → *Fix:* Controleer het deurmateriaal (base color kan te verzadigd/roze staan of alleen door het paarse licht zo ogen); zet naar warm naturel douglas/eik. Overweeg de wand van bijna-zwart naar warm antraciet/verbrand-hout (shou sugi ban) zodat wand en deur in één japandi-palet vallen.
- **🟠 MAJOR · Vegetation** — Het gras is een egale, uniforme, CG-perfecte mat zonder variatie in hoogte, kleur of dichtheid; er zitten geen paadjes, mos of kale plekken in. Linksonder is een vage vuil-vlek maar verder is alles identiek. Dit oogt als een tiled scatter, niet als een echte tuin.
  → *Fix:* Voeg variatie toe aan de grass-scatter (density-painting, hoogte-random, 2-3 kleurvarianten, wat klaver/onkruid). Breek het vlak met een mos-rand rond het grind en een paar losse pollen. Voeg een subtiel klinker- of stapsteen-pad toe dat naar de deur leidt.
- **🟠 MAJOR · Composition** — De cabin staat vrijwel frontaal en dood-centraal in beeld, met de deur bijna op het midden; er is geen leidende lijn naar de deur en geen duidelijke voorgrond-laag behalve leeg gras. Het grindveld ligt scheef rechtsvoor en trekt het oog wég van de hero i.p.v. ernaartoe.
  → *Fix:* Draai de camera ~15-25° zodat de cabin op 3/4 komt en de open overkapping meer diepte krijgt; plaats de deur op een derde-lijn. Leg een stapsteen-pad of grind-lijn die vanuit de voorgrond naar de deur/overkapping leidt. Geef de cabin meer ademruimte bovenaan of breng een voorgrond-element (lantaarn/plant) in de onderhoek voor diepte.
- **🟠 MAJOR · Backdrop** — Achter de cabin en heg zweeft een egale grijs-paarse hemel; de bomen zijn ijl en dunbebladerd (vooral de dennen rechts en de boom linksvoor) waardoor de sky doorheen schijnt en een 'vliegend eiland'-void ontstaat. De verre bergen zijn wazig-paars en versterken de doodse waas.
  → *Fix:* Zet minimaal 2-3 ringen dichtere bomen achter de cabin zodat de sky geoccludeerd wordt; vervang/verberg de ijle low-poly boom-clusters (scripts/hide_bare_trees.py) door vollere assets. Verlaag de atmospheric-haze op de achtergrond of geef de bergen een warmere ochtendtint zodat ze niet als dode paarse smurrie lezen.
- **🟡 minor · Grounding** — Onder de overkapping lijken de bank en de twee ronde witte objecten (kiezels?) net op de rand te staan; de overgang van het houten dek naar het grind is een harde, te schone lijn zonder contactschaduw of vuil, waardoor het dek los op het maaiveld lijkt te liggen.
  → *Fix:* Voeg contact-AO/dirt toe op de dek-grond-overgang en zet een lage grind- of houten-drempel-rand. Controleer dat de bankpoten echte contactschaduw hebben; voeg wat verstrooid grind/blad rond de dek-rand voor natuurlijke overgang.
- **🟡 minor · Uncanny** — Het grindveld is een gladde, uniform-witte plaat zonder korrelstructuur of variatie — het leest als een geverfd vlak, niet als grind, en de scheve platte betonranden eromheen ogen te schoon en te dun.
  → *Fix:* Geef het grind een echte pebble/gravel-displacement of scatter van kleine steentjes met roughness-variatie; maak de begrenzing van natuursteen/houten balkjes i.p.v. dunne betonstrips en voeg wat mos/vuil in de voegen.


## Lelie — Avondkubus — **4/10**
*Sfeervolle blue-hour mist, maar het kernconcept faalt: de "verlichte kubus" is juist pikdonker en dood — alleen de paaltjes branden, terwijl de cabine zelf de held-lichtbron zou moeten zijn.*

**Concept/licht:** Nee. Het bedoelde verhaal is "modern avond, verlichte kubus" — de kubus moet gloeien als een baken in de schemering. In deze render is de cabine juist het donkerste vlak in het beeld: geen binnenverlichting die door het glas/de deur naar buiten schijnt, geen gevel-uplights, geen warme spill op de overkapping. De enige warme accenten zijn drie tuinpaaltjes die van de deur wég leiden. De blue-hour mist en lucht zitten goed, maar zonder brandende kubus verkoopt het beeld het concept niet.

**Sterk:** Overtuigende blue-hour hemel met echte volumetrische mist die de achterste dennen laat wegvagen — geen 'vliegend eiland', mooie dieptelagen naar achteren. · De warme tuinpaaltjes (bollards) hebben een geloofwaardige gloed en pool-of-light op de tegels, precies de juiste kleurtemperatuur-tegenstelling met de koele lucht. · Voorgrond-blad linksonder geeft echte compositielaag/diepte (foreground framing) zonder in de weg te zitten.

**Problemen:**

- **🔴 BLOCKER · Lighting** — De 'verlichte kubus' is niet verlicht: de hele cabine (gevel midden, overkapping rechts, dak) is het donkerste, vlakste vlak in het frame. Geen interieurgloed door de deur/ramen, geen gevel-uplight, geen warme spill onder de overkapping rechts. Het concept staat of valt hiermee en het ontbreekt volledig.
  → *Fix:* Plaats een warm area-light (2700K, ~30-50W) BINNEN de cabine achter de deur zodat het door beide glaspanelen naar buiten schijnt; maak het deurglas echt transmissief (Transmission 1, IOR 1.45). Voeg 2-3 kleine warme spots/uplights onder de overkapping rechts en langs de gevel toe zodat de kubus als lantaarn oplicht. Til de exposure/emissie zo dat de gevel 1-2 stops helderder is dan de omgeving.
- **🔴 BLOCKER · Materials** — Het linker deur-glaspaneel is een dichte, egaal-crème rechthoek (zie deur-crop): geen transparantie, geen reflectie, geen interieur — leest als karton/broken material. Het rechter paneel is wél donker-transparant, dus de twee panelen matchen niet.
  → *Fix:* Vervang het linker glasmateriaal door hetzelfde glas-shader als rechts (Glass BSDF of Principled met Transmission=1, Roughness ~0.03). Als de crème kleur een bedoelde 'gordijn/frosted' look is, maak er dan een echt frosted-glass van (Roughness 0.4-0.6) MET een warme interieur-emissie erachter, niet een platte fill.
- **🟠 MAJOR · Materials** — De cabinegevel (wall-crop) is een bijna egaal dof-grijs vlak zonder zichtbare plank-articulatie, naad of houtnerf; leest als geverfd beton/karton i.p.v. modern zwart-hout. Rechter overkapping-wand is helemaal richel-loos.
  → *Fix:* Controleer of de wand-UV met de plank meeloopt via cl.uv_board_textures() (bekende 90°-box-projectie-bug); voeg een donker-hout of zwart-gebrande-hout PBR met zichtbare normal/roughness-variatie toe zodat horizontale plankschaduwen ontstaan. Verlaag roughness net genoeg voor subtiele blue-hour sky-reflectie op de gevel.
- **🟠 MAJOR · Composition** — De paaltjes-lichtlijn (leading line) loopt van de deur naar rechtsonder de frame uit, wég van de held. De cabine staat vrij frontaal/centraal en het pad naar de deur (midden) is kort en zwak; de sterkste leidende lijn wijst dus de verkeerde kant op.
  → *Fix:* Draai de bollard-rij zo dat de lichtlijn juist NAAR de deur toe leidt (van rechtsvoor naar de entree). Verplaats de camera iets naar rechts en verlaag naar ~1.6m ooghoogte/35mm zodat de deur op een derde-lijn valt en het toegangspad de blik naar binnen trekt.
- **🟠 MAJOR · Uncanny** — Het toegangspad bij de deur (tegels links van de heg) is deels versmolten/vervormd en de grasstekels groeien dwars door de tegelvoegen; de tegels ogen nat-plastic en onregelmatig uitgesneden. Leest CG en rommelig.
  → *Fix:* Herstel het klinker/tegel-pad met cl.klinker_strip of een net paving-grid met schone voegen; masker de gras-scatter uit op het padoppervlak (weight-paint/geometry-node mask) zodat er geen sprieten door de tegels prikken. Verlaag de nat-glans (roughness omhoog) op de tegels.
- **🟡 minor · Vegetation** — De heggen (voor de deur en rechts) zijn dicht maar bijna uniform egaal-lime van kleur en gelijkmatig van vorm; de heg voor de deur blokkeert bovendien de rechter helft van de entree.
  → *Fix:* Voeg kleur/hoogte-variatie en wat losse uitstekende twijgen toe aan de heg-scatter, en verklein/verplaats de heg vóór de deur zodat de entree vrij komt te staan als focuspunt.


## Magnolia — Groene Long (eco-groendak) — **4/10**
*Het groendak-concept is herkenbaar maar de scene is te leeg, plat belicht en de sedum ziet er als geel stro uit — dit verkoopt "duurzaam" nog niet overtuigend.*

**Concept/licht:** Half. Het groendak leest wel als de hero-feature en de regenton links ondersteunt het duurzaamheidsverhaal netjes, maar het "sedum" oogt als droog geel gras/stro i.p.v. sappig groen sedum, en het lichtmoment "helder" ontbreekt volledig: de lucht is grijs-melkachtig, de zon is nauwelijks richtinggevend en er is geen frisse heldere sfeer. Het eco-verhaal komt dus wel binnen, maar de "gezonde, levende, duurzame" emotie niet.

**Sterk:** Het platte groendak met dakrand-detail is duidelijk de hero-feature en meteen leesbaar als eco/sedum-dak · De groene regenton met valpijp links onderbouwt het duurzaamheidsverhaal en is een geloofwaardig Blokhutwinkel-product · De dichte donkere hag rondom occludeert de lucht goed en voorkomt een 'zwevend eiland'-effect achter de cabin

**Problemen:**

- **🔴 BLOCKER · Vegetation** — Het sedum-groendak (bovenop, hele daklengte) is geel/stro-kleurig en ziet eruit als dor gras of graanhalmen, niet als vet groen sedum. Dit ondermijnt letterlijk de kern van de 'Groene Long / eco-groendak' — het dak oogt dood i.p.v. levend.
  → *Fix:* Vervang de gele grass-scatter door een sedum/vetplant-scatter: korte gedrongen instances, kleurmix van groen naar roodpaars, veel lagere hoogte (2-4cm i.p.v. de huidige lange halmen). Zet basiskleur van de scatter-instances naar verzadigd groen en varieer met een ColorRamp op random per-instance.
- **🔴 BLOCKER · Lighting** — Het lichtmoment 'helder' ontbreekt: de lucht (boven, achter de bomen) is vlak melkgrijs, schaduwen zijn zwak en er is geen duidelijke zonrichting behalve de vage tak-schaduw links op de wand. Alles oogt bewolkt/dof, niet helder.
  → *Fix:* Wissel naar een heldere HDRI met blauwe lucht en lage warme zon (~10-15° elevatie), verhoog sun strength, en voeg lichte volumetrische haze (Volume Scatter, dichtheid ~0.002) toe voor Beike's 'licht-komt-erdoorheen'-look. Behoud AgX. Zorg dat elke prop een duidelijke grondschaduw krijgt.
- **🟠 MAJOR · Composition** — De cabin staat vrijwel frontaal en centraal in het frame; het pad rechtsonder loopt niet naar de deur maar naar de rechter beeldrand toe, dus er is geen leading line naar de entree. Weinig voorgrond-laag, weinig diepte.
  → *Fix:* Draai de camera ~15-20° zodat de cabin een sterkere 3/4-hoek krijgt en verplaats het klinker/tegelpad zo dat het vanaf de voorgrond naar de dubbele deur leidt. Zet de deur op een derde-lijn i.p.v. centraal.
- **🟠 MAJOR · Grounding** — De regenton (linksvoor) staat op het gras zonder duidelijke contactschaduw/AO en lijkt licht op het gras te 'plakken' i.p.v. erin te staan; onderrand oogt zwevend. Ook de losstaande tegels rechtsonder liggen bovenop het gras zonder inzinking/vuilrand.
  → *Fix:* Voeg contact-AO toe (kleine ambient occlusion of los shadow-plane), zak de regenton 1-2cm in het maaiveld en scatter wat gras-instances tegen de voet. Zink de tegels iets in de grond en voeg mos/vuil-randen toe langs de voegen.
- **🟠 MAJOR · Backdrop** — Boven de hag staan losse donkere naaldbomen (bovenaan het frame) als silhouetten tegen een lege grijze lucht; ze ogen als losse plakkers zonder tussenliggende diepte, en de lucht ertussen is een kale void.
  → *Fix:* Voeg 2-3 ringen bomen met variatie in hoogte/soort achter de haag toe zodat de treeline gelaagd wordt, en gebruik een HDRI met wolkenstructuur zodat de lucht tussen de bomen niet leeg is.
- **🟡 minor · Materials** — De wandplanken (rechterwand, rond de deur) ogen erg schoon en uniform met bijna plastic-gladde look; de deurpanelen (donker hout onder het glas) hebben een iets te egale, natte glans. Weinig slijtage of variatie.
  → *Fix:* Voeg subtiele roughness-variatie en een lichte grunge/dirt-map toe op de wandplanken en verlaag de specular op de deurpanelen iets. Voeg minieme kleurvariatie per plank toe voor natuurlijker hout.
- **🟡 minor · Dressing** — De scene is verder vrijwel leeg: buiten regenton en pad is er geen aankleding, waardoor het meer een product-shot dan een levende Nederlandse tuin is.
  → *Fix:* Voeg 1-2 geloofwaardige eco-props toe: een lage border met vaste planten links van de cabin, of een houten plantenbak, om het duurzaamheidsverhaal te versterken zonder rommel.


## Zonnebloem — Zomeravond (boerderij, sunset, samen eten) — **4/10**
*Sfeervolle avond-opzet met feestverlichting en eethoek, maar de voorgrond wordt geruineerd door een grote plas glimmend nat/reflecterend gras dat het beeld voor marketing onbruikbaar maakt.*

**Concept/licht:** Het concept "samen eten op een zomeravond" komt deels over: de eettafel met stoelen onder de overkapping, de lichtslinger en de warme gloed door het raam vertellen het verhaal. Maar het lichtmoment "sunset" wordt zwak verkocht — de lucht is bleek/koel grijsroze zonder echte zonsondergangsgloed, er is geen duidelijke lage warme zonrichting en geen volumetrische haze. De sfeer neigt eerder naar "schemer/blauw uur" dan naar een warme zomeravond-zonsondergang. De natte glansplek op de voorgrond breekt de illusie volledig.

**Sterk:** De lichtslinger (feestverlichting) over de patio en langs de gevel verkoopt de gezellige avond-eet-sfeer echt goed en is een sterke storytelling-keuze. · De warme gloed uit het raam en de open deur tegenover de koelere buitenlucht geeft geloofwaardig avond-contrast. · De houtwand leest correct: plankrichting horizontaal, grain loopt mee met de plank, geen 90°-box-projectie-bug zichtbaar.

**Problemen:**

- **🔴 BLOCKER · Materials** — De hele voorgrond (onderste derde, midden-links tot midden) is een grote glimmende, natte, spiegelende plek — het gras/de grond reflecteert het licht als een plas water. Dit oogt als een nat/kapot grondmateriaal en verwoest het beeld direct.
  → *Fix:* Controleer het grondmateriaal onder/naast de grass-scatter: roughness staat waarschijnlijk veel te laag (bijna 0) en/of Specular te hoog. Zet grond-roughness naar 0.85-1.0, Specular naar ~0.2, en verwijder eventuele Wetness/Water-mixnode. Check ook of er geen tweede transparante/glossy plane over de voorgrond ligt.
- **🔴 BLOCKER · Vegetation** — Het voorgrondgras (onderste derde) is een uniform, kort, stekelig raster van identieke sprietjes — leest als CG-'painted grass' die overal even hoog en even dicht is, zonder pollen, variatie of langere randen. Rondom de rozen/pad springt het onnatuurlijk hard af.
  → *Fix:* Vervang/verrijk de grass-scatter: meng 2-3 grasvarianten met verschillende hoogtes, voeg lengte-variatie (Random scale 0.6-1.4) en clumping toe, laat het gras rond paden/borders uitlopen, en verlaag de perfect-uniforme dichtheid. Voeg wat klaver/onkruid/gele bloemetjes toe voor boerderij-natuurlijkheid.
- **🟠 MAJOR · Lighting** — Ondanks 'sunset' is er geen zichtbare lage warme zonrichting: schaduwen zijn diffuus/afwezig, de lucht is bleek koelgrijs-roze zonder oranje horizon-gloed, en de volumetrische 'licht-komt-erdoorheen'-haze (Beike's doellook) ontbreekt volledig. Beeld voelt vlak/schemerig i.p.v. gouden avond.
  → *Fix:* Draai de zon laag (5-10° boven horizon) vanaf links/achter voor rim-light op cabin en bomen, kleurtemperatuur ~2800-3200K. Voeg een subtiel volumetrisch mist-domein (density ~0.002-0.005) toe zodat de lichtslinger en zonstralen 'glow' krijgen. Warm de HDRI/sky-horizon op naar oranje. AgX view transform behouden.
- **🟠 MAJOR · Grounding** — De rozenstruiken en hortensia's (voorgrond links, midden en rechts) missen contactschaduw/AO — ze lijken op het glimmende gras te zweven i.p.v. erin geworteld te staan. Ook de eettafel/stoelen onder de overkapping hebben weinig zichtbare grondschaduw.
  → *Fix:* Voeg AO/contactschaduw toe: zet de plant-bases iets in de grond (Z iets omlaag), voeg een klein donker AO-decal of dichte scatter rond de stam toe. Verhoog Ambient Occlusion in de render-settings of voeg een grond-shadow-catcher check toe; controleer dat objecten daadwerkelijk de grond raken (bbox Z-min = terrein-hoogte).
- **🟠 MAJOR · Composition** — De cabin staat vrijwel frontaal/plat en bijna centraal; de eettafel en de mooiste sunset-story (rechts) worden half afgesneden door de rechterrand, en er is geen leidende lijn (pad) die het oog naar de deur voert — het klinkerpad loopt onopvallend rechts weg.
  → *Fix:* Draai de camera iets naar rechts/lager (ooghoogte ~1.6m, ~35mm) zodat de open eethoek volledig in beeld komt en de cabin onder een 3/4-hoek staat. Leg een duidelijker klinker/graspad dat vanaf de voorgrond naar de deur leidt (rule-of-thirds: deur op linker-derde-lijn).
- **🟡 minor · Backdrop** — De boom-backdrop is een silhouet-rij die redelijk de lucht occludeert, maar de bomen zijn erg donker/plat en er zit een lichte 'floating'-band bleke lucht onder de kruinen rechts; weinig dieptelagen tussen heg en bomen.
  → *Fix:* Voeg 1-2 ringen bomen/struiken toe achter de heg voor diepte, breng minimale rim-light op de boomsilhouetten (van de lage zon) zodat ze niet als vlakke zwarte cut-outs lezen, en sluit de lucht-gap onder de kruinen.
- **🟡 minor · Dressing** — De tafel is gedekt met alleen een karaf en een lantaarn/fles — voor 'samen eten' is dit erg leeg; er ontbreken borden, glazen of eten die het verhaal 'samen eten' echt verkopen.
  → *Fix:* Voeg 2-4 couverts toe (borden, wijnglazen, een schaal/broodplank) op de tafel, klein en realistisch. Houd het boerderij-passend en uncluttered.


## Camelia — Buitenbad (hot-tub-premium / scandi-spa, blue hour) — **4.5/10**
*Het beeld leest als een net-buitenbad-render, maar zwakke compositie (cabin bijna frontaal-centraal), een dood grasveld en een pad-dat-nergens-heen-leidt houden het ver van marketing-klaar.*

**Concept/licht:** Gedeeltelijk. De hot-tub met opgevouwen handdoeken, de open overkapping en het houten terras verkopen wél het wellness-idee. Maar het "blue hour"-moment mist: de lucht is warm-roze/paars i.p.v. koel-blauw, en er is geen enkele lampsfeer (spa bij schemer = warme gloed uit cabin/tub die de koele lucht contrasteert). Nu voelt het als bewolkte late namiddag, niet als premium blue-hour-spa. Het "licht-komt-erdoorheen"-doel (volumetrische haze, lage warme zon) ontbreekt volledig — de lucht is vlak en er is geen atmosfeer tussen de bomen.

**Sterk:** Hot-tub zelf is een geloofwaardig, echt 3D-asset met nette houten mantelpanelen, opgevouwen handdoeken en een klein bijzettafeltje — verkoopt het spa-verhaal · Terrasdeck onder de overkapping en de klinkerstrip zijn echte materialen, geen procedurele boxjes · Dichte hoge dennenboom-backdrop occludeert de horizon netjes, geen 'vliegend eiland'-effect achter de cabin

**Problemen:**

- **🔴 BLOCKER · Composition** — De cabin staat bijna frontaal en centraal-links; het beeld is statisch en 'catalogus-plat'. Er is geen duidelijke hero-diagonaal, en de rechterhelft (hot-tub) en linkerhelft (cabin) concurreren om aandacht i.p.v. dat het pad de blik naar de deur leidt.
  → *Fix:* Camera ~20-30° naar rechts draaien en iets dichterbij zetten zodat de cabin een sterke 3/4-hoek krijgt met de lange overkapping+tub als diepte-laag rechts. Zet cabin-deur op de linker-derde lijn. Eye-level ~1.6m, ~35mm behouden.
- **🔴 BLOCKER · Lighting** — Het bedoelde 'blue hour' is niet geleverd: de lucht is warm roze/paars en overal vlak-diffuus, geen richting-zon, geen koel-blauwe schemertint, en geen enkele kunstlicht-accent. Een premium schemer-spa hoort een koele lucht + warme lampgloed contrast te hebben.
  → *Fix:* Zet een koele blue-hour HDRI/sky (world naar diep blauw-paars, lagere strength). Voeg warme point/area lights toe: gloed binnen de cabin achter het glas, LED-strip onder de tub-rand, en een klein spotje op het bijzettafeltje. Behoud AgX. Zon laag en warm zetten zodat er tóch één zwakke richting-schaduw ontstaat.
- **🔴 BLOCKER · Vegetation** — Het gazon links en in de voorgrond is dood/schraal: spichtige, verspreide grassprieten op kale donkere aarde i.p.v. een dicht groen wellness-gazon. Ziet er verwaarloosd uit, ondermijnt het 'premium' verhaal volledig.
  → *Fix:* Grass-scatter density fors omhoog (kortere maar veel dichtere sprieten), grondkleur naar rijk groen, en een korte gemaaide gazon-look. Voeg wat clustervariatie/klaver toe tegen de gridded look. Overweeg een grond-plane met echte gras-textuur onder de scatter zodat er geen kale aarde doorschijnt.
- **🟠 MAJOR · Composition** — Het klinkerpad loopt van rechts-onder naar de deur maar 'sterft' halverwege in het gras aan de rechterkant — het leidt de blik niet consistent en de losse klinkers rechtsonder rafelen uit in het niets. Ook loopt het pad naar de deur, niet naar het terras/tub, terwijl de tub de eyecatcher is.
  → *Fix:* Pad als één doorlopende, nette strook maken die van voorgrond naar de deur loopt én aftakt naar het terrasdeck. Losse uitrafelende klinkers rechtsonder verwijderen; randen recht afkaderen.
- **🟠 MAJOR · Grounding** — De hot-tub en het terrasdeck lijken op het maaiveld te zweven: er is nauwelijks contactschaduw/AO waar deck en tub het gras raken, waardoor het geheel bovenop het gras 'plakt' i.p.v. erin te zakken.
  → *Fix:* Contact-AO versterken (ambient occlusion in compositing of donkere gras-transition onder deckrand), deck 1-2cm laten inzakken of een grind/kiezelrand langs het deck leggen. Zachte slagschaduw van tub op gras toevoegen.
- **🟠 MAJOR · Backdrop** — De dennenbomen achter de cabin zijn ijl/uitgedund aan de onderzijde — de stammen zijn zichtbaar met gaten tussen heg en kroon, waardoor de skyline 'kaal onderaan' oogt en niet als dichte tuinbeplanting leest.
  → *Fix:* Extra ring lagere struiken/coniferen tussen heg en dennen plaatsen zodat de overgang dicht is, of de dennen naar voren/omlaag schalen zodat kronen de gaten dichten. Minimaal geen zichtbare kale stammen tussen heg en kroon.
- **🟡 minor · Materials** — De cabin-wanden zijn egaal donkergrijs met erg lage variatie en een licht plastic/matte uniforme uitstraling; op de linker zijwand zijn vage horizontale plank-naden nauwelijks zichtbaar en de textuur oogt vlak.
  → *Fix:* Meer roughness-variatie en subtiele houtnerf/plank-detail in de wandtextuur; check dat de nerf mét de plankrichting loopt (geen 90°-box-projectie). Lichte kleurvariatie per plank toevoegen tegen de egale look.
- **🟡 minor · Dressing** — De open overkapping rechts is helemaal leeg — een donker gat naast de tub. Voor een premium spa mist hier dressing (bijv. loungebank, handdoekrek, plant), nu leest het als ongebruikte lege ruimte.
  → *Fix:* Één geloofwaardig Blokhutwinkel-passend item onder de overkapping zetten (lounge/bankje of teak-krukje met opgerolde handdoeken) plus een subtiele warme lamp, zodat de overkapping bij het spa-verhaal hoort.
- **🟡 minor · Uncanny** — De twee terracotta potplanten links en rechts van de compositie zijn identiek en spiegelsymmetrisch geplaatst (zelfde pot, zelfde plant), wat CG-perfect/nep oogt.
  → *Fix:* Eén pot vervangen door een ander model/plant en de plaatsing asymmetrisch maken; lichte rotatie/schaalvariatie zodat het niet als gespiegeld duo leest.


## Dahlia — Leeshoek (scandi) — **4.5/10**
*Een technisch nette maar levenloze catalogus-render die het "leeshoek/rust"-verhaal niet vertelt: de compositie is te frontaal, het licht plat, en de scattered lavendel plus zwevende meubels doorbreken de illusie.*

**Concept/licht:** Nauwelijks. Het "leeshoek / rust"-idee zit alleen in de losse boek-op-tafel en de fauteuil, maar de compositie voelt als een productfoto van het gebouw, niet als een uitnodigende rustplek. Het "zacht daglicht" ontbreekt volledig: de lucht is helderblauw met harde zon, geen warm, diffuus of volumetrisch licht — precies het tegenovergestelde van de zachte, sfeervolle look die Beike overal wil. Er is geen intieme, geborgen leeshoek-sfeer; alles staat te ver uit elkaar op een lege vloer.

**Sterk:** De Scandi-fauteuil met plaid en het boek op de tafel zijn echte, geloofwaardige props die bij de stijl passen · De houtnerf op de overkapping-achterwand loopt correct verticaal/horizontaal mee met de planken — geen 90°-projectiebug zichtbaar daar · De heg achter de cabin leest als dichte foliage en occludeert de lucht redelijk, geen floating-island

**Problemen:**

- **🔴 BLOCKER · Composition** — De cabin staat vrijwel frontaal (flat-on) en centraal in beeld, met de gevel evenwijdig aan de camera. Geen driekwart-hoek, geen leidende lijn naar de deur, geen duidelijke foreground→midground→background gelaagdheid. Het oogt als een technische elevatie-render, niet als een marketing-hero.
  → *Fix:* Roteer de camera naar een driekwart-hoek (30-45°) zodat zowel de dichte gevel als de open overkapping in perspectief lopen. Plaats de cabin uit het midden (rechts-derde), gebruik het terras/patiopad als leidende lijn naar de leeshoek. Lens ~35mm, ooghoogte 1.6m.
- **🔴 BLOCKER · Lighting** — Het licht is plat en hard: strakblauwe lucht, felle zon, nauwelijks slagschaduwen, geen atmosfeer. Het bedoelde 'zacht daglicht' en Beike's volumetrische 'licht-komt-erdoorheen'-look ontbreken compleet. De overkapping-ruimte is dood en grijs zonder sfeerlicht.
  → *Fix:* Vervang HDRI door een zachtere bewolkt/gouden-uur variant, verlaag de zon-hoek voor langere warme schaduwen, voeg een lichte volumetrische haze toe (Volume Scatter in world of een cube), en render met AgX. Warm colortemp ~4500-5000K.
- **🟠 MAJOR · Vegetation** — De lavendel staat als een rcommelige, gegridde rij losse pollen dwars door de voorgrond (foreground-midden), deels drijvend/op de terrasrand geplakt en botsend met de tafelvoet. Het leest als scatter-instances, niet als een natuurlijke border. Het gras eromheen is CG-perfect en repetitief.
  → *Fix:* Cluster de lavendel in 2-3 natuurlijke groepen met variatie in schaal/rotatie i.p.v. een gelijkmatige rij; haal ze weg voor de tafel zodat ze de leeshoek niet blokkeren. Grond elke pol met contact-AO. Breek het gras met noise/variatie en losse plukken/onkruid.
- **🟠 MAJOR · Grounding** — Meerdere objecten lijken te zweven of missen contactschaduw: de tafel en fauteuil op de lichte houten vloer werpen nauwelijks AO, de lavendelpollen rechts staan half op de vloerrand, en de stapel brandhout rechts (blok tegen de gevel) zweeft los tegen de wand zonder grounding.
  → *Fix:* Zet Ambient Occlusion / contactschaduwen aan en verifieer dat elk meubelpoot de vloer raakt (drop-to-ground). Verplaats het brandhout zodat het stevig op de vloer/grond staat, niet tegen de muur geplakt.
- **🟠 MAJOR · Dressing** — De houten terrasvloer stopt met een harde, drijvende rand zonder plint/fundering — de rechtervoorhoek zweeft boven het gras en de vloer sluit links niet aan op de grijze tegels (er zit een gat/niveauverschil). De grijze betontegels links ogen te schoon en abrupt afgekapt.
  → *Fix:* Voeg een randbalk/opstand onder de terrasrand toe zodat het deck op de grond rust; laat de tegels en het deck vloeiend op elkaar aansluiten of scheid ze met een grindstrook. Voeg lichte vuil/wear op tegels en deck toe.
- **🟡 minor · Uncanny** — Alles is te schoon en perfect: smetteloze grijze wand, gloednieuw deck, vlekkeloze tafel en tegels. Geen vuil, mos, bladafval of gebruikssporen — typische CG-perfectie.
  → *Fix:* Voeg subtiele roughness-variatie en dirt-maps toe op wand/deck/tegels, wat bladafval/mos in hoeken, en lichte wear op de meubels voor geleefde realisme.
- **🟡 minor · Composition** — De boomtoppen achter de cabin worden bovenaan door de framerand afgesneden (tangent langs de bovenrand) en de bomen staan als een symmetrische rij, wat kunstmatig oogt.
  → *Fix:* Kadreer iets ruimer of laat een boom volledig binnen frame; varieer boomhoogte/spacing zodat de treeline organisch en niet-gegrid leest.


## Jasmijn — Familietuin — **4.5/10**
*Een schone maar bloedeloze catalogus-render: de cabin staat er plat-frontaal bij als een technische tekening, het gras is CG-perfect en er is geen enkel spoor van middaglicht-sfeer of familieleven.*

**Concept/licht:** Zwak. Het "familietuin"-verhaal wordt niet verteld: er is een zandbak, picknicktafel en vogelbad, maar niks leeft (geen speelgoed, geen dekens, geen kussens, geen gevallen bladeren in de zandbak) dus het oogt als een showroom-opstelling in plaats van een gebruikte gezinstuin. Het bedoelde lichtmoment "middag" komt totaal niet over: de belichting is vlak en schaduwloos-diffuus, zonder duidelijke zonrichting, zonder warmte en zonder de volumetrische "licht-komt-erdoorheen"-haze die Beike overal wil. Het beeld is helder maar emotieloos.

**Sterk:** De houtnerf op de wandplanken loopt correct horizontaal mee met de plankrichting — geen 90°-box-projectie-bug hier zichtbaar. · De hydrangea's (blauw links, rood/roze midden en rechts) zijn echte volumetrische 3D-planten met geloofwaardig blad, geen flat cards. · De achterste dennenboom-rij is dicht genoeg om de lucht grotendeels te occluderen; geen echt 'vliegend eiland'-gat achter de cabin.

**Problemen:**

- **🔴 BLOCKER · Camera** — De cabin staat vrijwel dood-frontaal en horizontaal gecentreerd in het frame; de camera kijkt recht op de voorgevel, waardoor het beeld leest als een productfoto/technische tekening in plaats van een sfeervolle tuinscene. Er is geen leidende lijn naar de deur en nauwelijks diepte-gelaagdheid.
  → *Fix:* Roteer de camera ~25-35° naar een 3/4-hoek zodat zowel voorgevel als de open overkapping-zijde onder perspectief te zien zijn. Plaats de cabin op een derde-lijn (bijv. deur op linker verticale derde). Zet lens op ~35mm en camerahoogte op 1.6-1.7m ooghoogte. Leg een pad of steppende tegels van de voorgrond naar de deur als leading line.
- **🔴 BLOCKER · Lighting** — De belichting is volledig vlak en diffuus — nergens een duidelijke, enkele zonrichting; slagschaduwen ontbreken vrijwel (kijk onder de picknicktafel, het vogelbad en de cabin: alleen zwakke AO, geen echte gerichte schaduw). Dit dood het 'middag'-gevoel en de hele scene oogt als een bewolkt studio-shot.
  → *Fix:* Voeg een Sun-lamp toe met duidelijke azimut/elevatie voor middag (elevatie ~45-55°), warme kleur (~5200-5500K, licht warm), strength ~3-4. Gebruik een HDRI met richting-cue of stem de sun op de HDRI af. Zet Cycles zon-schaduwen aan zodat picknicktafel, vogelbad, hydrangea's en cabin echte grondende slagschaduwen krijgen.
- **🟠 MAJOR · Lighting** — De door Beike gewenste signatuur-look (volumetrische ochtend/middag-haze + lage warme zon + AgX 'licht-komt-erdoorheen') ontbreekt volledig; de lucht is koel en de sfeer neutraal-kil, wat het gezinstuin-verhaal koud maakt.
  → *Fix:* Voeg een dunne volumetrische mist/atmosphere toe (Volume Scatter in een world- of box-volume, lage density) zodat licht tussen de dennenbomen door zichtbaar wordt. Controleer dat AgX view transform actief is en warm de world/zon iets op voor middaggloed.
- **🟠 MAJOR · Materials** — Het gras is CG-perfect: uniform egaal groen, gelijkmatige spriethoogte, geen kale plekken, geen kleurvariatie, geen platgelopen paden bij de cabin/tafel. Dit is een klassiek uncanny-valley-signaal en verraadt direct dat het een render is.
  → *Fix:* Voeg kleur- en lengtevariatie toe aan het grass-scatter (density- en scale-noise via een Noise/Musgrave texture op de GN-scatter), meng gele/bruine sprietjes en wat klaver/onkruid, en druk het gras plat (kortere density) op looproutes rond de deur, tafel en zandbak.
- **🟠 MAJOR · Materials** — Vrijwel al het hout (cabin-wanden, dakrand, zandbak-rand) is fabrieksnieuw, vlekkeloos en identiek van tint — geen verwering, geen vuil onderaan de wand, geen spatwater/aarde bij de grondcontact-lijn. Bij een 'gebruikte familietuin' is dit ongeloofwaardig.
  → *Fix:* Voeg subtiele weathering toe: donkerdere/vochtige tint onderaan de wandplanken (gradient mask van onder), lichte grijs-vergrijzing op de dakrand, en wat variatie in plank-tint via een per-plank random color node. Voeg AO/vuil toe waar wand het gras raakt.
- **🟠 MAJOR · Dressing** — De scene 'vertelt' geen familie: de zandbak is spierwit-leeg en steriel (geen schepje, emmertje, voetafdrukken, geen bladeren), de picknicktafel is kaal, en er is geen enkel spoor van gebruik. Het leest als een lege productopstelling, niet als een gezinstuin.
  → *Fix:* Kleed het verhaal aan: leg 1-2 speelgoed-props in/bij de zandbak (emmer, schepje), leg een dienblad met kannetje of een paar kussens op de picknicktafel, en breng lichte onregelmatigheid in het zand (bult/kuiltje). Houd het spaarzaam en realistisch (Blokhutwinkel-plausibel).
- **🟠 MAJOR · Grounding** — De zandbak in de linker-voorgrond lijkt eerder op het gras te liggen dan erin te zakken; de contactschaduw is minimaal en het gras stopt hard aan de rand in plaats van er tegenaan/overheen te groeien, waardoor het object licht 'zwevend'/opgeplakt oogt.
  → *Fix:* Zak de zandbak een paar cm in het maaiveld, voeg een stevigere contact-AO/slagschaduw toe onder de rand, en laat het grass-scatter tot tegen (en licht over) de houten rand groeien zodat de overgang natuurlijk wordt.
- **🟡 minor · Backdrop** — Achter de heg staat een strakke, egale gele maïs/graanstrook die als een uniforme horizontale band over de volle breedte loopt — te regelmatig en te fel, waardoor het als een getextureerde muur leest in plaats van diepte.
  → *Fix:* Breek de band met hoogte-/kleurvariatie, laat de heg op plekken hoger komen om de strook deels te occluderen, of vervang door een tweede struik/boom-ring voor natuurlijker diepteverloop; demp de saturatie van de gele strook iets.
- **🟡 minor · Composition** — Het vogelbad rechts-voor snijdt met zijn schaal bijna de rechter beeldrand (tangent-risico) en staat visueel geïsoleerd van de rest van de aankleding, waardoor de rechterhelft leeg-druk aanvoelt.
  → *Fix:* Schuif het vogelbad iets naar binnen (weg van de rechterrand) en groepeer het met wat lage beplanting of een tweede plant eromheen zodat het als bewust compositie-element leest in plaats van losstaand rekwisiet.
- **🟡 minor · Vegetation** — De hydrangea-clusters staan als losse, gelijkmatig verdeelde bollen in een verder kale grasvlakte (links-voor, midden-voor, rechts bij heg) — te 'geplaatst' en zonder onderbegroeiing, wat gridderig/opgesteld oogt.
  → *Fix:* Cluster de bloemen in onregelmatige groepjes met variatie in grootte, voeg lage onderbeplanting/gras-pollen rond de voet toe en meng 1-2 extra soorten zodat het als een gegroeid border leest in plaats van losse potplanten op het gazon.


## Roosmarijn — Zentuin (japanese-zen, overcast) — **4.5/10**
*Het zen-concept komt op zich door (grind, rotsen, lantaarn), maar de foto is verpest door een agressief plat CG-grasveld en een halfslachtige overkapping die leeg en verkeerd aangekleed staat — nog geen marketingbeeld.*

**Concept/licht:** Half. De ingrediënten van een zentuin zijn er (geharkt grind-veld, drie rotsen als kōan-groepje, stenen lantaarn, donkere strakke cabin, esdoorn links) en de overcast-lucht past bij contemplatie. Maar het beeld ademt geen rust: het felle, drukke gazon vecht met het rustige grindveld, de overkapping is grotendeels leeg en donker (dood in plaats van uitnodigend), en er is geen enkele volumetrische haze of zacht strijklicht dat de "licht-komt-erdoorheen" sfeer geeft die de zen-rust zou verkopen. Het leest nu als een technische opstelling, niet als een plek waar je thee wilt drinken.

**Sterk:** Het rotsgroepje rechts is echt overtuigend: drie verschillende natuursteen-assets met goede schaal, mos-verkleuring en contactschaduw op het grind — dat verkoopt de zentuin. · De houten deurpartij (redwood kozijn + panelen) contrasteert mooi met de antracietgrijze wanden en heeft geloofwaardige noerf en verstek. · De donkere strakke cabin met platte lessenaar-dak past qua stijl goed bij het japanese-zen concept.

**Problemen:**

- **🔴 BLOCKER · Vegetation** — Het gazon (hele voorgrond + zijkanten) is een uniform felgroen, kaarsrecht opstaand CG-grasveld zonder variatie in lengte, kleur of platgedrukte plekken. Het leest als groen tapijt/plastic en trekt alle aandacht weg van de hero. Dit is het grootste uncanny-valley-probleem.
  → *Fix:* Vervang/hercalibreer de grass-scatter: meng 2-3 grasclumps met variatie in hoogte (kort/middel), voeg clumping + wat gele/bruine sprieten toe, verlaag density iets, en zet een subtiele wind/tilt (Rotation randomization) zodat het niet als borstel rechtop staat. Voeg klavertje/onkruid-strooisel toe voor breuk in het uniforme groen.
- **🔴 BLOCKER · Dressing** — De open overkapping (midden) is vrijwel leeg en pikzwart van binnen: alleen een smalle bank tegen de achterwand en een vaag wit rond krukje/object linksvoor de vloer dat niet leesbaar is. De ruimte oogt kaal en dood i.p.v. een uitnodigende zen-veranda.
  → *Fix:* Kleed de overkapping aan met een lage tatami/zitkussen-set of een lage theetafel + kussens, een hangende papieren lantaarn of plant in pot, en licht de binnenruimte op met een zwakke warme area-light/emissive zodat het niet in het zwart wegvalt. Identificeer en verwijder of vervang het onleesbare witte ronde object linksvoor (lijkt placeholder).
- **🟠 MAJOR · Lighting** — De belichting is volkomen plat en grijs: geen richting, nauwelijks contactschaduwen behalve onder de rotsen, en de binnenkant van de overkapping is crushed black. Er is geen spoor van de gewenste volumetrische ochtend-haze of zacht strijklicht — het voelt als een dode overcast-testrender.
  → *Fix:* Behoud overcast maar geef richting: draai de zon/HDRI zodat er zacht strijklicht van rechts/achter komt, voeg een lichte volumetrische mist (Volume Scatter, lage density) toe voor diepte tussen bomen en cabin, en til de zwarten iets op met fill zodat de overkapping-binnenkant leesbaar wordt. AgX houden.
- **🟠 MAJOR · Vegetation** — De esdoorn linksboven heeft grotendeels kale/bruine takken met dunne, verdorde bladeren die als losse kaartjes tegen de wand hangen (zie schaduw op de linker cabin-wand) — leest als een half-dode boom, niet als weelderige Japanse esdoorn.
  → *Fix:* Vervang door een gezonde Japanse esdoorn-asset met dichte bladmassa (rood/groen), of verhoog het bladvolume en verwijder de kale skeletale takken. Controleer dat het geen <50k-verts kale tree-cluster is (hide_bare_trees.py-regel).
- **🟠 MAJOR · Backdrop** — De achtergrond-boomrij achter de heg (midden/rechts) bestaat uit een handvol losse, dunne, ijle naaldbomen met veel lucht ertussen — de hemel schemert overal doorheen, wat het 'zwevend eiland'-effect geeft en de scène ondiep maakt.
  → *Fix:* Verdicht de treeline: zet minimaal 2-3 ringen bomen achter de heg zodat de lucht wordt geoccludeerd, meng loof- en naaldbomen van verschillende hoogtes, en zorg dat de heg + bomen samen een gesloten groene achterwand vormen.
- **🟠 MAJOR · Composition** — De cabin staat vrijwel frontaal/plat in beeld en vult samen met de overkapping bijna de hele breedte; de dakrand raakt de bovenrand bijna (tangent) en er is geen leidende lijn (pad) naar de deur. Het geharkte grind loopt weg naar rechts i.p.v. het oog naar de hero te leiden.
  → *Fix:* Draai camera lichtjes voor meer 3/4-aanzicht op de cabin, zak/verplaats zodat er lucht-marge boven het dak komt, en leg een subtiel tredsteen-pad (stapstenen door het grind) dat vanaf de voorgrond naar de deur leidt. Zet camera op ooghoogte ~1.6m, ~35mm.
- **🟡 minor · Grounding** — De stenen lantaarn (midden-rechts) staat direct op het grind zonder duidelijke voetplaat of ingezonken basis en heeft een erg zwakke contactschaduw — hij lijkt licht op het grind te plakken i.p.v. erin te staan.
  → *Fix:* Zet de lantaarn op een platte fundatiesteen of laat de basis licht in het grind zakken, en versterk de AO/contactschaduw eronder.
- **🟡 minor · Materials** — De antracietgrijze wandpanelen ogen erg uniform en vlak; de horizontale plankvoegen zijn zichtbaar maar er is weinig noerf-variatie of subtiele slijtage, waardoor het richting egaal geverfd MDF neigt i.p.v. gebeitst hout.
  → *Fix:* Voeg subtiele per-plank kleurvariatie en een fijnere wood-grain normal/roughness toe, met lichte weathering onderaan de wand; controleer dat de noerf mét de plankrichting loopt (uv_board_textures FLAT).


## Lavendel — Pluktuin (boerderij, overcast) — **5/10**
*Vrolijke bloementuin met echte 3D-planten, maar de cabin staat te centraal-frontaal, het gras is een duidelijk getild/repeterend tapijt en het overkapping-deel plus de rozenboog ogen leeg en verkeerd geschaald — nog geen marketing-hero.*

**Concept/licht:** Het "pluktuin"-verhaal komt half over: de rijk gemengde border met hortensia's, rozen, vlinderstruik en rode bloemen leest wel als pluktuin, maar het "boerderij"-karakter ontbreekt vrijwel (geen rustieke props, moestuinbakken, gereedschap of landelijke details — alleen een maisveld op de achtergrond suggereert het). Het bedoelde OVERCAST-lichtmoment klopt qua zachte schaduwen, maar de lucht is te blauw en te zonnig-vrolijk; er is geen echte bewolkt-diffuse egaliteit en zeker geen volumetrische "licht-komt-erdoorheen"-sfeer. De lege overkapping met één zwevend-ogende tafel en de kale rozenboog zonder klimrozen ondergraven het verhaal.

**Sterk:** De bloemenborder bestaat uit echte 3D-assets (hortensia, rozen, vlinderstruik) met goede kleurvariatie en clustering — leest als een levendige pluktuin. · Het maisveld áchter de haag geeft een geloofwaardige boerderij-context en dieptelaag i.p.v. een leeg 'vliegend eiland'. · Zachte, richtingloze schaduwen passen bij een bewolkt lichtmoment; geen harde CG-slagschaduwen.

**Problemen:**

- **🔴 BLOCKER · Materials** — Het gras is een overduidelijk repeterend, opgetild grastapijt: over het hele voorterrein zie je herhalende plukken en een zichtbare naad/rand links-voor en midden-voor waar de grasvlakte 'zweeft' boven de grond. Het leest als een groene mat, niet als grond. Dit is direct diskwalificerend voor marketing.
  → *Fix:* Vervang het losse grasvlak door een GN-scatter van echte grassprieten over een goed gegronde ground-plane (subdivide + kleine displacement), meng 2-3 grasvarianten met random rotation/scale, en zorg dat de scatter-density naar de randen uitfadet zodat er geen harde naad is. Verwijder de zwevende mesh-rand.
- **🔴 BLOCKER · Composition** — De cabin staat vrijwel dead-center en frontaal-plat in het frame; de linkerzijde is een grote lege grasvlakte zonder interesse, terwijl alle dressing rechts geklonterd zit. Er is geen leidende lijn (pad) die het oog naar de deur brengt — het pad ligt volledig uiterst rechts en loopt wég van de cabin.
  → *Fix:* Draai de camera ~20-30° zodat de cabin een driekwart-hoek krijgt, plaats de cabin op een derde-lijn (iets naar links), en leg een klinker-/grindpad van de voorgrond richting de dubbele deur zodat het oog geleid wordt. Vul de lege linkervoorgrond met een border-uitloper of een enkele struik voor foreground-framing.
- **🟠 MAJOR · Vegetation** — De rozenboog (rechts-midden) is volledig kaal metaal zonder klimrozen of enig groen — hij leest als een leeg zwart frame dat nergens naartoe leidt en staat los in het gras. Bovendien snijdt hij de bloemenborder visueel doormidden.
  → *Fix:* Scatter echte klimroos-/klimplant-geometrie over de boog (GN curve-instance of handmatig gedrapeerd blad+bloem), of verwijder de boog en zet er een gevulde border of pergola-met-begroeiing neer. Verplaats hem zodat hij een doorgang markeert i.p.v. midden in een border te staan.
- **🟠 MAJOR · Scale** — De tafel onder de overkapping (rechts) oogt te klein/te ondiep en lijkt licht te zweven — de contactschaduw met de vloer is zwak, en de overkapping-ruimte is verder helemaal leeg (geen stoelen, geen dressing), waardoor het als een onbenutte carport oogt i.p.v. een zithoek.
  → *Fix:* Vervang/schaal de tafel naar realistische ~75cm hoogte en zet er 2-4 echte tuinstoelen bij; voeg AO/contactschaduw toe (check dat de poten de vloer raken). Kleed de overkapping aan met een plant in pot, een lantaarn of een bankje zodat de ruimte een functie krijgt.
- **🟠 MAJOR · Lighting** — Het lichtmoment is als 'overcast' bedoeld maar de lucht toont een fel blauwe hemel met zonnige highlights op het dak en de haag; er is geen diffuse bewolkt-egaliteit en geen volumetrische ochtendnevel-haze. Het beeld voelt daardoor plat-zonnig i.p.v. sfeervol bewolkt.
  → *Fix:* Wissel naar een echte overcast HDRI (egale grijs-witte lucht, lage zon-contrast) of temper de zonsterkte en verhoog de sky-diffusie; voeg een lichte volumetrische mist-laag toe (Volume Scatter, lage density) voor de 'licht-komt-erdoorheen'-look, en behoud AgX voor zachte highlight-rolloff.
- **🟡 minor · Uncanny** — De cabin oogt fabrieksnieuw en te perfect: smetteloos licht hout zonder enige verwering, nerf-variatie of vuil aan de onderrand, en de dakrand is strak-schoon. Dit versterkt het CG-plastic gevoel, zeker naast de levendige planten.
  → *Fix:* Voeg subtiele verweer/vuil toe aan de onderste plankrand (dirt-mask via AO of vertex paint), lichte kleur-/nerfvariatie per plank, en een minieme roughness-variatie zodat het hout niet uniform egaal reflecteert.
- **🟡 minor · Grounding** — De bloemclusters (hortensia's, rode bloemen) staan op een egaal grastapijt zonder plantvak, mulch of aarde eronder — ze lijken direct in het gras geprikt, wat de pluktuin-border minder geloofwaardig maakt.
  → *Fix:* Leg onder de borders een smalle strook donkere aarde/mulch-mesh met lichte displacement, en laat het gras aan de border-rand uitfaden zodat de planten in een echt bed staan i.p.v. in gazon.


## Lelie — Ochtendnevel (forest-wilderness) — **5/10**
*De mistsfeer en bos-backdrop zitten goed, maar een verpletterende roze/paarse waas over het hele beeld en een levenloze, plat-belichte cabin trekken dit van "sfeervol" naar "kapotte white-balance".*

**Concept/licht:** Ten dele. Het BOS + ochtendmist-verhaal komt echt over: dichte dennen-treeline die de lucht occludeert, atmosferische diepte-lagen en een dromerige waas — precies het "licht-komt-erdoorheen"-doel dat deze scene als referentie moet dienen. MAAR de kleur klopt niet: alles baadt in een uniforme roze/magenta gloed (de mist zelf is roze, de cabin is roze, het gras is verzadigd zuurgroen eronder). Dageraad-mist is koel-neutraal met een warme zon-kern, niet monochroom roze. En de cabin — de eigenlijke hero — is dood plat belicht zonder duidelijke zonrichting, dus het "licht komt erdoorheen"-moment mist juist op het belangrijkste object.

**Sterk:** Overtuigende dichte dennen-treeline die de lucht occludeert met echte atmosferische diepte (voor/midden/achter-lagen + berg-silhouet rechts) — geen 'vliegend eiland'. · De volumetrische mist zelf is geloofwaardig gelaagd en geeft echte dieptewerking, precies het referentie-effect dat deze scene moet leveren. · De stapstenen rechts vormen een nette leading line en de rots als focal point in de voorgrond geeft schaal en voorgrond-interesse.

**Problemen:**

- **🔴 BLOCKER · Lighting** — Het HELE beeld heeft een uniforme roze/magenta waas — de mist is roze, de cabin-wand is roze, zelfs de schaduwzijde. Dit leest als een kapotte white-balance / verkeerd gekleurde volume- of zonkleur, niet als dageraad. Dageraad-mist hoort koel-neutraal grijsblauw te zijn met alleen een warme zon-kern.
  → *Fix:* Zet de World/volume-scatter kleur terug naar (bijna) neutraal grijsblauw i.p.v. roze. Verlaag de saturatie van het zonlicht (Sun color naar warm-wit ~5500-6000K, niet magenta). Check de compositor: een Color Balance/Mix-node met roze tint eroverheen weghalen. Doel: koele mist, warme zon-kern — niet monochroom roze.
- **🔴 BLOCKER · Lighting** — De cabin (de hero) is compleet plat belicht: voor- en zijwand hebben nagenoeg dezelfde helderheid, er is geen duidelijke zonrichting, geen warme highlight-kant vs koele schaduw-kant. Het 'licht-komt-erdoorheen'-moment mist juist op het belangrijkste object. Ook geen zichtbare grondschaduw onder de cabin/overkapping.
  → *Fix:* Roteer de Sun tot een lage dageraad-hoek (elev ~8-15°) die duidelijk van links-achter of rechts-achter komt, zodat één cabin-vlak oplicht en het andere in koelere schaduw valt. Verhoog sun strength iets zodat er een echte warme kant + slagschaduw ontstaat. Voeg een god-ray/volumetric shaft toe die langs de cabin strijkt.
- **🟠 MAJOR · Vegetation** — Het gras is een uniforme, verzadigd zuurgroene mat met korte, gridderige sprietjes en zonder variatie of kale plekken — CG-perfect en te felgroen onder een mistige dageraad, wat botst met de gedempte achtergrond. In de voorgrond staan bloemen (rood/roze) los in het gras verspreid zonder clustering.
  → *Fix:* Verlaag grass base-color saturation en helderheid (mist dempt kleur — mistige ochtend = grijzig-groen, niet neon). Voeg lengte-/kleurvariatie en wat aarde/kale plekken toe via een noise-mask op de scatter-density. Cluster de bloemen in 2-3 pollen i.p.v. gelijkmatig verstrooid, en dim ook hun verzadiging in de mist.
- **🟠 MAJOR · Materials** — De cabin-wandtextuur ziet er extreem strak/nieuw uit met heel lichte, bijna uniforme houtkleur en weinig grain-contrast; op deze afstand leest het vlak en plastic-achtig. Het dak (witte rand) is nagenoeg wit uitgeblazen. Geen enkele wear/vuil/verwering — CG-schoon.
  → *Fix:* Verhoog het contrast/detail in de hout-albedo en voeg een subtiele roughness- en bump-variatie toe (grain, lichte vlekken). Temper de witte dakrand (verlaag albedo of exposure) zodat hij niet clipt. Voeg lichte verwering/AO in de plank-naden toe voor realisme.
- **🟠 MAJOR · Composition** — De cabin staat vrijwel frontaal en midden-links met een erg vlakke, symmetrische aanblik; de rechter carport/overkapping is een donker leeg gat dat niets doet. De grote rots zit pal vóór de deur en blokkeert de entree/leading line naar de deur — de stapstenen leiden juist WEG naar rechts i.p.v. naar de deur.
  → *Fix:* Draai de camera iets zodat de cabin op 3/4-hoek staat (meer diepte in de zijwand). Verplaats de rots uit de deur-as (naar links-voor als repoussoir) zodat het pad + zicht vrij naar de deur leidt. Dress de lege overkapping rechts met bijv. brandhout-stapel of een stoel zodat het geen zwart gat is.
- **🟡 minor · Backdrop** — Links op de middengrond staat een strook lichte, kale grond/pad achter de cabin die als een harde lichte band door het bos snijdt en de mist-illusie doorbreekt; ook rechts-achter een vergelijkbare lichte veeg.
  → *Fix:* Verleng de mist-densiteit/depth-fade zodat die lichte grondstroken wegvagen in de nevel, of scatter er laag struikgewas/varens overheen zodat er geen harde lichte band door de treeline loopt.
- **🟡 minor · Grounding** — De losse stapstenen rechts liggen bovenop het gras zonder ingezonken contactschaduw en met een lichte glans, waardoor ze eerder op het gras lijken te zweven dan erin te liggen.
  → *Fix:* Zink de stenen licht in, voeg AO/contactschaduw en wat overgroeiend gras langs de randen toe, en verlaag hun specular/roughness zodat ze niet glimmen in de mist.


## Zonnebloem — Ochtendhoek (scandi) — **5/10**
*Het beeld verkoopt een leuke Scandi-koffiehoek, maar het gras is spikey/plastic en de cabin staat te vlak-frontaal in beeld — nog niet marketing-klaar.*

**Concept/licht:** Half. De open overkapping met twee leren fauteuils, bijzettafel, cafetière en lavendel leest wél als een rustige koffiehoek, dus het Scandi-verhaal komt op meubelniveau over. Het bedoelde "frisse ochtend"-lichtmoment ontbreekt echter grotendeels: de lucht is dof paars-roze, er is geen lage warme scheerzon en geen volumetrische ochtendnevel/"licht-komt-erdoorheen"-gloed. Het voelt eerder als een kleurloze schemer dan als een frisse ochtend, waardoor de emotionele belofte van de scene niet landt.

**Sterk:** De meubelset (twee leren loungefauteuils + rond bijzettafeltje + cafetière) onder de overkapping is geloofwaardig en past bij de Scandi-koffiehoek · Terracotta-pot met plant links van de fauteuils en het lavendelveld rechts geven kleuraccent en midground-diepte · Het houten vlonderdek onder de overkapping oogt netjes en verankert de zithoek visueel

**Problemen:**

- **🔴 BLOCKER · Vegetation** — Het gazon (hele voorgrond + zijkant, zie GAZON-crop) bestaat uit losse, rechtopstaande, egaal-groene spikes op kale bruine grondvlekken — leest als plastic/CG-gras, niet als een echt Nederlands gazon. Er zit geen variatie in bladlengte, geen liggende sprieten en geen klaver/onkruid.
  → *Fix:* Vervang de huidige grass-scatter door een gelaagd Geometry-Nodes-gazon: minstens 2-3 grass-clump-assets uit assets/polyhaven/ mengen, density fors omhoog zodat de bruine grond dichtslaat, random scale (0.6-1.4) + random tilt (tot 35°) voor liggende sprieten, en 5-10% kruidjes/klaver door de mix voor breuk in de uniformiteit.
- **🟠 MAJOR · Composition** — De cabin staat vrijwel vlak-frontaal en centraal in het frame; de linker zijwand en de front lopen bijna recht op de camera. Er is geen leidende lijn (pad) naar de deur, de compositie is statisch en de dode voorgrond (onderste derde is puur gras) voegt niets toe.
  → *Fix:* Draai de camera ~15-25° naar een driekwart-hoek zodat front én zijwand samen diepte geven, zet camera op ooghoogte 1.6-1.7m met ~35mm, en leg een klinker-/tegelpad (cabin_lib klinker_strip) vanaf de rechter-onderhoek naar de dubbele deur als leidende lijn. Verklein de lege gras-voorgrond.
- **🟠 MAJOR · Lighting** — Het licht is vlak en koel-dof: paars-roze lucht, nauwelijks richtingsschaduwen behalve één vage boomschaduw op de linker zijwand. Geen lage warme zon, geen ochtendnevel, geen gloed — het beoogde 'frisse ochtend'-moment ontbreekt volledig.
  → *Fix:* Zet een lage warme zon (elevation ~8-12°, 4500-5500K) schuin van rechts-achter zodat de overkapping en meubels warm worden aangelicht en er lange schaduwen over het gazon vallen. Voeg een lichte volumetrische mist toe (Volume Scatter, density laag) voor de 'licht-komt-erdoorheen'-haze, en check AgX zodat de lucht niet dof-paars wegzakt.
- **🟠 MAJOR · Backdrop** — De boom-backdrop is een dunne rij losse dennen met veel open lucht ertussen (bovenrand hele breedte) — de sky wordt niet geoccludeerd, waardoor het als een 'vliegend eiland' achter de heg oogt. De heg is een strakke egale groene balk zonder dieptevariatie.
  → *Fix:* Plaats minstens 2-3 ringen bomen achter de cabin zodat de tree-line de lucht dichtzet en er geen gaten meer zijn; varieer boomsoort/hoogte. Geef de heg volume met een GN-scatter van echte shrub-blaadjes (outward normals) i.p.v. een vlakke muur, en breek de bovenkant licht onregelmatig af.
- **🟠 MAJOR · Grounding** — Rechts staat een plukje lavendel dat op zwevende/losse pollen lijkt zonder duidelijk grondcontact of AO-schaduw; de terracotta-pot en de fauteuils hebben nauwelijks contactschaduw waardoor ze licht boven het dek/gras lijken te hoveren.
  → *Fix:* Verlaag lavendel-, pot- en meubelobjecten tot ze de grond/dek net snijden en bak sterkere contact-AO (of voeg kleine ambient-occlusion-shadow-catchers toe). Cluster de lavendel dichter met random rotatie zodat het als één border leest i.p.v. losse plukjes.
- **🟡 minor · Materials** — De front-wandpanelen (rond en boven de deur) tonen zichtbare rechthoekige naad-/tegelblokken en een licht schaakbord-achtige toon-variatie tussen panelen — de plankstructuur oogt onrustig en deels als box-projectie i.p.v. doorlopend hout.
  → *Fix:* Controleer de UV-richting van de wandpanelen met cl.uv_board_textures() (UV+FLAT) zodat de nerf overal met de plank meeloopt, en verminder de per-plank kleur/roughness-variatie zodat het geen schaakbordpatroon geeft.
- **🟡 minor · Uncanny** — Klimplantjes/rankjes op de dubbele deur (front) ogen als losse platte sprietjes die uit het niets omhoog komen; ze hebben geen wortel/pot en klimmen nergens tegenaan, wat kunstmatig oogt.
  → *Fix:* Verwijder de zwevende rankjes of vervang ze door één echte klimplant-asset die vanuit een bakje/pot bij de deurstijl opgroeit, met grondcontact.


## Lavendel — Lavendelveld (mediterraan, golden hour) — **5.5/10**
*Sterk basisbeeld met echte props en een mooie treeline, maar het "golden hour" ontbreekt volledig (koud, plat avondlicht), het gras is een uniform CG-tapijt en het lavendelveld staat gek genoeg alleen rechts — het verhaal wordt maar half verkocht.*

**Concept/licht:** Half. De cabin, buxusbollen in terracotta en de overkapping zien er geloofwaardig mediterraan uit, maar het kernconcept "lavendelveld" komt niet over: lavendel staat alleen als losse pol rechts en rechts-onder, terwijl links en het hele midden-voorgrond kale groene grasvlakte zijn. Het bedoelde lichtmoment (golden hour) is er totaal niet — het licht is koel, grijs-blauw en plat, meer bewolkte schemering dan warme gouden zon. Zonder warm strijklicht en zonder een echt vééld lavendel verkoopt het beeld noch de sfeer noch het verhaal.

**Sterk:** Echte 3D-props: buxusbollen in terracotta potten, bistro-set en de treeline zijn volumetrisch en geen kaartjes · De achtergrond-treeline occludeert de lucht netjes met een maisveld/heg als middenlaag — geen zwevend-eiland effect · De overkapping met doorkijk naar de bistro-set geeft diepte en een geloofwaardig mediterraan terras-idee

**Problemen:**

- **🔴 BLOCKER · Lighting** — Het bedoelde golden hour ontbreekt compleet. Het hele beeld is koel grijs-blauw en plat: de cabin-wand toont geen warm strijklicht, er zijn nauwelijks lange schaduwen, en de lucht is een dof grijs verloop. Dit leest als bewolkte schemering, niet als gouden uur.
  → *Fix:* Zon-object naar lage hoek (~5-8 graden boven horizon) uit camera-links-achter zetten, kleur naar warm (2800-3200K, oranje-amber), strength omhoog. HDRI vervangen door een golden-hour sky. Volumetrische haze toevoegen (Volume Scatter in world of een grote cube) voor Beike's 'licht-komt-erdoorheen' look. AgX view transform bevestigen. Lange warme slagschaduwen van cabin/potten over het gras naar rechts.
- **🔴 BLOCKER · Vegetation** — Het 'lavendelveld' bestaat niet als veld. Lavendel staat alleen als losse pol rechts (midden-rechts) en een cluster rechts-onder. Het hele midden en de linkerhelft van de voorgrond zijn kaal groen gras. Voor een scene die 'Lavendelveld' heet is dit een concept-failure.
  → *Fix:* Lavendel-scatter (GN of particle) uitbreiden tot echte stroken/rijen die door het midden en links lopen, richting de camera aflopend als leading lines naar de deur. Variatie in hoogte/dichtheid, in banen geplant (mediterrane pluktuin-rijen) i.p.v. losse plukjes rechts.
- **🟠 MAJOR · Materials** — Het gras is een uniform CG-tapijt: overal exact dezelfde sprietlengte, kleur en dichtheid, zonder plekken, paadjes-slijtage, aardevlekken of kleurvariatie. In de voorgrond zie je herhaling/tiling. Dit is een klassieke uncanny-valley 'te perfect gras'.
  → *Fix:* Kleur- en lengtevariatie via noise-texture op de scatter density + hue/value. Dode/gele plekken en aarde-doorkijk toevoegen. Tweede, kortere grassoort mengen. Voorgrond-tiling breken met een grote noise-mask op de density.
- **🟠 MAJOR · Composition** — De cabin staat vrijwel plat frontaal en bijna dead-center; er is geen pad dat het oog naar de deur leidt. De terracotta potten staan pal vóór de deur en blokkeren juist de entree. De horizon zit precies op het midden.
  → *Fix:* Camera iets naar links/rechts draaien voor een driekwart-hoek zodat de cabin-hoek diepte krijgt. Een terras-/klinkerpad of lavendel-lane als leading line naar de deur leggen. Potten iets opzij schuiven zodat de deur vrij is. Horizon naar het bovenste derde brengen (camera iets omlaag/kantelen).
- **🟠 MAJOR · Lighting** — De open overkapping rechts is een dode donkere grot: de vloer en achterwand onder het dak zijn egaal donker/plat zonder enig invullicht of warme reflectie, waardoor de bistro-set half in het zwart verdwijnt.
  → *Fix:* Zwak warm fill-light (area light) onder de overkapping plaatsen, of bounce verhogen. Vloer-materiaal lichter/warmer maken. Zorg dat de stoel/tafel contactschaduwen en wat rim-light krijgen zodat de ruimte leest als uitnodigend terras.
- **🟡 minor · Grounding** — De buxusbollen en potten staan wel op het gras maar hebben nauwelijks contactschaduw/AO; ze lijken licht op het gras te 'zweven'. Ook de bistro-tafelpoot mist een duidelijke schaduw op de terrasvloer.
  → *Fix:* AO/contactschaduw versterken, gras rond de potvoet iets platdrukken of een klein donker contact-gradient toevoegen. Zon-schaduwen inschakelen zodra golden-hour zon staat lost dit deels vanzelf op.
- **🟡 minor · Materials** — De cabin-wand oogt egaal en vlak — weinig zichtbare houtnerf-richting of variatie tussen planken, en de wand is bijna smetteloos schoon zonder enige verwering. Dat maakt de gevel wat plat/CG.
  → *Fix:* Controleer dat de wand-UV met de plank meeloopt (cl.uv_board_textures FLAT), voeg subtiele roughness- en kleurvariatie per plank toe en lichte verwering/vuil onderaan de wand voor realisme.


## Roosmarijn — Kruidenterras (mediterraan, kruiden/koken, namiddag) — **5.5/10**
*Nette basis met een charmante overkapte kruidenterras, maar het licht is vlak-middags i.p.v. warme namiddag en het hout is overal knalnieuw-blank waardoor het beeld CG en niet echt mediterraan aanvoelt.*

**Concept/licht:** Half en half. De overkapte hoek met bistrotafel, terracottapotten en kruidenbakken links leest wel als een gezellig eet-/kruidenplekje, maar het "koken/kruiden"-verhaal is zwak: er is geen enkele keukenreferentie (kruidenschaaltjes, snijplank, olijfolie, hangende kruidenbossen) en de beplanting oogt als willekeurige struiken i.p.v. herkenbare keukenkruiden. Het bedoelde NAMIDDAG-licht ontbreekt: de zon staat te hoog en te neutraal, schaduwen zijn kort, en de lage warme mediterrane gloed + volumetrische haze die Beike overal wil is er niet.

**Sterk:** De overkapte terrashoek met feestverlichting, bistroset en terracottapotten vormt een geloofwaardig, uitnodigend mediterraan zithoekje · Echte 3D-beplanting (boompje, kruidenbakken, potplanten) staat overtuigend geclusterd, geen flat cards · De haag op de achtergrond loopt door en occludeert de horizon links en rechts van de cabin, geen zwevend eiland

**Problemen:**

- **🔴 BLOCKER · Lighting** — Het bedoelde NAMIDDAG-licht ontbreekt volledig: schaduwen onder de bistroset en potten op het terras zijn kort en steil, de kleurtemperatuur is neutraal-koel, en er is nul volumetrische haze. Het hele beeld leest als vlakke middagbelichting, niet als lage warme mediterrane namiddag.
  → *Fix:* Zet de zon lager (elevation ~12-18 graden) en warmer (blackbody ~4000-4500K), draai hem naar links-achter zodat er lange schaduwen over terras en gras vallen. Voeg een lichte volumetrische World/Principled Volume haze toe (density ~0.002-0.005) voor de light-comes-through gloed. Behoud AgX.
- **🔴 BLOCKER · Materials** — Al het cabinehout (voorwand links, deur, binnenwand overkapping) is uniform knalwit-blank en veel te licht/verzadigingsloos. Het oogt als onbehandeld vers vuren onder studioverlichting, niet als warm mediterraan hout. Dit is de grootste realisme-killer en maakt de cabin plat en CG.
  → *Fix:* Geef het hout een warmere basiskleur (richting honing/licht-eiken), verhoog roughness variatie en voeg subtiele grain/dirt/AO in de naden toe. Overweeg lichte verwering aan de onderrand. Zeker onder de overkapping mag het hout donkerder en warmer ogen.
- **🟠 MAJOR · Grounding** — De twee betonnen/witte terrasplaten drijven boven het gras: er is een zichtbare naad/gat tussen de deurplaat en de grote terrasplaat (midden-voor), de platen hebben een dikke zwevende rand en missen contactschaduw/AO naar het gras. Ze zien eruit als losse zwevende dienbladen.
  → *Fix:* Zak de platen ~1-2cm in het gras, sluit de naad tussen beide platen (of maak er 1 doorlopend vlak van), en voeg contact-AO + een randje gras/aarde-overgang toe. Dun de zichtbare plaatrand uit of verberg hem met beplanting.
- **🟠 MAJOR · Composition** — De cabin staat vrijwel frontaal/plat en centraal, en er is geen leidende lijn (geen pad) naar de deur. De deur-terrasplaten liggen als losse eilanden in leeg gras; de hele onderste helft van het frame is leeg groen voorgrond zonder verhaal. Geen duidelijke voorgrond-laag.
  → *Fix:* Draai de camera iets meer 3/4 zodat de zijwand en overkapping meer diepte krijgen, en leg een klinker/grind-pad of stapstenen aan dat vanaf de onderrand naar de deur leidt. Vul de lege voorgrond met een kruidenpluk, wat losse potten of een lage border.
- **🟠 MAJOR · Dressing** — Het kern-concept (kruiden/koken) is niet aanwezig op de terras. Er staat alleen een lege bistroset en een boompje midden op het terras dat het zicht op de tafel blokkeert. Geen kookrekwisieten, geen herkenbare kruidenpotjes op tafel, en het boompje botst bijna tegen de overkappingswand.
  → *Fix:* Verplaats/verklein het boompje uit het zichtcentrum, en dress de tafel/terras met kruidenrekwisieten: terracotta kruidenpotjes (basilicum/rozemarijn/tijm), een snijplank, olijfoliefles, hangende gedroogde kruidenbossen aan de overkapping. Zet de kruidenbak dichter bij de eethoek voor het pluk-verhaal.
- **🟡 minor · Vegetation** — De bomenrij achter de haag bestaat uit dunne, kale/naaldarme dennenstammen die als silhouetten tegen de lucht schrale skeletten vormen, vooral rechtsboven. Het gras is een egale, tegelachtig-uniforme groene mat zonder variatie of pluk-hoogte.
  → *Fix:* Vervang/verdicht de achtergrondbomen met vollere kronen (of extra ring loofbomen) zodat ze niet als kale stammen tegen de lucht steken. Breek het gras op met color/height-variatie en wat losse pollen/onkruid voor een minder CG-perfecte mat.
- **🟡 minor · Materials** — Het glas in de deur (midden-links) is dof/vlak en mist reflectie of transparantie-diepte, waardoor het als grijze plaat oogt en de deur goedkoop maakt. De feestverlichting-bolletjes zijn puur wit zonder emissie-gloed in de namiddag.
  → *Fix:* Geef het deurglas lichte roughness + reflectie/omgevingsspiegeling en een vleugje transmissie. Geef de lampjes een warme emissieshader (blackbody ~2700K, lichte bloom in compositing) zodat ze bij de namiddagsfeer passen.
