# HANDOFF — Filmpjes v2: nieuwe clips na de plankfix (3 sep 2026)

Beike, 3 sep: "we moeten met de plankfix ook nieuwe renders maken van de video's, maar ik was eigenlijk
niet content met de video's. Hoe we de scènes hebben opgebouwd is bij veel dat het er goed uitziet vanuit
een bepaalde hoek. Op de filmpjes zag je angles waardoor de tuin lelijk leek."

## Oorzaak

`scripts/nachtclips_multishot.py` (vakantierun 6–11 aug) bouwde per clip drie shots: A = hero-beweging,
**B en C = orbits van 28–42° om het kijkdoel** naar "écht andere standpunten". De scènes zijn alleen richting
de hero-camera aangekleed (grasranden, backdrop-naden, kale zones opzij), dus die orbits toonden precies wat
niet af is. De raycast-guard van toen keek alleen of de lens niet in een heg zat, niet of het beeld nog in
de aangeklede kegel lag.

## Nieuwe aanpak: `scripts/clips_v2/`

**Regel: elke shot blijft binnen het hero-beeld.** Het goedgekeurde final-beeld is de bewezen-goede
compositie; de clip mag daar alleen ín bewegen.

| bestand | wat |
|---|---|
| `scenes.py` | registry: scène → blend (PLANKFIX/HOEKFIX; R4 = `_OLD`-kopie) + runtime-tweaks van de R4-fixronde (exposure/mats/zon/fill_canopy, niet in de blend) + clipnaam. 23 blokhut-scènes prio 1, 7 kapschuur/overkapping prio 2 |
| `geo.py` | `Ctx`: hero-cam, cabin-bbox, grond, prop-vignetten in het hero-beeld, en **`frame_score()`** = raycast-raster 32×18 door een kandidaat-camera → aandeel dat óók in het hero-beeld ligt (`inside`), plus grond/lucht/void |
| `shotlib.py` | shot-woordenschat: `push`, `settle` (pedestal met shift_y-compensatie, camera blijft waterpas), `truck`, `detail` (50–55 mm op een vignet), `reveal` (opent op vignet → landt op exact het hero-beeld), `focus_pull`; `default_recipe` = A reveal / B push / C detail |
| `shots/<scene>.py` | optionele eigen shotlijst per scène (`def shots(ctx, sl): return [...]`) — dit zijn "de scripts per blend" |
| `render_clip.py` | engine: tweaks → Ctx → shots → **toets per shot** (inside ≥ 0,90, geen void, lucht/grond ≤ hero + marge, blik niet geblokkeerd) → `probe` (begin/eind-still 960×540/24) of `full` (PNG 1920×1080/48, hervatbaar). Shot die faalt wordt in full overgeslagen (`--force` om toch te renderen). Blend nooit opgeslagen |
| `encode_clip.py` | PNG-reeksen → mp4, H.264 via PyAV (crf 18, yuv420p), crossfades 12 fr |
| `build_review.py` | contactvel per scène + `_clips_v2_review/index.html` met de oude clip ernaast |
| `run_probe_all.sh` / `run_stills_all.sh` / `run_full_all.sh` | JSON-probe / probe-stills / nachtrun (wacht op vrije GPU, encode + Telegram per clip) |

Uitvoer: probe-JSON's `scripts/clips_v2/_probe/<scene>.json`, stills `_probe/stills/<scene>/`, frames
`scripts/clips_v2/_frames/<scene>/`, clips `ALLE_FINALS/filmpjes-v2/<clip>.mp4`.

## Lessen tijdens het bouwen

* Yaw voor een waterpas camera: `rot.z = atan2(dy, dx) − 90°` (B13: kijk (0.545, −0.838) → −146,98°).
* De hero-toets moet op dezelfde beeldverhouding als de clip: S/B-finals zijn 4:3, clips 16:9 → resolutie
  zetten vóór `Ctx()`, anders klopt `inside` niet (hero zelf scoorde 0,78).
* Detailshots: **niet verplaatsen, laten de lens zoomen.** 30 % richting het vignet lopen gaf inside 0,59
  (grasranden buiten het hero-beeld); 6–10 % + 50–55 mm geeft 0,91–1,00.
* Vignet-ranking op "leven" (meubels/lampen/spullen, `LIFE_RE`), niet op aantal objecten — anders wint de
  border met 40 plantjes van de zithoek.
* Windows: `python … > lijst.txt` schrijft `\r\n`; Blender weigert een pad met `\r` ("Cannot read file:
  Invalid argument") → `tr -d '\r'`.
* Blender 5.1 heeft geen video-uitvoer; cv2 `avc1` faalt stil (openh264 ontbreekt) — PyAV (`av` 13) zit op
  de PC en levert echte H.264.

## Status (4 sep, 10:30)

**Probe-JSON's: 30/30 klaar.** Probe-stills: 3 scènes definitief klaar (`dahlia_ochtendkoffie`,
`roosmarijn_schaakavond`, `zonnebloem_zomerselunch`), de overige **28 draaien nu** in één pass
(gestart 10:20, ~4,5 min/scène → klaar rond 12:30). Nog geen frames en geen mp4's.

Belangrijk voor het reviewen: **Beike heeft nog niets gezien.** Alle verdicts in
`_probe/TUNING_NOTES.md` ("alles OK, laten", de C-shot-fixes) zijn Claude-oordelen van de contactvellen.

