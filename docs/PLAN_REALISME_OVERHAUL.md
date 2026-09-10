# Realisme-overhaul — onderzoek + per-render plan (2026-06-16)

Gebaseerd op research (4 streams) + keiharde kritiek per render (16 agents). De gebruiker heeft gelijk: de scenes lezen als "3D-mockup", niet als foto. Twee hoofdoorzaken, in ELKE scene:
1. **Zelfgemaakte BLOKKEN** — vlonders, terrassen, plantenbakken, zandbak, handdoeken, potten zijn kale `add_box`/cilinder-primitieven met één vlakke kleur: geen plank-naden, geen bevels (100% scherpe CG-randen), geen PBR-variatie, geen dikte/rand, zwevend zonder contactschaduw.
2. **PADEN** — platte ribbon-meshes of losse identieke cilinders ("random rondjes") die nergens op aansluiten, zonder kantopsluiting, plat op het gras geplakt met een mes-scherpe snijrand.

Plus globaal: Filmic i.p.v. AgX, geen DoF, oververzadigd gras, kale gras↔hardscape-snijlijnen.

---

## A. GEDEELDE REALISME-TOOLKIT (bouw eerst in `scripts/cabin_lib.py`)

Deze helpers + globale settings repareren ~80% van élke scene. Eenmaal bouwen, overal toepassen.

### A1. Globaal (in `render_setup`)
- **AgX i.p.v. Filmic**: `view_transform='AgX'`, look `'AgX - Medium High Contrast'` (zonnig) / `'AgX - Base Contrast'` (overcast/zen). Grootste gratis realisme-winst (camera-achtige highlight-rolloff).
- **DoF**: `cam.dof.use_dof=True`, `aperture_fstop=6.0`, `focus_object=cabin` (of focus_distance op de gevel). Subtiel — voorgrond/achterboomring net zacht.
- Behoud: 35mm, ooghoogte 1.6m, waterpas + shift_y (geen kantelende verticalen), zon-angle 1.5–3° (zachte schaduw, nooit 0), texture_limit 2048, persistent_data off.

### A2. `plank_deck(name, x0,x1,y0,y1, top_z, mat, plank_w=0.145, gap=0.005, thick=0.028, dir='Y', fascia=True)`
Vlonder/terras uit LOSSE planken i.p.v. één box: rij plank-cubes (14,5cm breed, 5mm voeg), elke plank micro-bevel (3mm) + per-plank val-jitter (±0.05) + Z-rot-jitter (±0.2°), staggered koppen. **Fascia/plint** rondom (verbergt plankkoppen, geeft dikte), 1–2cm in de grond verzonken → contactschaduw, niet zwevend. Materiaal `pbr_from_folder(wood_floor_deck)` (heeft normal+rough), nerf langs de plank.

### A3. `slat_planter(name, x0,x1,y0,y1, h, mat_wall, mat_post, plank_h=0.15, gap=0.006, thick=0.02, post=0.07, post_over=0.03)`
Plantenbak/verhoogd bed/zandbak uit losse planken (3–4 gestapeld met 4–6mm voeg) + 4 hoekpalen die uitsteken, alles bevelled. Materiaal `pbr_from_folder(brown_planks_09)` (nerf langs plank). Vult de bak (aarde-plane + beplanting). Voor zandbak: zand = noise-displaced bol oppervlak ONDER de plankrand, niet vlakke box.

### A4. `stone_path(curve_pts, width, mode='flagstone'|'klinker'|'gravel', edging=True, sink=0.02)`
Echt gelegd pad langs een curve, **aansluitend op deur/terras**, met **kantopsluiting** en **verzonken** in het gras:
- **flagstone/stapsteen**: losse onregelmatige scan-stenen (`stone-pathway/Stones.blend`, `cobblestones_scan`, `rocky_stone_path_scan`) als instances; stapstenen op stride-afstand 55–65cm, random rot_z + index → geen identieke rondjes; 1–2cm boven gras, onderkant in de grond.
- **klinker**: individuele klinker-meshes (21×7×6,5cm, 5mm voeg) in halfsteens/keperverband, micro-bevel, ±2° rot + ±3mm z-jitter, `beton`/`paving_stones_64` PBR + per-steen kleurvariatie (Object-Info Random).
- **gravel**: `construction_gravel` PBR-vlak (bump) + GN-scatter losse `small_stones_pack`-kiezels erbovenop.
- **edging**: doorlopende houten kantplank/betonband/cortenstrip langs beide randen (2–3cm boven pad), via curve.
- **aansluiting**: pad begint ONDER de dorpel/terrasrand (5–10cm overlap), zelfde z als terras; gras 1–2cm lager dan padrand; valideer z via bbox.

### A5. `bevel_all(obj, w=0.004)` — Bevel-modifier (width 3–5mm, 2 seg, angle-limit 45°, harden_normals) + shade_smooth/auto_smooth op ELK zelfgemaakt object. De rand-highlight is dé "echt materiaal"-tell. Bevel laten staan als modifier.

