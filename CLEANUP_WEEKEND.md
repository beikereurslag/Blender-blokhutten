# CLEANUP_WEEKEND — voorbereiding grote opschoning

> Gegenereerd als **voorstel**. Er is **niets** verwijderd, verplaatst, ge-`add`, ge-`commit` of
> ge-`checkout`. Alle acties hieronder voer je maandag zelf uit. Meetmoment: working tree op
> branch `weekend-renders`.

## TL;DR

- `git status --porcelain` toont **993 untracked entries** (sommige zijn ingeklapte, volledig
  untracked mappen; achter die 993 entries zitten **~2772 losse untracked bestanden**).
- De ruis komt bijna volledig uit **3 hoeken**: `assets/` (479 entries, ~27 GB downloads),
  `overkappingen-website/` (229 entries, apart deel-project) en `pilots/` (185 entries,
  scenes + previews). `_diag/` (57) + `__pycache__/`/`*.pyc` (17) is de rest van de echte rommel.
- **Aanbevolen mechanisme per categorie:**
  - **GITIGNORE** = voortaan negeren, bestand blijft gewoon op schijf staan (niet-destructief).
  - **QUARANTAINE** = fysiek verplaatsen naar `_quarantine_weekend/` via `_cleanup_weekend.ps1`
    (omkeerbaar; verwijderen doe je pas ná controle).
  - **HANDMATIG BEKIJKEN** = risico op referenties door scripts/pipeline of het is een
    deliverable/projectbestand → jij beslist per stuk.
- **Enige QUARANTAINE-voorstel in dit ronde: `_diag/` (89 bestanden, ~17,3 MB).** Bewust klein
  en veilig gehouden. Al het grote spul (assets, thumbs) gaat via GITIGNORE zodat er geen
  gigabytes verplaatst hoeven worden.

## Belangrijke bevindingen vooraf (lees dit eerst)

1. **De "~74 losse `_*.py` scripts in root" zijn al getrackt.** Op schijf staan 74 `_*.py` in
   root, maar **73 daarvan zijn al door git getrackt**. Slechts **1** is untracked:
   `_anker_kampvuur3.py`. Er is dus géén grote berg untracked root-scripts om op te ruimen.
2. **Er zijn 0 untracked `.blend1`-bestanden.** `.blend1` werd vroeger juist wél getrackt
   (`git status` toont nu `D pilots/Magnolia-.../magnolia_modern.blend1` = een getrackte backup die
   verdween). Het `*.blend1`-patroon in de voorgestelde `.gitignore` is dus **preventief**.
3. **`assets/` is deels getrackt.** 896 bestanden onder `assets/` staan al in git (o.a. de hele
   `assets/3daistudio/`). GITIGNORE is niet-destructief (raakt getrackte bestanden niet), maar bij
   de **deels-getrackte** libs (polyhaven, sketchfab) moet jij nog beslissen of je de rest wilt
   `git add`-en óf gitignoren + de getrackte binaries `git rm --cached`-en. Daarom staan die op
   HANDMATIG.
4. **`_diag/` is óók deels getrackt** (286 getrackte bestanden). Het quarantaine-script raakt
   uitsluitend de **untracked** `_diag`-bestanden aan (het vraagt de lijst live op bij git), dus de
   286 getrackte bestanden blijven ongemoeid.
5. **`overkappingen-website/` is een apart, levend deel-project** met o.a. `scenes/` = **~70 GB**
   aan `.blend`-bestanden. Per opdracht: **niet aanraken.** De ruis daar (diag/logs) ruim je op
   binnen dat sub-project zelf, niet in deze ronde.

## Categorie-tabel

