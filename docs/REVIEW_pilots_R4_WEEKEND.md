# QC-review R4-pilots — weekendrun (10 jul 2026)

**Wat dit is.** Een autonoom in het weekend gegenereerde *technische* QC van alle 13 R4-pilotscènes, bedoeld als startpunt voor Beikes R4-review op Fable 5. De diagnose komt uit 13 analyse-agents (probe-data + beeld-crops per scène).

**Belangrijk — geen fixes toegepast.** Dit is puur diagnose. Er is niets aangepast, niets gecommit, niets gerenderd als final. Alle genoemde fixes zijn *voorstellen* voor Beike om per stap te sturen.

**3 scènes zijn getrouwe R4-rebuilds** (uit de 2-jul libs) op lage preview-resolutie: `magnolia_wintertuin`, `zonnebloem_zomeravond`, `zonnebloem_ochtendhoek`. Hun eindoordeel ("goed genoeg als R4?") ligt bij Beike — de QC hieronder is technisch, niet het laatste woord.

**Telling over alle 13 scènes:** 3 blockers · 26 high-severity punten.

---

## 1. Overzichtstabel

| Scène | Techn. OK | #blockers | #high | Stand (1 regel) |
|---|:---:|:---:|:---:|---|
| camelia_buitenbad | ✓ | 0 | 2 | Sterke avond-hero; gele HDRI-vlek + uitstekend hot-tub-deck zijn de twee hoofdpunten |
| camelia_wijnterras | ✓ | 0 | 1 | Technisch schoon (~6,5); bistroset staat in gras i.p.v. op terras, terras + afdak leeg |
| dahlia_tuinkantoor | ✓ | 0 | 3 | Tuinkantoor-verhaal ontbreekt (geen bureau) + cabin "staat random" in kaal grasveld |
| dahlia_leeshoek | ✓ | 1 | 1 | Dichtst bij klaar (~7); rooibos-textuur is landmine, mood + afwerking resteren |
| jasmijn_theehuis | ✓ | 1 | 2 | Grindterras rendert als vlakke betonplaat (textuur weg) + losse aankleding |
| jasmijn_familietuin | ✓ | 0 | 3 | Beste licht van de reeks; reuzenschep, zwevende zandbak, uitstekende bay-vloer |
| lavendel_pluktuin | ✓ | 0 | 3 | Techniek prima (~5,5); gras over verharding, grond leest als beton, vlak grijs licht |
| lavendel_lavendelveld | ✓ | 0 | 2 | Warme mist top; "lavendel" als losse pollen in te-groen gazon, deur geblokkeerd |
| lelie_ochtendnevel | ✓ | 0 | 3 | Plankenpad zweeft, backdrop-banding rechts, te grote rots dood vóór de deur |
| lelie_avondkubus | ✓ | 0 | 2 | Deurgloed werkt; heg blokkeert zichtlijn, gras over stenen, rechter glasvlak dood |
| magnolia_wintertuin | ✓ (rebuild) | 0 | 1 | REBUILD; sterke hero, dekrand zweeft, seizoenskeuze winter/lente open (Beike) |
| zonnebloem_zomeravond | ✓ (rebuild) | 0 | 2 | REBUILD (~6,5); GEEN zonnebloemen, lichtsnoer dood, geen pad naar de deur |
| zonnebloem_ochtendhoek | ✗ (rebuild) | 1 | 1 | REBUILD, technisch NIET OK; Deur_Stoep-grind weg → vlakke grijze plaat |
| **Totaal** | **12/13** | **3** | **26** | |

*Blocker = technische landmijn die vóór een final gefixt moet (missende textuurbestanden of `technical_ok=false`). Deze tellen ook mee in #high wanneer ze high-severity zijn.*

---

## 2. Systemische bevindingen (het waardevolste deel)

Patronen die over meerdere scènes terugkomen, van meest structureel naar cosmetisch.

### S-A · Missende / kwetsbare texturen — migratie-erfenis  → **oorzaak van alle 3 blockers**
De C:→D:-migratie en oude temp-mappen hebben texturen losgekoppeld. Twee scènes delen letterlijk hetzelfde weesbestand.
- **`T_vl0mfbllw_8K_B/_N.png`** (construction_gravel / path_stones) ontbreekt in **jasmijn_theehuis** én **zonnebloem_ochtendhoek** → grind valt terug op een vlakke grijze plaat. Fix: relink/pack, of de al-bestaande R4-fix overnemen (AmbientCG PavingStones125A, in de blend gepakt).
- **`wild_rooibos_bush_*`** (4 files) ontbreekt in **dahlia_leeshoek** → nu buiten beeld (landmine): zodra de scatter/crop verschuift rendert hij magenta/alpha-loos.
- **Latente paden**: **dahlia_leeshoek** verwijst naar 11 texturen in `AppData/.../Temp/tmp*` + oude `C:/Users/...`-paden; **magnolia_wintertuin** draagt nog de `aerial_grass_rock`-referentie (de textuur die eerder witte rotsvlekken door het gras gaf).
- **Actie:** vóór elke final `File > External Data > Pack` of remap naar `assets/` op D:.
- **Getroffen:** jasmijn_theehuis, zonnebloem_ochtendhoek, dahlia_leeshoek, magnolia_wintertuin.

