# PLAN — Rigs A–E uitrol + verificatie (n.a.v. HANDOFF_16_scene_fixes.md)

Doel: alle 16 scenes van "R2-preview" (3–5,5/10) naar marketing-klaar (≥8/10) via 5 gedeelde,
herbruikbare rigs, daarna per-scene fine-tuning. **Roosmarijn Zentuin blijft buiten scope** (Beike doet die zelf, v8).

---

## STAP 0 — Reconciliatie vóór ik iets bouw (moet eerst rond zijn)

**0a. Versie-conflict (3 scenes).** Mijn gras/grond-uitrol schreef naar `_v4.blend`, maar er bestaat een hoger versienummer dat ik niet als basis nam:
- Magnolia Wintertuin → v5 bestaat (mijn gras zit in v4)
- Zonnebloem Zomeravond → v6 bestaat (mijn gras zit in v4)
- Roosmarijn Kruidenterras → v5 bestaat (mijn gras zit in v4)

Aanpak: ik **diff** v4↔v5/v6 (object-count, collections, camera, materialen) en rapporteer wat er in de hogere versie zit dat v4 mist. Dan kies jij (of ik adviseer) de basis. Default zonder jouw input: ik neem de versie met de meeste/juiste content als basis en her-applyeer daar het gras op. **Ik bouw geen rigs tot dit per scene beslist is.**

**0b. Zentuin.** Ik raak `roosmarijn_zentuin` niet meer aan. Mijn eerdere gras/grond ging op een throwaway-`v4`; jouw `v8` is ongemoeid. Ik sluit hem uit alle batches uit.

**0c. Mijn eerdere gras/grond-werk.** Dat was ad-hoc en wordt **opgenomen in de rigs**: `grass_lib.py` (huidig: 1 gekruiste sprietjes-tuft + grond-only masker) is de basis voor RIG B, maar wordt opgewaardeerd naar de handoff-spec (2–3 gemengde clumps, density-noise, kale/platgelopen plekken, klaver/onkruid, uitfadende randen). De grond-materiaal-tweak (groener+donkerder) blijft als onderlaag onder het gras.

---

## STAP 1 — Rigs bouwen in `cabin_lib.py` / `grass_lib.py`

Elke rig = één functie, per scene één call. Bouwen + los testen op 1 scene vóór uitrol.

### RIG A — `cl.setup_light(moment, azimuth_deg)`  [licht]
- Sun-object: elevatie 5–15° (laag), azimut per scene (zon 3/4 van voren-opzij), energy ~3–5, **blackbody** kleur per moment (golden hour 3000–3500K · namiddag 4000K · ochtend 4500K · blue hour 6500K+koele world+lage energy · overcast = grote zachte area/dome i.p.v. harde zon).
- **Volumetrische haze = BEGRENSDE cube** rond de scene met Principled Volume, density 0.002–0.005. **NOOIT World Volume Scatter** (maakt Cycles-exterieur pikzwart).
- AgX gegarandeerd aan + exposure ~0.3; `scene.use_nodes=False` als er geen compositor-tree nodig is (anti-zwart).
- HDRI matchen aan het moment (`hdri_swap.py`).
- Presets per moment als dict; referentie-look = Lelie Ochtendnevel.

### RIG B — `gl.lawn(area, moment)`  [gazon]  — upgrade van huidige grass_lib
- 2–3 échte Polyhaven-grasclumps gemengd (append per object, geen `libraries.load` van hele LOD-set), Poisson-distributie, alles **INSTANCED** (nooit Realize → VRAM-crash).
- density-noise → kale plekken + platgelopen looppaden; density **uitfaden naar de randen** (geen naad/"zwevend tapijt").
- random scale 0.6–1.4 + random tilt tot ~35° + random Z-rotatie; 5–10% klaver/onkruid/gele sprieten; kleurvariatie via ColorRamp op instance-index/noise.
- **grond-only masker behouden** (raycast omlaag: nooit op deck/pad/terras/water/grind/hut) + roughness hoog (geen "natte plas").
- per moment de kleur dempen (mist/ochtend = grijzig-groen, niet neon).

### RIG C — `cl.uv_board_textures()` + warm-hout PBR-preset  [hout]
- Hermap elke wand naar mesh-UV + FLAT (nerf mét de plank; fixt 90°-box-projectie).
- Gedeeld warm-hout materiaal: per-plank kleur/tint-variatie, roughness-breakup, dirt/AO in de naden, subtiele verwering onderrand. Voor "blank/wit"-scenes: warmere honing/amber basis + lagere value (geen uitblaas).

