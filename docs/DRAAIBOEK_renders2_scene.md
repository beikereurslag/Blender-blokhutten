# Draaiboek Renders 2.0 — een scène opnieuw bouwen

Vastgelegd 26-10-2026 na de pilot De Regentuinkamer (`scenes/regentuinkamer_v2/`). Beike: "Ja, deze aanpak
wordt het voorbeeld voor de andere 22 scènes." Gebruik dit voor elke volgende scène; begin pas aan een
scène als de hoofdsessie met Beike heeft besloten welke.

## Uitgangspunten

- De scène wordt **in Blender opnieuw gebouwd**, rondom af, zodat elke camerahoek en een filmpje kloppen.
  Geen AI-overpaint per beeld.
- De hut is **exact het tekentool-product** (`source-glbs-new/<datum>/<naam>.glb`) via
  `scripts/swap_cabin_tekentool.py`. Product nooit aanpassen.
- Assets in deze volgorde: lokaal (`assets/`) → BlenderKit gratis → PolyHaven (CC0) → AI-3D alleen na
  Beikes akkoord op het geld. AI-3D is zwak in bomen en hagen; niet gebruiken voor de omgeving.
- Geen props of hardscape uit code-primitieven. Pad = één doorlopende mesh met echte PBR-textuur.
- Oude blends niet aanraken; nieuwe map `scenes/<scene>_v2/`. Niets committen zonder Beikes akkoord.

## Stappen en wat Beike per fase ziet

| Fase | Wat | Beike ziet |
|---|---|---|
| 0. Stand | inventaris oude scène (probe headless, niet opslaan), juiste tekentool-GLB, ontwerp/concept van de scène | niets |
| 1. Plan | `docs/PLAN_<scene>_v2.md` via de architect: assets per onderdeel met bron en licentie, licht, camera's, controles | alleen als er geld of een keuze van hem in zit (HQ-vraag) |
| 2. Anker | hut, grond met eventuele kuilen, gazon, pad, hagen, boomringen, statement-boom, zon/HDRI, 3 camera's | bundel: 3 standpunten + haagproef naast referentie + 12 hoeken rondom |
| 3. Aankleding | per laag een script: water/bekken, borders, terras/meubels, details | één bundel na alle lagen: 3 standpunten + close-ups per zone + 12 hoeken |
| 4. Finals | na zijn akkoord: 2560×1440 per camera | de finals als bundel |

Bouw na zijn akkoord op het anker pas verder; leg tussendoor niets voor dat je zelf al fout ziet.

## Bestanden (kopieer de pilot als sjabloon)

Uit `scenes/regentuinkamer_v2/`:

- `stap0_assets.ps1` + `stap0b_polyhaven.py` — downloads (BlenderKit per asset-ID via
  `pilots/_bk_fetch.py -- "asset_base_id:<id>" renders2`; marker per ID in `assets/blenderkit/renders2/.ids/`).
- `rtk_lib.py` — helpers: grond, bomen plaatsen (weigert kale bomen < 50k vertices en schaal buiten 0,8–1,1),
  haagmodules, gazon-zoden, schaduwtoets, luchttoets, audits, zon/HDRI-verhouding.
- `rtk_dressing.py` — helpers voor de aankleding (donorcollecties, plaatsen, kloon- en zichtlijntoets, renders).
- `stap1_anker.py`, `stap2_bekken.py`, `stap3_borders.py`, `stap4_terras.py` — elk opent de vorige blend en
  schrijft een eigen blend; herhaalbaar (vaste seeds), crash-veilig (pas aan het eind opslaan), versie via
  `RTK_VERSIE`. Opties: `--geen-render`, `--alleen-render`, `--negatief <test>`.
- `finals_run.ps1` + `finals_render.py` — finals-keten, één GPU-job tegelijk, log in `logs/finals_chain.log`.
- `review/review_server.py` — review-site (poort 8767; per scène een eigen poort), leest
  `previews/anker/` en `previews/dressing/`; keuzes in `review/review_keuzes.json`.
- `LICENTIES.md` — per gebruikt asset de licentie; bijwerken bij elk nieuw asset.

Scène-specifiek aanpassen: hutpositie en deur-toleranties, tuinmaten, zones, camera's, zonrichting, de
assetlijst. Schrijf scripts met de Write-tool (bash mangelt Windows-backslashes).

## Recepten die werkten