### S-B · Verankering — Beike's #1 "staat er random"  → **breedst gedeelde kunst-punt**
Pad ontbreekt of leidt nergens heen; props/verharding liggen los op het gras; borders zonder ingesneden bed/mulch. Terugkerend advies: verzonken leading-line-pad van voorgrond-onderhoek naar de deur + border-/grind-randen langs verharding.
- **Getroffen:** vrijwel alle 13 — het scherpst bij **dahlia_tuinkantoor**, **jasmijn_theehuis**, **lavendel_lavendelveld**, **lelie_ochtendnevel**, **zonnebloem_zomeravond**, **zonnebloem_ochtendhoek** (geen pad naar de deur); en **camelia_wijnterras** (hero-bistroset staat in het gras i.p.v. op de tegels).

### S-C · Gras-door-verharding / hardscape zweeft op grastoppen (S3)
Gras-mask niet strak om de verharding gesneden; tegels/planken/decks liggen bovenop de sprieten i.p.v. 1-2 cm verzonken. Standaardfix: `apply_r4` mask-cell 0.22 rond de footprint + verharding verzinken + vuil/AO-randje.
- **Getroffen:** camelia_buitenbad, camelia_wijnterras, dahlia_tuinkantoor, dahlia_leeshoek, jasmijn_theehuis, jasmijn_familietuin, lavendel_pluktuin, lavendel_lavendelveld, lelie_ochtendnevel, lelie_avondkubus, magnolia_wintertuin, zonnebloem_zomeravond, zonnebloem_ochtendhoek.

### S-D · Vlakke roze-paarse dawn-waas zonder zonrichting (S4)
Alle gevels even licht, geen oplichtende/schaduwgevel, geen slagschaduwen. Referentie dat het beter kan: **jasmijn_familietuin** (echte zon + tak-schaduwen). Standaardfix: zon laag (elev 8-15°, 3500-4500K, energy 3-5), azimut zo dat één gevel oplicht.
- **Getroffen:** dahlia_tuinkantoor, dahlia_leeshoek, jasmijn_theehuis, lelie_ochtendnevel, zonnebloem_ochtendhoek; verwant grijs-overcast bij lavendel_pluktuin.

### S-E · Uniform "borstel-tapijt" gras (S1)
Elke spriet even hoog/even fel groen/recht omhoog; het duidelijkste CG-signaal. Standaardfix: `scripts/grass_lib.py` — 2-3 clump-varianten, random scale 0.6-1.4, tilt tot ~30°, ColorRamp 3 groentinten + 5-8% droog/geel, density-noise.
- **Getroffen:** camelia_buitenbad, camelia_wijnterras, dahlia_tuinkantoor, dahlia_leeshoek, jasmijn_theehuis, lavendel_pluktuin, lavendel_lavendelveld, lelie_ochtendnevel, lelie_avondkubus, zonnebloem_zomeravond, zonnebloem_ochtendhoek.

### S-F · Dode practicals / lege overkapping-bay (S2)
Lantaarns en lichtsnoeren staan uit (dof wit plastic); de open bay is een donker/leeg gat. Standaardfix: emissie 2200-2700K + kleine warme point; zwakke warme area-fill (10-20 W, `use_shadow=False`).
- **Getroffen:** camelia_buitenbad, camelia_wijnterras (festoon), dahlia_leeshoek, jasmijn_theehuis, lavendel_lavendelveld, lelie_ochtendnevel, lelie_avondkubus (rechter glas), zonnebloem_zomeravond (lichtsnoer), zonnebloem_ochtendhoek.

### S-G · Uitstekende auto-vloer onder de overkapping
De toegevoegde bay-vloer steekt buiten de gevel/dakrand uit of loopt het beeld uit. NB: bij de meeste scènes blijft de vloer nu wél netjes binnen de footprint (bevestigd).
- **Getroffen:** camelia_buitenbad (hot-tub-deck), jasmijn_familietuin (voorrand + funderingslat), lavendel_pluktuin (apron steekt ver het gazon in).

### S-H · Concept-signaal ontbreekt (naam ≠ inhoud)
- **zonnebloem_zomeravond**: geen enkele zonnebloem in beeld.
- **lavendel_lavendelveld**: "lavendel" staat als losse pollen, geen veld/rijen.
- **magnolia_wintertuin**: seizoenskeuze winter/vroege-lente nog open (voorgrond zomergroen, achtergrond golden veld) — **beslissing bij Beike**.

### S-I · Gekleurde HDRI-vlek in de boomlijn
Warme zon-hotspot prikt door het bladerdek. Fix: HDRI ~20-40° draaien of gat dichtzetten met donker boom-silhouet.
- **Getroffen:** camelia_buitenbad (gele vlek — reeds door Beike aangemerkt), lelie_ochtendnevel (roze waas + harde horizon-banding), lelie_avondkubus (oranje light-leak links).

### S-J · Probe-floaters zijn grotendeels vals-positief
De `possible_floaters` uit de probe zijn bij kruis-check meestal geen echte zwevers: lantaarn-handles, props op een verhoogd dek, en boombladermassa achter de heg. Niet achterna jagen tenzij visueel bevestigd.
- **Bevestigd vals-positief bij:** camelia_buitenbad, camelia_wijnterras, dahlia_tuinkantoor, dahlia_leeshoek, jasmijn_theehuis, magnolia_wintertuin, zonnebloem_zomeravond/ochtendhoek. **Wél echte grounding-punten:** jasmijn_familietuin (zandbak-frame zweeft).

---

## 3. Per scène

Issues gesorteerd op severity (blocker/high eerst). `[B]` = blocker.

---

### camelia_buitenbad — techn. OK ✓ · 0 blockers · 2 high
Technisch schone avond-render; hero (cabin + verlichte deur + doorkijk + premium hot tub) leest sterk.