### RIG D — `cl.hero_camera()` + verplicht entry-pad
- 35 mm, ooghoogte 1.5–1.65 m, 3/4-hoek 20–35°, cabin op verticale derde-lijn, 50–65% breedte, verticalen recht via `shift_y` (nooit tilten).
- `cl.klinker_strip`/pad van voorgrond-onderhoek → DEUR als leading line (bestaande paden die wéglopen vervangen).

### RIG E — `cl.drop_to_ground(objs)` + overkapping-dressing
- Alle props bbox-Z-min op terreinhoogte, contact-AO forceren, scatter tot tegen de basis. Terrasdekken/tegels: randinzinking 1–2 cm + grind/aarde-overgang.
- Regel: **overkapping nooit leeg/zwart** → altijd zithoek/plant/lantaarn + zwakke WARME fill-area-light onder elk afdak (avond/schemer: warme binnengloed door het glas).

---

## STAP 2 — Uitrol-volgorde
Per handoff-prioriteit: **A (licht) → B (gazon) → C (hout) → D (camera+pad) → E (grounding+overkapping)**, dan per-scene de scene-specifieke bullets (concept-dressing, backdrop-ringen, scene-eigen problemen).

Per rig: eerst bouwen → **op 1 representatieve scene testen + verifiëren** → dan pas over de 15 scenes (excl. zentuin) uitrollen (headless, sequentieel op de GPU). Zo vang ik een fout op 1 scene i.p.v. 15.

---

## STAP 3 — Verificatie (hoe ik bewijs dat het werkt)
Voor ELKE scene, in deze volgorde, vóór ik "klaar" zeg:
1. **Code-audit:** `scripts/validate_scene.py` + `_probe_junk.py` (in-frame zwevers/low-poly/transparantie) + bbox-in-cabin/zombie-dim check → moet PASS. Numeriek, niet op thumbnail.
2. **Headless 1080p preview** (256 samples, OIDN, AgX) — nooit via MCP.
3. **Eigen full-res inspectie**: ik bekijk de render + gerichte crops (grond-hoeken, overkapping, backdrop) en loop de 7 systemische punten + de scene-specifieke bullets na. Pas na deze zelf-kritiek toon ik het.
4. **Beike-akkoord-gate**: op de viewer (`localhost:8765`) tonen; ik render de finale (2560×1440 / 512 / 16-bit) **pas na jouw akkoord**.
5. Nieuwe lessen documenteren.

Per rig-test extra: side-perspective + top-down crop om te bevestigen dat het effect klopt (bijv. camera-oriëntatie, gras-masker op hardscape, slagschaduw-richting).

---

## STAP 4 — Definition of done (per scene, uit handoff)
Rigs A–E toegepast + scene-bullets af → validate+audit PASS (geen in-cabin/zombie/broken-tex/zwevers) → 1080p preview → Beike-akkoord → finale 2560×1440/512/OIDN/16-bit → lessen documenteren.

## STAP 5 — Harde regels die ik strikt volg
Headless render only · compositor `use_nodes=False` tenzij nodig (anti-zwart) · GEEN World Volume Scatter (begrensde cube) · AgX + exposure ~0.3 · render-recept RTX 3070 (256/512, OIDN RGB_ALBEDO_NORMAL, texture_limit 2048, persistent_data False) · GLB in cm → 0.01× · UV-board FLAT · shared-data transform-val (data.copy vóór transform_apply) · planten via `wm.append` (niet libraries.load) · nooit deleten op "Object_X" · geen USD-bomen · `hide_bare_trees.py` · validate via code · pure Cycles (geen AI-upscale) · **nooit auto-"klaar" zonder Beike-akkoord** · **Zentuin niet aanraken**.

---

## Open vragen aan Beike (blokkeren de start van RIG-bouw)
1. **Versie-basis** voor Magnolia Wintertuin / Zonnebloem Zomeravond / Roosmarijn Kruidenterras: bouw ik op jouw v5/v6 (en her-apply ik gras daar), of op mijn v4-met-gras? (Ik kan eerst diffen en adviseren.)
2. Akkoord op deze rig-aanpak + volgorde, of eerst één rig als proof-of-concept op één scene laten zien?
