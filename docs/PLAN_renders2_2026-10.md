# Renders 2.0 — plan pilot De Regentuinkamer (26-10-2026)

Opgesteld door de architect-agent, nagelopen en vastgelegd door de projectsessie Renders 2.0.

Invoer: `docs/renders2_fase0_2026-10.md` (stand), `docs/PLAN_astra_garden.md` (goedgekeurd ontwerp en
coördinaten; blijft het ontwerp), `pilots/ai_omgeving_2026-10/contactvel.png` (rechterbeeld = referentie
voor bomen en haag). Dit plan gaat over de **ankerfase** en schetst de lagen daarna. Pas na Beikes akkoord
op de pilot volgen de andere 22 scènes.

## 1. Doel en wat er bewust niet gebeurt

Doel: de Regentuinkamer opnieuw bouwen als één echte 3D-tuin, rondom af, zodat elke camerahoek en een
filmpje kloppen. De zwakke plekken van de oude scène (kale bomen, herhalend haagpatroon, ijle boomrand,
egaal gras, vlak pad, vlakke zon) krijgen andere assets en een andere opzet, geen bijwerking.

Bewust niet:
- De oude blends (`pilots/G1-.../regentuinkamer_G1*.blend`) en `pilots/base/*.blend` nooit opslaan. Ze dienen
  alleen als bron (deur, greep, fundering via de swap-route).
- Geen ComfyUI-overpaint. Geen ComfyUI-texturen in het anker: SDXL maakt zonder tegel-node geen naadloze
  tegels en levert geen normal-/roughness-maps; een node installeren is een nieuwe afhankelijkheid. Pas
  terug op tafel als een PolyHaven/BlenderKit-textuur aantoonbaar tekortschiet.
- `scripts/cabin_lib.py`, `grass_lib.py`, `validate_scene.py` en `hoektest.py` niet wijzigen (cabin_lib heeft
  al niet-gecommitte wijzigingen van anderen). Nieuwe helpers komen in de scènemap.
- Geen AI-3D en geen geld uitgeven (zie vraag 1). Geen nieuwe pip-pakketten.
- Geen camerarit of film, geen finals, geen andere scènes. Dat zijn latere fases.
- Niets committen. Geen `git add .`: de map staat vol untracked blends van samen ~68 GB.

## 2. Bestandsopzet

