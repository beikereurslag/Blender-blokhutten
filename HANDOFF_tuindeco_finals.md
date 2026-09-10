# HANDOFF — finals verrijken met échte Tuindeco-producten

> Gestart 17 jul 2026. Doel: props in de goedgekeurde finals vervangen door
> échte Tuindeco-producten (via GLB Creator) → shoppable renders. Werkwijze:
> `PROMPT_nieuwe_sessie_tuindeco_finals.md` + Obsidian "GLB Creator werkwijze".

## Stand van zaken (17 jul)

- **Inventaris gedaan voor 13 van de 21 finals** (parallelle read-only analyse).
  8 finals nog niet geïnventariseerd omdat de **Claude org-maandlimiet** halverwege
  werd geraakt: A avonddiner, Vuurtafel, Wellness, Buitenkeuken, Zwembadtuin,
  Kapschuur A/B/C. (Deze afmaken kan zonder subagents: scripts zelf lezen.)
- **GLB genereren zelf kost Meshy-credits, geen Claude-spend** → productie is NIET
  geblokkeerd door de Claude-limiet; alleen zware parallel-analyse wel.
- Nog niets gegenereerd/gewijzigd. Wacht op Beikes keuze + akkoord (credits).

## Tuindeco-assortiment: wat is er WEL en NIET (uit sitemap + categoriepagina's)

WEL (categorieën bevestigd):
- `buitenleven/tuinmeubelen`: **tuinsets, loungesets** (Barbados/Dominica/Jamaica/
  Tambora/Riverside…), **tuinbanken, tuinstoelen, tuintafels, picknicktafels**, werkbanken
- `buitenleven/plantenbakken`, `buitenleven/pergola-s`, `buitenleven/containerbergingen`
- `wellness`: **hottubs** (+accessoires), sauna's, saunabarrels, **spa's, zwembaden**
- `buitenspelen`: speelhuisjes, schommels, glijbanen, speeltoestellen, zandbakken
- kern: schuttingen, tuinhout, blokhutten/buitenverblijven, overkappingen, bouwmateriaal

WAARSCHIJNLIJK GAT (geen eigen categorie gezien — vraag Beike / nader checken):
- ligbedden/zonnebedden · zweefparasols · vuurtafels/vuurschalen · lantaarns/
  buitenverlichting · poefs · buitenvloerkleden · sierkussens · deco (schalen/karaffen)

TECHNISCH: producten staan NIET als leesbare slugs in de sitemap (die is vooral
hout/schutting). Ze staan op de **categoriepagina's** (server-rendered productnamen,
bv. tuinsets-pagina toont "Loungeset Barbados/Dominica/Jamaica/Tambora/Riverside").
De sitemap-"~8500 detail-URL's filteren"-methode uit de prompt klopt niet voor
meubels → categoriepagina's scrapen voor de echte product-URL's.

## Al beschikbare assets (nu direct herbruikbaar)

- `assets/glbcreator/wembley-sunlounger-rev2-simplified.glb` — Teak Sunlounger
  Wembley → vult de **ligbedden** in B spa / P poolhouse / I riviera (+Wellness).
- `assets/glbcreator/speelhuis-sneeuwwitje-rev3-439k.glb` — voor een buitenspelen-scène.

## Kern-inzicht: dezelfde generieke assets keren terug → genereer 1×, hergebruik overal

