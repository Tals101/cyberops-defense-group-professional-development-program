# Ticket 010 - V1 Configuration Preflight
# No deployment is performed.

param(
    [Parameter(Mandatory=$true)]
    [string]$ManifestPath,

    [Parameter(Mandatory=$true)]
    [ValidatePattern('^[a-zA-Z0-9-]+$')]
    [string]$TestId
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

try {
    $manifest = (Resolve-Path -LiteralPath $ManifestPath).Path
    $reportPath = Join-Path $root "evidence\v1-preflight-$TestId.json"

    Write-Output "STAGE 1: Fresh Trivy configuration scan"

    trivy config --format json --output $reportPath $manifest

    if ($LASTEXITCODE -ne 0) {
        throw "Trivy scan execution failed."
    }

    $report = Get-Content $reportPath -Raw | ConvertFrom-Json

    if (-not $report.Results) {
        throw "Missing or empty scan results."
    }

    Write-Output "STAGE 2: Workload security policy"

    $policy = Join-Path $PSScriptRoot "v1-policy-gate.ps1"

    & powershell.exe -NoProfile -File $policy -ReportPath $reportPath

    $policyExit = $LASTEXITCODE

    Write-Output "STAGE 3: Image digest policy"

    $digestGate = Join-Path $PSScriptRoot "v1-image-digest-gate.ps1"

    & powershell.exe -NoProfile -File $digestGate -ManifestPath $manifest

    $digestExit = $LASTEXITCODE

    Write-Output "STAGE 4: Untrusted registry findings"

    $untrusted = @(
        $report.Results |
        ForEach-Object { $_.Misconfigurations } |
        Where-Object { $null -ne $_ -and $_.ID -eq "KSV-0125" }
    )

    foreach ($finding in $untrusted) {
        Write-Output "BLOCK: KSV-0125 - Untrusted registry finding"
    }

    if ($policyExit -notin @(0,1) -or $digestExit -notin @(0,1)) {
        throw "One or more policy engines failed."
    }

    if ($policyExit -ne 0 -or $digestExit -ne 0 -or $untrusted.Count -gt 0) {
        Write-Output "V1 CONFIGURATION PREFLIGHT: BLOCK"
        exit 1
    }

    Write-Output "V1 CONFIGURATION PREFLIGHT: CHECKS PASSED"
    Write-Output "NOT RELEASE AUTHORIZATION - Additional controls pending"
    exit 0
}
catch {
    Write-Output "V1 CONFIGURATION PREFLIGHT ERROR: $_"
    exit 2
}