### Twee dingen die tijdens deze pass zijn gerepareerd

* **Sessie-botsing.** De stills-run van 3 sep 16:37 leefde nog (hij hervatte om 09:39 met de PC) en er
  liep om 10:20 een tweede runner naast. Twee headless Blenders op één RTX 3070 met de GUI erbij = OOM-
  risico; de oude tree (bash 29612 → 4124 → blender 36736) is beëindigd. De `zonnebloem_zonnegroet`-render
  die daarin liep is weg en wordt in deze pass opnieuw gedaan. Runners vind je op deze PC **niet** met
  `pkill`/`ps -ef` maar met `Get-CimInstance Win32_Process` (naam `bash.exe`, CommandLine `run_stills_all`).
* **`settle` is geen veilige C-fallback.** Een pedestal duwt het beeld aan de boven/onderrand open en
  faalde de toets op `lavendel_buitenbioscoop` (C_settle inside 0,865/0,837). Vervangen door een nieuwe
  `zoom`-shot: zelfde loc/rot/shift als de hero, alleen de lens loopt 35 → 45,5 mm. Dat is een smaller
  frustum van het hero-beeld en daarmee per definitie frame-veilig. **Regel: alleen een pure push en een
  lens-inzoom zijn strikte deelverzamelingen van het hero-beeld.** Oude versie: `_probe/shotlib_voor_zoomfix.py.bak`.

### Open punten na deze pass

* ~~`jasmijn_familiemiddag` C faalt op 0,851/0,847~~ en ~~`lavendel_buitenbioscoop` mist een shotfile~~ —
  **opgelost met een nieuwe shot `crop_in`** (4 sep). Uitleg staat onder "De uitsnede-shot".
  `lavendel_buitenbioscoop` pakt zijn shotfile automatisch mee in de lopende pass.
* **`lelie_goudenborrel` C faalde nog harder: 0,597/0,582** (200 van 576 stralen op GrassTuft/IB-Hedge/
  Ground_Grass). Oorzaak: `detail()` met `dz=-0.35` + `hoogte_ndc=0.40` — camera zakte, liep naar het
  subject toe en kadreerde omlaag. Ook opgelost met `crop_in`; de "vuur in het onderste derde"-kadrering
  komt nu uit het mikpunt (80 cm boven de grond) i.p.v. uit een lagere camera.
* **Deze twee scènes moeten ná de pass opnieuw geprobed worden** (het waren scène 1 en 2, dus al gerenderd
  met de oude C):

      rm -rf _probe/stills/jasmijn_familiemiddag _probe/stills/lelie_goudenborrel              _probe/stills/roosmarijn_uitslaapochtend _probe/stills/zonnebloem_modern              _probe/stills/camelia_buitenbad
      bash run_stills_all.sh jasmijn_familiemiddag lelie_goudenborrel roosmarijn_uitslaapochtend                              zonnebloem_modern camelia_buitenbad

  `camelia_buitenbad` (R4) faalde als **enige op twee shots**: A_reveal opende op **0,792** (Ground_Grass 46
  stralen, HedgeSprig 39) en C_detail gaf **0,859/0,875**. Het hero-beeld heeft daar veel grond (0,234) en
  beide vignetten liggen ver naar rechts (u = 0,794 en 0,699), dus elke camerabeweging haalt gras en heg
  binnen. Nu volledig op uitsnede-shots: A via de nieuwe `crop_reveal` (opent 60 mm, zoomt uit naar de 35 mm
  hero-stand), C via `crop_in` (60 -> 70 mm, bank gecentreerd). De beweging komt van B_push.

  `zonnebloem_modern` faalde op **0,625/0,627** (Ground_Grass 60 stralen, Deck_Wood 45, drie berken 62;
  grondaandeel 0,132 tegen hero 0,049). Het standaardrecept mikt daar op vignet 1 = `modern_arm_chair_01`
  op u = 0,135, vlak tegen de linkerrand. Die is niet te centreren onder de 118 mm, dus dit is het eerste
  **geklemde** crop-geval: 70 -> 80 mm, uitsnede tegen de linker hero-rand, fauteuil op u = 0,29 -> 0,33.
  Deze scene heeft een hero-lens van **32 mm**, niet 35.

  `roosmarijn_uitslaapochtend` faalde in deze pass op **0,818/0,811** (GrassTuft_A/B/C, HedgeSprig,
  Ground_Grass, Mist_Rig buiten het beeld) met dezelfde oorzaak als goudenborrel: `dz=-0.25` +
  `hoogte_ndc=0.45` liet de camera naar z=1,17 zakken. Ook omgezet naar `crop_in` (62 → 70 mm, mikpunt
  70 cm zodat de plantenbakken op v = 0,41 vallen).

  Let op de tegenvoorbeelden: `jasmijn_vinylmiddag` heeft dezelfde `dz`-signatuur maar **haalt** de toets
  (0,944/0,967), en `zonnebloem_zomerselunch` heeft het meest randgelegen doel van allemaal (u = 0,88,
  centreren pas vanaf 143 mm) en haalt hem ook (0,969/0,991). De afstand tot de beeldrand voorspelt het dus
  niet; wat telt is wat er *rond* het subject staat (aangekleed terras of kale grasrand), en dat weet alleen
  de raycast-toets. Gebruik daarom de nieuwe `toets`-mode i.p.v. voorspellen.
