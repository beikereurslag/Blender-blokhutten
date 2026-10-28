# WEEKEND-OPDRACHT — Blokhut Blender renders (autonoom, 20–23 jun 2026)

> Beike is het hele weekend weg. Plak dit hele bestand als **eerste bericht** in een nieuwe Claude Code sessie
> in `C:\Users\beike\Documents\Blender-blokhutten`. De sessie werkt dit dan autonoom af, scene voor scene,
> en logt alles zodat Beike maandag precies ziet wat er gebeurd is.
>
> **Scope-toggle (lees vóór plakken):** standaard draaien Fase 1 → 2 → 3. Wil je minder, verwijder een fase
> uit dit bestand vóór je het plakt. Fase 1 alleen = veilige eindrenders (~30 min). Fase 1+2 = de echte
> weekend-vulling (kwaliteit-v2 met zelfkritiek). Fase 3 = extra camerahoeken als er tijd over is.

---

## 0. Wie je bent dit weekend & de gouden regels

Je bent Claude Code, autonoom aan het werk aan het blokhut-marketing-renderproject van **Beike**
(spreek hem in logs/samenvattingen aan als "Beike"). Beike is weg — **dus deze keer ben JIJ de ogen.**

> ⚠️ **Regel-omkering voor dit weekend.** Normaal kijkt Beike live mee in Blender en maak je geen eigen
> screenshots. Nu is hij er niet. Dus: **render headless → lees de PNG zelf met de Read-tool → beoordeel →
> itereer.** Zonder de render terug te kijken kun je kwaliteit niet beoordelen. Dit is expliciet toegestaan
> en zelfs verplicht dit weekend.

Gouden regels (overtreed deze nooit):
1. **Headless CLI only.** Gebruik NIET de Blender-MCP (zware scenes crashen via MCP). Render via
   `blender.exe -b ... --python ...`. De MCP-Blender hoeft niet open te staan.
2. **Sequentieel renderen.** Nooit twee renders tegelijk → parallelle GPU-renders crashen (CUDA illegal
   memory access). Eén render per keer, wacht tot hij klaar is.
3. **Niet-destructief.** Raak de bestaande `*.blend` en `*_REALISM_PREVIEW.png` niet over. Eindrenders en
   v2-werk gaan naar NIEUWE bestanden (zie naamgeving per fase). Verwijder nooit iets automatisch
   (geen cleanup-scripts, geen `rm` van bestaande assets/renders).
4. **Geen `/tmp` / geen temp-locaties.** Alle output op vaste paden in de repo.
5. **Valideer via code, niet op gevoel.** `audit()` / bbox / `_diag_generic.py`, en lees daarna de PNG terug.
6. **Niets verzinnen.** Geen marketing-claims/stats/jaartallen bedenken. Dit weekend gaat puur om renders.
7. **Commit per scene** zodat niets verloren gaat als de sessie sneuvelt (zie §5).
8. **Bij een blokkade:** los het op of log een kant-en-klaar copy-paste-command in `RENDER_STATUS.md`;
   stop niet de hele pipeline om één scene.

---

## 1. Projectstatus (waar we staan)

- **16/16 scenes** hebben een goedgekeurde realisme-preview (`<scene>_REALISM_PREVIEW.png`,
  1600×900 / ~130 samples). Kwaliteitsniveau is "goed genoeg, kan beter" (Beike akkoord).
- Alleen **Zonnebloem Zomeravond** heeft al een finale 2560×1440 (`zonnebloem_zomeravond_HERO_2560x1440.png`).
- De rest heeft **nog geen finale 2560×1440** → dat is Fase 1.
- Bekende v2-polish die bewust nog NIET is toegepast (consistentie): **AgX i.p.v. Filmic**, **DoF**,
  **gras ontzadigen**, **flagstones donkerder**. Dat is Fase 2.

### De 16 scenes (blend → output-map). `<R>` = `C:\Users\beike\Documents\Blender-blokhutten`

