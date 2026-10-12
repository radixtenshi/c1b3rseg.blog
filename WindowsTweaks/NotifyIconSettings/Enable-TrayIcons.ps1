#Requires -Version 5.1
<#
.SYNOPSIS
    Promotes new Windows 11 system tray icons to "On" automatically.
.DESCRIPTION
    Windows 11 22H2+ hides new tray icons by default (Settings > Personalization >
    Taskbar > Other system tray icons). This script sets IsPromoted=1 for icons
    with no explicit user choice, and for brand-new entries that appear hidden.
    Icons the user explicitly turned Off (IsPromoted=0) are left untouched,
    tracked via a JSON snapshot of known registry subkeys.
.NOTES
    Registry: HKCU:\Control Panel\NotifyIconSettings\<id>\IsPromoted (DWORD)
    Absent value = never touched by the user (hidden by default).
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$basePath  = 'HKCU:\Control Panel\NotifyIconSettings'
$stateFile = Join-Path $PSScriptRoot 'tray-icons-state.json'
$logFile   = Join-Path $PSScriptRoot 'Enable-TrayIcons.log'

function Write-Log([string]$Message) {
    '{0} {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message |
        Add-Content -LiteralPath $logFile -Encoding UTF8
}

$subs = @(Get-ChildItem -LiteralPath $basePath)

$known = $null
if (Test-Path -LiteralPath $stateFile) {
    $known = [System.Collections.Generic.HashSet[string]]::new(
        [string[]](Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json))
}

$promoted = [System.Collections.Generic.List[string]]::new()

foreach ($sub in $subs) {
    $props   = $sub.GetValueNames()
    $hasFlag = $props -contains 'IsPromoted'
    $isKnown = $null -ne $known -and $known.Contains($sub.PSChildName)

    # Promote when: no value yet (user never touched it), or new entry still at 0.
    $mustPromote = (-not $hasFlag) -or (-not $isKnown -and $sub.GetValue('IsPromoted') -eq 0)
    if ($mustPromote) {
        New-ItemProperty -LiteralPath $sub.PSPath -Name IsPromoted `
            -PropertyType DWord -Value 1 -Force | Out-Null
        $exe = if ($props -contains 'ExecutablePath') {
            ($sub.GetValue('ExecutablePath') -split '\\')[-1]
        } else {
            $sub.PSChildName
        }
        $promoted.Add($exe)
    }
}

$subs.PSChildName | ConvertTo-Json | Set-Content -LiteralPath $stateFile -Encoding UTF8

if ($promoted.Count -gt 0) {
    Write-Log ('Promoted {0} icon(s): {1}' -f $promoted.Count, ($promoted -join ', '))
}
