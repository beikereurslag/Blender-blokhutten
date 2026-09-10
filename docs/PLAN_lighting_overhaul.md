# PLAN — Licht-overhaul alle renders (start: 25 jun)

> Doel: het licht van **alle scenes** fixen zoals vandaag bij **Lelie Ochtendnevel** (warme dauw + sterke zon + mist) en **Lelie Avondkubus** (dusk-HDRI + koele maan + neutrale mist). Geen platte schaduwen, geen blauwe "horror"-gloed, geen vage waas. Realistisch, sfeervol, scherp genoeg.

Blender 5.1 · headless CLI · niet-destructief (werk op `*_v3.blend`, schrijf terug of `*_v4`).
Render-check verplicht: na elke wijziging preview 1600×900 teruglezen (de "wees de ogen"-regel).

---

## A. Het gevalideerde licht-recept (Lelie-template)

Per scene vier lagen, in deze volgorde:

1. **HDRI-wereld** (i.p.v. vlakke kleur / kale puresky). Node-setup: `TexCoord(Generated) → Mapping(rot_z) → Environment(image) → Background(strength) → World`. Strength **0.6–1.1**. Rotatie zo dat de zon-kant van de HDRI ongeveer met de Sun-lamp meekomt.
2. **Directionele key (Sun-lamp)** — de bron van diepte/schaduw, NIET plat:
   - Dag/ochtend: energy **4–10**, warm (1.0, 0.95, 0.85), elevatie **35–45°** (middag) of **8–15°** (dauw/golden).
   - Avond/blue-hour: energy **2–7**, **zacht koel-wit** (0.85, 0.88, 0.93) — *niet* verzadigd blauw.
   - `sun.angle` **0.6–1.8°** (zachte maar duidelijke schaduwrand).
   - Azimuth vanaf de **camerazijde / zijkant** zodat de gevel wordt aangelicht én schaduw werpt. **Géén pure backlight** (= donkere gevel).
3. **Volumetrische mist** (optioneel; geeft het "licht-komt-erdoorheen"): begrensde box `x[-12,12] y[-2,15] z[0,2.4]`, Principled Volume, **height-falloff** (grond `0.010–0.016` → top `~0.003`), **anisotropy 0.4–0.6** (forward-scatter glow), **kleur NEUTRAAL** (≈0.85,0.85,0.84) of vleugje warm. Houd 't licht (0.010–0.014) → niet vaag.
4. **AgX + warme praktische lampen**: `view_transform='AgX'`; look **'AgX - Base Contrast'** (overcast/mist/zacht) of **'AgX - Medium High Contrast'** (zonnig/golden/punch + om vaagheid te doden); exposure **0.2–0.4**. Interieur/veranda/bollard-lampen behouden = warme gloed tegen de koele/atmosferische buitenkant.

## B. Valkuilen + fixes (vandaag geleerd)

| Symptoom | Oorzaak | Fix |
|---|---|---|
| **Platte schaduwen / dof** | zwakke zon + vlakke/kale puresky | sterke directionele zon (300%) + echte HDRI + beetje mist voor diepte |
| **Blauwe "horror"-gloed** | mist neemt de verzadigd-koele licht/fog-kleur over | **fog-kleur neutraliseren** (≈0.86,0.85,0.83) **én** zon/maan ontzadigen (zacht koel-wit). Avondsfeer via laag lichtniveau + warme lampen, niet via blauw |
| **Vaag / wazig** | mist te dicht + te laag contrast | mist-dichtheid omlaag (→~0.012) + **AgX Medium High Contrast** + key iets sterker. Scherp onderwerp, atmosferische achtergrond |
| Poppenhuis-effect | dat is **camera**, geen licht | aparte ronde (lager standpunt, 3/4, ~50mm) |

## C. Per-scene toewijzing (sfeer → HDRI → key → mist → AgX)

Sfeer-kolom uit `docs/WEEKEND_PROMPT.md` §1.