* De 8 R4-scènes hebben generieke propnamen (`Object_8`, `SM_vgztealha`), dus de `LIFE_RE`-ranking is daar
  zwak — reken op handgeschreven shotfiles.
* Na de run: `_probe/keep_awake.flag` weggooien (PID 31904 stopt dan). `run_full_all.sh` start zijn eigen
  keep-awake onder `_frames/`.
* `run_full_all.sh` pas ná Beike's akkoord op het reviewblad (≈ 3,5 u per scène).

### Status 4 sep 10:30 — run overgedragen aan een andere sessie
Sessie 61 bouwde de engine en reviewde 13 van 30 probe-stills (eigen oordeel, Beike heeft nog niets gezien):
tuinscenes S1–S8 + B10–B14 allemaal A/B binnen het hero-beeld; de C-detailshot faalde bij 8 scènes (deur aan de
linkerrand of prop aan de rechterrand → 0,58–0,89) en is per scène herschreven in `shots/<scene>.py`
(10 bestanden). Aantekeningen: `_probe/TUNING_NOTES.md`. Om 10:19 gaf Beike de job aan sessie
blender-blokhutten-36; die sessie draait nu de (her)probe van de 9 verouderde + 17 resterende scènes en
rapporteert aan Beike. Open punten voor die sessie: `settle` als C-fallback faalt de toets (pedestal
verbreedt het beeld; alleen push en lens-zoom zijn strikt deelverzamelingen) → zoom-in als fallback;
`lavendel_buitenbioscoop` heeft een eigen shotfile nodig; R4-scènes hebben generieke propnamen → handmatige
shotfiles; `keep_awake.flag` onder `_probe/` weggooien na de run; nachtrun pas na Beikes akkoord op het
reviewblad.

## De uitsnede-shot (`crop_in`, 4 sep)

Het terugkerende probleem met de C-shots: een prop die je wilt uitlichten zit vaak dicht bij de rand van
het hero-beeld, en `detail()` loopt 10 % naar dat subject toe plus een zijwaartse drift. Dat kleine stapje
onthult precies de niet-aangeklede randen (familiemiddag C: 149 van 576 stralen op IB-Hedge, GrassTuft_A/B/C,
Ground_Grass, een pine-trunk → inside 0,851).

`crop_in(ctx, doel, lens0, lens1)` doet het zonder te bewegen: **standpunt en blikrichting blijven exact die
van de hero**, alleen de lens snijdt naar binnen en `shift_x`/`shift_y` pannen naar het subject. Het beeld is
dan een uitsnede van het hero-beeld — een smaller frustum binnen het hero-frustum — en dus frame-veilig voor
elk subject, ook aan de rand.

Rekenregel (uit `geo.rays`: `lx = (u − 0,5 + sx)·S/L`, `ly = ((v − 0,5)·a + sy)·S/L`), met `k = L/L0`:

    sx ∈ [k(sx0 − 0,5) + 0,5 ,  k(sx0 + 0,5) − 0,5]        (idem verticaal met a/2)

Voor `k > 1` is dat interval niet leeg, dus er is altijd een veilige uitsnede; wil het subject verder naar
buiten dan het interval toestaat, dan wordt de shift geklemd en komt het subject uit het midden te liggen
**in plaats van dat de toets faalt**. Hoe verder ingezoomd, hoe meer panruimte: op 35 mm (`k = 1`) valt het
interval samen met het hero-beeld zelf, op 55 mm mag de shift ±0,214.

Wat dit oplost: een subject centreren dat je met yaw of translatie niet frame-veilig kunt halen. De deur van
familiemiddag zit op `u = 0,29`; die is op géén enkele brandpuntsafstand te centreren met een gedraaide
camera, maar het punt tussen deur en border (`u = 0,346`) valt op 55 mm precies in het midden.

* Nieuwe shots in `shotlib.py`: `zoom` (pure lens-inzoom, hero-midden), `crop_in` (lens + pan) en
  `crop_reveal` (opent als uitsnede, zoomt uit naar exact het hero-beeld). `crop_reveal` is frame-veilig
  over de **hele** shot, niet alleen op de sleutels: het bevattingsgebied is per as begrensd door twee
  lineaire ongelijkheden in (k, shift) en dus convex, en de baan tussen de sleutels is recht.
* Een **geklemde** uitsnede houdt 1 % marge van de hero-rand (`_CROP_MARGE`): zonder marge vallen er door
  afrondingen randstralen buiten (buitenbioscoop verloor ongeklemd al 2 van 576 stralen).
* `render_clip.py` animeert nu ook `shift_x` (keys hebben een optionele `shift_x`; ontbreekt die, dan
  `ctx.shift[0]` — dus alle bestaande shots renderen identiek). Back-ups: `_probe/shotlib_voor_zoomfix.py.bak`,
  `_probe/render_clip_voor_shiftx.py.bak`.
* Regressietest: `blender -b --python _probe/_test_crop_in.py` — nep-ctx met de hero-cijfers van beide scènes,
  vergelijkt de shifts met de handberekening, controleert dat de camera niet beweegt/draait en dat `push`
  onveranderd is. Draait in 2 s zonder scène en zonder GPU.
* **Regel: alleen een pure push, een lens-inzoom en een uitsnede zijn strikte deelverzamelingen van het
  hero-beeld.** Yaw, translatie en pedestal zijn dat niet.

## Ontbrekende textures (gevonden 4 sep tijdens de stills-pass)