### A6. Materiaal-realisme (in `pbr_from_folder`/nieuwe `realush`-helpers)
- Vlakke base-color → albedo-variatie (2× Noise + HueSat ±8% via MixRGB Fac≤0.15).
- Roughness-variatie (Noise→MapRange 0.55–0.78) i.p.v. vlakke roughness (= plastic).
- Edge-wear (Geometry Pointiness → ColorRamp smalle band → lichtere/ruwere randen) + cavity-dirt (AO → donkerder voegen).
- Geen pure (0,0,0)/(1,1,1): staal 0.18, wit textiel 0.88.
- Lichte displacement (Displacement+Bump, scale 1–2cm) ALLEEN op het hoofd-klinkerpad (paving_stones_64 + adaptive subdiv).

### A7. Gras + grond-overgang
- Gras ontzadigen (HueSat sat 0.7–0.8), patch-variatie (Noise+Voronoi tussen 2 tinten), tiling-vlekken breken.
- **Geen kale snijlijn**: GN-grasscatter die 5–15cm OVER elke pad-/terras-/cabinrand hangt + vuilrand (aarde/grind) langs paden. Alles 1–3cm in de grond verzonken voor contact-AO.
- Voorgrond: echte 3D-grassprieten-scatter (15–20%) i.p.v. alleen platte textuur.

### A8. Water (`pbr_water`)
Echte diepte: Principled Transmission=1, IOR 1.333, lage roughness, lichte base + **Volume Absorption** (turquoise/donker, density 1.5–3) + gesloten donkere bodem eronder + 2× noise-bump rimpels. Voor dompelbad: damp-volume erboven.

### A9. Grounding (`ground_to` + contact)
Elk object min-Z exact op draagvlak, 0,5–2cm laten inzakken (geen lichtkier) → Cycles GI rekent contactschaduw. Verifiëren met `inspect_cams` close-up + `audit`, niet op aanname.

---

## B. PER-RENDER PLANNEN

Legenda fixes: **[deck]**=A2 **[slat]**=A3 **[pad]**=A4 **[bevel]**=A5 **[mat]**=A6 **[gras]**=A7 **[water]**=A8 **[ground]**=A9 **[global]**=A1.

### 1. Camelia Buitenbad (scandi-spa, blue hour)
- Vlonder = één platte slab → **[deck]** losse planken + fascia (grootste enkele winst).
- Pad = 5 identieke discs "naar nergens" + 2 losse drempel-slabs → **[pad]** flagstone-stapstenen die deur-stoep ↔ tuin verbinden, onregelmatig, verzonken; één doorlopende stoep tegen de gevel.
- Handdoeken (boxen) → gedrapeerde cloth-mesh + badstof-bump. Handdoekrek/badtrap/houtstapel → **[bevel]**+kops-hout-PBR; houtstapel variatie + schors.
- Dompelbad: duig-**[bevel]** + per-duig nerf-offset, banden in hout drukken (0.18 niet 0.04); **[water]** warmer + damp.
- **[global]** AgX+DoF, **[gras]** randovergang, **[ground]** alles contact.

### 2. Camelia Wijnterras (mediterraan)
- **BUG eerst**: potten staan ONDERSTEBOVEN (180° draaien, smal onder) + boompje IN de grootste pot planten; wijnfles+glazen ZWEVEN tegen de heg → echt op het tafelblad (raycast).
- Travertine terras-box → **[pad]**-tegels met dikte/voegen/bevel; gravel-pad random → **[pad]** recht/aangesloten + edging; gat terras↔stoep dichten.
- Potten rand-lip + wanddikte + aarde; festoon warm laten gloeien. **[global]+[gras]+[ground]**.

### 3. Dahlia Tuinkantoor (modern-urban, ochtend)
- Slab-pad diagonaal "naar nergens" → **[pad]** doorlopend, aangesloten op vlonderrand, in beeld leesbaar; losse bollard weg of langs pad.
- Vlonder slab → **[deck]**+skirt. Cor-ten bakken (kartonnen dozen) → echte rust-PBR (`rust_coarse_01`), OPEN bak + wanddikte + aarde + siergras. Bollards → kop+voet+glow of weg. Bureau/laptop → echt asset of subtiele gloed achter glas.
- **[global]+[bevel] op alles+[gras]+[ground]**.

### 4. Dahlia Leeshoek (scandi)
- Vlonder slab → **[deck]**. Ribbon-pad random → **[pad]** aangesloten op stoep+vlonder, edging, verzonken. Vacht/boek/mok (boxen) → echte gedrapeerde/getextureerde props op stoel/tafel (raycast). **[global]+[gras]+[ground]**.

### 5. Jasmijn Familietuin (klassiek, middag)
- 4 losse niet-aansluitende bestratingsvlakken + z-fight → **[pad]** één doorlopend terras+stoep+pad (coplanair, edging), pad van logisch begin→deur. Fontein-eilandje verbinden of fontein in border.
- Zandbak boxen → **[slat]** + noise-displaced zand onder de rand. **BUG**: bruine cirkelvlek in gazon opsporen+weg; hortensia uit terrasrand halen. **[gras]** ontzadigen+randovergang. **[global]+[ground]**.

