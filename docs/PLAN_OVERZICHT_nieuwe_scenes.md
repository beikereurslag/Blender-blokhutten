# Overzicht — 8 nieuwe hero-scenes, één per cabin-lijn (2026-06-12)

Elke cabin-lijn in `pilots/` krijgt een nieuwe scene met een **nog niet gebruikt scene-idee** (originaliteitsregel). Reeds gedaan en dus vermeden: scandi-forest (Camelia), English cottage (Lelie), modern strak ×2 (Lavendel, Zonnebloem), modern Japandi (Magnolia), mediterraan-warm terras (Roosmarijn), hygge-avondvuur (Jasmijn), boerderij-oogsttuin (Dahlia).

Alle 8 base-blends zijn geprobed (`scripts/probe_all_bases.py`, output in `scripts/probe_all_bases_OUTPUT.txt`): consistente familie — deur +Y-voorzijde, gesloten deel rechts (+X), open veranda links (−X), plat dak, GLB-restcamera, lege `basetexture-firstLayer-*` materialen. Uitzondering: Magnolia (geen veranda, deur gecentreerd, 3.46×2.41 m).

| # | Cabin | Scene | Stijl | Lichtmoment | Plan |
|---|---|---|---|---|---|
| 1 | Camelia 250x300+300+zijwand | **Het Buitenbad** — wellness/dompelbad | scandi-spa | blue hour + lantaarns | `PLAN_camelia_buitenbad.md` |
| 2 | Dahlia 250x250+300+zijwand | **Het Tuinkantoor** — werken vanuit de tuin, fiets + bureau | modern-urban-cottage | frisse ochtend 08:30 | `PLAN_dahlia_tuinkantoor.md` |
| 3 | Jasmijn 300x250+300+zijwand | **De Familietuin** — speelgazon, picknicktafel, zandbak | klassiek-familie | zomermiddag, licht bewolkt | `PLAN_jasmijn_familietuin.md` |
| 4 | Lavendel 400x300+400+zijwand | **Het Lavendelveld** — Provence-rijen als leading lines | mediterraan | golden hour avond | `PLAN_lavendel_lavendelveld.md` |
| 5 | Lelie 400x250+300+zijwand | **De Ochtendnevel** — wildflower-meadow + volumetrische mist | forest-wilderness | dageraad 06:15 | `PLAN_lelie_ochtendnevel.md` |
| 6 | Magnolia 300x200 | **De Groene Long** — sedum-dak, zonnepaneel, regenton, wadi | eco-groendak | helder voorjaar 10:00 | `PLAN_magnolia_groendak.md` |
| 7 | Roosmarijn 200x300+400+zijwand | **De Zentuin** — karesansui, mos, tsukubai, engawa | japanese-zen | zacht bewolkt | `PLAN_roosmarijn_zentuin.md` |
| 8 | Zonnebloem 300x300+300+zijwand | **De Zomeravond** — gedekte lange tafel + lichtslinger | boerderij | sunset 21:15 | `PLAN_zonnebloem_zomeravond.md` |

## Spreiding (bewust)
- **Licht**: dageraad-mist / ochtend / middag / golden hour / sunset / blue hour / overcast / helder — geen twee scenes delen een lichtmoment.
- **Verhaal**: wellness, werken, gezin, veld, natuur, duurzaamheid, contemplatie, samenzijn — elke scene verkoopt een ándere reden om deze blokhut te kopen.
- **Techniek-primeurs**: volumetrische mist (Lelie), dak-feature (Magnolia), harkpatroon-displacement (Roosmarijn), waterreflectie (Camelia), lichtslinger + tafellandschap (Zonnebloem), veld-rijen (Lavendel), interieur-doorkijk (Dahlia).

## Gedeelde werkwijze (alle 8)
Per Cabin Hero Build Playbook: gefaseerde headless scripts (build → save → diag 1280×720/64) → full-res crops → numeriek proben bij twijfel → P4b prop-inspectiecams → validate + audit → 1080p/160 preview → **user-akkoord** → finale 2560×1440/240. Alleen echte Blokhutwinkel-producttextures (`assets/blokhutwinkel-textures/8192/`), GN-heg via shrub_03, GLTF-bomen (nooit USD), cluster-donor fix bij polyhaven multi-variant blends.

## Voorgestelde bouwvolgorde
1. **Zonnebloem Zomeravond** (laagste techniek-risico, bewezen patronen + slinger)
2. **Dahlia Tuinkantoor** (klein risico: alleen fiets-GLB nieuw)
3. **Jasmijn Familietuin** (zandbak proceduraal, rest bewezen)
4. **Lavendel Lavendelveld** (veld-schaal proben)
5. **Roosmarijn Zentuin** (displacement-experiment)
6. **Camelia Buitenbad** (proceduraal bad + water + avond)
7. **Magnolia Groene Long** (dak-scatter + camera-uitzondering)
8. **Lelie Ochtendnevel** (volumetrie = zwaarste, alle lessen meenemen)