Twee scenes renderen met ontbrekende image-textures. Cycles logt dat als `ERROR Image file ... does not
exist` en rendert het materiaal zwart/magenta - dus dit zit ook in de stills die Beike reviewt en zou in de
finals terechtkomen.

| scene | ontbreekt | waar het naar wijst |
|---|---|---|
| `zonnebloem_modern`, `jasmijn_vinylmiddag` | `periwinkle_plant_{diff,disp,nor_gl,opacity,rough,translucency}_2k` (6) | `assets/polyhaven/models/textures/` - de blend `periwinkle_plant_2k.blend` staat er wel, de textures zijn nooit meegekomen (Ottoman_01 en Sofa_01 staan er wel) |
| `jasmijn_vinylmiddag` | `Metal032_8K_Metalness.jpg`, `Metal032_8K_Roughness.jpg`, `brushed-metal-texture.jpg` | een absoluut pad op de machine van de oorspronkelijke maker (`...BlenderProgects/винил/шаблоны/текстуры/...`) - lost hier nooit op |

Dat tweede geval is extra zuur: het is de platenspeler, juist het onderwerp van vinylmiddag, waarvan de
metalen delen dus ongetextureerd renderen. Nog niet aangeraakt - de blends worden alleen gelezen en nooit
opgeslagen, en dit is een materiaalingreep die Beike eerst moet willen. Opties: periwinkle opnieuw van
Polyhaven halen, en voor het metaal een vervangende texture of een vlak metaalmateriaal zonder maps.

## Twee bugs die de verdicts van deze pass raken (4 sep)

### 1. De toets meet tegen de LEVENDE camera, niet tegen het opgeslagen hero-beeld

`geo.Ctx.ndc()` is `world_to_camera_view(scn, self.cam, p)` en leest dus `cam.matrix_world` en `cam.data`
zoals ze op dat moment zijn - niet `self.matrix`/`self.lens`. `render_clip.reset_cam()` zette de hero-waarden
wel terug maar riep **geen** `view_layer.update()`, dus `matrix_world` stond nog op de laatste render-stand
van de vorige shot. Omdat C altijd na B_push komt, en B_push op hero + 10 % eindigt, is **elke C-shot van
deze pass getoetst tegen een 10 % ingedrukte referentie** in plaats van tegen het echte hero-beeld.

Bewijs: `camelia_wijnterras` C_zoom key0 *is* per constructie het hero-beeld (zelfde loc/rot/lens/shift) en
heeft exact dezelfde beeldinhoud als `hero_score` (cabin 0,373, ground 0,125, veg 0,222, sky 0,097) - maar
scoorde 0,804 terwijl `hero_score.inside` 1,0 is. Een hero-identiek beeld verloor dus 19,6 % van zijn stralen
aan een verkeerde referentie.

Fix: `view_layer.update()` aan het eind van `reset_cam()` (toegepast 11:37:47, back-up
`_probe/render_clip_voor_resetfix.py.bak`). Scenes die daarna startten (vanaf `dahlia_tuinkantoor`, 11:38:23)
hebben betrouwbare verdicts; **alles daarvoor moet opnieuw gemeten worden** met de `toets`-mode.

Let op bij het herlezen van de oude verdicts: 0,85-0,86 kan onder een juiste referentie prima 1,00 zijn,
maar 0,50-0,63 is te ver weg om door deze bug verklaard te worden.

### 2. De vignet-ranking promoveert vloeren tot onderwerp

Twee dingen samen in `geo._vignetten()`:

* `SKIP_RE` is geankerd (`^`), dus een naam met scene-prefix ontsnapt: `DlTerras_base` matcht niet op
  `^Terras`. Zelfde patroon bij `CwTerrasMain`, `LaDeck_p10`, `OnDeck_base`, `Betonvloer`.
* De drempel `cl['w'] < 3` is bedoeld als "minstens iets van leven erin" (LIFE_RE = w 3), maar een stapel
  gewone objecten haalt hem ook: 17 terrastegels x w 1 = 17. En omdat op `-w` gesorteerd wordt, verslaat
  zo'n stapel bijna de zithoek (leeshoek v0 w 18 met tafel+fauteuil+boek, v1 w 17 puur terras).

Gevolg: het standaardrecept mikt C soms op een **vloer**, en een detailshot op een vloer haalt onvermijdelijk
grond in beeld. `dahlia_leeshoek` C = `DlTerras_*` gaf 0,502/0,503, de slechtste van de pass (178 stralen op
Ground_Grass, grond 0,363 tegen hero 0,085).

Scenes waar een vloercluster A- of C-doel is: `dahlia_leeshoek` (beide), `dahlia_tuinkantoor` (C),
`kapschuur_C_bergkap` (C, Betonvloer), `lelie_avondkubus` (**A en C**, LaDeck), `lelie_ochtendnevel` (v2, geen doel).

**geo.py is niet aangepast** - een betere ranking (eisen dat er echt een LIFE-lid in zit, en daarop sorteren
i.p.v. op totaalgewicht) verandert ook de A-doelen van scenes die Beike nog niet gezien heeft. Keuze voor
Beike: ranking structureel repareren, of per scene een shotfile met vaste coordinaten (nu gedaan voor
leeshoek).

## Stills-pass afgerond 12:26:58 - alle 30 scenes hebben verdicts

