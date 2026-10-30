param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^127\.0\.0\.1:5500/[a-z0-9._/-]+@sha256:[a-f0-9]{64}$')]
    [string]$Image,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-zA-Z0-9_-]+$')]
    [string]$EvidenceName
)

$root = Split-Path -Parent $PSScriptRoot
$keyPath = Join-Path $root "supply-chain\v3-local-cosign.pub"
$evidencePath = Join-Path $root "evidence\v3-signature-gate-$EvidenceName.txt"

$expectedKeyHash = "cce0c1d401a7b7776e77c4d4b1c67684c226f527f3bb8293866e3daa01441a09"

Write-Output "=== V3 SIGNATURE GATE ==="
Write-Output "Image: $Image"

if (-not (Test-Path $keyPath)) {
    Write-Output "GATE SIGNATURE ERROR: Trusted public key missing."
    exit 2
}

$actualKeyHash = (Get-FileHash $keyPath -Algorithm SHA256).Hash.ToLowerInvariant()

if ($actualKeyHash -ne $expectedKeyHash) {
    Write-Output "GATE SIGNATURE ERROR: Trusted public key hash mismatch."
    exit 2
}

Write-Output "Trusted public key hash: VERIFIED"

# Pass the image as a positional argument, not shell source.
$linuxScript = @(
    'set -euo pipefail'
    'COSIGN="$HOME/.local/bin/cosign"'
    'KEY="$PWD/supply-chain/v3-local-cosign.pub"'
    'test -x "$COSIGN"'
    'test -f "$KEY"'
    '"$COSIGN" verify --key "$KEY" --allow-http-registry --insecure-ignore-tlog=true "$1" >/dev/null'
    'echo "Cosign signature verified against trusted public key"'
) -join "`n"

$output = $linuxScript |
    wsl -d Ubuntu -- bash -s -- $Image 2>&1

$verifyExit = $LASTEXITCODE
$outputText = $output | Out-String

Write-Output $outputText
Write-Output "Cosign exit code: $verifyExit"

$approved = ($verifyExit -eq 0)

if ($approved) {
    $decision = "GATE SIGNATURE PASS: Trusted signature verified."
    $gateExit = 0
} else {
    $decision = "GATE SIGNATURE ERROR: Signature verification failed."
    $gateExit = 2
}

Write-Output $decision

@(
    "=== V3 IMAGE SIGNATURE GATE ==="
    "Image: $Image"
    "Trusted key SHA256: $actualKeyHash"
    $outputText
    "Cosign exit code: $verifyExit"
    $decision
    "Gate exit code: $gateExit"
) | Set-Content $evidencePath -Encoding UTF8

exit $gateExit
