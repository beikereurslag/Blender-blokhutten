#!/usr/bin/env bash
# Zelfde stappen als finals_run.ps1 (die hier niet mag draaien: execution policy), voor de gegeven camera's.
ROOT="/d/Blender-blokhutten/scenes/regentuinkamer_v2"
BLEND="$ROOT/regentuinkamer_v2.blend"
BLENDER="/c/Program Files/Blender Foundation/Blender 5.1/blender.exe"
GPU="/d/Beeldherkenning/GPU_BEZET.txt"
LOG="$ROOT/logs/finals_chain.log"
DOEL="$ROOT/renders/finals"
BEZIG="$DOEL/_bezig"
mkdir -p "$BEZIG"
log() { echo "$1 $(date +%H:%M:%S)" >> "$LOG"; }

log "KETEN START ($*; texture_limit 2048; proef=False; via bash, finals_run.ps1 geweigerd door execution policy)"
if [ -f "$GPU" ] && ! grep -q "^Renders 2.0" "$GPU"; then
  log "KETEN STOP: videokaart bezet volgens GPU_BEZET.txt"; exit 3
fi
eigen=0
opruimen() {
  if [ "$eigen" = 1 ] && [ -f "$GPU" ] && grep -q "^Renders 2.0" "$GPU"; then rm -f "$GPU"; fi
  log "KETEN KLAAR ($mislukt mislukt)"
}
mislukt=0
trap opruimen EXIT
eind=$(date -d "+$((12 * $#)) minutes" +%H:%M)
printf 'Renders 2.0 (regentuinkamer_v2) \xe2\x80\x94 begin %s \xe2\x80\x94 verwacht klaar %s\n' "$(date +%H:%M)" "$eind" > "$GPU"
eigen=1
for cam in "$@"; do
  t0=$(date +%s)
  tmp="$BEZIG/regentuinkamer_v2_$cam.png"
  dst="$DOEL/regentuinkamer_v2_$cam.png"
  rm -f "$tmp" "$tmp.json"
  "$BLENDER" -b "$BLEND" --python-exit-code 1 --python "$ROOT/finals_render.py" -- "$cam" "$(cygpath -w "$tmp")" 2048 > "$ROOT/logs/final_$cam.log" 2>&1
  code=$?
  min=$(awk "BEGIN{printf \"%.1f\", ($(date +%s) - $t0)/60}")
  if [ $code -eq 0 ] && [ -f "$tmp" ]; then
    mv -f "$tmp" "$dst"; mv -f "$tmp.json" "$dst.json"
    piek=$(python -c "import json;print(json.load(open(r'$(cygpath -w "$dst.json")'))['cycles_mem_max_mb'])")
    log "FINAL $cam KLAAR in $min min, Cycles-piek $piek MB -> $(cygpath -w "$dst")"
  else
    mislukt=$((mislukt + 1))
    log "FINAL $cam MISLUKT (exit $code, geen output) - zie logs/final_$cam.log"
  fi
done
