# START HIER — weekend-run 10 jul 2026 (autonoom, Opus)

Beike, ik heb het weekend de 4 werkstromen gedraaid die **zonder Fable 5 en zonder
jouw live-review** konden. **Niets gecommit, niets gewist, geen finals gerenderd,
geen creatieve keuzes voor jou gemaakt.** Alles is reversibel.

## → Voor Fable 5 (implementatie): [FABLE5_IMPLEMENTATIE.md](FABLE5_IMPLEMENTATIE.md)
Concreet runbook om de R4-ronde af te maken: werkwijze, de 5 beslissingen die eerst
bij Beike opgehaald worden, blocker-fixes, de S-A…S-J-recepten, en de valkuilen.

## Bekijk eerst
- **Review-galerij:** http://localhost:8767 — bovenaan (sectie ①) de **3 getrouwe
  R4-rebuilds**, daaronder (②) alle 8-jul R4-previews zodat je kunt vergelijken.

## Deliverables
| Doc | Wat |
|---|---|
| [docs/REVIEW_pilots_R4_WEEKEND.md](docs/REVIEW_pilots_R4_WEEKEND.md) | Diepe technische QC van alle 13 scènes: **3 blockers · 26 high**, 10 systemische bevindingen, per-scène fixlijst. **Geen fixes toegepast.** |
| [docs/ASSET_AUDIT_WEEKEND.md](docs/ASSET_AUDIT_WEEKEND.md) | Asset-catalogus per familie + gebruik per scène + **missende texturen** + BlenderKit-toets. |
| [CLEANUP_WEEKEND.md](CLEANUP_WEEKEND.md) + [_cleanup_weekend.ps1](_cleanup_weekend.ps1) + [.gitignore.proposed](.gitignore.proposed) | Opschoonplan. Script staat op `$DryRun=$true` (verplaatst niets tot jij 'm aanzet); quarantaine = 89 `_diag`-bestanden. |
| [HANDOFF_WEEKEND_progress.md](HANDOFF_WEEKEND_progress.md) | Volledig werklog + de kritieke lib-les (bijna R5-gras in R4). |

## JOUW BESLISSINGEN (geparkeerd — ik heb hier niets over beslist)
1. **Zijn de 3 R4-rebuilds goed genoeg als R4?** (fidelity-oordeel op Fable 5). NB:
   het zijn R3 + `apply_r4` met de **getrouwe 2-jul libs**, dus ze missen eventuele
   post-R4-handfixes van 8 jul. Concreet gezien: `zonnebloem_ochtendhoek` mist de
   `Deur_Stoep`-grindfix (rendert als grijze plaat) — die zat wél in de verdwenen
   8-jul R4-blend.
2. **3 blockers = missende texturen** (jasmijn_theehuis + zonnebloem_ochtendhoek delen
   `T_vl0mfbllw_8K`; dahlia_leeshoek `wild_rooibos`). Klaar om te fixen op jouw sein.
3. **magnolia_wintertuin:** winter of vroege lente? (stond al open).
4. **Opschoning:** `_cleanup_weekend.ps1` draaien + `.gitignore.proposed` overnemen?
5. **Sketchfab-compliance:** ~50+ ongetrackte CC-BY-downloads (zie asset-audit).

## Blocker-texturen — waar ze staan (weekend-vervolg, niet gefixt)
Ik heb de 3 blocker-texturen op schijf opgezocht zodat de fix één stap is:
- **`T_vl0mfbllw_8K` (construction_gravel)** — theehuis + ochtendhoek. Bron staat als
  gltf/bin in `assets/sketchfab/path_stones/construction_gravel_vl0mfbllw_8k_ue_raw/`,
  maar NIET als de verwachte `_B/_N.png`. **Aanbevolen fix = de bekende R4-swap
  `PavingStones125A`** (compleet aanwezig in `assets/ambientcg/PavingStones125A/`) —
  die zat al in de 8-jul-R4 van ochtendhoek. (Ik heb dit niet toegepast: materiaalkeuze = jouw stap.)
- **`wild_rooibos_bush_*`** — leeshoek. Model-`.blend` staat er
  (`assets/polyhaven/models/wild_rooibos_bush_2k.blend`); de losse textures ontbreken
  (waarschijnlijk gepackt in dat .blend → relink naar de packed versie, of struik vervangen).

## 3 systemische bevindingen (rode draad over de scènes)
1. **Migratie-texturen** — losgekoppelde/temp-/oude-C:-paden; pack/relink vóór elke final.
2. **Verankering ("staat er random")** — pad ontbreekt/leidt nergens; props los op het gras.
3. **Gras-door-verharding + vlakke roze dawn-waas** — terugkerend; `jasmijn_familietuin`
   is de enige scène met echt gericht licht + schaduwen (referentie).

## Bonus: overkappingen tuin-finals (pre-commit health)
De 4 goedgekeurde tuin-finals (Zwembad/Wellness/Keuken/Vuurtafel) zijn read-only
geprobed: **texture-schoon, geen magenta, AgX+Cycles** — veilig om te committen
wanneer jij dat wil. (Zwembad's 7 "missing" = interne datablocks `Map #N`/`uv colorgrid`,
vals-positief.) Ik heb hier niets aan gewijzigd of gecommit.

*Gemaakt door de autonome weekend-run. Vragen kwamen via Telegram; ik heb geen aannames
als jouw goedkeuring behandeld.*
