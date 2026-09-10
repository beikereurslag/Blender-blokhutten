# Plan — Zonnebloem 300x300+300+zijwand "De Zomeravond" (2026-06-12)

## 1. Concept & waarom dit origineel is
- Zonnebloem heeft een modern-strakke hero. Maar de lijn-identiteit is "Boerderij sun" — warmte en samenzijn. Dat beeld bestaat nog niet.
- **Scene-idee dat nog nooit is gedaan: het buitendiner op een zomeravond.** Een gedekte lange tafel vóór de veranda, lichtslinger tussen cabin en boom, zonsondergang, lantaarns net aan. Dit is de "samen eten in je eigen tuin"-belofte — gezelligheid als product. Persona: gezinnen/vriendengroepen die de blokhut als buitenkamer voor zomeravonden kopen.
- Onderscheid t.o.v. Dahlia-oogsttuin (zelfde boerderij-stijlfamilie): daar de *productieve* tuin overdag bij golden hour; hier het *sociale* moment op de overgang dag→avond. Onderscheid t.o.v. Jasmijn-hygge: dat was intiem rond vuur (2 stoelen); dit is de **lange tafel** — uitnodigend, feestelijk.
- Lichtmoment sunset→vroege dusk met brandende lichtslinger: nog niet gedaan (Jasmijn was dieper in de avond rond vuur; hier hangt er nog gloed in de lucht).

## 2. Model-feiten (geprobed 12 jun, `pilots/base/Zonnebloem-300x300-300-zijwand.blend`)
- Footprint **6.43 × 3.41 m**, hoogte 2.37 m, plat dak (`flatroof-67-*`).
- Deur **+Y-voorzijde**, X 0.73..2.24; veranda links, pole-0 op (−2.94, 1.43), open naar +Y.
- GLB-camera aanwezig → weg in P1. Materialen leeg → `build_clean_wood`.

## 3. Stijl & materialen (alleen echte producttextures)
Stijlbijbel: **Boerderij/landelijk**, honingwarm.
- Wanden: `assets/blokhutwinkel-textures/8192/douglas-rabat.jpg` (honingbruin — gloeit in sunset)
- Balken/palen: `douglas.jpg`
- Deur: `hardhout-deuren-ramen.jpg`
- Dak: `epdm.jpg`, rand `staalpannen-antraciet.jpg`
- Terras: klinkers `paving_stones_64` (polyhaven) warm hertint — boerenerf-gevoel
- Géén zwart, géén composiet — alles warm hout.

## 4. Scene-layout (coördinaten; cabin op origin, voorzijde +Y)
| Element | Positie | Detail |
|---|---|---|
| Grasgrond | 30×30 m | zomeravond-warm gedempt |
| Klinker-terras | X −3.2..1.5, Y 1.7..5.5 | groot — het diner-podium |
| **Lange tafel (focal)** | (−1.0, 3.4), as evenwijdig aan gevel | `dining_set_gltf` als basis; te kort? → tafelblad verlengen met douglas-planken + extra stoelen/bank (`wooden_bench_low_poly`) aanschuiven; gedekt: 4-6 borden (cilinders plat), 2 karaffen (afgeronde cilinders), lantaarn midden |
| **Lichtslinger** | van dakrand (−2.8, 1.7, 2.3) naar boom op (4.5, 5.5) en terug naar (1.5, 1.7, 2.3) — 2 spans | proceduraal: catenary-curves + emission-bolletjes (2200K, zwak) om de 0.4 m |
| Boom (slinger-anker) | (4.5, 5.5) flinke esdoorn | `maple_tree_scan` |
| Lantaarns | 2× op tafel + 1× bij deur wandhoogte 1.6 m | `old_lantern_gltf` + `wooden_lantern_01`, warm emissief |
| Klinkerpad | 0.9 m, Y 9 → recht naar deur (boerderij-regel) | zelfde klinker |
| Borders | rozen + spiraea + hortensia rechts van deur en langs terras | hoog-laag, dicht aan gesloten kant |
| Gele accenten | `flower_gazania` drifts bij borderrand (zonnebloem-knipoog — er is géén zonnebloem-asset, dus NIET verzinnen; gazania geeft het gele accent eerlijk) | |
| Heg perimeter | Y −5.5, X ±9 | GN shrub_03 1.6 m |
| Bomenringen | 3 ringen 14/18/23 m | maple/birch/pine — silhouet tegen avondlucht |

