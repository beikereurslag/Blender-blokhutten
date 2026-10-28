# Renders 2.0 - Regentuinkamer v2: finals-keten (WERKWIJZE_REVIEWLOOP.md, "Finals-keten").
# Alleen starten na Beikes akkoord. Als los proces, zodat er geen tool-timeout op zit:
#   Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','D:\Blender-blokhutten\scenes\regentuinkamer_v2\finals_run.ps1' -WindowStyle Minimized
# Proef (alleen HeroCam, naar renders\finals\_proef\):
#   powershell -NoProfile -ExecutionPolicy Bypass -File finals_run.ps1 -Cams HeroCam -Proef
# Sequentieel, een GPU-job tegelijk. Per final een regel in logs\finals_chain.log (FINAL/KETEN/MISLUKT).
# GPU_BEZET.txt: wachten zolang hij van een ander is; zelf zetten bij start, weghalen aan het eind
# (ook bij falen, via finally). Geen Telegram hier: dat doet de projectsessie.
param(
    [string[]]$Cams = @("HeroCam", "Cam_Bekken", "Cam_Westhoek", "Cam_Close_Bekken", "Cam_Close_Oostborder", "Cam_Close_Zitplek"),
    [string]$TextureLimit = "2048",
    [switch]$Proef
)
$ErrorActionPreference = 'Continue'
$root = "D:\Blender-blokhutten\scenes\regentuinkamer_v2"
$blend = "$root\regentuinkamer_v2.blend"
$blender = "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
$gpuBezet = "D:\Beeldherkenning\GPU_BEZET.txt"
$chainlog = "$root\logs\finals_chain.log"
$doel = if ($Proef) { "$root\renders\finals\_proef" } else { "$root\renders\finals" }
$bezig = "$root\renders\finals\_bezig"
New-Item -ItemType Directory -Force -Path $doel, $bezig, "$root\logs" | Out-Null

function Log($tekst) { "$tekst $(Get-Date -Format 'HH:mm:ss')" | Out-File $chainlog -Append -Encoding utf8 }

Log "KETEN START ($($Cams -join ', '); texture_limit $TextureLimit; proef=$Proef)"
while ((Test-Path $gpuBezet) -and -not ((Get-Content $gpuBezet -Raw) -like "Renders 2.0*")) {
    Log "KETEN WACHT: videokaart bezet volgens GPU_BEZET.txt"
    Start-Sleep -Seconds 60
}
$eigen = $false
$mislukt = 0
try {
    $eind = (Get-Date).AddMinutes(12 * $Cams.Count).ToString('HH:mm')
    $streep = [char]0x2014      # PowerShell 5.1 leest dit bestand als ANSI: geen letterlijk gedachtestreepje
    # zonder BOM: de Python-kant (rtk_dressing.gpu_status) controleert op startswith("Renders 2.0")
    [IO.File]::WriteAllText($gpuBezet, "Renders 2.0 (regentuinkamer_v2) $streep begin $(Get-Date -Format 'HH:mm') $streep verwacht klaar $eind`n", (New-Object Text.UTF8Encoding $false))
    $eigen = $true
    foreach ($cam in $Cams) {
        $t0 = Get-Date
        $tmp = "$bezig\regentuinkamer_v2_$cam.png"
        $dst = "$doel\regentuinkamer_v2_$cam.png"
        Remove-Item $tmp, "$tmp.json" -ErrorAction SilentlyContinue
        & $blender -b $blend --python-exit-code 1 --python "$root\finals_render.py" -- $cam $tmp $TextureLimit *> "$root\logs\final_$cam.log"
        $code = $LASTEXITCODE
        $min = [math]::Round(((Get-Date) - $t0).TotalMinutes, 1)
        if ($code -eq 0 -and (Test-Path $tmp)) {
            Move-Item $tmp $dst -Force
            Move-Item "$tmp.json" "$dst.json" -Force -ErrorAction SilentlyContinue
            $piek = (Get-Content "$dst.json" -Raw | ConvertFrom-Json).cycles_mem_max_mb
            Log "FINAL $cam KLAAR in $min min, Cycles-piek $piek MB -> $dst"
        } else {
            $mislukt++
            Log "FINAL $cam MISLUKT (exit $code, geen output) - zie logs\final_$cam.log"
        }
    }
} finally {
    if ($eigen -and (Test-Path $gpuBezet) -and ((Get-Content $gpuBezet -Raw) -like "Renders 2.0*")) {
        Remove-Item $gpuBezet -Force
    }
    Log "KETEN KLAAR ($mislukt mislukt)"
}
