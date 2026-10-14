# Her-export 33 blokhutten uit de nieuwe tekentool (11 sep 2026)

Bron: https://tekentool.blokhutwinkel.nl/ — systeem **BHW select**, template **BHW-select**.

De handmatige route (wandlijnen slepen) is vervangen door aansturing via de
interne API van de tekentool. Dat is exact in plaats van visueel, en scheelt
33 keer handwerk.

## Hoe het werkt

De editor heeft een globale `blokhutwinkel` API en `window._2deditor` is de
levende Editor-instantie. De plattegrond is op te vragen als JSON:

```js
const b = window.blokhutwinkel;
const js = b.Serializer.serialize(b.StructureSherlock.getCurrentStructure());
```

Daarin staat alles in **millimeters**:

| onderdeel | waar | inhoud |
|---|---|---|
| hut | `floors.items[0].rooms.items[0]` | 4 wanden type `chalet` |
| luifel | `floors.items[0].rooms.items[1]` | type `canopy`, 3x `none` + 1x `invisible` |
| luifelwand | `floors.items[0].lines.items[0]` | de dichte achterwand (= `wall-7` in de GLB) |
| palen | `floors.items[0].poles.items` | op `X2 - 45,25` |
| dak | `floors.items[1].rooms.items[0]` | type `pent`, wanden type `roof` |

Anker linksboven is vast: `X0 = -900`, `Y0 = 800`. Daaruit volgt alles:

    X1 = X0 + B*10      Y1 = Y0 + D*10      X2 = X1 + L*10
    dak: x [X0-200 .. X2+200], y [Y0-150 .. Y1+200]
    palen: (X2-45,25, Y0+45,25) en (X2-45,25, Y1-45,25)

Aanpassen en terugladen:

```js
const nieuw = b.Unserializer.unserialize(js);
window._2deditor.setStructure(nieuw);
```

**Zijwand** = canopy-wand **index 1** (de buitenrand bij `x = X2`) op `chalet`
zetten. Dat geeft `wall-8`: 2 cm dik over de volle diepte. Wand index 2 (de
korte zijde bij `Y1`) is *fout* — dan komt de wand aan de voorkant te staan.

**Geen luifel** = `rooms.items[1]`, `lines.items` en `poles.items` leegmaken en
het dak tot `X1 + 200` laten lopen.

## Exporteren

Gebruik **niet** de knop "Exporteer GLB" in het informatiepaneel. Die valt soms
terug op een ander exportpad dat de hele scene dumpt: root `shed`, 573
materialen, ~92 MB, bestandsnaam `testing123.glb`.

Het goede pad is de 3D-viewer zelf:

```js
document.querySelector('iframe').contentWindow
  .blokhutwinkel3d.exporter.exportCleanGlb('Camelia 250x300 + 300');
```

Die filtert op zichtbare meshes met vertices (164 stuks; de meubelbibliotheek
`Buitenbar` valt vanzelf af), schaalt naar meters en bundelt alles onder een
node `blokhut`. Het resultaat komt als dataURL binnen via een `postMessage` naar
de parent — een **JSON-string**, met `params` op het topniveau:

```js
window.addEventListener('message', e => {
  const d = JSON.parse(e.data);           // let op: string, geen object
  if (/glbExported/.test(d.action)) { /* d.params.dataUrl */ }
});
```

## Valkuilen

- **Informatiepaneel dicht houden.** Staat het open, dan ligt het over het
  canvas en komt er geen enkele muisinteractie meer door.
- **Altijd vanaf een vers sjabloon werken.** Configureer je een model zonder
  luifel, dan is `rooms.items[1]` weg en kan het volgende model met luifel niet
  meer gebouwd worden. Leg de template-JSON eenmalig vast direct na het laden.
- **Downloads.** Zet in Chrome `chrome://settings/downloads` de optie "vragen
  waar een bestand moet worden opgeslagen" uit. Chrome hangt er `" (2)"` achter
  als de naam al bestaat; `pak_export.py` stript dat.
- De tool geeft bij het laden van de template een gele melding
  "Cannot read properties of undefined (reading 'map')" — die is onschuldig.

## Scripts

| script | doet |
|---|---|
| `scripts/pak_export.py` | haalt exports uit Downloads, keurt ze en zet ze weg |
| `scripts/pak_export.py --alles` | idem, in bulk |
| `scripts/controleer_exports.py` | meet elke GLB en vergelijkt met de naam |
| `scripts/import_tekentool_glb.py` | import in Blender, leest oud én nieuw formaat |

