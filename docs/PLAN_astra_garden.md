# De Regentuinkamer — garden, walkthrough and print proposal

Date: 10 September 2026. Status: **CONCEPT — awaiting Beike's approval**.

## The garden

A garden immediately after a summer shower: darkened stone, pale grass seedheads and a shallow rain basin catching the first warm sunlight. A continuous dry path follows the basin's eastern edge and straightens toward the cabin door. The sheltered terrace overlooks the planting and the small remaining patches of water. The experience is arrival, discovery, shelter.

The cabin is **Jasmijn 300 × 250 + 250**, with an open canopy and no added side wall. Its compact closed room and sheltered outdoor room make a clear destination at the back of the garden. Keep its actual construction and product materials. Use warm natural timber, grey-brown stone, deep green foliage and restrained white/pale violet flowers. Wetness is selective: stone joints and the basin floor, with a dry, matte walking surface.

The defining composition is the relationship between the dry route, the low basin and the shelter. This is a new layout from the source GLB. The older scene index was consulted to avoid repeating a concept; its scene files supply no garden geometry or staging. The lighting reference supplies technical parameters only.

This is a visual garden proposal, not a drainage engineering specification. The basin reads as a planted depression after rain; no claim about real infiltration performance is made.

## Source and measured cabin

Source: `D:\Blender-blokhutten\source-glbs\Jasmijn 300x250 + 250.glb`.

Read-only probe: `scripts/probe_astra_source.py`; full results: `docs/astra_source_probe.json`. The probe evaluates node transforms and vertex positions without loading textures or creating a Blender scene.

| Measurement | Result |
|---|---|
| File | 6,640,520 bytes; 137 mesh nodes |
| Structural bounds including roof | 5.926 × 2.90727 × 2.34009 m |
| Source door assembly | 1.510 m wide, 1.900 m high |
| Source front | +Y after glTF-to-Blender axis conversion |
| Canopy supports | Two standalone `pole-N` meshes identified |
| Embedded camera | One, named `camera` |

Garden axes: metres; X east/right, Y north/back, Z up. Following normal glTF import and exactly one 0.01 scale conversion, rotate the complete cabin hierarchy 180° around Z. The concept transform on the probed metre coordinates is:

`garden = (-source_x + 8.428, -source_y + 11.82338, source_z + 0.05)`.

This places the structural envelope at **X 7.300–13.226, Y 7.800–10.70727, Z 0–2.34009**. The door faces south at approximately **(9.028, 8.002, 0.05)**; the open canopy is east of the closed room. These coordinates are measured design inputs, not yet a verified Blender import. During anchoring, probe the imported hierarchy again before placement and verify the closed-room exclusion volume separately from the open canopy.

## Layout

Garden extent: **14 × 12 m**. The visible landscape continues beyond this boundary through supporting ground and vegetation, so the render never reveals the edge of a display base.

```text
                         NORTH / +Y
  12  +HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH+
      | rear planting     | rear hedge / tree depth |
      |  fern shade       | +------------+---------+|
      |                   | | JASMIJN    | OPEN    ||
      | tree              | | closed room| CANOPY  ||
   8  |       damp border | +---DOOR-----+--chairs-+|
      |   rain basin      |     |      stone apron |
   6  |-------------------+-----|------------------|
      |   shallow planted |     |                  |
      |   depression      |    / dry path           |
      |   low flowers     |   /     planted drift  |
      |        grasses    |  /                      |
   0  +HHHHHHHHHHHHHHHHHH ENTRY HHHHHHHHHHHHHHHHHHH+
      0                   7                        14
                          X / EAST ->

      dashed division at X=7 / Y=6 = print tile seams
      H = enclosing hedge; tree layers continue beyond the garden
```

Coordinates below take precedence over the schematic's character spacing.

