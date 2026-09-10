# Werkwijze: live review-loop (goedgekeurd door Beike, 8 jul 2026)

Dit is het draaiboek zoals de Outback-overkappingen van concept tot final
liepen. Beike: "dit werkte heel fijn" — dit is voortaan de standaard, ook
voor de blokhut-pilots (Camelia enz.).

## Het hele traject in fases

1. **Plan per scène** (bijna-tekening): coördinaten + assets + sfeer,
   volgens PLAN_TEMPLATE.md. Eén scène = één script (`scene_x_*.py`)
   met `stap1` (vloer+anker) en `stap2` (aankleding) gescheiden.
2. **Anker eerst** (stap 1): vloer, hagen, coulissen, pad/borders — renderen,
   Beike keurt het kader vóórdat er props in gaan.
3. **Aankleding** (stap 2): props één zone per keer, elke plaatsing met
   expliciete rot_z (random-rotatie-valkuil!) en bbox-vangnetten (te_groot).
4. **Diag + eigen QC vóór tonen**: 1280×960/64 headless renderen, dan
   PIL-crops op ware grootte van elke nieuwe/gewijzigde zone + zo nodig
   bbox-probes op de saved blend. Pas als de crops schoon zijn → site.
5. **Review-loop met Beike** (de kern, zie hieronder).
6. **Finals pas na expliciet akkoord**, als losse sequentiële keten.

## De review-loop (fase 5) — zo werkte het

- **Review-server** (`review_server.py`, localhost:8766): secties op
  werkfase (① te reviewen / ② ankers / ③ finals / ④ archief), knoppen
  houden/weg + notitieveld per beeld → `review_keuzes.json`.
  **Cache-les**: renders overschrijven dezelfde bestandsnaam — server
  MOET `Cache-Control: no-store` + `?v=mtime` op alle beelden zetten,
  anders reviewt Beike oude thumbnails (dat gebeurde, gaf spookfeedback).
- **Betekenis van de knoppen**: houden + lege notitie = goedgekeurd ·
  houden/None + notitie = fix gevraagd · weg = afgekeurd/vervalt.
- **Live wachtpost**: een Monitor op wijzigingen in `review_keuzes.json`
  (md5-poll, 15 s). Beike klikt → Claude ziet het direct → fix → render →
  vers op de site. Doorlooptijd per fix-rondje: minuten.
- **Eén ding tegelijk afwerken** (Beikes regel): niet parallel aan
  meerdere concepten; begin bij de afgesproken eerste, werk de feedback
  volledig af, meld het af, dan pas de volgende. Volgorde die Beike
  noemt is leidend.
- **Melden per afgeronde fix**: Telegram via `notify.ps1` (`& $notify -Title
  "..." -Message "..."`) met wat er is gedaan in gewone taal + waar het staat.
  Vragen mag ook zo; Beike antwoordt via de notitievelden of chat.
- **Onduidelijke feedback → vraag stellen, niet gokken** (bijv. "weg"
  zonder notitie); maar alles wat wél uitvoerbaar is eerst afmaken.
- **Elke fix meteen registreren**: nieuwe asset-lessen in het register
  (OPUS_WERKWIJZE §8), voortgang in de handoff-tabel per concept
  (ronde-nummer + wat/waarom in één regel).

## Finals-keten (fase 6)

- Alleen na Beikes expliciete akkoord ("mag je een finalrender maken").
- `finals_run.ps1`-patroon: los gestart proces (Start-Process, geen
  tool-timeout), rendert sequentieel (één GPU-job tegelijk, RTX 3070
  8GB), verplaatst elke final naar `renders\finals\`, Telegram per stuk +
  eindmelding, voortgang in `logs\finals_chain.log` met een Monitor
  (tail -f op FINAL/KETEN/MISLUKT-regels).
- Claude QC't elke final zodra hij landt (verkleinde preview + crops).
- Ondertussen mag licht werk (lezen/plannen/edits) gewoon doorgaan —
  géén tweede render starten zolang de keten loopt.

## Harde randvoorwaarden (ongewijzigd)

- Headless CLI renderen, nooit Blender-MCP voor renders.
- AgX Medium High Contrast; diag 1280×960/64; final 2560×1920/512.
- Product nooit aanpassen (tenzij Beike het expliciet vraagt).
- Geen commits zonder Beikes akkoord.
