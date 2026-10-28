# Licenties Regentuinkamer 2.0 (nagekeken 26-10-2026, fauteuils bijgewerkt 28-10-2026)

**Conclusie**
1. Alle BlenderKit-assets (royalty_free of cc_zero) en alle PolyHaven-assets (CC0) mogen in commerciële renders voor de webshop; naamsvermelding is niet nodig. Het BlenderKit-bestand zelf mag niet doorverkocht/doorgegeven worden als model (render is geen "dezelfde vorm").
2. Sinds 28-10-2026 staat er geen GLB Creator/Meshy-asset meer in de scène: de twee fauteuils zijn eigen werk (`stoel_teak.py`, script-gebouwd) met PolyHaven-teaktextuur (CC0). Het vroegere aandachtspunt (Meshy-fauteuil uit een Tuindeco-productfoto, plan niet vastgelegd) geldt alleen nog voor de oude renders in `renders\finals\_v1_meshy\`.
3. De hut komt uit de eigen tekentool (herkomst van de hut-texturen niet in de repo vastgelegd) en voor één Sketchfab-pakket (mosstenen) bestaat geen licentiebestand: dat is bewust niet gebruikt (vervangen door PH rock_moss_set).

Bronnen licentietekst (BlenderKit heet sinds 2026 "Blendkit", blenderkit.com stuurt door naar blendkit.com):
- https://www.blendkit.com/docs/licenses/ — "Everything you download is available for commercial use." / royalty free: "allows commercial use without mentioning the author" maar "doesn't allow for re-sale of the asset in the same form".
- https://www.blendkit.com/docs/licenses/licensing-faq/ — vraag "Can I sell renders and animations made with Blendkit?" Antwoord: "Yes, you can." Ook stockfoto's/mockups van gerenderde 2D-beelden: "Yes, you can do that." Scenes met BK-modellen op andere 3D-marktplaatsen: "No you can't."
- BK CC0: "reuse the works for any purposes without restriction" (zelfde licentiepagina).
- https://polyhaven.com/license — "You can use our assets for any purpose, including commercial work." Geen credit nodig.
- https://help.meshy.ai/en/articles/9992001-can-i-use-meshy-assets-commercially-license-copyright-explained en https://www.meshy.ai/pricing — betaald: "you own all assets you create with Meshy"; gratis plan: CC BY 4.0 (credit nodig).

Licentieveld per BlenderKit-ID komt uit de publieke API `https://www.blenderkit.com/api/v1/search/?query=asset_base_id:<id>` (veld `license`), vandaag opgevraagd. Detailpagina: `https://www.blenderkit.com/asset-gallery-detail/<versie-id>/` (zie tabel).

## A. BlenderKit (in de scène gebruikt volgens scripts)

| Asset | Bron | ID/pad | Licentie | Commercieel in renders? | Bron-URL |
|---|---|---|---|---|---|
| Tree Fagus Sylvatica09 (Pandora Land) | BlenderKit | caa82c72-91c1-402b-a23f-653a31fb8a60 · assets\blenderkit\renders2\Tree_Fagus_Sylvatica09.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/19721e35-d390-451e-96b2-b4ad67baccd3/ |
| European Maple Acer Campreste (Digi Motion Studio) | BlenderKit | 4c89fc98-7e5a-4362-9523-dadf6717a9bd · ...\European_Maple_Acer_Campreste.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/8a4724d0-ebe0-4c7c-92fd-dc1a0f173c71/ |
| Tree Fagus Sylvatica05 (Pandora Land) | BlenderKit | 4986c7f3-f564-4e0b-afd3-6ef0247c1055 · ...\Tree_Fagus_Sylvatica05.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/6a0bf2b9-5f8a-481d-bda6-f557f333c904/ |
| Tree Fagus Grandifolia05 (Pandora Land) | BlenderKit | 9bdd29e6-5022-4dba-911a-ec0e15bcb196 · ...\Tree_Fagus_Grandifolia05.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/3a6fd430-852f-4fb4-8bdf-828c586afe73/ |
| Cotoneaster (Alexander Novgorodtsev), haag | BlenderKit | 8d7ae4d8-cb9c-4063-96e7-8904e14124b0 · ...\Cotoneáster.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/e522a7cf-d2e9-4a3b-ae45-b178ef8b816f/ |
| Greenleaf Treeline Backdrop 001 (Levi Magony), ring 4 | BlenderKit | f93c7f44-18c8-42c2-a4c3-9c03b69aa7d5 · ...\Greenleaf_Treeline_Backdrop_001.blend | cc_zero | Ja | https://www.blenderkit.com/asset-gallery-detail/41ab2529-83e6-44e3-9800-f2ee62bcfcd2/ |
| Multi-stem Deciduous Tree (Ken Xie), statement-boom | BlenderKit | 0282c2fa-b532-4c53-89fc-d889d4f71167 · ...\Multi_stem_Deciduous_Tree.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/5f43d553-bc0f-4d3d-b9fb-147c91e8557c/ |
| Abelia grandiflora (Maxtree), oostborder | BlenderKit | 17cff3d0-8f44-4a2a-86f5-adbaacff17c3 · ...\Abelia_grandiflora.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/f756824d-925f-4076-a85b-3ccd9509f9b5/ |
| Geranium Max Frei (Alexander Novgorodtsev), oostborder | BlenderKit (lokaal, ID via naamzoek-API) | d07d9acb-2e49-4472-8d60-6589b4e6f126 · assets\blenderkit\border-planten\Geranium_Max_Frei.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/8409c65b-6054-4edb-8ae2-778d981d271b/ |
| Mown Grass Large area (Adam Krhanek), gazonbron "bk" (oude gazonvariant, nog in rtk_lib) | BlenderKit | af46ecce-d6b7-4655-b24a-972a27c1dc7f · ...\Mown_Grass_Large_area.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/de9b152f-5809-46d1-82f3-c699134c8c44/ |
| Garden Grass Free (Amanpreet Bajwa), gazonbron "tuin" (nieuw in rtk_lib, 14:58) | BlenderKit | a459e09d-fc97-4cea-ad69-1dc3e1903b81 · ...\Garden_Grass_Free.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/0c5cbe11-9dba-4271-b610-5d2dedd49a81/ |
| grass lawn cut 1x1 m (Blendkit Community), gazonbron "kort" (nieuw in rtk_lib) | BlenderKit | e89bded5-6a35-4469-8128-2556287f1d6f · ...\grass_lawn_cut_1x1_m.blend | royalty_free | Ja | https://www.blenderkit.com/asset-gallery-detail/1e5b2567-4081-4c3f-9045-361e9fedf96e/ |

