# HANDOFF — Overkapping Website Renders (2–9 jul 2026)

## 🏡 RONDE 3-B (9 jul) — CREATIEVE TUIN-ELEMENTEN (nieuwe koers)

**Beike stopte de losse omgevingen** ("we stoppen met dit; we houden de tuin
setting die we al hadden met heg + HDRI erachter; leuke creatieve ideeën ín de
tuin zoals dat zwembad"). Nieuwe lijn: **vertrouwde tuin + één blikvanger-element
per blend.** Beike koos alle 4:
- **Zwembad-tuin** (Douglas 700x400): DIY rechthoekig bad in pooldeck vóór de
  kap (poolhouse) + ligbedden. `scene_zwembad.py`. ✓
- **Wellness/hottub** (Douglas 600x300): DIY douglas-hottub (scene_b-recept) +
  ligbedden + stoom, avond. `scene_wellness.py`. ✓
- **Buitenkeuken** (Douglas 1000x400): DIY keukenblok + inbouwgrill (concept
  C-recept) + pizza-oven + lange eettafel + festoen, golden hour.
  `scene_keuken.py`. ✓
- **Vuurtafel-lounge** (Douglas 600x300): DIY corten gas-vuurtafel (gloeiend
  sintelbed + warme point light; géén geometrie-vlammen — klippen wit onder
  AgX) + loungekring + plaid, gouden avond. `scene_vuurtafel.py`. ✓

Alle 4 delen **`scene_tuin_basis.py`** (gedeelde staging: hardscape/groen/gazon/
licht/camera/afronden). Site: review_server TUIN-lijst; sectie ① aangekleed,
② ankers, ③ al-goedgekeurd (R3 Regendag + S3 Stadspatio). Wacht op Beikes review.
Les: gazon-veld tot y-11 (anders kale grond-slab op de voorgrond bij brede maten).
De omgeving-scènes (W3/B3/O3/D3) zijn geparkeerd (op schijf, van de site af).

## 🌊 RONDE 3 (9 jul, Fable) — omgevings-concepten [GEPARKEERD, zie ronde 3-B]

Beike: "voor dezelfde overkappingen nog meer blends, creatiever in de
omgeving, zoek online op, gebruik het plan in Obsidian." → 5 nieuwe concepten
waar de OMGEVING het verhaal is (research 9 jul: waterkant = benoemde
2026-trend; NIEMAND toont regen — hét productargument; gaten: polder/duin/
bos/stadspatio). Plannen: `PLAN_concept_[W3|B3|R3|D3|S3]_*.md`.

| Concept | SKU | Omgeving/tijd | Stand |
|---|---|---|---|
| W3 Waterkant | Douglas 500x300 | sloot+vlonder+rietkraag, golden hour | **stap1+stap2 op review-site** (11 anker-QC-rondes; lessen in OPUS_WERKWIJZE §8: OOM→linked-kopieën, waterband-hoeken, ooghoogte-vs-haag, bleke-bloeiers-tegenlicht, camera-ray-probe) |
| B3 Bosrand | Douglas 700x400 | boskavel, ochtendmist, sparren, hangstoel | **stap1+stap2 op review-site** (BK-hangmatten = muur-gemonteerd, boren in productpalen = nee → hangstoel; DIY-douglas-hangmatframe = wishlist) |
| R3 Regendag | KDI 600x420 | regen! plassen spiegelen warme verlichting | **stap1+stap2 op review-site** (het beeld dat geen concurrent heeft; regen-streaks als optionele fixronde) |
| D3 Duintuin | Douglas 400x300 | helmgras/zand/schelpenpad, kustdag | **stap1+stap2 op review-site** (zand-PBR is grijs-beige → warme MULTIPLY-node nodig; painted bench las als rode kast → weg) |
| S3 Stadspatio | KDI 300x300 | ommuurd hofje, blauw uur, bistro | **stap1+stap2 op review-site** (baksteen-BUG: muurdeksel-boxen met zbot=-0.06 = vólle-hoogte grijze platen dekten de steen af → dunne kap 8cm bovenop; AmbientCG→PH-naamgeving voor pbr_from_folder) |

**ALLE 5 RONDE-3-CONCEPTEN staan stap1+stap2 op localhost:8766, wachten op Beikes
review.** Volgende: Beike-feedback per concept afwerken (live-loop), dan finals na
akkoord. Optie R3: echte regen-streaks (geometry-nodes-recept in het plan).

### 🔁 KOERSWIJZIGING 9 jul (Beike review) — LEES DIT
Beike: **"de omgevingen zijn nog lang niet goed genoeg"** + **"klopt niet bij een
overkapping"** + strand **"dat thema wordt hem niet"**. Kernles: een overkapping
is een terras/tuin-bouwwerk → hoort in een **echte, bewoonde tuin/terras**, NIET
los in de natuur (water/bos/duin = fout). Gekozen koers: **echte tuinen; natuur
alleen als RAND** (achter een echte tuingrens).
- **Site opgeschoond**: review_server toont nu ALLEEN de ronde-3-omgevingen
  (RONDE3-lijst = W3/B3/R3/S3), al het oude werk + de strandscene D3 zijn eraf
  (files blijven op schijf). D3-strand = **geschrapt** (thema afgekeurd).
- **W3 HERZIEN → "tuin aan het water"**: kap in ontworpen tuin (gazon/pad/
  borders/buxus/tuinboom), water als achtergrond achter een lage rietoever
  (`bank_y = D+3`); loungeset kijkt naar het water. Stap1+stap2 gerenderd,
  leest nu als echte tuin. **Wacht op Beikes OK op de richting** vóór uitrol.
  Open vraag: kiara_7 geeft bergen (Como-look) — Nederlandser/vlakker kan.
- **KOERS VOLLEDIG UITGEVOERD (9 jul):** feedback per scène verwerkt:
  - **W3 Waterkant** herzien r3: Beike "water slecht te zien" → brede OPEN plas
    links+rechts van de kap, natuurlijke rietoever, kap in echte tuin. ✓
  - **B3 Bosrand** herzien: Beike "bos veel te leeg, niet 5 bomen" → DICHT bos
    (73 instanties: gelaagd edge-struiken+varens + hoge sparren-rijen + zij-
    schermen, mist), kap in echte tuin, gazon-voorgrond. `dicht_bos()` in
    scene_b3. ✓
  - **O3 Boomgaard** NIEUW (`scene_o3_boomgaard.py`, vervangt strand): landelijk
    erf, fruitbomen, appels in gras + appelkist + fruitschaal, warme namiddag. ✓
  - **R3 Regendag** + **S3 Stadspatio**: door Beike op "houden" gezet (geen
    wijziging). ✓
- **Site**: review_server RONDE3 = [W3,B3,O3,R3,S3]; alle 5 stap1+stap2 op
  localhost:8766. Wacht op Beikes review van de herziene set.
- Kernles vastgelegd: overkapping hoort in ECHTE tuin, natuur/erf als RAND —
  wild-natuur (kap in water/bos/duin) is afgekeurd. Zie OPUS_WERKWIJZE + memory.

Assets 9 jul: BK free hangmat (2x, royalty_free) + bistroset (2x) binnen
(`_bk_ronde3.py`); riet/helmgras bestaat niet free → DIY (riet_pol-recept in
scene_w3) / PH-pollen schuin; PH `aerial_beach_01` zand-PBR (CC0) gedownload.
GPU gedeeld met pilots-sessie: vóór elke render `blender -b`-processen checken.
**Geen commits, geen finals zonder akkoord.**

## ☀️ OCHTEND-SUMMARY 8 JUL (nachtrun Fable) — LEES DIT EERST

**FINALS KLAAR (8 jul 14:58): alle 9 goedgekeurde concepten (A,B,C,D,
F,G,H,I,P) staan op 2560x1920/512 in `renders\finals\` — elk ~2.5-4 min,
allemaal QC ✓ (H als laatste met banktafel-kwartslag r9).
NIEUWE RONDE (Beikes opdracht): 5 SKU's compleet opnieuw — E2 "Scandi-
ontbijthoek" (Douglas 300x300, ochtend), J2 "Minimal courtyard" (KDI
300x300, middag), M2 "Avondlounge" (KDI 360x300, dusk), BO2 "Botanische
kamer" (KDI 600x300, ochtend) én D2 "Fietsen-thuisbasis" (KDI 420x300,
namiddag — D was "toch net niet", D-final vervalt; bakfiets+stadsfiets
uit BK-voorraad, middenpaal blijft staan). Plannen `PLAN_concept_*2_*.md`,
scripts `scene_*2_*.py`. NIEUW: `st.border_lush()` (Beike: "plantenbakken
overal niet goed gelukt") — volle borders uit BK `border-planten\`
(bush+lavendel+geranium; max 5+6 instanties, BO2 r2 = GPU-OOM-les;
texture_limit '1024' in alle nieuwe diag-takken).
STAND 8 jul ~16:40: stap2-feedbackronde 1 VERWERKT en QC ✓ op de site:
E2 r3 (mysterie-object op stoel = Kan, mee met side_table), J2 r2
(betonbank h 0.80 = 2x zo groot; bad uit de muur, x tot 2.55), M2 r2
(lichtfix: zon 1.4 elev 8, fills 18/14, glow 14/12/12, exp 0.40 —
avond nu leesbaar), BO2 r2 (gieter bij plantentafel, varenbak recht
rot_z=0.0, monstera vrij van bank op (5.2,1.2), zonniger: zon 3.0
elev 42, exp 0.37). D2 r4 = NIEUWE FIETSEN (Beike: "niet de goede
fietsen en ze staan scheef"): BK-zoekrun `_bk_fietsen.py` (veel ruis:
schepen/containers/broeken) → Vintage_Bicycle___Old_City_Style
(opafiets) + Pink_city_bicycle_clean (mand+drager; _clean_pink.py
stripte 2x2x2 Icosphere-dummy + schaduwvlak — bbox was vervuild,
zmin -1.0). Beide RECHT geparkeerd langs de achterwand, weerszijden
van de middenpaal (x=2.16): vintage (1.2,2.1) rot 90, pink (3.0,2.05)
rot -90. RONDE 2 (8 jul ~17:00, "staat er"): alleen BO2 + J2 nieuw —
BO2 r3: plantenbak kwartslag (rot_z 90). J2 r3 = PIVOT (Beike: "zou
het lukken om hier gewoon alleen een hottub in te zetten?"): betonbank/
boomkuip/waterelement eruit, de bewezen DIY-hottub uit concept B als
enige prop op (1.5,1.7) — via `import scene_b_spa as sb; sb.hottub()`.
D2/E2/M2-notities in de JSON waren oude state (ronde 1, al verwerkt).
RONDE 3 (8 jul ~17:20, druppelde in 4 saves binnen — altijd herlezen
vóór renderen): BO2 "haal de gieter weg, maak het ook iets meer
goldenhour" (gieter eruit; zon 2.8 elev 25 kleur 1.0/0.80/0.55, fills
warm) · J2 "iets van licht in de overkapping + golden hour" (LED-lijn
onder dakrand via sb.emissie_mat + Fill_LED 16 + lantaarn glow 5 bij
de tub; zon 2.6 elev 20 warm, str 0.9) · M2 "verander de zon zodat
het wat vrolijker lijkt" (qwantani_dusk → venice_sunset_4k.exr str
1.0, zon 2.0 elev 14 — B-bewezen warme avondlucht). Alle 3 QC ✓
(J2: LED-lijn + lange gouden schaduwen; M2: venice-avondrood,
vrolijk; BO2: gieter weg, warmer). FINALS-AKKOORD 8 jul ~17:00
(Beike: "oke ze zijn allemaal klaar voor finale render") →
`finals2_run.ps1` KLAAR (17:13): E2 3.9min / J2 1.7 / M2 2.0 /
BO2 6.2 / D2 2.2, alle 5 QC ✓ in renders\finals\ — **de set van 14
finals is compleet** (A,B,C,D2,E2,F,G,H,I,J2,M2,BO2,P + D vervallen).
Avond 8 jul: pilots-review geschreven voor maakdag 9 jul —
`docs/REVIEW_pilots_R4_voor_9jul.md` + 2 nieuwe pilotplannen
(vijvertuin, kampvuur); zie HANDOFF_R4_progress.md.
D2-vloerlessen: pbr_from_folder leest alleen PH-naamgeving (klinkers =
paving_stones_64); wit muurtje linksboven lythwood = geaccepteerd (BO).
Review-site cachte oude thumbnails (gefixt: no-store + ?v=mtime).**
Status per concept (diags in `overkappingen-website\diag\`,
klaar voor review op localhost:8766):

| Concept | Stand | Bijzonderheden / open punten voor Beike |
|---|---|---|
| G carport (1000x400) | **stap 2 klaar (r6, feedback verwerkt)** | Beike: bak-in-paal → x 5.40; "fiets random + rare boog" → kruiwagen; "stoelen raar" → teak-set uit C. Drapeer-doek-mysterie: `garden_tools.fbx` = alleen reuze-planes → geschrapt |
| H bioscoop (700x400) | **stap 2 klaar (r8, ronde 5 verwerkt)** | r6/r7: 3 witte Pouf-krukjes weg (children-bug zoals F); r8 (Beike: "tussen het doek en de bank in"): banktafel naar (5.2,2.05) — Outdoor_Sofa kijkt bij rot 90 naar +x/het doek (register klopte, mijn aanname niet) |
| F vuurtafel (600x300) | **stap 2 klaar (r6, ronde 3 verwerkt)** | r5: ottoman + plaid-stapel weg; r6 (Beike): wit krukje 180° gedraaid — bleek Pouf.fbx-stoeltje; wit was óók een bug (override liep over children i.p.v. children_recursive) |
| A avonddiner (500x300) | **stap 2 klaar (r3, feedback verwerkt)** | Beike: stoelen om (painted front=−y, register!) + kast naar binnen (x 1.2) + diya-lamp/mand tegen "standaard"-gevoel. Buffet-look blijft smaakpunt |
| I riviera (400x300) | **stap 2 klaar (r10, ronde 5 verwerkt)** | r9: parasol op de patio (mast 5.3,0.6; doekcentrum 3.7,-1.0) + 2 zonnebedjes in de schaduw; r10 (Beike): bedjes kwartslag naar rechts — hoofdleuningen richting de parasol, onder elkaar op (3.3,-0.9)/(3.5,-1.9) |
| E cottage (300x300) | **stap 2 klaar (r3)** | er lifte een 1000W-studiolamp mee uit een PH-4k-blend (nu overal gestript); bank-front-fix; hortensia's zichtbaar (GLB bevatte 2 planten 18 m uit elkaar → st.hortensia-helper); IvyGen gaf niets bruikbaars — paal blijft kaal |
| BO boerenerf (KDI 600x300) | **stap 2 klaar (r6, ronde 5 verwerkt)** | r5: wandbankje weg; r6 (Beike: "piknikbank kwartslag draaien, niks in de weg"): tafel rot 98 op (2.0,1.35) — banken vrij van achterwand/vat/middenpaal, schaal+mand mee op het blad |
| P poolhouse (KDI 600x420) | **stap 2 klaar (r8, ronde 5 verwerkt)** | r6: ferns in de bakken, ligbedden +0.45 y, salontafel rot_z=0.0; r7: parasol x +0.7 + handdoek naast het bed; r8 (Beike: "zweeft nog ~5 cm"): rol-origin ligt in het midden → z TZ+0.02, ligt nu op de tegels |
| D tuinkamer (KDI 420x300) | **stap 2 klaar (r4, ronde 2+3 verwerkt)** | r3: schoren `pole-1-scaffold-e/w` op naam gefilterd + monstera naar (3.15,1.55) vrij van de pui. r4 (Beike: "tafel moet recht ervoor"): salontafel rot_z=0.0 — zonder rot_z geeft place_cluster een RANDOM rotatie (register-les!) |
| M moestuin (KDI 360x300) | **stap 2 klaar (r3, ronde 2 verwerkt)** | Beike: "geclusterd, ik heb niet door wat het is" → wandrek (SM_Storage, overlapte het tafeluiteinde) weg, krukje van (2.5,1.9) naar (2.75,2.30) vrij aan de achterwand, 2 terracotta grondpotten erbij; lijn ton→tafel→kruk→potten→gieter leest nu per prop |
| J japandi (KDI 300x300) | **stap 2 klaar (r5)** | fotoscans = 2× GPU-OOM → DIY-platen; r3 platen om wereldoorsprong geroteerd (add_box-origin-les); lege pot bleek max_w=4.0-filter (tree_small is 4.3 m breed); vlakke plaat rechtsonder zit al in het goedgekeurde anker |

**Review-server heringedeeld (Beikes verzoek 8 jul):** sectie ① = alle stap 2's
(de review-rij), ② ankers, ③ finals, ④ archief. Filter "Nog te beoordelen"
toont alleen open beelden. Server herstart met de nieuwe indeling.

**Nieuwe register-lessen vannacht** (allemaal in OPUS_WERKWIJZE §8): garden_tools-planes,
SM_Storage-rotatie, add_box=massief (badwater!), grondplaat vs verzonken bakken,
badwater-spec-cheat, painted_wooden_bench front=+y, parasol-pivot, witte FBX-props
(gieter), moss/min_h-filter, IvyGen-camelCase, Outdoor_Sofa-werkt.

**Geen finals, geen commits — alles wacht op Beikes review.** Telegram-updates verstuurd.

## ⭐⭐⭐ OVERDRACHT FABLE → OPUS (7 jul avond) — BEGIN HIER

Beike werkt vanaf 8 jul met Opus. Alles wat nodig is ligt klaar:

1. **Lees eerst `overkappingen-website\OPUS_WERKWIJZE.md`** — het complete recept:
   harde regels, bouw-cyclus, QC-protocol (crop + bbox-probe vóór tonen),
   licht/vloer/camera-presets, asset-inventaris, kijkrichtingen-register,
   Telegram-contact (via `notify.ps1`), en het recept om zelf nieuwe plannen
   te schrijven (`PLAN_TEMPLATE.md`).
2. **13 plannen klaar** (elk een bijna-tekening; status-tabel in OPUS_WERKWIJZE §10):
   C=final ✓ · B=stap 1 klaar/wacht op Beike · G/H/F/A/E/I (Douglas) en
   Japandi/Moestuin/D-tuinkamer/Boerenerf/Poolhouse (KDI) = ter uitvoering.
   KDI 1200x420 = klaar (familietuin), geen nieuw plan.
3. **Werkvolgorde**: **✅ Finals klaar: C (1200x400), B (840x400, spa), KDI-familietuin
   (1200x420).** **✅ ALLE 11 ANKERS GEBOUWD & DOOR BEIKE GROENGELICHT (7 jul avond,
   review_keuzes.json — alles "houden").** Eén notitie: **concept D (KDI 420x300):
   "Paal in het midden mag weg"** → in stap 2 middenpaal verwijderen (expliciete
   product-afwijking op Beikes verzoek, zie PLAN_concept_D). Anker-scripts:
   `scene_[g|h|f|a|i|e|bo|p|d|m|j]_*.py` — elk met stap1 (anker, klaar) en stap2
   (stub, te bouwen). **NACHT-/VERVOLGFASE: per anker stap 2 bouwen — één per keer,
   crop-QC vóór opslaan, volgorde G → H → F → A → I → E → BO → P → D(paal!) → M → J;
   resultaat per scène op de review-server laten staan voor de ochtend-review.**
   Laatste anker-herstel (P-terras-gat rond het bad, M-race-herstel, BO/D extra
   HDRI-blockers, J-stapstenenlijn) gerenderd in de slotbatch van 7 jul laat.
   → daarna per plan: probe → anker-diag → tonen → zones-diag → tonen →
   catalogus-shot → final na akkoord. Eén scène per keer, buren in de grid
   altijd een andere sfeer/tijd-van-dag.
4. **Memory is bijgewerkt** (map `~\.claude\projects\D--Blender-blokhutten\memory\`)
   — de feedback-lessen daar zijn hard verdiend; punt 7 (kijkrichtingen) en
   punt 8 (crop-QC + bbox-probe) zijn verplicht vóór elk tonen.
5. Open punten: Gscatter/Graswald wacht op hun server (503, zie OPUS_WERKWIJZE §6);
   gasvuurtafel-prop = wishlist (plan F heeft het beslispunt); kruiden-FBX te oud.

---

## ⭐⭐ HARDE RESET (4 jul avond) — één scène per keer, huidige stand

Beike keurde de complete batch (37 finals) af: voelde als "maar wat gedaan", regels/voorkeuren kwijt. Nieuwe werkwijze (zie memory `feedback-overkapping-reset-werkwijze`): **één overkapping per keer, plan eerst → Beike-akkoord → bouwen → tonen.** Afgekeurd werk gearchiveerd in `renders/_oud_v4_afgekeurd/` (37) + `diag/_oud_v4/` (28) — niks weggegooid. Review-tool voor Beike: `review_server.py` → **localhost:8766** (keuzes → `review_keuzes.json`).

**⭐ 7 jul — feedback op Douglas 1200x400-diag: "zelfde scène in ander formaat".** Beike wil per maat een eigen concept; meer tijd nemen, online research, tools/assets installeren mag, opties voorleggen → hij kiest. Uitgevoerd: 3 research-agents (concurrenten/trends, assets, tools) + eigen downloads ontgrendeld (7-Zip nu geïnstalleerd; portable fallback in `tools/7z/`; parasol/plaid+kussens/gazon/tropische bloemen uitgepakt — kruiden-FBX blijft te oud). Resultaat: **9 concepten (A–I) ter keuze** in vault `wiki/projects/Overkapping Scene Concepten 2026.md` + visueel keuzebord repo-root **`_concept_keuzebord.html`** (klik-en-kopieer). Marktgat bevestigd: geen NL-concurrent staged de grote maten met leefzones. Beste vondsten: Globe String Lights (BK GN), Antigua-eettafelserie, wisteria/klimroos, daybed, pampas, rattan-kleed; gaten die geld kosten: kamado $15, hottub $10-40 (of DIY douglas-tub). Tools-menu: Gscatter+Graswald 145 soorten gratis · IvyGen/Nishita zit al in 4.1 (headless getest) · Photographer 5 $25 · Real-ESRGAN gratis · BagaPie = 4.2+ (later). **Wacht op Beikes concept-keuze + install-akkoord; daarna assets ophalen → bouwplan → diag → final.**

**⭐ 7 jul middag — Beike koos B+C+D+F+G (B en C voorop); gratis tools akkoord; CC-BY akkoord (credit-lijst = `assets/CREDITS.md`).** Uitgevoerd: 20 BlenderKit-assets binnen via `_bk_concepts.py` (daybed, ligbedden ×3, fake-caustics-water, inbouwgrill, pizza-oven, Antigua-tafel + teakstoel, festoen-GN, rattan-kleed, pampas ×2, vloerlamp, cargo bike, kruidenpotten ×2, corten ×2 — "gas fire table" = 0 hits, op vraaglijst; 2 junk-hits opgeruimd). Sketchfab CC-BY via Chrome-extensie: outdoor-kitchen-scan 8k (62 MB) + rolled towel 4k → `assets/sketchfab/` (GLB-header gevalideerd; Chrome's opslaan-als-dialoog blokkeerde het net-afronden → bytes uit .tmp gekopieerd, dialogen kunnen bij Beike open staan). **Bouwplannen ter akkoord:** `PLAN_concept_C_1200x400.md` (leefwerelden-hero, eerst) en `PLAN_concept_B_840x400.md` (spa met DIY douglas-hottub). Maat-toewijzing-voorstel: C→1200x400, B→840x400, G→1000x400, F→600x300, D→KDI 600x300. **Gscatter/Graswald:** Beike is ingelogd (Google-account) en de flow werkt, maar `asset-downloads.gscatter.com` geeft 503 op add-on én asset-packs (7 jul ~10:45) — server aan hun kant plat. Juiste versie voor onze 4.1 = **Gscatter 0.11.9 (Blender 3.5–4.5)** op store.gscatter.com/account/gscatter. Later opnieuw proberen; fallback: BD3D Plant Library via Superhive. Volgende stap na plan-akkoord: `scene_c_leefwerelden.py` stap 1 (kaal+tuinanker) → diag op localhost:8766.

**⭐ 7 jul namiddag — plannen akkoord; concept C stap 1 gebouwd** (`scene_c_leefwerelden.py`, 3 zelf-QC-rondes): r1 Porcelain002 las als glanzend roze gietvlak → r2 `large_square_pattern_01` (grootformaat tegel mét voegen, greige) + zon opzij (elev 20/azim 282, lange paalschaduwen) + fills getemperd (9/10W) + 4e haagblok rechts + 2 coulisse-bomen → r3 HDRI-rot terug naar 245 (sky-glow links = zelfde kant als schaduwen; les: HDRI-rot en zonlamp-azimut apart tunen). Diag: `diag/conceptC-douglas-1200x400-stap1.png` — door Beike goedgekeurd ("anker ziet er goed uit"). Pampas-GLB's renderen goed. Review-server draait (achtergrond-shell).

**⭐ 7 jul avond — stap 2 (zones) gebouwd, 2 QC-rondes:** r1: Cozy_Outdoor_Lounge_Set = magere ligstoel (junk-hit uit parasol-map), keuken-fotoscan = donkere rotsmassa mét meegebakken kei (scan-terrein), Stone_Fire_Pit op Z-schaal = rotspartij. → r2-fixes: lounge = **Eichholtz Cap-Antibes-sofa** (rot 0 = rug naar achterwand, klopt) op rattan-kleed + salontafel + kussens + Beikes plaid (uitgepakt naar `assets/props-beike/blanket-and-pillows/uitgepakt/`); **buitenkeuken = DIY-blok** (douglas-front producttexture + betonblad TZ+0.88/0.93) met BK-inbouwgrill verzonken (rot −90, by_dim X) + kruiden + schaal op blad — de CC-BY-scan vervalt voor dit concept (credit kan uit CREDITS.md als hij nergens anders gebruikt wordt); vuurschaal by_dim='X' h=1.6. Eettafel-zone stond in r1 meteen goed (Antigua + 6 teakstoelen rot 0/180 kloppen native). Diag getoond → **Beike: "stoelen verkeerd om, hottub (=grill/keukenblok) half in de muur — zoek echt even de fouten op."** r3-foutenjacht met PIL-zone-crops + bbox-probe (`_probe_c2.py`): zijwand-plankzone begint al op x=10.69 (blok stond erin) → blok naar x 9.85..10.60 met zelfcorrigerende grill-plaatsing (bbox meten → centreren/verzinken, dekseltop TZ+1.13); teakstoel-front = +y bij rot 0 → rijen geruild; kussens stonden op de GROND (sp.ph grondt op vloer-z) → root.z=TZ+0.34; plaid was 1,55 m breed (fbx_prop schaalt op hoogte; h 0.40→0.22) én spierwit (FBX-textuur mist) → terracotta-override MAT_Plaid; Stone_Fire_Pit verwijderd (2 clusters vallen bij schaling uit elkaar — nette gasvuurtafel blijft wishlist). Crop-QC r3: alle 3 zones schoon. **Werkwijze-les vastgelegd in memory (punt 8): crops op ware grootte + bbox-probe vóór elke preview.** r4 (Beike): keuken naar de ACHTERWAND (front naar camera, vult rechterhelft) — achterpalen staan op x 0.31/4.12/7.93/11.75 (níét de voorpaal-posities!), echte zijwand-binnenkant = x≈11.71 (eerdere 10.69-meting was vervuild door achterwand-stijlen); blok x 8.60-11.00 in het vak tussen achterpalen, y tot 3.64 (stijlen vanaf 3.713); grill rot 180 = front/knoppen naar camera ✓. r5 (Beike, foto-crop: "grill nog niet goed geplaatst"): grill-unit is 0.88 diep vs blok 0.65 → vuurkast stak door het front; blok naar 0.94 diep (KY0 2.70) + grill RUG-uitgelijnd op y-center 3.16 i.p.v. bbox-gecentreerd. Grill-zoom r5 schoon. r6 (Beike): grill stond met zijkant tegen de muur — Char-Broil-front (acendedores-paneel) = +x native → rot 270, brede kant (0.88) langs de wand, blok terug naar 0.84 diep; kijkrichting in memory. r7 (Beike bij final-akkoord): losse kussens + plaid van de bank (Eichholtz heeft native kussens).

**✅ FINAL KLAAR (7 jul avond): `renders/stap4-douglas-1200x400-conceptC.png`** (2560×1920/512, AgX MHC, 25,6 MB) — tweede goedgekeurde hero van de nieuwe werkwijze, eerste uit het concept-keuzebord. Vooruit-plannen klaar: `PLAN_concept_G_1000x400.md` (carport-combi, ochtend na regen) + `PLAN_concept_F_600x300.md` (vuurtafel/hygge, incl. vuur-prop-beslispunt). **Concept B (spa, 840×400) in aanbouw**: `scene_b_spa.py` geschreven (DIY douglas-hottub met producttexture + RVS-banden + fake-caustics-water + stoomvolume, daybed/ligbedden/handdoek-scan, LED-emissielijn + lantaarn-glow tegen kiara_9-schemer); stap 1-diag draait. Geen commits.

**Actueel: 1200x420 KDI webshop-hero** in `overkappingen-website/scene_stap.py` (run: `blender 4.1 -b --python scene_stap.py -- 1200 420 kdi diag 3`).
- Plan: `PLAN_scene_1200x420.md` (v1 familietuin akkoord → afgekeurd na preview → V2 omgevings-HDRI-concept).
- Iteraties: v1 puresky leeg → v2 eilenriede (herfst) → v3 whipple (vlak) → **v3/v4 symmetrical_garden_4k** (zonnig, rot 210) + sun 4.0/elev 48/azim 215. Beike 2×: "andere omgeving, realistischer licht, rechterkant leeg, gazon staat bijna niks" → v4: perk-eilanden (perk()-helper: aarde-disc maskeert gras-raycast) links + rechts-voor, tuinboom island_tree_02 (W+4.3, 1.0), CRAIG rotan-hoek rechts onder kap, gieter, voorgrond-bloemenborder, wooden_bowl op tafel (kruiden-FBX = versie 6100, onbruikbaar).
- **v4 afgekeurd via grondige zelf-review** (op Beikes verzoek): binnenmeubels buiten, tuin zonder ontwerp, KDI wast wit uit, geen slagschaduw, statische compositie. Checklist nu in memory (`feedback-scene-verankering-lessen`).
- **v5/v5b gebouwd (akkoord Beike op het v5-plan)**: outdoor-familes (2× CRAIG rotan in L + kussens, houten tafel zonder geruit kleed + 6 painted-wood tuinstoelen, hangstoel + bijzet + pot), tuinontwerp (tegelpad x 6.8–8.2 met banden + aarderanden, erfgrens-hagen achter/links met eigen procedureel MAT_Haag — BK-haag-GLB's komen textuurloos binnen, borders met betonrand + donkere aarde in 2 rijen, planter boxes op de terrasrand), island_tree_01 (BK-berken renderen als wit spookskelet), zon elev 33/azim 238 (zichtbare slagschaduw), camera 0.85·diag+1.8 met f/2.8, gemaaid gazon (grass_lib `h_mul=0.7`) op donkere grond, KDI-tint-correctie (HSV-nudge op GLB_*_kdi na replace_materials).
- **v5b door Beike goedgekeurd ná eigen orientatie-fix in Blender** (15:47): hij draaide de twee CRAIG-banken zelf goed (hoofdbank 180°→356°, L-bank +90°→−93°; CRAIG native front = -y). Rotaties uit zijn blend geprobed en in `scene_stap.py` teruggevoerd + les in memory-checklist (punt 7: kijkrichting-check).
- **✅ FINAL KLAAR (4 jul ~16:00)**: `renders/stap3-kdi-1200x420.png` (2560×1920/512, rechtstreeks uit Beikes bewerkte blend — eerste goedgekeurde hero van de nieuwe werkwijze).
- **Douglas 1200x400 diag klaar** (zelfde keten): `diag/stap3-douglas-1200x400.png` — v5b-formule incl. Beikes bank-rotaties, douglas leest warm vs. KDI. Wacht op Beikes oordeel → dan final.
- Resterende nits v5b (gemeld): pad leest subtiel (rechts in beeld), kleed vrij licht, rechter vak voorste helft bewust open.
- Beikes eigen downloads staan veilig in `assets/props-beike/downloads-4jul/` (RAR's niet uitpakbaar — geen 7-Zip; kruiden-FBX te oud; rest bruikbaar op afroep).

Daarna: één voor één de overige maten/scènes, telkens plan → akkoord → bouwen. **Geen commits zonder akkoord.**

---

## ⭐ [GEARCHIVEERD na reset] KLAAR VOOR REVIEW (4 jul middag) — galerij: `_overkapping_review.html`

1. **Webshop-serie (15 finals)** in `overkappingen-website/renders/` op de complete tekentool-GLB's, incl. herstelde kdi-360x300 (oriëntatie-fix) en avond-hero.
2. **Hero-checks scene-playbook (22 finals)**: alle 10 sferen + catalogus, elk in KDI én Douglas — de playbook-gate vóór de lifestyle-batch. Naming `outback-<hout>-<maat>-<scene>.png`.
3. Scene-verbeterloop gedocumenteerd in `overkappingen-website/PLAN_scene_verbetering.md` (3 diag-rondes met reviews).
4. Vraaglijst assets (niet op BlenderKit free): parasol, Japanse esdoorn (acer), bamboe-scherm, wollen plaid, mooie losse hortensia.
5. Openstaand: 360x300-GLB her-export zodra de tekentool-3D het weer doet (zie ronde-4-notitie); tot dan vaste 180°-fallback in de pipeline.

**Geen commits gedaan.** Na akkoord per scène: lifestyle-batch volgens de toewijzingsmatrix (playbook §4).

Plan: vault `wiki/projects/Overkapping Website Renders Plan.md` (beslissingen daar afgevinkt).
Opdracht: website-renders Outback overkappingen, KDI + Douglas, achterwand + 1 zijwand.

## Beslissingen (Beike, 2 jul avond)

- **Maten (representatieve set):**
  - Douglas: 300x300, 400x300, 500x300, 600x300, 700x400, 850x400, 1000x400, 1200x400
  - KDI: 300x300, 360x300, 420x300, 600x300, 600x420, 1200x420
- **Bouw:** plat dak + EPDM + boeideel, rabat-wanden, zijwand rechts vanaf camera, palen 12×12, wand buitenkant palen. Middenpalen: >5500mm +1, >6500 +2, >9700 +3.
- **Output:** basis-serie 2560×1920 tuinscène; creatieve accenten mogen ("wat origineels").
- **Autonomie:** volledige batch vannacht, zelf-QC i.p.v. hero-gate, review 's ochtends. **Geen git-commits.**

## Werkmap

- Builder/scene-scripts: `overkappingen-website/`
- Renders: `overkappingen-website/renders/`
- Naming: `outback-<kdi|douglas>-<breedte>x<diepte>-aw-zw.png`

## Status

- [x] Builder-script v1 (`overkapping_builder.py`) — frame/wanden/dak/schoren OK op eerste diag; fixes: wand-paneel rabat i.p.v. donker basis-paneel, fix_broken_image_materials (magenta planten), gras 560, terras minder rood
- [x] Materialen KDI/Douglas — beide op echte 8K producttextures; KDI leest lichter/grijziger, Douglas warm; macro zone-noise toegevoegd
- [x] Paal-telling gevalideerd: 1200 breed = 5-portaal (3 middenpalen) conform tekentool-regel
- [x] Scene-template + props v3 — camera/terras/gras schalen met maat; brede maten krijgen bank + extra plant + vuurschaal; avond-heromodus (`mode=avond`) met festoen + dusk-HDRI toegevoegd
- [x] Validatie-diags: 1200 v3 ✓ (gras tot camera), KDI 600x300 ✓ (3-portaal klopt)
- [x] Hero-check + zelf-QC gedaan op 4 maten (paal-telling, wand buitenkant, geen z-fighting, binnen donkerder dan buiten, AgX MHC)
- [x] **BATCH KLAAR 17:56** — alle 14 finals, exit=0, 23–25 MB/stuk in `renders/`; QC-spotcheck grootste maat (KDI 1200x420) OK
- [x] Extra concepten gebouwd en gevalideerd op diag: carport (sedan native schaal, WGT-rig-junk gefilterd), lounge (sofa-set gesplitst: 2-zits + salontafel; pouf 0.001-groepschaal gebakken), tuinwerk (brandhoutwal met Timber-textures; tools-pack = fotovlakken → vervallen; EV-lader multi-variant-mesh → vervallen)
- [x] Finale renders concepten (carport/lounge/tuinwerk) + avond-hero — klaar
- [x] Review-galerij: **`_overkapping_review.html`** in de repo-root (25 beelden: 18 finals + 7 diags)

## KLAAR VOOR REVIEW (3 jul ochtend)

**Webshop-serie:** 14 finals in `overkappingen-website/renders/` — 8 Douglas + 6 KDI, 2560×1920, 512 samples, AgX Medium High Contrast, naming `outback-<hout>-<b>x<d>-aw-zw.png`.

**Extra's (pitch — zie `overkappingen-website/PITCH_extra_scenes.md`):**
- `concept-carport-kdi-600x300.png` — sedan + fietsenrek + oprit
- `concept-lounge-douglas-500x300.png` — hangstoel + sofa-set + karpet + festoen
- `concept-tuinwerk-douglas-300x300.png` — brandhoutwal + kruiwagen + gieter/laarzen
- `outback-douglas-600x300-aw-zw-avond.png` — schemering + lichtsnoer

**Reproduceren:** elke maat = `blender 4.1 -b --python overkapping_builder.py -- <kdi|douglas> <b> <d> final`; concepten via `extra_scenes.py -- <concept> final`; batch via `run_batch.ps1`. Alle .blends staan in `overkappingen-website/scenes/`.

**Bekende nitpicks voor evt. ronde 2:** zand-band aan de horizon bij brede maten (grond-texture op afstand), fietsenrek leest licht, boeideel-hoekverstek is recht (geen 45°-verstek). **Geen commits gedaan.**

## RONDE 4 — STAND 4 jul middag

- **Webshop-serie compleet her-renderd op de goede GLB's** (15 finals in `renders/`; douglas-1200x400 crashte eerst op geheugen naast de asset-downloads — solo-retry OK).
- **360x300-GLB heeft de zijwand aan de verkeerde kant getekend** (webshop-final toonde eerst de dichte hoek). Her-export geprobeerd (3 verse sessies + vers tabblad): de tekentool bouwt vandaag de 3D-scene niet meer op (wanden verschijnen niet in de 3D-view/mini-preview; gisteren werkte dezelfde flow — vraag voor Beike, mogelijk tijdelijke tool-bug). **Interim-fix:** vaste 180°-fallback-rotatie voor (360,300) in `glb_scene_builder.import_product` — visueel geverifieerd correct (open hoek voor, aw achter, zw rechts); de wall_state-checker is voor deze ene export onbetrouwbaar (losse wall-skeleton-roots bucketten verkeerd). Webshop-final 360x300 opnieuw gerenderd met de fix. Zodra de tekentool-3D het weer doet alsnog netjes her-exporteren.
- **Scene-verbeterloop afgerond** (3 diag-rondes, zie `PLAN_scene_verbetering.md`): alle 11 scènes akkoord. **Hero-checks draaien** (11 scènes × KDI + Douglas op final-kwaliteit) → galerij → Beike-review. Lifestyle-batch pas na akkoord. Geen commits.

## RONDE 4 (3 jul avond): scene-playbook uit de vault in uitvoering

Beike's "Overkapping Scene Differentiation Playbook" (vault; PC-kopie `iCloudDrive\Desktop\overkapping-scene-playbook-PC.md`) is nu leidend: per SKU 1 neutrale catalogus-shot + 1 lifestyle-shot uit 10 sferen (toewijzingsmatrix §4).

- **`scene_playbook.py`** — alle 10 sferen + catalogus als scene-functies bovenop de GLB-productpipeline (glb_scene_builder.import_product + replace_materials). Helpers: acg_mat (ambientCG-PBR), build_floor/rand_strook, backdrop_wall, water_plane (poolhouse), mist_volume (scandi), carpet, bk (BlenderKit-GLB-props). Run: `blender 4.1 -b --python scene_playbook.py -- <b> <d> <hout> <scene> diag|final`.
- **Assets binnengehaald (3 jul):** 45 BlenderKit-modellen (`assets/blenderkit/INDEX_wishlist.txt`, licentie per asset geregistreerd; alles cc_zero/royalty_free) — o.a. olijfboom, berk, hortensia, monstera, strelitzia, lavendel, hangstoel, rotan/moderne loungesets, vuurschalen, zwembaden, stapstenen, hagen, betonbanken + Cozy Outdoor Lounge Set. 12 ambientCG-materialen (travertijn, baksteen, corten, porcelain, bamboe, wicker). PolyHaven-aanvulling (43 modellen + 16 vloertexturen + 8 playbook-HDRI's) — draait op moment van schrijven.
- **Niet gevonden op BlenderKit free (vraaglijst Beike):** parasol, Japanse esdoorn (acer), bamboe-scherm, wollen plaid, outdoor vloerkleed als model (opgelost met plane + Carpet016-textuur).
- **Volgende stap (gate):** per gebruikte scène 1 KDI + 1 Douglas hero-check → eerst aan Beike laten zien, dan pas lifestyle-batch (playbook §8.4). Geen commits.

## RONDE 3 — STAND 3 jul namiddag: GLB-set COMPLEET, herbatch loopt

- **Alle 12 unieke maten als complete GLB binnen** in `overkappingen-website/glb/` (300x300 … 1200x400 én 1200x420; 850 werd 840 door de 100mm-snap — echte SKU). De laatste twee (1200x420, 1200x400) op 3 jul via verse tekentool-sessies geëxporteerd: resize met JS-smoothDrag op de wandlijn (native drag verplaatst het plan i.p.v. resizen), wanden met smoothDrag door beide hoekpalen, wandtotaal-teller als check (11,58 + zijwand), 3D-view-verify vóór export.
- **Valkuil bevestigd:** na één export-cyclus is de 3D-rebuild van de tool kapot (skelet in de lucht) → per maat een verse pagina-sessie.
- **Pipeline-fix (belangrijk):** nieuwere tekentool-exports zetten de wand-skeletons (mét alle rabat-planken) en 2 schoren als EXTRA scene-roots naast `shed`. `glb_scene_builder.import_product` bundelt nu alle top-level objecten onder een eigen `glb_root` vóór scale/rotatie — anders blijft de wand op cm-schaal en ontbreekt het product in de render. Alleen de allereerste export (300x300, 88 MB) had alles onder `shed`.
- **KDI-fix:** catch-all in `replace_materials` — resterende `basetexture`/`firstLayer`-materialen (wand-stijlen) → frame-materiaal; geen oranje stijlen meer (diag KDI 1200x420 ✓).
- `run_batch_glb.ps1`: 850→840. Oude renders → `renders/_oud_v3_glb-incompleet/`. **Herbatch (14 finals + avond-hero) gestart** → log `logs/batch_glb_master2.log`.

## RONDE 3 (3 jul): ECHTE tekentool-GLB's als productbron

Beike: gebruik de tekentool-GLB's. Uitgevoerd via Chrome-automatisering van tekentool-v2 (Outback Douglas-template, maat per maat geresized met wand-meegroei, "Meer informatie… → Exporteer GLB"):
- **12 GLB's** in `overkappingen-website/glb/` — alle unieke maten (300x300 … 1200x420), mét achterwand + rechter zijwand, ~88 MB/stuk.
- GLB-inhoud = de echte constructie tot op de plank: palen 15×15×231, liggers 5×15, wallBeams, dakbeschot + EPDM-pakket + boeidelen + **alu daktrim (chrome-mat)**, schoren (`scaffold`), wanden als losse rabat-planken 2,2×14,5 cm werkend ~13,9. Wandhoogte 2310 / nok 2525 (tool-waarheid).
- Materialen heten `basetexture-firstLayer-<onderdeel>` → vervanging per naam (zelfde patroon als cabins/kapschuur).
- Nieuwe pipeline: `glb_scene_builder.py` (GLB 1:1 + producttextures + bestaande scene-template). Parametrische builder v2 blijft als fallback/referentie.
- Wanden in de tekentool tekenen lukte niet via automatisering (bug in de tool, na refresh door Beike handmatig gedaan; groeien daarna mee met resizen).
- Pipeline-validatie: oriëntatie-zoeker (wereld-matrix-rotatie; euler op de shed-root was fout door glTF X-rotatie), producttextures via UV-mapping van de GLB (BOX/object smeert op cm-schaal lokale assen). Diag douglas 300x300 = het echte product ✓.
- **GLB-serie-batch loopt** (14 maten + avond-hero) → `logs/batch_glb_master.log`. Oude parametrische renders in `renders/_oud_v2/`.
- **Beike (3 jul): scène-ideeën schrijft hij zelf uit → komen in de vault.** Concepten/pitch geparkeerd; focus = het product zelf goed in beeld (neutrale serie). Bij nieuwe scène-docs in de vault: GLB's + `glb_scene_builder.py` als basis gebruiken.

## RONDE 2 (3 jul): constructie-correctie naar echte Outback-bouw

Beike: "schoren en planken en alles kloppen niet". Referenties verzameld in `overkappingen-website/referentie/`:
- Pext montagehandleiding Douglas Duplo vrijstaand (PDF + pagina-PNG's): dwarsligger 120x120 OP de staanders, liggers 58x140 staand over de diepte, tussenbalkjes 60x120, middenbalkjes 60x60 bij uitval ≥360, schoren 58x140 plat tegen de zijkant, betonpoer + alu stelvoet, afschot-advies 5°.
- blokhutwinkel.nl Outback-specs: palen 14x14 verlijmd (240 cm), **buitenmaat = dakmaat**, fundament = buitenmaat − 40, overstek 21 rondom, wandhoogte 220 / nok 255 (klopt exact met opbouw nok − trim − beschot − ligger − dwarsligger = paaltop 2.218), boeidelen 28 mm + aluminium daktrim + EPDM + HWA, paal-schoor.

**Status ronde 2:** validatie-set v3 goedgekeurd (schoren-verstek ✓, plankmaten ✓, strepen-fix ✓, KDI/Douglas-onderscheid ✓, 5-portaal 1200 ✓). V1-renders gearchiveerd in `renders/_oud_v1/`. Herbatch v2 (14 maten + 3 concepten + avond) gestart — log `logs/batch_master2.log`.

Close-up-validatie (diag/det_*.png) leverde 3 extra fixes: schoren nu parallellogram-prisma's met verticale verstek-eindvlakken (i.p.v. haakse boxen die door de paal staken), texture projection-blend 0 op planken (regenboog-sliver op de buitengevel weg), hoek-/eindlatten op verticale-nerf-materiaal.

**Asset-sourcing vanaf nu (Beike, 3 jul):** BlenderKit toegevoegd — eerst daar zoeken, anders bij Beike aanvragen. Vraaglijstje na deze ronde: EV-laadpaal (carport), 2-3 gevarieerde tuinsets, moderne loungeset.

Builder v2 herbouwd op deze specs (afschot gekozen: 4% i.p.v. 5° — site-maten wandhoogte/nok zijn per diepte constant, dus strakke EPDM-look aangehouden; gedocumenteerde aanname). Wanden = losse rabat-planken (werkend 17,6 cm, 28 mm) buitenkant palen met kern-schaduwgroef, hoek-/eindlatten, afdek-wig op de zijwand. KDI = groen-grijs getinte douglas-nerf (rabat-fotopatroon gaf conflict op losse planken).
