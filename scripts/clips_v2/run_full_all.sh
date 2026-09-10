#!/bin/bash
# Nachtrun clips-v2: per scène alle shots op 1920x1080/48 renderen (PNG-reeksen, hervatbaar), daarna encoden
# naar ALLE_FINALS/filmpjes-v2/<clip>.mp4 en een Telegram-melding sturen. Fouten loggen en doorgaan.
#
#   bash run_full_all.sh                 alle prio-1 scenes (volgorde = _lijst.txt, kapschuren/overkappingen erna)
#   bash run_full_all.sh scene1 scene2   alleen deze scenes
#
# Frames: scripts/clips_v2/_frames/<scene>/  (blijven staan voor her-encode).  Log: _frames/<scene>.log
# Klare mp4's worden overgeslagen. Blend wordt nooit opgeslagen. Wacht op een vrije GPU (<25% bezet).
cd /d/Blender-blokhutten || exit 1
BL="C:/Program Files/Blender Foundation/Blender 5.1/blender.exe"
PY=C:/Python312/python.exe
FR=scripts/clips_v2/_frames
UIT=ALLE_FINALS/filmpjes-v2
LIJST=scripts/clips_v2/_probe/_lijst.txt
NOTIFY="D:/Blender-blokhutten/notify.ps1"
mkdir -p "$FR" "$UIT"
# PC wakker houden zolang de run loopt (3 sep: PC viel in slaap midden in de stills-run)
FLAG="$PWD/scripts/clips_v2/_frames/keep_awake.flag"
powershell -ExecutionPolicy Bypass -File scripts/clips_v2/keep_awake.ps1 -Flag "$(cygpath -w "$FLAG")" >/dev/null 2>&1 &
trap 'rm -f "$FLAG"' EXIT

clipnaam() { $PY -c "import sys; sys.path.insert(0,'scripts/clips_v2'); import scenes; print(scenes.alle()['$1']['clip'])" | tr -d '\r'; }
gpu_vrij() {
  local u; u=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
  [ -z "$u" ] || [ "$u" -lt 25 ]
}

while IFS=$'\t' read -r naam blend; do
  if [ $# -gt 0 ]; then case " $* " in *" $naam "*) ;; *) continue;; esac; fi
  clip=$(clipnaam "$naam")
  [ -s "$UIT/$clip.mp4" ] && { echo "klaar: $clip"; continue; }
  until gpu_vrij; do echo "$(date +%H:%M:%S) GPU bezet, wacht..."; sleep 120; done
  echo "=== $(date +%H:%M:%S) START $naam -> $clip"
  "$BL" -b "$blend" --python scripts/clips_v2/render_clip.py -- "$naam" full "$FR/$naam" > "$FR/$naam.log" 2>&1
  if grep -q "SCENE KLAAR" "$FR/$naam.log"; then
    $PY scripts/clips_v2/encode_clip.py "$FR/$naam" "$UIT/$clip.mp4" --fps 24 --fade 12 >> "$FR/$naam.log" 2>&1 \
      && echo "=== $(date +%H:%M:%S) KLAAR $clip" \
      && powershell -ExecutionPolicy Bypass -File "$NOTIFY" -Title "Clip klaar: $clip" \
           -Message "ALLE_FINALS/filmpjes-v2/$clip.mp4 ($(grep -oE '[0-9.]+ s\)' "$FR/$naam.log" | tail -1))" >/dev/null 2>&1
  else
    echo "=== $(date +%H:%M:%S) FOUT $naam (zie $FR/$naam.log)"
    grep -E "Traceback|Error:" "$FR/$naam.log" | head -3
  fi
done < "$LIJST"
echo "=== NACHTRUN KLAAR $(date +%H:%M:%S)"
powershell -ExecutionPolicy Bypass -File "$NOTIFY" -Title "Clips v2: wachtrij klaar" -Message "Alle clips in ALLE_FINALS/filmpjes-v2/" >/dev/null 2>&1
