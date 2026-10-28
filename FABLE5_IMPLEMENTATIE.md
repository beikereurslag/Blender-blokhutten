# FABLE 5 — runbook: de R4-ronde afmaken

> Jij (Fable 5) doet vanaf nu de **creatieve R4-review + sign-off + implementatie**,
> in de **live review-loop mét Beike**. Opus heeft in het weekend alleen de
> *technische* voorbereiding gedaan (verifiëren, getrouwe rebuilds, QC-diagnose,
> asset-audit, opschoonplan) — **geen fixes, geen commits, geen finals, geen
> creatieve keuzes**. Dit document zet om wat je concreet moet doen.

---

## 0. Lees dit eerst (± 5 min)
Volgorde:
1. `WEEKEND_START_HERE.md` — landingspagina + geparkeerde beslissingen.
2. `docs/REVIEW_pilots_R4_WEEKEND.md` — **de QC**: overzichtstabel, 3 blockers,
   26 high-punten, 10 systemische bevindingen (S-A…S-J), per-scène fixlijst.
3. `docs/ASSET_AUDIT_WEEKEND.md` — assets + missende texturen + BlenderKit-toets.
4. `HANDOFF_WEEKEND_progress.md` — werklog + de valkuilen die Opus tegenkwam.
5. Diepe regels: `docs/VAULT_blender_blokhutten_compendium.md` (grep hierin) +
   `WERKWIJZE_REVIEWLOOP.md` (het draaiboek van de loop).

**Harde regels (overrulen alles):** geen `git commit` en geen finale 2560×1440-render
zonder Beikes expliciete akkoord · elke render is **headless CLI** (`blender.exe -b
--python …`), **nooit via de Blender-MCP** (zware scènes crashen) · **AgX + Medium
High Contrast** · Nederlands · spreek hem aan met **"Beike"**.

---

## 1. Werkwijze — zo wil Beike werken (niet onderhandelbaar)
- **ÉÉN scène tegelijk**, in Beikes volgorde. **Geen batch** — dat is eerder afgekeurd.
- Loop per scène: **anker/kader → akkoord → aankleding → crop-QC vóór tonen →
  review op :8767 → volgende**. Harde regel: anker → akkoord → dán pas dressing.
- **Check-renders** (laag, snel) tijdens iteratie; **finale hoge-res alleen in de
  laatste pass, met akkoord**.
- Beike klikt op de review-site *houden / weg / notitie* → dat landt in
  `pilots_review_keuzes.json`. Zet een **Monitor** op dat bestand: houden+leeg =
  akkoord, notitie = fix, weg = afgekeurd/nieuw plan.
- **Telegram-melding per afgeronde fix:** `& "D:\Blender-blokhutten\notify.ps1"
  -Title "..." -Message "korte status"` (roept de bestaande tg.py aan; niets in te vullen).

---

## 2. Opstarten
- Review-server: `python pilots_review_server.py` → http://localhost:8767
  (draaide in het weekend al; herstart als je hem hebt aangepast). De galerij toont
  **sectie ① de 3 getrouwe R4-rebuilds** bovenaan en **② de 8-jul-R4-previews**
  eronder, zodat Beike direct kan vergelijken.
- Overkappingen-track (apart project) heeft z'n eigen server op :8766.

---

## 3. Beslissingen die je EERST bij Beike ophaalt (ze sturen al het werk)
Vraag deze via de review-loop / Telegram vóór je begint te bouwen:

1. **De 3 rebuilds** (`magnolia_wintertuin`, `zonnebloem_zomeravond`,
   `zonnebloem_ochtendhoek`): goed genoeg als R4-basis, of moeten de
   **post-R4-handfixes van 8 jul** terug? Let op: het zijn `R3 + apply_r4` met de
   getrouwe 2-jul-libs, dus ze missen 8-jul-handwerk. Concreet: `zonnebloem_ochtendhoek`
   mist de `Deur_Stoep`-grindfix (rendert als grijze plaat → zie blocker hieronder).
2. **`magnolia_wintertuin`: winter of vroege lente?** (voorgrond zomergroen,
   achtergrond golden veld — inconsistent tot Beike kiest).
3. **Gras-aanpak** — zie ⚠️ bij S-E: de R5-grasmix is afgekeurd. Als gras-realism
   op tafel komt, welke richting wil Beike? Niet zelf de R5-mix terugzetten.
4. **Welke van de 13 scènes gaan door** (houden) en welke opnieuw (weg)?
5. **Opschoning uitvoeren?** (`_cleanup_weekend.ps1` draaien + `.gitignore.proposed`
   overnemen) en de overkappingen-finals committen — beide wachten op Beikes go.

---

## 4. Blockers eerst — technische landmijnen (vóór élke final)
Alle 3 zijn missende texturen (migratie-erfenis). Bron staat op schijf; fix = 1 stap.

- **`Deur_Stoep`-grind — `jasmijn_theehuis` + `zonnebloem_ochtendhoek`**
  (`zonnebloem_ochtendhoek` is hierdoor technisch NIET OK). De verwachte
  `T_vl0mfbllw_8K_B/_N.png` bestaan niet als PNG. **Aanbevolen fix = de bekende
  R4-swap `PavingStones125A`** (compleet in `assets/ambientcg/PavingStones125A/`):
  append `PavingStones125A_4K-JPG.blend`-materiaal óf vervang de image-nodes door
  `..._Color.jpg` + `..._NormalDX.jpg`. Dit is wat de verdwenen 8-jul-R4 al deed.
