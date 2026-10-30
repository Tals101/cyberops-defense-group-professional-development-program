# Ticket 010 - V1 Trusted Registry Policy
# Synthetic lab registry allowlist
# Configuration validation only - no deployment

param(
    [Parameter(Mandatory=$true)]
    [string]$ManifestPath
)

$ErrorActionPreference = "Stop"

$allowedRegistries = @(
    "registry.example.local"
)

try {
    if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
        throw "Manifest not found."
    }

    $json = kubectl create --dry-run=client -f $ManifestPath -o json

    if ($LASTEXITCODE -ne 0 -or -not $json) {
        throw "Unable to parse manifest."
    }

    $manifest = $json | ConvertFrom-Json

    if ($manifest.kind -ne "Deployment") {
        throw "Unsupported resource type."
    }

    $spec = $manifest.spec.template.spec

    $containers = @(
        $spec.containers | Where-Object { $null -ne $_ }
    ) + @(
        $spec.initContainers | Where-Object { $null -ne $_ }
    )

    if ($containers.Count -eq 0) {
        throw "No containers found."
    }

    $blocked = $false

    foreach ($container in $containers) {
        $image = [string]$container.image

        if ($image -notmatch '^(?<registry>[a-zA-Z0-9.-]+(?::[0-9]{1,5})?)/[a-zA-Z0-9._/-]+@sha256:[a-fA-F0-9]{64}$') {
            Write-Output "BLOCK: Invalid or unqualified image reference: $image"
            $blocked = $true
            continue
        }

        $registry = $Matches["registry"].ToLowerInvariant()

        if ($registry -notin $allowedRegistries) {
            Write-Output "BLOCK: Unapproved registry: $registry"
            $blocked = $true
        }
        else {
            Write-Output "PASS: Approved lab registry: $registry"
        }
    }

    if ($blocked) {
        Write-Output "REGISTRY POLICY: BLOCK"
        exit 1
    }

    Write-Output "REGISTRY POLICY: PASS"
    exit 0
}
catch {
    Write-Output "REGISTRY POLICY ERROR: $_"
    exit 2
}