**Belangrijke nuance bij de reset_cam-bug: alleen de C-shots zijn besmet.** De A-toets loopt als eerste in
een scene, voordat een render de camera heeft verplaatst, dus die meet altijd tegen het echte hero-beeld.
B_push volgt op A_reveal, en die landt op het hero-beeld, dus ook B is goed. Alleen C volgt op B_push, die
op hero + 10 % eindigt. **A- en B-verdicts zijn dus betrouwbaar, ook van voor 11:37:47.**

| meting | scenes | falende shots |
|---|---|---|
| POST-fix (betrouwbaar) | 12 | pluktuin C 0,807 - avondkubus A 0,861 - ochtendnevel C 0,814 - keuken C 0,878 - zwembad C 0,748 |
| pre-fix, A/B betrouwbaar, C opnieuw meten | 18 | wijnterras A 0,688 - buitenbad A 0,792 (echt) / familiemiddag C 0,847 - goudenborrel C 0,582 - uitslaapochtend C 0,811 - modern C 0,625 - buitenbad C 0,859 - leeshoek C 0,502 (opnieuw meten) |

`camelia_wijnterras` C_zoom 0,804 was **volledig artefact**: de eerste sleutel van een zoom *is* het
hero-beeld, dus die is in werkelijkheid 1,000. Die C hoeft niet gerepareerd.

### Shotfiles die nu klaarstaan (11 crop-gevallen in de regressietest)

| scene | wat | reden |
|---|---|---|
| `jasmijn_familiemiddag` | C crop 55-64 | C 0,847 (opnieuw meten - kan onnodig blijken) |
| `lelie_goudenborrel` | C crop 65-74 | C 0,582 |
| `roosmarijn_uitslaapochtend` | C crop 62-70 | C 0,811 |
| `zonnebloem_modern` | C crop 70-80 geklemd | C 0,625 |
| `camelia_buitenbad` | A crop_reveal 60, C crop 60-70 | A 0,792 (echt) + C 0,859 |
| `camelia_wijnterras` | A crop_reveal 65 geklemd, C zoom | A 0,688 (echt) |
| `dahlia_leeshoek` | C crop 75-85 | C 0,502, vloer-vignet |
| `lavendel_pluktuin` | C crop 62-72 op de bank | C 0,807 (post-fix) |
| `overkapping_keuken` | C crop 72-80 | C 0,878 (post-fix) |
| `overkapping_zwembad` | C crop 75-85 geklemd | C 0,748 (post-fix) |
| `lavendel_buitenbioscoop` | eigen shotfile, C crop 58-66 | had er geen; C_crop haalde 0,997/1,000 |

### Wat nog open staat

1. **Beslissing mist** (zie hieronder): beslissend voor avondkubus A en ochtendnevel C.
2. **Beslissing vignet-ranking** in geo.py: structureel repareren of per scene shotfiles.
3. **Beslissing ontbrekende textures** (periwinkle + het platenspeler-metaal).
4. Daarna: uniforme hermeting van alle 30 met `toets`-mode (~90 s per scene, geen GPU), zodat elk verdict
   tegen hetzelfde juiste hero-beeld staat. Pas dan is te zien welke van de drie twijfelgevallen
   (familiemiddag, buitenbad C, uitslaapochtend) echt gerepareerd moesten worden - de rest kan terug naar
   de oorspronkelijke compositie.
5. Daarna de gerepareerde scenes opnieuw stillen en het reviewblad bouwen.
6. `_probe/keep_awake.flag` weggooien als er niets meer draait (PID 31904 stopt dan).

### Truc: het live C-doel terugrekenen uit een gerenderde camerasleutel

Als de probe-JSON verouderde vignetten heeft, hoeft een scene niet opnieuw te draaien om te weten waar C op
mikte. Uit `<shot>_score.json` -> `cam[0]`: met `r = shift_y * 36 / lens` (standaardrecept heeft
`hoogte_ndc = 0.5`), `dist_h = focus / sqrt(1 + r^2)` en `dz = r * dist_h` volgt
`doel = loc + (-sin(yaw), cos(yaw)) * dist_h + (0, 0, dz)`. Gebruikt voor keuken (2,118 / 3,201 / 0,973) en
zwembad (0,633 / -3,842 / 0,368); beide kwamen exact uit op de u/v die de audit voorspelde.

---

## 4 sep, na de crash: de drie beslissingen zijn genomen en verwerkt

Beike gaf om 13:45 akkoord op alle drie de open beslissingen ("alle drie ja, ga maar"). De PC was net
herstart omdat de Claude-app was gecrasht; er liep toen niets zwaars (de stills-pass was om 12:26:58 klaar,
er waren nog geen frames), dus er is geen renderwerk verloren.

### 1. Mist: twee bugs, niet een

`geo.rays()` deed `scn.ray_cast` zonder filter, dus de toets-straal stopte op de **mistdoos**. Die doos
staat dicht bij de camera, dus zijn raakpunt projecteert ergens ver buiten het hero-beeld -> vals alarm
(`lelie_avondkubus` A 0,861 en `lelie_ochtendnevel` C 0,814, beide met `Mist` bovenaan `outside_top`).

De mist doorlaatbaar maken **alleen** was niet genoeg: `lelie_ochtendnevel` C ging toen van 0,814 naar
**0,781**. Achter de mist houdt de wereld gewoon op, dus stralen die eerst op de mist stopten (en als
`prop` meetelden) werden nu `void` = gat in de wereld. In de render staat op die pixels echter gewoon
nevel, en dat is precies waarom het hero-beeld daar wél werkt.

