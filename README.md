# Blender Blokhutten — Marketing Visuals voor Blokhutwinkel.nl

3D verkoopvisuals van **blokhutten** (Nederlandse tuinhuisjes/kantoren) gemaakt in **Blender** via **Claude/MCP integratie**. Eén blokhut wordt aangekleed in meerdere tuin-stijlen (Modern Minimalist, English Cottage, Scandinavian, etc) om de veelzijdigheid te tonen voor verkoopcontent.

## Status

| Pilot | Cabin | Stijl | Status |
|---|---|---|---|
| 1 | Magnolia 300×200 | Modern Minimalist | ✅ Final v4 (2560×1440) |
| 2 | Lelie 400×250 + 300 + zijwand | English Cottage | ⚠️ Gerenderd maar te donker — HDRI fix nodig |
| 3 | Camelia 250×300 + 300 + zijwand | Scandinavian + Hottub | 🟡 .blend klaar, render nog niet gestart |

## Repo structuur

```
Blender-blokhutten/
├── README.md                      ← deze file
├── HANDOFF.md                     ← uitgebreide handoff voor nieuwe machine/Claude
├── source-glbs/                   ← 33 source GLB-bestanden van blokhutwinkel.nl
│   ├── Camelia 250x300.glb
│   ├── Magnolia 300x200.glb
│   └── ...
├── pilots/                        ← Per blokhut × stijl een eigen folder
│   ├── Magnolia-300x200/
│   │   └── style-modern/
│   │       ├── magnolia_modern.blend
│   │       ├── magnolia_modern_FINAL_v4_2560x1440.png  (finale)
│   │       └── magnolia_modern_v[1-8]_PREVIEW.png  (iteraties)
│   ├── Lelie-400x250-300-zijwand/
│   │   └── style-cottage/
│   │       ├── lelie_cottage.blend
│   │       └── lelie_cottage_FINAL_2560x1440.png
│   └── Camelia-250x300-300-zijwand/
│       └── style-scandi/
│           └── camelia_scandi.blend  (render nog niet gedraaid)
└── docs/                          ← Research + landscape architecture principes
    └── wiki/
        ├── concepts/              ← Garden style, dressing, Blender best practices
        ├── entities/              ← Klant + asset-bron beschrijvingen
        ├── sources/               ← Externe research-bronnen
        └── questions/             ← Synthesis page met findings + open questions
```

## Quickstart op nieuwe machine

1. **Clone** + LFS pull:
   ```bash
   git clone https://github.com/beikereurslag/Blender-blokhutten.git
   cd Blender-blokhutten
   git lfs pull
   ```

2. **Lees** [HANDOFF.md](HANDOFF.md) — sectie 3 (tools setup) + sectie 4 (status) + sectie 8 (next steps)

3. **Setup** Blender + blender-mcp addon (zie HANDOFF sectie 3)

4. **Open** een `.blend` file. **Belangrijk**: textures kunnen breken op nieuwe machine (Polyhaven assets staan in tijdelijke macOS folders op originele machine). Twee opties:
   - **A**: Re-download via blender-mcp (asset-list in HANDOFF sectie 9)
   - **B**: Originele machine moet `File → External Data → Pack Resources` doen vóór commit

## Technisch

- **Blender** 4.0+ (getest 5.1.1)
- **Cycles** GPU + OpenImageDenoise + Adaptive Sampling, 256 samples
- **Render-target**: 2560×1440 PNG (16-bit)
- **MCP tooling**: `ahujasid/blender-mcp` v1.5.5+ op port 9876
- **Asset-bronnen**: Poly Haven (CC0) + Sketchfab (CC0/CC BY filter only)

## Belangrijkste learnings

Volledige uitleg in [HANDOFF.md](HANDOFF.md). Highlights:

- **GLB-bestanden van blokhutwinkel komen in centimeters** → altijd 0.01x scale na import
- **Plants ALLEEN in defined bed-zones** (anders "vliegend gras")
- **Hardscape +10cm boven gravel** met cortenstaal edging (anti-coplanair)
- **Sketchfab licenties**: alleen CC0 of CC BY (commercial use); xfrog/CC BY-NC = no-go
- **Cycles render** krijgt MCP-timeout maar render gaat door — check filesystem voor output
- **Object parenting bug** in Blender — gebruik direct world coords, geen `parent_inverse`
- **DIY furniture proporties**: bij twijfel Sketchfab pakken (Adirondack, lounge)
- **Camera regels**: 35-50mm, 1.5-1.6m hoogte, 22-35° angle, cabin op 1/3 lijn

## Klant context

**Blokhutwinkel.nl** (Zutphen) — verkoper van blokhutten, tuinhuizen, veranda's, garages, paviljoens. 10K+ modellen. Hun eigen 3D-tool genereert technische CAD-tekeningen; deze repo levert sfeer-vol gerenderde verkoopvisuals als aanvulling.

## Licentie

- **Source GLB-bestanden**: eigendom van Blokhutwinkel.nl
- **3D-assets ingebed in renders**:
  - Polyhaven CC0 (HDRIs, textures, models)
  - Sketchfab "Wooden Lounge Chair with metal legs" door [varvashenko.lida](https://sketchfab.com/varvashenko.lida) — **CC Attribution** (attributie verplicht bij gebruik)
- **Renders**: voor blokhutwinkel.nl marketing gebruik

---

*Laatste update: 2026-04-30. Zie [HANDOFF.md](HANDOFF.md) voor volledige project-context.*
