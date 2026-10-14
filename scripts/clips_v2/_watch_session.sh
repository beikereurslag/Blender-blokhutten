#!/bin/bash
# Sessie-waakhond voor de clips_v2-nachtrun (4 sep, sessie die Beike aan liet staan).
# Emit ALLEEN regels die actie verdienen; stilte = alles loopt. Vult watchdog.ps1 aan
# (die herstart + Telegram doet); dit is het oog en oor van de Claude-sessie zelf.
cd /d/Blender-blokhutten/scripts/clips_v2 || exit 1
LOG=_frames/_run_full.log
seen=$(wc -l < "$LOG" 2>/dev/null || echo 0)
stall_gemeld=0
squat_gemeld=0
tb_gemeld=""
while true; do
  # 1. nieuwe runner-regels (START / KLAAR / FOUT), GPU-wachtregels onderdrukt
  tot=$(wc -l < "$LOG" 2>/dev/null || echo 0)
  if [ "$tot" -gt "$seen" ]; then
    sed -n "$((seen+1)),${tot}p" "$LOG" 2>/dev/null | grep -E "START |KLAAR|FOUT" | grep -v "GPU bezet" || true
    seen=$tot
  fi
  laatste=$(tail -1 "$LOG" 2>/dev/null || echo "")
  af=$(grep -c "NACHTRUN KLAAR" "$LOG" 2>/dev/null || echo 0)

  # 2. stilstand: geen nieuw frame in 25 min terwijl de run niet op de GPU wacht en niet af is
  if [ "$af" -eq 0 ] && ! echo "$laatste" | grep -q "GPU bezet"; then
    versfr=$(find _frames -name '*.png' -newermt '-25 minutes' 2>/dev/null | head -1)
    if [ -z "$versfr" ]; then
      [ "$stall_gemeld" -eq 0 ] && echo "STILSTAND $(date +%H:%M) - geen nieuw frame in 25 min, runner wacht niet op GPU. Laatste log: $laatste"
      stall_gemeld=1
    else
      stall_gemeld=0
    fi
  fi

  # 3. extra GPU-slurper: meer dan 2 headless Blenders op de 3070 = OOM-risico
  nb=$(tasklist /FI "IMAGENAME eq blender.exe" /FO CSV /NH 2>/dev/null | grep -c blender || echo 0)
  if [ "$nb" -gt 2 ]; then
    [ "$squat_gemeld" -eq 0 ] && echo "GPU-DRUKTE $(date +%H:%M) - $nb Blenders actief (>2). Nachtrun wordt uitgehongerd; kijk welke erbij hoort."
    squat_gemeld=1
  else
    squat_gemeld=0
  fi

  # 4. Traceback in een scene-log (mislukte encode valt anders niet op)
  for f in _frames/*.log; do
    [ -f "$f" ] || continue
    if grep -q "Traceback" "$f" 2>/dev/null && ! echo "$tb_gemeld" | grep -q "$f"; then
      echo "TRACEBACK $(date +%H:%M) in $f: $(grep -m1 -A2 Traceback "$f" | tail -1)"
      tb_gemeld="$tb_gemeld $f"
    fi
  done

  [ "$af" -gt 0 ] && { echo "NACHTRUN AF $(date +%H:%M) - alle scenes verwerkt, log zegt NACHTRUN KLAAR"; exit 0; }
  sleep 600
done