## B. BlenderKit: aanwezig maar NIET in de scène (afgekeurd/gedownload zonder gebruik)

| Asset | ID/pad | Licentie | Opmerking |
|---|---|---|---|
| European Maple Acer Platanoide | 288d4b10-b252-408a-9b34-862b56f37a25 | royalty_free | afgekeurd (herfstblad), wel gedownload; stap1 laadt hem niet |
| Silver Birch Tree (Andrei Petrukovich) | 7dbc5c1a-23a3-45f0-b25c-f2c692431e7e · assets\blenderkit\berk\ | royalty_free | vervangen door Multi-stem; stap1 definieert BERK maar laadt hem niet |
| SJ-Radiant Moonlight Lavender Petals (sahra javid) | 10197d0f-05dc-47d8-a286-e39586865511 | royalty_free | in stap3 uitgecommentarieerd (v4), staat nog in de docstring |
| Grass (lawn) procedural (Ibrohim Toxirov) | 9e1d0072-5ddb-4cd1-99ff-8ffe8163ad30 | royalty_free | gedownload, niet in scripts |

## C. PolyHaven (CC0, https://polyhaven.com/license), naamscontrole via https://api.polyhaven.com/info/<naam>

| Asset | Type | Pad/ID | Licentie | Commercieel? |
|---|---|---|---|---|
| eilenriede_park_2k.hdr | HDRI | polyhaven\hdri\ · https://polyhaven.com/a/eilenriede_park | CC0 | Ja |
| grass_medium_02 (modellen/siergras, gazon "ph") | model | polyhaven\models\grass_medium_02_2k.blend · https://polyhaven.com/a/grass_medium_02 | CC0 | Ja |
| periwinkle_plant (maagdenpalm) | model | https://polyhaven.com/a/periwinkle_plant | CC0 | Ja |
| fern_02 (varen) | model | https://polyhaven.com/a/fern_02 | CC0 | Ja |
| shrub_02 (struiklaag) | model | https://polyhaven.com/a/shrub_02 | CC0 | Ja |
| rock_moss_set_02 (stenen bekken), rock_moss_set_01 (gedownload) | model | https://polyhaven.com/a/rock_moss_set_02 | CC0 | Ja |
| side_table_01 (bijzettafel) | model | https://polyhaven.com/a/side_table_01 | CC0 | Ja |
| watering_can_metal_01 (gieter) | model | https://polyhaven.com/a/watering_can_metal_01 | CC0 | Ja |
| wicker_basket_01 (mand) | model | https://polyhaven.com/a/wicker_basket_01 | CC0 | Ja |
| teak_veneer (hout fauteuils, 2k diff/rough/nor_gl, gedownload 28-10) | textuur | assets\polyhaven\textures\teak_veneer\ · https://polyhaven.com/a/teak_veneer | CC0 | Ja |
| forrest_ground_01 (bosgrond, oever) | textuur | https://polyhaven.com/a/forrest_ground_01 | CC0 | Ja |
| grey_stone_path (pad, kapvloer) | textuur | https://polyhaven.com/a/grey_stone_path | CC0 | Ja |
| brown_mud (bekkenbodem) | textuur | https://polyhaven.com/a/brown_mud | CC0 | Ja |
| leafy_grass (gazonbodem) | textuur | https://polyhaven.com/a/leafy_grass | CC0 | Ja |
| shrub_sorrel_01, flower_heliophila | model | gedownload 26-10 (nog niet in scripts; waarschijnlijk nieuwe struiken oostborder) · https://polyhaven.com/a/shrub_sorrel_01 en .../flower_heliophila | CC0 | Ja |

