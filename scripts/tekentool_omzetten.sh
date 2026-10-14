#!/usr/bin/env bash
# Zet scenes om naar de nieuwe tekentool-modellen (okt 2026) en controleert ze.
#
#   bash scripts/tekentool_omzetten.sh <naam> [<naam> ...]
#
# Namen komen uit scripts/scenes.txt (naam|bronblend|model). Per scene:
#   1. swap_cabin_tekentool.py: nieuwe cabin erin, verslag + validatie voor/na,
#      opslaan als <bronblend zonder .blend>_TEKENTOOL.blend naast de bron
#   2. tekentool_controle.py: toets het verslag, proefrender 1080p met de
#      hero-camera, hoektest rond de cabin
#   3. de OUDE scene op dezelfde instellingen (oud_1080.png), zodat elk verschil
#      in het beeld aan de swap toe te schrijven is en niet aan andere instellingen
# Uitvoer per scene in _tekentool_2026-10/<naam>/. De bronblend blijft onaangeroerd.
# Renders strikt na elkaar: parallel crasht de GPU.
set -u
BLENDER="C:/Program Files/Blender Foundation/Blender 5.1/blender.exe"
ROOT="D:/Blender-blokhutten"
GLBDIR="$ROOT/source-glbs-new/2026-09-11"
UITROOT="$ROOT/_tekentool_2026-10"

for naam in "$@"; do
  regel=$(grep -E "^${naam}\|" "$ROOT/scripts/scenes.txt" | tr -d '\r')
  if [ -z "$regel" ]; then echo "FOUT: $naam staat niet in scripts/scenes.txt"; continue; fi
  IFS='|' read -r _ blend model <<< "$regel"
  glb="$GLBDIR/$model.glb"
  nieuw="$ROOT/${blend%.blend}_TEKENTOOL.blend"
  uit="$UITROOT/$naam"
  mkdir -p "$uit"
  echo "=========== $naam  ($model)"
  [ -f "$glb" ] || { echo "FOUT: GLB ontbreekt: $glb"; continue; }

  "$BLENDER" -b "$ROOT/$blend" --python "$ROOT/scripts/swap_cabin_tekentool.py" -- \
    --glb "$glb" --draai180 --geen-render --uit "$uit/ongebruikt.png" \
    --verslag "$uit/swap.json" --blend "$nieuw" > "$uit/swap.log" 2>&1
  grep -E "^\[swap\]|Traceback|Error" "$uit/swap.log" | grep -v "materialen uit de scene" | tail -12
  [ -f "$uit/swap.json" ] && [ -f "$nieuw" ] || { echo "FOUT: swap mislukt, zie $uit/swap.log"; continue; }

  "$BLENDER" -b "$nieuw" --python "$ROOT/scripts/tekentool_controle.py" -- \
    --verslag "$uit/swap.json" --out "$uit" > "$uit/controle.log" 2>&1
  grep -E "^\[controle\]|Traceback|Error" "$uit/controle.log" | tail -12

  if [ ! -f "$uit/oud_1080.png" ]; then
    "$BLENDER" -b "$ROOT/$blend" --python "$ROOT/scripts/swap_cabin_tekentool.py" --       --alleen-render --samples 256 --breedte 1920 --uit "$uit/oud_1080.png" > "$uit/oud.log" 2>&1
    [ -f "$uit/oud_1080.png" ] && echo "   oud_1080.png klaar" || echo "FOUT: oude render mislukt, zie $uit/oud.log"
  fi
done
echo "=========== klaar"