| Productfamilie | Komt terug in (finals) | Tuindeco? | Prio |
|---|---|---|---|
| Loungebank/loungeset (crème Eichholtz + rotan CRAIG) | C, D, M2, P, I, BO2, H | JA (loungesets) | HOOG |
| Eettafel + tuinstoelen (teak dining) | C, P, G | JA (tuinsets/tafels/stoelen) | HOOG |
| Ronde tuin-/bistrotafel + stoelen | E2, G | JA (tuintafels) | HOOG |
| Plantenbakken (hout + wit rond + terracotta) | B, D, E2, F, G, P, BO2, I | JA (plantenbakken) | MED-HOOG |
| Hottub | J2, B (+Wellness) | JA (wellness/hottubs) | HOOG |
| Ligbed/zonnebed | B, P, I (+Wellness) | ?? (Wembley al beschikbaar) | HOOG |
| Zweefparasol | I, P | ?? (Beike's Parasol.fbx = echt product?) | HOOG |
| Vuurtafel/vuurschaal | F (+Vuurtafel) | ?? gat | HOOG |
| Lantaarn/buitenverlichting | bijna alle | ?? gat | MED |
| Bijzettafel | B,E2,F,G,H,I | ?? mogelijk onder tuinmeubelen | MED |
| Poef, vloerkleed, sierkussen, deco | diverse | grotendeels gat | LAAG |

## Productie-log P poolhouse (17 jul) — Beike: startscène = P; "alleen in-assortiment"; variatie mag (2800 cr)

Gegenereerd (6 × ~30 cr) via `POST /api/create {url}` (tuindeco /detail/-links):
- `loungeset-barbados-b20fbaf3` — Loungeset Barbados. **HELE SET** (bank+2 stoelen+tafel, 3.11×1.66 m); wit/crème alu frames + beige kussens + teak blad. → P poolhouse lounge (incl. eigen tafel, dus losse salontafel vervalt).
- `teak-loungeset-riverside-fauteuil-incl-kussens-eb43e37c` — losse teak fauteuil (0.56×0.64, iets ondermaats). → bibliotheek.
- `teak-bijzettafel-hocker-tambora-d365e725` — LET OP: de "Lounge set Tambora"-tile linkte naar de **bijzettafel/hocker** (80×80×40, teak+glas), NIET de bank. Model kwam +103% te breed → non-uniforme rescale (x×0.49, y×0.84). → bibliotheek (bijzettafel-slots).
- `teak-tuinstoel-bantam-66fa124e` — Teak tuinstoel Bantam. **2-STOELS model** (1.36 m). → P dining als 2 paren (west+oost = 4 stoelen).
- `teak-tuinstoel-toledo-*` (klaar) + granada (liep nog) — extra stoel-variatie, niet nodig voor P.

Bibliotheek-hergebruik (0 cr, gedownload naar assets/glbcreator/):
- `tuintafel-teak-300-x-100-cm-47a25758` — eettafel. Maat: +10% te lang (3.31 vs 3.00), -8% smal → non-unif rescale of accepteren.
- `teakhouten-bloembak-moro-40899118` — MAAT-FOUT: tool las 43³ maar Moro = **83×43×43** (langwerpig); model is ~43 cm kubus. Nu als kleine teak-plantenbak gebruikt; hergenereren op 83 cm voor accurate Moro.
- `wembley-sunlounger-rev2-simplified.glb` — ligbed (lokaal, echt Tuindeco-product P002490).

Import-pijplijn: `cl.import_gltf_prop` maakt een nieuw XYZ-empty-root en parent daaronder → quaternion-wrapper-valkuil al opgelost; roughness-clamp ≥0.55 los toevoegen. Non-uniforme catalogus-rescale nog niet toegepast (eerste diag op hoogte-anker).
Job-ID's + product-URL's: scratchpad `jobs.txt` / `cat_*.html`-extracties.
Swap-script: `overkappingen-website/scene_p_poolhouse_tuindeco.py` (output `conceptP-kdi-600x420-tuindeco`, naast het origineel).

## Volgende stap (voorstel)

1. Beike kiest: startscène + hoe de "gat"-props te behandelen (generiek laten of hij
   levert een categorie/URL).
2. Voor de startscène: categoriepagina('s) scrapen → concrete product-URL's + creditkosten
   → **voorstel-lijst ter akkoord** → pas dán genereren.
3. Bestaande finals nooit overschrijven; `_tuindeco`-suffix ernaast.

## Per-scène inventaris (13 gedaan)
Bron: workflow-journal `subagents/workflows/wf_a381674f-63b/journal.jsonl`.
Volledige replaceable-lijsten per scène (current asset → categorie → keywords →
prio → zichtbaar) staan daar; hergebruik via `resumeFromRunId` als de spend-limiet
weer open is om de 8 ontbrekende finals af te maken.