### 6. Jasmijn Theehuis (japandi)
- Grind-box → **[pad gravel]** bed verzonken + bamboe/steen-kant, aangesloten op engawa. 7 identieke ronde cilinders → **[pad flagstone]** onregelmatige tobi-ishi naar de deur, om de boulder. Mos-discs (jelly-bollen) → GN-mos verzonken. Engawa dun → **[deck]**+fascia. Theekommen → echte kom-holte. **[global AgX-Base]+[ground]**.

### 7. Lavendel Lavendelveld (mediterraan, golden hour)
- Terras+stoep boxen + 0,45m gat → **[pad]** doorlopende tegels; maaipad ribbon random → **[pad]** edged+verzonken+aangesloten op stoep. Lavendelrijen te regelmatig+gekloond → 2–3 mesh-varianten, kleur-jitter, rij-verstoring, aarden bedjes. Potten op gras → op stoep. **[global]+[gras]+[ground]**.

### 8. Lavendel Pluktuin (boerderij, overcast)
- Klinker-terras+pad boxen → **[pad klinker]** echt verband + edging, aangesloten. Rozenboog-klimrozen al toegevoegd — verdichten. Bank/potten cluster al gespreid — **[bevel]+[mat]+[ground]**. **[global]+[gras]**.

### 9. Lelie Ochtendnevel (forest, mist)
- Vlonderpad plank-boxen → echte plank-stapstenen/houten loopplanken; deur-vlonder box → **[deck]**. Boulders+mos al echt — mos-bollen → GN-mos. Mist behouden (sfeer-topper). **[global AgX]+[ground]**; pad echt aansluiten op deur-vlonder.

### 10. Lelie Avondkubus (modern, blue hour)
- Ipé-deck box → **[deck]**. Slab-pad → **[pad]** aangesloten. Cor-ten bak → rust-PBR open bak. Bollards langs pad. **[global]+[bevel]+[ground]**.

### 11. Magnolia Groene Long (eco-groendak)
- Stapstenen+loopplaat → **[pad]** doorlopend naar deur (deels al gefixt). Regenton cilinder → PBR+banden+deksel realistischer, pijp aangesloten. Wadi-box → grind-bed met rand. Sedum-dak scatter verdichten/variëren. Zonnepaneel detail. **[global]+[bevel]+[ground]**.

### 12. Magnolia Wintertuin (scandi)
- Ash-deck box → **[deck]**. Stepping-stones (al solide steen) → onregelmatige scan-stenen op stride-afstand. Houtstapel kops-hout. Vacht box → gedrapeerd. (zwarte schijf al opgelost). **[global]+[bevel]+[ground]**.

### 13. Roosmarijn Zentuin (japandi, overcast)
- Karesansui-rake (redelijk) → fijnere displacement + scherpere harklijnen. Mos-eilanden (afgeplatte bollen) → GN-mos op onregelmatige vorm. Tsukubai cilinder → uitgehouwen steenbak + **[water]**. Stepping-stones cilinders → onregelmatige scan-stenen. **[global AgX-Base]+[ground]**.

### 14. Roosmarijn Kruidenterras (mediterraan)
- Travertine-box → **[pad]**-tegels. Kruidenbakken boxen → **[slat]** + aarde + kruiden (magenta al gefixt). Gravel-pad → edged+aangesloten. **[global]+[gras]+[ground]**.

### 15. Zonnebloem Zomeravond (boerderij, sunset) — was goedgekeurd, maar valt onder "allemaal"
- Klinker-terras+pad boxen → **[pad klinker]** echt verband + edging (behoud compositie+slinger). Tafel-dekking cilinders → echte borden/glazen. **[global AgX]+[bevel]+[ground]**. Voorzichtig: dit is de sterkste compositie, alleen materiaal/hardscape-realisme optillen.

### 16. Zonnebloem Ochtendhoek (scandi)
- Ash-deck box → **[deck]**. Ribbon-pad → **[pad]** edged+aangesloten. Lavendel (al van pad af) → kleur-jitter. Mok/kan → echte props. **[global]+[gras]+[ground]**.

---

## C. UITVOERING
1. Bouw de toolkit (A2–A9) + pas `render_setup` aan (A1). Test elke helper los met een close-up render.
2. **Proof op de zwaarste scene (Camelia Buitenbad)** → tonen aan user ter validatie van het nieuwe realisme-niveau VOOR ik alle 16 omzet.
3. Na akkoord: rol de toolkit per scene uit (volgorde: zwaarste hardscape eerst), elke scene: bouw → diag → close-up inspect → audit → 1080p preview.
4. Pas finale 2560×1440 na user-akkoord per scene.

Research-detail (volledige recepten) staat in de workflow-output; kernpunten verwerkt in `cabin_lib.py` helpers en vault 'Lavendel Build Lessons Learned'.
