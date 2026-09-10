#!/bin/bash
# Probe alle scenes uit scenes.py (prio 1 + 2) -> scripts/clips_v2/_probe/<scene>.json ; log ernaast.
cd /d/Blender-blokhutten || exit 1
BL="C:/Program Files/Blender Foundation/Blender 5.1/blender.exe"
OUT=scripts/clips_v2/_probe
mkdir -p "$OUT"
# let op: python op Windows schrijft \r\n -> tr haalt de \r weg, anders "Cannot read file: Invalid argument"
C:/Python312/python.exe -c 'import sys; sys.path.insert(0, "scripts/clips_v2"); import scenes
for k, v in scenes.alle().items(): print(k + "\t" + v["blend"].replace("\\", "/"))' | tr -d '\r' > "$OUT/_lijst.txt"
while IFS=$'\t' read -r naam blend; do
  [ -s "$OUT/$naam.json" ] && { echo "skip $naam"; continue; }
  echo "=== $(date +%H:%M:%S) $naam"
  "$BL" -b "$blend" --python scripts/clips_v2/probe_scene.py -- "$naam" "$OUT/$naam.json" > "$OUT/$naam.log" 2>&1
  grep -E "^\[probe\] $naam|Traceback|Error" "$OUT/$naam.log" | head -3
done < "$OUT/_lijst.txt"
echo "=== PROBE ALLES KLAAR $(date +%H:%M:%S)"
