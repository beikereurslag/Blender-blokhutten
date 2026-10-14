# PLAN — Magnolia 300×200 "Vijvertuin" (vervangt magnolia_groene_long)

> Nieuw concept voor de kleinste cabin, 8 jul. Beikes richting: "je mag
> creatief zijn, vooral in de tuin, zoals bij het zwembad — die was echt
> mooi." Dit plan zet dat waterelement in eco-vorm in: de Magnolia als
> **vijverhuisje aan een natuurlijke tuinvijver**. Het groendak + de
> regenton blijven het productverhaal (duurzaam) dragen — de vijver maakt
> het eindelijk vóelbaar i.p.v. aangewezen.

## Verhaal in één zin
Een ochtend aan de natuurvijver: de Magnolia met sedumdak spiegelt in
stil water, een vlonder steekt de vijver in, koffie staat klaar op de
rand — biodiversiteit als luxe.

## Basis
- **Map (nieuw):** `pilots/Magnolia-300x200/style-vijvertuin/` —
  bouw vanaf `magnolia_groene_long_v4.blend` (product + groendak +
  regenton + heg staan er al in; alle oude paden/tegels weg).
- **Moment:** vroege ochtend, zon elev 9°, ~4300K, energy 4, van
  rechtsachter → cabin + treeline spiegelen mét warme rand in het water.
  Dunne mist-cube (density 0.003) laag boven het wateroppervlak.
- **Camera:** 35 mm, hoogte 1.5 m, LAAG over het water gericht: vijver
  vult de onderste 40% van het frame als spiegel, cabin op de rechter
  derde-lijn, 3/4-hoek. De reflectie is de foto.

## Anker (stap 1 — eerst akkoord vragen)
1. **Vijver:** organische nierviorm ~4×2.5 m vóór de cabin (tussen
   camera en cabin, iets links). Bouw: verlaagde bodem-mesh (-0.35 m),
   donkere bodem (humus, val 0.03), watervlak op -0.04 m: glass/principled
   met Transmission 1, roughness 0.03, IOR 1.33, licht groenige tint —
   het B-hottub-waterrecept maar dan STIL (geen bump: spiegel!).
2. **Oever:** geen harde rand — grind/kiezelstrook (10-20 cm) die onder
   het wateroppervlak doorloopt + gras dat tot aan de kiezels groeit.
   Aan de achteroever 2-3 grote keien (rots-asset uit ochtendnevel).
3. **Vlonder:** 1.6×1.2 m douglas-plankjes, steekt 0.5 m over het water
   uit (zelfde plank-materiaal als het cabin-dek), 6 cm boven waterlijn.
4. **Terreinverbinding:** stapstenen van de cabin-deur naar de vlonder
   (verzonken, S3-regels uit de review).
5. Heg + treeline uit de bestaande blend behouden; horizon dichtzetten.

## Dressing (stap 2 — na anker-akkoord)
- **Waterplanten:** 2 clusters riet/lisdodde aan de achteroever (BK
  "cattail"/"reed", linked copies), 3-4 waterlelieblad-vlakken (plat op
  het water, simpele groene discs met waxy shader werken al) + 1-2
  bloemen.
- **Vlonder-still-life:** koffiekop + boekje of verrekijker (vogels
  kijken), opgevouwen plaid.
- **Eco-signalen:** de bestaande regenton tegen de cabin (blijft),
  insectenhotel-blokje aan de heg-zijde, 1 nestkastje aan de wand.
- **Border:** border_lush-achtig cluster (geranium/lavendel uit de
  BK-map `border-planten\`) op de linker oeverhoek als kleuranker.
- GEEN meubelset — de vlonder + kop koffie is het zitverhaal; leegte
  houdt het serene.

## Techniek/valkuilen
- Water = vlak op -0.04 m, NIET realizen; reflectie heeft samples nodig:
  diag op 96 samples i.p.v. 64.
- Mist-cube verbergen tijdens raycast/mask-passes (R4-les).
- Gras-mask rond vijver én onder vlonder (geen sprieten door water/hout).
- Zonnepanelen op het dak liggen er al — laten liggen, leest eco.
- Groendak: sedum-kleur naar groen-rood mix (de gele stro-kritiek uit de
  oude review geldt nog steeds — korte instances 2-4 cm, ColorRamp).
- Preview-naam: `magnolia_vijvertuin_R1_PREVIEW.png` → review-site :8767.
