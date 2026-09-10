# Kickoff-prompt nieuwe sessie — Pilots maakdag

> Kopieer alles onder de streep als eerste bericht in de nieuwe sessie.

---

Je bent Claude Code op het Blokhutwinkel-renderproject (map `D:\Blender-blokhutten`).
Spreek me aan met **"Beike"**, in het Nederlands. We gaan vandaag de 13 pilot-
cabin-scènes van "R4-preview" naar marketing-klaar tillen, plus 2 nieuwe scènes
bouwen. Voordat je iets aanraakt: eerst inlezen, dan pas werken.

## 1. LEES DIT EERST (in deze volgorde, hele bestanden)
1. `docs/REVIEW_pilots_R4_voor_9jul.md` — **de hoofdopdracht van vandaag.** Bevat
   het scorebord van alle 13 scènes, 5 systemische fixes (gras-mix, practicals
   aan, paden, zonrichting, horizon) mét bouwrecept, per scène een genummerde
   fixlijst, en de aanbevolen dagvolgorde.
2. `docs/PLAN_pilot_magnolia_VIJVERTUIN.md` — nieuw concept, vervangt
   magnolia_groene_long (natuurvijver + vlonder; het waterelement waar ik om vroeg).
3. `docs/PLAN_pilot_roosmarijn_KAMPVUUR.md` — nieuw concept, vervangt
   roosmarijn_kruidenterras (vuurkuil + boomstambanken, blue hour).
4. `HANDOFF_R4_progress.md` — R4-status, wat R4 fixte, de kritieke lessen
   (img.has_data-val, os.path.abspath, mist-cube-raycast, vuren-rene wandtextuur).
5. `HANDOFF_16_scene_fixes.md` — de originele diepe review + de HARDE REGELS/
   GOTCHAS-sectie (§3) en de systemische diagnose (§4). Lees minimaal §3 en §4.
6. `WERKWIJZE_REVIEWLOOP.md` — het bewezen draaiboek (anker → akkoord →
   dressing → crop-QC → review-loop → finals). Dit is hoe we werken.
7. Skim de gedeelde toolkit: `scripts/cabin_lib.py`, `scripts/grass_lib.py`,
   `scripts/swap_lib.py`, `scripts/validate_scene.py`, en `apply_r4.py` (repo-root).
8. Voor het practicals/gloed-recept: `overkappingen-website/scene_b_spa.py`
   (functies `emissie_mat` + de Fill-LED-aanpak) — kopieer dat patroon.

## 2. WAT ER NET AF IS (context, niet aanraken)
De Outback-overkappingen-webshoprenders zijn KLAAR: 14 finals in
`overkappingen-website/renders/finals/` (A,B,C,D2,E2,F,G,H,I,J2,M2,BO2,P).
Die zijn goedgekeurd en afgerond — laat ze met rust. Vandaag = alleen de
`pilots/`-cabins.

## 3. DE OPDRACHT
Werk de 13 pilot-scènes af volgens de fixlijsten in de review, in de daar
aanbevolen volgorde. Begin met de 5 systemische fixes (die tillen de hele lijn
in één klap), dan de bijna-klare groep (leeshoek, wijnterras, familietuin,
wintertuin, zomeravond, ochtendhoek), dan de rest. Bouw daarna de 2 nieuwe
scènes volgens hun plan (anker eerst, akkoord vragen, dan pas dressing).
**Roosmarijn-zentuin NIET aanraken — die doe ik zelf.**

Nieuwste previews per scène staan in `pilots/<Cabin>/<style>/*_R4_PREVIEW.png`
(R3 waar geen R4 is). Bekijk ALTIJD eerst de bestaande preview vol formaat zodat
je ziet wat de review beschrijft.

## 4. HARDE REGELS (breek deze nooit)
- Elke echte render = **headless CLI, nooit via Blender-MCP.** Blender 5.1 voor
  de pilot-blends. Eerst `.blend` naar schijf, altijd `os.path.abspath` voor het
  output-pad (relatieve paden schrijven soms naar `C:\pilots\...`).
- **AgX** view transform (Medium High Contrast), exposure ~0.3. Nooit Filmic.
- **Geen World Volume Scatter** op exterieur (maakt alles zwart) — altijd een
  BEGRENSDE volume-cube voor mist/rook.
- **Compositor-val:** `scene.use_nodes = False` als je de node-tree niet gebruikt.
- Diag/preview eerst (1080p-achtig, snelle samples) → review → **pas finale
  2560×1440/512 ná mijn expliciete akkoord.**
- **Geen commits** zonder mijn akkoord.
- Valideer via CODE (bbox, view-layer, os.path.exists), niet via gok.
- Mist-cube (`Mist_Rig`) tijdens mask/vloer-raycasts hide_viewport (zit in
  apply_r4.py) — anders verdwijnt het gras.

## 5. WERKWIJZE (de review-loop die goed werkt)
- Fix één scène af → headless diag → op de pilots-review-server (`:8767`,
  start met `python pilots_review_server.py`) → laat mij reviewen via
  `review_keuzes.json` (houden+leeg = akkoord, notitie = fix gevraagd, weg =
  afgekeurd) → verwerk → herhaal. Werk niet aan alles tegelijk; maak er één af
  en meld het.
- Detached renderketens via Start-Process + ps1 + tail-Monitor (geen tool-
  timeout), één zware GPU-render tegelijk (RTX 3070, 8 GB).
- Meld elke afgeronde fix via Telegram met `notify.ps1`
  (`& "D:\Blender-blokhutten\notify.ps1" -Title "..." -Message "..."`).
- Werk `HANDOFF_R4_progress.md` en het register bij terwijl je gaat.

## 6. START
Begin met de 5 systemische fixes uit de review (§DEEL 1), te beginnen met de
gras-mix in `grass_lib.py` + een testrender op dahlia_leeshoek — dat is de
grootste winst van de dag. Meld je zodra de eerste scène klaar is voor review.