| # | Scene | .blend (relatief aan `<R>\`) | AgX-look (Fase 2) |
|---|---|---|---|
| 1 | Camelia Buitenbad | `pilots\Camelia-250x300-300-zijwand\style-hot-tub-premium\camelia_buitenbad.blend` | base (blue hour) |
| 2 | Camelia Wijnterras | `pilots\Camelia-250x300-300-zijwand\style-mediterraan\camelia_wijnterras.blend` | high (namiddag) |
| 3 | Dahlia Tuinkantoor | `pilots\Dahlia-250x250-300-zijwand\style-modern-urban-cottage\dahlia_tuinkantoor.blend` | high (ochtend) |
| 4 | Dahlia Leeshoek | `pilots\Dahlia-250x250-300-zijwand\style-scandi\dahlia_leeshoek.blend` | base (zacht daglicht) |
| 5 | Jasmijn Familietuin | `pilots\Jasmijn-300x250-300-zijwand\style-klassiek-familie\jasmijn_familietuin.blend` | high (middag) |
| 6 | Jasmijn Theehuis | `pilots\Jasmijn-300x250-300-zijwand\style-japandi\jasmijn_theehuis.blend` | base (ochtend/japandi) |
| 7 | Lavendel Lavendelveld | `pilots\Lavendel-400x300-400-zijwand\style-mediterraan\lavendel_lavendelveld.blend` | high (golden hour) |
| 8 | Lavendel Pluktuin | `pilots\Lavendel-400x300-400-zijwand\style-boerderij\lavendel_pluktuin.blend` | base (overcast) |
| 9 | Lelie Ochtendnevel | `pilots\Lelie-400x250-300-zijwand\style-forest-wilderness\lelie_ochtendnevel.blend` | base (mist/dageraad) |
| 10 | Lelie Avondkubus | `pilots\Lelie-400x250-300-zijwand\style-modern\lelie_avondkubus.blend` | base (blue hour) |
| 11 | Magnolia Groene Long | `pilots\Magnolia-300x200\style-eco-groendak\magnolia_groene_long.blend` | high (helder) |
| 12 | Magnolia Wintertuin | `pilots\Magnolia-300x200\style-scandi\magnolia_wintertuin.blend` | base (zacht daglicht) |
| 13 | Roosmarijn Zentuin | `pilots\Roosmarijn-200x300-400-zijwand\style-japanese-zen\roosmarijn_zentuin.blend` | base (overcast) |
| 14 | Roosmarijn Kruidenterras | `pilots\Roosmarijn-200x300-400-zijwand\style-mediterraan\roosmarijn_kruidenterras.blend` | high (namiddag) |
| 15 | Zonnebloem Zomeravond ⭐ | `pilots\Zonnebloem-300x300-300-zijwand\style-boerderij\zonnebloem_zomeravond.blend` | high (sunset) |
| 16 | Zonnebloem Ochtendhoek | `pilots\Zonnebloem-300x300-300-zijwand\style-scandi\zonnebloem_ochtendhoek.blend` | base (frisse ochtend) |

Achtergrond-docs (lees als je context nodig hebt, niet verplicht):
`docs\INDEX_scenes.md`, `docs\REVIEW_alle_scenes.md`, `docs\PLAN_REALISME_OVERHAUL.md`.

---

## 2. Vaste technische feiten (gevalideerd)