Map `D:\Blender-blokhutten\scenes\regentuinkamer_v2\`:

| Bestand | Wat |
|---|---|
| `rtk_lib.py` | helpers voor deze scène: bodemmesh met bekken, BK-boom plaatsen, haagmodule plaatsen, schaduwtoets, luchttoets, eigen audit |
| `stap0_assets.ps1` | draait `pilots\_bk_fetch.py` één keer per asset-ID (lijst in §3) en downloadt de PH-textuur |
| `_hut_tekentool.blend` | uitvoer van de swap (hut alleen, op de oude base-plek) |
| `stap1_anker.py` | opent `_hut_tekentool.blend` → schrijft `regentuinkamer_v2_anker.blend` + previews |
| `stap2_bekken.py` … `stap5_details.py` | latere lagen: openen de vorige blend en schrijven een eigen blend |
| `regentuinkamer_v2.blend` | eindbestand, geschreven door de laatst goedgekeurde stap |
| `previews\anker\`, `previews\dressing\` | wat Beike op de review-site ziet |
| `previews\_werk\<fase>_<versie>\` | crops, hoektest, `audit.json` (eigen QC) |
| `review\review_server.py` | **staat er al**: kopie van `overkappingen-website\review_server.py`, poort **8767**, leest `previews\anker` en `previews\dressing`, keuzes in `review\review_keuzes.json` (getest 26-10) |
| `logs\` | één log per run (`stap1_v1.log`, ...) |

Regels voor elk stap-script:
- **Herhaalbaar.** Opent altijd zijn eigen invoerbestand, vaste seeds, eigen uitvoernaam.
- **Crash-veilig.** Pas aan het eind opslaan (`save_as_mainfile`), daarna renderen.
- Versienummer via omgevingsvariabele `RTK_VERSIE`.

Hergebruik uit `scripts/cabin_lib.py` (`import cabin_lib as cl`): `delete_glb_cameras`, `wbbox_meshes`,
`warm_wood_walls`, `fix_glass_chrome`, `pbr_from_folder`, `ribbon_path`, `load_asset_clusters`,
`place_cluster`, `ground_root`, `import_gltf_prop`, `add_sun`, `setup_hdri`, `_kelvin_rgb`,
`volumetric_fog`, `add_camera`, `set_camera_dof`, `render_setup`, `set_agx`, `audit`,
`fix_broken_image_materials`, `inspect_cams`. Verder `validate_scene.run/print_report`, en
`swap_cabin_tekentool.py` en `hoektest.py` als CLI.

Niet hergebruiken: `build_hedge_system`, `pine_rings` en `grass_lib.add_grass`: precies de afgekeurde haag,
dennen en het egale gras.

## 3. Assets per onderdeel

Volgorde van bronnen: lokaal → BlenderKit (gratis) → PolyHaven (CC0) → AI-3D (alleen na akkoord).
Licentie BlenderKit "royalty_free": gebruik in commerciële renders mag, het bestand zelf niet doorgeven
(vóór de finals de licentietekst op blenderkit.com nalezen). Kosten: alles hieronder €0. Downloaden met
`blender -b --python pilots\_bk_fetch.py -- "asset_base_id:<id>" renders2` (gecontroleerd: precies één
resultaat, `canDownload=True`). Nog niets bekeken, dus alles is **toetsen in het anker**.

| Onderdeel | Kandidaat (bron, maat) | Waarom | Terugval |
|---|---|---|---|
| Boomrand ring 1 (2–8 m buiten de haag) | BK **Tree Fagus Sylvatica09** `caa82c72-91c1-402b-a23f-653a31fb8a60` (12,4 m); BK **European Maple Acer Campreste** `4c89fc98-7e5a-4362-9523-dadf6717a9bd` (15,2 m) | Europese beuk en veldesdoorn: volle kruin, past bij het referentiebeeld | lokaal `assets/blenderkit/berk/Silver_Birch_Tree.blend` |
| Ring 2 (15–30 m) | BK **Tree Fagus Sylvatica05** `4986c7f3-f564-4e0b-afd3-6ef0247c1055` (18,9 m); BK **Tree Fagus Grandifolia05** `9bdd29e6-5022-4dba-911a-ec0e15bcb196` (15,6 m); BK **European Maple Acer Platanoide** `288d4b10-b252-408a-9b34-862b56f37a25` (13,3 m) | volwassen silhouet dat de lucht afsluit | ring 1-assets op schaal 0,9–1,1 |
| Ring 3 (35–70 m) | dezelfde vijf, als instances | sluit de horizon | — |
| Ring 4 (>80 m), alleen als de luchttoets faalt | BK **Greenleaf Treeline Backdrop 001** `f93c7f44-18c8-42c2-a4c3-9c03b69aa7d5` (kaart 31×5 m) | op >80 m geen zichtbare parallax | — |
| Statement-boom westhoek (X 0,8–2,5, Y 6,5–10,5) | lokaal `assets/blenderkit/berk/Silver_Birch_Tree.blend` | ontwerp wil een berk | BK **Multi-stem Deciduous Tree** `0282c2fa-b532-4c53-89fc-d889d4f71167` (9 m) |
| Haag | BK **Cotoneáster** `8d7ae4d8-cb9c-4063-96e7-8904e14124b0` (module 7,5×1,3×1,6 m, eigen donkere kern) | zie §4 | eigen GN-haag, verbeterd (§4) |
| Gazon | BK **Mown Grass Large area** `af46ecce-d6b7-4655-b24a-972a27c1dc7f`: sprieten als donor in een eigen GN-scatter | echt gemaaid gras i.p.v. laagpoly-pluimen | PH `grass_medium_02_2k.blend` (lokaal) op 8–12 cm |
| Grond onder gras/bedden | PH `forrest_ground_01` (lokaal, met disp) | heeft een hoogtekaart | PH `leafy_grass` (lokaal) |
| Pad + terras-schort | één doorlopend vlak (§7) met PH **grey_stone_path** (CC0, downloaden) | echte stenen met voegen en reliëf | lokaal PH `slate_floor_02`; daarna BK **Stone pavment** `009f256d-078b-4e4e-8846-4abf17c58517` langs een curve |
| Bekken + water (laag 2) | bodem `forrest_ground_01` + PH `brown_mud`; rand met stenen uit `assets/sketchfab/path_stones/mossy_stones_pack_*` (licentie nalopen) | — | lokaal BK `stapstenen/Scan_Floor_Old_Step_Stone.blend` |
| Borders (laag 3) | BK **Abelia grandiflora** `17cff3d0-8f44-4a2a-86f5-adbaacff17c3` (witte bloei); lokaal BK `Geranium_Max_Frei`, PH `fern_02`, `periwinkle_plant`, `grass_medium_02` | palet wit/lichtviolet, in drifts | lokaal BK `lavendel/` |
| Meubels (laag 4) | lokaal GLB Creator teak-fauteuil ×2 en Tambora-bijzettafel | echte producten | — |
| Lucht | lokaal `assets/polyhaven/hdri/kloppenheim_06_puresky_2k.hdr` (CC0, pure sky, weinig contrast) | nooit HDRI-grond in beeld; zonlamp bepaalt de schaduw | `kloofendal_48d_partly_cloudy_puresky_2k.hdr` (lokaal; sterker dimmen) |

**AI-3D, eerlijk ingeschat.** AI-3D is zwak in bomen en hagen: klonterige kruinen, geen losse bladeren,
geen alpha. Voor de omgeving dus niet. Het kan helpen bij één los voorwerp dat nergens te vinden is, alleen
in de dressing. Kosten ~$0,40–0,60 per model; GLB Creator heeft vermoedelijk nog ruim 2.000 credits, de
sleutel van 3D AI Studio is verlopen.

Boomschaal altijd 0,8–1,1, nooit 2–3× opgeschaald. Elke unieke boom-mesh één keer in het geheugen;
plaatsingen delen hun mesh-data.

## 4. Haag en boomrand

**Haag: de BK Cotoneáster-module.** Gemodelleerde haag met kleine echte bladeren en een eigen donkere
kern: leest als geschoren haag zonder het patroon van één herhaald takje.

- Rughaag: 2 modules (Y 11,4–12,4, hoogte 1,8 m via schaal-Z 1,12).
- Zijhagen: 1,5 module per kant (X 0–1,0 en 13,0–14,0).
- Voorhaag 0,65 m: module op schaal 0,45, opening X 7,3–8,7.
- Modules 0,5–1 m in elkaar schuiven, om en om 180° gedraaid en gespiegeld: geen naad of herhaling in beeld.
- Diepte ~1,0 m (schaal-Y 0,75); achter de hut blijft 0,7 m vrij.
- Rode bessen verbergen of het bladmateriaal geven: passen niet bij het witte/violette palet.

Proef in het anker: één crop 960×540 van de rughaag op ~6 m, naast het referentiebeeld. Goed als: geen
herhalend motief, strakke bovenkant met licht afgeronde randen, holtes donker maar niet zwart, en de
voorhaag op 0,45 oogt niet als plastic. Faalt de proef: eigen GN-haag in `rtk_lib` (basisvolume met
Displace noise 0,4 m / 3–4 cm; `shrub_03`-takje verkleind naar 0,10 m, Poisson ~3000/m²; ±8% kleurwaarde
per instance, `Distribute.Rotation`).

**Boomrand.** Drie ringen, een vierde alleen als reserve.
- Ring 1: N, W, NO en Z, 2–8 m buiten de haag. Ring 2: 15–30 m. Ring 3: 35–70 m.
- Groepjes van 2–3, Poisson-afstand 6–9 m met jitter. Nooit een rechte rij.
- Achter de hut (X 7–13) geen kruin die precies op de daklijn zit: in de HeroCam óf duidelijk hoger óf
  ≥ 9 m verder naar achter.
- In de zonsector (§5) geen boom dichter dan 2,1 × zijn hoogte bij de tuin.

**Luchttoets in code** (`rtk_lib.sky_closure`, geen videokaart): stralen vanaf de HeroCam en vanaf het
tuinmidden (7, 6, 1,6), rondom per 2°, op 0°, 3° en 6° boven de horizon. Eis ≥ 95% raakt boom of haag.
Gaten (azimut, hoogte) naar `audit.json`.

## 5. Licht

- **Zon:** kompas 115° (oostzuidoost: ochtend na de bui, zoals het ontwerp). De HeroCam kijkt naar kompas
  ~8°, recht achter de camera is 188°: de zon staat 73° opzij. In de cl-conventie (azimut 0 = zon in het
  zuiden, positief = naar oost; `rotation_euler=(90-elev, 0, azim)`) is dat **`SUN_AZ = 65`**.
- **Hoogte 26°**: schaduw 2,05× de objecthoogte (bij de oude 16° was dat 3,5×).
- Kleur 4500 K, sterkte 4,0, hoek 1,2°.
- De hut werpt een schaduw naar het westnoordwesten, links naast de hut in de HeroCam: de strook die in de
  oude final goed werkte.
- **HDRI:** `kloppenheim_06_puresky_2k.hdr`, sterkte 0,8. HDRI-zon automatisch op de zonlamp uitlijnen
  (helderste pixel; werkwijze uit de oude `regentuinkamer_stap1_anker.py` r.229–247). Gemeten HDRI-zonhoogte
  loggen; boven 40° de sterkte naar 0,6.
- **Kleurweergave:** `cl.render_setup(...)` zet standaard Filmic; daarom direct daarna
  `cl.set_agx('AgX - Medium High Contrast', exposure=0.0)` en `scene.view_settings.look` loggen
  (`set_agx` valt stil terug als een naam niet bestaat).
- **Waas:** `cl.volumetric_fog` begrensd (X −40..55, Y −40..55, Z 0..25), dichtheid 0,0012.
- **Schaduwtoets in code** (`rtk_lib.shadow_test`): raster 0,5 m over X 0–14, Y 0–12 zonder hut en haagvoet;
  per punt een straal naar de zon, blokkeerder ingedeeld als hut/haag/boom. Eis: boomschaduw ≤ 20% van de
  punten, hutschaduw > 0 ten westen van X 7,3. Faalt de toets: boom verplaatsen, nooit schaduw uitzetten.

## 6. Camera's

- **HeroCam:** (8,0, 0,7, 1,55) → doel (9,028, 8,0, 1,2): 33 mm, shift_y −0,03, f/5.6, focus op de deur.
  Benadert het heldenbeeld van de oude final. Preview 960×540.
- **Cam_Bekken:** (12,8, 6,2, 1,6) → (3,5, 2,5, 0,8), 28 mm: over het bekken naar entree, voorhaag, zuidbomen.
- **Cam_Westhoek:** (1,5, 1,2, 1,6) → (10,0, 9,2, 1,4), 30 mm: diagonaal naar hut en kap.
- **Hoektest:** `blender -b regentuinkamer_v2_anker.blend --python scripts\hoektest.py -- --out
  previews\_werk\anker_<v>\hoektest --target 7.0,4.3,1.0 --radius 3.5 --height 1.65 --count 12 --res 960x540`.
  Hoektest slaat niet op.

## 7. Fases

**Fase anker (stap 0 + 1). Beike krijgt te zien:** 3 previews (HeroCam, Cam_Bekken, Cam_Westhoek) op
960×540/24 met denoise; de haagproef-crop naast het referentiebeeld; een contactvel met de 12
hoektest-beelden; één regel met de toetsuitkomsten.

Inhoud van het anker:
- **Hut:** tekentool-GLB via de swap.
- **Grond:** bodemmesh met bekkenkuil (functies `basin_n`/`basin_depth` en raster uit de oude stap1):
  bekken X 2,8–6,7 / Y 2,8–7,8, max 0,12 m; `Ground_Far` (900 m) op −0,14 met grond onder de bomen.
- **Gazon.**
- **Lege borderbedden** als grondvlak met strakke rand; voor Beike benoemd als "nog te beplanten".
- **Pad + schort als één mesh** `Route_Steen`: middenlijn (8,0)→(8,0,1,5)→(7,7,3,5)→(9,028,5,8)→ deur;
  stopt op de gemeten deurvoorkant; laatste 2,2 m recht; 1,2 m breed; schort X 7,5–13,1 / Y 6,6–8,1;
  bovenkant 5 mm onder de dorpel; 6 cm dik met afgeronde rand; Displace 1–1,5 cm uit de disp-map; gras
  loopt 3–5 cm over de rand.
- **Hagen, boomringen 1–3, statement-berk, licht, camera's.**

Namen: `Route_Steen` (niet "Pad_": telt in validate_scene als meubel), `Haag_*`, `Boom_*`, `Gazon`.

**Daarna, elk na akkoord, één zone per keer:**
- **Laag 2, bekken + water:** IOR 1,33, roughness 0,02, donkere bodem; twee plassen, natte stenen rand,
  natte voegen alleen in het lage deel.
- **Laag 3, borders:** oostborder in drie in elkaar grijpende drifts, westrand met accenten 0,9–1,2 m,
  schaduwhoek met varens.
- **Laag 4, kap + meubels:** 2 fauteuils + tafel onder de kap, X 11,4–12,6 / Y 8,6–9,5.
- **Laag 5, details.**

Per laag: dezelfde 3 camera's + crops van de nieuwe zone + hoektest.

**Controle per fase, vóór iets naar Beike gaat:**
1. `validate_scene.print_report(run())` en `cl.audit(...)` met het gemeten gesloten deel.
2. Eigen audit: niets in het gesloten-ruimtevolume; niets zwevend (> 5 cm, raycast omlaag); boomoorsprong
   z≈0; boomschaal binnen 0,8–1,1; geen ontbrekende texturen; geen grassprieten op `Route_Steen`.
3. Luchttoets en schaduwtoets.
4. Uitkomst in `audit.json`; bij een fout een bruikbare melding en exitcode ≠ 0.
5. Crop-QC op volle grootte: haagtop, boomrand tegen de lucht, pad–dorpel, schaduwstrook links van de hut,
   grasrand. Zelf bekijken.
6. Hoektest-contactvel zelf bekijken.
7. Pas daarna naar `previews\anker\` (review-site) en Telegram via `D:\Blender-blokhutten\notify.ps1`.

**Videokaart:** één job tegelijk. Vóór elke render `nvidia-smi` en `D:\Beeldherkenning\GPU_BEZET.txt`
controleren; bestaat het bestand en is het niet van ons, wachten. Tijdens eigen renders het bestand zelf
neerzetten (wie, begin, verwachte eindtijd) en daarna weghalen. Geheugenpiek uit de Cycles-log in
`audit.json`; grens 6,5 GB.

## 8. Wat kan misgaan (opdracht voor de tester)

1. **Hut niet op de ontwerpplek of verkeerd om** (tekentool-maten wijken af; `--draai180` plus de
   Cabin_Root-draaiing). Merkbaar: deurmidden ≠ 9,028 ± 0,05, deurvoorkant ≠ 8,0 ± 0,08, palen niet ten
   oosten (X > 11). Het script moet dan **stoppen**. `logs\swap_verslag.json` nalopen: deur aanwezig,
   fundering bewaard, plankfix toegepast.
2. **BK-assets vallen tegen of passen niet in 8 GB:** bessen of naden in de haag; kale delen in de beuken
   (<50.000 vertices = weigeren); te hoge geheugenpiek; download faalt omdat de BlenderKit-token verlopen is
   (dan moet Beike één keer inloggen in de BlenderKit-add-on; tot die tijd lokale terugval).
3. **Lange boomschaduw of gat in de boomrand:** schaduwtoets > 20%, luchttoets < 95%, of lucht tussen de
   stammen in een hoektestbeeld. Negatieve test verplicht: één boom bewust in de zonsector → schaduwtoets
   moet falen; één boom uit ring 1 weg → luchttoets moet falen. Ook: pad steekt niet de hut in, geen gras
   op het pad.

## 9. Open vragen voor Beike (met advies)

1. **Geld aan AI-3D?** Advies: nu niet. Het anker heeft het niet nodig en AI-3D is zwak in bomen en hagen.
   Hooguit later 1–3 losse voorwerpen in de dressing met de bestaande GLB Creator-credits (~$0,40–0,60 per
   stuk). De sleutel van 3D AI Studio vernieuwen hoeft niet.
2. **Haagsoort:** de BK-haag is cotoneaster (kleine glanzende blaadjes); het referentiebeeld lijkt meer op
   beuk of liguster. Advies: accepteren als de crop leest als geschoren haag; een gratis beukenhaag bestaat
   niet op BlenderKit, dan wordt het de eigen GN-haag.
3. **Lichtmoment:** ochtend met zon uit het zuidoosten (ontwerp "na de bui", schaduw links naast de hut) of
   late middag uit het zuidwesten (warmer, schaduw onder de kap). Advies: ochtend uit het zuidoosten.

## 10. Schatting

- **Ankerrun:** opbouw ~5–10 min processor; 3 previews ~1–2 min per stuk; haagproef ~1 min; hoektest
  12 × ~1 min. Samen ~20–25 min videokaart per ronde; 3–4 rondes ~1,5 uur.
- **Dressing:** 4 lagen × ~2 rondes × ~15 min ≈ 2 uur. **Pilot tot akkoord:** ~3,5–4 uur videokaart.
- Geschat uit de AI-proef, niet gemeten; de eerste ankerrun meet het echt.
- **Geld:** €0.

## 11. Voor Beike

De tuin rond de Jasmijn wordt opnieuw opgebouwd in Blender, niet meer per foto bijgewerkt. Daardoor klopt
hij vanuit elke hoek en straks ook in een filmpje. De hut is precies het product uit de tekentool. Bomen en
haag komen uit kant-en-klare, gratis modellen van echte Europese beuken en esdoorns en een gemodelleerde
haag, in plaats van uitvergrote of herhaalde blaadjes. Je krijgt eerst alleen het "anker": hut, gazon, pad,
hagen, bomenrand en licht, vanuit drie standpunten plus twaalf controlebeelden rondom. De zon komt schuin
van opzij, zodat de hut een zichtbare schaduw werpt, en de computer controleert zelf dat bomen geen schaduw
over de hele tuin gooien en dat er geen lucht tussen de bomen doorkijkt. Risico: de gratis modellen kunnen
van dichtbij tegenvallen of te zwaar zijn voor de videokaart; dan valt het plan terug op een eigen haag en
andere bomen. Er wordt geen geld uitgegeven.

## Bouwvolgorde voor de coder (fase anker)

1. Mappen staan er al (`previews\`, `review\`, `logs\`). Niets in `pilots\` of `scripts\` wijzigen.
2. `stap0_assets.ps1`: per ID uit §3 (5 bomen, Cotoneáster, Mown Grass, reserve Treeline, Multi-stem)
   `blender -b --python pilots\_bk_fetch.py -- "asset_base_id:<id>" renders2`; PH `grey_stone_path` 2k
   (diff/rough/nor_gl/disp) naar `assets\polyhaven\textures\grey_stone_path\` (URL's via
   `https://api.polyhaven.com/files/grey_stone_path`). Loggen; faalt een download: stoppen en melden.
