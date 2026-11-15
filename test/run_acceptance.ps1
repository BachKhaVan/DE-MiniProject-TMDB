<# Run from repository root or anywhere, with Windows PowerShell 5.1+. #>
[CmdletBinding()]
param(
  [ValidateSet('all','31','32','33','34')][string]$Section = 'all',
  [ValidateSet('readonly','integration')][string]$Mode = 'readonly',
  [switch]$IsolatedConfirmed
)
$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Runner = Join-Path $PSScriptRoot 'acceptance\run.py'
Push-Location $RepoRoot
try {
  $arguments = @($Runner,'--section',$Section,'--mode',$Mode)
  if ($Mode -eq 'integration') {
    if (-not $IsolatedConfirmed) { Write-Error 'Mode integration yeu cau -IsolatedConfirmed va environment co lap'; exit 2 }
    $arguments += '--approved'
  }
  python @arguments
  exit $LASTEXITCODE
} finally { Pop-Location }
