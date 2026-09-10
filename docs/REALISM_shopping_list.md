# Realism Overhaul — Master Shopping List

Generated 2026-06-16 from a 16-scene procedural-prop audit (17 parallel agents).
Goal: replace hand-built/procedural props with real downloaded assets, OR rebuild as
approved `cabin_lib` hardscape. Source of truth was the per-scene build scripts; verify
against the live `.blend` object names when swapping.

Legend: `[x]` done · `[~]` deferred/skipped · ⭐ high priority · 🔸 medium · ▫ low

> **Session 2026-06-16 status:** Asset-download phase **complete** — 15 real assets pulled
> from Sketchfab (all CC-BY / CC-BY-SA / Free Standard, commercial-safe) into
> `assets/sketchfab/`, textures packed, validated loadable. 4 items intentionally skipped
> (see notes). **Next phase = headless per-scene swaps** (delete procedural props → append
> these assets + rebuild `use_existing` hardscape via `cabin_lib`).

---

## A. DOWNLOADS — DONE (saved to `assets/sketchfab/<cat>/<name>.blend`, textures packed)

| # | Pri | Item | Saved file | target_size | Used in scenes | Status |
|---|-----|------|-----------|-------------|----------------|--------|
| 1 | ⭐ | Scandi hot tub (1-3D light-wood, UID 6d679d3f…) | `spa/hot_tub_scandi.blend` | 2.0 | Camelia Buitenbad | [x] |
| 2 | ⭐ | Folded towel stack | `spa/towel_stack.blend` | 0.6 | Camelia Buitenbad | [x] |
| 2b| ⭐ | Single folded towel (draped) | `spa/towel_folded.blend` | 0.55 | Camelia Buitenbad | [x] |
| 4 | 🔸 | Two-tier wooden step stool | `spa/spa_step.blend` | 0.55 | Camelia Buitenbad | [x] |
| 5 | 🔸 | Firewood pile (4 arrangements in one file) | `decor/firewood_stack.blend` | 1.0 | Camelia, Dahlia Leeshoek, Magnolia Wintertuin, Zonnebloem Ochtendhoek | [x] |
| 6 | 🔸 | Sheepskin/fur throw (419k faces, keep full-res) | `textiles/throw_sheepskin.blend` | 1.0 | Dahlia Leeshoek, Magnolia Wintertuin, Lelie Ochtendnevel | [x] |
| 7 | 🔸 | Ceramic mug (retint glossy red → scandi neutral) | `tableware/mug.blend` | 0.12 | Dahlia Leeshoek, Zonnebloem Ochtendhoek | [x] |
| 8 | 🔸 | Japanese tea set (white pot + stone cups + tray) | `tableware/tea_set.blend` | 0.35 | Jasmijn Theehuis, Roosmarijn Zentuin | [x] |
| 9 | 🔸 | Open hardcover book (red cover) | `decor/book.blend` | 0.3 | Dahlia Leeshoek | [x] |
| 10/11 | 🔸 | Red wine bottle **+ glass** (one set; dup glass ×2) | `tableware/wine_set.blend` | 0.32 | Camelia Wijnterras | [x] |
| 12 | 🔸 | French press (chrome cage + glass) | `tableware/french_press.blend` | 0.22 | Zonnebloem Ochtendhoek | [x] |
| 14 | 🔸 | Rain barrel (blue plastic → retint dark green/anthracite) | `decor/rain_barrel.blend` | 0.9 | Magnolia Groene Long | [x] |
| 15 | 🔸 | Single rooftop solar panel | `energy/solar_panel.blend` | 1.6 | Magnolia Groene Long | [x] |
| 17 | ▫ | Dinner plate 27 cm (STL — assign ceramic mat) | `tableware/plate.blend` | 0.27 | Zonnebloem Zomeravond | [x] |
| 19 | ▫ | Wooden desk (behind door glass) | `furniture/office_desk.blend` | 1.4 | Dahlia Tuinkantoor | [x] |

## A2. SKIPPED / DEFERRED downloads (with reason)

| # | Item | Decision | Reason |
|---|------|----------|--------|
| 3 | Towel rack | `[~]` **dropped** | Only options were a dark modern metal bar + a wire laundry rack — both wrong for a premium scandi spa. Place real folded towels on the step/tub rim instead. |
| 13 | Tsukubai | `[~]` **deferred** | Only Sketchfab match is CC-BY-**NC**-SA (noncommercial) + 680k faces. In swap phase, build from library `boulder_01`/`stone_01` or restyle `decor/birdbaths`. |
| 16 | Festoon string lights | `[~]` **keep procedural** | Only asset was multicolored Christmas capsules — worse than the procedural warm-globe `cabin_lib.festoon`. Keep procedural, retint bulbs to warm Edison emission in swap phase. |
| 18 | Wine carafe/decanter | `[~]` **skip** | Zonnebloem Zomeravond is approved-FINAL/low; the `wine_set` glass + procedural carafe suffice. |
| — | Laptop | `[~]` **drop** | Behind door glass, low prominence (per audit). Keep `L_Werkplek` area light for the lit-window glow. |

## B. USE EXISTING (no download — rebuild with library asset / `cabin_lib` helper)

