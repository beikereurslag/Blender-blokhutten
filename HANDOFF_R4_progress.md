# HANDOFF — R4-ronde voortgang (2 jul 2026, ~15:45, na PC-herstart)

> **UPDATE 12 aug — VAKANTIERUN 44/44 GESLAAGD + DRIVE-EXPORTMAP:** de
> wachtrij liep foutloos af op 9 aug 11:06 (0× MIS; het 3:00-vangnet
> bevestigde daarna "niets te doen"). Totaal 51 clips + 44 renders =
> 3,0 GB. Voor Beike's Drive-upload: **`D:\Blokhutwinkel-visuals-2026-08\`**
> — genummerde categorie-mappen 01–05 (renders) + 06-filmpjes met
> submappen rondom-versies/ (7) en experimenten/ (4). ALLE_FINALS blijft
> de werk-master. Open: rondom- vs origineel-keuze per clip, camelia's
> B90-review, restore-point-commit (laatste commit nog 13 jul!).

> **UPDATE 6 aug — VAKANTIERUN: ALLES ALS FILMPJE (Beike 5 dagen weg,
> "laat alles renderen, je mag experimenteren"):** wachtrij van **37
> clips** als geplande taak `BlokhutVakantieClips` (+ dagelijks-3:00-
> vangnet; ONSTART-trigger vergt admin — commando aan Beike gegeven).
> Volledig hervatbaar: skip klare mp4's én klare shots; encode alleen na
> "SCENE KLAAR" in de log. Inhoud: 6 ronde-2-restanten + S1–S8 + 6
> stijlen (leeshoek/tuinkantoor/lavendelveld/avondkubus/ochtendnevel/
> zonnebloem-modern) + 13 webshop-concepten + **4 experimenten**
> (ochtendnevel-focuspull = rack-focus door de mist; goudenuur-zonsweep
> = zon zakt 12°→1.5° tijdens de shots; avondkubus-longform = 4-shot
> 16 s; tuinkantoor-ochtendpush = focus-pull + diepe push).
> `nachtclips_multishot.py` v2: dict-shots, focus_pull/zon-keyframes
> (render-only, blend NIET gesaved), webshop-scènes krijgen variatie uit
> een deterministische pool. BEWUST OVERGESLAGEN: camelia's (onbeoordeelde
> R5-staat in blend), lavendel_tuinfeest + roosmarijn_buitenbioscoop +
> roosmarijn_modern (blend↔final-mapping onzeker; alleen
> "roosmarijn_warm.blend" gevonden). Eerdere run-2-taak vervangen; de
> les "app-herstart doodt runners → schtasks" staat in memory.
> Telegram-notify per clip. Geen commits.

> **UPDATE 5 aug (ochtend) — NACHTRUN GESLAAGD: 7/8 clips klaar, #8
> rendert:** de wachtrij draaide ononderbroken door (ook door de
> Claude-sessieherstart heen — de PS-runner leeft los van de sessie).
> Klaar in `ALLE_FINALS/filmpjes/`: kapschuur-A-lounge (18:08) ·
> kapschuur-B-dining (21:06) · wellness-hottub (22:16) · buitenkeuken
> (23:19) · lavendel-buitenbioscoop (04:47 — blauw uur is ~5× zo traag
> door adaptive sampling!) · roosmarijn-schaakavond 1080p (08:14) ·
> lavendel-pluktuin (09:28). **Vuurtafel rendert nu, klaar ~12:30.**
> Spot-check-QC op wellness/keuken/kapschuur-frames: goed. Schaakavond-
> clip als voorbeeld naar Beike gestuurd. Frames blijven in
> `_diag/nachtclips/<naam>/` (her-encode mogelijk). Reviewsite-monitor
> opnieuw bewapend (oude stierf met de sessie); camelia's B90 nog steeds
> open. Geen commits.

> **UPDATE 4 aug (namiddag) — NACHTRUN FILMPJES GESTART (Beike: "wachtrij
> van 18+ uur, filmpjes van de finals die ik het mooist vond, laat lopen
> tot minimaal 9:00"):** wachtrij van 8 drieluik-clips op 1080p/48
> (~3–3,5 u/scène ≈ 25+ u totaal), volgorde = Beikes favorieten eerst:
> kapschuur-A-lounge → kapschuur-B-dining → wellness-hottub →
> buitenkeuken → B14 bioscoop → B13 schaakavond (bespoke shots) →
> lavendel-pluktuin (Beikes eigen edit) → vuurtafel. Generiek recept:
> `scripts/nachtclips_multishot.py` (dolly/zij-truck/crane rond de
> hero-cam, kijkdoel uit DOF; B13 = geprobde bespoke-shots). Runner
> wacht zelf tot de GPU vrij is; per scène frames → cv2-crossfade-encode
> → `ALLE_FINALS/filmpjes/<naam>.mp4` + Telegram-notify; fouten loggen
> en doorgaan. Status: scratchpad `nachtrun_status.txt`. De 720p-drieluik
> van B13 rendert nog af en gaat apart naar Beike. Geen commits.

> **UPDATE 4 aug (middag) — HELE B-REEKS GEACCEPTEERD → 6 FINALS IN
> ALLE_FINALS; eerste bewegende render in de maak:** Beike keurde B13-fix2
> goed ("dit is goed zo") en gaf opdracht de finals-map bij te werken.
> Alle 6 B-finals gerenderd (recept `pilots/_s1_final.py`: pack_all +
> 2560×1920/512/adaptive 0.008, 10:48–11:55, ~8–13 min/stuk) naar
> `ALLE_FINALS/blokhutten-tuinscenes/`: jasmijn_vinylmiddag,
> roosmarijn_uitslaapochtend, jasmijn_vlindertuin, roosmarijn_schaakavond,
> lavendel_buitenbioscoop, zonnebloem_zonnegroet. Visuele QC op 3 gedaan ✓.
> Camelia-R5's bewust NIET ververst (nog in review; oude goedgekeurde
> finals blijven staan). **NIEUW SPOOR — filmpjes:** Beike wil bewegende
> renders; akkoord op testclip B13 (dolly-in 0.75 m, 5 s/24 fps/720p/48
> samples). LES: **Blender 5.1 heeft de ingebouwde FFmpeg-video-uitvoer
> verwijderd** (`file_format='FFMPEG'` bestaat niet meer) → PNG-framereeks
> + cv2-encode (mp4v), scripts `schaakavond_dollyclip.py` +
> scratchpad `_encode_clip.py`. Testclip (`_diag/B13_dollyclip_test.mp4`)
> door Beike goedgekeurd ("mooie clip") → vervolg: **drieluik met meerdere
> hoeken van de veranda** (Beikes wens, "subtiel"): shot A hero-dolly,
> B zij-truck langs de open kap-kant, C lage close-in op het schaakvignet;
> 3×4 s met 0,5 s crossfades (~11 s totaal). Nieuwe hoeken eerst als
> probe-stills geQC'd (backdrop houdt stand, DOF scherp op het vignet) —
> volledige orbit kan NIET (scène is alleen aan de camerakant aangekleed).
> Scripts: `schaakavond_multiclip.py` (probe/full-modes) + scratchpad
> `_encode_multiclip.py` (crossfade-encoder). Geen commits.

> **UPDATE 4 aug (ronde 5) — B10/B11/B12 GEACCEPTEERD; B13 beenruimte-fix:**
> Beike zette na de ronde-4-fixes B10 vinylmiddag, B11 uitslaapochtend én
> B12 vlindertuin op **houden** (scorebord: 5 van 6 binnen — B10/B11/B12/
> B14/B15). **B13**: "nog verder. als je nu in de stoel zit heb je geen
> ruimte om je benen te laten" → oorzaak is de Horizon-salontafel die met
> zijn LANGE as (~1,2 m) tussen de stoelen ligt; verder schuiven kan niet
> (kapvloer-rand ~−3.1). Fix2: tafel 90° gedraaid (korte kant naar de
> stoelen, klassieke schaakopstelling), vignet-centrum naar x −1.38,
> stoelen op gemeten 0.32 m beenruimte, glazen opnieuw op het blad
> (`schaakavond_fix2.py`, diag `B13_stoelen_v2`). **KLAAR: crop-QC goed
> (stoel A rug op −2.93, beenruimte 0.32/0.32), preview op :8767 +
> Telegram met foto.** B90-camelia's: nog steeds geen nieuw oordeel
> (oude notities blijven staan).

> **UPDATE 4 aug — BEIKE TERUG VAN VAKANTIE; REVIEWRONDE 4 BINNEN, FIXES
> DRAAIEN:** Beike heeft de site opnieuw doorgelopen. Scorebord: **B14
> bioscoop + B15 zonnegroet = houden** ✅ · **B10** "stoelen staan niet de
> goede kant op" (fauteuil-rug stond naar de camera; rot 243→130, zitting
> naar camera-driekwart, `vinyl_fix1.py`) · **B11** "de handdoek bij de
> tafel moet weg" — bleek AL gefixt in de blend (v9, 17 jul 10:25); de site
> toonde nog de oudere v8-render → alleen verse preview · **B12** "de tuin
> zelf is te chaotisch" → de 3 losse BorderWild-bakken in het gras weg,
> vogelbad van los-in-het-gras naar het linkereinde van de border-rij,
> gras her-run (`vlindertuin_fix3.py`) · **B13** "stoelen mogen iets verder
> van de tafel af" → StoelA −2.42→−2.56, StoelB −0.82→−0.64
> (`schaakavond_fix1.py`). **KLAAR (10:18): alle 4 door eigen crop-QC en
> als preview op :8767 gezet + Telegram-notify.** QC-les B12: vogelbad
> eerst naar het border-rij-einde (−3.85,3.05) verplaatst, maar dat bleek
> precies de camera-zichtlijn naar het bank-vignet te blokkeren → fix4
> terug naar de bewezen plek (−3.50,3.55); alleen de wilde bakken weg is
> het juiste minimale verschil. B10-platenspeler heeft 3 missende
> metal-maps uit de BK-bron (cyrillisch C:-pad) — niet zichtbaar in de
> render, wel bekend punt vóór een final. **B90 camelia's
> (buitenbad/wijnterras R5): oude notities stonden nog in de velden, geen
> nieuw oordeel — meenemen in de volgende ronde.** Geen finals, geen
> commits. Wacht op Beikes herbeoordeling (monitor op de keuzes-file
> staat aan).