## 5. Compositie & camera
- 35 mm, 1.60 m, vanaf voor-rechts **(8.0, 9.5, 1.6)**, target (−0.5, 1.0, 1.2).
- Vanaf (+X,+Y): cabin links, lange tafel rechts-diep onder de slinger — de slinger maakt een **lichtboog over het middenvlak** die het oog van deur naar tafel leidt.
- Deur op linker power point, tafel-lantaarns op rechter power point; pad start onderin frame.
- Horizon onderste derde; avondlucht krijgt ~30% (de sunset-HDRI is hier décor).

## 6. Licht & sfeer (zonsondergang ~21:15, slinger net aan)
- HDRI: `assets/polyhaven/hdri/venice_sunset_2k.hdr` (backup: `the_sky_is_on_fire_2k.hdr` — proben welke de wand mooier gloeit zonder oranje-clipping), strength 0.7-0.9, zon-disc achter de bomenring links-achter.
- Zon: 3200K, energie 1.8, elevatie 4-6° — laatste strijklicht op de douglas-gevel.
- Praktijklicht: slinger-bolletjes (2200K, emission 4-8 W-equiv — subtiel!), tafel-lantaarns, zwak warm interieurlicht achter deurglas.
- Balans is het hele spel: lucht nog leesbaar, slinger al zichtbaar — exposure 0.2, crops op overbelichte bolletjes.
- Filmic, Medium High Contrast.

## 7. Props & asset-paden
- Tafel/stoelen: `assets/sketchfab/furniture/dining_set_gltf` + `wooden_bench_low_poly_gltf` + evt. `bistrot_table_and_chair_gltf`-stoelen mixen (geleefd, niet showroom)
- Lantaarns: `assets/sketchfab/lighting/old_lantern_gltf`, `assets/polyhaven/models/wooden_lantern_01/`
- Slinger: proceduraal (curve + array van emission-bolletjes; bewezen patroon, geen asset nodig)
- Servies: procedurele cilinders, keramiek off-white — alleen wat in close-up overtuigt
- Rozen: `assets/sketchfab/flowering_bushes/roses_gltf`; hortensia: `bigleaf_hydrangea`; spiraea: `goldmound_spiraea`
- Geel accent: `assets/polyhaven/models/flower_gazania_2k.blend` (cluster-donor fix!)
- Boom + ringen: maple_tree_scan, birch pack, pine trio

## 8. Bouwfases (headless, per fase script + save + diag 1280×720/64)
| Fase | Script | Inhoud |
|---|---|---|
| P1 | `build_zonnebloem_avond_p1.py` | GLB-cam weg, douglas-materialen, gras, sunset-HDRI+lage zon, camera |
| P1b | HDRI-keuze | 2 diags (venice vs sky_on_fire) → beste kiezen |
| P2 | `build_zonnebloem_avond_p2.py` | Heg + bomenringen + anker-esdoorn |
| P3 | `build_zonnebloem_avond_p3.py` | Klinker-terras + pad |
| P4 | `build_zonnebloem_avond_p4.py` | **Tafel + dekking + slinger + lantaarns + interieurlicht** + borders + gazania |
| P4b | inspectiecams | close-ups: tafel (GLTF-oriëntatie!), slinger-spans, deurzone, border |
| P5 | `build_zonnebloem_avond_p5.py` | validate + audit + licht-balans-polish + 1080p preview |
| P6+ | fixes na feedback → finale | |

## 9. Risico's & fallbacks
- **Dining_set-kwaliteit/schaal onbekend** → P4b verplicht; tegenvallend = picknicktafel-aanpak (bewezen in Dahlia) met banken, dekking maakt het feestelijk.
- **Slinger-doorhang**: catenary netjes berekenen (niet strak gespannen = amateur-tell); bolletjes-emissie laag beginnen — overstraalde bollen verpesten avondrenders, crops checken.
- **Sunset-HDRI's zijn geen puresky** (venice/sky_on_fire hebben omgeving in reflecties) → glas-reflecties checken in crop; storend = HDRI alleen als achtergrond/licht en glas-roughness iets op.
- **Te donker totaal** → eerst praktijklichten op, dán pas HDRI-strength; de gevel moet douglas-warm blijven, niet zwart.
- Servies druk in beeld → minder is meer, 4 borden max.

## 10. Validatie & render-trap
- Audit per fase; anti-empty checklist (pad→deur recht, heg + boomwand, meubel = de tafel).
- Extra avond-check: geen pure zwarte vlakken >10% van frame (full-res crops onderkant frame).
- Preview 1080p/160 → user-akkoord → finale 2560×1440/240 (playbook-instellingen).

## Output
`pilots/Zonnebloem-300x300-300-zijwand/style-boerderij/zonnebloem_zomeravond.blend` (nieuwe stijlmap) + diag PNGs.