- **Bomen:** BlenderKit Fagus Sylvatica 05/09, Fagus Grandifolia05, Acer Campreste in drie ringen
  (2–13 m, 15–30 m, 35–70 m), groepjes van 2–3, nooit een rij; ring 4 met Treeline-kaarten op ~90 m als de
  luchttoets onder 95% blijft. Niet gebruiken: Acer Platanoide (herfstoranje), Silver_Birch (kale takken),
  2–3× opgeschaalde PolyHaven-bomen.
- **Haag:** BlenderKit Cotoneáster-module, om en om gedraaid en in elkaar geschoven; bessen naar
  bladmateriaal.
- **Gazon:** BlenderKit "Garden Grass Free" samengevoegd tot zoden (`bouw_zoden`), ~9.000 pollen/m² met weinig
  instances, frisgroen met maaibanen (1,6 m, ±7%) en kleurvlekken; groen getinte `leafy_grass`-bodem eronder.
  BK "Mown Grass" en PH `grass_medium_02` lazen als klaver of stro.
- **Licht:** zon 60–90° naast de camera-as, 26–35° hoog, 4500 K, sterkte 9; HDRI pure/daglucht op 0,35
  (zon moet ≥ 2× het luchtlicht geven; bij 1,2× oogt het bewolkt). AgX Medium High Contrast, exposure 0.
  Interieurlicht in de hut, anders zijn de ramen zwart.
- **Buiten de hagen:** struiklaag (PH shrub_02), ruig gras en varens tot ~40 m; nooit kale bosgrond.
- **Water:** plassen ≥ 1,5 m², donkere natte bodem, smalle natte rand (~12 cm), fijne rimpeling; geen
  beplanting in de zichtlijn naar de camera; geen steen in het water.
- **Borders:** losse struiken, hooguit één of twee bollen als accent (Beike, 26-10); drifts met wisselende
  soort en hoogte.

## Controles (verplicht, vóór iets naar Beike gaat)

1. `validate_scene`, `cl.audit`, eigen audit (niets in de hut, niets zwevend > 5 cm, geen gras op het pad,
   geen magenta).
2. Hut-tolerantie (deurmidden ± 5 cm), schaduwtoets (boomschaduw ≤ 20% van de tuin), luchttoets (≥ 95% op
   0–6°, plus de ring 1-eis op 10–15°). Elke toets één keer bewust laten falen (negatieve test).
3. Kloon- en zichtlijntoets bij de aankleding.
4. Videogeheugen: Cycles-piek < 6,5 GB (pilot: 6,2 GB op 960×540, 6,56 GB op 2560×1440 met texture_limit
   2048). Zware assets (hortensia 2,2 M vlakken, lavendel Moonlight) eruit laten.
5. Zelf de beelden op volle grootte nakijken (crops), plus de 12-hoeken-hoektest.

## Videokaart en renderen

- Altijd headless (`blender.exe -b <blend> --python <script>`), nooit via de Blender-MCP; OPTIX expliciet
  zetten (een losse `blender -b` rendert anders stil op de CPU).
- Vóór elke render `nvidia-smi` en `D:\Beeldherkenning\GPU_BEZET.txt`; van een ander → wachten. Tijdens eigen
  renders het bestand zelf zetten en daarna weghalen.
- Previews 960×540, 24 samples, denoise. Finals 2560×1440, 512 samples adaptive 0,008, OIDN, 16-bit PNG
  (~7 min per beeld op de RTX 3070).

## Tijd en kosten (pilot)

Van stand tot finals ongeveer één werkdag sessietijd; videokaart ~3 uur. Geld: €0 (BlenderKit gratis,
PolyHaven CC0).

**Geen betaalde AI-modellen** (Beike, 28-10: "doe het liever zonder dat want het is betaald"): meubels uit
GLB Creator/Meshy niet gebruiken. Een meubel dat niet gratis te vinden is, bouw je zelf in Blender met echte
details, zoals `scenes/regentuinkamer_v2/stoel_teak.py` (teak-loungefauteuil: afgeronde latten met nerf in de
lengte, ingezakte kussens met naad, PH `teak_veneer`; ~21.000 driehoeken, lichter dan het Meshy-model).
Controleer met een vergelijkingsbeeld naast het alternatief en met een close-up op finalformaat.
`finals_run.ps1` kan geblokkeerd worden door de PowerShell execution policy: draai hem dan als
achtergrond-PowerShell (`& finals_run.ps1 -Cams ...`) of via bash met dezelfde stappen.