- **`wild_rooibos_bush_*` — `dahlia_leeshoek`** (nu buiten beeld = landmijn). Model-
  `.blend` staat er: `assets/polyhaven/models/wild_rooibos_bush_2k.blend` (textures
  waarschijnlijk daarin gepackt). Relink de leeshoek-images naar die packed versie,
  of re-append de struik uit dat .blend. Anders rendert hij magenta zodra de crop schuift.
- **Latente paden**: `dahlia_leeshoek` verwijst naar `AppData/…/Temp/tmp*` + oude
  `C:/Users/…`-paden; `magnolia_wintertuin` draagt nog de `aerial_grass_rock`-ref
  (witte rotsvlekken). → **Pack álles vóór elke final**: `bpy.ops.file.pack_all()`
  of File ▸ External Data ▸ Pack, of remap naar `assets/` op D:.

---

## 5. Systematische fixes (patroon-recepten; detail per scène staat in de QC-doc)
Werk deze in de review-loop per scène af; hieronder het standaardrecept per patroon.

- **S-B · Verankering ("staat er random" — Beikes #1, breedst gedeeld).** Verzonken
  leading-line-pad van de voorgrond-onderhoek naar de deur + border-/grind-randen
  langs verharding; zet hero-props (bv. camelia_wijnterras' bistroset) ÓP de tegels,
  niet in het gras. Dit vanaf fase 1 meenemen, niet als sausje achteraf.
- **S-C · Gras-door-verharding / hardscape zweeft op grastoppen.** `apply_r4`
  mask-cell 0.22 rond de footprint + verharding 1-2 cm verzinken + vuil/AO-randje.
- **S-D · Vlakke roze-paarse dawn-waas zonder zonrichting.** Zon laag (elev 8-15°,
  3500-4500K, energy 3-5), azimut zó dat één gevel oplicht + slagschaduwen.
  Referentie dat het kan: `jasmijn_familietuin` (echte zon + tak-schaduwen).
- **⚠️ S-E · Uniform "borstel-tapijt"-gras.** De QC beveelt clump-variatie +
  kleur/hoogte-variatie aan — **maar dat is de R5-grasmix die Beike afkeurde.**
  NIET zelf terugzetten. Leg de optie aan Beike voor en volg zijn richting; de
  huidige `scripts/grass_lib.py` bevat de R5-versie (257 rgls), de 2-jul-versie
  staat in `…_OLD\scripts` (132 rgls).
- **S-F · Dode practicals / lege overkapping-bay.** Emissie 2200-2700K + kleine
  warme point in de bol/lantaarn; zwakke warme area-fill in de bay (10-20 W,
  `use_shadow=False`).
- **S-G · Uitstekende auto-vloer onder de overkapping.** Houd de bay-vloer binnen
  de gevel/dakrand (buitenbad hot-tub-deck, familietuin voorrand, pluktuin apron).
- **S-H · Concept-signaal ontbreekt.** `zonnebloem_zomeravond` heeft géén
  zonnebloemen; `lavendel_lavendelveld` mist een lavendel-veld/rijen. Naam = belofte.
- **S-I · Gekleurde HDRI-vlek in de boomlijn.** HDRI ~20-40° draaien of het gat
  dichtzetten met donker boom-silhouet (buitenbad, ochtendnevel, avondkubus).
- **S-J · Probe-"floaters" zijn meestal vals-positief** (lantaarn-handles, props op
  een dek, bladermassa achter de heg). Niet achterna jagen tenzij visueel bevestigd;
  échte grounding-fout alleen bij `jasmijn_familietuin` (zandbak-frame zweeft).

---

## 6. Kritieke valkuilen (niet opnieuw in trappen)
- **Elke R4-rebuild uit R3 → gebruik de 2-jul `_OLD`-libs** (via `importlib`, zoals
  `scratchpad/apply_r4_faithful2.py`). De huidige `scripts/grass_lib.py` is naar de
  afgekeurde R5-gras gedrift; een naïeve `sys.path.insert` verliest van `cabin_lib`'s
  eigen insert. Zie `HANDOFF_WEEKEND_progress.md` › "KRITIEKE LES".
- **8 GB VRAM (RTX 3070):** `apply_r4`'s interne render (200 spp / 1920 + volume-mist)
  loopt vast (CPU-fallback). Voor rebuilds: **save-only** + preview los & licht
  (1280×720 / 110 spp, OPTIX). Finals apart renderen met bewuste settings.
- **Headless render wordt zwart** als de compositor aan staat → `scn.use_nodes = False`
  vóór `bpy.ops.render.render`. En schrijf output met `os.path.abspath`.
- **Pack vóór elke final** (anders magenta bij verplaatste texturen).

---

## 7. Aanbevolen volgorde
1. Server op :8767 + Monitor op `pilots_review_keuzes.json`.
2. Haal de 5 beslissingen uit §3 bij Beike (vooral: rebuilds oké? gras-richting?).
3. Fix de 3 **blockers** (§4) — puur technisch, geen creatief oordeel nodig.
4. Start de **review-loop, één scène tegelijk** in Beikes volgorde; pas per scène de
   relevante S-recepten (§5) toe; check-render → tonen → fix → volgende.
5. Pas als Beike per scène akkoord geeft: **finale render** (headless, hoge res, pack).
6. Commit / opschoning / overkappingen-finals: alleen op Beikes expliciete go.

*Bron: autonome weekend-run (Opus, 10 jul 2026). Alles hierin is voorbereiding —
de creatieve knopen en de sign-off liggen bij jou samen met Beike.*
