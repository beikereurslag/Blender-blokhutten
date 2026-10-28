# PROMPT nieuwe sessie — stijlreeks één-voor-één op kapschuur-niveau (16 jul 2026)

Kopieer dit als startprompt. Lees eerst dit hele document, dan pas bouwen.

---

Je werkt voor Beike aan de blokhut-stijlreeks in `D:\Blender-blokhutten`. De
vorige sessie is geëindigd midden in een scène-voor-scène rework. Beike is
meerdere rondes ontevreden geweest; de kern van zijn feedback (letterlijk):

- "de paden zijn hele tijd soort zelfgemaakte lelijke stenen... dat kan jij
  veel beter en heb je al beter gedaan bij de kapschuren"
- "alle paden sluiten niet aan... NIET ALLES HOEFT DEZELFDE ANGLE... gebruik
  de omgeving, niet alles moet onder de overkapping... als je het in de
  overkapping zet zorg dat het zichtbaar is... een asset moet de goede kant
  op facen... een plantenbak moet planten erin, NIET EEN PLANTENPOT IN EEN
  PLANTENBAK... alles helemaal opnieuw... één voor één, niet alles tegelijk"
- "neem even goed de tijd om het uit te werken en niet maar dom dingen
  neerzetten"

## Wat je EERST doet (verplicht, vóór enige bouw)

1. Lees memory: `feedback-plaatsing-en-paden-discipline`,
   `pilots-overkapping-werkwijze`, `preview-kwaliteit-laag`,
   `blenderkit-headless-fetch`, `render-collaboration-rules`.
2. BEKIJK (Read, visueel) deze referentie-finals en analyseer per beeld
   camera/vloer/voorgrond/vignet-verdeling:
   - `kapschuren/scenes/kapschuur_A_lounge_FINAL.png` (golden hour lounge)
   - `kapschuren/scenes/kapschuur_B_dining_FINAL.png` (bijna-frontale dining)
   - `overkappingen-website/renders/creatieve-tuin-finals/overkapping-wellness-hottub-600x300.png`
   - `overkappingen-website/renders/creatieve-tuin-finals/overkapping-buitenkeuken-1000x400.png`
3. Lees `kapschuren/SCENE_CONCEPTS.md` (het brief-format: verhaal, zones,
   licht-recept, backdrop, camera, props reuse/fetch, onderscheid) en
   `pilots/SCENE_CONCEPTS_stijlreeks.md` + `pilots/BOUWPLANNEN_stijlreeks_v2.md`
   (de goedgekeurde concepten).

## De compositie-wetten (uit de referentie-analyse van 16 jul)

1. **Vloer = één doorlopend PBR-veld** (patio_tiles / paving_stones_64 via
   `cl.pbr_from_folder` + `cl.add_box` + bevel) dat ónder de kap begint en op
   de voorgrond uit beeld loopt; overgangen tussen twee bestratingen sluiten
   strak aan met een opsluitband. NOOIT losse stapsteen-blobs; GEEN
   `cl.klinker_strip` met platen ≥0.3 m (leest als losse vellen) — strip
   alleen voor kleine klinkers, en een ribbon alleen als hij AANSLUIT op de
   terrasrand.
2. **Camera per scène anders** (frontaal-laag / driekwart / zij-doorkijk),
   laag (±1.2 m), product vult 70–90% van het kader; wat onder de kap staat
   moet vanaf de camera zichtbaar zijn (occlusie-wig checken).
3. **Voorgrond-frame**: bakken/borders met buxus + bloemen die er DIRECT in
   groeien (aarde-vlak + plant, geen pot-in-bak), onderin het kader.
4. **Omgeving doet mee**: vignet verdeeld binnen én buiten de kap (ligbedden
   half buiten, boom over het dak, lantaarns bij de palen).
5. **Elke asset bewust gericht** (dining_chair front = −y bij rot 0;
   Sofa/PH-zitmeubels ≈ −y; barkruk-zitting naar de bar). Check in de crop.
6. **Niets zweeft, niets leeg**: bbox-grounden; potten/bakken gevuld.
7. Humus-grondrecept, AgX Medium High Contrast, bewezen schemer-recept
   (sky MULTIPLE_SCATTERING elev −1.5, strength 1.1, zonlamp E 0.8 warm,
   expo 0.95) — zie memory render-debug-recepten.

