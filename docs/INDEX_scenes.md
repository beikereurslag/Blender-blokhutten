# Index — alle 16 nieuwe cabin-scenes (2026-06-13)

Twee scenes per cabin-lijn: een **primaire** hero + een **alternatieve stijl**. Alle op 1080p preview;
Zonnebloem-Zomeravond heeft al een finale 2560×1440. Finale renders van de rest pas na jouw review.

| Cabin | Primair (stijl, licht) | Preview | Alternatief (stijl, licht) | Preview |
|---|---|---|---|---|
| **Camelia** 250x300+300 | Buitenbad — scandi-spa, blue hour | `style-hot-tub-premium/camelia_buitenbad_PREVIEW.png` | Wijnterras — mediterraan, namiddag | `style-mediterraan/camelia_wijnterras_PREVIEW.png` |
| **Dahlia** 250x250+300 | Tuinkantoor — modern-urban, ochtend | `style-modern-urban-cottage/dahlia_tuinkantoor_PREVIEW.png` | Leeshoek — scandi, zacht daglicht | `style-scandi/dahlia_leeshoek_PREVIEW.png` |
| **Jasmijn** 300x250+300 | Familietuin — klassiek-familie, middag | `style-klassiek-familie/jasmijn_familietuin_PREVIEW.png` | Theehuis — japandi, ochtend | `style-japandi/jasmijn_theehuis_PREVIEW.png` |
| **Lavendel** 400x300+400 | Lavendelveld — mediterraan, golden hour | `style-mediterraan/lavendel_lavendelveld_PREVIEW.png` | Pluktuin — boerderij, overcast | `style-boerderij/lavendel_pluktuin_PREVIEW.png` |
| **Lelie** 400x250+300 | Ochtendnevel — forest-wilderness, mist/dageraad | `style-forest-wilderness/lelie_ochtendnevel_PREVIEW.png` | Avondkubus — modern, blue hour | `style-modern/lelie_avondkubus_PREVIEW.png` |
| **Magnolia** 300x200 | Groene Long — eco-groendak, helder | `style-eco-groendak/magnolia_groene_long_PREVIEW.png` | Wintertuin — scandi, zacht daglicht | `style-scandi/magnolia_wintertuin_PREVIEW.png` |
| **Roosmarijn** 200x300+400 | Zentuin — japanese-zen, overcast | `style-japanese-zen/roosmarijn_zentuin_PREVIEW.png` | Kruidenterras — mediterraan, namiddag | `style-mediterraan/roosmarijn_kruidenterras_PREVIEW.png` |
| **Zonnebloem** 300x300+300 | Zomeravond — boerderij, sunset ⭐FINAL | `style-boerderij/zonnebloem_zomeravond_HERO_2560x1440.png` | Ochtendhoek — scandi, frisse ochtend | `style-scandi/zonnebloem_ochtendhoek_PREVIEW.png` |

Paden relatief aan `pilots/<Cabin-folder>/`.

## Spreiding (bewust gevarieerd)
- **8 stijlen vertegenwoordigd**: boerderij, modern, scandi, japandi, mediterraan, forest-wilderness, eco-groendak, scandi-spa.
- **Lichtmomenten**: dageraad-mist, frisse ochtend, ochtend, middag, namiddag, golden hour, sunset, blue hour, overcast, helder — breed spectrum.
- **Verhalen**: wellness, werken, gezin, lezen, thee-ritueel, bloemen plukken, koken/kruiden, samen eten, duurzaamheid, contemplatie, natuur.
- Elke cabin-lijn heeft nu twee compleet verschillende sferen → sterke marketing-spreiding.

## Techniek
Alle scenes via `scripts/cabin_lib.py`. Build-scripts in repo-root (`build_*.py`). Review: `docs/REVIEW_alle_scenes.md`.
Finale render-recept (na akkoord): 2560×1440 / 240 samples / OIDN / 16-bit — zie `render_zonnebloem_final.py` als sjabloon.
