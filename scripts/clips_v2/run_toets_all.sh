#!/bin/bash
# Hero-toets voor alle scenes ZONDER te renderen -> scripts/clips_v2/_probe/toets/<scene>/
# Kost alleen het laden van de blend (~60-90 s/scene, geen GPU, geen VRAM), dus veilig naast ander werk.
# Nodig omdat de C-verdicts van de stills-pass tegen een verkeerde referentie zijn gemeten
# (reset_cam miste view_layer.update(), gefixt 4 sep 11:37:47) en omdat geo.py daarna is gerepareerd
# (mist laat de straal door, vignet-ranking mikt niet meer op vloeren).
# Hervatbaar: scenes met _toets.json worden overgeslagen. Gebruik: bash run_toets_all.sh [scene ...]
cd /d/Blender-blokhutten || exit 1
BL="C:/Program Files/Blender Foundation/Blender 5.1/blender.exe"
OUT=scripts/clips_v2/_probe/toets
LIJST=scripts/clips_v2/_probe/_lijst.txt
mkdir -p "$OUT"
FLAG="$(pwd)/$OUT/keep_awake.flag"
powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File scripts/clips_v2/keep_awake.ps1 -Flag "$FLAG" &
KA=$!
trap 'rm -f "$FLAG"; kill $KA 2>/dev/null' EXIT
while IFS=$'\t' read -r naam blend; do
  if [ $# -gt 0 ]; then case " $* " in *" $naam "*) ;; *) continue;; esac; fi
  [ -s "$OUT/$naam/_toets.json" ] && { echo "skip $naam"; continue; }
  echo "=== $(date +%H:%M:%S) $naam"
  "$BL" -b "$blend" --python scripts/clips_v2/render_clip.py -- "$naam" toets "$OUT/$naam" > "$OUT/$naam.log" 2>&1
  grep -E "^\[clip\] ([ABC]_|ontbrekende textures)|Traceback|Error:" "$OUT/$naam.log" | head -8
done < "$LIJST"
rm -f "$FLAG"
echo "=== TOETS ALLES KLAAR $(date +%H:%M:%S)"