| Zone | Proposed position and treatment |
|---|---|
| Entry | X 7.3–8.7 at Y 0; a 1.4 m opening in the low front hedge |
| Main route | 1.2 m wide; centreline (8,0) → (8,1.5) → (7.7,3.5) → (9.028,5.8) → (9.028,8.002). Gentle continuous curves before the final straight; endpoints and tangents adjusted to preserve width |
| Door approach | Last 2.2 m straight and centred on the door; no pots, grass, hedge emitters or furniture in its clearance |
| Terrace apron | X 7.5–13.1, Y 6.6–8.1; stone meeting the actual threshold, with no raised lip across the route |
| Rain basin | Irregular outline within X 2.8–6.7, Y 2.8–7.8; 0.12 m maximum depression; gently sloping soil edge; small isolated residual puddles, mostly planted ground |
| West shade pocket | X 0.8–2.5, Y 6.5–10.5; ferns beneath a leafy birch |
| East border | X 10.0–13.2, Y 1.2–5.8; three interlocking low planting drifts, highest plants away from the cabin sightline |
| Back hedge | X 0–14, Y 11.4–12; about 1.8 m tall, with deeper staggered tree planting outside the garden |
| Side hedges | X 0–0.6 and 13.4–14; do not intrude into roof or path bounds |
| Front hedge | About 0.65 m tall; interrupted at the entry opening |
| Sitting group | Under the canopy near X 11.4–12.6, Y 8.6–9.5; two chairs and one small table; actual asset bounds will set final centres |

Planting has three heights: groundcover 0.15–0.30 m, flowering/mid grasses 0.4–0.7 m, and a few 0.9–1.2 m accents along the western basin edge. Keep the eastern basin edge low enough to reveal the cabin from entry. Every surface receives an intentional finish and edge treatment: planted soil, close groundcover, stone or shallow water. Maintain usable clear walking space.

## Asset shopping list and provenance

BlenderKit is the first search source. Use the existing local caches where suitable, then the real product GLBs, Polyhaven and Sketchfab. **Local file present does not mean geometry, textures or license are approved.** Every selected asset needs a close inspection and source record before dressing. No asset download or purchase has been made in this phase.

| Item / intended quantity | Source and current evidence | Acceptance / fallback |
|---|---|---|
| Cabin / 1 | Exact source GLB above; geometry measured | Re-probe actual import, repair board alignment, preserve product proportions |
| Stone route + apron | BlenderKit live search returned **Stone Sidewalk Segment**, assetBaseId `d2fe6b10-a06f-4ac7-ab09-2ef12a522b59`, and **Footpath pavment**, `b64e4698-6970-45c6-8aa3-f02513cf508a`; both marked `royalty_free` by API | Inspect surface modules and textures; avoid urban curbs. Local alternate: `assets/blenderkit/stapstenen/Scan_Floor_Old_Step_Stone.blend`; secondary `assets/sketchfab/path_stones/flagstone_floor_vl1iaf0lw_8k_ue_raw/vl1iaf0lw_tier_0.gltf`. Use fitted scanned surfaces with flush joints, never generated box pavers |
| Shelter chairs / 2 | `assets/glbcreator/teak-loungeset-riverside-fauteuil-incl-kussens-eb43e37c-opt.glb` | Real product asset; verify fit below canopy and keep clear of poles |
| Small table / 1 | `assets/glbcreator/teak-bijzettafel-hocker-tambora-d365e725-opt.glb` | Ground complete hierarchy; readable at human scale |
| Full leafy birch / 2 principal trees plus background instances | `assets/blenderkit/berk/Silver_Birch_Tree.blend` and `Birch_tree.blend` | Verify leaves, materials and cluster vertex count. Reject/hide clusters below 50k vertices. Background fallback: `assets/polyhaven/models/pine_tree_01_2k.blend`, complete approved donor only |
| Continuous enclosing hedge / perimeter with entry gap | `assets/polyhaven/models/shrub_03_2k.blend` | Individually append a verified real sprig; Poisson GN scatter, outward rotation, instances retained; no leaf cards |
| Basin grass / 3 interlocking drifts | Live BlenderKit query `sedge grass` returned no free results on 10 September | Species-appropriate sedge remains a sourcing gap. Local `assets/polyhaven/models/grass_medium_02_2k.blend` can cover dry upper margins only; do not relabel it as a wetland species |
| Fern groups / about 7 | `assets/polyhaven/models/fern_02_2k.blend` | Shade pocket and upper damp margins; append one verified variant |
| Low flowers / about 12 clusters | `assets/blenderkit/border-planten/Geranium_Max_Frei.blend` | Dry upper border only, restrained violet; actual identity and material quality still to inspect |
| Soil, moss and basin stones | `assets/sketchfab/path_stones/mossy_stones_pack_tliiadmva_gltf_high/Mossy_Stones_Pack_tliiadmva_High.gltf` plus suitable local scanned ground material | Inspect attribution/license and bound all loose stone placement; no decorative boulder blocking the cabin |
| Lighting environment / 1 | `assets/polyhaven/hdri/kiara_1_dawn_2k.hdr` | File present; inspect HDRI direction against sun |

