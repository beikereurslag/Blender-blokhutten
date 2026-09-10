# Asset-audit blokhut-renders — weekendrapport

> **Autonoom gegenereerd in het weekend van 10 jul 2026.** Dit document is een naslag voor volgende renderrondes en bundelt de inventaris van alle asset-families, het gebruik per pilotscène en de openstaande opschoon-/compliance-punten.
>
> **Let op:** de scène-gebruik-kaart is gebaseerd op 10 van de 13 geprobede pilots. De 3 herbouw-scènes (`magnolia_wintertuin`, `zonnebloem_zomeravond`, `zonnebloem_ochtendhoek`) zaten mogelijk nog **niet** in de probe-data op het moment van genereren; hun asset-families zijn nog niet in de kaart verwerkt.

---

## 1. Samenvatting

- **Totale asset-omvang: ~27 GB** verdeeld over **8 asset-families** (submappen) + **1 groep losse root-bestanden**. Grootste families: `blenderkit` (13 GB), `polyhaven` (6,1 GB), `sketchfab` (3,7 GB).
- **~496 modelbestanden** (.blend/.glb/.gltf/.fbx/.obj) en **~1.400 losse texturen**; daarnaast **50 HDRI's** (25 PolyHaven + 2 ambientCG-DayEnvironment-zips). BlenderKit-textures zitten volledig gepackt in de .blend-files.
- **6 ontbrekende texturen over 2 scènes** (zie sectie 4) — dit veroorzaakt magenta/kapotte materialen bij render en is het enige concrete, direct te fixen renderprobleem.
- **Licentie-administratie is gefragmenteerd.** CC0 (PolyHaven/ambientCG) en BlenderKit royalty_free/cc_zero zijn veilig zonder credit, maar de **sketchfab-familie heeft een compliance-gat**: ~50+ downloads zonder license-bestand en niet in `CREDITS.md`. Ook `props-beike`, `3daistudio` en `replicate-textures` zijn niet in `CREDITS.md` opgenomen.
- **Fors opschoonpotentieel** (~5 GB): off-topic BlenderKit-junk in `fietsen-d2/` (~2 GB schepen/e-bikes/windmolen), byte-identieke duplicaten (~1,2 GB blenderkit + diverse sketchfab/polyhaven/3daistudio-dubbels), nog-ingepakte staging-archieven. **Nog niet verwijderen** — alleen gemarkeerd.

---

## 2. Catalogus per familie

| Familie | #Modellen | #Texturen | Grootte | Licentie-status | Opmerkingen |
|---|---|---|---|---|---|
| **blenderkit** | 218 (112 .blend + 106 .glb) | 0 los (alle gepackt) | 13 GB | royalty_free / cc_zero → commercieel OK, geen credit. Admin via `INDEX_wishlist.txt` (~90) + `INDEX.txt` (10) + `CREDITS.md` | 45 thema-subfolders (NL-slugs). Grootste: fietsen-d2 3,3G, border-planten 2,1G. Veel off-topic junk in fietsen-d2 |
| **polyhaven** | 85 (81 .blend + 4 .gltf); 2 .blend zijn material-previews | 732 (430 png + 194 jpg + 108 exr) + 25 HDRI | 6,1 GB | **CC0**, geen credit (`CREDITS.md` r.21) | Gedeelde texturepool `models/textures/` (3,1G). Levert de universeel gebruikte grond-/model-textures + HDRI's |
| **sketchfab** | ~127 (25 .blend, 8 .glb, 67 .gltf, 14 .fbx, 3 .obj, 10 .usd) | 397 (320 png + 77 jpg) | 3,7 GB | **RISICO:** slechts 2 assets gedocumenteerd (CC-BY, in gebruik); ~50+ ongetrackt, licentie per stuk te verifiëren | 9 bron-ZIP's nog ingepakt. UE-raw-planten leveren dubbele gltf-varianten (UE + non-UE) |
| **props-beike** | 33 (13 .blend, 16 .fbx, 2 .obj, 2 .glb) | 249 (171 png + 40 jpg + 21 exr + 17 jpeg) | 2,0 GB | **GEEN** in-folder licentie; niet in `CREDITS.md`. Open risico: bamboe-hek = Blendswap-licentie (nog te checken) | 14 nog-ingepakte archieven (10 zip/2 rar/2 7z). `downloads-4jul/` = ongesorteerde staging-map |
| **losse-assets-root** | ~16 (4 losse .blend + ~12 in 13 zips) | ~49 (in zips) | 1,38 GB | Mix: Stone Pack CC0, ambientCG CC0, rest vermoedelijk BlenderKit (niet per stuk geverifieerd) | Alle 13 .zip nog onuitgepakt. Mogelijke cross-familie duplicaten met subfolders |
| **ambientcg** | 14 .blend (material-previews, GEEN objecten) | 102 (88 jpg + 14 png) | 417 MB | **CC0** (`CREDITS.md` r.21) | 15 PBR-oppervlaktematerialen + sidecars (mtlx/tres/usdc). Bricks097_PH = onvolledige dubbel |
| **blokhutwinkel-textures** | 0 | 28 (21 jpg + 6 png + 1 psd) | 307 MB | In-house product-texturen; geen externe attributie | Diffuse-only bibliotheek; alleen `luxehouse-onbehandeld` heeft volledige 8K PBR-set. Universeel gebruikt voor cabin |
| **3daistudio** | 3 .obj (bicycle, hydrangea, lavender) | 12 png (PBR per model) | 58 MB | AI-gegenereerd (3D AI Studio); niet in `CREDITS.md`, geen credit nodig | Elke .zip is dubbel van de uitgepakte inhoud (~28M redundant) |
| **replicate-textures** | 0 | 8 png (hedge/urban) | 14 MB | **Onbekend/ongedocumenteerd**; niet in `CREDITS.md` | AI-gegenereerd (Replicate). PNG's zonder alpha → beperkt bruikbaar voor cutout. 2 error-jsons (401) |

