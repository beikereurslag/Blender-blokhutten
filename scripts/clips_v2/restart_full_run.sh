#!/bin/bash
# Herstart-hulpje voor watchdog.ps1: eigen bestand omdat een inline 'bash -lc "..."' vanuit
# Start-Process stil faalt (getest 4 sep: er werd niets uitgevoerd, geen foutmelding).
cd /d/Blender-blokhutten/scripts/clips_v2 || exit 1
echo "=== watchdog-herstart $(date +'%m-%d %H:%M:%S')" >> _frames/_run_full.log
exec bash run_full_all.sh >> _frames/_run_full.log 2>&1