BlenderKit discovery endpoint: https://www.blenderkit.com/api/v1/search/ . Query parameters used: `asset_type:model order:_score is_free:true`, `page_size=3`, `addon_version=3.21.0`. Record final download IDs and license terms in the build manifest. Before fetch, use the OAuth refresh flow in `pilots/_bk_fetch.py`; omit its optional automatic test render and perform the required 960×720/24 inspection separately.

Some cache folder names are misleading: `duingras` currently contains a Mediterranean pine, and `border-planten` includes whole buildings. Select by inspected content, never by folder name alone. No substitute is accepted merely because a search returned it.

## Light and walkthrough

Start with a low warm sun around 10–15° elevation, illuminating the south-facing facade from the southeast. Match the HDRI's bright direction. Use a bounded neutral volume with height falloff and modest density; keep the cabin crisp while light becomes visible between trees. Start below the dense legacy fog setting and tune in previews. AgX, restrained highlights, natural green. No World Volume.

Target: **40 seconds, 24 fps, 960 frames, 1920×1080 final**. The camera moves through the garden at roughly 0.3 m/s, slowing as it arrives. Continuous motion follows the dry route and then turns along the apron toward the canopy. It does not circle the building.

| Time | Camera position, approximate metres | View and purpose |
|---|---|---|
| 0 s | (8,0.7,1.55) | Cabin beyond low planting, path legible immediately; 32–35 mm |
| 8 s | (7.8,2.5,1.30) | Damp stone in foreground, basin on the left, cabin still visible |
| 16 s | (8.2,4.3,1.45) | Rise gently as the enclosed room and canopy separate in perspective |
| 24 s | (9.028,6.0,1.65) | Straight door approach; grain, foundation and threshold become readable |
| 32 s | (10.5,7.2,1.55) | Move east along the apron, turn toward the canopy; no door collision |
| 40 s | (11.5,8.25,1.45) | Arrive just inside shelter, frame furniture against the cabin wall with a peripheral view back to the basin |

The detailed rig is a later phase. Aim for smooth arc-length travel, eased start/finish, modest changes in height and no abrupt lens jumps. Early wide views show the whole cabin; close arrival views show purposeful construction details rather than trying to fit the entire building from too close.

Camera verification: approximately 12 review keyframes distributed across the route, all rendered at **960×720 / 24 samples** with the final 16:9 framing indicated. Run `scripts/clips_v2/geo.py`'s `Ctx.frame_score()` using the final aspect ratio. Report cabin/ground/vegetation/sky/void/fog fractions and blocked sightlines. Also check path clearance and intermediate positions, not only endpoints.