**Centrale licentiebron:** `D:/Blender-blokhutten/assets/CREDITS.md` (Beike-akkoord 7 jul 2026). CC-BY toegestaan mits credit op colofonpagina blokhutwinkel.nl; CC0 en BlenderKit royalty_free/cc_zero zonder credit. Assets zelf nooit herdistribueren.

---

## 3. Gebruik per scène + herbruik-hotspots

### 3.1 Per scène (10/13 geprobed)

| Scène (stijl) | PolyHaven | Sketchfab | Overig |
|---|---|---|---|
| **camelia_buitenbad** (hot-tub-premium) | models/textures, wooden_lantern_01, aerial_grass_rock, wood_floor_deck, hdri | trees/five_birch_trees_pack | blokhutwinkel/8192; 5 packed-temp |
| **camelia_wijnterras** (mediterraan) | models/textures, patio_tiles, aerial_grass_rock, hdri | furniture/bistrot_table_and_chair (24 tex), path_stones/flagstone_floor | blokhutwinkel/8192; 1 packed-temp |
| **dahlia_leeshoek** (scandi) | models/textures, wooden_lantern_01, aerial_grass_rock, hdri | trees/five_birch_trees_pack | 3daistudio/lavender; blokhutwinkel/8192 — **MISSING: wild_rooibos_bush** |
| **dahlia_tuinkantoor** (modern-urban-cottage) | models/textures, brown_planks_09, aerial_grass_rock, wood_floor_deck, hdri | topiary_hedge/hetz_midget_arborvitae, trees/five_birch_trees_pack, furniture/outdoor_chair_scan_medpoly | blokhutwinkel/8192; 2 packed-temp |
| **jasmijn_familietuin** (klassiek-familie) | models/textures, aerial_grass_rock, paving_stones_64, hdri | flowering_bushes (goldmound_spiraea, multi_color_butterfly_bush, bigleaf_hydrangea), decor/birdbaths, trees/maple_tree_scan, furniture/picnic_table_low_poly, tools/garden_shovel | blokhutwinkel/8192; 1 packed-temp |
| **jasmijn_theehuis** (japandi) | models/textures, boulder_01, Lantern_01, aerial_grass_rock, hdri | furniture/wooden_bench_low_poly, trees/maple_tree_scan, path_stones/construction_gravel | blokhutwinkel/8192 — **MISSING: construction_gravel** |
| **lavendel_lavendelveld** (mediterraan) | models/textures, aerial_grass_rock, hdri | furniture/bistrot_table_and_chair (24 tex), lighting/old_lantern, topiary_hedge/hetz_midget_arborvitae, decor/old_wicker_basket, decor/terracotta_pot | 3daistudio/lavender; blokhutwinkel/8192 |
| **lavendel_pluktuin** (boerderij) | models/textures, aerial_grass_rock, paving_stones_64, hdri | flowering_bushes (goldmound_spiraea, multi_color_butterfly_bush, bigleaf_hydrangea, roses), furniture/wooden_bench_low_poly, decor/old_wicker_basket, decor/cc0_rose_arch | blokhutwinkel/8192 |
| **lelie_avondkubus** (modern) | models/textures, aerial_grass_rock, hdri | — | blokhutwinkel/8192 (strakste scène, geen sketchfab/3daistudio) |
| **lelie_ochtendnevel** (forest-wilderness) | models/textures, boulder_01, aerial_grass_rock, hdri | flowering_bushes/field_poppy | blokhutwinkel/8192 (grootste scène: 1824 objs / 1632 meshes, smalle asset-set) |

