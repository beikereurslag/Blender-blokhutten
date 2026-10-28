#!/usr/bin/env bash
BL="/c/Program Files/Blender Foundation/Blender 5.1/blender.exe"
R="C:/Users/beike/Documents/Blender-blokhutten"
declare -a S=(
"pilots/Camelia-250x300-300-zijwand/style-hot-tub-premium|camelia_buitenbad"
"pilots/Camelia-250x300-300-zijwand/style-mediterraan|camelia_wijnterras"
"pilots/Dahlia-250x250-300-zijwand/style-modern-urban-cottage|dahlia_tuinkantoor"
"pilots/Dahlia-250x250-300-zijwand/style-scandi|dahlia_leeshoek"
"pilots/Jasmijn-300x250-300-zijwand/style-klassiek-familie|jasmijn_familietuin"
"pilots/Lavendel-400x300-400-zijwand/style-boerderij|lavendel_pluktuin"
"pilots/Lavendel-400x300-400-zijwand/style-mediterraan|lavendel_lavendelveld"
"pilots/Magnolia-300x200/style-scandi|magnolia_wintertuin"
"pilots/Roosmarijn-200x300-400-zijwand/style-japanese-zen|roosmarijn_zentuin"
"pilots/Roosmarijn-200x300-400-zijwand/style-mediterraan|roosmarijn_kruidenterras"
"pilots/Zonnebloem-300x300-300-zijwand/style-boerderij|zonnebloem_zomeravond"
"pilots/Zonnebloem-300x300-300-zijwand/style-scandi|zonnebloem_ochtendhoek"
)
for entry in "${S[@]}"; do
  dir="${entry%%|*}"; sc="${entry##*|}"
  v2="$R/$dir/${sc}_v2.blend"; v3="$R/$dir/${sc}_v3.blend"; png="$R/$dir/${sc}_REVIEW_PREVIEW.png"
  echo "===== FIX $sc ====="
  "$BL" -b --python "$R/fix_ground_generic.py" -- "$v2" "$v3" 2>&1 | grep -E "\[ground\]|Error|Traceback" || echo "  (fix-fout $sc)"
  echo "===== PREVIEW $sc ====="
  "$BL" -b --python "$R/scripts/render_final.py" -- "$v3" "$png" 130 1600 900 2>&1 | grep -E "\[final\]" || echo "  (render-fout $sc)"
done
echo "BATCH_DONE"
