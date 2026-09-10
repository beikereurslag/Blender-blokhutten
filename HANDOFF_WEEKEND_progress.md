# HANDOFF — Weekend-run (autonoom, 10–13 jul 2026)

> Beike gaat het weekend weg en laat Opus autonoom draaien op **werk dat GEEN
> creatief oordeel / geen live-review nodig heeft** (de R4-review + sign-off gaan
> vanaf **Fable 5**, niet op Opus). Dit bestand is de durende bron van waarheid;
> ik update het per mijlpaal. Vragen/keuzes voor Beike gaan via Telegram
> (`notify.ps1`) en worden hier onder "GEPARKEERD VOOR BEIKE" gezet.

## Harde kaders (blijven gelden)
- **Geen git commits.** Geen finale 2560×1440-renders. Previews (≤1920×1080) mogen.
- **Headless CLI Blender** (`blender.exe -b --python …`), nooit via MCP.
- **Opschoning = voorbereiden/verplaatsen, NIETS definitief wissen.** Alles reversibel.
- AgX Medium High Contrast. Beike aanspreken met "Beike". Nederlands.
- Eén GPU-renderjob tegelijk (RTX 3070, 8 GB VRAM). Analyse-werk mag ernaast.

## De 4 weekend-werkstromen (Beike koos alle vier)
1. **R4-set review-klaar** — 3 ontbrekende R4-blends getrouw herbouwen + alle 13
   blends verifiëren + verse complete preview-galerij.
2. **Diepe QC + fixlijst per scène** — exhaustieve technische diagnose, GEEN fixes.
3. **Repo-opschoning prep** — 991 untracked bestanden inventariseren, .gitignore,
   quarantaine-script (verplaatsen, niet wissen) + rapport. Niets uitgevoerd.
4. **Asset-audit** — inventaris assets/, gebruik per scène, missend/dubbel,
   t.o.v. BlenderKit-first-beleid.

## KRITIEKE BEVINDING (bepaalt werkstroom 1)
- De originele `_RIG.blend`-basissen staan NIET meer op D:. Alleen 3 `_R3.blend`
  (2 jul, ~1,2 GB) voor de scènes zonder R4-blend: **magnolia_wintertuin,
  zonnebloem_zomeravond, zonnebloem_ochtendhoek**.
- `grass_lib.py` is op 9 jul aangepast voor de **afgekeurde R5-grasmix** (257 rgls
  nu vs 132 in `_OLD`, 27 jun). Rebuild met huidige libs = R5-gras = afgekeurde look.
- **Oplossing:** rebuild draait tegen `_OLD/scripts` (2-jul libs) via een kopie van
  `apply_r4.py` met aangepast sys.path → `scratchpad/apply_r4_faithful.py`.
  Output: `<key>_R4.blend` (bestond nog niet, veilig) + `<key>_R4_PREVIEW_rebuilt.png`
  (aparte naam; 8-jul `_R4_PREVIEW.png` blijft als referentie staan).
- **GEPARKEERD:** eindoordeel of de rebuild goed genoeg is als R4 = Beike op Fable 5
  (side-by-side vergelijking wordt klaargezet).

## KRITIEKE LES (weekend — bijna R5-gras in R4 gebakken)
- Eerste rebuild-poging (`apply_r4_faithful.py`) FAALDE stil: de log toonde
  `grass_lib.__file__ = ...\Blender-blokhutten\scripts\grass_lib.py` (huidige R5!)
  en "gras-mix (3 varianten…)" = de AFGEKEURDE R5-look. Oorzaak: `cabin_lib.py`
  regel 20 doet zélf `sys.path.insert(0, ROOT+"\scripts")` → dat duwt de huidige
  scripts vóór mijn `_OLD`-pad zodra cabin_lib geïmporteerd wordt.
- **FIX (`apply_r4_faithful2.py`):** modules met `importlib` DIRECT uit de
  `_OLD`-bestanden laden en in `sys.modules` registreren vóór exec. Gevalideerd:
  log toont nu `grass_lib <- ..._OLD\...` + "gemaskeerd gras (alleen op echte grond)"
  = de 2-jul R4-look. ✓
- **2e fix:** apply_r4's interne render (200spp/1920 + volume-mist) liep vast op
  8 GB VRAM (CPU-fallback, 18 min geen progress). Daarom nu SAVE-ONLY in de rebuild
  (monkeypatch `cl.save_and_diag`) + previews los & licht (1280×720, 110spp, GPU).

## STATUS (live — laatst bijgewerkt: 15:31, keten + cleanup gestart)
| # | Werkstroom | Status |
|---|-----------|--------|
| 1a | Probe/verify 10 bestaande R4-blends | ✅ KLAAR (10× exit 0, AgX+Cycles) |
| 1b | 3 R4-blends getrouw herbouwen (_OLD-libs) | ✅ KLAAR (3× getrouw, previews technisch gaaf) |
| 1c | Verse preview-galerij compleet | ✅ KLAAR (:8767, 34 beelden, 3 rebuilds bovenaan) |
| 2 | Diepe QC + fixlijst (13 scènes) | ✅ KLAAR (3 blockers · 26 high · 10 systemisch) |

> **✅ ALLE 4 KERN-WERKSTROMEN AF.** Landingspagina voor maandag: `WEEKEND_START_HERE.md`.
> Niets gecommit/gewist/gefinaliseerd. Geparkeerde beslissingen staan in START_HERE.
| 3 | Opschoning-prep (.gitignore + quarantaine-script + rapport) | ✅ KLAAR |
| 4 | Asset-audit (catalogus-doc) | 🟢 draait (workflow wo94ta4b7) |