### 3.2 Herbruik-hotspots (scène-telling van 10)

**Universeel (10/10 — in elke scène):**
- `polyhaven/models/textures` — gedeelde model-texturenpool (grootste enkele bron)
- `polyhaven/textures/aerial_grass_rock` — grond/gras-basis
- `blokhutwinkel-textures/8192` — cabin-producttexturen
- `polyhaven/hdri` — wereld-verlichting

**Gedeeld over meerdere scènes:**

| Asset/map | Scènes | Noot |
|---|---|---|
| sketchfab/trees/five_birch_trees_pack | 3/10 | buitenbad, leeshoek, tuinkantoor |
| sketchfab/furniture/bistrot_table_and_chair | 2/10 | wijnterras, lavendelveld — **24 tex/scène, zwaarste prop** |
| sketchfab/topiary_hedge/hetz_midget_arborvitae | 2/10 | tuinkantoor, lavendelveld |
| sketchfab/trees/maple_tree_scan_trunk_4_lod | 2/10 | familietuin, theehuis |
| sketchfab/flowering_bushes/goldmound_spiraea | 2/10 | familietuin, pluktuin |
| sketchfab/flowering_bushes/multi_color_butterfly_bush | 2/10 | familietuin, pluktuin |
| sketchfab/flowering_bushes/bigleaf_hydrangea | 2/10 | familietuin, pluktuin |
| sketchfab/furniture/wooden_bench_low_poly | 2/10 | theehuis, pluktuin |
| sketchfab/decor/old_wicker_basket | 2/10 | lavendelveld, pluktuin |
| polyhaven/textures/paving_stones_64 | 2/10 | familietuin, pluktuin |
| polyhaven/models/wooden_lantern_01 | 2/10 | buitenbad, leeshoek |
| polyhaven/models/boulder_01 | 2/10 | theehuis, ochtendnevel |
| polyhaven/textures/wood_floor_deck | 2/10 | buitenbad, tuinkantoor |
| 3daistudio/lavender | 2/10 | leeshoek, lavendelveld (enige 3D-AI-Studio-asset) |

**Transient (6/10):** packed-temp `AppData/.../tmp*/textures` — uitgepakte packed-texturen (geen sourcing-familie).

**Eenmalig (1/10):** patio_tiles, flagstone_floor, brown_planks_09, outdoor_chair_scan_medpoly, birdbaths, picnic_table_low_poly, garden_shovel, Lantern_01, construction_gravel (MISSING), old_lantern, terracotta_pot, cc0_rose_arch, roses, field_poppy.

---

## 4. ⚠️ ONTBREKENDE TEXTUREN (te fixen — veroorzaakt magenta materialen)

**6 unieke ontbrekende texturen over 2 scènes; geen overlap.** Ontbrekende maps renderen als magenta/kapot materiaal in Cycles. De overige 8 geprobede scènes hebben `missing_images = []` en `broken_images = []`; alle blends: `errors=[]`, `libraries=[]` (geen linked libs, alles packed/lokaal).

| # | Textuur | Verwacht pad | Type | Getroffen scène |
|---|---|---|---|---|
| 1 | `wild_rooibos_bush_alpha_2k.png` | `assets/polyhaven/models/textures/` | alpha | dahlia_leeshoek |
| 2 | `wild_rooibos_bush_diff_2k.jpg` | `assets/polyhaven/models/textures/` | diffuse | dahlia_leeshoek |
| 3 | `wild_rooibos_bush_nor_gl_2k.exr` | `assets/polyhaven/models/textures/` | normal | dahlia_leeshoek |
| 4 | `wild_rooibos_bush_rough_2k.exr` | `assets/polyhaven/models/textures/` | roughness | dahlia_leeshoek |
| 5 | `T_vl0mfbllw_8K_B.png` | `assets/sketchfab/path_stones/construction_gravel_vl0mfbllw_8k_ue_raw/Textures/` | basecolor | jasmijn_theehuis |
| 6 | `T_vl0mfbllw_8K_N.png` | `assets/sketchfab/path_stones/construction_gravel_vl0mfbllw_8k_ue_raw/Textures/` | normal | jasmijn_theehuis |