3. Hut: `blender -b pilots\base\Jasmijn-300x250-250.blend --python scripts\swap_cabin_tekentool.py -- --glb
   "source-glbs-new\2026-09-11\Jasmijn 300x250 + 250.glb" --draai180 --geen-render --uit
   scenes\regentuinkamer_v2\logs\swap_dummy.png --blend scenes\regentuinkamer_v2\_hut_tekentool.blend
   --verslag scenes\regentuinkamer_v2\logs\swap_verslag.json`. Daarna `swap_verslag.json` nalezen.
4. `rtk_lib.py`: `make_ground`, `place_bk_tree` (weigerregel <50k vertices), `place_hedge_modules`,
   `shadow_test`, `sky_closure`, `audit_extra` (elk geeft een dict voor `audit.json`).
5. `stap1_anker.py` deel A, hut: openen, GLB-camera's weg, `warm_wood_walls`, `fix_glass_chrome`,
   deurpanelen naar het wandmateriaal; Cabin_Root 180° en naar (10,263, 9,25, 0); deur, palen en envelop
   meten met harde stop buiten de toleranties uit §8.1.
6. Deel B: grond, `Ground_Far`, lege borderbedden.
7. Deel C: `Route_Steen` als één mesh, displacement, materiaal via `cl.pbr_from_folder`.
8. Deel D: hagen en de haagproef-camera.
9. Deel E: boomringen 1–3 + berk, vaste seed, zonsector vrij.
10. Deel F: zon, HDRI-uitlijning, waas, `render_setup(24, (960,540))` + `set_agx`, loggen wat er echt staat.
11. Deel G: camera's HeroCam, Cam_Bekken, Cam_Westhoek.
12. Deel H, gazon als laatste: GN-scatter met de Mown Grass-donor, vrij van route + 0,15 m, bekkenkern,
    bedden en haagvoet.
13. Toetsen (validate_scene, cl.audit, audit_extra, schaduw, lucht). Bij een fout: niet opslaan, exitcode 1
    met reden.
14. Opslaan als `regentuinkamer_v2_anker.blend`; haagproef-crop + 3 previews renderen (één GPU-job,
    bezet-controle vooraf), geheugenpiek loggen.
15. Hoektest met de parameters uit §6; contactvel van 12 beelden (PIL); crops nalopen volgens §7.
16. Review-site bijvullen, Telegram via `notify.ps1`. Wachten op Beike. Niets committen.