| # | Categorie | Entries (porcelain) | Losse bestanden | Grootte | Aanbeveling |
|---|-----------|--------------------:|----------------:|--------:|-------------|
| A | `__pycache__/` + `*.pyc` (root, `scripts/`, `overkappingen-website/`) | 17 | 16 untracked (+14 al getrackt) | < 1 MB | **GITIGNORE** |
| B | `_diag/` wegwerp-diagnostiek (untracked) | 57 | 89 | ~17,3 MB | **QUARANTAINE** (+ gitignore `_diag/`) |
| C | `assets/` — externe download-libs, overwegend untracked (`blenderkit/`, `ambientcg/`, `blenderkit-v3.21.0.260628/`, losse `*.zip`) | ~70 | ~530 | ~13,7 GB | **GITIGNORE** |
| D | `assets/` — deels getrackte libs + eigen props (`polyhaven/`, `sketchfab/`, `blokhutwinkel-textures/`, `props-beike/`, losse `.blend`) | ~409 | ~1000 | ~12,5 GB | **HANDMATIG** |
| E | Review-thumbs die de review-server serveert (`_pilots_review_thumbs/`, `_r3_thumbs/`) | 2 | 81 | ~13,4 MB | **GITIGNORE** |
| F | Review-/feedback-snapshots (`_round2_review/`, `feedback_pages/`) | 2 | 47 | ~135 MB | **GITIGNORE** |
| G | `tools/` — portable 7-zip binary | 1 | 109 | ~8,1 MB | **GITIGNORE** |
| H | `pilots/**` — `.blend` scenes (62) + previews (116, incl. **13× `*_R4_PREVIEW.png` = deliverables**) | 185 | 178 | groot | **HANDMATIG / NIET AANRAKEN** |
| I | `overkappingen-website/**` — apart deel-project (incl. `scenes/` ~70 GB) | 229 | ~500 | ~71 GB | **NIET AANRAKEN / HANDMATIG** |
| J | `kapschuren/**` — `.glb`, `.blend`, `*_PREVIEW.png` | 12 | ~75 | — | **HANDMATIG / NIET AANRAKEN** |
| K | `training/**` — `.blend` + `builds/` | 3 | ~5 | — | **HANDMATIG** |
| L | `scripts/_*.sh` — losse one-off shell-helpers | 4 | 4 | < 1 MB | **HANDMATIG** |
| M | Losse root-bestanden (`_anker_kampvuur3.py`, `hedge_test.blend`, `pilots_review_keuzes.json`, `HANDOFF_WEEKEND_progress.md`) | 4 | 4 | klein | **HANDMATIG** |

> Groottes zijn afgerond (`du`/`stat`). Entry-tellingen tellen deels dubbel over rijen heen door
> ingeklapte mappen; ze zijn indicatief, niet exact optelbaar tot 993.

---

## Detail per categorie

### A. `__pycache__/` + `*.pyc` — GITIGNORE
Untracked: 7× `__pycache__/*.pyc` (root, o.a. `swap_dl_fix`, `swap_pk_fix`), 9×
`scripts/__pycache__/*.pyc` (o.a. `cabin_lib`, `grass_lib`, `render_final`), plus de ingeklapte
`overkappingen-website/__pycache__/`. Puur regenereerbare bytecode.
- **Let op:** er staan al **14 `.pyc` getrackt** in de repo. `.gitignore` haalt die *niet* weg.
  Wil je ze schoon uit de index: `git rm --cached <pad>` (jouw keuze, niet in dit voorstel).

### B. `_diag/` — QUARANTAINE (+ gitignore)
89 untracked bestanden, ~17,3 MB: `chain*.log`, `prev_*.log`, `anker_*.txt`, `crop_*.png`,
`qc_*.png`, `s2*.png`, `sun_A/B/C.png`, `spruce_test_*.png`, `wt_test_*.png`, de
server-logs (`http_server.log`, `pilots_review_server.log`) en de map `_diag/weekend/` (33 stuks).
Dit is klassieke wegwerp-diagnostiek, niet gebruikt als input door de render-pipeline.
- **Dit is de enige categorie die `_cleanup_weekend.ps1` verplaatst.** Het script vraagt de lijst
  live bij git op (`ls-files --others`), dus alleen untracked `_diag`-bestanden bewegen; de 286
  getrackte `_diag`-bestanden blijven staan.
- **Kleine kanttekening:** draait er nog een review-/http-server, dan kan een `.log` in gebruik
  (locked) zijn. Het script vangt dat per bestand op en gaat door. Stop de servers vóór het runnen.
- In de voorgestelde `.gitignore` staat `_diag/` zodat toekomstige diag-runs niet opnieuw ruis
  geven (getrackte `_diag`-bestanden blijven getrackt; gitignore raakt die niet).

### C. `assets/` externe download-libs (overwegend untracked) — GITIGNORE
`assets/blenderkit/` (13 GB, 2/220 getrackt), `assets/ambientcg/` (417 MB, 0 getrackt),
`assets/blenderkit-v3.21.0.260628/` (68 MB, 63/149 getrackt), losse `assets/*.zip` (Bed.zip,
Chairs.zip, Carpet016…, Stone Pack…, etc.). Dit zijn **reproduceerbare externe downloads**
(BlenderKit/AmbientCG) die scenes als **input** gebruiken → moeten op schijf blijven → gitignore
(uit git-status, blijft op disk), **nooit quarantaine, nooit verwijderen**.
- Gitignore is niet-destructief; de enkele getrackte bestanden hierin blijven getrackt.

### D. `assets/` deels-getrackte libs + eigen props — HANDMATIG
- `assets/polyhaven/` (6,1 GB, **353/847 getrackt** → 372 untracked entries, de **grootste enkele
  bron van git-status-ruis**).