> **UPDATE 17 jul — SCOREBORD NA REVIEWRONDE 3: B12/B13/B14/B15
> GEACCEPTEERD** (Beike wiste de notities na de fixes) · **B11** wacht op
> herbeoordeling (rol ligt al bij de wandvoet, pantoffels weg — notitie
> staat mogelijk nog uit ronde 2) · **B10** open: "ander thema"-notitie
> gewist zonder keuze — vraag uitgezet (thema A/B/C of speelmiddag houden).
> Vraag-notify verstuurd; geen renders in de wacht. Finals/commits blijven
> wachten op expliciet akkoord.

> **UPDATE 17 jul — REVIEWRONDE 2 + TUINDECO-VERVOLGPROJECT KLAARGEZET:**
> ronde-2-notities verwerkt: B12 insectenhotel van de hut-gevel naar de
> kap-ACHTERWAND boven de bank ("hang hem op een muur in de overkapping") ·
> B11 pantoffel-blokjes weg + dekenrol naar de wandvoet naast de mand ·
> B13 dekenrol verwijderd. Previews ververst. Op Beikes verzoek:
> **GLB-Creator-werkwijze vastgelegd in Obsidian** (`wiki\projects\GLB
> Creator werkwijze (Tuindeco-producten).md`) en **startprompt voor de
> 2e sessie** geschreven: `PROMPT_nieuwe_sessie_tuindeco_finals.md`
> (finals inventariseren → Tuindeco-matches per thema → lijst ter akkoord →
> genereren → QC-pijplijn → vervangen → previews; finals nooit
> overschrijven, `_tuindeco`-suffix ernaast). Open: B10-themakeuze
> (A vinyl / B snijbloemen / C sterren) + oordeel B14/B15-fixes.

> **UPDATE 17 jul — REVIEWRONDE 1 VERWERKT (5/6):** Beikes zes notities via
> de reviewsite verwerkt: **B11** proc-blokken ("witte vierkanten") weg →
> echte fbx-kussens+dekenrol op gemeten maat op het ligvlak + lantaarn/boek/
> mand · **B12** insectenhotel van de kap-zijwand naar de hut-voorgevel
> (leesde als zwevend) + lage douglas-bank met saliekussen tegen de
> achterwand · **B13** Milano-front blijkt +X bij rot 0 (rotatie-probe!) →
> stoelen facen nu écht + dekenrol tegen de wandvoet · **B14** 2 poufs +
> dubbel vloerkussen (3 zitplekken op het doek gericht) · **B15** lantaarn/
> waterfles/handdoek/potplantje. Alle previews ververst na crop-QC.
> **B10 open**: concept afgekeurd ("dood, ander thema") — themakeuze bij
> Beike uitgezet: A vinyl-middag / B snijbloemen-werkbank / C sterrenavond.
> Nieuwe fbx-les: losse onderdelen uit blanket_pillows hebben wilde
> bron-schalen per object → altijd per item op doelmaat schalen + bbox-log.