Daarom nu twee regels samen:

* `Ctx.cast()` kijkt door onzichtbare meshes heen en geeft terug of de straal door mist is gegaan.
  Onzichtbaar = `visible_camera` uit, holdout, `hide_render`, of alle materialen zonder oppervlak op de
  output (alleen volume, of een pure Transparent BSDF). `hide_render` zat er bewust bij: die objecten
  staan wél in de depsgraph waar `ray_cast` tegenaan kijkt, dus de toets zag dingen die de render niet ziet.
* Een straal die door mist gaat en daarna niets raakt is **`fog`** en telt niet mee in `inside` (noch
  boven, noch onder de streep). **Mist verbergt onafgewerkte tuin, hij kan hem niet onthullen.** Raakt de
  straal na de mist wél iets (de blokhut door de nevel), dan telt hij gewoon normaal mee.

`inside` is dus nu "aandeel van de stralen mét beeldinhoud dat ook in het hero-beeld ligt". Is alles nevel,
dan is `inside` 1,0: er is dan niets dat buiten het hero-beeld kan vallen.

### 2. Vignet-ranking: vloeren zijn geen onderwerp meer

Drie ingrepen in `geo.py`, allemaal aan de ranking - `default_recipe` is niet aangeraakt:

* **`skip_naam()`** i.p.v. `SKIP_RE.match()`: het patroon mag nu ook aan het begin van een *woorddeel*
  staan, dus `DlTerras_base`, `CwTerrasMain`, `LaDeck_p10` en `OnDeck_base` vallen af. Zoeken zonder anker
  kon niet - `Veranda` bevat `rand` - daarom split op `_ . - cijfers` en op de camelCase-grens
  (`(?<=[a-z])(?=[A-Z])`, zonder `re.I`, anders matcht de grens overal).
* **`w_life`** per cluster: alleen de leden die LIFE_RE halen. Gesorteerd op `(-w_life, -w)`, dus een stapel
  van 17 terrastegels (w 17) verliest van een zithoek met tafel + fauteuil (w_life 6). Geen *harde* eis dat
  er leven in zit: de R4-scenes hebben generieke propnamen (`Object_8`, `SM_vgztealha`) en zouden dan
  helemaal zonder vignet komen te staan (`lelie_avondkubus` en `lelie_ochtendnevel` hebben 0 LIFE-clusters).
* Het **mikpunt** van een cluster komt uit de LIFE-leden, niet uit het gemiddelde van de hele stapel - zo
  trekt een terras onder de bank het doel niet meer naar beneden.

Bewezen op echte scenes: `dahlia_leeshoek` C 0,502 -> **1,000**, `kapschuur_C_bergkap` C (Betonvloer)
-> **1,000**, `jasmijn_familiemiddag` C 0,847 -> **1,000**.

### 3. Ontbrekende textures

* **Periwinkle**: de 6 maps opnieuw van Polyhaven gehaald naar `assets/polyhaven/models/textures/`
  (`periwinkle_plant_{diff_2k.jpg, disp_2k.png, nor_gl_2k.exr, opacity_2k.png, rough_2k.exr,
  translucency_2k.png}`, groottes exact gelijk aan de API). Fixt `zonnebloem_modern` en `jasmijn_vinylmiddag`.
* **Platenspeler-metaal**: die paden staan op de schijf van de oorspronkelijke maker en lossen hier nooit
  op. Daarom `fix_missing_textures()` in `render_clip.py`: altijd-aan, runtime, blend wordt nooit opgeslagen.
  Het zoekt image-datablocks waarvan het bestand niet bestaat, haalt hun link uit de node tree en zet de
  Principled-socket terug op een eigen waarde (`Roughness` 0,25 / `Metallic` 1,0 / `Base Color` grijs), zodat
  het vlak metaal wordt i.p.v. zwart. Logt elk ontbrekend pad (`ONTBREEKT: ...`) en elke losgemaakte link.
* **Nieuw gevonden tijdens de validatie**: `dahlia_leeshoek` mist `wild_rooibos_bush_{alpha,diff,nor_gl,rough}.png`
  (4 maps) - een bos die dus zwart zou renderen in een scene die Beike nog moet reviewen. De Polyhaven-maps
  zijn gedownload, maar de blend verwijst naar andere bestandsnamen (zonder `_2k`, alles `.png`), dus de
  exacte paden komen uit de `ONTBREEKT`-regels van de hermeting.

### Keep-awake heeft nooit gewerkt

`keep_awake.ps1` deed `SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED)`. `-bor` promoveert
naar int64 en dan faalt de P/Invoke-cast met een `InvalidCastException` - op de eerste ronde van de lus, dus
na `New-Item`. Het vlagbestand stond er dus wel, terwijl de watcher al dood was. Dat verklaart de stilstand
van 3 sep 17:11 tot 09:39. Gefixt met een expliciete `[uint32]`-cast rond de or.

### Nieuwe bestanden

| bestand | wat |
|---|---|
| `run_toets_all.sh` | hero-toets voor alle scenes zonder te renderen -> `_probe/toets/<scene>/`; ~1,6 min/scene, geen GPU, hervatbaar (slaat scenes met `_toets.json` over), eigen keep-awake |
| `_probe/_test_geo_fixes.py` | regressietest voor beide geo-fixes: 29 checks in ~3 s, zonder scene en zonder GPU. Bevat negatieve controles (een echt oppervlak blokkeert nog steeds; `Veranda` wordt niet geskipt) |