## D. GLB Creator (Meshy): NIET MEER GEBRUIKT sinds 28-10-2026

Vervangen door de eigen fauteuil (sectie E). Alleen de oude finals in `renders\finals\_v1_meshy\` en de reservekopie `regentuinkamer_v2_v1_meshy.blend` bevatten hem nog.

| Asset | Bron | Pad | Licentie | Commercieel in renders? | Bron-URL |
|---|---|---|---|---|---|
| (niet meer gebruikt) Teak loungeset Riverside fauteuil (2x, Zit_Fauteuil_A/B) | eigen GLB Creator, Meshy, gemaakt 17-07-2026 uit Tuindeco-productfoto (30 credits) | assets\glbcreator\teak-loungeset-riverside-fauteuil-incl-kussens-eb43e37c-opt.glb | Meshy: betaald plan = eigendom van de output; gratis plan = CC BY 4.0 (credit "Model created with Meshy"). Plan op 17-07 niet vastgelegd. | Waarschijnlijk ja, maar zie "Niet vast te stellen" | https://help.meshy.ai/en/articles/9992001-can-i-use-meshy-assets-commercially-license-copyright-explained |

docs\GLB_CREATOR_verkenning.md zegt niets over licentie of commercieel gebruik van Meshy-output; alleen over credits (30 per generatie) en techniek.

## E. Eigen werk

| Asset | Bron | Opmerking |
|---|---|---|
| Teak-loungefauteuil (2x, Zit_Fauteuil_A/B), sinds 28-10-2026 | `stoel_teak.py` (eigen script: geometrie, kussens en stofmateriaal procedureel) | hout = PH teak_veneer (CC0); verder geen externe assets |
| Hut (_hut_tekentool.blend, Cabin_Root), hutmaterialen/texturen (assets\tekentool-textures\2026-09-11: woodbeams, roofing-felt, tiles, terrace, grass3 e.d.) | eigen tekentool Blokhutwinkel | geometrie is eigen werk; herkomst/licentie van de texturen zelf niet vastgelegd in de repo |

## Niet vast te stellen / aandachtspunten

1. **Fauteuil (Meshy), alleen nog relevant voor de oude renders in `_v1_meshy`:** (a) was het Meshy-account op 17-07-2026 een betaald plan? Zo niet: CC BY 4.0, dan is een credit-regel nodig. (b) Meshy-eigendom geldt alleen als de invoer geen rechten van anderen schendt; de invoer is een Tuindeco-productfoto (sourceUrl tuindeco.com). Tuindeco is leverancier van het assortiment, maar of hun foto's als Meshy-invoer voor shopbeelden gebruikt mogen worden, staat nergens vastgelegd. De Meshy-voorwaarden (https://www.meshy.ai/terms-of-use) zelf niet volledig gelezen; alleen de FAQ/helppagina.
2. **Hut-texturen** (tekentool-textures): herkomst onbekend; waarschijnlijk eigen of uit de tekentool zelf, niet gecontroleerd.
3. **Sketchfab-mosstenenpack:** geen licentiebestand; in de scène vervangen door PH rock_moss_set, dus niet gebruikt (zie stap0b_polyhaven.py). `assets\sketchfab\` bevat CC-BY-modellen (outdoor kitchen, rolled towel; zie assets\CREDITS.md) die niet in deze scène staan.
4. **Nieuwe assets na 14:58:** een andere agent voegt gazon- (Garden Grass Free, grass lawn cut) en borderassets (PH shrub_sorrel_01, flower_heliophila) toe; stap3_borders.py was bij lezing (mtime 14:38) nog niet aangepast. Wijzigt dat nog, dan zijn nieuwe BK-IDs na te lopen met `python -X utf8 bk_lic.py` (scratchpad) of dezelfde API.
5. BlenderKit-licentie verbiedt alleen doorverkoop van de modellen zelf. Het scène-.blend (359 MB, met ingesloten BK-modellen) niet aan derden/klanten meegeven of op een modelmarktplaats zetten; renders en stills mogen wel.
6. De BK-API geeft het `license`-veld; de licentiepagina zegt over AI-training niets. Niet relevant voor renders.