The legacy `inside >= 0.90` test in `render_clip.py` refers to containment within one hero camera. A real walkthrough intentionally leaves that view. Preserve and report the raw score, and add full-garden coverage/collision checks with stage-specific cabin visibility criteria; do not call the untouched legacy test passed when it is not. No black void, world edge, hedge crossing or cabin penetration is acceptable. Reference views for the three dressed previews: entry, basin reveal and canopy approach.

After camera review, prepare a PowerShell night-run script for Beike to start. It must render sequentially, resume from verified complete frames, encode the walkthrough, and retain logs and intermediate files. Runtime will be estimated from an approved sample, not from old single-frame timings.

## Print strategy — 1:50

Choose **1:50** to retain the cabin and furniture detail. The assembled garden is **280 × 240 mm**; it is intentionally a tile set. A 1:75 version would be 186.7 × 160 mm but make the small furniture and timber details less legible.

Four base tiles, each **140 × 120 mm**, at X=7 m and Y=6 m. The entire cabin including roof lies within NE, so no building straddles a joint. Source envelope at scale: **118.52 × 58.15 × 46.80 mm**. The 120 mm real-world basin depth becomes **2.4 mm** relief.

| Tile | Real-world bounds | Built-in relief and separate pieces |
|---|---|---|
| SW | X 0–7, Y 0–6 | Basin floor, soil and low groundcover fused into base; stones as continuous relief |
| SE | X 7–14, Y 0–6 | Entry path and border relief; a few substantial grass clumps as keyed drop-ins |
| NW | X 0–7, Y 6–12 | Basin head and shade pocket; tree/hedge sockets and fern relief |
| NE | X 7–14, Y 6–12 | Apron, continuous cabin landing and planting sockets; removable cabin and sitting group |

Base design allowance: 6.4 mm overall thickness with at least 4 mm below the deepest depression. Flat underside with a chamfered edge; determine infill/wall settings in slicing. Soil, path and low vegetation become connected sculpted relief. Residual water is a shallow solid surface in the print, not an open hole or liquid. Do not try to print individual grass blades or alpha foliage planes.

Tile joints: sliding tongue-and-groove alignment with separate underside dovetail keys, all printed. Use the measured **0.15 mm sliding gap** from the existing calibrated implementation; confirm whether that parameter is total or per-side before reproducing it. Do not silently double the clearance. Assemble each row first, then connect the rows; keep key channels accessible until final assembly. Hide top seam transitions in planting edges where possible, and retain the necessary path seam as a clean joint.

Cabin: separate print-only derivative with solidified/remeshed connected wall and frame components. Preserve dimensions and door layout from the source. Keep crisp **18° sawtooth** relief on vertical faces; test voxel resolution on a wall coupon before remeshing all fine detail. The roof is a separate part so the enclosed room and canopy do not demand a large hidden support mass. Decide the roof's bed orientation from the measured roof geometry during print design. No alteration to the archviz source follows from print accommodations.

Posts/frame: use ribs-in-groove **3×3 mm, 60% of post height**, only where the receiving printed component can accommodate the joint. The measured 90 mm real posts scale to 1.8 mm, so these connectors cannot simply fit inside an exactly scaled post. Prefer joints in the thicker base/roof interfaces; any local print-only thickening must be documented and reviewed. No magnets, screws, inserts or fragile snap fits.

Vegetation: hedge sections are connected watertight volumes with leaf relief and broad keys. Trees use a continuous trunk/canopy solid with reinforced branch junctions; split into keyed halves if layer support requires it. Furniture becomes a small unified group on an inconspicuous ground insert where independent legs are too fragile. Preserve recognisable silhouettes and document every thickening or lost detail.

