param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^127\.0\.0\.1:5500/[a-z0-9._/-]+@sha256:[a-f0-9]{64}$')]
    [string]$Image,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-zA-Z0-9_-]+$')]
    [string]$EvidenceName
)

$root = Split-Path -Parent $PSScriptRoot

$signatureGate = Join-Path $PSScriptRoot "v3-image-signature-gate.ps1"
$vulnerabilityGate = Join-Path $PSScriptRoot "v3-vulnerability-gate.ps1"

$evidencePath = Join-Path $root "evidence\v3-release-$EvidenceName.txt"

$log = New-Object System.Collections.Generic.List[string]

$log.Add("=== V3 COMBINED RELEASE GATE ===")
$log.Add("Image: $Image")

Write-Output "=== V3 COMBINED RELEASE GATE ==="
Write-Output "Image: $Image"

if (-not (Test-Path $signatureGate) -or
    -not (Test-Path $vulnerabilityGate)) {

    Write-Output "RELEASE ERROR: Required gate script missing."
    exit 2
}

# Phase 1: Verify the trusted signature
Write-Output "=== PHASE 1: SIGNATURE VERIFICATION ==="

$signatureOutput = & $signatureGate `
    -Image $Image `
    -EvidenceName "combined-$EvidenceName" 2>&1

$signatureExit = $LASTEXITCODE
$signatureText = $signatureOutput | Out-String

Write-Output $signatureText

$log.Add($signatureText)
$log.Add("Signature exit code: $signatureExit")

if (
    $signatureExit -ne 0 -or
    -not $signatureText.Contains("GATE SIGNATURE PASS:")
) {
    $decision = "RELEASE ERROR: Signature verification failed."
    $log.Add("VULNERABILITY GATE SKIPPED")
    $log.Add($decision)
    $log.Add("Release exit code: 2")

    $log | Set-Content $evidencePath -Encoding UTF8

    Write-Output "VULNERABILITY GATE SKIPPED"
    Write-Output $decision
    exit 2
}

Write-Output "PHASE 1: PASS"

# Phase 2: Scan the SAME immutable reference
Write-Output "=== PHASE 2: VULNERABILITY AND DB CHECKS ==="

$vulnerabilityOutput = & $vulnerabilityGate `
    -Image $Image `
    -EvidenceName "combined-$EvidenceName" 2>&1

$vulnerabilityExit = $LASTEXITCODE
$vulnerabilityText = $vulnerabilityOutput | Out-String

Write-Output $vulnerabilityText

$log.Add($vulnerabilityText)
$log.Add("Vulnerability gate exit code: $vulnerabilityExit")

if (
    $vulnerabilityExit -eq 0 -and
    $vulnerabilityText.Contains("GATE DB PASS:") -and
    $vulnerabilityText.Contains("GATE PASS:")
) {
    $decision = "RELEASE PASS: Signature, DB freshness and vulnerabilities approved."
    $releaseExit = 0
}
elseif (
    $vulnerabilityExit -eq 1 -and
    $vulnerabilityText.Contains("GATE BLOCK:")
) {
    $decision = "RELEASE BLOCK: Vulnerability threshold exceeded."
    $releaseExit = 1
}
else {
    $decision = "RELEASE ERROR: Vulnerability scan or freshness verification failed."
    $releaseExit = 2
}

Write-Output "=== FINAL RELEASE DECISION ==="
Write-Output $decision

$log.Add($decision)
$log.Add("Release exit code: $releaseExit")

$log | Set-Content $evidencePath -Encoding UTF8

exit $releaseExit
