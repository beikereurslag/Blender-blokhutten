# Tekentool-swap: 23 scenes op de nieuwe modellen (14-10-2026)

Alle 23 scenes uit `scripts/scenes.txt` hebben nu de blokhut uit de tekentool-export van 11-09
(`source-glbs-new/2026-09-11/`). Tuin, camera, licht, props, deur en de goedgekeurde materialen
zijn gebleven. Alle 23 komen door de controle.

- Contactvel: `contactvel.png` (1800 px breed, zonder tekst) en `contactvel.jpg` (kleiner bestand).
  Welke scene waar staat: `legenda.md`.
- Nieuwe scenes: naast de bron, met `_TEKENTOOL` achter de naam, bv.
  `pilots/S7-leesplek-Camelia250x300/camelia_leesplek_S7_PLANKFIX_TEKENTOOL.blend`.
  De bronblends zijn niet aangeraakt.
- Werkbestanden per scene: `_tekentool_2026-10/<naam>/` met de proefrender (`hero_1080.png`), dezelfde
  oude scene op dezelfde instellingen (`oud_1080.png`), acht hoektest-beelden, het swapverslag en
  de uitkomst van de controle.
- `roosmarijn_modern` (de Zentuin) is bewust niet omgezet; dat is Beikes eigen werk.

## Hoe

1. `scripts/tekentool_omzetten.sh <naam> ...` per scene:
   - `swap_cabin_tekentool.py`: oude cabin eruit, nieuwe GLB erin (halve slag gedraaid), op de oude
     fundering, materialen terug, plankfix, deuropening gesneden, opgeslagen als `_TEKENTOOL.blend`.
   - `tekentool_controle.py`: toetst het verslag, maakt de proefrender en de hoektest.
   - de oude scene nog eens op dezelfde instellingen, om oud en nieuw naast elkaar te leggen.
2. `scripts/maak_contactvel.py` maakt contactvel en legenda.

Een scene telt als omgezet als: de maat binnen het bekende verschil tussen oud en nieuw formaat valt
(breedte en diepte binnen 10 cm, hoogte tot 20 cm hoger), elke oude luifelpaal een nieuwe paal naast zich heeft (anders is de
luifel gedraaid), de wand op de oude fundering staat, de deur er nog is en alle planken voor de ruit zijn
weggesneden, en `validate_scene.py` geen nieuwe zware melding geeft. Die controles zijn getest door ze
expres te laten falen (gedraaide luifel, ander model, verzakte wand, dichte deur, boom door de wand).

## Wat onderweg is gerepareerd

- **Luifelwand kreeg de hutkleur.** Materialen gingen alleen op soort onderdeel terug. De Dahlia's
  hebben een natuurhouten luifelwand naast een grijze hut, en die wand heet in de nieuwe export anders:
  hij werd grijs. Nu krijgt elk onderdeel het materiaal van het oude onderdeel op dezelfde plek.
- **Oude scenes renderden met EEVEE.** Een deel van de scenes is opgeslagen met de viewport-renderer;
  de vergelijkingsrender nam die over. Nu altijd Cycles.
- **Headless pakte de CPU** en de zware scenes vulden de 8 GB van de videokaart. Nu GPU en texturen
  bij renderen hooguit 2K (op 1080p niet te zien).

## Waar Beike naar moet kijken

1. **Nieuwe balk en paal in de luifel.** Het nieuwe model heeft boven de luifelopening een balk en
   achterin de luifel een paal die het oude model niet had. Daar lag geen oud onderdeel, dus ze krijgen
   het balk- en paalmateriaal van de scene. Bij de Dahlia's (Leeshoek, Ochtendkoffie, Tuinkantoor) is
   dat donkergrijs naast een natuurhouten luifelwand. Niet zelf veranderd.
2. **Schoren aan de luifelpaal zijn weg** bij de modellen zonder zijwand (Vinylmiddag, Vlindertuin,
   Buitenbioscoop Lavendel, Schaakavond, Uitslaapochtend, Zonnegroet): de nieuwe tekentool-export heeft
   ze niet meer.
3. **Acht scenes stonden op 4:3** (Buitenbad, Wijnterras, Vinylmiddag, Vlindertuin, Buitenbioscoop
   Lavendel, Schaakavond, Uitslaapochtend, Zonnegroet). De proefrender is 16:9, dus boven en onder valt
   een strook weg. De finals worden 2560x1440 (16:9), dus dat geldt daar ook.
4. **De hoektest** laat bij veel scenes vooral heg en hoge planten zien: de tuinen zijn rond de
   hero-camera aangekleed, niet rondom. Voor de blokhut zelf (deur, luifel, achterwanden) was hij wel
   bruikbaar. De tuinen rondom afmaken hoorde niet bij deze klus.

## Niet gedaan

- Geen finals in 2560x1440; die pas na Beikes akkoord.
- De nieuwe `_TEKENTOOL.blend`-bestanden staan op EEVEE opgeslagen, net als hun bron; het final-script
  moet Cycles zetten (de proefrenders deden dat al).
