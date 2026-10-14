#!/usr/bin/env bash
# Swap de cabin in alle scenes en render oud + nieuw op dezelfde preview-instellingen.
# Raakt ALLE_FINALS en de pilot-blends niet aan.
#
# Gebruik:  swap_alle_scenes.sh <lijst> [uitvoermap]
#
# De OUD-renders komen altijd uit _tekentool_ab/scenes/ en worden nooit opnieuw
# gedraaid als ze er al staan: de oude scene verandert immers niet. Een tweede
# ronde na een scriptwijziging schrijft dus alleen nieuwe NIEUW-renders, in een
# eigen map, zodat de vorige ronde blijft staan om mee te vergelijken.
set -u
BLENDER="C:/Program Files/Blender Foundation/Blender 5.1/blender.exe"
ROOT="D:/Blender-blokhutten"
OUDDIR="$ROOT/_tekentool_ab/scenes"
UIT="${2:-$OUDDIR}"
GLBDIR="$ROOT/source-glbs-new/2026-09-11"
BREEDTE=1280
SAMPLES=128
mkdir -p "$OUDDIR" "$UIT"

lijst="$1"
[ -f "$lijst" ] || { echo "FOUT: lijst $lijst bestaat niet"; exit 1; }
echo "lijst: $lijst"
echo "oude renders uit: $OUDDIR"
echo "nieuwe renders naar: $UIT"

n=0
while IFS='|' read -r naam blend model; do
  model=${model%%$'\r'}   # vangnet tegen Windows-regeleindes
  [ -z "$naam" ] && continue
  n=$((n+1))
  glb="$GLBDIR/$model.glb"
  echo "=========== [$n] $naam  ($model)"
  if [ ! -f "$glb" ]; then echo "   GLB ONTBREEKT: $glb"; continue; fi

  if [ ! -f "$OUDDIR/${naam}_OUD.png" ]; then
    "$BLENDER" -b "$ROOT/$blend" --python "$ROOT/scripts/swap_cabin_tekentool.py" -- \
      --alleen-render --samples "$SAMPLES" --breedte "$BREEDTE" \
      --uit "$OUDDIR/${naam}_OUD.png" 2>&1 | grep -E "^\[swap\]|Saved|Error" | tail -2
  else
    echo "   OUD bestaat al"
  fi

  if [ ! -f "$UIT/${naam}_NIEUW.png" ]; then
    "$BLENDER" -b "$ROOT/$blend" --python "$ROOT/scripts/swap_cabin_tekentool.py" -- \
      --glb "$glb" --draai180 --samples "$SAMPLES" --breedte "$BREEDTE" \
      --uit "$UIT/${naam}_NIEUW.png" --blend "$UIT/${naam}_NIEUW.blend" 2>&1 \
      | grep -E "^\[swap\]|Saved|Error|Traceback" | tail -8
  else
    echo "   NIEUW bestaat al"
  fi
done < "$lijst"
echo "=========== klaar: $n scenes"
