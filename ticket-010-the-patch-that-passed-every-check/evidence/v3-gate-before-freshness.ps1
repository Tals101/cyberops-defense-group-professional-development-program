param(
    [Parameter(Mandatory = $true)]
    [string]$Image,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-zA-Z0-9_-]+$')]
    [string]$EvidenceName
)

$projectRoot = Split-Path -Parent $PSScriptRoot
$reportPath = Join-Path $projectRoot "evidence\v3-gate-$EvidenceName.json"

if (-not (Get-Command trivy -ErrorAction SilentlyContinue)) {
    Write-Output "GATE ERROR: Trivy is unavailable."
    exit 2
}

# Never reuse a previous scan report
if (Test-Path $reportPath) {
    Remove-Item $reportPath -Force
}

Write-Output "=== V3 VULNERABILITY GATE ==="
Write-Output "Image: $Image"

# Collect findings; the wrapper makes the release decision
& trivy image `
    --image-src docker `
    --scanners vuln `
    --severity HIGH,CRITICAL `
    --format json `
    --exit-code 0 `
    --output $reportPath `
    $Image

$scanExit = $LASTEXITCODE

if ($scanExit -ne 0 -or -not (Test-Path $reportPath)) {
    Write-Output "GATE ERROR: Scanner failed or report missing."
    exit 2
}

try {
    $report = Get-Content $reportPath -Raw |
        ConvertFrom-Json
}
catch {
    Write-Output "GATE ERROR: Invalid JSON report."
    exit 2
}

if (
    $report.ArtifactType -ne "container_image" -or
    $report.ArtifactName -ne $Image -or
    $null -eq $report.Results
) {
    Write-Output "GATE ERROR: Unexpected scan report."
    exit 2
}

$findings = @(
    $report.Results |
        ForEach-Object { $_.Vulnerabilities } |
        Where-Object { $null -ne $_ }
)

$high = @($findings | Where-Object Severity -eq "HIGH").Count
$critical = @($findings | Where-Object Severity -eq "CRITICAL").Count

Write-Output "HIGH findings: $high"
Write-Output "CRITICAL findings: $critical"
Write-Output "Report: $reportPath"

if (($high + $critical) -gt 0) {
    Write-Output "GATE BLOCK: Vulnerability threshold exceeded."
    exit 1
}

Write-Output "GATE PASS: No HIGH or CRITICAL findings detected."
exit 0