- `assets/sketchfab/` (3,7 GB, 424/618 getrackt).
- `assets/blokhutwinkel-textures/` (307 MB, 22/28 getrackt).
- `assets/props-beike/` (2,0 GB, 0 getrackt — jouw eigen gesourcete props).
- Losse root-`.blend` in `assets/` (Chess set, Classic Milano Armchair, Horizon coffe table,
  Set of japanese lamps).

Waarom handmatig: deze libs zijn **half getrackt**. Wil je ze uit git-status krijgen, dan is er een
keuze te maken (rest `git add`-en, óf gitignoren én de getrackte binaries `git rm --cached`-en).
`props-beike/` is jouw eigen materiaal — mogelijk wil je dat juist versioneren. Deze keuze wil ik
niet voor je maken. Concreet advies staat in "Uitvoerplan".

### E. Review-thumbs die de server serveert — GITIGNORE
`_pilots_review_thumbs/` (8,9 MB, 44 stuks) en `_r3_thumbs/` (4,5 MB, 37 stuks). **Volledig
untracked**, maar wél gerefereerd door `pilots_review_server.py` / `_r3_review_gen.py`. Daarom
**gitignore (blijft op schijf, server blijft werken)** i.p.v. quarantaine (verplaatsen zou de
review-server breken). Regenereerbaar.

