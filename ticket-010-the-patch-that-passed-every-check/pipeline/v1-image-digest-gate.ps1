# Ticket 010 - V1 Immutable Image Policy
# P04: Require SHA256 image digest references

param(
    [Parameter(Mandatory=$true)]
    [string]$ManifestPath
)

$ErrorActionPreference = "Stop"

try {
    if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
        throw "Manifest not found: $ManifestPath"
    }

    $json = kubectl create --dry-run=client -f $ManifestPath -o json

    if ($LASTEXITCODE -ne 0 -or -not $json) {
        throw "Unable to parse Kubernetes manifest."
    }

    $manifest = $json | ConvertFrom-Json

    if ($manifest.kind -ne "Deployment") {
        throw "Unsupported resource type."
    }

    $spec = $manifest.spec.template.spec

    $containers = @(
        $spec.containers
        $spec.initContainers
        $spec.ephemeralContainers
    ) | Where-Object { $null -ne $_ } |
        ForEach-Object { $_ }

    if ($containers.Count -eq 0) {
        throw "No containers found."
    }

    $violations = 0

    foreach ($container in $containers) {
        $image = $container.image

        if ($image -notmatch '@sha256:[a-fA-F0-9]{64}$') {
            Write-Output "BLOCK P04: Mutable image reference: $image"
            $violations++
        }
        else {
            Write-Output "PASS P04: Immutable image reference: $image"
        }
    }

    if ($violations -gt 0) {
        Write-Output "P04 DECISION: BLOCK"
        exit 1
    }

    Write-Output "P04 DECISION: PASS"
    exit 0
}
catch {
    Write-Output "P04 ERROR: $_"
    exit 2
}
