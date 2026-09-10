# PROMPT nieuwe sessie — finals verrijken met échte Tuindeco-producten (17 jul 2026)

Kopieer dit als startprompt. Lees eerst dit hele document, dan pas werken.

---

Je werkt voor Beike in `D:\Blender-blokhutten`. Missie: loop de bestaande
**goedgekeurde finals** langs en vervang er **zoveel mogelijk props door
échte producten uit het Tuindeco-assortiment** (gegenereerd met de interne
GLB Creator) — maar álles wat je vervangt **moet in de stijl van het thema
van die scène passen**. Renders worden daarmee letterlijk shoppable; elk
gegenereerd model levert als bijvangst een AR-webshop-viewer op.

## Wat je EERST doet (verplicht, vóór enig werk)

1. Lees memory: `glb-creator`, `render-collaboration-rules`,
   `preview-kwaliteit-laag`, `plaatsing-en-paden-discipline`,
   `render-debug-recepten` (bevat de gltf/rotatie/roughness-valkuilen).
2. Lees de werkwijze-notitie in Obsidian:
   `C:\Users\beike\iCloudDrive\Vault\Claude\wiki\projects\GLB Creator
   werkwijze (Tuindeco-producten).md` — dé pijplijn, volg hem exact
   (maat-check! rescale-bug! solo-probe! front-probe bij meubels!).
3. Lees `docs/GLB_CREATOR_verkenning.md` (API-details) en bekijk als
   voorbeeld `pilots/B11-uitslaapochtend-Roosmarijn200x300/
   uitslaapochtend_bouw.py` (Wembley-import-blok).

## Waar de finals staan

- **Kapschuren**: `kapschuren/scenes/kapschuur_[ABC]_*_FINAL.png` + de
  bijbehorende blends/scripts in `kapschuren/`.
- **Overkappingen**: `overkappingen-website/renders/finals/` (9 concepten)
  en `renders/creatieve-tuin-finals/` (zwembad, wellness, buitenkeuken,
  vuurtafel) + `scene_*.py`-scripts en blends in `overkappingen-website/`.
- **Blokhut-stijlreeks (B10–B15)**: nog geen finals — alleen meenemen als
  Beike het zegt; previews staan in `pilots/B1*/`.

## Werkwijze (hard — per scène, één tegelijk)

1. **Inventariseer** de props van de scène (uit het scenescript/blend +
   het final-beeld): wat is generiek/BlenderKit/procedureel en zou een echt
   product kunnen zijn? Benoem per scène ook het THEMA/de stijl.
2. **Match met Tuindeco**: doorzoek het assortiment via de sitemap-methode
   (zoekpagina is JS-only): `tuindeco.com/sitemap.xml` → NL-sub-sitemap
   (gz) → ~8500 detail-URL's → filter op trefwoorden. Alleen kandidaten
   die bij het thema passen (teak-lounge ≠ zen-tuin); twijfelgevallen
   markeren i.p.v. schrappen.
3. **Voorstel-lijst per scène** → aan Beike (notify.ps1 / keuzebord): per
   prop: huidige prop → Tuindeco-product (naam + URL) + stijl-motivatie +
   creditkosten (~30/stuk). **Wacht op zijn akkoord vóór je genereert** —
   credits (±2800 tegoed, "niet dom veel spenderen").
4. **Genereer** de goedgekeurde lijst via de API (jobs draaien in de
   cloud — start ze en werk ondertussen door). Per GLB de vaste QC:
   maten vs catalogus-json → **lokale non-uniforme rescale** (de
   tool-rescale is een no-op-bug) → gratis **simplify keepRatio 0.3** →
   download naar `assets/glbcreator/` → **solo-probe** (naamles!) →
   front-probe bij meubels → roughness-clamp ≥0.55 bij import →
   `rotation_mode='XYZ'` op de wrapper.
5. **Vervang in de scène**: oude prop eruit, product erin op dezelfde
   plek/rol; oriëntatie bewust (front naar waar het hoort), bbox-grounden;
   ALS er gras met raycast-mask ligt: gras her-runnen na de wissel.
   Product zelf (cabin/kap) NOOIT aanpassen.
6. **Preview 960×720/24/tex-'1024'** naar de reviewsite → `notify.ps1`
   → wachten op Beikes oordeel → dán pas de volgende scène.
7. **Finals (2560×1920/512/adaptive 0.008) en git-commits ALLEEN op Beikes
   expliciete akkoord** — de bestaande finals nooit overschrijven: nieuwe
   naast de oude zetten (bv. `_tuindeco`-suffix) zodat vergelijken kan.

## Harde randvoorwaarden

- Headless CLI (`"C:\Program Files\Blender Foundation\Blender 5.1\
  blender.exe" -b <blend> --python <script>`), nooit Blender-MCP; één
  GPU-render tegelijk; `scn.use_nodes = False` vóór elke render; AgX
  Medium High Contrast.
- Niets verwijderen uit de GLB-Creator-bibliotheek zonder Beikes akkoord.
- Herbruikbaar gereedschap: `pilots/_stijlreeks_lib.py`
  (veilige_import_blend, raycast-helpers, licht-momenten). Nieuwe lessen →
  memory én HANDOFF (prepend-updates in `HANDOFF_R4_progress.md` of een
  eigen `HANDOFF_tuindeco_finals.md`).
- Beike bereiken: `notify.ps1 -Title .. -Message .. [-Photo <pad>]`;
  reviewsites: `pilots_review_server.py` :8767 (pilots) en
  `overkappingen-website/review_server.py` :8766 (overkappingen).

## Suggestie voor de eerste scène

Begin met één overkapping-tuin-final met veel generieke props (bv. de
wellness- of buitenkeuken-final) — inventaris + voorstel-lijst is daar het
snelst overtuigend. Liever één scène perfect doorgewisseld en goedgekeurd
dan vijf half.