`_probe/_test_crop_in.py` draait onveranderd door (alle crop-shifts en `push` identiek), dus de
uitsnede-wiskunde is niet geraakt door de geo-wijzigingen.

---

## 4 sep 15:30 — Beike's akkoord: nachtrun/weekendrun gestart

Beike ging vrijdagmiddag weg en gaf "go" op de volledige run. Wat er sindsdien is gebeurd:

### Vier scenes gerepareerd vóór er GPU-tijd in ging
De toets-pass (sessie 36) stond op 24/30 en gaf vier keer LET OP — alle vier hetzelfde bekende patroon:
`detail()` en `reveal()` verplaatsen de camera en halen daarmee ongeklede randen binnen.

| scene | shot | score | nu |
|---|---|---|---|
| `lavendel_lavendelveld` | C_detail | 0,762 / 0,772 | `crop_in` op vignet 1 (52 → 60 mm) |
| `lelie_ochtendnevel` | C_detail | 0,868 / 0,874 (grond 0,352 tegen hero 0,196) | `crop_in` op vignet 1 (52 → 60 mm) |
| `lelie_avondkubus` | A_reveal **en** C_detail | 0,614 (grond 0,443 tegen hero 0,161) / 0,828 | `crop_reveal` 60 mm + `crop_in` 55 → 65 mm |
| `zonnebloem_modern` | A_reveal | 0,694 | `crop_reveal` 58 mm (C_crop stond al goed) |

`lelie_avondkubus` is naast `camelia_buitenbad` de tweede scene die op twee shots faalde en dus volledig op
uitsnede-shots draait; de beweging komt daar van B_push. De shotfiles mikken op `ctx.vignet(n)` in plaats van
vaste wereldcoördinaten — `crop_in` klemt zelf tegen de hero-rand, dus dat is per constructie frame-veilig.

Hertoets van deze vier draait achter de lopende toets-runner aan (`_probe/_hertoets_4.sh`, wacht tot de
runner weg is en toetst dan opnieuw). Hun probe-stills in `_clips_v2_review/` zijn nog van de **oude** shots.

### Pre-flight vóór een run van ~60 uur
* **Schijf:** D: heeft 595 GB vrij; ruim genoeg voor PNG-reeksen van ~1,5 GB per scene.
* **Slaapstand:** `powercfg` staat op AC al op nooit (slaap 0, sluimer 0), dus de run overleeft het weekend
  ook als `keep_awake.ps1` faalt. De `InvalidCastException` in `_toets_run.log` komt uit een run van vóór de
  uint32-fix; het script zelf is al gerepareerd.
* **GPU:** `run_full_all.sh` wacht zelf tot de GPU < 25 % is, dus hij loopt netjes achter de viewer-thumbnails
  en de printjobs aan.

### Wat er nu draait
`nohup bash run_full_all.sh` (log `_frames/_run_full.log`), volgorde van `_lijst.txt`: S1–S8, B10–B15,
zonnebloem_modern, de 8 R4-scenes, daarna kapschuren en overkappingen. Klare mp4's worden overgeslagen en
PNG-reeksen zijn hervatbaar, dus de run mag zonder schade onderbroken worden. Per klare clip gaat er een
Telegram-melding naar Beike.

Reken op ~3,5 uur per scene: van vrijdagmiddag tot maandagochtend haalt hij grofweg **17 à 18 van de 23
prio-1 clips** — dus zeker S1–S8 en B10–B15 compleet.

**Claim: deze sessie heeft de runner gestart. Start geen tweede `run_full_all.sh`** — de GPU-wachtlus vangt
gelijktijdig renderen grotendeels op, maar tussen twee scenes in kunnen er alsnog twee Blenders tegelijk
starten en dat is op een 3070 met 8 GB een OOM-risico.

### Reviewblad
`_clips_v2_review/index.html` is opnieuw gebouwd en dekt nu alle **30** scenes (was 13), met per scene het
contactvel naast de oude, afgekeurde clip.

### Bijstelling 15:40 — Beike is t/m woensdag weg, run mag t/m do 10 sep doorlopen
Daarmee past de **hele lijst van 30** in het venster (vr 4 sep 15:32 → do 10 sep ≈ 137 uur; ~4 à 5 uur per
scene, dus rond woensdag klaar). Er hoeft dus niets uit de wachtrij geschrapt te worden: na de 23 prio-1
blokhutten komen ook de 3 kapschuren en 4 overkappingen aan de beurt.

Gemeten: het eerste frame van `jasmijn_familiemiddag` kostte ~60 s terwijl de viewer-thumbnails en een
printjob nog GPU pakten. Zonder die concurrentie hoort ~40 s/frame te halen zijn (312 frames = 3,5 uur).

**Eerste frame visueel gecontroleerd** (`A_reveal_0001.png`): blokhut met verlicht interieur, picknicktafel
onder de overkapping, heg en klinkerpad — compositie klopt, geen magenta materialen of zwevende props. De
hele keten blend → shots → toets → PNG is daarmee bewezen; alleen de encode-stap is pas bewezen als de
eerste mp4 er staat (vanavond).

### Watchdog (nieuw, met Beike's akkoord)
Zes dagen onbewaakt kruist Patch Tuesday (8 sep) en een Windows-herstart zou de hele week stilleggen.
Daarom `scripts/clips_v2/watchdog.ps1` + geplande taak **`clips-v2-watchdog`** (elk half uur, plus 3 min na
aanmelden, herhaling stopt vanzelf na 7 dagen):

