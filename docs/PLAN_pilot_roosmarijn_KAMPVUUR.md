# PLAN — Roosmarijn 200×300 + 400-kap "Kampvuuravond" (vervangt kruidenterras)

> Nieuw concept, 8 jul. Het kruidenterras strandde op een ziek-geel
> mosveld, zwevende tegels en een verhaal dat niet uit de verf kwam.
> Deze vervanger kiest een heel andere, fotogenieke tuin: een **vuurkuil
> met boomstambanken in de schemering** — de Roosmarijn met zijn lange
> 400-overkapping wordt het basecamp (houtopslag + schuilplek), het vuur
> is de emotie. Geen enkele andere pilot heeft vuur; dit vult het gat
> tussen de dag-scènes en de avondkubus.

## Verhaal in één zin
Blauwe-uur avond: een knapperend kampvuur in een keienkring, twee
boomstambanken met plaids en marshmallow-stokken, en achter het vuur de
Roosmarijn waarvan de overkapping vol brandhout ligt en warm oplicht.

## Basis
- **Map (nieuw):** `pilots/Roosmarijn-200x300-400-zijwand/style-kampvuur/`
  — start vanaf `roosmarijn_kruidenterras`-blend (product staat er goed
  in); ALLE terrein/tegels/potten strippen tot kaal gazon + heg.
- **Moment:** blue hour. Koele HDRI (venice_sunset of kloofendal-schemer,
  strength 0.5) + zon NET onder: geen sun, de practicals dragen het beeld
  (het M2/B-recept: koele omgeving, warme kern).
- **Camera:** 35 mm, 1.5 m, het VUUR in de voorgrond-onderderde als
  warmtebron, cabin daarachter op de linker derde-lijn, 3/4. De kijklijn:
  vuur → banken → verlichte overkapping.

## Anker (stap 1 — eerst akkoord vragen)
1. **Vuurkuil:** ring van 10-12 veldkeien (Ø 1.1 m) op een cirkel van
   aangestampte aarde/grind (Ø 2.2 m, 1 cm verzonken, gras-mask) op
   ~3.5 m vóór de cabin-opening.
2. **Zitkring:** 2 halve boomstammen (Ø 0.35, L 1.6 m, schors-textuur)
   haaks op elkaar rond de kuil + 1 losse stronk als bijzettafel.
3. **Pad:** platgetreden gras-strook (density-mask, GEEN tegels) van de
   kuil naar de overkapping — boskamp-gevoel, geen aangelegde tuin.
4. **Cabin:** wanden zoals ze zijn; onder de 400-kap alvast de zonering
   bepalen: 2/3 houtopslag, 1/3 schuil-zitje.
5. Heg + extra donkere boomring erachter (avond-silhouet, horizon dicht).

## Dressing (stap 2 — na anker-akkoord)
- **Het vuur:** stapeltje brandende blokken — vlam als 2-3 gekruiste
  emission-planes (flame-textuur met alpha, 1800K-oranje, strength 8)
  + gloeiende sintels (emission-puntjes in de askern) + warme point
  light (1600K, radius 0.15, ~80 W) 0.4 m boven de kuil als lichtbron
  + BEGRENSDE rook-cube (density 0.08, licht grijs) die schuin wegdrijft.
  GEEN simulatie — stills hebben alleen de suggestie nodig.
- **Banken:** 2 plaids (blanket-props, kleur-override les: children_
  recursive), 2 marshmallow-stokken tegen een stam, emaille mok op de
  stronk.
- **Overkapping:** houtstapel (bewezen firewood-asset uit leeshoek) over
  2/3 van de diepte + bijl-hakblok; warme wandlantaarn AAN (S2-preset)
  + zwakke warme fill zodat de kap een gouden kader wordt.
- **Deurgloed:** warm interieurlicht achter het deurglas (avondkubus-les:
  glas transmissief).
- **Randen:** 2-3 lage varens/grassen-pollen bij de stammen; verder
  soberheid — het vuur moet het frame dragen.

## Techniek/valkuilen
- Vuur-emissie clampt snel: sample_clamp_indirect 5.0 aanhouden, vlam-
  planes uit de shadow-ray halen (visible_shadow=False) anders harde
  vlekken op de stammen.
- Rook-cube: klein en begrensd houden (World Volume = zwart exterieur!).
- Boomstammen: cylinder + schors-PBR werkt; bbox-check zodat ze niet
  in de kuil steken; 1-2 cm het gras in (grounding).
- Blue-hour ruis: 96-128 samples voor de diag, OIDN aan.
- De oude gele-grond-fout: gazon volledig herbouwen met de S1-grasmix,
  avond-donker en mat.
- Preview-naam: `roosmarijn_kampvuur_R1_PREVIEW.png` → review-site :8767.
