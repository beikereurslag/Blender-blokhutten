# Renders 2.0 - Regentuinkamer v2, stap 0: assets binnenhalen (plan §3, bouwvolgorde stap 2).
# Draaien:  powershell -ExecutionPolicy Bypass -File stap0_assets.ps1
# - BlenderKit: per asset-ID één keer pilots\_bk_fetch.py (headless), doelmap assets\blenderkit\renders2\
# - PolyHaven: grey_stone_path 2k (diff/rough/nor_gl/disp) naar assets\polyhaven\textures\grey_stone_path\
# Bestaat een download al, dan wordt hij overgeslagen (herhaalbaar).
# Een mislukte download stopt het script niet: hij komt als FOUT in het log en in
# logs\stap0_assets.json, zodat stap1 de terugval uit het plan kan nemen.

$ErrorActionPreference = "Stop"
$Root    = "D:\Blender-blokhutten"
$Blender = "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
$Scene   = "$Root\scenes\regentuinkamer_v2"
$Log     = "$Scene\logs\stap0_assets.log"
$Json    = "$Scene\logs\stap0_assets.json"
$BkDir   = "$Root\assets\blenderkit\renders2"
$PhDir   = "$Root\assets\polyhaven\textures\grey_stone_path"

$IdDir   = "$BkDir\.ids"
New-Item -ItemType Directory -Force -Path "$Scene\logs", $BkDir, $PhDir, $IdDir | Out-Null

function Log($m) {
    $regel = "[{0}] {1}" -f (Get-Date -Format "HH:mm:ss"), $m
    Write-Host $regel
    Add-Content -Path $Log -Value $regel -Encoding UTF8
}

# Volgorde en ID's uit plan §3
$Assets = @(
    @{ rol = "ring1";      id = "caa82c72-91c1-402b-a23f-653a31fb8a60"; naam = "Tree Fagus Sylvatica09" },
    @{ rol = "ring1";      id = "4c89fc98-7e5a-4362-9523-dadf6717a9bd"; naam = "European Maple Acer Campreste" },
    @{ rol = "ring2";      id = "4986c7f3-f564-4e0b-afd3-6ef0247c1055"; naam = "Tree Fagus Sylvatica05" },
    @{ rol = "ring2";      id = "9bdd29e6-5022-4dba-911a-ec0e15bcb196"; naam = "Tree Fagus Grandifolia05" },
    @{ rol = "ring2";      id = "288d4b10-b252-408a-9b34-862b56f37a25"; naam = "European Maple Acer Platanoide" },
    @{ rol = "haag";       id = "8d7ae4d8-cb9c-4063-96e7-8904e14124b0"; naam = "Cotoneaster" },
    @{ rol = "gazon";      id = "af46ecce-d6b7-4655-b24a-972a27c1dc7f"; naam = "Mown Grass Large area" },
    @{ rol = "ring4";      id = "f93c7f44-18c8-42c2-a4c3-9c03b69aa7d5"; naam = "Greenleaf Treeline Backdrop 001" },
    @{ rol = "berk_reserve"; id = "0282c2fa-b532-4c53-89fc-d889d4f71167"; naam = "Multi-stem Deciduous Tree" },
    # dressing laag 3 (borders, plan §3): witte bloei
    @{ rol = "border";     id = "17cff3d0-8f44-4a2a-86f5-adbaacff17c3"; naam = "Abelia grandiflora" }
)

Log "=== stap0 start ==="
$Uitkomst = @()

