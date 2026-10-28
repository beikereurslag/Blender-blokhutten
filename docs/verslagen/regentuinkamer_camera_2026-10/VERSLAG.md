# Regentuinkamer: camera en proeffilmpje (14-10-2026)

De walkthrough-camera van De Regentuinkamer (G1) staat in de scene. Ernaast liggen een hero-render,
drie stills uit de route en een proeffilmpje op lage resolutie. Het echte filmpje (1920x1080, 960
beelden) komt pas na Beikes akkoord op de stills.

## Bestanden

- `stills_v17.jpg`: linksboven de hero (startpunt van de route), rechtsboven 8 s (regenbekken),
  linksonder 24 s (deur en dorpel), rechtsonder 40 s (zitgroep onder de kap). De losse 1080p-beelden
  staan in `pilots/G1-regentuinkamer-Jasmijn300x250-250/_camera/` (`G1_hero_1080_v14.png`,
  `G1_still_t08s/t24s/t40s_1080_v17.png`).
- `rondom_v15.jpg`: acht standpunten verspreid door de tuin, elk naar de overkant kijkend. Van links
  naar rechts, per rij: noord-midden, noordwesthoek / onder de kap, oost / west, zuidoosthoek /
  zuid-west, zuidwesthoek.
- Proeffilmpje: `G1_proef_v17_640x360_12fps.mp4` (ook in `pilots/G1-regentuinkamer-Jasmijn300x250-250/_animatic/`)
  (640x360, 16 samples, 12 beelden per seconde; alleen om de beweging te beoordelen).
- Scene met camera: `regentuinkamer_G1_v17_camera.blend` (gebouwd uit v13, die onaangeroerd is).

## Hoe

- `regentuinkamer_stap3_camera.py` bouwt de route uit het plan (40 s, 24 fps) en toetst twaalf
  punten langs de route: ooghoogte, niet door hut of haag, geen wereldrand in beeld, zichtlijn vrij.
  Alle twaalf in orde, in elke versie.
- `regentuinkamer_stap3b_stills.py` maakt hero, stills en de rondom-beelden.
- `regentuinkamer_stap4_animatic.py` rendert het filmpje; met persistent data kost een beeld op
  640x360 ongeveer 3 seconden in plaats van bijna een minuut.

## Wat er aan de route is veranderd

De standpunten zijn die van Astra's plan. De kijkrichtingen zijn bijgesteld nadat de eerste twaalf
kijkpunten (v14) bekeken waren:

- 8 s keek strak naar de deur; het regenbekken, het hart van het concept, kwam nergens in de film.
  Nu kijkt de camera daar naar links: bekken in beeld, hut rechts.
- 24 s keek op 2 m afstand recht tegen de wand. Nu omlaag naar deur, dorpel en schort.
- 32 s lag 0,6 m van de zuidwand (een paar seconden alleen planken); een halve meter zuidelijker.
- 40 s stond 1 m van de stoelen; nu op de rand van de kap, met beide stoelen en de tafel tegen de
  wand (lens loopt rustig van 31 naar 28 mm).

## Wat Beike moet weten

1. **De tuin is aan de zuidkant niet af.** Achter de lage voorhaag ligt een kaal, vlak veld tot aan de
   bergen van de lucht (zie de bovenste vier rondom-beelden). De film loopt naar het noorden en ziet
   dat nooit, maar een tweede camerastandpunt of een productfoto vanaf de hut wel. Dat is aankleding,
   niet camerawerk; niet zelf veranderd.
2. **Onder de deur zit een donkere spleet** van een paar centimeter boven de drempel. Op afstand is
   het een dun lijntje, in de still van 24 s valt het op.
3. **Deze blokhut is nog het oude tekentool-model** (Jasmijn 300x250 + 250 uit de base-blend). De
   23 andere scenes zijn op 14-10 omgezet; deze niet, want hij stond niet in die lijst.
4. **Aankleding officieel nog niet goedgekeurd.** Astra's review van v12 liet die open; v13 is daarna
   nooit gerenderd. De stills zijn de eerste beelden van v13.

## Niet gedaan

- Geen echt filmpje in 1920x1080; pas na akkoord op de stills.
- Het nachtscript voor de lange render (PowerShell, hervatten na een onderbreking) is nog niet
  gemaakt; dat volgt na akkoord.

## Aanvulling later op 14-10: zuidkant en deur (v20)

Nieuwe versie `regentuinkamer_G1_v20_zuid.blend` (gebouwd uit v17; v13 en v17 staan er nog), met
`regentuinkamer_stap5_zuidkant.py`. Nieuwe beelden naast de oude: `stills_v20.jpg` en `rondom_v20.jpg`.

- **Zuidkant.** Achter de voorhaag ligt nu een weide met op ongeveer 8 m een veldhaag (1,4-1,9 m,
  zelfde haag als in de tuin), daarachter bomen in groepjes op 30-58 m, een verre ring op 64-105 m
  en hoekbossen naar zuidoost en zuidwest. Recht naar het zuiden en schuin naar de hoeken zijn de
  bergen van de lucht weg.
- **Schaduw.** De zon staat laag in het zuiden (16 graden): een boom werpt dan 3,5 keer zijn hoogte
  aan schaduw naar het noorden. Daarom stond er eerst niets. Het script toetst elke nieuwe boom en
  haag en slaat niet op als er één schaduw in de tuin valt; die toets is ook expres op fout gezet en
  ving dat. De belichting van de hero is gemeten gelijk gebleven (minder dan 0,5 procent verschil).
- **Deur.** Het stenen schort hield 11 cm voor de dorpel op (Astra kortte het in v6 over de hele
  breedte in om een overlap met de kapvloer weg te halen). Een strook steen tot onder de deur sluit
  de donkere band; de top blijft onder de dorpel, dus er komt geen opstaande rand.

Nog zichtbaar: vanuit het westen kijkend naar het oosten piepen achter de oostflank nog bergen door.
Dat deel stond er al zo en is geen zuidkant; niet aangepast. De stills en de film kijken die kant
niet op. Het proeffilmpje is niet opnieuw gemaakt: de route is niet veranderd.