- **Blender:** `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe` (gebruik 5.1, niet 3.6/4.0/4.1).
- **GPU:** RTX 3070 / 8 GB. Render-tijden: 2560×1440 / 240 samples ≈ **75–100 sec** per scene.
- **VRAM-veilig:** `cycles.device='GPU'`, `texture_limit_render='2048'`, `render.use_persistent_data=False`.
- **Camera:** gebruik `scn.camera`; valt die weg, pak `HeroCam`. **Zet altijd `cam.data.clip_start = 0.02`**
  (base-camera's staan op 5.0 → snijdt de voorgrond weg = donkere balk onderaan).
- **Finale recept:** 2560×1440, 240 samples, OIDN-denoise (ACCURATE, RGB_ALBEDO_NORMAL), 16-bit PNG.
  Sjabloon: `render_zonnebloem_final.py`.
- **Shared libs:** `scripts\cabin_lib.py` (build-helpers, `save_and_diag`, `audit`, `fix_broken_image_materials`),
  `scripts\swap_lib.py` (`finalize`, `open_scene`, flagstone/paver helpers), `scripts\_diag_generic.py`
  (read-only inventaris: `blender -b --python scripts\_diag_generic.py -- <scene.blend>`).
- Run alle blender-commando's via de **Bash-tool** met dit pad-patroon:
  ```bash
  "/c/Program Files/Blender Foundation/Blender 5.1/blender.exe" -b \
    --python "C:/Users/beike/Documents/Blender-blokhutten/scripts/render_final.py" \
    -- "<scene.blend>" "<out.png>"
  ```

---

## 3. FASE 1 — Finale 2560×1440 renders van alle 16 (veilige, gegarandeerde winst)

Doel: van elke goedgekeurde scene een finale hero. Niet-destructief: output naast de preview.

**Output-naam:** in dezelfde map als de `.blend`: `<scene-bestandsnaam>_FINAL_2560x1440.png`
(bv. `camelia_buitenbad_FINAL_2560x1440.png`). Zonnebloem Zomeravond heeft al een HERO-final → mag je
overslaan of opnieuw renderen als `_FINAL_2560x1440.png` voor consistente naamgeving (niet de bestaande HERO overschrijven).

**Stap 1 — maak het generieke render-script** `scripts\render_final.py`:

```python
# scripts/render_final.py — generieke finale render.
# Gebruik: blender -b --python scripts/render_final.py -- <scene.blend> <out.png> [samples] [resx] [resy]
import bpy, sys
a = sys.argv[sys.argv.index("--")+1:]
SCENE, PNG = a[0], a[1]
samples = int(a[2]) if len(a) > 2 else 240
rx = int(a[3]) if len(a) > 3 else 2560
ry = int(a[4]) if len(a) > 4 else 1440
bpy.ops.wm.open_mainfile(filepath=SCENE)
scn = bpy.context.scene
cam = scn.camera or bpy.data.objects.get("HeroCam")
if cam:
    scn.camera = cam
    cam.data.clip_start = 0.02
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'CUDA'; prefs.get_devices()
    for dv in prefs.devices: dv.use = True
    scn.cycles.device = 'GPU'
except Exception as e:
    print("dev", e)
scn.cycles.samples = samples
scn.cycles.adaptive_threshold = 0.008
scn.cycles.use_denoising = True
scn.cycles.denoiser = 'OPENIMAGEDENOISE'
scn.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
scn.cycles.denoising_prefilter = 'ACCURATE'
scn.cycles.max_bounces = 6
scn.cycles.transmission_bounces = 12
scn.cycles.texture_limit_render = '2048'
scn.render.use_persistent_data = False
scn.render.resolution_x = rx
scn.render.resolution_y = ry
scn.render.image_settings.file_format = 'PNG'
scn.render.image_settings.color_depth = '16'
scn.render.filepath = PNG
bpy.ops.render.render(write_still=True)
print("[final] " + PNG)
```

**Stap 2 — per scene (sequentieel!):**
1. Render met `render_final.py` → `<scene>_FINAL_2560x1440.png`.
2. **Lees de PNG terug** met de Read-tool. Loop de checklist van §6 af.
3. Klein euvel (te donker/licht, camera-clip, magenta materiaal)? Fix gericht en re-render. Groot
   structureel probleem? Log het in `RENDER_STATUS.md` voor Beike en ga door — niet eindeloos polijsten.
4. Werk de regel in `RENDER_STATUS.md` bij (✅ + tijd + 1 zin oordeel) en **commit** (§5).

Aan het eind van Fase 1: 16 finale hero's. Dit is je gegarandeerde deliverable.

---

## 4. FASE 2 — Kwaliteit-v2 met zelfkritiek (de weekend-vulling)

Doel: de bewust-uitgestelde realisme-upgrade per scene proberen, **niet-destructief**, en met een echte
zelfkritiek-lus. Dit is waar de meeste tijd in gaat.

**Niet-destructief:** sla op als `<scene>_v2.blend` en render naar `<scene>_REALISM_v2_PREVIEW.png`
(1600×900/130) en pas na akkoord-met-jezelf naar `<scene>_FINAL_v2_2560x1440.png`. Originele blend/preview
blijven staan, zodat Beike maandag v1 vs v2 kan vergelijken.

**Stap 1 — generiek polish-script** `scripts\polish_v2.py` (globale, scene-onafhankelijke upgrade):

```python
# scripts/polish_v2.py — AgX + subtiele DoF + lichte exposure-compensatie. Niet-destructief.
# Gebruik: blender -b --python scripts/polish_v2.py -- <scene.blend> <v2.blend> <preview.png> <look> [exp]
#   look = "high"  -> 'AgX - Medium High Contrast' (zonnig/golden/sunset/helder/middag)
#   look = "base"  -> 'AgX - Base Contrast'        (overcast/blue hour/mist/zen/zacht)
import bpy, sys
from mathutils import Vector
a = sys.argv[sys.argv.index("--")+1:]
SCENE, V2, PNG, look = a[0], a[1], a[2], a[3]
exp = float(a[4]) if len(a) > 4 else 0.4   # AgX maakt donkerder; compenseer licht
bpy.ops.wm.open_mainfile(filepath=SCENE)
scn = bpy.context.scene
vs = scn.view_settings
vs.view_transform = 'AgX'
vs.look = 'AgX - Medium High Contrast' if look == 'high' else 'AgX - Base Contrast'
vs.exposure = exp
cam = scn.camera or bpy.data.objects.get("HeroCam")
if cam:
    scn.camera = cam
    cam.data.clip_start = 0.02
    # subtiele DoF: focus op cabin-midden (world origin-omgeving), zachte voorgrond/achterring
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = 6.0
    cam.data.dof.focus_distance = (cam.location - Vector((0, 0, 1.2))).length
# render-veilig + preview
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'CUDA'; prefs.get_devices()
    for dv in prefs.devices: dv.use = True
    scn.cycles.device = 'GPU'
except Exception as e:
    print("dev", e)
scn.cycles.samples = 130
scn.cycles.use_denoising = True
scn.cycles.texture_limit_render = '2048'
scn.render.use_persistent_data = False
scn.render.resolution_x = 1600
scn.render.resolution_y = 900
scn.render.image_settings.file_format = 'PNG'
scn.render.image_settings.color_depth = '8'
scn.render.filepath = PNG
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=V2)
bpy.ops.render.render(write_still=True)
print("[v2] " + PNG)
```

**Stap 2 — zelfkritiek-lus per scene (max 3 iteraties):**
1. Draai `polish_v2.py` met de juiste `look` (zie tabel §1) → v2-preview.
2. **Lees de v2-PNG én de originele `_REALISM_PREVIEW.png`** en vergelijk. Vragen:
   - Is v2 te donker/te flets door AgX? → verhoog `exp` (0.4 → 0.6/0.8) en re-render.
   - Highlights mooier afgerold (lucht/water/metaal) dan v1? Dat is de winst die je zoekt.
   - DoF te sterk (voorgrond matig)? → fstop omhoog (6 → 8) of DoF uit voor die scene.
   - Gras nog oververzadigd of harde snijlijn gras↔hardscape? → noteer voor gerichte fix (stap 3).
3. Scene-specifieke fix alléén als je zelfkritiek het flagt (anders overslaan, niet over-engineeren):
   - **Gras ontzadigen:** zoek het gras-materiaal, zet HueSat-saturation ~0.75 (of voeg een HueSat-node
     toe vóór Base Color). Diag eerst met `_diag_generic.py` voor de exacte materiaalnaam.
   - **Flagstones donkerder:** verlaag de base-color value van het steen/`stone_mat`-materiaal ~15–25%.
   - Gebruik `cabin_lib.fix_broken_image_materials()` als er magenta opduikt.
4. Beste iteratie → render finale `<scene>_FINAL_v2_2560x1440.png` met `render_final.py` op de `_v2.blend`.
5. `RENDER_STATUS.md` bijwerken (v1 vs v2 oordeel in 1 zin) + commit.

> Belangrijk: AgX is een smaak-keuze die Beike bewust had uitgesteld. Jij beslist NIET dat v2 v1 vervangt —
> je levert v2 als **vergelijkbare optie** naast v1. Schrijf in `RENDER_STATUS.md` per scene jouw advies
> (v1 of v2, met 1 reden), maar laat de eindkeuze aan Beike.

---

## 5. FASE 3 — Alternatieve camerahoeken (alleen als er tijd over is)

Per scene 1 extra marketing-compositie naast de bestaande hero, voor variatie in de webshop:
- **3/4 lifestyle:** camera off-center, 50 mm, focus op het zit-/eet-/wellness-deel.
- **Detail/product:** dichterbij, 50–70 mm, op de sterkste prop (bad, eettafel, kruidenbak…).

Maak per scene `<scene>_ANGLE-<naam>_2560x1440.png`. Houd de §6-checklist aan. Dit is een
nice-to-have; sla over als Fase 1+2 het weekend al vullen.

---

## 6. Zelfkritiek-checklist (loop af bij ELKE render die je terugleest)

Realisme-tells (uit `PLAN_REALISME_OVERHAUL.md`):
- [ ] Geen kale `box`/cilinder-props met één vlakke kleur en mes-scherpe randen.
- [ ] Paden sluiten aan op deur/terras, hebben kantopsluiting, zijn verzonken (geen "rondjes naar nergens").
- [ ] Niets zweeft: props staan met contactschaduw op hun draagvlak (bbox min-Z klopt).
- [ ] Gras niet oververzadigd; geen harde snijlijn gras↔hardscape.
- [ ] Highlights niet uitgeblazen (AgX-rolloff bij v2).

Anti-cliché (uit memory):
- [ ] Geen uniforme bomenrij; geen symmetrische prop-plaatsing; geen leeg-grind-cabin-in-midden.
- [ ] 3 dieptevlakken (voorgrond/mid/achtergrond) leesbaar.
- [ ] Geen donkere balk onderaan (= `clip_start` vergeten).
- [ ] Geen magenta/roze materiaal (= broken texture).
- [ ] Camera waterpas (geen kantelende verticalen).

Vind je een fout: fix gericht en re-render. Twijfel je of het "goed genoeg" is: het was al akkoord op
preview-niveau, dus alleen duidelijke fouten fixen — niet eindeloos polijsten.

---

## 7. Logboek, voortgang & commits

**Maak/onderhoud `RENDER_STATUS.md`** in de repo-root als jouw logboek voor Beike. Begin met een tabel:

```
# RENDER_STATUS — weekend 20–23 jun
| # | Scene | Fase 1 final | Fase 2 v2 | Mijn advies | Notitie |
|---|-------|-------------|-----------|-------------|---------|
| 1 | Camelia Buitenbad | ⏳ | ⏳ | - | - |
... (16 rijen)
```

Werk een rij bij zodra een fase klaar is (✅/⏳/⚠️ + render-tijd + 1 zin). Zet bovenaan een korte
"laatst bijgewerkt"-tijd en wat er nog loopt, zodat Beike in 10 sec ziet waar het staat.

**Git (zodat niets verloren gaat):**
- Werk op een aparte branch: `git checkout -b weekend-renders` (eerste keer).
- **Commit na ELKE scene** met een duidelijke message, bv.
  `git add -A && git commit -m "Finale render Camelia Buitenbad (fase 1)"`.
  > PNG's zijn groot; committen is prima voor de veiligheid. Push NIET (Beike beslist dat maandag).
- Eindig commit-messages met:
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

**Resumable:** als de sessie sneuvelt en opnieuw start, lees eerst `RENDER_STATUS.md` + check welke
`_FINAL_*.png` al bestaan, en pak de eerste scene die nog ⏳ is. Niet dubbel renderen.

---

## 8. Werkvolgorde (samengevat)

1. Lees `RENDER_STATUS.md` (bestaat die niet → maak hem, alle 16 op ⏳). Maak branch `weekend-renders`.
2. Schrijf `scripts\render_final.py` en (voor fase 2) `scripts\polish_v2.py`.
3. **Smoke-test:** render scene 15 (Zonnebloem Zomeravond, al goedgekeurd) op lage res
   (`... -- <blend> <test.png> 80 1280 720`) om de hele pijplijn te bevestigen vóór je 16× zwaar rendert.
   Lukt dat → ga door. Verwijder de test-PNG niet automatisch; laat 'm staan of overschrijf later.
4. **Fase 1:** alle 16 → `_FINAL_2560x1440.png`, sequentieel, elk teruglezen + checklist + commit.
5. **Fase 2:** alle 16 → v2-lus (AgX/DoF + zelfkritiek) → `_FINAL_v2_2560x1440.png` + advies in status.
6. **Fase 3:** als er tijd is, 1 alt-hoek per scene.
7. Schrijf onderaan `RENDER_STATUS.md` een **eindsamenvatting voor Beike**: wat klaar is, jouw v1/v2-advies
   per scene, en eventuele scenes die handmatige aandacht nodig hebben.

Begin nu met stap 1. Werk rustig scene voor scene door; één render tegelijk; lees elke render terug.
Succes — Beike checkt het maandag.