**Rooktest OK (15:30):** probe op dahlia_leeshoek → AgX+Cycles bevestigd, en meteen
een echte vondst: 4 ontbrekende texturen `wild_rooibos_bush_*` (polyhaven, relatief
pad `//..\..\..\assets\polyhaven\models\textures\` niet gevonden, niet gepackt).
Zulke C:→D:-restanten vangt de QC dus automatisch.

## Deliverables die maandag klaarstaan (verwacht)
- `_diag/weekend/probe_<key>.json` — technische health-dump per blend.
- `docs/REVIEW_pilots_R4_WEEKEND.md` — diepe QC + fixlijst per scène (geen fixes).
- `docs/ASSET_AUDIT_WEEKEND.md` — asset-catalogus + missend/dubbel + BlenderKit-toets.
- `CLEANUP_WEEKEND.md` + `_cleanup_weekend.ps1` (niet uitgevoerd) + nieuwe `.gitignore`.
- 3× `<key>_R4.blend` + `_R4_PREVIEW_rebuilt.png` (rebuild, geparkeerd voor oordeel).
- Review-galerij op :8767 met alle 13 R4-previews (bestaand + 3 rebuild ernaast).

## Logboek
- 15:20 infrastructuur + scripts aangemaakt (`scratchpad/_weekend_probe.py`,
  `apply_r4_faithful.py`, `chain_weekend.ps1`).
- 15:30 rooktest probe geslaagd (leeshoek).
- 15:31 keten gestart (background bepb8b1kc): probe 10 → rebuild 3 → probe 3.
  Statuslog: `_diag/weekend/chain_status.txt` (ASCII, veilig te tailen).
- 15:31 opschoning-prep-agent gestart (levert CLEANUP_WEEKEND.md +
  _cleanup_weekend.ps1 + .gitignore.proposed; voert niets uit).
- 15:33 opschoning-prep KLAAR: `CLEANUP_WEEKEND.md` + `_cleanup_weekend.ps1`
  (DryRun default aan, verifieerd: verplaatst niets) + `.gitignore.proposed`.
  Quarantaine-lijst = 89 `_diag`-bestanden (17,3 MB); groot spul via gitignore.
  Vondst: de 74 "losse root-scripts" zijn al getrackt (73/74) — geen rommel.
- 15:34 alle 10 probes exit=0; keten rendert nu de 3 rebuilds.
- 15:34 asset-audit-workflow gestart (wo94ta4b7): 8 familie-agents + gebruik +
  synthese → `docs/ASSET_AUDIT_WEEKEND.md`.
- 16:02 lib-fix gevalideerd op magnolia (getrouwe 2-jul-gras). Zie KRITIEKE LES.
- 16:05 keten v2 gestart (background btzd7ul12): bouw zonnebloem×2 getrouw →
  render 3 previews licht (1280×720/110spp GPU) → probe 3. Log: `chain2_status.txt`.
- 16:06 `pilots_review_server.py` aangepast: herkent nu `_R4_PREVIEW_rebuilt.png`
  → sectie ① (3 rebuilds bovenaan) + sectie ② (8-jul R4 ter vergelijking).
  Server moet HERSTART na de rebuilds (oude instance draait nog op :8767).
- 16:40 keten v2 KLAAR (exit 0): 3 getrouwe R4-blends + 3 previews (OPTIX,
  1280×720/110spp) + 13/13 probe-dumps. Zelf bekeken: alle 3 rebuilds technisch
  gaaf (geen zwart/magenta/zwever, gemaskeerd R4-gras).
- 16:41 server herstart op :8767 (PID 30588, nieuwe code). Galerij geverifieerd:
  34 beelden — ① 3 rebuilds, ② 13 R4-ref, ③ 2 ankers, ④ 16 AGXv2.
- 16:42 QC-workflow gestart (w1zir7pj0): 13 scene-agents + synthese →
  `docs/REVIEW_pilots_R4_WEEKEND.md`.
- 16:55 QC-workflow KLAAR (14 agents, 0 fouten): `docs/REVIEW_pilots_R4_WEEKEND.md`
  (36 KB). 3 blockers (missende texturen), 26 high, 10 systemische bevindingen.
  QC ving zelf de vals-positieve probe-floaters af (S-J) — niet blind gevolgd.
- 16:56 NUANCE bevestigd: `zonnebloem_ochtendhoek`-rebuild mist `T_vl0mfbllw_8K`
  (Deur_Stoep-grind) — dat is de post-R4-handfix van 8 jul die niet in R3 zat.
  De rebuild is dus getrouw aan R3+apply_r4, niet aan de verdwenen 8-jul-R4-blend.
  magnolia/zomeravond-rebuilds: geen missende texturen.
- 16:57 `WEEKEND_START_HERE.md` geschreven (landingspagina). Telegram naar Beike verstuurd.
- **KERN-4 KLAAR.**
- 17:00 blocker-texturen op schijf gelokaliseerd (zie WEEKEND_START_HERE.md):
  gravel → PavingStones125A-swap aanbevolen; rooibos → textures in model-.blend.
  GEEN relink-script geschreven (materiaalkeuze = Beikes stap).
- 17:02 OPTIONEEL dieptewerk: 4 overkappingen tuin-finals geprobed (read-only).
  UITKOMST: Keuken/Vuurtafel/Wellness texture-schoon (0 missend/magenta, AgX+Cycles).
  Zwembad meldt 7 "missing" maar dat zijn interne/gegenereerde datablocks
  (`Map #N`, `uv colorgrid`) — vals-positief, geen echte textuur. **Finals zijn qua
  texturen veilig te committen** (commit-beslissing zelf = Beike). Dumps: `probe_tuin*.json`.
- **WEEKEND-RUN COMPLEET.** Alles staat klaar voor Beikes review op Fable 5. Geen
  verder werk gestart — opdracht is af, ik verzin geen busywork.
