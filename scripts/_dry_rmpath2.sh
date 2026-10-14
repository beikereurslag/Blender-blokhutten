BL="/c/Program Files/Blender Foundation/Blender 5.1/blender.exe"
R="C:/Users/beike/Documents/Blender-blokhutten"
OUT="$R/scripts/_scratch_dry_rmpath.txt"; : > "$OUT"
declare -a S=(
"Camelia-250x300-300-zijwand/style-hot-tub-premium|camelia_buitenbad"
"Camelia-250x300-300-zijwand/style-mediterraan|camelia_wijnterras"
"Dahlia-250x250-300-zijwand/style-modern-urban-cottage|dahlia_tuinkantoor"
"Dahlia-250x250-300-zijwand/style-scandi|dahlia_leeshoek"
"Jasmijn-300x250-300-zijwand/style-klassiek-familie|jasmijn_familietuin"
"Jasmijn-300x250-300-zijwand/style-japandi|jasmijn_theehuis"
"Lavendel-400x300-400-zijwand/style-boerderij|lavendel_pluktuin"
"Lavendel-400x300-400-zijwand/style-mediterraan|lavendel_lavendelveld"
"Magnolia-300x200/style-scandi|magnolia_wintertuin"
"Roosmarijn-200x300-400-zijwand/style-japanese-zen|roosmarijn_zentuin"
"Roosmarijn-200x300-400-zijwand/style-mediterraan|roosmarijn_kruidenterras"
"Zonnebloem-300x300-300-zijwand/style-boerderij|zonnebloem_zomeravond"
"Zonnebloem-300x300-300-zijwand/style-scandi|zonnebloem_ochtendhoek"
)
for e in "${S[@]}"; do
  dir="${e%%|*}"; sc="${e##*|}"
  echo "===== $sc =====" >> "$OUT"
  "$BL" -b --python "$R/remove_paths_blobs.py" -- "$R/$dir/${sc}_v3.blend" "x" dry > "$R/scripts/_tmp_one.txt" 2>&1
  grep "rmpath" "$R/scripts/_tmp_one.txt" >> "$OUT" || echo "  (geen log)" >> "$OUT"
done
echo "done"