foreach ($a in $Assets) {
    # Licentie en bestandsnaam opvragen bij de publieke zoek-API (dezelfde die _bk_fetch gebruikt)
    $info = $null
    try {
        $q = [uri]::EscapeDataString("asset_base_id:$($a.id) asset_type:model")
        $r = Invoke-RestMethod -Uri "https://www.blenderkit.com/api/v1/search/?query=$q&page_size=2" -TimeoutSec 30
        $info = $r.results | Select-Object -First 1
    } catch {
        Log "  zoek-API faalde voor $($a.naam): $($_.Exception.Message)"
    }
    $bestand = $null
    if ($info) {
        $schoon = (($info.name.ToCharArray() | ForEach-Object { if ([char]::IsLetterOrDigit($_) -or $_ -in @('_', '-', ' ')) { $_ } else { '_' } }) -join '').Trim().Replace(' ', '_')
        $bestand = Join-Path $BkDir "$schoon.blend"
    }
    $rec = [ordered]@{ rol = $a.rol; id = $a.id; naam_plan = $a.naam;
                       naam_bk = $(if ($info) { $info.name } else { $null });
                       licentie = $(if ($info) { $info.license } else { $null });
                       is_free = $(if ($info) { $info.isFree } else { $null });
                       bestand = $bestand; status = "" }

    # Overslaan op asset-ID: na een geslaagde download staat er een marker .ids\<id>.txt met het
    # pad (de bestandsnaam uit de API wijkt soms af van die op schijf, bv. Cotoneáster).
    $marker = Join-Path $IdDir "$($a.id).txt"
    if (Test-Path $marker) {
        $gemarkeerd = (Get-Content $marker -Encoding UTF8 -TotalCount 1).Trim()
        if ((Test-Path -LiteralPath $gemarkeerd) -and ((Get-Item -LiteralPath $gemarkeerd).Length -gt 10000)) {
            $bestand = $gemarkeerd
        }
    }
    if ($bestand -and (Test-Path -LiteralPath $bestand) -and ((Get-Item -LiteralPath $bestand).Length -gt 10000)) {
        Log "OVERGESLAGEN (staat er al): $($a.naam) -> $bestand"
        [IO.File]::WriteAllText($marker, $bestand, (New-Object Text.UTF8Encoding $false))
        $rec.bestand = $bestand
        $rec.status = "al aanwezig"
        $Uitkomst += [pscustomobject]$rec
        continue
    }

    Log "download $($a.rol): $($a.naam) ($($a.id))"
    $runlog = "$Scene\logs\stap0_bk_$($a.id.Substring(0,8)).log"
    # Start-Process i.p.v. & ... *> : PowerShell 5.1 schrijft dat als UTF-16 en maakt van
    # Blender-stderr een afbrekende fout. Niet -Wait: dat wacht ook op de BlenderKit-client
    # die Blender start en die nog minuten blijft draaien. WaitForExit wacht alleen op Blender.
    $p = Start-Process -FilePath $Blender -PassThru -NoNewWindow `
        -ArgumentList @("-b", "--python", "`"$Root\pilots\_bk_fetch.py`"", "--", "`"asset_base_id:$($a.id)`"", "renders2") `
        -RedirectStandardOutput $runlog -RedirectStandardError "$runlog.err"
    $null = $p.Handle   # PS 5.1: zonder handle blijft ExitCode leeg
    $p.WaitForExit()
    $code = $p.ExitCode
    $klaar = Select-String -Path $runlog -Pattern "\[bkfetch\]   klaar: (.+) \(" | Select-Object -Last 1
    if ($klaar) {
        $pad = $klaar.Matches[0].Groups[1].Value
        $rec.bestand = $pad
        $rec.status = "gedownload"
        [IO.File]::WriteAllText((Join-Path $IdDir "$($a.id).txt"), $pad, (New-Object Text.UTF8Encoding $false))
        Log "  OK -> $pad"
    } else {
        $rec.status = "FOUT (exit $code), zie $runlog"
        $staart = (Get-Content $runlog -Tail 6) -join " | "
        Log "  FOUT: $($a.naam) niet gedownload (exit $code). Laatste regels: $staart"
    }
    $Uitkomst += [pscustomobject]$rec
}

# PolyHaven grey_stone_path (CC0), URL's via de API
try {
    $files = Invoke-RestMethod -Uri "https://api.polyhaven.com/files/grey_stone_path" -TimeoutSec 30
    $kaarten = @{ Diffuse = $files.Diffuse.'2k'.jpg.url; Rough = $files.Rough.'2k'.jpg.url;
                  nor_gl = $files.nor_gl.'2k'.jpg.url; Displacement = $files.Displacement.'2k'.jpg.url }
    foreach ($k in $kaarten.Keys) {
        $url = $kaarten[$k]
        $doel = Join-Path $PhDir ([IO.Path]::GetFileName($url))
        if ((Test-Path $doel) -and ((Get-Item $doel).Length -gt 10000)) {
            Log "OVERGESLAGEN (staat er al): $doel"
        } else {
            Invoke-WebRequest -Uri $url -OutFile $doel -TimeoutSec 120
            Log "PH $k -> $doel ($([int]((Get-Item $doel).Length / 1KB)) kB)"
        }
    }
    $Uitkomst += [pscustomobject]@{ rol = "pad"; id = "polyhaven:grey_stone_path"; naam_plan = "grey_stone_path";
                                     naam_bk = $null; licentie = "CC0"; is_free = $true; bestand = $PhDir; status = "gedownload" }
} catch {
    Log "FOUT PolyHaven grey_stone_path: $($_.Exception.Message)"
    $Uitkomst += [pscustomobject]@{ rol = "pad"; id = "polyhaven:grey_stone_path"; naam_plan = "grey_stone_path";
                                     naam_bk = $null; licentie = "CC0"; is_free = $true; bestand = $null; status = "FOUT" }
}

# zonder BOM: Set-Content -Encoding UTF8 zet er in PS 5.1 een BOM voor (json.load faalt dan)
[IO.File]::WriteAllText($Json, ($Uitkomst | ConvertTo-Json -Depth 4), (New-Object Text.UTF8Encoding $false))
$fout = @($Uitkomst | Where-Object { $_.status -like "FOUT*" }).Count
Log "=== stap0 klaar: $($Uitkomst.Count) assets, $fout fout(en). Overzicht: $Json ==="
