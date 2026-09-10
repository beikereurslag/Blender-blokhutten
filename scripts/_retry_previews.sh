BL="/c/Program Files/Blender Foundation/Blender 5.1/blender.exe"
R="C:/Users/beike/Documents/Blender-blokhutten"
declare -a S=(
"pilots/Magnolia-300x200/style-scandi|magnolia_wintertuin"
"pilots/Camelia-250x300-300-zijwand/style-mediterraan|camelia_wijnterras"
"pilots/Lavendel-400x300-400-zijwand/style-mediterraan|lavendel_lavendelveld"
"pilots/Roosmarijn-200x300-400-zijwand/style-japanese-zen|roosmarijn_zentuin"
)
for e in "${S[@]}"; do
  dir="${e%%|*}"; sc="${e##*|}"
  echo "===== RENDER $sc ====="
  "$BL" -b --python "$R/scripts/render_final.py" -- "$R/$dir/${sc}_v3.blend" "$R/$dir/${sc}_REVIEW_PREVIEW.png" 130 1600 900 2>&1 | grep -E "\[final\]|Error|CUDA|illegal" | tail -3 || echo "  (faalde weer: $sc)"
done
echo "RETRY_DONE"