| # | Scene | Sfeer | HDRI | Zon/maan | Mist | AgX |
|---|---|---|---|---|---|---|
| 1 | Camelia Buitenbad | blue hour | qwantani_dusk_2 (~0.4) | koel zacht, energy ~3, elev ~12° | licht, neutraal | Base→MHC; warme hottub/interieur-gloed |
| 2 | Camelia Wijnterras | namiddag (mediterraan) | syferfontein_18d_clear / spaichingen_hill | warm, energy ~5, elev ~35° | geen/licht | MHC |
| 3 | Dahlia Tuinkantoor | ochtend | kiara_1_dawn | warm laag, energy ~6, elev ~15° | licht | MHC |
| 4 | Dahlia Leeshoek | zacht daglicht | kloofendal_overcast / partly_cloudy | zacht, energy ~3, elev ~40° | geen | Base |
| 5 | Jasmijn Familietuin | middag | syferfontein_18d_clear | helder, energy ~6, elev ~45° | geen | MHC |
| 6 | Jasmijn Theehuis | ochtend/japandi | kiara_1_dawn (zacht) | zacht warm, energy ~4, elev ~18° | licht (kalm) | Base |
| 7 | Lavendel Lavendelveld | golden hour | venice_sunset / the_sky_is_on_fire | warm-goud laag, energy ~6, elev ~10° | lichte haze | MHC |
| 8 | Lavendel Pluktuin | overcast | kloofendal_overcast_puresky | diffuus, energy ~2, hoog | geen | Base |
| 9 | **Lelie Ochtendnevel** | mist/dageraad | kiara_1_dawn (1.05) | warm, **9.6** (300%), elev ~8° | **0.022** neutraal-warm | Base | ✅ KLAAR (template) |
| 10 | **Lelie Avondkubus** | blue hour | qwantani_dusk_2 (~0.35) | koel-wit, ~15, elev ~17°, azim -95 | **0.012** neutraal | MHC | ✅ KLAAR (template) |
| 11 | Magnolia Groene Long | helder | — | — | — | — | ⏸️ overgeslagen (Beike) |
| 12 | Magnolia Wintertuin | zacht daglicht (winter) | partly_cloudy / overcast | zacht koel-wit, energy ~3, elev ~30° | geen/licht | Base |
| 13 | Roosmarijn Zentuin | overcast | kloofendal_overcast_puresky | diffuus zacht, energy ~2 | licht (zen-kalm) | Base |
| 14 | Roosmarijn Kruidenterras | namiddag | syferfontein_18d_clear / spaichingen_hill | warm, energy ~5, elev ~35° | geen/licht | MHC |
| 15 | Zonnebloem Zomeravond | sunset | venice_sunset / the_sky_is_on_fire | warm laag, energy ~5, elev ~8° + string-light gloed | lichte haze | MHC |
| 16 | Zonnebloem Ochtendhoek | frisse ochtend | kiara_1_dawn / clear morning | fris warm laag, energy ~6, elev ~15° | licht | Base→MHC |

HDRI's staan in `assets/polyhaven/hdri/`: kiara_1_dawn, qwantani_dusk_2, kloofendal_48d_partly_cloudy_puresky, kloofendal_overcast_puresky, kloofendal_43d_clear, syferfontein_18d_clear, spaichingen_hill, forest_slope, eilenriede_park, venice_sunset, the_sky_is_on_fire, kloppenheim_06_puresky, moonless_golf.

## D. Werkwijze per scene (max ~2 iteraties)
1. Open `<scene>_v3.blend`. Zet HDRI + Sun + (mist) + AgX volgens de tabel.
2. Render preview 1600×900/130 (`scripts/render_final.py`). **Lees terug.**
3. Toets aan §B: plat? → key/HDRI/mist sterker. Blauw? → fog+zon ontzadigen. Vaag? → mist dunner + MHC.
4. Bij akkoord-met-jezelf: finale 2560×1440/240. Niet-destructief opslaan.
5. Galerij ververst automatisch (`_render_review.html`); Beike reviewt per scene.

## E. Volgorde
1. Groepeer per sfeer voor consistentie: **golden/sunset** (7,15) · **ochtend/dauw** (3,6,16) · **namiddag/middag** (2,5,14) · **overcast/zacht** (4,8,12,13) · **blue hour** (1) (10 is af).
2. Begin met 1 scene per groep → toon Beike → bij akkoord de rest van die groep.
3. Sequentieel renderen (één GPU-render tegelijk; HIP-warning is onschuldig).

## F. Referentie-scripts (van vandaag, als sjabloon)
- `fix_ochtendnevel_light.py` — HDRI + zon 300% (dag/ochtend-key).
- `fix_avondkubus_atmosphere.py` / `_atmosphere2/3/4/5.py` — mist + maan + hoek/hoogte-tuning.
- `fix_avondkubus_deblue.py` — fog+maan-kleur neutraliseren (blauw weg).
- `fix_avondkubus_clarity.py` — mist dunner + MHC + key sterker (vaag weg).
- `cabin_lib.volumetric_fog()`, `setup_hdri()`, `add_sun()`, `set_agx()`.

## G. Let op (context van de andere ronde-2-klussen)
- Paden + blob-eilanden zijn al weg (8 scenes). Bloemen die het pad flankeerden worden hergroepeerd (Zonnebloem als voorbeeld).
- PDF-feedback scenes 12-16 (bank/patio, lege potten, zwevende bloemen, lampen door dak, sfeer) staat los nog open — zie `docs/ROUND2_feedback.md`.
- Licht-overhaul = déze ronde; doe 'm NA of gecombineerd met de per-scene PDF-fixes per scene.