- **HIGH · hdri-vlek** — Links door de bomen gloeit een felle geel-groene lichtvlek (zonsondergang-HDRI door het bladerdek) + roze/rood vlekje erboven; exact Beike's "gele vlek weg" (review 8 jul). Geen kapotte textuur. → HDRI-rotatie zodat de hotspot niet achter de boomsilhouetten valt, of bomenrij dichter/hoger, of donkere tree-card achter het gat.
- **HIGH · vloer-onder-overkapping** — Donkere houten deck-slab (auto-vloer) steekt vóór/rechts buiten de gevel uit en loopt het beeld uit; zichtbare naad tussen grijze binnenvloer en warm buitendeck. → Deck terugtrimmen tot begrensde terrasvorm, rand afwerken met border/trim, materialen op elkaar afstemmen.
- MEDIUM · verankering — Hot-tub-deck staat met harde opstap los op het gazon; linker beeldhelft grote lege felgroene lawn. → Deck-rand verankeren met beplantingsstrook, ankerplanten naast de tub, lege lawn breken met border/heg.
- MEDIUM · waterig-glimmend — Voorgrondgras fel/verzadigd en carpet-uniform met kaarsrechte randen. → Albedo/verzadiging omlaag, randen laten rafelen, halmvariatie.
- MEDIUM · overig — Hot-tub-deksel ligt nog deels op het bad, geen stoompluim. → Deksel weg, subtiele stille stoom (Volume Cube).
- LOW · overig — Buitenbad-lantaarn leest niet duidelijk als brandend. → Emissie 2200-2700K + kleine warme point checken.
- LOW · gras-door-verharding — Donkere gap tussen deck-rand en stapstenenpad; halmen over de deck-lip. → Gap dichten met grind/border, grasscatter langs de lip terugzetten.

**Sterk:** probe technisch schoon (AgX, 0 missing/broken); probe-floaters vals-positief; sterke hero-diepte; nerf correct horizontaal; prop-schaal klopt + stapstenenpad/rughaag als basis.

---

### camelia_wijnterras — techn. OK ✓ · 0 blockers · 1 high
Technisch schoon (AgX Medium High, 130 spl); problemen zijn compositie/verankering. Dekt de 8-jul review (6,5/10).