Deliver one **3MF project containing the required plate layouts**, plus per-part STLs and QA reports in `C:\Users\beike\blokhut-print\output\garden\`. Do not promise all parts fit on one physical plate: two 140×120 tiles already consume most of a plate. Start from one tile per plate, then arrange the cabin and vegetation on further plates after support/brim checks.

Use P2S / PLA Basic / 0.16 mm layers. Confirm the installed printer profile before layout. Enforce the user-specified ceilings of 180 mm with support and 194 mm without. Prefer minimal support, grid 5, plate-only, Z gap 0.24; any tree-support slicing runs through the GUI.

### Per-part QA gate

The specifically named "10-point rookie checklist" was not located in the supplied compendium or the searched vault/print Markdown files. This explicit working checklist consolidates the supplied rules; it is not presented as a recovered quotation:

1. Correct physical scale and complete source geometry accounted for.
2. Each intended part watertight, consistent normals and positive volume.
3. No unintended disconnected fragments; classify every component.
4. Wall thickness and thin/tall ratios checked, including vegetation and chair legs.
5. Run `qa/island_check.py <part.stl> 0.16` in the actual print orientation for every part.
6. Investigate marginal support and bridges; exclude bed-contact surfaces and narrow sloping relief from false bridge reports.
7. Flat bed contact, sensible orientation and support accessibility verified in the slicer. Any raw island failures require redesign or demonstrated sliced support; never silently waive them.
8. Plate, brim, support and machine height limits pass.
9. Dovetail/tongue/rib fits and assembly sequence verified; measured gap preserved, 18° relief retained.
10. Inspect sliced layers and orthographic detail views; report every unprintable or materially altered feature before delivery.

## Build gates and present status

| Gate | Deliverable and verification | Required next approval |
|---|---|---|
| Concept — current | This document, source probe, layout and print arithmetic | Beike approves concept/cabin/layout/scale |
| Anchoring | Fresh scene, ground/path/borders/backdrop/cabin; code audit; one 960×720/24 preview | Beike approves anchoring |
| Dressing | Verified real assets, all placement/material checks; three 960×720/24 previews | Beike approves dressing |
| Camera | Route in scene, frame scores, clearance checks, ~12 preview keyframes | Beike approves camera and final rendering |
| Walkthrough | Headless sequential 1080p night-run script started by Beike | Review finished walkthrough |
| Print | Reviewed print accommodations, per-part STL/QA, 3MF plate layouts | Review print set before physical printing |

All preview helpers must explicitly override their older defaults to 960×720/24. Use AgX, texture limit 2048 and persistent data off. Run `validate_scene.py`, measured closed-room exclusion tests, object/bbox summaries, terrain grounding, texture-path checks, the bare-tree check and board alignment checks. Add crop/visual inspection after the numerical checks; neither replaces the other. Keep grass outside the full route plus a 0.15 m exclusion band.

Do not call the old hedge helper unchanged: it imports all variants, removes objects and uses RANDOM scatter. Adapt to a single verified donor and Poisson scatter. Some library roots still point to the old Documents junction; resolve all scene paths to this project explicitly. Keep all checkpoints, source files and logs. No auto-cleanup, commits, final rendering or unauthorized deletion. Remove only the imported GLB camera from the new working scene as explicitly required by this brief; retain the source file.

**Checked now:** source geometry and door direction; local asset candidates; BlenderKit discovery search; 1:50 tile/cabin bounds; the camera score implementation; print QA entry points. Branch is `weekend-renders` with pre-existing changes, which remain untouched.

**Failures/gaps now:** the community MCP `get_scene_info` call returned "Could not connect to Blender. Make sure the Blender addon is running." The sedge search returned no free results. The named rookie checklist was not found. Assets have not been visually certified, and there is no built scene, render, sliced plate or print QA pass yet.

To open Blender if necessary, this PowerShell command is ready to paste:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe'
```

Then start the community Blender MCP connection from the add-on's sidebar panel. The stdio server is already registered in Codex; the failed link is the connection to the Blender add-on. Re-test read-only before any interactive scene work. Headless source inspection remains available.

**Decision requested:** approve De Regentuinkamer with this Jasmijn, the 14×12 m layout and four-tile 1:50 print strategy, or specify the concept change. Work stops here at the requested concept gate.
