# GLB Creator — verkenning (16 jul 2026)

> Opdracht Beike: "verdiep je heel erg in deze generator en gebruik hem waar
> mogelijk — eerst goed inspecteren, dan kijken hoe we hem gaan gebruiken."
> Juiste URL: **https://glbcreator.intern.blokhutwinkel.nl/** (zónder
> streepje; de variant mét streepje is een geparkeerd Yourhosting-domein).
> Alles hieronder is read-only onderzocht; er is níets gegenereerd of
> verwijderd (genereren kost Meshy-credits).

## Wat het is

Intern tooltje: **productfoto's → AI-3D-model (GLB) op ware grootte**, via
Meshy, met een ingebouwde Claude die per productpagina de beste foto's kiest
en de maten uit maattekening + specificaties leest.

**Invoer** (3 manieren):
1. **Tuindeco-productlink** — `https://tuindeco.com/nl/detail/<hash>` (Beike:
   "tuindeco producten kan hij scrapen").
2. **Woodvision-artikelnummer** (bv. 1073990).
3. **Handmatig**: 1–4 eigen foto's (≤25 MB) + maten in cm + optionele
   materiaalbeschrijving + optionele achtergrond-verwijdering.

**Kosten** (Meshy-credits): genereren ~30 · retexture ~10 · opnieuw genereren
~30 (of Meshy-T2 snel/low-poly 5) · **gratis**: herschalen (nieuwe maten!),
simplify (minder polygonen mét texturebehoud), top/iso-PNG's, optimize
(kleinere textures), webshop-embed-snippet, onderdelen-editor.

## API (voor scripting/automatisering)

| Endpoint | Wat |
|---|---|
| `POST /api/create` `{url}` | genereer van productpagina/artikelnr → jobId |
| `POST /api/create-manual` `{name, images[], dimensionsCm, textureHint, removeBackground}` | genereer van eigen foto's |
| `GET /api/jobs/<id>` | voortgang (steps + result) |
| `POST /api/revise` `{base, mode: retexture\|regenerate\|simplify\|rescale, …}` | nieuwe versie |
| `GET /api/models` | bibliotheek (JSON) |
| `GET /output/<base>.json` | volledige metadata per model |
| `GET /output/<base>.glb` / `<base>-opt.glb` / `-top.png` / `-iso.png` | bestanden |
| `POST /api/render` `{base}` | gratis top+iso-PNG's |
| `POST /api/optimize` `{base}` | texture-verkleinde kopie |
| `POST /api/models/<base>/edit` | onderdelen-editor opslaan |
| `DELETE /api/models/<base>` | verwijderen (niet gebruiken zonder akkoord) |

Geen auth op het interne netwerk; HTTP en HTTPS werken allebei.

## Testcase: Speelhuis Sneeuwwitje (enige model in de bibliotheek, 16 jul)

- Bron: tuindeco-detailpagina; engine "multi-image" (2 vrijstaande
  productrenders gekozen, sfeer-/interieurfoto's bewust vermeden — staat
  allemaal in de metadata-`notes`).
- Maatlezing: "plattegrond geeft 152 breed en 149 diep (122+27 luifel),
  nokhoogte 170 uit specificaties" → **scaleBasis: hoogte 170 cm**.
- 30 credits gebruikt; 47,6 MB GLB + 4,3 MB "opt"-versie.

### Blender-keuring (headless, 5.1)

- **Drop-in-vriendelijk**: één root `real-size-wrapper`, één mesh, schaal in
  **meters**, rotatie 0, netjes gegrond op z=0, bbox exact = metadata.
  (Simpeler dan de tekentool-GLB's: geen cm-schaal/X-rotatie/multi-root-fix.)
- **Zwaar**: 1.466.184 driehoeken. De "opt"-variant verkleint alléén de
  textures (2048²→1024²), zelfde mesh — voor scènes met meerdere props is de
  gratis *simplify*-modus (of lokaal decimeren) nodig.
- Materiaal: 1× Principled met basecolor (sRGB), metallic-roughness +
  normal (Non-Color), alles packed. Geen ingebakken schaduwen in de
  basecolor (beter dan verwacht bij Meshy).
- **Cycles-probe** (960×720/24, AgX MHC, neutrale zon+lucht;
  `_diag/glbcreator_probe_*.png`): geometrie strak (deur, scharnieren,
  raamroedes, veranda-hekjes leesbaar). Twee materiaal-punten:
  1. het bitumen-dak wordt blauwgrijs (roughness-map te glad → lucht-
     reflectie) — fix: roughness-clamp/boost bij import;
  2. het hout leest bleker dan in de tool-viewer — deels tone-mapping-
     verschil; per scène gradeert dat weg, wel even checken.

### Belangrijkste valkuil: proporties op niet-geschaalde assen

Model 1,58 × **2,285** × 1,70 m vs catalogus 152 × **149** × 170 cm — de
diepte is ~53% te groot (Meshy raadt proporties uit de foto's; alleen de
scaleBasis-as klopt gegarandeerd). **Regel: na elke generatie de drie maten
tegen de catalogus leggen en zo nodig de gratis rescale-modus (non-uniform)
draaien.** Voor het speelhuis: rescale naar 152×149×170 vervormt de veranda
mee — acceptabel voor decor, checken per geval.

## Wat dit voor de renders betekent (voorstel, ter bespreking)

1. **Decor-props = échte producten uit het assortiment.** Loungestoelen
   (bv. Miami), picknicktafels, kachels, plantenbakken, speeltoestellen,
   pergola-meubels… van tuindeco.com in plaats van BlenderKit-lookalikes.
   Renders worden daarmee letterlijk shoppable — alles in beeld is te koop.
2. **Níet voor de hoofdproducten** (blokhutten/kappen): die blijven uit de
   tekentool (exacte geometrie); Meshy-proporties zijn daarvoor te
   onbetrouwbaar.
3. **Workflow-voorstel** per scène: propslijst → tuindeco-URLs verzamelen →
   genereren (30 cr/stuk; wie drukt op de knop: Beike of ik via API, nader
   af te spreken i.v.m. credits) → maat-check + rescale → simplify ~30% →
   materiaal-fix (roughness) → solo-probe → `assets/glbcreator/` → scène.
4. **Webshop-synergie**: elk gegenereerd model kan direct als AR-viewer op
   de productpagina (embed-snippet zit ingebouwd) — dubbel rendement per
   generatie.
5. **Stijlreeks-kansen nu al**: het bestaande Speelhuis Sneeuwwitje past 1-op-1
   in concept 3 (Speeltent-middag → wordt "Speelhuis-middag" met écht
   product); voor concept 2 (Uitslaapochtend) kan een echt loungebed/daybed
   uit het assortiment de BlenderKit-daybed vervangen.

## Openstaande vragen aan Beike

1. Hoeveel Meshy-credits zijn er (geen credits-endpoint zichtbaar) en wat
   mag een renderronde kosten?
2. Mag ik zelf via de API genereren (met een props-lijst vooraf ter
   akkoord), of wil je zelf op de knop drukken?
3. Geldt "gebruik waar mogelijk" ook voor bestaande goedgekeurde scènes
   (props vervangen door echte producten), of alleen voor nieuw werk?