- **HIGH · verankering** — De hero-bistroset (het "wijnterras") staat rechts half/heel op het gazon, niet op de terracotta tegels. Probe-floaters zijn vals-positief; het probleem is horizontale plaatsing. → Set ~0,4-0,6 m naar links-voor zodat alle 4 de poten op de tegels staan + grounding-check. (Review-fix #2.)
- MEDIUM · compositie — Terras ~60% leeg, ruimte ónder het afdak volledig kaal. → Aankleden met olijf/rozemarijn/lavendel + tweede zit + zwakke warme fill. LET OP: Trimmed_Olive_Tree GLB is een reuzenboom, geen kuipplantje.
- MEDIUM · overig — Lichtsnoer staat uit + eindigt in een kale den. → Snoer aan via S2-emissie-preset (kopieer uit `scene_b_spa.py`); snoer-eind ankeren; kale boom vervangen.
- MEDIUM · waterig-glimmend — Uniform borstel-tapijt-gras, te koel voor mediterraan. → S1 grass-mix, rond dit terras droger/warmer.
- MEDIUM · gras-door-verharding — Lange sprieten prikken over de tegel-voorlip. → Gras-mask ~3-5 cm van de rand, tegel 1-2 cm laten opsteken + AO-randje.
- LOW · compositie — Lege lucht/veld-strook boven de heg rechts. → 1-2 extra boomringen of camera 2-3° lager.
- LOW · overig — Namiddag-goud mag dieper/warmer. → Zon elev ~15°, 3800K. Nice-to-have.

**Sterk:** technisch gezond (AgX, geen missing/broken); vloer blijft binnen de footprint; nerf horizontaal; blokhut vrij/hero-leesbaar; heg sluit achtergrond, geen HDRI-vlekken.

---

### dahlia_tuinkantoor — techn. OK ✓ · 0 blockers · 3 high
Geldige render, maar het tuinkantoor-verhaal ontbreekt volledig en de cabin "staat random" in een egaal grasveld.

- **HIGH · verankering** — Dek + cabin zweven in een onafgebroken zee van gras: geen pad naar de dektrap, geen border langs de dekrand. Exact de "staat er random"-kritiek. → Stapstenenpad van voorgrond-onderhoek naar de trap (verzonken + gras-mask) + beplantings-/grindstrook langs de dek-voorrand.
- **HIGH · compositie** — Open zijde onder de kap toont alleen lege vloer + klein potplantje; geen bureau/stoel/laptop/lamp. Concept "tuinkantoor" wordt niet verteld; bay is donker. → Camera 10-15° naar rechts of bureau-opstelling 0,8 m naar de open zijde + zwakke warme fill. ("HET BUREAU MOET ZICHTBAAR".)
- **HIGH · overig (gras)** — Uniform borstel-tapijt, te grote sprietschaal (leest kniehoog), vult ~40% frame. → grass_lib S1-patch + sprietschaal omlaag.
- MEDIUM · gras-door-verharding — Graspollen over de dek-voor/rechterrand; dek rust op grastoppen. → Dek 1-2 cm verzinken + gras-mask + AO-randje.
- MEDIUM · zwever — Grijze ronde sokkeltafel oogt misplaatst (staat wel op het dek). → Vervangen door loungestoel + bijzettafel, of verwijderen.
- MEDIUM · compositie — Twee (vrijwel) identieke bolboompjes symmetrisch → CG-kloon. → Eén vervangen door siergras-bak of maat ~20% variëren + asymmetrisch.
- MEDIUM · overig (licht) — Vlakke roze-paarse dawn zonder zonrichting. → Zon laag van rechts (elev 8-15°, 3500-4500K).
- LOW · zwever — ~40 probe-floaters, allemaal achtergrond-boomonderdelen achter de heg (niet zichtbaar). → Optioneel boombases naar z=0 clampen.
- LOW · compositie — Smalle open luchtstrook rechtsboven. → 1-2 extra bomen of camera lager.

**Sterk:** technisch schoon (AgX, geen missing/broken); nerf correct; vloer binnen de gevel (dek bewust naar voren); cabin vrij/leesbaar met nette raamgloed; rughaag + dichte treeline als achterkader.

---

### dahlia_leeshoek — techn. OK ✓ · 1 blocker · 1 high
Dichtst bij klaar (~7/10): hero-cabin vrij/centraal, goede gelaagde verankering. Grootste hefbomen zijn mood + afwerking.

- **HIGH [B] · missende-textuur** — `wild_rooibos_bush_alpha/diff/nor_gl/rough` ontbreken. Nu geen magenta zichtbaar (struik buiten beeld/hidden), maar een landmine: bij scatter-/crop-verschuiving rendert hij magenta/alpha-loos. → Relink/pack de 4 texturen uit `assets/polyhaven/models/textures`, of struik verwijderen als ongebruikt; daarna full-render controleren.
- MEDIUM · verankering — Grijs tegelpad eindigt abrupt midden in het gazon en ligt bovenop het gras. → Pad doortrekken naar de linker-onderhoek + tegels ~1 cm verzinken.
- MEDIUM · overig — Wandlantaarn onder de kap uit; achterwand leeg grijs vlak. (Probe-floater wandlantaarn = logische hoogte, geen zwever.) → S2-praktijk-preset + achterwand aankleden.
- MEDIUM · overig (licht) — Vlakke roze-paarse dawn zonder schaduwrichting. → S4 lage zon rechtsachter (3800-4000K).
- MEDIUM · overig (gras/aarde) — Gras grijzig/koel/uniform; kale aarde grijzig i.p.v. humus. → S1 gras-mix + humus-bruine border.
- LOW · overig — 11 texturen uit temp-mappen + oude C:-paden (resolven nu, maar fragiel). → Pack/remap naar `assets/` op D:.

**Sterk:** sterke hero (cabin vrij/centraal, dubbele deur + open kap); AgX + Base Contrast; goede gelaagde verankering (lavendel-border, tegelpad, terras, rughaag, dennen); props netjes gegrond; nerf correct; vloer binnen footprint.

---

### jasmijn_theehuis — techn. OK ✓ · 1 blocker · 2 high
Geldige render, blokhut leest goed; maar het grindterras rendert als betonplaat en de aankleding mist verankering.

- **HIGH [B] · missende-textuur** — `T_vl0mfbllw_8K_B.png` (BaseColor) + `_N.png` (Normal) van construction_gravel ontbreken → terras is een glad egaal lichtgrijs betonvlak i.p.v. grind (de #1-kritiek). Geen magenta in dit frame, maar full-res kan alsnog roze geven. → Grind-material herstellen (relink) OF echte grind bouwen (pebble-textuur + normal/displacement of kiezel-scatter) + AO-voegen; verweesde image-datablocks purgen.
- **HIGH · verankering** — Bronzen theepot-lantaarn staat los + uit midden op het lege betonterras; geen pad; bolstruiken los. → Lantaarn naar de bank onder het afdak + aan; stapstenen-lijn naar het terras; bolstruiken groeperen langs een mos-/grindrand.
- MEDIUM · zwever — Betonvlak zweeft op de grastoppen (voorrand op de sprieten). → 1-2 cm verzinken + gras-mask + AO-randje.
- MEDIUM · overig (licht) — Vlakke roze-paarse dawn zonder richting. → Zon laag links-achter (elev 8-15°, 3500-4500K).
- MEDIUM · vloer-onder-overkapping — Bank + theeset onder het afdak bijna onleesbaar donker (vloer zelf blijft binnen de gevel). → Zwakke warme fill (10-20 W, 2700K, `use_shadow=False`).
- LOW · zwever — Esdoorn-branches/tile probe-flag; stamvoet in het gras verborgen (visueel gegrond). → Optioneel origin naar z=0.
- LOW · compositie — Horizon-gat rechts boven de heg. → 1-2 extra boomringen of camera lager.
- LOW · overig (gras) — Gras hoog/dicht/uniform, bedekt de terrasrand. → S1 gras-mix, korter rond het terras.

**Sterk:** blokhut vrij/hero-leesbaar; AgX Base Contrast, geen zwart/magenta; nerf correct; zwart + blank-hout leest als japandi; geen gras door verharding, geen HDRI-vlekken; rughaag + esdoorn als kader.

---

### jasmijn_familietuin — techn. OK ✓ · 0 blockers · 3 high
Technisch gezond en het **sterkste licht van de reeks** (echte zon + tak-schaduwen — referentie voor de dawn-scenes).

- **HIGH · prop-schaal** — Tuinschep in de zandbak staat bijna deurhoog (~0,8-1 m) rechtop en kruist vóór de entree (reuzenschep). → Schalen naar ~0,35-0,40 m en liggend half in het zand, weg uit de deur-sightline.
- **HIGH · zwever** — Zandbak-frame zweeft op de grastoppen (donkere spleet, sprieten eronderdoor). → ~2 cm laten zakken + gras-mask + zandmorseling op het gras.
- **HIGH · vloer-onder-overkapping** — Auto-vloer van de open bay steekt vóór het voorgevelvlak uit; funderingslat loopt buiten de wand op het gras. → Vloer terugtrimmen tot binnen/gelijk met de gevellijn; lat inkorten tot onder de wand.
- MEDIUM · verankering — Tegel-eiland ligt los, geen stoep vóór de dubbele deuren. → Smal tegelpad van deur-stoep naar het eiland + drempeltegel.
- MEDIUM · gras-door-verharding — Sprieten over de patio-voorrand; opstaande lichte plaatrand. → Gras-mask strak op de plaatrand + plaat ~1 cm verzinken.
- MEDIUM · nerf-richting — Front-wandpaneel rechts van de deur leest verticale nerf terwijl de courses horizontaal liggen. → Vuren-rene mapping 90° roteren per gevel.
- MEDIUM · verankering — Vogelbad droog + solitair midden in het gazon. → Waterschijf (glas-shader) toevoegen + verzinken + dichter bij een border.
- LOW · zwever — Maple-branches/tile probe-flag; bleke kale tak links-boven. → Trunkvoet op z=0 checken, of dichter blad/tak terugtrekken.
- LOW · missende-textuur — Zandoppervlak vlak/schoon zonder korrel (geen echt missend bestand). → Displacement/bump + korrel-normal + kuiltjes.
- LOW · compositie — Gat tussen heg en bomen rechts (gele horizonstrook). → Heg doortrekken of extra den.

**Sterk:** echte zonrichting + tak-schaduwen + heldere lucht (referentie-licht); product goed in beeld; geen technische defecten; doordachte basisopstelling (borders, heg, picknicktafel, zandbak, vogelbad); gras mat/droog.

---

### lavendel_pluktuin — techn. OK ✓ · 0 blockers · 3 high
Technisch schoon; blokkeert niets. De bekende 5,5/10-scene die met licht + grond naar ~7 gaat. Opstelling is door Beike goedgekeurd.

- **HIGH · gras-door-verharding** — Losse graspollen bovenop patio, tegelpad en verharding rond de rozenboog; gras-mask niet strak. Beike's #1 kritiek. → Mask strak clippen op de footprint (marge ~2-3 cm), grasdichtheid 0 op hard-surface (mask-cell 0.22) + AO-randje.
- **HIGH · overig (grond=beton)** — Lichtgrijze kale ondergrond schijnt door tussen de pollen → leest als beton. → Grond-basiskleur naar donkere humus + dichtheid/clump-overlap omhoog + S1 grass-mix.
- **HIGH · overig (licht)** — Volledig vlak grijs overcast; bloemen knallen niet, hout bleek. → Warme zon elev 10-12° van links (3800K) + heldere ochtend-HDRI. GEEN World Volume Scatter.
- MEDIUM · verankering — Borders staan als losse pollen bovenop verharding/gazon zonder plantvak/mulch. → Smal aarde/mulch-vlak onder elke clump + gras-mask-fade (geen planten verplaatsen).
- MEDIUM · vloer-onder-overkapping — Vloer ónder de kap correct binnen de wanden (sterk); maar de grijze apron steekt ver het gazon in met harde voorrand. → Apron terugbrengen tot vóór de zitplek/deur + rand verzinken/onregelmatig.
- LOW · compositie — Grote lege lawn links; horizon-gaatje rechts. → Camera 2-3° lager/rechts; voorste border 10-15 cm zakken; extra bomen rechts.
- LOW · zwever — Probe-floaters = []; enkele buddleja-pluimen leunen over het pad. → Pluimen terugbuigen/roteren of bush ~10 cm terug (cosmetisch).

**Sterk:** nerf correct horizontaal (belangrijkste R4-feedback zit goed); vloer binnen de wanden (raycast-vloerfix werkt); AgX + HeroCam, geen missing/broken; gras mat (geen natte look); rozenboog geankerd; goed bloempalet.

---

### lavendel_lavendelveld — techn. OK ✓ · 0 blockers · 2 high
Technisch schoon; zwakte in verankering + mediterrane identiteit. Reviewpunten #7 (6/10) nog niet doorgevoerd in deze preview.

- **HIGH · verankering** — "Lavendel" staat als losse gestrooide pollen in het gazon: geen border/mulch/drifts/rijen. Beike's #1 kritiek. → Plant in drifts/rijen als leading line richting camera, elke rij in smal mulch/grind-bed, borderbreedte ≥40-60 cm.
- **HIGH · overig (gras)** — Uniform fel-verzadigd groen met lange weide-sprieten → Hollands gazon, niet mediterraan. → S1-kleurshift naar droger/geler + korter + droge-aarde/grind-stroken tussen de rijen.
- MEDIUM · verankering — Geen pad van veld naar de deur; grote lege gazonvoorgrond. → Smal grindpad tussen twee rijen naar de stoep; camera evt. zakken.
- MEDIUM · compositie — 3 topiary-potten geclusterd pal voor de deur, blokkeren de entree + off-thema. → 1 pot naast de deur, rest naar de kap-zijde; overweeg lavendel/olijf/rozemarijn.
- MEDIUM · waterig-glimmend — Paarse bloemtrossen tonen wit-uitgeblazen speculaire spikkels (wasachtig). → Roughness omhoog/specular omlaag; highlight-spikkels dempen; backlight-strength checken.
- MEDIUM · overig — Onder de kap alleen stoel + statafel + mand verloren in lege betonvlakte. → Kleedje + boeket/kruik + zwakke warme fill (S2).
- LOW · prop-schaal — Statafelhoogte tegen lage bistrostoel (zit klopt niet). → Lage bistro-tafel of barkruk.
- LOW · gras-door-verharding — Lang gras botst hard tegen de patio-slab. → Maaistrook/edging (200-300 mm flush) + korter gras.
- LOW · overig — Lichtpaarse sticker/prijs-decals op de terracottapotten. → Decal uit UV/albedo of pot 180° draaien.
- LOW · overig — Linker achtergrondboom iel/schaars blad. → Vollere donor of foliage-dichtheid omhoog (secundair).

**Sterk:** warme mist/godray-backlight rechts is de **sterkste sfeer van de reeks** (behouden); Douglas-hout warm + nerf correct; vloer als patio-slab binnen de gevel; cabin vrij/centraal; technisch valide (AgX, geen missing/broken, geen zwevers).

---

### lelie_ochtendnevel — techn. OK ✓ · 0 blockers · 3 high
Technisch schoon; zwaktes in afwerking + verankering.

- **HIGH · gras-door-verharding** — Plankenpad rechts (losse kris-kras segmenten) zit bovenop de grastoppen, sprieten prikken ertussen; deur-oprit rust op de toppen. → Elke plank 1-2 cm verzinken + grass-attribuut 0 binnen de footprint (GN_GrassMasked) + onderste 3 planken uitlijnen + AO-randje.
- **HIGH · hdri-vlek** — Achtergrond rechts toont harde horizontale banden (groen veld / paars berg / roze lucht) → platte backdrop; roze waas-vlek boven de blokhut. → 1-2 extra boomringen rechts, of mist-cube doortrekken, of camera 2-3° lager.
- **HIGH · compositie** — Rots staat dood-centraal vóór de dubbele deur, blokkeert looproute + zicht op de entree (hero). → Rots ~1,5 m naar links, half in de klaprozen, licht in de grond gedrukt.
- MEDIUM · prop-schaal — Boulder is ~mensgroot, domineert de voorgrond. → ~25-35% verkleinen of cluster van 2-3 kleinere stenen + onderkant verzinken.
- MEDIUM · verankering — Geen leesbaar frame: pad resolveert niet, klaprozen verspreid zonder bed, geen rughaag/border. → Doorlopend pad naar de deur + begrensd bloembed + border langs de gevel + dennen-rughaag.
- MEDIUM · waterig-glimmend — Donkere glimmende plekken rond de rotsvoet/pad; gazon uniform plastic-groen. → Roughness omhoog, natte-decal weg, gras-mix S1.
- MEDIUM · overig (licht) — Ochtendnevel overal even dik/vlak, geen godrays. → Zon laag rechtsachter (elev 8-15°, 3500-4500K) + begrensde volume-cube (density 0.002-0.005) i.p.v. World Volume Scatter.
- MEDIUM · overig — Deurglas melkachtig-dicht (leest als blinde plaat). → Glas-shader (Transmission 1.0, IOR 1.45, ~12 bounces); frosted mét warme gloed erachter.
- LOW · overig — Open kap-bay donker/leeg (vloer binnen de wanden). → Warme fill + houtstapel/hakblok (wilderness).

**Sterk:** nerf correct horizontaal (UV/FLAT-fix goed); vloer binnen de gevel; klaprozen + bos-mist-decor geven dieptelagen; technisch schoon (AgX, geen missing/broken, geen floaters — zwevende boomvoeten verholpen met FarGround + dennen); dennen realistische schaal; blokhut vrij.

---

### lelie_avondkubus — techn. OK ✓ · 0 blockers · 2 high
Technisch schone blue-hour render; compositie/verankering is het zwakke punt. Alle 8-jul restpunten nog aanwezig.

- **HIGH · compositie** — Heg-blok staat pal voor/rechts van de verlichte deur; bollard-pad buigt erlangs i.p.v. ernaartoe → zichtlijn pad→entree geblokkeerd. → Heg-blok ~1,5 m naar links of halveren + pad recht naar de deur.
- **HIGH · gras-door-verharding** — Sprieten overlappen de randen van de stapstenen + de terras-apron-voorrand. → Scatter-exclusie rond elke footprint + gras ~2-3 cm terug van elke steenrand.
- MEDIUM · hdri-vlek — Warme oranje/gele lichtvlek in de boomlijn linksboven (light-leak). → HDRI ~20-40° draaien of vlek maskeren met donkere boom.
- MEDIUM · compositie — Rechter glas/schuifpaneel leest als donker vlak gat; "verlichte kubus"-concept maar half waar. → Zwakke warme Area (2700K, ~30-60 W, `use_shadow` uit) achter het glas + één zichtbaar object.
- MEDIUM · verankering — Groot glimmend tropisch/banaan-blad linksonder, off-palet + los in het gras + onderbelicht. → Vervangen door moderne-palet pol (Hakonechloa/Miscanthus/Buxus) in border, of verwijderen.
- MEDIUM · overig — Lucht grijzig-groen met ruis/fireflies. → Schonere blue-hour HDRI + world-strength/samples/denoise (OIDN).
- LOW · zwever — Stapstenen liggen licht boven de grastoppen (zwakke contactschaduw). → 1-2 cm verzinken + contact-AO.
- LOW · waterig-glimmend — Gazon opvallend helder/verzadigd voor blue-hour, "gloeit". → Albedo/helderheid omlaag, desat + roughness minimaal omhoog.

**Sterk:** deurgloed werkt (uitnodigende entree); bollard-pad met warme pools + correcte lampschaal (~0,7 m); technisch schoon (AgX, geen missing/broken, geen floaters); modern zwart/antraciet palet leest als product; nerf correct; entree-apron binnen de gevel.

---

### magnolia_wintertuin — techn. OK ✓ (REBUILD) · 0 blockers · 1 high
**R4-rebuild (2-jul libs), lage preview-res — eindoordeel bij Beike.** Technisch gezond; sterke compositie/hero.

- **HIGH · verankering** — Houten dek staat als verhoogd platform bovenop de grastoppen (harde opstaande rand, geen verzonken maaiveld/gras-mask). Bekend S3-punt. → Dek 1-2 cm verzinken + gras rond de omtrek maskeren (3-5 cm) + AO-strook.
- MEDIUM · overig (seizoen — **beslissing bij Beike**) — Naam "wintertuin" maar heg + bomen zomergroen, gazon lush helgroen, veldstrook golden, witte spikkels als sneeuwklokjes/rijp → gemengde signalen. → Eerst beslissing ophalen; bij "winter": gazon ontkleuren, spikkels kleiner/lager, koele haze-cube, veldstrook verzoenen.
- MEDIUM · verankering — Geen pad/aanloop naar het dek (stap direct op een verhoogd platform). → Korte stapsteen-/grindstrook als aanloop of opstap verlagen.
- LOW · overig — Witte spikkel-scatter landt ook op de beukenhaag (onnatuurlijk). → Scatter beperken tot grond/gras, heg-mesh uitsluiten.
- LOW · compositie — Grote helderwitte pot met succulent concurreert met de blokhut. → Pot kleiner/naar links of matter/minder wit.
- LOW · overig — Kleine terracottapot met dun zaailingetje oogt schraal. → Vollere kuipplant of weglaten.
- LOW · missende-textuur — Latent: `used_image_dirs` verwijst nog naar `aerial_grass_rock` (gaf eerder witte rotsvlekken; op 2 jul naar painted_grass omgezet). Niet actief zichtbaar. → Vóór final verifiëren dat het grondmateriaal painted_grass gebruikt.

**Sterk:** technisch schoon (AgX Base Contrast, geen missing/broken); probe-floaters vals-positief (props op het dek); nerf correct; bistroset netjes verankerd; sterke hero (blokhut vrij, beukenhaag als kader, dek + dressing, tak-schaduwen + deurgloed); schone overcast zonder HDRI-vlekken; gras mat/groen.

---

### zonnebloem_zomeravond — techn. OK ✓ (REBUILD) · 0 blockers · 2 high
**R4-rebuild (2-jul libs), lage preview-res — eindoordeel bij Beike.** ~6,5-niveau; nette boerderij-hero, maar kernpunten uit de reviewlijst nog niet verwerkt.

- **HIGH · overig (concept)** — Naam "zonnebloem" maar geen enkele zonnebloem in beeld (borders zijn rozen + hortensia). Fix #1. → Rij van 5-7 zonnebloemen (BlenderKit, 1,6-2,2 m, linked copies met variatie) langs de rechterheg/achter de linkerborder, gegrond in het gras.
- **HIGH · verankering** — Dubbele deur heeft alleen een grijze drempel + rozenstruik; geen pad/stapsteen-lijn naar tuin/terras. Klassiek "staat er random". → Tegel-/stapsteenpad van de deurstoep naar het terras (verzonken, vanaf de border) dat deur en terras verbindt.
- MEDIUM · overig — Lichtsnoer langs de daklijst leest als UIT (matte witte bolletjes). → Bulbs op emissie (~2200-2700K + halo/bloom via compositor glare) + diepere goudzon (elev ~8°, ~3200K).
- MEDIUM · compositie — Interieur onder de kap donker/dood; dinerset onderbelicht, geen lichtbron op tafel. → Warme fill onder de kap + brandende lantaarn op tafel.
- MEDIUM · overig (gras) — Uniforme sterk-verzadigde eenkleurige scatter, iets te fel. → Gras-mix S1 + verzadiging temperen.
- LOW · prop-schaal — Donkere wijnfles op tafel iets te groot. → Flesschaal terug naar ~0,30 m, glazen mee-schalen.
- LOW · gras-door-verharding — Geen gras door de tegels, wel strak tegen de voorrand/linkervoorhoek. → Slab ~14 cm verhogen (Beike-voorkeur) of grass=0 marge ruimer.
- LOW · vloer-onder-overkapping — Vloer lijkt binnen de footprint (controlepunt). → In Blender bevestigen dat de plaat niet voorbij de zij-/achterwand steekt.
- LOW · zwever — `wooden_lantern_01_handle` probe-flag = handvat-bogen op een grondlantaarn (vals-positief). → Geen actie; wel garland-palen/draad links zichtbaarder maken zodat bulbs niet los in de lucht hangen.

**Sterk:** hero leest goed (blokhut in 3/4-hoek, deur + kap-opening + dinerverhaal tegen duskslucht); nerf horizontaal correct; verankeringsbasis aanwezig (rughaag + borders); vloer lijkt binnen de footprint; technisch schoon (AgX Medium High, geen missing/broken, geen echte zwevers).

---

### zonnebloem_ochtendhoek — techn. NIET OK ✗ (REBUILD) · 1 blocker · 1 high
**R4-rebuild (2-jul libs), lage preview-res — eindoordeel bij Beike.** Nette Scandi-ochtendhoek, maar één technisch mankement + alle bekende scene-6-punten.

- **HIGH [B] · missende-textuur** — `T_vl0mfbllw_8K_B.png` (base) én `_N.png` (normal) van path_stones/construction_gravel ontbreken (pad wijst nog naar `C:\Users\...\Documents\...`) — exact de Deur_Stoep die sneuvelde bij de C:→D:-migratie. In beeld: twee grijze stoeptegels als vlakke textuurloze platen (geen magenta, valt terug op grijze default). Dit zet `technical_ok=false`. → Relink/pack de grindtextuur, of de al-bestaande R4-fix overnemen (AmbientCG PavingStones125A, gepakt — zie HANDOFF r116-117). Deze rebuild is teruggevallen op het kapotte oude gravel-materiaal.
- MEDIUM · gras-door-verharding — Stoeptegels + vlonder liggen bovenop het gras; hoog gras tot tegen/over het harde vlak. → Paving + vlonderrand 1-2 cm verzinken + gras-mask (mask-cell 0.22) + AO-randje.
- MEDIUM · verankering — Grijze stoep ligt los, verbindt nergens mee; geen pad/leading line naar deur of loungehoek. Beike's #1 kritiek. → Verzonken tegelpad van de stoep naar de rechter-onderhoek langs de stoelen.
- MEDIUM · overig (licht) — Vlak roze-paars ochtendwaas zonder schaduwrichting. → Echte zon laag rechts (elev 8-15°, 3500-4500K) + strijklicht/slagschaduw.
- MEDIUM · overig — Interieur van de open kap donker; rechter rechthoek (raampje/luik) leest als zwart gat. → Zwakke warme fill-area (10-20 W, `use_shadow=False`) + luik-materiaal checken.
- MEDIUM · compositie — Cabin vrijwel dood-centraal; onderste ~40-50% lege grasvoorgrond zonder verhaal. → Camera ~0,5 m naar links + 2° omlaag zodat het (nieuwe) pad de voorgrond vult.
- MEDIUM · zwever — `wooden_lantern_01` op zmin ~1,6-1,9 m zonder zichtbare haak/ketting → zweefrisico (en dode practical). → Plaatsing verifiëren (ophangen aan balk met zichtbare haak, of op tafel/paal) + emissie aan (2200K).
- LOW · waterig-glimmend — Voorgrondgras uniform borstel-tapijt, fel/verzadigd, aan de lange kant. → Gras-mix `grass_lib.py` (S1) + hoogte terug.
- LOW · verankering — 3 lavendel-clusters als losse bollen aan de vlonderrand zonder bedrand (Beike waardeert ze — behouden). → Smalle border/bed met grind/humus-strook eronder.

**Sterk:** hero-leesbaarheid goed (cabin vrij, glasdeur + open kap afleesbaar); nerf-richting correct; techniek-config correct (AgX Base Contrast, Cycles, HeroCam; errors/broken/none leeg — behalve de missende images); geen HDRI-vlekken (schone ochtendgradient); prettige loungehoek + lavendel-accenten (behouden); probe-floater plant vals-positief (gegrond op de vlonder).

---

## 4. Aanbevolen review-volgorde voor Fable 5

Begin bij de blockers/missende texturen (moeten sowieso vóór final), dan de rebuild-verdicten, dan de high-zware scènes, aflopend naar de scène die het dichtst bij klaar is.

**Blok 1 — Blockers / missende texturen (eerst):**
1. **zonnebloem_ochtendhoek** — `technical_ok=false`; Deur_Stoep-grind weg. (Tevens rebuild: R4-verdict koppelen.)
2. **jasmijn_theehuis** — grind-textuur weg, terras is zichtbaar een betonplaat.
3. **dahlia_leeshoek** — wild_rooibos-landmine (nu buiten beeld) relinken/purgen; verder ~7/10.

**Blok 2 — Overige rebuild-verdicten (goed genoeg als R4?):**
4. **magnolia_wintertuin** — + seizoensbeslissing winter/vroege-lente.
5. **zonnebloem_zomeravond** — + concept-check (zonnebloemen ontbreken).

**Blok 3 — High-zware scènes (3× high):**
6. **dahlia_tuinkantoor** — bureau ontbreekt + verankering.
7. **jasmijn_familietuin** — reuzenschep, zwevende zandbak, uitstekende bay-vloer (heeft wél het beste licht).
8. **lavendel_pluktuin** — gras/grond/licht (5,5→7 met 3 ingrepen).
9. **lelie_ochtendnevel** — pad zweeft, backdrop-banding, rots vóór de deur.

**Blok 4 — 2× high:**
10. **camelia_buitenbad** — gele HDRI-vlek + uitstekend hot-tub-deck.
11. **lavendel_lavendelveld** — lavendel-drifts + entree vrijmaken.
12. **lelie_avondkubus** — zichtlijn deur vrij + rechter kubus verlichten.

**Blok 5 — Dichtst bij klaar (1× high):**
13. **camelia_wijnterras** — alleen bistroset op de tegels + terras aankleden.

*(dahlia_leeshoek staat in blok 1 vanwege de textuur-landmine, maar is qua kunst de meest afgeronde scène — ~7/10.)*