`pak_export.py` weigert een export met scene-root `shed`, meer dan 12
materialen of groter dan 8 MB — dat is de verkeerde exportroute.

## Wat er verandert aan het GLB-formaat

| | oud (30 apr) | nieuw |
|---|---|---|
| eenheid | centimeters | **meters** (geen 0.01-scale meer) |
| scene-root | `shed` + `camera` | `blokhut` |
| materialen | 9 (`basetexture-firstLayer-*`) | 3 (`epdm`, `luxehouse-onbehandeld`, `chrome`) |
| plankhoogte | 150 mm | 130 mm |
| plankgang | 135 mm | 109,2 mm |
| wandhoogte | ~1970 mm | 2080 mm |

Gemeten verschil per model: breedte **+3 cm** (de tool rekent de luifel nu 3 cm
ruimer), hoogte **+8 tot +11 cm**, diepte **identiek**.

De import-pipeline (`pilots/base/build_base_templates.py`) gaat nog uit van cm +
`shed` + `parentBoard-*-scaled`-nesting en moet omgezet worden naar
`scripts/import_tekentool_glb.py`.

**De plankfout is niet opgelost.** Naastgelegen wanden liggen nog steeds op een
half laagraster (4,42 vs 10,17 cm bij een gang van 10,92) en de topslag verschilt
per wand (7,08 vs 12,25). `scripts/fix_cabin_boards.py` blijft dus nodig.

## Scene-swap: de cabin in een bestaande scene vervangen

`scripts/swap_cabin_tekentool.py` wisselt alleen de geometrie; camera, licht,
tuin, props en de goedgekeurde materialen blijven staan.

```bash
blender -b <scene.blend> --python scripts/swap_cabin_tekentool.py --     --glb "source-glbs-new/2026-09-11/<model>.glb"     --draai180 --uit "<render.png>" --blend "<opslaan.blend>"
```

Wat het script doet, in deze volgorde:

1. **Deur losmaken.** De deur (`.DEURBASIC`, `.doorhandle`, `.scharnier-*`) hangt
   aan `shed`. Die verdwijnt bij de swap, dus eerst de wereldtransform
   vastzetten en de parent losknippen -- anders vliegt de deur 300 m weg.
2. **Oude cabin verwijderen, nieuwe GLB importeren.**
3. **Halve slag draaien** (`--draai180`). De export zet de luifel rechts met de
   luifelwand aan de voorkant; de scenes hebben hem links en achter. Gebruik een
   rotatie, geen spiegeling: `scale.x = -1` klapt de normalen om.
4. **Materialen per objectnaam terugzetten.** De nieuwe GLB heeft nog maar drie
   materialen; de scene kent er negen, per onderdeel ingesteld. Koppelen gaat
   daarom op objectnaam (`wall-*` -> wand, `pole*` -> palen, enzovoort).
5. **Plankfix + veranda-hoekfix** uit `fix_cabin_boards.py`.
6. **Deuropening snijden.** Zie hieronder.

### De deuropening

De tekentool snijdt de opening zelf uit de wandplanken zodra er een deur-inset
op de wand staat. BHW select heeft geen productcatalogus, dus die inset is er
niet en komt de wand dicht binnen. Het gevolg is subtiel maar meteen zichtbaar:
de ruiten in de deur lijken verdwenen, want je kijkt tegen een plank aan die
2 cm voor het glas langs loopt.

Het script snijdt de opening alsnog, op basis van de bounding box van de
bewaarde deur (151 x 190 cm). Twee valkuilen:

- `bpy.ops.mesh.primitive_cube_add(size=1)` maakt een kubus van 1x1x1. Met
  `scale = afmeting / 2` wordt het snijblok dan half zo groot. Gebruik `size=2`.
- De `FLOAT`-solver struikelt over de coplanaire plankvlakken; `EXACT` werkt.

Volgorde is belangrijk: eerst de plankfix, dan pas snijden. `align_courses()`
rekent met hele planken en deelt door nul zodra er gaten in zitten.

### Controleren

Twijfel je of iets voor of achter het glas zit, doe een raycast vanaf de camera
door het midden van de ruit (`scn.ray_cast`) en loop de hits af. Dat is
sluitend; een bounding-box-vergelijking is dat niet.