**Blend-relatief pad (leeshoek):** `//..\..\..\assets\polyhaven\models\textures\`

**Fix-richting:** `wild_rooibos_bush` is een bestaand PolyHaven-model (`wild_rooibos_bush_2k.blend`) — de 4 maps horen in de gedeelde texturepool en moeten opnieuw beschikbaar/gepackt worden. `construction_gravel` is een sketchfab UE-raw-pakket; controleer of de `Textures/`-submap compleet is uitgepakt.

---

## 5. Duplicaten & verweesde downloads (opschoon-kandidaten — NIET nu verwijderen)

### 5.1 Duplicaten (byte-identiek, tenzij anders vermeld)

**blenderkit (~1,2 GB verspild):**
- Volledige folder `bicycle/` is subset van `fietsen-d2/` (Vintage_Bicycle 29,9M + City_bike 7,2M dubbel)
- `Fluffy_pampass_grass.blend` (201M) — pampas/ én border-planten/
- `Olive_tree.blend` (72M) — olijfboom/ én border-planten/
- `Lavender_Flower_Fence_Planter.blend` (158M) + `SJ-Radiant_Moonlight_Lavender_Petals.blend` (104M) — lavendel/ én border-planten/
- `Garden_Grass_Free.blend` (2,6M) + `Panorama_Garden.blend` (30,2M) — parasol/ én wandrek/
- `border-planten/` is grotendeels een verzamelbak van reeds elders aanwezige planten. Bijbehorende .glb's zijn eveneens gedupliceerd.

**sketchfab:**
- `uncategorized/forest_trail_path_gltf/` == `.../forest_trail_path_gltf (1)/` (~53M verspild)
- `Firewood.fbx` byte-identiek in `decor/stacked_firewood/` én `props/stacked_firewood/` (+ los `decor/firewood_stack.blend`, ander model, zelfde onderwerp → 3x firewood)
- 6 UE-raw-mappen leveren dubbele gltf-varianten (UE + non-UE); non-UE is de bruikbare voor Blender

**polyhaven:**
- `brass_candleholders` (2k 1,0M vs 4k 288M), `side_table_01` (2k 216K vs 4k 12M) — dubbele resoluties
- `grass_medium_02` en `tree_small_02` in models/textures: dubbele formatsets (jpg+png, exr+png)

**ambientcg:** `Bricks097_PH/` = onvolledige Poly-Haven-dubbel van `Bricks097/` → kandidaat verwijdering.

**3daistudio:** 3 .zip's (~28M, ~48%) zijn dubbels van reeds uitgepakte inhoud; `material.mtl` 3x byte-identiek.

**blokhutwinkel-textures:** `shingles-zwart.jpg` 2x (hi-res 5,1M vs lowres 726K); `luxehouse-onbehandeld` los vs in complete PBR-set.

**losse-assets-root:** mogelijke cross-familie dubbels — root-zips kunnen ook uitgepakt in `ambientcg/` resp. `blenderkit/` staan; te ontdubbelen.

### 5.2 Off-topic / foute downloads (grootste opschoonwinst)

**blenderkit `fietsen-d2/` (~2 GB non-fiets junk):** Dutch_Ship_Medium (424M), Dutch_Ship_Large_02 (425M), Power_bikes_lowrider_e_bike (398M), Fatbike_Lowrider (252M), Cargo_pants (65M), Old_Dutch_Windmill, Cargo_Container_Maersk, Retro_yellow_scooter.

Overige thema-mismatch: `regenton/` (Alien_Water_Nymph, Sci-Fi_Water-Tank), `laarzen/` (Rubber_Tracks_generator), `plaid/` (persoon, T-shirt-scan), `bamboe-scherm/` (pendant light, tray), `japanse-esdoorn/` (gebouwen), `border-planten/` (Pillow_Watercolor_flowers, Flowers_Pot 0,1M stub), `duingras/` (Desert_Procedural 0,2M stub, vazen).

### 5.3 Verweesde / onvolledige downloads

- **blenderkit:** `eettafel/` = alleen .glb geen .blend; `corten/` = materiaal (glb-loos verwacht, ok).
- **polyhaven:** `textures/painted_grass/` = 4 bestanden van 94 bytes (kapotte download, onbruikbaar).
- **sketchfab:** 6 `standard/*_nonUE.gltf` zonder eigen .bin (verwijzen naar ouder-map, losstaand onbruikbaar); 9 bron-ZIP's nog ingepakt.
- **props-beike:** `throw-pillows/` + `welcome-mat/` = geen model (zip niet uitgepakt); `tropische-bloemen/` = FBX zonder textures; `ev-charger-pole-pro-wall/` = OBJ+MTL zonder textures; `Bamboo Fence textures.zip` = textures zonder model (+ Blendswap-licentie te checken).
- **replicate-textures:** `urban/resp_A.json` + `resp_B.json` = mislukte API-calls (HTTP 401), restafval.
- **losse-assets-root:** `old-olive-tree.zip` = dubbel-gezipt (model in genest `source/olive-tree.zip`); alle 13 root-zips nog onuitgepakt.

---

## 6. BlenderKit-first-toets

Beleid sinds 3 jul: **BlenderKit-first bij nieuwe assets, minder prop-hergebruik.** Toetsing tegen het feitelijke scène-gebruik:

- **De pilotscènes leunen in de praktijk NIET op BlenderKit maar op PolyHaven + Sketchfab.** In de 10 geprobede scènes komt geen enkele blenderkit-map voor in de `used_image_dirs`; de universele bronnen zijn PolyHaven (models/textures, aerial_grass_rock, hdri) en de eigen blokhutwinkel-cabin-textures. Props komen uit sketchfab (bomen, meubels, bloeiende struiken) en 1 uit 3daistudio (lavender).
- **De 13 GB blenderkit-familie is grotendeels ongebruikt in R4.** Dit is deels aankoop-/wishlist-voorraad, deels off-topic junk (sectie 5.2). "Minder prop-hergebruik" wordt gehaald in de zin dat props breed gespreid zijn (veel 1/10-eenmalig), maar de zwaarste gedeelde prop (`bistrot_table_and_chair`, 24 tex) is sketchfab, niet vers per scène.
- **Compliance-spanning:** het BlenderKit-first-beleid stuurt aan op de veiligste licentiebron (royalty_free/cc_zero, geen credit), maar het feitelijke werk gebruikt vooral sketchfab (CC-BY, credit verplicht) — waarvan het merendeel ongetrackt is. Dit vergroot het compliance-risico i.p.v. het te verkleinen.

**Aanbevelingen (licentie/beleid):**
1. Verifieer per gebruikte sketchfab-asset de bronpagina-licentie vóór publicatie en leg vast in `CREDITS.md` (minimaal de 14 in sectie 3 genoemde in-gebruik-assets).
2. Vul `CREDITS.md` aan met `props-beike`, `3daistudio` en `replicate-textures` (nu volledig afwezig) + los het bamboe-hek Blendswap-risico op.
3. Overweeg voor terugkerende hotspot-props (bomen, bistroset, hagen) een CC0-alternatief uit PolyHaven i.p.v. de CC-BY-sketchfab-variant, om de credit-verplichting te elimineren.

---

## 7. Aanbevelingen voor volgende ronde (feitelijk)

1. **Fix eerst de 6 ontbrekende texturen (sectie 4)** vóór het opnieuw renderen van `dahlia_leeshoek` en `jasmijn_theehuis` — anders magenta materialen.
2. **Herbouw + probe de 3 ontbrekende scènes** (`magnolia_wintertuin`, `zonnebloem_zomeravond`, `zonnebloem_ochtendhoek`) via `apply_r4.py` op de R3-blend (keys in `_diag/r4_scenes.txt`); `magnolia_wintertuin_R4.blend` bestaat al maar is nog niet geprobed. Voeg hun asset-families daarna toe aan deze kaart.
3. **Opschoning (na akkoord Beike, niet autonoom):** grootste winst = ~2 GB off-topic junk in `fietsen-d2/` + ~1,2 GB blenderkit-duplicaten + `bicycle/` als geheel + sketchfab `forest_trail_path (1)/` + polyhaven `painted_grass/` (kapot). Totaal ~5 GB.
4. **Documenteer licentie centraal** (sectie 6): dicht het sketchfab-compliance-gat en registreer de 4 ongetrackte families.
5. **Standaardiseer de gedeelde bronnen:** PolyHaven `models/textures` + `aerial_grass_rock` + `hdri` en `blokhutwinkel-textures/8192` zijn de vaste basis van elke scène — behandel deze als kern-bibliotheek en houd de texturepool compleet (voorkomt herhaling van de `wild_rooibos_bush`-miss).
6. **Pak staging-archieven uit of ruim ze op:** `props-beike/downloads-4jul/`, de 9 sketchfab-ZIP's, de 13 root-zips en de 3 3daistudio-zips staan nu dubbel/ongesorteerd op schijf.

---

*Einde rapport. Bron: `_diag/weekend/probe_*.json` (10/13), `HANDOFF_R4_progress.md`, `assets/CREDITS.md`, `INDEX(_wishlist).txt` en schijfinventaris per familie.*
