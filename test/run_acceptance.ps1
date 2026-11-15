<# Run from repository root or anywhere, with Windows PowerShell 5.1+. #>
[CmdletBinding()]
param(
  [ValidateSet('all','31','32','33','34','35')][string]$Section = 'all',
  [ValidateSet('readonly','integration')][string]$Mode = 'readonly',
  [switch]$IsolatedConfirmed,
  [ValidateSet('unknown','full')][string]$Snapshot = 'unknown',
  [string]$Python = '',
  [string]$EnvFile = ''
)
$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Runner = Join-Path $PSScriptRoot 'acceptance\run.py'
Push-Location $RepoRoot
try {
  if (-not $Python) {
    foreach ($candidate in @('.venv_test\Scripts\python.exe','.venv\Scripts\python.exe')) {
      $full = Join-Path $RepoRoot $candidate
      if (Test-Path -LiteralPath $full) { $Python = $full; break }
    }
    if (-not $Python) { $Python = 'python' }
  }
  $arguments = @($Runner,'--section',$Section,'--mode',$Mode,'--snapshot',$Snapshot)
  if ($EnvFile) { $arguments += @('--env-file',$EnvFile) }
  if ($Mode -eq 'integration') {
    if (-not $IsolatedConfirmed) { Write-Error 'Mode integration yeu cau -IsolatedConfirmed va environment co lap'; exit 2 }
    $arguments += '--approved'
  }
  & $Python @arguments
  exit $LASTEXITCODE
} finally { Pop-Location }