| Fake | Replace with | Scenes |
|------|--------------|--------|
| Stepping-stone/flagstone **disc** paths (beveled cylinders) | `flagstone_path`/`ribbon_path` helper, or scatter `path_stones/stone-pathway`,`mossy_stones_pack`,`rocky_stone_path_scan` | Camelia Buitenbad, Magnolia Groene Long, Magnolia Wintertuin, Roosmarijn Zentuin |
| Concrete/composiet **slab** paths (extruded cubes) | `flagstone_path`/`klinker_strip`/`ribbon_path`, or `flagstone_floor` pavers | Dahlia Tuinkantoor, Lelie Avondkubus |
| Decks/boardwalks from raw `add_box`/loose cubes | `cabin_lib.plank_deck` | Lelie Ochtendnevel, Lelie Avondkubus, Magnolia Wintertuin |
| Cor-ten / rectangular planters & raised herb beds | `cabin_lib.slat_planter` (keep the real plant clusters inside) | Dahlia Tuinkantoor, Lelie Avondkubus, Roosmarijn Kruidenterras |
| Bollard / edge light **cylinders** | `lighting/low_poly_garden_lamp` or `garden_lamp` (keep the point lights) | Dahlia Tuinkantoor, Lelie Avondkubus |
| Procedural moss patches (flattened spheres + noise) | `polyhaven/moss_01` (already owned) | Jasmijn Theehuis, Lelie Ochtendnevel |
| Niwaki cloud-pruned topiary (donor spheres + GN scatter) | `topiary_hedge/hetz_midget_arborvitae` or `shrub_01..04` | Jasmijn Theehuis, Roosmarijn Zentuin |

## C. DROP (keep as-is / remove — not worth sourcing)

- **FestoenPaal** (Camelia Wijnterras) — plain pole anchoring the festoon.
- **SlingerPaal + crossarm** (Zonnebloem Zomeravond, FINAL) — generic festoon support pole.
- **Regenpijp + knie** (Magnolia Groene Long) — thin downpipe; a cylinder reads fine.

## D. Clean scenes (no fakes found — already realism-compliant)

- **Lavendel — Lavendelveld** ✅
- **Lavendel — Pluktuin** ✅

---

## Per-scene swap notes (for the headless phase)

- **Camelia Buitenbad** — delete `BadDuig*/BadBand*/BadBinnenwand/BadWater/BadRand` → `hot_tub_scandi` (tone down the bright-blue water material); `BadTrede*/BadTredePoot*` → `spa_step`; `Rek_Staander_L/R`+`Rek_Ligger` → **remove** (towel rack dropped); `Handdoek_1/2`+`HanddoekBad_Top/Flap` → `towel_stack`/`towel_folded` on step+rim; firewood cylinders → `firewood_stack`; `Stapsteen_0..4` → flagstone path helper.
- **Camelia Wijnterras** — `Wijnfles` → `wine_set` bottle; `Glas_0/1` → `wine_set` glass ×2; `Slinger_A/B` → keep procedural festoon (warm Edison emission); FestoenPaal keep.
- **Dahlia Tuinkantoor** — `CortenBak_0/1` → `slat_planter`; `Slab_0..7` → path helper; `Bollard_0/1/2` → garden lamp (keep point lights); `Bureau` → `office_desk`; `Laptop` → drop (keep `L_Werkplek` light).
- **Dahlia Leeshoek** — `Vacht` → `throw_sheepskin`; `Boek` → `book`; `Mok` → `mug` (retint); firewood cylinders → `firewood_stack`.
- **Jasmijn Familietuin** — `Zandbak` frame+sand → source `wooden sandbox` (target 1.5) **or** drop (picnic table carries kids theme).
- **Jasmijn Theehuis** — `Theekom_0/1` → `tea_set`; `Mos_0/1` → `moss_01`; `Snoeiwolk_0..2` → topiary/shrubs (or keep, GN scatter is real).
- **Lelie Ochtendnevel** — `Vlonderpad`(~35 cubes)+`Deur_Vlonder` → `plank_deck`; `Plaid` → `throw_sheepskin`; `MosPlek` → `moss_01`.
- **Lelie Avondkubus** — `Deck` → `plank_deck`; `Slab_0..7` → path helper; `CortenBak` → `slat_planter`; `Bollard_0..2` → garden lamp.
- **Magnolia Groene Long** — `Zonnepaneel`+rails → `solar_panel` (lay flat on roof); `Regenton`+`_Deksel` → `rain_barrel` (retint dark green); `Stapstenen` → path helper; downpipe = drop.
- **Magnolia Wintertuin** — `Vacht` → `throw_sheepskin`; firewood cylinders → `firewood_stack`; `Stap_0..4` → path helper; `Terras` → `plank_deck`.
- **Roosmarijn Zentuin** — `Stapsteen_0..7` → path helper; `Tsukubai`+water → build from `boulder_01`/`stone_01` or restyle `birdbaths`; `Theekom_0/1` → `tea_set`; `Snoeiwolk_0..2` → topiary/shrubs.
- **Roosmarijn Kruidenterras** — `Bed0/Bed1` (4 plank walls each) → `slat_planter` (keep herb clusters on top).
- **Zonnebloem Zomeravond** (FINAL — low) — plates×4 → `plate` (dup ×4, assign ceramic mat); carafes×2 → keep procedural; festoon → keep procedural; SlingerPaal = drop.
- **Zonnebloem Ochtendhoek** — `Mok` → `mug` (retint); `Kan` → `french_press`; firewood cylinders → `firewood_stack`.