## Werkwijze (hard)

- **Eén scène tegelijk.** Bouwen → EIGEN QC-render naar `_diag/` → zelf
  beoordelen op de wetten hierboven (crops!) → pas als het klopt de preview
  als `pilots/<map>/<naam>_fase2_PREVIEW.png` op de reviewsite zetten →
  `notify.ps1 -Title .. -Message ..` → wachten op Beikes oordeel
  (`pilots_review_keuzes.json`, monitor of AskUserQuestion) → dán pas de
  volgende scène.
- Previews/QC: **960×720, 24 samples, texture_limit '1024'** (snel). Finals
  (2560×1920/512/adaptive 0.008) en git-commits ALLEEN op Beikes expliciete
  akkoord.
- Headless CLI: `"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
  -b <blend> --python <script>` — nooit Blender-MCP. Eén GPU-render tegelijk.
  `scn.use_nodes = False` vóór elke render.
- Reviewsite: `python pilots_review_server.py` → :8767 (toont
  `pilots/[BD]*/**_PREVIEW.png`); keuzebord op :8768 (python -m http.server).
- BlenderKit zelf fetchen: `pilots/_bk_fetch.py -- "<query>" <map> [test]`
  (OAuth-refresh zit erin). Assets checken vóór gebruik (mapnamen liegen:
  "lavendel" = blauwe boom, "regenton" = alien; blends soms zonder tex → GLB).

## Status per scène (concepten door Beike gekozen; F sauna geparkeerd)

| # | Scène | Blend | Status |
|---|---|---|---|
| 1 | **Gin-tonic-bar** (Roosmarijn) | `pilots/B6-kruidenterras-Roosmarijn200x300/roosmarijn_gintonicbar_B6.blend` | **BEZIG** — v3b: PBR-keramiekvloer + klinker-hoek ✓, bar/krukken/flessenwand ✓, frontale lage camera ✓. Laatste QC: `_diag/scene1_bar_v3b.png`. NOG DOEN: rommel ín de kap opruimen (potgroep die daar belandde), kap-vloer netjes, bakken+buxus zichtbaar in het kader krijgen, terras-gras-rand links (witte rand zweeft), omgeving links vullen, dan preview → Beike |
| 2 | Oogstdiner (Roosmarijn) | `pilots/B7-zentuin-Roosmarijn200x300/roosmarijn_oogstdiner_B.blend` | wacht — na akkoord sc.1 opnieuw volgens de wetten (vloer aansluiten, eigen camera-hoek: zij-doorkijk?) |
| 3 | Rozenkap (Jasmijn) | `pilots/B1-limonademiddag-Jasmijn300x250/jasmijn_rozenkap_H.blend` | wacht — klimroos-drapering was al aardig; vloer/camera opnieuw |
| 4 | Jeu-de-boules (Jasmijn) | `pilots/B2-avondthee-Jasmijn300x250/jasmijn_jeudeboules_K.blend` | wacht — kap voller, eigen hoek |
| 5 | Kamado-chef (Zonnebloem) | `pilots/B8-ontbijthoek-Zonnebloem300x300/zonnebloem_kamadochef_A.blend` | wacht — interieur zichtbaar maken |
| 6 | Designlounge (Lavendel) | `pilots/B3-designlounge-Lavendel400x300/lavendel_designlounge_B3.blend` | wacht |
| — | D2 Regenfris (KDI) | — | **GESTOPT** (weggeklikt) |
| — | F Sauna-avond (Magnolia) | plan in `pilots/SCENE_CONCEPTS_stijlreeks.md` | geparkeerd tot Beike erop terugkomt |

Alle afgekeurde previews staan in `pilots/_afgekeurd_*`; de reviewsite is nu
leeg. Anker-previews per scène in `pilots/B*/_anker/`.

## Opdracht

Maak scène 1 (gin-tonic-bar) volledig af volgens de wetten, toon hem op de
site + notify, en wacht op Beikes oordeel voordat je iets anders bouwt. Neem
de tijd; liever één beeld dat klopt dan zeven die terugkomen. Werk daarna op
zijn tempo de lijst af. HANDOFF bijhouden in `HANDOFF_R4_progress.md`
(prepend-updates), lessen naar memory.
