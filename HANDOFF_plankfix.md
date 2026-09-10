# Plankfix — wandplanken blokhutten (18 aug 2026)

> **GECONTROLEERD 2 sep — alle 15 finals in orde, geen regressies.** Onafhankelijke
> read-only check (geen renders): md5 ALLE_FINALS == `_qa20aug/*_FIXED` ==
> `D:\Blokhutwinkel-visuals-2026-08-20` (15/15). Numeriek in de 15 PLANKFIX-blends:
> één raster (start-afwijking 0,0000 cm, steek 13,5), geen daglicht tussen lagen,
> geen splinter, closers exact op referentie (0,0000 cm) en op/onder de wandtop,
> groefketen op alle wandmaterialen met kloppend z_ref/steek. Beeld-diff vs backup:
> shift 0,0, 0,45–4,88 % gewijzigd, ≤ 0,26 % buiten de cabin. Twee zichtbare dingen
> zijn géén plankfix-effect (identiek in de pre-fix backup): het donkere inkepinkje
> bovenaan de hoekkolom (S-reeks) en de verticale streepjeslijn waar wall-0/wall-7
> overlappen (zonnegroet, schaakavond). Rapport, scripts, JSON en voor/na-crops:
> `_plankfix_review/_qa02sep/` (REPORT.md). Nog open: closer-patch + deze handoff
> ongecommit; `D:\Blokhutwinkel-visuals-2026-08\` heeft nog de oude 15.

> **UPDATE 20 aug — closer-bug gevonden en gefixt, ALLE 15 finals vervangen:**
> QA-ronde over alle 15 plankfix-finals: `align_courses()` schoof de
> roofWallBoard-closers mee omlaag met verlaagde wanden terwijl de wandtop
> (z_end) gelijk blijft → gap van een halve laag (6,75 cm) onder het dak.
> Numerieke check (closer-posities origineel vs PLANKFIX): **alle 15 scènes
> geraakt** (2–4 closers per scène). Duidelijk zichtbaar op
> jasmijn_familiemiddag en camelia_leesplek; op de rest een subtiele donkere
> spleet onder de daklijn. Fix: closers NIET meer meeschuiven
> (`fix_cabin_boards.py` gepatcht), closers in alle 15 PLANKFIX-blends
> teruggezet via `_qa20aug/restore_closers.py` (referentie-JSON uit de
> originele blends), alle 15 finals opnieuw gerenderd (zelfde recept) en na
> before/after-QC vervangen in ALLE_FINALS én
> `D:\Blokhutwinkel-visuals-2026-08-20\`. Defecte 18-aug-versies bewaard als
> `_qa20aug/<naam>_DEFECT18aug.png`; QC-crops = `_qa20aug/QC_*.jpg`.
> Sweep over de overige 30 finals (previews in `_qa20aug/_sweep/`):
> kapschuren/creatief/webshop clean; de 8 R4-stijlen houden hun bekende
> verticale-textuur + oude planknaden (approved blend-staat bestaat niet
> meer, R4-swap is een per-scène keuze voor Beike — zie CMP_*.jpg).

Beike: "de blokhutten renders zijn bijna allemaal niet goed, in de configurator
stond een fout waardoor de planken niet allemaal even mooi leken — haal ze
opnieuw uit de configurator." Her-exporteren blijkt het niet op te lossen; de
reparatie is in Blender gedaan.

## Het defect (gemeten, niet gegokt)

In alle 33 GLB's in `source-glbs/` liggen naastgelegen wanden op een ander
laag-raster:

| | eerste laag start | toplaag |
|---|---|---|
| voor/achter (wall-0/2/8) | z = 6,00 cm | 7,5 cm |
| zijwanden (wall-1/3/7) | z = 12,75 cm | 14,25 cm |
| wall-openEnded-* | z = 12,75 cm | **0,75 cm splinter** |

Steek is 13,5 cm, dus de verschuiving is precies een halve laag. Gevolg: bij
élke hoek sluiten de horizontale naden van de twee wanden niet op elkaar aan.
Oorzaak: de aanzetlaag (`parentBoard-*-scaled`) is per wandrichting 7,5 óf
14,25 cm hoog; alles daarboven erft die verschuiving.

Tweede probleem: **de wand is geometrisch vlak.** Opeenvolgende planken
overlappen 1,5 cm (de tand) en hun buitenvlakken zijn coplanair. Een
chamfer/bevel helpt dus niet — die verdwijnt ín de buurplank (getest op 0,35 /
0,8 / 1,5 cm, geen van drieën zichtbaar). Daarom leest de wand als één glad
vlak en smeert de houttextuur uit.

## Her-export getest — lost het NIET op

Verse GLB uit tekentool-v2 gehaald op 18 aug (BHW select → BHW-select template →
"Meer informatie…" → "Exporteer GLB"; landt als naamloze `.tmp` in Downloads,
magic bytes `glTF`).

* Het **exportformaat is wél veranderd**: nu meters i.p.v. cm, root heet
  `blokhut` i.p.v. `shed`, geen `parentBoard-*-scaled`-nesting meer.
* De **plankfout is identiek**: wanden starten op 0,044 vs 0,102 m bij een steek
  van 0,109 m, en de openEnded-wand sluit met een splinter van 0,013 m.
* Productiebundel is van **6 aug 2026** (`app.editor.js`, `main.js` en `/3d/`
  Last-Modified). Als de fix ná die datum gemaakt is, staat hij nog niet live —
  dat is één berichtje aan de bouwer waard.
* Nieuw formaat is geen drop-in: `build_base_templates.py` gaat uit van cm +
  `shed` + parentBoard-scaling.

Camelia/Lelie/etc. zijn trouwens **BHW Select webshop-producten**, geen
tekentool-templates; het systeem heeft één generieke `BHW-select` template die je
zelf op maat sleept. Her-exporteren = 13 configuraties met de hand natekenen.
De "3D offerte aanvragen"-knop op de productpagina is een klantformulier, geen
exportpad.

## De reparatie

`scripts/fix_cabin_boards.py` — werkt **in-place in de scene-blends**, die de
hele board-hiërarchie nog bevatten. Dus géén cabin-swap: alle materialen, props,
camera's en licht blijven staan.

* `align_courses()` — legt alle wanden op één raster (laagste aanzet wint), vult
  de ontbrekende toplaag aan, haalt de splinter weg.
* `plank_groove()` — zet een bump op de wandmaterialen, gestuurd door wereld-Z
  gevouwen op de gemeten steek, zodat de naad exact op elke laaglijn valt.
* Unit-agnostisch: werkt zowel op een verse GLB (1 unit = 1 cm) als in een
  scene-blend (1 unit = 1 m). Nooit een lengte hard-coden hier.

Valkuilen die al gefixt zijn (niet opnieuw introduceren):

1. `bound_box` ververst pas bij een depsgraph-evaluatie → posities zelf
   bijhouden, niet tussentijds teruglezen (anders verschuift alles dubbel).
2. Boards dragen een eigen rotatie uit de glTF-import → verschuif de **mesh**,
   niet `obj.location` (die leeft in parent-space).
3. Bevel-breedte is in **lokale** units; boards hangen onder een niet-uniforme
   parent-scale → omrekenen, anders klemt de modifier zichzelf weg.
4. Wandmateriaal heet niet overal hetzelfde (de B-reeks noemt het `DG_wand`) →
   materialen van de board-objecten aflezen, niet op naam matchen.
5. Zit er al een bump op de Normal (Lelie) → de groef *chainen*, niet skippen.

## Wat er gedraaid heeft

`scripts/apply_plankfix.py` doet fix + final render en schrijft
`<naam>_PLANKFIX.blend` naast het origineel; renders gaan naar
`_plankfix_review/`. Let op: de S-reeks-finals zijn 4:3 (2560×1920) terwijl de
blends 16:9 opslaan — geef de hoogte dus expliciet mee.

**15 finals vervangen** in `ALLE_FINALS/`, originelen in
`ALLE_FINALS/_pre_plankfix_backup/`. QC via `scripts/qc_plankfix.py`: alle 15 op
uitsnede-shift 0,0 en 0,7–5,0% gewijzigde pixels (alleen de wanden).

**Buiten de ronde gehouden:**

* `roosmarijn_modern` — Beike's eigen Zentuin-werk, niet aanraken.
* 8 R4-stijlen — hun blend is ná de goedgekeurde final doorgeschoven, dus
  opnieuw renderen verandert het hele beeld en niet alleen de planken. Zie
  `scripts/audit_final_sources.py`, dat die drift opspoort. Ter vergelijking wel
  gerenderd naar `_plankfix_review/_r4/` — niets vervangen.
* De 51 filmpjes — die tonen nog de oude wanden.

`lelie_ochtendnevel` is het waarschuwingsgeval: de goedgekeurde final is de v3
van 24 jun, maar de enige blend op schijf is de R4 van 2 jul. Die 24-jun-staat is
overschreven en bestaat nergens meer.

## Reviewpagina

`python scripts/build_plankfix_review.py` bouwt `_plankfix_review/index.html`:
twee secties (vervangen / R4 ter vergelijking), klik op een beeld om te wisselen.
Thumbnails op 1100px, dus de pagina is ~9 MB i.p.v. 300 MB.

## Let op: datumstempels

De machineklok liep tijdens deze sessie vier dagen achter en is daarna
gesynchroniseerd. Het werk is van **18 aug 2026**, maar de bestanden die die dag
zijn weggeschreven (renders in `_plankfix_review/`, de `*_PLANKFIX.blend`s en de
backups in `ALLE_FINALS/_pre_plankfix_backup/`) dragen **mtime 14 aug**. Wie
bestanden aan dit document probeert te koppelen: dat is dezelfde dag.

## Nog open

1. De 8 R4-stijlen: goedgekeurde final houden (advies) of per scène wisselen.
2. De 51 filmpjes opnieuw renderen — meerdere nachten.
3. `D:\Blokhutwinkel-visuals-2026-08\` bevat nog de oude versies van die 15.

## R4-stijlen (8): juiste bron gevonden — 2 sep 2026, avond

De `_R4.blend`s op D: zijn NIET de staat van de goedgekeurde finals. `scripts/audit_final_sources.py`
(hash-match final ↔ pilot-render) wijst uit: de 8 finals in `ALLE_FINALS/blokhutten-stijlen` zijn de
`FINAL_v2`-renders van 20–24 jun (Lelie: `FINAL_v3` van 24 jun). De bijbehorende blends bestaan alleen
nog in de projectkopie `C:/Users/beike/Documents/Blender-blokhutten_OLD/pilots/<model>/style-*/`:
`<naam>_v2.blend` (6 scènes) en `<naam>_v3.blend` (Lelie), elk minuten vóór de final opgeslagen,
0 ontbrekende bestanden. Een render vanaf de D:-`_R4.blend` (13–17 jul) verschilt 88,6 % van de final
(R5-gras, donkere lucht, geen pad) — die proefrender staat in `_plankfix_review/_r4_2sep/_afgekeurde_basis/`.

Werkwijze vannacht: `_plankfix_review/_r4_2sep/run_r4_bron.sh` → `apply_plankfix.py` op de bronblend
(PLANKFIX-blend komt ernaast in de _OLD-kopie, zodat relatieve paden kloppen), render 2560×1440 / 512
naar `ALLE_FINALS/r4-plankfix-2sep/`. Extra: `lelie_ochtendnevel_ALT-v2basis` omdat de v3-blend op
1 jul opnieuw is opgeslagen (ná de final). QC: `qc_r4_bron.sh` (verify_plankfix + CMP + % gewijzigd).
Doorvoeren na Beikes review in de Werkbank-job: `scripts/apply_r4_keuze.py` (dry-run; `--doen`).
Let op: `ALLE_FINALS/` is niet in git (0 bestanden getrackt) — "finals committen" vraagt eerst een besluit.
Bijvangst: drie `*_R4_PLANKFIX.blend` op D: (buitenbad 18:30, wijnterras 18:57, leeshoek 19:06) komen uit
de afgekeurde basis en zijn waardeloos; niet verwijderd, Beike beslist.

### Uitkomst nacht 2 → 3 sep (R4 vanaf bronblends)

Alle 9 renders klaar (19:11–21:46, 7–28 min per scène), `verify_plankfix.py` overal 0 issues / 9 closers / 105 planken.
Beeldverschil t.o.v. de goedgekeurde final (640×360, drempel 30):

| scène | basis | anders | opmerking |
|---|---|---|---|
| camelia_buitenbad | v2 | 0,1 % | alleen planken |
| camelia_wijnterras | v2 | 0,8 % | alleen planken |
| dahlia_leeshoek | v2 | 1,7 % | veranda-hoek (overlap wall-0/wall-7): dunne streepjeslijn → 4 grotere donkere blokjes; tekentool-geometrie, door uitlijnen zichtbaarder |
| dahlia_tuinkantoor | v2 | 1,3 % | alleen planken |
| lavendel_lavendelveld | v2 | 0,3 % | alleen planken |
| lavendel_pluktuin | v2 | 0,4 % | alleen planken |
| lelie_avondkubus | v3 | 6,6 % | onderrand ca. 3 % lichter (mist/denoise of nabewerking op de oude final); inhoud gelijk |
| lelie_ochtendnevel | v3 (1 jul) | 6,0 % | nerf loopt nu met de plank mee (oude final: verticale box-projectie), iets warmer |
| lelie_ochtendnevel_ALT-v2basis | v2 (20 jun) | 95,6 % | oudere scène-staat van vóór de review (barbecue, groen kleed, scherper licht) → geen kandidaat |

Resultaten: `ALLE_FINALS/r4-plankfix-2sep/` (9 PNG + 9 `CMP_` + 9 `CROP_`), overzicht `_plankfix_review/_r4_2sep/OVERZICHT_r4_plankfix.jpg`,
QC-log `qc_bron.log`, verify-JSON's `verify_<naam>.json`. PLANKFIX-blends staan naast de bron in de _OLD-kopie (`*_v2_PLANKFIX.blend` / `*_v3_PLANKFIX.blend`).
Open voor Beike: per scène goed/fix/weg in de Werkbank-job; daarna `python scripts/apply_r4_keuze.py --doen`.

### Veranda-hoek: coplanaire overlap wall-0/wall-7 (2 sep, 22:00)

Alle 8 R4-modellen (en de ALT) hebben dezelfde junction: `wall-7` (canopy-achterwand, materiaal `basetexture-firstLayer-canopyWall`)
loopt 20 cm door in de span van `wall-0`, in exact hetzelfde vlak (y −1,2947…−1,2747). Vóór het uitlijnen maskeerden de twee
plankensets elkaars naden (dunne streepjeslijn); na het uitlijnen vallen de naden samen → z-fight en donkere gaten in de hoek.
Probe (`_plankfix_review/_r4_2sep/_hoekprobe/`, border-render van de junction in dahlia_leeshoek):
A as-is = gekartelde hoek met zwarte gaten; **B wall-7 6 mm naar binnen = schone hoek** (wall-0 ligt vóór); C vulplaat = gaten dicht maar kartel blijft.
Uitgewerkt als opt-in stap `fix_cabin_boards.separate_overlapping_walls(offset=0.006)` (niet in `fix_cabin()`/`apply_plankfix.py`):
zoekt coplanaire overlappende wanden, schuift de canopy-wand (anders hoogste index) met closers `offset` van de camera af.
Demo-render: `ALLE_FINALS/r4-plankfix-2sep/dahlia_leeshoek_ALT-hoekfix.png` (+ CMP_/CROP_), via `_r4_2sep/apply_plankfix_hoekfix.py`.
Als Beike de hoekfix wil: stap toevoegen in `apply_plankfix.py` en de 8 R4 + 15 tuinscenes opnieuw renderen (zelfde junction zit in alle modellen).
Reikwijdte: van de 15 tuinscenes hebben 14 dezelfde junction in beeld (alleen `magnolia_atelier` niet; verify-JSON's in
`_plankfix_review/_qa02sep/json/`), plus alle 8 R4. Een hoekfix-ronde is dus 22 renders.
Uitkomst demo (22:12): `dahlia_leeshoek_ALT-hoekfix` verify 0 issues, 1,7 % anders dan de oude final, hoek schoon (geen blokjes, geen streepjeslijn).
Hoek-sweep 14 tuinscenes (22:16–22:33, `_hoekprobe/sweep_hoek.sh` + `analyse_sweep.py`, blad `SWEEP_hoek.jpg`): zichtbaar bij
zonnebloem_zonnegroet 3,3 % · lavendel_buitenbioscoop 3,1 % · roosmarijn_uitslaapochtend 2,6 % · roosmarijn_schaakavond 2,6 % ·
jasmijn_vinylmiddag 1,7 % (dunne donkere streepjeslijn in de veranda-binnenhoek); jasmijn_vlindertuin 0,7 % (achter paal);
de overige 8 hebben de junction achter het deurkozijn (0 %). Hoekfix-ronde = 8 R4 + 5 à 6 tuinscenes, niet 22.
Vervolg (22:37): hoekfix-kandidaten voor de 6 tuinscenes worden vannacht gerenderd vanaf de bestaande PLANKFIX-blends
(`_hoekprobe/render_tuin_hoekfix.sh` → `ALLE_FINALS/hoekfix-kandidaten-2sep/<naam>_ALT-hoekfix.png` + CMP_/CROP_ via `qc_tuin.py`),
te beoordelen in de nieuwe Werkbank-job 'Veranda-hoekfix: kandidaten tuinscenes (6)'; doorvoeren met `scripts/apply_hoekfix_keuze.py --doen`
(goed → vervangt in blokhutten-tuinscenes, oude naar `_pre_hoekfix_backup`). R4-hoekprobe (`sweep_r4.sh`) bepaalt welke R4-scènes de hoek tonen.
R4-hoekprobe (22:35–22:39, `_hoekprobe/R4_*`): bij de 7 andere R4-stijlen zit de junction achter het deurkozijn (0,0 %); alleen
dahlia_leeshoek toont de hoek → geen R4-hoekfix-ronde nodig, de kandidaat `dahlia_leeshoek_ALT-hoekfix` volstaat.
Uitkomst tuinscene-kandidaten (23:07): 6 renders, 0,1 % anders (zonnegroet 0,3 %), streepjeslijn weg, verder identiek. `*_PLANKFIX_HOEKFIX.blend` naast de PLANKFIX-blends in `pilots/B10…B15`.

### 3 sep ochtend: review doorgevoerd + hoekfix-richting
Beikes review (Werkbank): buitenbad, lavendelveld, pluktuin, avondkubus → vervangen in `blokhutten-stijlen` (oude in `_pre_plankfix_backup`).
Fix-notities: wijnterras overbelicht; tuinkantoor te glimmend; leeshoek donkere dak/wand-kier + belichting; ochtendnevel 'zwarte plank' links =
de closer van wall-3 (`parentBoard-3-scaled-roofWallBoard-0`, wél wandmateriaal) in de harde slagschaduw van de dakrand; ALT-v2basis = weg.
Hoekfix: 'naar binnen' gaf een grijze strook (cabinewand vóór), 'naar voren' (`offset=-0.006` toen, nu standaard) houdt de blanke canopy-wand vóór →
`dahlia_leeshoek_ALT-hoekfix2` is de betere kandidaat; standaardrichting in `separate_overlapping_walls` omgezet naar 'naar de camera toe'.
Werkbank-galerij gefixt (df5d64f): volgorde = raster, focus blijft na oordeel, thumbnails vooraf.

### 3 sep 11:29: alle 8 R4-finals vervangen
Via het nieuwe Werkbank-reviewblad koos Beike: wijnterras → `_ALT-fixB` (exposure −0,3), tuinkantoor → `_ALT-fixB` (wand ruwheid 0,9 / spec 0,25),
leeshoek → `_ALT-hoekfix2` (canopy-wand naar voren, geen vullamp), ochtendnevel → `_ALT-fixA` (zonneschijf 6°, hemel 1,25). Samen met de vier van
vanmorgen zijn alle 8 finals in `blokhutten-stijlen` vervangen; oude in `_pre_plankfix_backup`. Fixronde-tooling: `_plankfix_review/_r4_2sep/_fixronde/`
(`fixround.py` met tweaks exposure/sun_energy/sun_angle/sun_rot/world_strength/mats/fill_canopy). Let op: de fix-varianten zijn renders met
runtime-tweaks; de bijbehorende blend is NIET opgeslagen (de PLANKFIX-/HOEKFIX2-blend + de tweak-JSON in `vol_*.sh` zijn de bron).