1. **Herstart** `run_full_all.sh` als er geen runner én geen renderende Blender meer is — de run is
   hervatbaar, dus hij pakt de draad op waar hij lag, en stuurt een Telegram-melding dat hij herstart is.
2. **Meldt mislukte scenes** (`FOUT` in het runlog) — de runner zelf meldt alleen geslaagde clips.
3. **Meldt een Traceback in een scene-log**, zodat ook een mislukte *encode* opvalt; die zou anders
   ongemerkt doorlopen omdat de runner gewoon met de volgende scene verdergaat.
4. Stopt met starten zodra alle 30 clips er staan. Elke melding gaat één keer (`_watchdog_gemeld.txt`).

Getest: de taak draait, ziet de lopende runner en doet dan niets (geen dubbele runner). Valkuil onderweg:
een inline `bash -lc "..."` vanuit `Start-Process` **faalt stil** — er gebeurt niets en er komt geen fout.
Daarom start de watchdog een eigen scriptbestand, `restart_full_run.sh`; dat pad is apart getest.

**Opruimen als het klaar is:** `Unregister-ScheduledTask -TaskName 'clips-v2-watchdog' -Confirm:$false`

## 4 sep 16:50 — sessie die Beike aan liet staan: doorlooptijd bijgesteld + hervatfix

Beike liet deze sessie aanstaan om de run te bewaken. Drie dingen gevonden en gerepareerd.

### 1. Afgebroken planken-render hongerde de nachtrun uit (26 min verloren)
Om 15:38 startte een **derde** headless Blender (`_planken14/render_views.py` op
`lavendel_400x300_300_zijwand_v13.stl`) uit een *foreground* Bash-call van een andere Claude-sessie; die
tool-call was rond 15:48 al getimeout, dus er wachtte niemand meer op de uitvoer, en de doel-PNG's stonden
er al van 14:57. VRAM ging naar 7836/8192 MiB en de clips-run leverde tussen **15:37:55 en 16:03:47 geen
enkel frame**. Proces gestopt → frame 4 kwam 16 s later.

**Les:** start een planken/print-render nooit als foreground Bash-call zolang de clips-run loopt. Zo'n call
timeout op 10 min maar de Blender eronder blijft draaien en is dan van niemand meer.

### 2. Runner stierf 16:42, watchdog herstartte hem 16:43 — en dat kostte 34 frames
De watchdog heeft gedaan waarvoor hij is gemaakt (herstart + doorgaan waar het lag), maar
"hervatbaar" gold alleen **per shot**: `render_clip.py` sloeg een shot over als het *laatste* frame bestond.
A_reveal stond op frame 34 van 120 → de hele shot begon opnieuw bij frame 1.

Gerepareerd: `scn.render.use_overwrite = False` in de full-branch, plus het nieuwste frame weggooien (dat kan
half weggeschreven zijn als het proces midden in een write stierf). Een herstart kost nu **1 frame i.p.v.
maximaal 120** (~2 uur). Geverifieerd met een losse 32×32 workbench-test: Blender rendert 1 en 3 en slaat een
bestaande 2 over. Oude versie: `_probe/render_clip_voor_hervatfix.py.bak`.
De draaiende Blender heeft de oude code nog in geheugen; de fix pakt vanaf de volgende scene.

### 3. Doorlooptijd: 30 scenes passen NIET in het venster
Gemeten met de kaart exclusief voor de run (één Blender, VRAM 7498/8192, GPU 100 %):
**64 s/frame** (intervallen 69/64/62/64 s), niet de 40 s waar de planning op stond.

    9360 frames (30 × 312)  ×  64 s  =  166 uur
    venster 4 sep 16:50 -> 10 sep     ≈  136 uur   ->  ~24 van de 30 scenes

Dus: de **23 prio-1 blokhutten passen** (≈128 u) en daarna haalt hij er nog ongeveer één van de zeven
kapschuur/overkapping-scenes. De bijstelling van 15:40 ("de hele lijst van 30 past") was te optimistisch;
de oorspronkelijke schatting zat er dichter bij. Wil Beike alle 30, dan is de knop samples of resolutie —
dat is een kwaliteitskeuze, dus die laat ik aan hem.

### 4. Toets: 30/30 scenes, 90/90 shots OK
De hertoets van de vier scenes met nieuwe crop-shots was om 16:39 nog net klaar voordat de runner stierf.
`lavendel_lavendelveld`, `lelie_ochtendnevel`, `lelie_avondkubus` en `zonnebloem_modern` halen alle drie hun
shots met **inside 1,00**. Over alle 30 scenes samen: geen enkele falende shot, dus er wordt in de full-run
niets stilzwijgend overgeslagen. `crop_in`/`crop_reveal` doen precies wat ze moesten doen.

### Wat er nu draait
`run_full_all.sh` op `jasmijn_familiemiddag`, gestart door de **watchdog** (taak `clips-v2-watchdog`) en
daarmee niet meer afhankelijk van een Claude-sessie die kan sluiten — stabieler dan de nohup van 15:28.
Sessie-waakhond: `scripts/clips_v2/_watch_session.sh` (meldt START/KLAAR/FOUT, stilstand >25 min,
>2 Blenders, Traceback in een scene-log). Niets gecommit.