> **UPDATE 17 jul (ochtend) — PLANKEN-NAFIX OP ALLE 6 (Beike: "deels gedaan,
> bv boven de opening — check alles heel goed"):** de 17 parentBoard-panelen
> per blend (o.a. de strook boven de kap-opening) stonden nog op DG_balk met
> BOX-mapping → nu eigen DG_paneel + plank-UV (`pilots/_fix_planken_alle.py`,
> met volledige onderdelen-inventaris per blend: 122 meshes / 12 groepen,
> geen onbekende). Lib bijgewerkt (TOEWIJZING: parentboard→paneel). Alle 6
> fase2-previews ververst met crop-QC op de paneel-stroken; oude fase1-
> ankers hernoemd naar *_ARCHIEF_oudeplanken.png (site toont nu per scène
> één actueel beeld). Wacht op Beikes review van de reeks.

> **UPDATE 17 jul (nacht) — ALLE 6 SCRATCH-SCÈNES OP DE SITE (wacht op
> Beikes ochtend-review):** na Beikes plank-fix ("horizontaal!") en
> anker-akkoord B10: hele reeks gebouwd via gedeelde lib
> `pilots/_stijlreeks_lib.py` (product-materialen whitelist + plank-UV,
> tuin-recept-omgeving, licht-momenten, veilige asset-import, raycast-
> helpers). Op :8767, elk fase1+fase2: **B10 Speelmiddag** (Jasmijn, middag)
> · **B11 Uitslaapochtend** (Roosmarijn, ochtend — ECHT product Teak
> Sunlounger Wembley via GLB Creator, 30 cr, lokaal op catalogusmaat
> 70×206×80) · **B12 Vlindertuin** (Jasmijn, namiddag — Birdbath 02,
> proc. insectenhotel; BK-"vlinder" was een beer → geschrapt) · **B13
> Schaakavond** (Roosmarijn, schemer — schaakset/fauteuils/lampjes in huis)
> · **B14 Buitenbioscoop** (Lavendel, blauw uur — gloeiend doek, BK-projector
> + popcorn) · **B15 Zonnegroet** (Zonnebloem, zonsopkomst — proc. yoga).
> Credits: 30 van ~2800. Nieuwe lessen in memory render-debug-recepten
> (add_box-origin-rotatie-val, BK-naamleugens, base-schema's per product).
> Blends per B-map + bouw/fix-scripts; diags in `_diag/B1*_*.png`.
> **Geen finals, geen commits** — wacht op review; F sauna blijft geparkeerd.

> **UPDATE 16 jul (laat) — B10 FASE 2 OP DE SITE (wacht op oordeel):** anker
> door Beike goedgekeurd minus speelhuis ("dat speeltuin mag weg, voor de
> rest is het anker goed") → speelhuis verwijderd + gras her-run (mask-gat
> vult zich). Dressing v9: vlaggetjeslijn (proc. bunting paal→naad),
> krijtbord+kindertekening op de y-achterwand ín de zonwig, saliegroene
> speelgoedkist, dekenrol+kussen (sketchfab-set, kleur geforceerd — bron
> rendert zalmroze), balletjes binnen/buiten. **BK-teddy geschrapt: "Teddy
> Bear" = houten deco-beer, geen pluche** (solo-rotatie-probe). Meetlessen:
> kap-voorgevel deels dicht + −X-wand dicht (alleen opening rechts-voor
> zichtbaar vanaf de driekwart-camera); achterwand-BINNENKANT op y −1.275
> (wand 17 cm dik!) — props op wandvlakken altijd eerst raycasten; "lijst"
> als dichte box verbergt het bord (bord moet ervóór uitsteken). Preview:
> `speelhuismiddag_fase2_PREVIEW.png` + Telegram (incl. tipi-vraag). Bij
> akkoord → volgende scène (concept 2 Uitslaapochtend, eerste echte
> GLB-Creator-generatie: daybed ~30 cr). herbouwd op het goedgekeurde
> tuin-basis-recept (`overkappingen-website/scene_tuin_basis.py` — Beike:
> "blijf naar de handoffs kijken"): driekwart-herohoek (1.55 m, dirv-formule,
> DOF f/4), écht gras via `scripts/grass_lib.add_grass` (density 500, h_mul
> 0.72, raycast-mask), `st.border_lush`-borders strak tegen de band met
> doorgang vóór de hutdeur, island_tree-coulisses + dennen, donkere
> MAT_Grond. **Valkuil ontdekt: object met "veld" in de naam telt als
> GROUND_KW → gras groeide óp het terras** (TerrasVeld → Terras). Zon azim
> 245 (wig door de open zijkant), speelhuis (−4.55, 1.55) rot 205 vrij van de
> paal-zichtlijn. Preview v9 op :8767 + Telegram. Wacht op oordeel.
>
> *(eerdere update hieronder — v1-anker + tool-verkenning)*

> **UPDATE 16 jul (avond) — B10 SPEELHUIS-MIDDAG ANKER OP DE SITE (wacht op
> anker-akkoord):** Beike gaf go op de 6 scratch-concepten + GLB-Creator-
> mandaat (±2800 credits, zelf genereren mag, "niet dom veel spenderen").
> Gestart met concept 3 → map `pilots/B10-speelhuismiddag-Jasmijn300x250/`
> (BOUWPLAN.md + speelhuis_stap1_anker.py, herbruikbaar-definitief). Speelhuis
> Sneeuwwitje uit de tool: gratis **simplify 30%** werkt (439k tris, textures
> intact → `assets/glbcreator/speelhuis-sneeuwwitje-rev3-439k.glb`); gratis
> **rescale is een NO-OP (bug!)** → catalogusmaat lokaal via non-uniforme
> scale (0.962/0.652/1.0). Anker v7 na 6 QC-iteraties (lessen in memory
> render-debug-recepten: gltf-quaternion-rotatie, stale matrix_world,
> pine-bosjes-uitschieters, camera-rol-spiegeling, kap=−X bij Jasmijn,
> Nishita i.p.v. HDRI voor middaglicht). Preview:
> `B10-.../speelhuismiddag_fase1_anker_PREVIEW.png` op :8767 + Telegram-foto
> verstuurd. **Bij akkoord → fase 2 dressing** (speelgoedkist, vlaggetjes,
> krijtbord, borders linksvoor, bal/knuffel via BK). Daarna concept 2
> (Uitslaapochtend, daybed via GLB Creator — eerste echte generatie ~30 cr).

> **UPDATE 16 jul (avond) — GLB CREATOR VERKEND (Beike: eerst verdiepen, dan
> gebruiken):** interne tool https://glbcreator.intern.blokhutwinkel.nl/
> (zonder streepje!) maakt van tuindeco-links/Woodvision-nrs/eigen foto's via
> Meshy GLB's op ware grootte (~30 cr; rescale/simplify gratis). Volledig
> verslag + API + workflow-voorstel: `docs/GLB_CREATOR_verkenning.md`;
> memory: reference-glb-creator. Testcase Speelhuis Sneeuwwitje gekeurd:
> drop-in import (meters, gegrond, rot 0) maar 1,5M tris, roughness te glad
> (dak blauwgrijs in Cycles) en **diepte +53% vs catalogus** (alleen
> scaleBasis-as klopt) → regels: maat-check+rescale, simplify, roughness-fix.
> Probes in `_diag/glbcreator_probe_*.png`. Voorstel: decor-props voortaan
> als échte producten via deze tool (NIET de hoofdproducten — tekentool
> blijft); openstaande vragen aan Beike: credits-tegoed, wie genereert,
> ook bestaande scènes omzetten? **Stijlreeks-keuzebord v3 staat nog open**
> (zie update hieronder); speelhuis past 1-op-1 in concept 3. (Beike: "stap 5 niet volgen,
> ze moeten van scratch zelf ideeën verzinnen en assets opzoeken"):** de
> opdracht "scène 1 gin-tonic-bar afmaken + lijst afwerken" is vervangen door
> een verse conceptronde. Zes nieuwe verhalen (geen hergebruik van eerdere/
> afgekeurde concepten), hero-assets vooraf zelf gecheckt op de BK-API of al
> in huis: **1 Zonnegroet-yoga** (Zonnebloem, zonsopkomst) · **2 Uitslaap-
> ochtend buitenbed** (Roosmarijn, BK-daybed ✓) · **3 Speeltent-middag**
> (Jasmijn, proc. tipi) · **4 Vlindertuin** (Jasmijn #2, BK-vlinders ✓ +
> birdbath in huis) · **5 Schaakavond** (Roosmarijn #2, schaakset/fauteuils/
> tafel/lampjes ALLE in huis) · **6 Buitenbioscoop** (Lavendel, BK-projector
> ✓ + proc. doek) + alternatieven 5b sterren / 6b vinyl / 1b snijbloemen.
> Brief: `pilots/SCENE_CONCEPTS_stijlreeks_v3.md`; keuzebord:
> `_keuzebord_stijlreeks_v3.html` op :8768. Compositie-wetten van 16 jul per
> concept ingebakken (vloerveld, voorgrond-borders, camera per scène anders,
> boog zonsopkomst→blauw uur). **Gin-tonic-bar v3b + alle bestaande blends
> onaangeroerd gelaten** (niets weggegooid). Wacht op Beikes keuze (chat/
> Telegram/reviewsite); daarna per concept: props fetchen+proben → kort
> bouwplan → kaal anker vanaf `pilots/base/` → akkoord → dressing → preview.
> Eén scène tegelijk; finals/commits alleen op expliciet akkoord.

> **UPDATE 16 jul (sessie-einde) — OVERDRACHT:** volledige startprompt voor de
> nieuwe sessie staat in **`PROMPT_nieuwe_sessie_stijlreeks.md`** (repo-root):
> compositie-wetten uit de kapschuur/wellness-analyse, werkwijze (één scène
> tegelijk, eigen QC vóór de site), status per scène. Scène 1 (gin-tonic-bar)
> is halverwege v3b (`_diag/scene1_bar_v3b.png`); reviewsite leeg; afgekeurd
> werk in `pilots/_afgekeurd_*`. D2 gestopt, F sauna geparkeerd.

> **UPDATE 16 jul — REWORK OP KAPSCHUUR-KWALITEIT (Beike: "paden zijn
> zelfgemaakte lelijke stenen... random/verkeerd om/te weinig... neem de
> tijd"):** ontdekking: `scripts/cabin_lib.py` HEEFT het kapschuur-gereedschap
> dat de pilots nooit gebruikten — **ribbon_path** (gebogen pad),
> **klinker_strip** (echte klinkers/keramiek met voeg+jitter), plank_deck,
> slat_planter, setup_light (LIGHT_MOMENTS), festoon, audit. Alle zes scènes
> herwerkt (`_rework_bar_diner.py`, `_rework_fix2.py`, `_rework_rest.py`):
> flagstone-blobs overal vervangen door gebogen klinker-ribbons + masks ·
> bar: krukken 180° om, keramiek-60×60-terras, "cement bij de bloemen" bleek
> **Bed_R-mulchbak** (→ donkere aarde) + periwinkles stonden met 7 LOD-stapels
> (144 meshes weg) · diner: gebakken-klinker-terras + tafel voller · boules:
> witte baan weg (note), boules óp het pad, kap voller (kruk/plaid/lantaarn/
> plant) · rozenkap: zon azim 140 de kap in + fill 18W, stoelen facen de
> tafel (dining_chair front=−y), 2e klimroos · kamado: potten gevuld, prep
> naar voren + gereiplank, fill 16W · lounge: bakken met échte planten,
> camera dichter, keramiek-pad gedimd. **Regenfris (D2) weggeklikt → D2-spoor
> gestopt.** Previews op :8767; wacht op review. Memory:
> feedback-plaatsing-en-paden-discipline.

> **UPDATE 16 jul — STIJLREEKS v2 GEBOUWD (concept + plan akkoord; F sauna
> geparkeerd op Beikes verzoek):** 7 previews op :8767 — A Kamado-chef
> (proc. kamado; prep-tafel valt in schaduw, punt voor reviewnote) · B Oogst-
> diner (B7-basis, zen gestript) · C Gin-tonic-bar 2.0 (greige/eiken +
> ijsemmer) · D Designlounge 2.0 (civiele schemer i.p.v. blauw uur −3.5: dat
> bleef te donker) · H Rozenkap (BK-klimroos-wand over de kaprand; drapering
> kan mooier — evt. Sketchfab-wisteria) · K Jeu-de-boules (grindbaan +
> petanque-fetch) · L Regenfris D2v3 (nat-wegdek-shader werkt: plas-spots
> ramp 0.46/0.60 op roughness; cloudy_vondelpark). Eigen fetches: kaarsen-
> lantaarn, klimroos (66MB), petanque, ijsemmer; kamado/wisteria bestaan niet
> gratis (vault bevestigd) → kamado procedureel. Afgekeurde wow-previews →
> `pilots/_afgekeurd_wow_v1/`. Blends: *_A/B/H/K.blend naast de anker-blends;
> D2: `overkappingen-website/scene_d2_v3.py`. **Wacht op Beikes review;
> finals + commits alleen op expliciet akkoord.**

> **UPDATE 16 jul — TERUG NAAR DE ECHTE WERKWIJZE (Beike: "lees nu echt even
> goed obsidian door en ga dan bezig hoe het hoort"):** vrijwel alle wow-
> previews weggeklikt (notes: pizzaoven te groot voor de kap · ontbijthoek te
> donker + camera moet de kap in; gin-tonic-bar en designlounge géén weg).
> Vault + kapschuur-brief herlezen: de aanpak is **gebruiksverhaal met zones
> + licht-recept per beeld + tijd-van-de-dag-boog + backdrop-plan +
> onderscheid-criterium + prop-sourcing als aparte stap + Beike kiest van een
> keuzebord** (kapschuren/SCENE_CONCEPTS.md + vault "Overkapping Scene
> Concepten 2026"; 2026-principes: geen antraciet, keramiek greige, zones).
> Nieuwe concept-brief: `pilots/SCENE_CONCEPTS_stijlreeks.md` (9 kandidaten
> A/B/C/D/E/F/H/K/L incl. toewijzingsvoorstel; liever 8 rake beelden dan 10
> gevulde slots) + keuzebord `_keuzebord_stijlreeks.html`. **Wacht op Beikes
> concept-keuze; daarna per concept: props fetchen → kort bouwplan → akkoord
> → bouw+QA → snelle preview → oordeel → final.**

> **UPDATE 16 jul — ALLE 10 WOW-PREVIEWS KLAAR (Beike-mandaat: "maak alle
> previews maar af"):** op :8767 staan nu exact 10 concept-previews:
> Pizzanacht (B1) · Hangmat-siësta (B2, schemer→zomermiddag terug) ·
> Designlounge+lamp/kleed (B3) · Urban jungle (B4; **wandrek-GLB bleek een
> complete showroom met reuzenvloer → verwijderd**, planten dragen het) ·
> Vuurschaal-nacht (B5) · Gin-tonic-bar (B6, eigen BK-fetch-barkrukken +
> flessenwand) · Spiegelvijver (B7, stapstenen uit de vijver verplaatst) ·
> Ontbijthoek (B8, ongewijzigd) · Oogstkraam (B9, BK-fetch-pompoenen +
> OOGST-krijtbord) · D2v2 Fietsenpad. Anker-previews (fase1) naar
> `pilots/B*/_anker/`; site-regex nu `^[BD]\d+-`. **Nieuwe preview-standaard
> (Beike): 960×720/24/'1024' — alles vóór final snel.** Beike reviewt alles
> in één keer; daarna per akkoord → packfix + finals (expliciet akkoord
> vereist; commits idem).

> **UPDATE 16 jul — KOERSWIJZIGING NAAR WOW-CONCEPTEN + BLENDERKIT-FETCH:**
> Beike keurde 7 van de 9 batch 3-fase 2's af ("veel te saai... echt nieuwe
> ideeen, zoals de kapschuren") → nieuwe conceptlijst (Pizzanacht, Hangmat-
> siësta, Urban jungle, Vuurschaal-nacht, Gin-tonic-bar, Spiegelvijver,
> Oogstkraam; B3 designlounge + B8 ontbijthoek niet weggeklikt). Afgekeurde
> previews → `pilots/_afgekeurd_batch3_v1/`. **Keuze Beike: eerst 2 wow-
> pilots** → gebouwd op de bestaande ankers: **Pizzanacht** (B1-map,
> `jasmijn_pizzanacht_B1.blend`, BK-pizzaoven mond naar camera + gloed +
> werkblad/deeg + festoen + schemer) en **Vuurschaal-nacht** (B5-map,
> `magnolia_vuurschaalnacht_B5.blend`, satara_night-HDRI (nieuw gedownload) +
> vuur + marshmallows + plaid + festoen-naar-staak). Previews op :8767;
> vlam leest nog als lichte kegel (volgende iteratie: BK-kampvuur-asset).
> **DOORBRAAK: BlenderKit headless fetch werkt** — `pilots/_bk_fetch.py`
> (OAuth-refresh verplicht; zie memory reference-blenderkit-headless-fetch).
> Al binnengehaald: barkruk (Kasiko, voor Gin-tonic-bar) + pompoen (Kabocha,
> voor Oogstkraam). D2v2 Fietsenpad: 2e diag klaar
> (`overkappingen-website/diag/conceptD2v2-kdi-420x300.png`), nog niet op de
> pilotsite. Beike reviewt morgen (bouw-autonomie voor de nacht gegeven;
> finals + commits blijven wachten op expliciet akkoord).

> **UPDATE 15 jul — BATCH 3 ANKERS B1–B9 GEBOUWD (concept + plannen akkoord):**
> `build_batch3_anchor.py` (vloer-varianten: klinker/tegel/natuursteen/grind/
> vlonder + karrenspoor B9; lage/dichte camera's; hagen+bosrand dichterbij).
> QC-fixes via `_b3_anchor_fix.py`: **misty_dawn-HDRI toont open veld +
> hoogspanningsmasten** boven de haag (B4/B7) → kloofendal_48d;
> **Trimmed_Olive_Tree leest als bonsai-sculptuur** → Olive_tree (B6);
> B1/B3 camera's iets terug (dak was gekropt). Gekozen azims: B1 205, B2 210,
> B3 250, B4 110, B5 235, B6 230, B7 120, B8 85, B9 230. Fase 1-previews
> (1280×960) per scène in pilots/B*-mappen op :8767. **Wacht op anker-gate.**
> D2v2 (fietsenpad, overkapping-pipeline) start na de B-gates.

> **UPDATE 15 jul — HERBOUW BATCH 3 GESTART (Beike):** alle finals verzameld
> in `ALLE_FINALS/` (submaps: blokhutten-tuinscenes, blokhutten-stijlen,
> overkappingen-webshop, overkappingen-creatieve-tuinen, kapschuren). Daarna
> door Beike afgekeurd + eruit gehaald: jasmijn_familietuin, jasmijn_theehuis,
> lavendel_modern, magnolia_groene_long, magnolia_wintertuin,
> roosmarijn_kruidenterras, roosmarijn_zentuin, zonnebloem_ochtendhoek,
> zonnebloem_zomeravond, conceptD2-kdi. **Opdracht: van scratch herbouwen
> (vaste werkwijze) met kapschuren + overkappingen als kwaliteitslat** ("by
> far beter"). Analyse van het verschil + concept per scène in
> `pilots/PLAN_HERBOUW_batch3.md` (5 bouwregels: lage/dichte camera,
> pad+border-geleiding, sfeerlicht, één getextureerd vignet, volle
> achtergrond). **Wacht op concept-gate.**

> **UPDATE 16 jul — BATCH 2 FINALS KLAAR (Beike-akkoord op de gate):**
> S5 Buitenbioscoop + S8 Tuinfeest gepackt (pack_all) en gerenderd op
> 2560×1920/512/adaptive 0.008 → `roosmarijn_tuinwerkzaterdag_S5_FINAL.png`
> en `lavendel_goudenuur_S8_FINAL.png`; kopieën in
> `renders_definitief_20260716/` als **roosmarijn_buitenbioscoop.png** en
> **lavendel_tuinfeest.png**. Daarmee staan alle **8** pilots als final in die
> map. Git-commit wacht nog op Beikes expliciete akkoord.

> **UPDATE 16 jul — S5 AKKOORD (reviewsite "houden"); S8 v2d-c:** Beikes note
> "de tafel moet iets meer in de overkapping" bleek over de **lage witte
> salontafel** te gaan (eerst de buffettafel verplaatst → "verkeerde tafel.
> die tafel mag terug, ik bedoelde de lage witte"). `_s8_salontafel_in_kap.py`:
> buffettafel terug naar het gazon (−4.4, 2.4) + mask; salontafel y −0.25 de
> kap in en de lounge-bank y −0.35 mee naar achteren (bank stond 0.8 m los van
> de achterwand; anders klapte de tafel in de bank) — kussens/plaid/stilleven
> mee. Crop-QC: tafel volledig onder de kaprand, vrij van de bank. Preview op
> :8767; **wacht op S8-her-gate** (S5 wacht op final-akkoord).

> **UPDATE 16 jul — BATCH 2 v2d (Beikes notes op v2c: S5 "tv op de rechter
> zijwand, 2 stoelen die facen richting die tv met een kleine tafel" · S8
> "vlaggetjes weg, tafel staat in de plank"):** `_b2_v2d_fix.py`. **S5**:
> bank/poef/plaids weg → 2× mid_century_lounge_chair toe-in op de tv +
> side_table_01 + popcornkom; tv naar de zijwand. **Les: het binnenvlak van
> de zijwand ligt op x −2.99, niet −3.06** — tv op −3.03/−3.01 zat ín de
> wanddikte (dit was óók de v2b-"onzichtbaar"-oorzaak; de wand is wél volledig
> zichtbaar vanaf HeroCam, kijkhoek 45°) → `_s5_tv_raycast.py`: scene.ray_cast
> vanuit de kap meet het echte vlak, tv op hit+0.012/0.030. **S8**: alle
> vlaggenlijnen weg (festoen+lampionnen blijven); buffettafel (−4.9,3.4)→
> (−4.4,2.4), vrij van de jacaranda-stam, masks bijgewerkt. Previews op
> :8767; **wacht op fase 2-her-gate v2d**.

> **UPDATE 16 jul — BATCH 2 v2c: SCHEMER-KALIBRATIE + S5-HERPOSITIONERING
> (Beike: S5 "te donker, positionering interieur klopt niet" · S8 "slecht
> zichtbaar en rare positionering"):** v2b-tussenstap (zon +4) vrat de lucht
> wit uit → **civiele-schemer-recept**: sky MULTIPLE_SCATTERING elev −1.5,
> strength 1.1 + warme zonlamp E 0.8 kleur (1.0,0.60,0.40) angle 8° elev 8
> azim 210(S5)/220(S8) + exposure 0.95. **S5**: doek op de zijwand was
> onzichtbaar (occlusie-wig) → terug naar de achterwand (−1.05,−1.47,1.30);
> Bioscoopbank driekwart (rot_z π−0.85, (−0.15,0.35)); poef/plaids/popcorn
> mee. **S8** (v2b): vlaggenstaak+lijn B pal voor de kap weg → lijn C
> jacaranda→zijtuin (−8.3,5.6) 11 vlaggetjes; buffettafel van de opening naar
> het gazon onder de jacaranda (−4.9,3.4). Eigen QC v2c: gevel-lum 103/122,
> doek leesbaar, bank driekwart, vlaggen+buffet vrij van de gevel. Previews
> op :8767; **wacht op fase 2-her-gate v2c**.

> **UPDATE 16 jul — BATCH 2 v2: AVOND-CONCEPTEN (Beike: "te saai, maak het
> origineel" op béíde fase 2's → conceptkeuze via gates):** S5 = **Buiten-
> bioscoop** (blauw uur: doek 2.6×1.5 zwak emissief (0.35! — 0.9 bleekte uit)
> tegen de kap-achterwand, Sofa_01+Ottoman+plaids+popcorn, festoen 14, 2 warme
> lantaarns; moestuin-vignet gestript + masks hersteld) · S8 = **Tuinfeest**
> (schemer: 2 procedurele vlaggenlijnen (parabool+driehoekjes, 5 kleuren) naar
> jacaranda en staak, festoen 12, 2 lampionnen, buffettafel+stilleven; lounge
> bleef). Beide: `build_batch2_v2.py`. **Blender 5.1-les: Nishita-sky heet nu
> `MULTIPLE_SCATTERING`** (ShaderNodeTexSky.sky_type). Avond-kalibratie:
> sky-strength 1.3/1.5 + koele maan-vul-zon (E 0.25, elev 35, angle 40°,
> (0.65,0.75,1.0)) + exposure 1.3/1.15; Lantern_01-glas emissie 6.0 warm;
> festoen-emissie 4.0. Previews op :8767; wacht op fase 2-gate v2.

> **UPDATE 16 jul — BATCH 2 FASE 2 S5+S8 (ankers waren akkoord):**
> `build_batch2_fase2.py` + `_b2_fase2_fix.py` na crop-QC. **S5** moestuin:
> ronde werktafel + kruidenset (BK Chive + Set_of_3_Ceramic_Planters) +
> oogstmand + kleipotten + 2 moestuinbakken met aarde-inzet + regenton +
> BK-gieter; **regenton-donor is KOBALTBLAUW plastic → Base Color-override
> donkergroen + image-link losgekoppeld**. Laarzen/welcome_mat: geen donor
> aanwezig → vervallen. **S8** gouden uur: CRAIG-bank rot π (S2-les) + kussens
> + plaid + coffee_table_round (marmer-top; tex-swap werkte) + stilleven;
> **Sun_lounger_for_pool leest als leeg groen metaalframe → verwijderd**
> (incl. handdoek), fill 16→22 W. **Nieuwe les: heester-zichtbaarheid is
> camera-afhankelijk — check de sightline over de cabin-hoek** (x < sightline-x
> op de heester-diepte, anders verstopt achter de cabin; S5 → (−6.0/−7.8),
> S8 → (−6.2)). Previews op :8767; wacht op fase 2-gate batch 2.

> **UPDATE 16 jul — BATCH 2 ANKERS S5+S8 GEBOUWD:** azim-minis → S5 zon 210/
> elev 30, S8 zon 220/elev 20 (beide symmetrical_garden rot azim−5). LET OP:
> tune-conventie zon = `rotation_euler=(radians(90−elev), 0, radians(az))` —
> zelfde als anker-script; een 180−az-variant zat er eerst fout in (gestopt,
> hersteld). Zelf-QC-fixes vóór de gate: pad-gras tot 4 cm van de stenen
> (S7-les, nu ook hier) + exposure S5 0.40 / S8 0.45 (voorgrond te donker).
> Previews op :8767; wacht op anker-gate S5+S8. Bekende anker-punten voor
> fase 2: S5 Bed_L leest nog als grijze plaat (border_lush lost op), S8
> jacaranda leest groen-geel (bloei niet zichtbaar op diag-res).

> **UPDATE 16 jul — BATCH 2 GESTART (Beike: "doe maar" + plan-gate "beide
> akkoord"):** finals van batch 1 verzameld in `renders_definitief_20260716/`
> (6 stuks, schone namen). Batch 2 = de 2 resterende modellen:
> **S5 Roosmarijn 200x300-400** (plan bestond al) + **S8 Lavendel 400x300-300**
> (nieuw: `PLAN_S8_goudenuur_lavendel400x300.md` — gouden uur, rotan lounge,
> jacaranda; basis geprobed: env ±3.71, dense −0.54..3.51, kap −3.50..−0.53,
> deur 0.73..2.24 op y+1.51). `build_batch_anchor.py` uitgebreid met s5+s8-CFG's
> én het nieuwe humus-recept (spec 0/rough 1/warme ramp) zit er nu standaard in;
> bosrand meteen 15 dennen (2 rijen, −x-les verwerkt). Boom-donors geprobed:
> jacaranda keep=(jacaranda_tree_LOD0, jacaranda_tree_trunk_LOD0) — LOD-stapels
> + geometry_nodes-duplicaat op x−24.75!; tree_small_02 keep=(LOD0, trunk).
> coffee_table_round_01 heeft de .png-extensie-mismatch (fase 2 fix_images).
> S5-afwijking van plan-tekst: haag-anker-bed verplaatst naar de linker zijhaag
> (−6.4..−4.0) — het geplande (+x)-bed lag in de onzichtbare zone (−x-les).
> Ankers draaien met azimut-minis; daarna azim kiezen → diag → anker-gate.

> **UPDATE 16 jul — BATCH COMPLEET: S7-FINAL KLAAR (Beike-akkoord via gate):**
> packfix + `camelia_leesplek_S7_FINAL.png` (2560×1920/512, gepackt, op :8767).
> Daarmee zijn álle zes reset-scènes final: S1 Jasmijn, S2 Lelie, S3 Magnolia,
> S4 Zonnebloem, S6 Dahlia, S7 Camelia. **Geen enkele final is gecommit** — dat
> wacht op Beikes expliciete commit-akkoord. Enige open punten: S5 Roosmarijn
> (plan geschreven, NIET goedgekeurd, geparkeerd) en de oude R5-notities
> (camelia_buitenbad/wijnterras — apart spoor, niet in de reset-batch).

> **UPDATE 16 jul — S4 + S6 FINAL KLAAR (Beike: "houden" op beide fase 2's =
> deels-akkoord-gate):** packfix (96/82 files gepackt) + `_s1_final.py` →
> `zonnebloem_zomerselunch_S4_FINAL.png` en `dahlia_ochtendkoffie_S6_FINAL.png`
> (2560×1920/512, op :8767). NIET gecommit — wacht op expliciet akkoord.
> **S7**: Beikes "zelfde kleur groen als de andere 2" → zon E 1.15→2.0 warm +
> exposure 0.85 (gras matcht S4/S6 nu); daardoor lichtte de kale humus-band rond
> de stapstenen geel op → humus donkerder én `_s7_pad_gras.py`: gras hergroeid
> tot 4 cm van de steenranden (gazania-masks uitgespaard). Nieuwe fase 2-preview
> op :8767, wacht op S7-gate. S5 (Roosmarijn) blijft geparkeerd zonder akkoord.

> **UPDATE 16 jul — FASE 2d + GROND-FIX (Beikes reviewsite-punten):**
> `build_batch_fase2d.py`: S7 bijzettafel+boeken+kommetje 0.45 m de kap in
> ("tafel staat in de muur"); S4 potten-ensemble naar de kap-hoekkant, tafelzicht
> vrij ("plantenbakken aan de rechterkant"). Grond-note (alle drie: "grijs, niet
> groen of bruin"): ramp donkerder maken was NIET genoeg — de vlakke humus
> reflecteerde de koele lucht speculair → **Specular IOR Level 0.0 + roughness
> 1.0 op MAT_Humus + verzadigder ramp (0.022,0.034,0.006)↔(0.085,0.058,0.018)**
> → leest olijfgroen-bruin in zon én overcast (crop-QC bevestigd). Memory
> bijgewerkt (render-debug-recepten NB2). Previews op :8767; wacht op her-gate.

> **UPDATE 16 jul — FASE 2b/2c VERRIJKING (Beike op de 2-gate: "zijn allemaal
> niet slecht. maar gewoon heel leeg en saai" → geen finals, eerst vullen):**
> `build_batch_fase2b.py` + `build_batch_fase2c.py` + `_s4_fix_vignet.py`.
> Toegevoegd per scène: heesters (shrub_02, per variant LOD0) vóór de achterhaag,
> gazania-plukken langs de stapstenen, potten-ensemble (potted_plant + kleipot
> met gazania) bij de kap-opening; S4 golf-zonnebed (BK Sunbed, procedureel hout)
> op het gazon + emmer + gieter; S6 koperen vogelbad (Birdbath 03) bij de berk +
> gieter; S7 wijnvat+plant naast de kap + tweede kussenset op de daybed.
> **Nieuwe lessen:** (1) zichtbare achterveld = NEGATIEVE x (heesters stonden
> eerst op +x achter de cabin, scherm-onzichtbaar — screen-links = +x!);
> (2) shrub/gazania-blends wijzen naar .jpg/.exr maar de texturen staan als .png
> op schijf → extensie-swap-helper `fix_images()` in fase2b; flower_heliophila
> heeft GEEN texturen op schijf (niet gebruiken); (3) gazania 0.16 verdrinkt in
> 0.72-gras → 0.26+ met mask r 0.30; (4) fbx-picknickkleed op klein formaat
> rendert wit/mini → vervangen door BK Sunbed; wicker_basket_02 heeft een LOSSE
> deksel die gekanteld valt — niet blind neerzetten; (5) meubels met open frame
> op gras NIET maskeren (kale-aarde-plek leest slordig), alleen platte items.
> Previews op :8767; wacht op fase 2-her-gate.

> **UPDATE 16 jul — FASE 2-BATCH S4+S6+S7 GEBOUWD (ankers waren batch-akkoord):**
> `pilots/build_batch_fase2.py -- <s4|s6|s7>` + fixes na zelf-QC. **S4**: eettafel-
> set gedekt (plank/schaal+bananen/2 goblets); stoelen los van de set-root gezet —
> occlusie-wig-les: diep in de kap is alles met sightline-x > −0.03 op het
> openingsvlak onzichtbaar achter de moduulwand → stoelen ondiep (y 0.7-0.9)
> geplaatst en via hoek-delta naar de tafel gericht (`_s4_fix_stoelen.py`);
> let op: 'table_chair_set' matcht óók '_chair_' (substring-les nogmaals).
> **S6**: bistroset — krukken waren KRUISLINGS gegroepeerd (naam-suffix .001
> pairt niet met de ruimtelijke ligging in de donor!) → opnieuw geappend en
> spatiaal geclusterd op donor-x (`_s6_fix_bistro.py`); dekenrol (blanket_round,
> terracotta) op kruk 2; mand h 0.22 naar de kap-hoek (blokkeerde eerst de
> stapsteen-aanloop), opengeslagen boek ernaast. **S7**: daybed Pita + kussens +
> plaid + opengeslagen boek; bijzettafel met 3 procedurele dichte boeken
> (sketchfab book.blend is een ópengeslagen boek — niet stapelbaar) + kommetje;
> Lantern_01 h 0.45 van de grasrand naar schoon terras. Overal: border_lush
> R+L + warme fill (16/12/14 W, use_shadow=False). Previews op :8767;
> **wacht op fase 2-batch-gate**; daarna finals (packfix + `_s1_final.py`)
> per expliciet akkoord.

> **UPDATE 15 jul-nacht — ANKER-FIXES S4+S7 (Beike-note "kale achtergrond, andere
> hdri ofzo. of dikkere en meer bomen achter de heg"):** beide via
> `pilots/_fix_achtergrond_batch.py`: **S4** kloofendal-puresky →
> `symmetrical_garden_4k` rot 100 (zon-azim 105 − 5, S1-conventie) · **S7**
> kloofendal_overcast → `cloudy_vondelpark_4k` **rot 0** (rot-hunt 0/90/180/270:
> 0 = groenst, geen gebouwen; 180 toont parkpaviljoen boven de daklijn!) · beide
> +9 dennen (gaten dicht + hogere 2e rij op y ≈ −11/−12, duplicaten van bestaande
> Bosrand-roots). S7 was daarna te donker (lum 57.5 vs 80–103 elders) →
> `_s7_licht_lift.py`: strength 1.35, exposure 0.80 → lum 72. Previews op :8767
> ververst; **wacht op anker-her-gate**. Fase 2-batch staat klaar:
> `pilots/build_batch_fase2.py -- <s4|s6|s7>` (donors geprobed:
> bistroset = tafel-90h+2 krukken-61h naast elkaar (los groeperen!), Daybed Pita
> schoon 1.95×0.74, BK-"parasol"-map bevat GEEN parasol → S4-parasol vervalt
> (plan voorzag dit), sketchfab book.blend = opengeslagen boek cm-schaal —
> stapeltje wordt procedureel; geen (0,0)-images in de donors).

> **UPDATE 15 jul-avond — BATCH-WERKWIJZE (Beike: "alles in één keer zodat ik
> makkelijker kan checken"):** S3-final klaar (gepackt, op :8767). Voor de 4
> resterende cabins staan de volledige plannen klaar, zelfde diepgang als S1–S3,
> alle bases opgemeten (kap steeds op −x, opening +Y):
> `PLAN_S4_zomerselunch_zonnebloem300x300.md` (heldere middag, puresky) ·
> `PLAN_S5_tuinwerkzaterdag_roosmarijn200x300.md` (namiddag, moestuin, 4m-kap) ·
> `PLAN_S6_ochtendkoffie_dahlia250x250.md` (dageraad misty_dawn zónder mist) ·
> `PLAN_S7_leesplek_camelia250x300.md` (diffuus overcast — uniek in de reeks).
> Flow: batch-gate plannen → álle ankers bouwen+tonen → batch-gate → álle
> fase 2's → batch-gate → finals per expliciet akkoord.

> **UPDATE 15 jul — S3 "Atelier in de tuin" (Magnolia 300x200) FASE 2 AKKOORD →
> FINAL:** plan `pilots/PLAN_S3_atelier_magnolia300x200.md`, map
> `pilots/S3-atelier-Magnolia300x200/`. Licht: symmetrical_garden + zon 75°/24°
> (azimut-tests). Anker-iteraties: tree_small_02 heeft LOD0+LOD1 gestapeld +
> leaf-cards bij origin (ontdubbelen!) en stond eerst achter de daklijn (dode
> toptakken boven het dak) → vrij rechts in beeld gezet; rechter beeldrand
> dichtgezet met Haag_L2 + extra den. Dressing: **ezel procedureel** — eerste
> versie afgekeurd door Beike ("klopt nog niet"): poten liepen parallel; herbouwd
> als echte veldezel via slat()-helper (voorpoten → apex, achterpoot, legplank
> óp het pootvlak, doek ervoor, topklem). potted_plant_04 miste álle PH-texturen
> (magenta) → overrides; let op: match op `_pot`-suffix, want "potted_plant"
> matcht óók op 'pot' (plant werd eerst terracotta). Packfix-script
> (`pilots/_s2_packfix.py`) is generiek: vervangt missende bronnen door
> generated (AO→wit, rest→grijs) en packt; gebruikt vóór elke final.

> **UPDATE 15 jul — S2 "Gouden borrel" (Lelie 400x250-300-zijwand) FASE 2 AKKOORD →
> FINAL:** plan `pilots/PLAN_S2_goudenborrel_lelie400x250.md`, map
> `pilots/S2-goudenborrel-Lelie400x250/`. Licht: azimut-tests → zon 138°/13°
> E3.4; kiara-HDRI afgekeurd (bergen op de horizon, niet af te dekken met
> hagen/dennen — kale stammen laten precies de horizonband vrij) → **the_sky_is_
> on_fire rot 90** (avondrood; rot 180/270 toont FLATS — rotatie is kader-
> gebonden!). Dressing: rotan lounge (CRAIG) + PH-kussens, borreltafel (PH-
> texturen ontbraken → donker-hout-override), wijnvat ×0.82, procedurele
> festoen (koord + 12 emissieve bolletjes, strength 3.5), vuurschaal-hoekje
> (Stone_Fire_Pit ×donker-HSV + firewood met schors-override + sintels-emissie +
> 30W gloed — 130W bleekte alles uit!) + 2 PH-krukjes. Beike-notities verwerkt:
> bank stond 180° verkeerd; lege voorgrond → vuurhoekje. Nieuwe prop-lessen:
> pine_tree_01_2k bevat 3 varianten × 3 LOD's — per variant alleen LOD0+trunk
> kopiëren en per KOPIE de bbox centreren (groepsgewijs kopiëren zet bomen
> dwars door de kap); adirondack-gltf komt gekanteld/zwevend binnen (afgekeurd);
> BK-stapstenen zijn reuze-rotsscans → `cl.flagstone_path` gebruiken.

> **UPDATE 13 jul-avond — S1 "Familie-middag" FASE 2 AKKOORD → FINAL:** eerste
> scène van de volledige reset (zie `pilots/PLAN_S1_familiemiddag_jasmijn300x250.md`,
> map `pilots/S1-familiemiddag-Jasmijn300x250/`). Dressing-iteraties op Beikes
> notities: mand ×0.68 · tuintje-rechts en kussens-vignet op Beikes verzoek weer
> volledig verwijderd (was te slordig) · vervangen door solitaire **zilverberk
> 5,5 m** (BlenderKit `berk/Silver_Birch_Tree.blend`) op (−5.2, 3.0) met donkere
> boomspiegel — Beikes keuze uit 4 vul-opties → **fase 2 akkoord, final gestart**
> (2560×1920/512/adaptive 0.008 + pack_all, `pilots/_s1_final.py`).
> Nieuwe lessen: (1) `birdbaths_gltf` is een SHOWCASE met 4 baden + koperen
> voederpaal — altijd 1 variant strippen; Birdbath 02 = klassiek stenen bad mét
> eigen wateroppervlak. (2) `materials.append(None)` (materiaal was gepurged na
> save) geeft stil een leeg slot = rendert WIT; altijd het slot verifiëren.
> (3) `blanket_pillows.fbx`: "blanket_round" is een OPGEROLDE deken, geen
> uitgespreid kleed. (4) humus-ramp 55% donkerder tegen "grijs onder het gras".
>
> **UPDATE 13 jul-middag — WERKWIJZE-PIVOT (Beike):** "je werkt te snel; kijk hoe
> we bij de overkappingen werkten — begin liever opnieuw dan kleine aanpassingen
> stapelen." → pilots voortaan HERBOUWEN via OPUS_WERKWIJZE.md (plan → kaal+anker
> → akkoord → dressing → akkoord). Vastgelegd in memory
> `feedback-pilots-overkapping-werkwijze`. Eerste resultaat: **theehuis herbouwd
> en goedgekeurd** (`_rebuild_theehuis_stap1.py`, plan in
> `pilots/PLAN_rebuild_jasmijn_theehuis.md`): overkapping-grasmix (density 560,
> h_mul 0.72) + humusgrond + grindterras gravel_floor_02 met edging + donkere
> stapstenen + misty_dawn rot315 (315 = mast-vrij!) world 0.52 + zon E8
> elev15/azim150 + AgX MedHigh exp0.35; dressing = bank/theeset/kei/lantaarn.
> Gras-mask-les: expliciet cellen nullen onder bay/deur/bed + rond verborgen
> props (raycast ziet hidden objects niet). Promotie: `_R4.blend`; oude staat =
> `_R4_pre_rebuild.blend`; patch-route (_ziel) verwijderd. Ook eerder vandaag
> goedgekeurd: pluktuin + magnolia (die waren vóór de pivot, patch-route).
>
> **UPDATE 13 jul (Fable 5, live review-loop met Beike):**
> - **Beslissingen opgehaald:** rebuilds = goede R4-basis · wintertuin = vroege
>   lente · gras = milde variant (kleurtint+hoogte, GEEN R5-clumps) · huishouden
>   akkoord (cleanup + finals-commit).
> - **3 QC-blockers gefixt:** (1) Deur_Stoep-grind theehuis+ochtendhoek →
>   PavingStones125A-remap; wortelaak bleek dubbel: node-links naar Base Color/
>   Normal waren óók los (`_fix_grind_relink.py`) + mapping naar Object+BOX
>   (`_fix_grind_mapping.py`). (2) wild_rooibos leeshoek: 4 texturen bestonden
>   nergens op schijf → met Beikes akkoord opnieuw van PolyHaven (CC0) gedownload
>   naar `assets/polyhaven/models/textures/` + gepackt. (3) magnolia: alle
>   aerial_grass_rock-images zitten gepackt — geen actieve landmijn.
> - **Blender 5.1-valkuil:** colorspace zetten vóór `img.reload()` laat de reload
>   stil mislukken; toets met `img.size[0]>0`, niet `has_data`.
> - **Huishouden:** `_cleanup_weekend.ps1` LIVE gedraaid (127 untracked `_diag`-
>   bestanden → `_quarantine_weekend/`), `.gitignore.proposed` overgenomen
>   (commit 64881cf), 4 overkapping-tuinfinals gecommit (da93bd9).
> - **Pluktuin doorbraak (Beike-akkoord, gepromoveerd naar `_R4.blend`):**
>   Beikes "grond is grijs → scène onbruikbaar" bleek de **Mist_Rig-volume** die
>   alles waste (rode-verf-test + kale-grond-render bewezen het). Fix: mist uit +
>   warme zon elev11/azim110/3800K + syferfontein-HDRI (`_fix_pluk_licht.py`),
>   grond = procedureel donkergroen/humus + roughness 0.95 (`_fix_grond_humus2.py`),
>   mild gras: per-pol tint-attribuut + hue±0.03/value 0.88-1.14 + scale
>   0.62-1.50 (`_gras_mild_test.py`). Oude blend = `_R4_pre13jul.blend`.
> - **Review-server :8767:** nieuwe sectie ⓪ voor `*_R4_FIX_PREVIEW.png` (fixes
>   van vandaag); server herstart (PID 3104).
> - **Volgende:** review-loop per scène in QC-volgorde; gras/humus/licht-recepten
>   per scène uitrollen na Beikes per-scène akkoord.

> **UPDATE 9 jul (fixronde R5, live):**
> - **S1 gras-mix** GEBOUWD in `scripts/grass_lib.py`: 3 tuft-varianten (pick
>   instance), per-instance kleur (3 groentinten + ~7% droog via ObjectInfo.Random),
>   density-noise kale plekjes + rand-fade, scale 0.6-1.4 + tilt, GEEN realize meer
>   (instanced). Signature `add_grass()` ongewijzigd + nieuwe kwargs
>   dry_frac/sat_mul/val_mul/fade/bare voor scene-smaak. Eerste test te schraal
>   → density×1.45, noise-min 0.40. LET OP: `FunctionNodeRandomValue` INT-sockets
>   op index [4]/[5] benaderen (naam 'Min' pakt het vector-socket!).
> - **S2 practicals** GEBOUWD in `scripts/cabin_lib.py`: `emissie_mat()` (spa-recept)
>   + `practicals_on(mode)` — bollen/snoeren 2200K sterkte 2 (dag) / 4 (schemer),
>   MAT_Bulb-festoons ook naar 2-4 (28 blies uit naar wit), lantaarns glow-mats +
>   warme point (radius 0.05) in bbox-centrum. `overhang_fill` bestond al.
> - **Reviewserver :8767 gepatcht**: sectie ① = `*_R5_PREVIEW.png` + `*_R1_PREVIEW.png`
>   (fixronde + nieuwe scènes), ② = R4-referentie, ③ = AGXv2. Herstart gedaan.
> - Fixes per scène draaien op de **_R4.blend** (NIET opnieuw apply_r4 vanaf R3 —
>   post-R4 handfixes zitten alleen in de R4-blends), output `_R5.blend` + `_R5_PREVIEW.png`.
> - dahlia_leeshoek = eerste scène (fixscript `_fix1_leeshoek.py`).
> - **Ketens (detached, Start-Process):** `_chain_scenes26.ps1` (wijn-iter4,
>   familietuin, wintertuin-deel1, zomeravond, ochtendhoek) →
>   `_chain_scenes713.ps1` (veld, bad, kubus, nevel, pluk, thee, kantoor; wacht
>   op 26) → `_chain_ankers.ps1` (zomeravond-iter2 + vijvertuin-anker +
>   kampvuur-anker; wacht op 713). Logs: `_diag/chain*.log` (LET OP: PS `*>`
>   schrijft UTF-16 — grep faalt, lees met PowerShell of check exit-codes).
> - **QC-stand (eigen review, R5):** leeshoek ✓ (5 iteraties: zon-HDRI-balans!),
>   wijnterras ✓ (4 iteraties: monster-olijf eruit geleerd — Trimmed_Olive_Tree
>   GLB is een reuze-oude-boom, GEEN kuipplantje), familietuin ✓, wintertuin ✓
>   (deel 1; winterkeuze + plaid open), zomeravond ✓ na iter2 (stapstenen van
>   flagstone_path lezen te wit bij lage zon → donker+smooth).
> - **Open vragen aan Beike (via Telegram gesteld):** (1) wintertuin: winter of
>   vroege lente? (2) zonnebloem-asset ontbreekt — BlenderKit aanzetten of
>   alternatief? (3) anker-akkoorden vijvertuin + kampvuur.
> - **QC 7-13 (alle 13 R5-previews af, 11:26):** veld ✓ (rijen+stroken+pad;
>   smetje: bolboompje half voor de deur), bad ✓ na iter2-in-wachtrij (deksel =
>   Object_11 'metal', asset heeft EIGEN water Object_5 — eigen schijf weg),
>   kubus ✓ (bay leeft met sofa; groene HDRI-vlekken resteren), nevel ✓
>   (banden opgelost; houtstapel-iter2 in wachtrij), pluk ✓✓ (lichtfix =
>   transformatie), thee ✓ (grind = echt grind), kantoor ✓ (bureau zichtbaar!).
> - **Bekend restpunt hele lijn:** flagstone-domes lezen wit onder lage zon
>   ondanks donkere ramp (contrast-effect) — evt. dome-hoogte verlagen; eerst
>   Beikes oordeel afwachten.
> - Slot-iteratieketen klaar om te draaien ná ankers: `_fix8b_buitenbad.py`,
>   `_fix11b_ochtendnevel.py`.
>
> **BESLUIT 10 jul (Beike): R5-RONDE VERWORPEN.** "Round 5 is allemaal slecht" →
> alle 26 R5-bestanden (13 blends + 13 previews) + de GRASMIX-test verwijderd.
> R4 blijft de basis; Beike geeft R4-feedback **vanaf Fable 5** (niet nu op Opus).
> LET OP — de R4-`.blend`-bestanden staan NIET meer op D: (alleen de 13
> `*_R4_PREVIEW.png`); ze zijn door een eerdere opschoning van D: gehaald (blends
> zijn ~1 GB elk). Backup: `C:\Users\beike\Documents\Blender-blokhutten_OLD\pilots`
> (159 blends) — MAAR die R4-blends zijn van **2 jul 13:26**, ouder dan de
> R4-previews van 8 jul (dus vóór de vuren-rene-wandronde van 3 jul + latere
> fixes). Voor de Fable-5 R4-ronde: R4-blends terugzetten uit _OLD en checken of
> de 2-jul-staat volstaat, of de 8-jul-R4 opnieuw opbouwen. De 2 nieuwe ankers
> (vijvertuin/kampvuur R1) staan er nog — Beike moet zeggen of die blijven.
> (Niet mijn R5-wis: dry-run bewees R4-blends al 0 vóór de wis; wis raakte enkel R5.)
>
> **TERUGGEZET UIT _OLD (10 jul, op verzoek Beike):**
> - 10 R4-blends terug op D: (buitenbad, wijnterras, tuinkantoor, leeshoek,
>   theehuis, familietuin, pluktuin, lavendelveld, ochtendnevel, avondkubus) —
>   staat = **2 jul 13:26** (vóór de vuren-rene-wandronde van 3 jul; de 8-jul-
>   R4-previews kunnen dus iets afwijken van deze blends).
> - 3 scènes hadden GEEN R4 in _OLD (ná de snapshot gerenderd): magnolia_wintertuin,
>   zonnebloem_zomeravond, zonnebloem_ochtendhoek. Voor die 3 is de **R3-blend
>   (2 jul)** teruggezet als werkbare basis — R4 is daaruit te herbouwen via
>   apply_r4.py op de R3 (zo is R4 oorspronkelijk gemaakt; keys in _diag/r4_scenes.txt).
> - Alle blends ~1 GB (packed), zelfstandig te openen.
>
> **EINDSTAND 9 jul (na sessie-herstart + Opus-overname) — GEARCHIVEERD, R5 verworpen:**
> - **Alle 13 pilots op R5 + 2 nieuwe ankers op R1** — alle 15 in sectie 1 van
>   de review-site :8767 (server + klik-monitor herstart na de crash). Nog GEEN
>   review-kliks van Beike ontvangen (`pilots_review_keuzes.json` leeg).
> - Slot-iteraties gedraaid: buitenbad open bad (deksel = tub-child `Object_11`
>   'metal'; tub heeft eigen water `Object_5` → eigen schijf verwijderd), ochtend-
>   nevel houtstapel 1.5× + 2e stapel in de bay.
> - **Vijvertuin-anker** (3 iteraties): iter2 = water lag ÓNDER de grondplane
>   (z-0.04) → onzichtbaar; opgelost door water op +0.02 + kuip die de grond
>   afdekt. iter3 = vlonder +7 cm/naar oever, oever smaller+donker, camera naar
>   (5.3,8.9) zodat de cabin in het water spiegelt (= het plan-shot). KADER AF.
> - **Kampvuur-anker** (4 iteraties): strippen tot kaal (kruidenterras-restanten:
>   Bed*/Kruid*/Kt2*/OlijfPot/Rozemarijn_N via bbox-root-match), vuurkuil-ring +
>   2 boomstambanken + stronk, blue hour venice_sunset. iter4-LES: HDRI-rotatie
>   275° bracht de venice-VILLA in de camera-kijkkegel → absoluut naar 185°
>   (vlakke-horizon-stand) = schone bomen-silhouet. Placeholder-gloed 22W/0.8m
>   (was 35-60W/0.45m → wast props roze). KADER AF. Echt vuur/sintels/plaids/
>   houtstapel-in-kap = DRESSING (stap 2, wacht op akkoord).
> - **GEBLOKKEERD op Beike:** (a) review-feedback op de 13 R5-scènes, (b) anker-
>   akkoord vijvertuin+kampvuur vóór dressing (harde regel: anker→akkoord→dressing),
>   (c) wintertuin winter/lente?, (d) zonnebloem-asset (BlenderKit aan of alt?).
>   Akkoord-vraag via Telegram verstuurd 9 jul.
> - **S4-LES (zon in dawn-scènes, geverifieerd met A/B/C-isolatietests):** de zon
>   "deed niks" — maar hij werkte prima. De dawn-HDRI's (kiara_1_dawn) zijn zó helder
>   dat world 0.85-1.0 een E5-9-zon volledig wegwast (ambient op een gevel ≈ 6-10 W/m²
>   vs 4.7 van de zon). Fix = BALANS: world naar ~0.45-0.5 + zon E7-9. Verder: camera
>   staat IN de mist-cube → hoge zonne-energie geeft melkwitte in-scatter-waas (test A,
>   E50). En azim ~140 = recht van achter de camera = vlak; kies 100-125 (zijlicht).
>   Isolatietest-recept: `_test_sun_ab.py`/`_test_sun_c.py` (world 0 → alleen zon).

> **UPDATE 8 jul (avond): LEES EERST `docs/REVIEW_pilots_R4_voor_9jul.md`**
> — complete in-depth review van alle 13 actieve pilot-scènes op
> R4-niveau met per scène een uitvoerbare fixlijst + 5 systemische
> fixes (gras-mix, practicals aan, paden, zonrichting, horizon) + de
> aanbevolen dagvolgorde voor 9 jul. Voor de 2 vervallen scènes liggen
> er nieuwe plannen: `docs/PLAN_pilot_magnolia_VIJVERTUIN.md`
> (natuurvijver + vlonder, vervangt groene_long) en
> `docs/PLAN_pilot_roosmarijn_KAMPVUUR.md` (vuurkuil + boomstambanken
> blue hour, vervangt kruidenterras). Werkwijze: WERKWIJZE_REVIEWLOOP.md
> (anker → akkoord → dressing → reviewloop op :8767). Zentuin = Beike.

## Waar we zijn
Sessie-doel: alle renders verbeteren (vault + eerdere feedback + online research).
Ronde R3 (concept-dressing) is AF op 15 scenes. Ronde R4 is AF: 13/13 scenes
(exit 0, _R4.blend + _R4_PREVIEW.png). Eindreview gedaan; 2 gevonden defecten
gefixt en herrenderd: familietuin (4 overlappende vogelbaden -> 1) en
ochtendhoek (Deur_Stoep gravel-texturen misten door C:->D:-migratie ->
AmbientCG PavingStones125A, gepakt in blend). Zie _diag/r4_fix_*.txt.

## Beike-feedback die R4 fixt (apply_r4.py, gevalideerd op Pluktuin)
1. UV-nerf mét de plank (lange-as-normalisatie per board, island-center-rotatie) — baas-feedback, BELANGRIJKSTE.
2. Waterige/doorzichtige gras-tapijten: repareren (dicht+mat), NIET verbergen (tapijt = gazon-basis + raycast-grond).
3. Vloer onder overkapping waar gras onder het dak zit (raycast-grid-detectie, plank_deck).
4. Gras-rebuild met fijne mask (cell 0.22) — geen sprieten door patio/verharding.
5. Zwevende boom-onderkanten gronden.
KRITIEKE LES: mist/haze-cube (Mist_Rig) blokkeert raycasts → tijdelijk hide_viewport
tijdens mask/vloer-checks (zit al in apply_r4.py). Zonder dit: gras verdwijnt overal.

## Status per scene (R4)
KLAAR (exit 0, _R4.blend + _R4_PREVIEW.png):
lavendel_pluktuin (testscene, gevalideerd goed), camelia_buitenbad (vloer toegevoegd),
camelia_wijnterras, dahlia_tuinkantoor, dahlia_leeshoek,
jasmijn_familietuin (vloer toegevoegd), jasmijn_theehuis (vloer toegevoegd),
lavendel_lavendelveld, lelie_ochtendnevel.

NOG TE DOEN (batch was bij scene 9/12 gestopt voor herstart):
lelie_avondkubus, magnolia_wintertuin, zonnebloem_zomeravond, zonnebloem_ochtendhoek.

VERVALLEN (Beike): magnolia_groene_long, roosmarijn_kruidenterras. Zentuin = Beike zelf.

## Hervatten (exact)
1. Server: `cd C:/Users/beike/Documents/Blender-blokhutten && python -m http.server 8765 --bind 127.0.0.1`
   → galerij op http://localhost:8765/_r3_review.html (thumbs in _r3_thumbs/, gen: `python _r3_review_gen.py`).
2. Restant-batch (zelfde patroon als _diag/r4_scenes.txt-loop, alleen deze 4):
   voor elke key in {lelie_avondkubus, magnolia_wintertuin, zonnebloem_zomeravond, zonnebloem_ochtendhoek}:
   `PYTHONUNBUFFERED=1 "C:/Program Files/Blender Foundation/Blender 5.1/blender.exe" -b <base>_R3.blend --python apply_r4.py -- <key> <base>_R4.blend <base>_R4_PREVIEW.png > _diag/r4_run_<key>.txt 2>&1`
   (paden: zie _diag/r4_scenes.txt; na elke scene `python _r3_review_gen.py`.)
3. DAARNA (expliciete opdracht Beike): **grondige eindreview van alles** — elke R4-preview
   vol formaat bekijken, checken op: gras door verharding, vloeren onder overkapping netjes
   binnen gevel (buitenbad/familietuin/theehuis kregen auto-vloer!), nerf-richting, zwevers,
   waterigheid, gras-look t.o.v. R3 (rebuild = nieuwe scatter). Log-check: _diag/r4_run_*.txt.
   Daarna eindrapport + galerij.

## Beike-feedback ronde 2 (2 jul ~16:00) + status
1. Wintertuin: witte glans door gras heen, geen tuinondergrond -> grond-textuur
   omgezet van aerial_grass_rock (witte rotsvlekken) naar painted_grass (groen,
   conform vault-regel "onderkant onder dicht gras = groen"). GEFIXT+herrenderd.
2. Ochtendnevel: zwevende boomvoeten achteraan (bomen op y<-17 staan buiten de
   grondplaat) -> FarGround_R4-plaat 120x120m op z=-0.02 + 6 extra dennen
   (linked copies BosDen) in de achterste band. GEFIXT+herrenderd.
3. Familietuin: 4 overlappende vogelbaden -> 1 (Birdbath 02). GEFIXT+herrenderd.
4. Ochtendhoek: Deur_Stoep gravel-texturen echt kwijt -> PavingStones125A. GEFIXT.

## KRITIEKE LESSEN (niet opnieuw doen)
- `img.has_data=False` is GEEN bewijs van kapotte textuur: gepakte images laden
  lui. Echt kapot = `packed_file is None` EN bronbestand weg, of `packed_file.size==0`.
  Fout gemaakt: unpack(REMOVE) op gezonde packs in wintertuin -> 3 Firewood-texturen
  vernietigd; hersteld via export uit leeshoek-pack naar
  assets/sketchfab/props/stacked_firewood/textures_orig/.
- Blender resolven van relatieve output-paden is onbetrouwbaar (schreef naar
  C:\pilots\...): ALTIJD os.path.abspath voor scn.render.filepath.
- Veel R4-blends verwijzen nog naar C:\Users\beike\Documents-paden maar hun packs
  zijn gezond; NIET blind remappen. Nieuwe assets van Beike staan in
  C:/Users/beike/Downloads/blokhut-props-verwerkt/ (props, geen bomen) +
  assets/sketchfab/trees/old_olive_tree (nieuw vandaag).

## Wand-textuur ronde (3 jul ~16:30) — Beike's eigen vuren-textuur
Beike leverde `C:/Users/beike/Documents/hout textuur, rene.jpg` (2048², naadloos
licht vuren, ~7 planken). Gekopieerd naar `assets/blokhutwinkel-textures/extra/vuren-rene.jpg`.
Toegepast op ALLEEN de 4 naturel-houten blokhutten (Beike koos eerst alle 13,
corrigeerde naar 4): zomeravond, wijnterras, familietuin, ochtendnevel.
Grijze/zwarte blokhutten houden hun eigen afwerking.
- Script `_apply_spruce.py`: herbouwt base-color-keten van `basetexture-firstLayer-wall`
  + `-canopyWall` -> TexCoord.UV -> Mapping(scale 0.55) -> vuren-rene (FLAT) -> Base Color
  + Bump(0.15). Verwijdert HueSat/Mix-tint-nodes (die de wanden eerder grijsden/warmden).
  rough 0.62, spec 0.25.
- Schaal 0.55 gekozen na test (0.55/1.5/3.0): 0.55 = warmst, leest als massief vuren,
  elke fysieke plank (3.2×0.15m, UV V-slice 0.04) pakt schone strip. Hoger = bleek/druk.
- Deur (hardhout), balken (douglas), dak blijven ongemoeid — alleen wandcladding.

## Bekende restpunten voor het eindrapport
- Tuinkantoor: bureau valt vanuit camerahoek deels achter topiary (verhaal leest matig; camera bewust niet aangeraakt).
- Avondkubus: gele HDRI-vlek in bomen linksboven; bay blijft gedempt (zwarte wanden eten licht).
- Zomeravond R3-previews: wijnset-flessen op tafel — check schaal in eindreview.
- Familietuin: 1m-tuinschep in zandbak — plausibel maar checken.
- Kruidenterras-R3 heeft een gerepareerde-maar-vervallen status (props op tafel gefixt; scene vervalt).
- Gallery-generator: _r3_review_gen.py — pakt automatisch R4 > R3 previews, DROPPED-lijst erin.

## Proces-regels (blijven gelden)
Headless CLI renderen (nooit MCP), AgX, texture_limit 2048, geen commits zonder akkoord,
geen finale 2560×1440 zonder akkoord, Beike aanspreken met "Beike".