### F. Review-/feedback-snapshots — GITIGNORE
`_round2_review/` (121 MB, 22 PNG's; VOOR/NA-vergelijkingen) en `feedback_pages/` (14 MB, 25 crops).
Volledig untracked, puur output. Ze worden bij naam genoemd in `HANDOFF_R4_progress.md` en het
compendium, dus **gitignore (op schijf laten)** houdt die verwijzingen geldig; quarantaine zou de
paden in die docs dood maken. Wil je ze écht weg, dan handmatig na controle.

### G. `tools/` — GITIGNORE
Portable 7-Zip (`tools/7z/…`, installer + dll's, 109 bestanden, 8,1 MB). Externe binary, niet door
een getrackt `.py` gebruikt (alleen genoemd in `HANDOFF_overkappingen.md`). Hoort niet in git →
gitignore, op schijf laten.

### H. `pilots/**` — HANDMATIG / NIET AANRAKEN
62 untracked `.blend` (o.a. de `*_R4.blend` scene-bestanden) en 116 untracked PNG's. Daarvan zijn
**13× `*_R4_PREVIEW.png` de huidige-ronde deliverables (MOETEN BLIJVEN)**. De rest zijn previews
van oudere iteraties (`R2/R3/RIG/REVIEW/WANDTEX/FIX2_PREVIEW.png`). Omdat `.blend` en
deliverable-previews expliciet níet aangeraakt mogen worden, én omdat het onderscheiden van
"welke ronde is definitief" jouw oordeel vergt: **niets quarantainen, niets gitignoren.** Jij
beslist per stuk wat je `git add`-t (deliverables) en wat weg mag (oude rondes).

### I. `overkappingen-website/**` — NIET AANRAKEN
Apart, levend deel-project. Untracked: `scenes/` (~70 GB `.blend`), `renders/creatieve-tuin-finals/`
(109 MB = **finals/deliverables**), `glb/` (951 MB productgeometrie), `logs/` (71 MB) + 46 losse
`logs_concept*_stap2_*.log`, `diag/` (169 bestanden), `referentie/` (26 MB), `_review_thumbs/`
(12 MB), `__pycache__/`. Per opdracht **off-limits in deze ronde.** De enige raakvlak: de generieke
`__pycache__/` + `*.pyc` gitignore-regels vangen ook `overkappingen-website/__pycache__/` af — dat
is niet-destructief. De rest ruim je binnen dat sub-project zelf op.

### J. `kapschuren/**` — HANDMATIG / NIET AANRAKEN
`glb/*.glb` (echte productgeometrie), `scenes/*.blend` (A_lounge, B_dining, C_bergkap) +
`*_PREVIEW.png`, `previews/`, `scenes/diag/`. Bevat `.blend`, `.glb` en previews → projectbestanden,
niet aanraken. `scenes/diag/` mag je later handmatig opschonen.

### K. `training/**` — HANDMATIG
`applied_test_01.blend`, `study_01_grass.blend`, `builds/`. Studie/test-`.blend`s → jij beslist of
dit bewaard/getrackt moet worden.

### L. `scripts/_*.sh` — HANDMATIG
`_batch_ground_fix.sh`, `_dry_rmpath.sh`, `_dry_rmpath2.sh`, `_retry_previews.sh`. One-off
shell-helpers in de `scripts/`-map. Klein maar het zijn scripts → risico op referenties. Zelf even
bekijken of ze nog nut hebben; niet automatisch verplaatsen.

### M. Losse root-bestanden — HANDMATIG
- `_anker_kampvuur3.py` — echt render-script (Kampvuur anker-iteratie 4, draait op `.blend` via
  `blender -b … --python`). Mogelijk committen of bewaren → jouw keuze.
- `hedge_test.blend` (212 K) — test-scene (`.blend`, niet aanraken).
- `pilots_review_keuzes.json` — keuze-data die de review-server leest/schrijft. Data, niet weg.
- `HANDOFF_WEEKEND_progress.md` — HANDOFF-doc → conform regels niet aanraken; waarschijnlijk
  committen.

---

## Wat NIET aangeraakt mag worden (harde lijst)

- **Alle `.blend`-bestanden** (pilots, kapschuren, training, overkappingen-website, root
  `hedge_test.blend`, losse `assets/*.blend`).
- **Deliverable-previews:** `pilots/**/**_R4_PREVIEW.png` (13 stuks) en
  `overkappingen-website/renders/creatieve-tuin-finals/**`.
- **Kernbibliotheken in `scripts/`**: `cabin_lib.py`, `grass_lib.py`, `swap_lib.py` en de andere
  getrackte `scripts/*.py` (niet in scope; alleen de untracked `_*.sh` zijn genoemd, als HANDMATIG).
- **Alle `PLAN_*.md`, `REVIEW_*.md`, `HANDOFF_*.md`** (incl. `HANDOFF_WEEKEND_progress.md`).
- **De hele `overkappingen-website/`-map.**
- **`.glb` productgeometrie** (`kapschuren/glb/`, `overkappingen-website/glb/`).
- **Assets die als scene-input dienen** (worden gitignored = blijven op schijf; nooit verwijderd).
- **De bestaande `.gitignore`** — dit voorstel schrijft naar `.gitignore.proposed`, niet erover.

---

## Twijfelgevallen → bewust op HANDMATIG (niet genegeerd, niet gequarantained)

- Oudere pilot-previews (`*_R2/R3/RIG/REVIEW/WANDTEX_PREVIEW.png`): staan náást echte deliverables;
  welke ronde definitief is, is jouw oordeel.
- `props-beike/`: eigen gesourcete props — misschien juist versioneren.
- Deels-getrackte `polyhaven/` + `sketchfab/`: gitignore vs. `git add` vs. `git rm --cached` is een
  bewuste keuze.
- `scripts/_*.sh` + `_anker_kampvuur3.py`: scripts kunnen door pipeline/handmatig aangeroepen worden.

---

## Uitvoerplan maandag (voorgestelde volgorde)

1. **Backup/rustpunt:** je hebt al commit `571719d` als restore-point. Prima startpunt.
2. **Gitignore toepassen:** controleer `.gitignore.proposed`, en als akkoord:
   voeg de inhoud toe aan `.gitignore` (bijv. handmatig samenvoegen). Dit haalt in één klap
   categorieën A, C, E, F, G uit `git status` (blijft allemaal op schijf).
3. **Quarantaine (categorie B):** draai eerst `.\_cleanup_weekend.ps1` (staat op `$DryRun = $true`,
   print alleen). Bevalt de lijst? Zet `$DryRun = $false` en draai opnieuw. `_diag`-untracked
   (~17,3 MB) staat dan in `_quarantine_weekend/_diag/…`. Controleer, en verwijder pas daarna
   handmatig als je zeker bent.
4. **Deels-getrackte assets (categorie D):** beslis per lib. Aanbeveling:
   - `polyhaven/`, `sketchfab/`: gitignore de mappen én `git rm --cached -r` de reeds getrackte
     binaries als je ze niet in git wilt (grote binaries horen niet in git). Puur jouw keuze.
   - `props-beike/`: bewust versioneren of gitignoren.
5. **Handmatige categorieën (H, I, J, K, L, M):** loop ze door wanneer je tijd hebt; geen haast,
   geen automatisering.
6. **Reeds getrackte rommel opschonen (optioneel):** 14 `.pyc` en de verdwenen `.blend1` staan in
   de index/historie. `git rm --cached` + committen ruimt de index op (verwijdert niets van schijf).

## Opgeleverde bestanden
- `D:\Blender-blokhutten\CLEANUP_WEEKEND.md` (dit rapport)
- `D:\Blender-blokhutten\_cleanup_weekend.ps1` (quarantaine-script, DryRun aan)
- `D:\Blender-blokhutten\.gitignore.proposed` (voorstel-gitignore, overschrijft de echte niet)
