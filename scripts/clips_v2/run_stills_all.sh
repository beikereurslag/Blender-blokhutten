#!/bin/bash
# Probe-stills (begin/eind per shot, 960x540/24) voor alle scenes -> scripts/clips_v2/_probe/stills/<scene>/
# Hervatbaar: scenes met _shots.json worden overgeslagen. Gebruik: bash run_stills_all.sh [scene ...]
cd /d/Blender-blokhutten || exit 1
BL="C:/Program Files/Blender Foundation/Blender 5.1/blender.exe"
OUT=scripts/clips_v2/_probe/stills
LIJST=scripts/clips_v2/_probe/_lijst.txt
mkdir -p "$OUT"
while IFS=$'\t' read -r naam blend; do
  if [ $# -gt 0 ]; then case " $* " in *" $naam "*) ;; *) continue;; esac; fi
  [ -s "$OUT/$naam/_shots.json" ] && { echo "skip $naam"; continue; }
  echo "=== $(date +%H:%M:%S) $naam"
  "$BL" -b "$blend" --python scripts/clips_v2/render_clip.py -- "$naam" probe "$OUT/$naam" > "$OUT/$naam.log" 2>&1
  grep -E "^\[clip\] [ABC]_|Traceback|Error:" "$OUT/$naam.log" | head -6
done < "$LIJST"
echo "=== STILLS ALLES KLAAR $(date +%H:%M:%S)"
