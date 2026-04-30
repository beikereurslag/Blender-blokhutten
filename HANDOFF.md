# Blokhutwinkel Marketing Visuals — Project Handoff

**Datum**: 2026-04-30
**Status**: 2 van 3 pilots gerenderd, 1 in progress (.blend klaar, render niet gestart)
**Eigenaar**: Rene Kroon (`claude@connect-smart.nl`)
**Doel handoff**: Project verhuizen naar krachtigere PC met andere Claude account.

---

## 1. Wat zijn we aan het doen?

### Klant en context

**Blokhutwinkel.nl** (Zutphen, Nederland) — verkoper van blokhutten, tuinhuizen, veranda's, garages, paviljoens, carports. 10.000+ modellen, 100+ permanent in showroom. Hun eigen 3D-visualisatie is technisch CAD (uit hun config-tool), niet sfeervol.

### Originele opdracht
Een **Twinmotion** bestand met een blokhut moest "aangekleed" worden — een mooie tuin er omheen ontwerpen om de blokhut in **verschillende settings** te tonen voor verkoopvisuals.

### Onze switch
Rene wilde **Blender + Claude/MCP integratie** ipv Twinmotion, omdat:
- Real-time samenwerken via blender-mcp addon
- Asset-libraries Polyhaven + Sketchfab via MCP-tools
- Reproduceerbaar (1 cabin × meerdere stijlen × andere blokhuts)
- Cycles render kwaliteit voor verkoopvisuals

### Doel-output per blokhut
- 3-4 **stijlen** uit een 9-palette (Modern Minimalist / Cottage / Scandinavian / Forest / Terras+Hottub / Japanese Zen / Boerderij / Golden Hour / Winter)
- Per stijl: 2 angles
- = 6-8 finale 2560×1440 of 4K renders per blokhut
- Hergebruik scenes voor andere blokhuts in zelfde stijl

---

## 2. Bron-bestanden (door Rene aangeleverd)

**33 GLB-bestanden** in `/Users/beikereurslag/Documents/blokhutten GLB/`:
- Camelia (5 varianten: 250x300, +300, +400, met/zonder zijwand)
- Dahlia (4 varianten)
- Jasmijn (5 varianten)
- Lavendel (5 varianten)
- Lelie (5 varianten)
- Magnolia (1 variant: 300x200)
- Roosmarijn (3 varianten)
- Zonnebloem (5 varianten)

**KRITIEKE LEARNING**: Deze GLB-bestanden komen in **CENTIMETERS** binnen, niet meters.
Een "Magnolia 300x200" (3m × 2m) komt binnen als 300m × 200m als je gewoon importeert.
Altijd `bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))` toepassen na import.

**Andere kritieke learning bij import**:
- GLB bevat een geïmporteerde camera (op weird positie) — verwijder die altijd eerst
- Object hierarchy gebruikt EMPTY parents: shed, poles, roofbeams, walls, boards, roof, FlatRoofParent, foundationBeam — handig voor selecties per onderdeel
- Materialen zitten ingebakken in GLB (basetexture-firstLayer-* voor door, foundationBeam, roofBeam, roofboard, roofPlate, wall, plus epdm voor dak)

---

## 3. Tools en setup vereist op nieuwe PC

### Blender
- **Versie**: 4.0+ (we draaiden op 5.1.1 — gebruikt nieuwe Eevee als standaard 'BLENDER_EEVEE')
- Op oudere Blender 4.x: gebruik `BLENDER_EEVEE_NEXT` voor preview
- **Cycles GPU**: Metal (M-series Mac) of CUDA/OptiX (NVIDIA)
- **Color management**: View Transform `Filmic`, Look `Medium High Contrast`

### blender-mcp addon (ahujasid)
- Repo: https://github.com/ahujasid/blender-mcp
- Versie tijdens werk: 1.5.5
- Installeren: download `addon.py`, `Edit → Preferences → Add-ons → Install...`
- Enable in 3D Viewport sidebar (N-key → tab "BlenderMCP")
- **Connect to MCP server** klikken (port 9876)
- **Use assets from Poly Haven** ✅ aanvinken
- **Use assets from Sketchfab** ✅ aanvinken + **Sketchfab API token** invoeren
  - Token krijg je op `sketchfab.com/settings/password` → API token kopieren
