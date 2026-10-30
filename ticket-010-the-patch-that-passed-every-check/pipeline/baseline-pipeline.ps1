# Ticket 010 - Intentionally Incomplete Baseline Pipeline
# SYNTHETIC LAB ONLY - NOT FOR PRODUCTION USE
# Demonstrates missing workload security enforcement.

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

Push-Location $root

try {
    $context = kubectl config current-context

    if ($LASTEXITCODE -ne 0 -or $context.Trim() -ne "minikube") {
        throw "Safety check failed: Minikube context required."
    }

    Write-Output "STAGE 1: Image vulnerability scan"

    trivy image --scanners vuln --severity HIGH,CRITICAL --exit-code 1 --format table --output ".\evidence\pipeline-image-scan.txt" ledger-api:ticket010-alpine

    if ($LASTEXITCODE -ne 0) {
        throw "BLOCKED: Image vulnerability scan failed."
    }

    Write-Output "PASS: Image vulnerability scan"

    Write-Output "STAGE 2: Kubernetes API validation"

    kubectl --context minikube create --dry-run=server -f ".\kubernetes\ledger-api-alpine-unsafe.yaml"

    if ($LASTEXITCODE -ne 0) {
        throw "BLOCKED: Kubernetes validation failed."
    }

    Write-Output "PASS: Kubernetes API validation"

    Write-Output "WORKLOAD SECURITY POLICY: NOT CHECKED"

    Write-Output "BASELINE DECISION: ELIGIBLE UNDER INCOMPLETE CHECKS"
    Write-Output "NO ACTUAL DEPLOYMENT PERFORMED"
}
finally {
    Pop-Location
}
