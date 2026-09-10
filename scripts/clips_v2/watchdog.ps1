# watchdog.ps1 - houdt de clips-v2 weekendrun in de lucht (4-10 sep 2026).
#
# Beike is van vr 4 sep t/m do 10 sep weg en de run duurt ~105 uur. Zonder toezicht is een
# Windows-Update-herstart (Patch Tuesday valt op 8 sep) genoeg om de hele week stil te leggen.
# Deze taak draait elk half uur en:
#   1. herstart run_full_all.sh als er geen runner en geen renderende Blender meer is
#      (de run is hervatbaar: klare mp4's worden overgeslagen, bestaande PNG's blijven staan);
#   2. stuurt een Telegram-melding voor elke scene die met FOUT eindigde - de runner zelf meldt
#      alleen geslaagde clips, dus zonder dit zie je een mislukte scene pas donderdag;
#   3. stopt met starten zodra alle scenes uit _lijst.txt een mp4 hebben.
#
# Handmatig testen:  powershell -ExecutionPolicy Bypass -File watchdog.ps1
# Taak verwijderen:  Unregister-ScheduledTask -TaskName 'clips-v2-watchdog' -Confirm:$false
$ErrorActionPreference = 'Stop'
$HIER   = 'D:\Blender-blokhutten\scripts\clips_v2'
$FRAMES = Join-Path $HIER '_frames'
$LOG    = Join-Path $FRAMES '_watchdog.log'
$RUNLOG = Join-Path $FRAMES '_run_full.log'
$GEMELD = Join-Path $FRAMES '_watchdog_gemeld.txt'
$UIT    = 'D:\Blender-blokhutten\ALLE_FINALS\filmpjes-v2'
$NOTIFY = 'D:\Blender-blokhutten\notify.ps1'
$BASH   = 'C:\Program Files\Git\bin\bash.exe'

function Log([string] $t) { Add-Content -Path $LOG -Value ("{0}  {1}" -f (Get-Date -Format 'MM-dd HH:mm:ss'), $t) -Encoding utf8 }

if (-not (Test-Path $FRAMES)) { New-Item -ItemType Directory -Force -Path $FRAMES | Out-Null }

# --- 1. mislukte scenes melden (eenmalig per regel) -------------------------------------------
if (Test-Path $RUNLOG) {
    $al = if (Test-Path $GEMELD) { Get-Content $GEMELD } else { @() }
    foreach ($regel in (Select-String -Path $RUNLOG -Pattern 'FOUT' -SimpleMatch | ForEach-Object { $_.Line.Trim() })) {
        if ($al -notcontains $regel) {
            Log "melding: $regel"
            & $NOTIFY -Title 'Clips v2: scene mislukt' -Message "$regel`n`nZie scripts/clips_v2/_frames/<scene>.log. De wachtrij loopt door met de volgende scene."
            Add-Content -Path $GEMELD -Value $regel -Encoding utf8
        }
    }
}

# --- 1b. python-fouten in een scene-log melden (vangt een mislukte encode) --------------------
# De runner meldt alleen geslaagde clips. Als render_clip of encode_clip struikelt loopt hij door naar
# de volgende scene en zou je dat pas donderdag zien. Een Traceback in een scene-log is het signaal.
foreach ($f in (Get-ChildItem -Path $FRAMES -Filter '*.log' -ErrorAction SilentlyContinue)) {
    if ($f.Name -like '_*') { continue }
    if (-not (Select-String -Path $f.FullName -Pattern 'Traceback' -SimpleMatch -Quiet)) { continue }
    $sleutel = "traceback:$($f.Name)"
    $al = if (Test-Path $GEMELD) { Get-Content $GEMELD } else { @() }
    if ($al -contains $sleutel) { continue }
    Log "melding: $sleutel"
    & $NOTIFY -Title 'Clips v2: fout in een scene' -Message "$($f.BaseName) gaf een Traceback (render of encode). De wachtrij loopt door; frames blijven staan, dus opnieuw encoden kan later."
    Add-Content -Path $GEMELD -Value $sleutel -Encoding utf8
}

# --- 2. is alles al klaar? --------------------------------------------------------------------
$lijst = Get-Content (Join-Path $HIER '_probe\_lijst.txt') | Where-Object { $_.Trim() }
$klaar = (Get-ChildItem -Path $UIT -Filter '*.mp4' -ErrorAction SilentlyContinue).Count
if ($klaar -ge $lijst.Count) { Log "alles klaar ($klaar/$($lijst.Count) clips) - niets te doen"; exit 0 }

# --- 3. loopt de run nog? ---------------------------------------------------------------------
$procs  = Get-CimInstance Win32_Process -Filter "Name='bash.exe' OR Name='blender.exe'"
$runner = $procs | Where-Object { $_.CommandLine -like '*run_full_all*' }
$render = $procs | Where-Object { $_.CommandLine -like '*render_clip.py*' }
if ($runner -or $render) { exit 0 }

# --- 4. herstarten ----------------------------------------------------------------------------
Log "geen runner en geen render actief bij $klaar/$($lijst.Count) clips - run_full_all.sh herstarten"
# Let op: een inline 'bash -lc "..."' faalt hier stil (getest 4 sep, er gebeurde niets en er kwam
# geen foutmelding). Daarom een eigen scriptbestand.
Start-Process -FilePath $BASH -WindowStyle Hidden -ArgumentList (Join-Path $HIER 'restart_full_run.sh')
& $NOTIFY -Title 'Clips v2: run herstart' -Message "De renderrun lag stil (waarschijnlijk een herstart) en is opnieuw gestart bij $klaar van $($lijst.Count) clips. Hervat waar hij gebleven was."
