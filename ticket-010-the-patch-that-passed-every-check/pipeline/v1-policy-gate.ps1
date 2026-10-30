param(
    [Parameter(Mandatory=$true)]
    [string]$ReportPath
)
# Ticket 010 - V1 Trivy Policy Gate
# Initial implementation - additional controls pending

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$path = $ReportPath

try {
    if (-not (Test-Path $path)) {
        throw "Missing Trivy report."
    }

    $report = Get-Content $path -Raw | ConvertFrom-Json

    if (-not $report.Results) {
        throw "Missing scan results."
    }

    $blockingRules = @{
        "KSV-0017" = "P01 - Privileged container"
        "KSV-0001" = "P02 - Privilege escalation"
        "KSV-0012" = "P03 - Root execution"
        "KSV-0105" = "P03 - Root execution"
        "KSV-0118" = "P03 - Insecure security context"
        "KSV-0011" = "P05 - Missing CPU limit"
        "KSV-0015" = "P05 - Missing CPU request"
        "KSV-0016" = "P05 - Missing memory request"
        "KSV-0018" = "P05 - Missing memory limit"
        "KSV-0003" = "P06 - Capabilities not dropped"
        "KSV-0004" = "P06 - Capabilities not restricted"
        "KSV-0030" = "P06 - Missing seccomp"
        "KSV-0104" = "P06 - Missing seccomp"
        "KSV-0106" = "P06 - Unsafe capabilities"
    }

    $findings = @(
        $report.Results |
        ForEach-Object { $_.Misconfigurations } |
        Where-Object { $null -ne $_ }
    )

    $violations = @(
        $findings |
        Where-Object { $blockingRules.ContainsKey($_.ID) }
    )

    foreach ($finding in $violations) {
        Write-Output "BLOCK: $($finding.ID) - $($blockingRules[$finding.ID])"
    }

    foreach ($finding in $findings) {
        if ($finding.ID -eq "KSV-0014") {
            Write-Output "WARN: P07 - Writable root filesystem"
        }
    }

    if ($violations.Count -gt 0) {
        Write-Output "V1 DECISION: BLOCK"
        exit 1
    }

    # Fail closed on all HIGH and CRITICAL findings,
    # including findings without a known policy mapping.

    if (-not $report.Results) {
        throw "Trivy report has no scan results."
    }

    $severeFindings = @(
        $report.Results |
        ForEach-Object { $_.Misconfigurations } |
        Where-Object {
            $null -ne $_ -and
            $_.Severity -in @("HIGH", "CRITICAL")
        }
    )

    if ($severeFindings.Count -gt 0) {
        foreach ($finding in $severeFindings) {
            Write-Output "BLOCK: $($finding.ID) - $($finding.Severity) severity guard"
        }

        Write-Output "V1 DECISION: BLOCK - Severity guard"
        exit 1
    }

    Write-Output "V1 PARTIAL GATE: PASS"
    Write-Output "Additional policy checks still required."
    exit 0
}
catch {
    Write-Error "Policy evaluation failed: $_"
    exit 2
}


