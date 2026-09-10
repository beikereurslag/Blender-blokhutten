# Houdt de PC wakker zolang het vlagbestand bestaat (SetThreadExecutionState, alleen dit proces - geen
# systeeminstelling). Gebruik vanuit een runner:
#   powershell -ExecutionPolicy Bypass -File keep_awake.ps1 -Flag "<pad>\keep_awake.flag"   (op de achtergrond)
#   ... en verwijder het vlagbestand als de run klaar is.
# Aanleiding: de stills-run van 3 sep stond van 17:11 tot 09:39 stil omdat de PC in slaap viel.
param([Parameter(Mandatory = $true)] [string] $Flag)
Add-Type -Namespace Win -Name Power -MemberDefinition @'
[DllImport("kernel32.dll", SetLastError = true)]
public static extern uint SetThreadExecutionState(uint esFlags);
'@
$ES_CONTINUOUS = [uint32]0x80000000
$ES_SYSTEM_REQUIRED = [uint32]0x00000001
# -bor promoveert naar int64 en dan faalt de P/Invoke-cast (InvalidCastException) -> expliciet
# terugcasten naar uint32. Zonder dit stierf de watcher op zijn eerste ronde: het vlagbestand
# stond er wel, maar de PC bleef gewoon in slaap vallen (gevonden 4 sep).
$WAKKER = [uint32]($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED)
New-Item -ItemType File -Force -Path $Flag | Out-Null
while (Test-Path $Flag) {
    [Win.Power]::SetThreadExecutionState($WAKKER) | Out-Null
    Start-Sleep -Seconds 50
}
[Win.Power]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null
