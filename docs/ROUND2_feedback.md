# Ronde-2 fixes — feedback Beike (24 jun)

Bron: `blender feedback.pdf` (scenes 12-16) + `renders feedback.pdf` (Lelie) + mondelinge feedback.
Annotated crops: `C:\Users\beike\Documents\blfb_pages\p1-3.png`.

## Status per scene
- **1-2 Lelie (Ochtendnevel/Avondkubus)** — ✅ KLAAR (v3 finals: groene schijf/bank/pad/plant/wand/heg + HDRI+zon/mist, de-blue + crisp).
- **11 Magnolia Groene Long** — ⏸️ overgeslagen op verzoek ("deze laten we").
- **Ronde 1 (generieke grond-fix)** — pad→natuursteen toegepast op 7 scenes; groene-blob-detector ving 0 (te streng — mist getextureerde/grotere blobs); 4 render/fix-fouten (zie onderaan).

---

## Round-2 per-scene actie-items (uit de PDF)

### 12 — Magnolia Wintertuin  (`Magnolia-300x200/style-scandi`)
Feedback: *"deze scene is een beetje kaal, de patio sluit niet aan op de blokhut. en de grijze bank, als dat het is, snap ik niet en staat verkeerd."*
- [ ] Patio **aansluiten** op de blokhut (nu losse plaat ervoor).
- [ ] **Grijze bank** verwijderen of vervangen door echte, goed geplaatste bank (materiaal + positie).
- [ ] Scene **aankleden** (te kaal) — beplanting/props langs gevel.
- ⚠️ Batch-fix faalde op deze scene (fix-fout) — apart uitzoeken.

### 13 — Roosmarijn Zentuin  (`Roosmarijn-200x300-400-zijwand/style-japanese-zen`)
Feedback: *"leuk begin"* (concept behouden), maar:
- [ ] **Bomen links**: low-poly, te dicht op elkaar, scheef → vervangen door volle Polyhaven-bomen, spreiden, rechtzetten.
- [ ] **"ik weet niet wat dit hier doet"** — onbekend object → identificeren + weg/fixen.
- [ ] **Kale bomen achterin** → `hide_bare_trees.py` / vervangen.
- [ ] **"snap niet wat dit witte is"** — verwarrend wit vlak (geharkt zand/grind?) → vorm verduidelijken of vervangen.
- [ ] **Groene blob** (groene schijf in het grind) → weg (batch-detector miste 'm — handmatig).
- ⚠️ Batch-render faalde — apart uitzoeken.

### 14 — Roosmarijn Kruidenterras  (`Roosmarijn-200x300-400-zijwand/style-mediterraan`)
Feedback:
- [ ] **Lege bloempotten** → vullen met planten/kruiden.
- [ ] **Zwevende plant** → gronden.
- [ ] **"bloemen naast de bak, lege onderkapping, heel druk op een plak"** → beplanting spreiden i.p.v. één kluit; **overkapping vullen/aankleden**.
- [ ] **Random losse plant vóór de heg** → verplaatsen + die plek dichter maken.

### 15 — Zonnebloem Zomeravond  (`Zonnebloem-300x300-300-zijwand/style-boerderij`) ⭐
Feedback:
- [ ] **Vliegende bloemen** (hortensia's) → op de grond zetten.
- [ ] **Lampen onlogisch + gaan door het dak** → herplaatsen/onder de dakrand monteren.

### 16 — Zonnebloem Ochtendhoek  (`Zonnebloem-300x300-300-zijwand/style-scandi`)
Feedback: *"leeg, saai en onlogisch. onderkapping ook niet gevuld. heeft meer sfeer nodig."*
- [ ] **Aankleden** (te leeg/saai) — beplanting, props, voorgrond-laag.
- [ ] **Overkapping vullen** (zithoek/styling).
- [ ] **Meer sfeer** — warmer licht / HDRI / atmosfeer.

---

## Terugkerend (uit eerdere visuele audit, geldt breed in ronde 2)
- Pad: niet alleen kleur maar **echte klinker-/tegel-geometrie** waar nodig + gronden + randafwerking.
- **Groene blobjes**: detector verfijnen (ook getextureerde/grotere) en per scene controleren.
- **Gras**: echte GN-grassprieten (ronde-1 deed alleen kleur).
- **Zwevende props** gronden, **kale bomen** verbergen, **bomenrij** verdichten (geen vliegend eiland).
- **Compositie/sfeer**: minder leeg/symmetrisch, voorgrond-laag, overkappingen aankleden.

## Batch ronde-1 fouten om uit te zoeken
- `magnolia_wintertuin` — fix-fout (script-fout bij openen/verwerken).
- `camelia_wijnterras`, `lavendel_lavendelveld`, `roosmarijn_zentuin` — render-fout (mogelijk CUDA/VRAM of v3-issue).