- Hyper3D Rodin / Hunyuan 3D — uit (alleen voor AI-generated assets als laatste redmiddel)
- **`DISABLE_TELEMETRY=true`** env var zetten voor je Claude Code start (anders gaan prompts/code/screenshots naar Ahuja's server)

### MCP server (op Claude/Claude Desktop)
- `uvx blender-mcp` — Python 3.10+ vereist, `uv` package manager
- Configureer in Claude's MCP config (`claude_desktop_config.json` of `.mcp.json` in project)
- Tools die beschikbaar moeten zijn:
  - `mcp__blender__get_scene_info`
  - `mcp__blender__execute_blender_code`
  - `mcp__blender__get_viewport_screenshot`
  - `mcp__blender__download_polyhaven_asset`
  - `mcp__blender__search_polyhaven_assets`
  - `mcp__blender__set_texture` (NB: bug in Blender 5.x — node `ShaderNodeSeparateRGB` is hernoemd naar `ShaderNodeSeparateColor`)
  - `mcp__blender__search_sketchfab_models`
  - `mcp__blender__download_sketchfab_model`
  - `mcp__blender__get_object_info`

### Werkdirectory
- Source GLBs: `/Users/beikereurslag/Documents/blokhutten GLB/`
- Output: `/Users/beikereurslag/Documents/Blokhutwinkel/<cabin>/<style>/`
- **Niet** in `/Users/beikereurslag/Documents/event-branding/` — dat is een ander project

---

## 4. Status van 3 pilots

### ✅ Pilot 1: Magnolia 300×200 — Modern Minimalist
**Locatie**: `~/Documents/Blokhutwinkel/Magnolia-300x200/style-modern/`

**Files**:
- `magnolia_modern.blend` (template voor andere stijlen op zelfde cabin)
- `magnolia_modern_FINAL_v4_2560x1440.png` — laatste finale (~17MB)
- Versies v1 t/m v8 PREVIEW PNGs (iteraties)

**Scene specs**:
- Hardscape: gravel ground (forest_ground_01) + raised wood deck (10cm plinth) + cortenstaal edging + flush stepping stones (60cm spacing) + cedar slat fence 14m breed
- 3 plant beds met mulch + cortenstaal edging
- 42 echte planten in beds (3-laagse: tall grass back, fern mid, low fern groundcover)
- 1 anthracite pot left of door + 1 mirror pot right (was side table — repositioned)
- Pots gevuld met anthurium + fern combo (lush leaves)
- **Sketchfab Wooden Lounge Chair** (UID `574ee9c52ef94b518ead1606b90b563e`, CC Attribution, varvashenko.lida) op deck
- 1 sierboom (tree_small_02) achter cabin als focal point
- 16 extra trees als groene backdrop (rondom cabin)
- HDRI: `kloofendal_43d_clear` (open landschap, geen pergola)

**Camera**: 11m afstand, 22° angle, 35mm lens, 1.65m hoogte

**User-feedback nog open**:
- Chair orientation "het is een begin" — accepteerd maar niet perfect
- "Achtergrond mag wel wat groener" → v4 lost dit op met 16 extra trees

---

### ⚠️ Pilot 2: Lelie 400×250 + 300 + zijwand — English Cottage
**Locatie**: `~/Documents/Blokhutwinkel/Lelie-400x250-300-zijwand/style-cottage/`

**Files**:
- `lelie_cottage.blend`
- `lelie_cottage_FINAL_2560x1440.png` (~18MB)

**Scene specs**:
- Cabin 7.4m × 2.9m × 2.3m (groot model met extension + zijwand)
- Cabin door world: (1.48, 1.25)
- 4-segment meandering cobblestone path naar deur (cottage feel)
- 5 flower beds met cottage-density planting (tegen voorgevel + 2 zijbeds + back bed)
- Mixed cottage planting: ferns + anthurium + celandine + dandelion + flower_empodium + grass
- 10 trees (tree_small_02 + jacaranda_tree mix) flanking + back
- DIY wooden bench (1.5m breed × 0.85m hoog met legs/seat/back/rails)
- 2 terracotta pots flanking voordeur met anthurium plants
- DIY lantaarn (zwart staal pole + glass head met emission)
- Lawn (forrest_ground_01) als ground

**HDRI**: `studio_garden` ← **PROBLEEM**

**🐛 ISSUE**:
- Render is **VEEL TE DONKER**
- studio_garden HDRI heeft strong shadows, te weinig diffuus licht
- Cabin texture barely readable
- Cottage flower-detail valt weg in schaduw

**Fix voor v2**:
- HDRI vervangen door `kloofendal_43d_clear` of `qwantani_dusk_2` met strength 1.5
- OF studio_garden behouden maar strength verhogen naar 2.0 in World shader

**Te overwegen extra polish**:
- Add white picket fence (DIY met thin slats)
- Add climbing roses tegen wall (gemaakt van grass scaled vertical?)
- Add rozenboog over path (DIY pergola)

---

### 🟡 Pilot 3: Camelia 250×300 + 300 + zijwand — Scandinavian + Hottub
**Locatie**: `~/Documents/Blokhutwinkel/Camelia-250x300-300-zijwand/style-scandi/`

**Files**:
- `camelia_scandi.blend` ← **WEL OPGESLAGEN, scene compleet gebouwd**
- ❌ **GEEN render PNG nog** (user interrupted vóór de render commando)

**Scene specs (in .blend al klaar)**:
- Cabin 5.93m × 3.41m × 2.37m
- Cabin door world: (-1.35, 3.82)
- Hardscape:
  - Stone patio (rocky_terrain texture) voor voordeur 4.5m × 2.5m
  - Dark Shou Sugi Ban deck (near-black wood) 3m × 2.5m naast patio
  - Cedar hottub Ø1.8m × 0.95m + water-disc met 0.05 roughness, blue-green color
- 7 boulders (icosphere-based, scattered langs zijden)
- 13 fir trees (fir_tree_01_a_LOD0) — **WAARSCHUWING**: Polyhaven fir is 19m tall! Ik heb ze 0.5x geschaald naar ~10m. Nog kan dit te groot zijn voor sommige cameras
- 4 small trees (tree_small_02_LOD0) als side accents
- 36 underplant ferns + grass tussen boulders en op forest floor
- Forest floor (forrest_ground_01)

**HDRI**: `qwantani_dusk_2` (golden hour dusk — past bij Scandinavian moody)

**Camera (al ingesteld in .blend)**:
- Target (0, 2.5, 1.4)
- Position: 14m distance, 30° angle, 1.7m height, 35mm lens

**TO DO**: Open `camelia_scandi.blend`, gewoon `bpy.ops.render.render(write_still=True)` met output path:
```
/Users/beikereurslag/Documents/Blokhutwinkel/Camelia-250x300-300-zijwand/style-scandi/camelia_scandi_FINAL_2560x1440.png
```

---

## 5. Kritieke learnings & valkuilen

### Schaal & import (verplichte boilerplate elke nieuwe blokhut)

```python
import bpy
from mathutils import Vector

# Import GLB
filepath = "/Users/beikereurslag/Documents/blokhutten GLB/Magnolia 300x200.glb"
bpy.ops.import_scene.gltf(filepath=filepath)

# 1. Verwijder geïmporteerde camera
if "camera" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["camera"], do_unlink=True)

# 2. Schaal 0.01x (cm → m)
bpy.ops.object.select_all(action='SELECT')
bpy.context.scene.cursor.location = (0,0,0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# 3. Centreer cabin op origin met bottom op Z=0
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
min_co = Vector((float('inf'),)*3); max_co = Vector((float('-inf'),)*3)
for o in meshes:
    for v in o.bound_box:
        wv = o.matrix_world @ Vector(v)
        for i in range(3):
            min_co[i] = min(min_co[i], wv[i])
            max_co[i] = max(max_co[i], wv[i])
cx = (min_co.x+max_co.x)/2; cy = (min_co.y+max_co.y)/2
offset = Vector((-cx, -cy, -min_co.z))
for o in bpy.context.scene.objects:
    if o.parent is None:
        o.location += offset

# 4. Vind voordeur positie
for o in bpy.data.objects:
    if 'DEURBASIC' in o.name and o.type == 'MESH' and 'doorhandle' not in o.name and 'scharnier' not in o.name:
        coords = [o.matrix_world @ Vector(c) for c in o.bound_box]
        cx = sum(c.x for c in coords)/8
        cy = sum(c.y for c in coords)/8
        print(f"Door: ({cx:.2f}, {cy:.2f})")
        break
```

### Render timeouts (NIET een fout — gewoon weten)

`bpy.ops.render.render(write_still=True)` blokkeert tot render klaar is. Bij Cycles 2560×1440 + 256 samples + zware scene = 5-10 min. **MCP-communicatie krijgt timeout** maar de render gaat door. Workaround:

```bash
# Wacht in shell tot PNG file > 5MB
until [ -f "$OUTPUT_PNG" ] && [ "$(stat -f%z "$OUTPUT_PNG" 2>/dev/null || echo 0)" -gt 5000000 ]; do sleep 30; done
```

### Sketchfab licenties (commercial use!)

| Licentie | Mag voor blokhutwinkel-marketing? |
|---|---|
| **CC0** | ✅ Ja, beste keus |
| **CC Attribution** | ✅ Ja, attributie verplicht |
| **CC Attribution-ShareAlike** | ⚠️ Viral — vermijd |
| **CC Attribution-NonCommercial** | ❌ NIET gebruiken |
| **CC Attribution-NoDerivs** | ❌ NIET gebruiken (geen aanpassen) |
| **Free Standard** | ❌ Vereist betaalde license voor commercial |

Bekende val: `xfrog` plant-modellen op Sketchfab zijn allemaal CC BY-NC-ND — niet bruikbaar.

### `set_texture` MCP-tool werkt NIET in Blender 5.x

Gebruikt oude `ShaderNodeSeparateRGB` die hernoemd is naar `ShaderNodeSeparateColor`. Bouw materialen handmatig met `execute_blender_code`:

```python
mat = bpy.data.materials.new("name")
mat.use_nodes = True
nt = mat.node_tree
# Build TexImage → Principled BSDF → Output graph
```

### Plant placement regels (uit landscape architecture research)

1. **Plants ALLEEN in defined bed-zones** — nooit op gravel/lawn los
2. **Bed-overgang**: corten staal edging 4mm × 100mm tussen zones
3. **3-laagse opbouw verplicht**:
   - Achter (120-180cm): tall grass, hoge struiken
   - Midden (60-90cm): lavendel, mid-height shrubs  
   - Voor (20-40cm): groundcover (sedum, kruipende thijm, ferns)
4. **Cluster theory**: oneven aantallen (3, 5, 7) per soort, triangulair niet grid
5. **Density**: 5-8 plants/m² perennial bed, 1 boom per 15-25m²
6. **Snap-to-ground**: Polyhaven plants hebben origin op base/trunk Z=0. Plaats op `bed_z = 0.05` (top of mulch) of via raycast snap

### Hardscape regels

1. **Deck +10cm boven gravel-niveau** (echte plinth, geen coplanair)
2. **Stepping stones FLUSH met gravel** (niet erbovenuit), 60cm spacing
3. **Path naar voordeur**: 90-120cm breed (twee personen)
4. **Cabin niet centered**: rule of thirds — cabin op 1/3 lijn

### Camera regels (verkoopvisuals)

1. **Hoogte**: 1.5-1.6m (ooghoogte volwassene)
2. **Focal length**: 35-50mm full-frame
3. **Angle**: 22-35° van gevel-as (3/4 hero shot)
4. **Cabin fills 50-65% van breedte**
5. **Min 2m gravel/lawn** vóór cabin in beeld
6. **Max 3 staffage-categorieën** (chair + pots + lantaarn — meer = rommel)

### Lighting

- **HDRI overcast** voor product-clarity (`kloofendal_partly_cloudy`, `kloofendal_43d_clear`)
- **HDRI golden hour** voor lifestyle hero (`qwantani_dusk_2`, `the_sky_is_on_fire`)
- **HDRI cottage**: `studio_garden` werkt mits **strength 1.5-2.0** (anders te donker — onze fout in pilot 2)
- Cycles **256 samples + OpenImageDenoise + Adaptive Sampling**

### Common AI-render anti-patterns die we hebben gemaakt en moeten vermijden

| Fout | Hoe het misgaat | Fix |
|---|---|---|
| ❌ UV-sphere "boxwoods" | Lijken op gym-ballen, niet planten | Use real Polyhaven/Sketchfab plant meshes |
| ❌ Grass-tufts op gravel | "Vliegend gras" | Plants ALLEEN in beds |
| ❌ Solid green plane als hedge | Plastic-look | GN scatter op displaced plane OR meerdere boom-instances |
| ❌ Tropische planten in modern Dutch garden | Calathea/Anthurium op gravel-zone | Houd ecology in mind, of gebruik ze als visuele leaf-mass IN bed |
| ❌ Stepping stones boven gravel-niveau | Onnatuurlijk | Z=0.005 = flush of ingegraven |
| ❌ Beds die DOOR deck snijden | Plants groeien door vloer | Beds moeten STOPPEN waar deck begint |
| ❌ DIY chair zonder slat-detail | Klompig, fake proporties | Gebruik Sketchfab CC0/CC BY chair model |
| ❌ Fence te smal | "Halve heg" | Verbreed naar 14-20m, edge-to-edge |
| ❌ Te druk in foreground | Rommel | Max 3 categorieën objects |
| ❌ Object parenting bug | Alle parts naar parent-origin verplaatst | Bouw met direct world-coords + manual rotation, geen parent_inverse issue |
| ❌ Polyhaven fir 19m groot | Reuze-bomen | Scale 0.5x voor realistic 10m |
| ❌ HDRI te donker (studio_garden) | Pilot 2 issue | Strength 1.5-2.0 of andere HDRI |
| ❌ Random tree silhouette planes | Groene blokken sticking up | Gebruik meerdere echte tree mesh instances |

### Object parenting issue (genuinely had this bug)

**Don't do this** (locations all collapse to parent origin):
```python
empty = bpy.context.active_object  # parent
child = ... 
child.parent = empty
# child.location reinterpreted as parent-relative → moved to wrong place
```

**Do this** (direct world coords with manual rotation math):
```python
def add_part(name, dims, local_xyz, rot_local_x=0):
    cos_r = math.cos(rot_z); sin_r = math.sin(rot_z)
    lx, ly, lz = local_xyz
    wx = chair_x + lx * cos_r - ly * sin_r
    wy = chair_y + lx * sin_r + ly * cos_r
    wz = chair_z + lz
    bpy.ops.mesh.primitive_cube_add(size=1, location=(wx, wy, wz))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = dims  # KEEP scale, no apply!
    obj.rotation_euler = (rot_local_x, 0, rot_z)
```

OF gebruik `transform_apply(scale=True)` — maar **NIET combineren** met scale-op-object om locatie te bewaren. Als je scale wil applyen: zorg dat object.location klopt vóór apply.

---

## 6. Wiki documenten (alle research + principes)

Locatie: `/Users/beikereurslag/Documents/Vault/Claude/wiki/` (Obsidian vault)

**Concepts** (workflow + principes):
- `concepts/Garden Style Palette for Cabin Visuals.md` — 9 stijlen matrix met materialen/planten/props per stijl
- `concepts/Garden Cabin Scene Dressing Principles.md` — eerste research naar layering, zones, props
- `concepts/Landscape Architecture Rules for Cabin Visuals.md` — concrete numerieke regels (m, cm, plant-spacing)
- `concepts/Blender Environment Art Best Practices.md` — Blender-techniek snap-to-ground, GN scatter, hedge construction
- `concepts/Blender Scene Composition Workflow via MCP.md` — iteratie-loop Claude+user
- `concepts/Custom Asset Import via execute_blender_code.md` — workaround voor missende MCP import-tool
- `concepts/Geometry Nodes Scattering for Outdoor Scenes.md` — moderne scatter techniek
- `concepts/Cycles vs Eevee Next for ArchViz.md` — render engine keuze

**Entities**:
- `entities/Blokhutwinkel.nl.md` — klant
- `entities/Polyhaven.md` — primaire CC0 asset bron
- `entities/Sketchfab.md` — secundaire 3D-model bron met license-matrix

**Sources**:
- `sources/Blokhutwinkel.nl - Product Categories.md` — productcatalogus
- `sources/Polyhaven - HDRI and Asset Library.md` — asset shortlist
- `sources/Sketchfab - CC Library.md` — license-matrix
- `sources/HDRMaps - Realistic HDRI Lighting Exterior ArchViz Blender.md` — Cycles HDRI workflow
- `sources/ahujasid blender-mcp.md` — bestaande MCP-tool docs

**Synthesis**:
- `questions/Research - Blender + Blokhutten aankleding.md` — overall synthesis met findings + open questions

**Memory** (auto-memory persistent across conversations):
- `feedback_blokhutwinkel_glb_scale.md` — GLB → 0.01x scale rule

**Niet sync'd?** Als de wiki niet meegaat naar de andere PC: alle essentiële regels staan al in dit HANDOFF.md.

---

## 7. Feedback van Rene (verzameld)

Genoteerd in chronologische volgorde, voor consistentie tussen sessies:

1. **"Vliegend gras op gravel"** → planten alleen in beds (verplicht)
2. **"Stoel die totaal niet klopt"** → DIY chair was te klompig, vervangen door Sketchfab Wooden Lounge Chair (CC BY)
3. **"Random tegel voor deur"** → deck moet duidelijk afgewerkt met edging + plinth +10cm
4. **"Gras op grind"** → ecology mismatch, geen plants op gravel-zone
5. **"Geen hele heg omranding"** → fence verbreden naar 14m+ edge-to-edge
6. **"Beds die door deck snijden"** → bed-positions moeten cabin-shape volgen, niet door hardscape
7. **"Random grijze pot midden op vloer"** → pots gepaird L+R van deur (matched pair, mirror)
8. **"Schaarse plant in pot"** → vervangen door anthurium + fern combo (lush)
9. **"Stoel verkeerd om"** → moet kijken NAAR tuin, rugleuning AAN cabin-zijde (Z=180° rotation needed na X=-90 FBX correction)
10. **"Achtergrond mag wat groener"** → meer trees in backdrop, hedge mass tegen fence
11. **"Mag meer in"** → meer dan 1 boom, meer detail
12. **"Achtergrond raar qua schaal"** → HDRI met pergola was uit-proportie, kloofendal_43d_clear werkt beter
13. **"Aparte folder ipv event-branding"** → /Documents/Blokhutwinkel/ ipv onder event-branding
14. **"Maakt niet uit dat het lang duurt"** → user accepteert iteratief werk
15. **"Als hij goed staat mag je 2560 renderen"** → 2560×1440 is finale-resolutie, 4K mag bij budget
16. **"Het is een begin"** → user accepteert imperfecties bij eerste pilot, fixed in next iteratie

---

## 8. Wat moet er nog gebeuren (volgorde)

### Onmiddellijk (op nieuwe PC)
1. **Verifieer Blender + MCP setup** werkt:
   - Open Blender, addon connected, port 9876
   - Sketchfab API token in field
   - Polyhaven enabled
2. **Render Camelia Scandi**:
   - Open `~/Documents/Blokhutwinkel/Camelia-250x300-300-zijwand/style-scandi/camelia_scandi.blend`
   - Verify scene is intact (cabin + hottub + 13 firs + boulders)
   - Set output path naar `camelia_scandi_FINAL_2560x1440.png` in zelfde folder
   - Cycles 256 samples + OIDN, 2560×1440
   - Render
3. **Lelie Cottage v2** (donker probleem fixen):
   - Open `~/Documents/Blokhutwinkel/Lelie-400x250-300-zijwand/style-cottage/lelie_cottage.blend`
   - In World shader: HDRI strength **2.0** (was 1.0)
   - OF wissel HDRI naar `kloofendal_43d_clear` (downloaden via MCP polyhaven download)
   - Re-render naar `lelie_cottage_FINAL_v2_2560x1440.png`

### Optioneel (volgende stap)
4. **Magnolia in andere stijl** (om zelfde cabin in andere context te tonen):
   - Open `~/Documents/Blokhutwinkel/Magnolia-300x200/style-modern/magnolia_modern.blend`
   - Save As → `~/Documents/Blokhutwinkel/Magnolia-300x200/style-cottage/magnolia_cottage.blend`
   - Wijzig: HDRI naar studio_garden (strength 2.0), corten staal naar wit picket fence, gravel naar lawn, koel chair naar warme bench, voeg flowers toe (celandine, dandelion)
   - Render
5. **Andere blokhut + andere stijl**:
   - Bv. Zonnebloem 300x300 + 400 + zijwand → Boerderij/Landelijk style
   - Volg het import-boilerplate uit sectie 5

### Open vragen voor Rene
- Welke cabin x stijl combinaties zijn prioriteit?
- 4K render-budget (4× zoveel render-tijd, ~30 min per scene)?
- Brand-rules voor blokhutwinkel — kleuren / logo / watermerk?
- Welke marketing-context (web carousel / print / social)?

---

## 9. Hoe over te zetten naar nieuwe PC

### ⚠️ KRITIEK: textures zijn NIET opgeslagen IN de .blend files

Polyhaven en Sketchfab assets die we via MCP downloadden, staan in **tijdelijke macOS folders** (`/var/folders/zl/...tmp...`). De .blend files refereren naar die paths. Op een nieuwe PC bestaan die paths niet.

**Twee oplossingen** (kies er één voordat je transferreert):

**Optie A — Pack resources IN de .blend (aanbevolen):**

Open elke .blend file in Blender op deze laptop. Per file:
1. `File → External Data → Pack Resources` (knop in menu)
2. `File → Save` (overschrijf .blend)
3. .blend wordt 50-200MB groter, maar fully portable

Doen voor:
- `~/Documents/Blokhutwinkel/Magnolia-300x200/style-modern/magnolia_modern.blend`
- `~/Documents/Blokhutwinkel/Lelie-400x250-300-zijwand/style-cottage/lelie_cottage.blend`
- `~/Documents/Blokhutwinkel/Camelia-250x300-300-zijwand/style-scandi/camelia_scandi.blend`

**Optie B — Re-download via MCP op nieuwe PC:**

Op nieuwe PC: open .blend → textures missen → MCP server opnieuw downloaden van Polyhaven (zelfde asset_ids). Wel nieuwe Sketchfab download nodig (UID `574ee9c52ef94b518ead1606b90b563e` voor Wooden Lounge Chair). Lijst van gebruikte assets:

**Polyhaven HDRIs gebruikt**:
- `kloofendal_43d_clear` (Magnolia)
- `studio_garden` (Lelie)
- `qwantani_dusk_2` (Camelia)

**Polyhaven textures gebruikt**:
- `gravel_stones` (Magnolia ground gravel)
- `wood_floor_deck` (Magnolia deck)
- `aerial_grass_rock` (Magnolia eerste ground texture)
- `cobblestone_floor_07` (Lelie path)
- `brick_wall_006` (Lelie alt)
- `forrest_ground_01` (Lelie + Camelia ground)
- `rocky_terrain` (Camelia stone patio)

**Polyhaven models gebruikt**:
- `tree_small_02` (Magnolia + Lelie)
- `jacaranda_tree` (Lelie)
- `fir_tree_01` (Camelia, schaal 0.5x)
- `grass_medium_02` (alle pilots)
- `fern_02` (Lelie + Camelia)
- `anthurium_botany_01` (alle pilots)
- `celandine_01` (Lelie + Magnolia)
- `dandelion_01` (Lelie)
- `flower_empodium` (Lelie)
- `cheiridopsis_succulent` (Magnolia eerste versie)

**Sketchfab models gebruikt**:
- `574ee9c52ef94b518ead1606b90b563e` — Wooden Lounge Chair (CC BY, varvashenko.lida) → Magnolia

### Bestanden die mee moeten
1. **GLB source files** (~210MB):
   - `/Users/beikereurslag/Documents/blokhutten GLB/` — alle 33 GLBs
2. **Output renders + .blend templates** (~150MB raw, of 400-600MB als textures gepackt):
   - `/Users/beikereurslag/Documents/Blokhutwinkel/` — heel deze map (inclusief HANDOFF.md)
3. **Optioneel — wiki research**:
   - `~/Documents/Vault/Claude/wiki/concepts/` — alle 8 concept-pages
   - `~/Documents/Vault/Claude/wiki/entities/`
   - `~/Documents/Vault/Claude/wiki/sources/`
   - `~/Documents/Vault/Claude/wiki/questions/Research - Blender + Blokhutten aankleding.md`

### Methode
- USB-stick / externe schijf
- iCloud / Dropbox / Google Drive sync van Documents-folders
- AirDrop (alleen bij Mac → Mac)
- SCP/rsync naar NAS dan terug

### Op nieuwe PC (zelfde Mac of Windows)
1. Bestanden plaatsen op zelfde paths (vervang `beikereurslag` door nieuwe username)
2. **Belangrijk: paden in .blend files updaten** als pad anders is:
   - Blender: `File → External Data → Find Missing Files`
   - Of edit .blend met script om paths te update
3. Python paden in dit document aanpassen
4. Blender + addon installen
5. MCP server installen + configureren
6. Connect en testen met `mcp__blender__get_scene_info`

---

## 10. Tips voor de nieuwe Claude (op andere account)

### Lees eerst
- Dit `HANDOFF.md` volledig
- `~/Documents/Vault/Claude/wiki/concepts/Landscape Architecture Rules for Cabin Visuals.md`
- `~/Documents/Vault/Claude/wiki/concepts/Blender Environment Art Best Practices.md`
- (Als wiki niet meekomt: alle regels staan ook in dit HANDOFF in sectie 5)

### Werkwijze
- Werk **iteratief**: build → screenshot → user feedback → adjust → render
- **`get_viewport_screenshot`** na elke significante wijziging om visueel te checken
- **Save .blend voor elke render** (zo kan je terugvallen bij issues)
- **Lower-res preview eerst** (1920×1080, 128 samples) → user OK → finale 2560×1440 256 samples

### Zonde-vermijders
- Niet **alle plants in 1 chunk** plaatsen — split in batches
- Niet **DIY furniture** zonder echt research naar specs (proporties)
- Niet **same-color objects** zonder material variatie (saai)
- Niet **alles centered** (rule of thirds!)
- Niet **te druk** (max 3 staffage-categorieën)

### Goeie patronen
- Sketchfab eerst zoeken voor furniture (filter CC0/CC BY)
- Polyhaven eerst voor textures + planten + HDRIs (altijd CC0)
- Multiple tree instances voor backdrop, niet faux silhouette planes
- Cortenstaal als modern accent (basecolor #6B3A1F, roughness 0.6, metallic 0.4)
- Anthurium + fern combo voor lush pot-fill
- Studio_garden HDRI **alleen met strength 2.0** voor cottage
- Kloofendal_43d_clear voor cleaner sky background

---

## 11. Quick recovery: hoe een werkende scene te bouwen

Voor als je from-scratch moet starten op de nieuwe PC:

```python
import bpy
import math
import random
from mathutils import Vector

# 1. Wipe + setup
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'
scene.cycles.samples = 256
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium High Contrast'
scene.render.resolution_x = 2560
scene.render.resolution_y = 1440

# 2. Import + scale + center cabin
filepath = "/path/to/cabin.glb"
bpy.ops.import_scene.gltf(filepath=filepath)
if "camera" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["camera"], do_unlink=True)
bpy.ops.object.select_all(action='SELECT')
bpy.context.scene.cursor.location = (0,0,0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
# (centering boilerplate from section 5)

# 3. Ground 30x30m
bpy.ops.mesh.primitive_plane_add(size=30, location=(0,0,-0.01))

# 4. Download HDRI + textures via MCP
# Use mcp__blender__download_polyhaven_asset

# 5. Build hardscape (deck, beds, fence) — see pilots above

# 6. Place plants (3-laagse, in beds only)

# 7. Place furniture (Sketchfab CC BY + DIY)

# 8. Camera (35mm, 1.65m, 22-35° angle, 11-14m dist)

# 9. Render
bpy.ops.wm.save_as_mainfile(filepath="path/to/save.blend")
bpy.ops.render.render(write_still=True)
```

---

**Einde handoff. Veel succes op de nieuwe PC.** 

Laatste tip: **vraag user altijd om viewport-screenshot bevestiging** vóór je een 5-10 min Cycles-render start. Bespaart re-renders.
