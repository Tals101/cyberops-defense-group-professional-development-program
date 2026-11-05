param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectRoot,

    [Parameter(Mandatory=$true)]
    [string]$GeneratorPath
)

$ErrorActionPreference = "Stop"

$linuxDir = Join-Path $ProjectRoot "evidence\linux"

$awsPath = Join-Path $ProjectRoot `
    "evidence\aws\aws-investigation-timeline.csv"

$kubePath = Join-Path $ProjectRoot `
    "evidence\kubernetes\DATASET-PROVENANCE.md"

if (-not (Test-Path -LiteralPath $awsPath -PathType Leaf)) {
    throw "AWS source timeline missing."
}

if (-not (Test-Path -LiteralPath $kubePath -PathType Leaf)) {
    throw "Kubernetes provenance missing."
}

$aws = @(Import-Csv -LiteralPath $awsPath)

if (
    $aws.Count -ne 12 -or
    @($aws | Where-Object {
        $_.EventID -eq "aws-0004" -and
        $_.TimestampUTC -eq "2026-11-02T13:05:41Z" -and
        $_.SourceIP -eq "203.0.113.77"
    }).Count -ne 1
) {
    throw "AWS synthetic timeline anchor changed."
}

$kubeText = [System.IO.File]::ReadAllText($kubePath)

if (
    -not $kubeText.Contains("SYNTHETIC LABORATORY EVIDENCE") -or
    -not $kubeText.Contains("203.0.113.77")
) {
    throw "Kubernetes synthetic provenance mismatch."
}

function New-Event {
    param(
        [string]$ID,
        [string]$TimeUTC,
        [string]$Category,
        [string]$Action,
        [string]$Actor,
        [string]$SourceIP,
        [string]$DestinationIP,
        [string]$Target,
        [string]$Outcome,
        [string]$SessionID,
        [string]$ProcessID,
        [string]$Detail
    )

    return [pscustomobject][ordered]@{
        eventId = $ID
        eventTime = $TimeUTC
        sourceSystem = "linux-synthetic"
        hostName = "linux-reporting-01"
        category = $Category
        action = $Action
        actor = $Actor
        sourceIp = $SourceIP
        destinationIp = $DestinationIP
        target = $Target
        outcome = $Outcome
        sessionId = $SessionID
        processId = $ProcessID
        detail = $Detail
        datasetType = "SYNTHETIC_LABORATORY_DATA"
    }
}

Write-Output "=== BUILD AUTHENTICATION SCENARIO ==="

$auth = @(
    New-Event 'lin-0001' '2026-11-02T12:50:00Z' 'authentication' 'ssh.accepted' 'ops-admin' '198.51.100.60' '' 'sshd' 'SUCCESS' 'sess-normal-01' '1001' 'Modeled routine maintenance login'
    New-Event 'lin-0002' '2026-11-02T12:50:01Z' 'authentication' 'ssh.session_open' 'ops-admin' '198.51.100.60' '' 'sshd' 'SUCCESS' 'sess-normal-01' '1001' 'Routine session established'
    New-Event 'lin-0003' '2026-11-02T13:03:10Z' 'authentication' 'ssh.failed_password' 'ops-runner' '203.0.113.77' '' 'sshd' 'DENIED' 'sess-unfamiliar-01' '1203' 'First failed login from unfamiliar modeled source'
    New-Event 'lin-0004' '2026-11-02T13:03:17Z' 'authentication' 'ssh.failed_password' 'ops-runner' '203.0.113.77' '' 'sshd' 'DENIED' 'sess-unfamiliar-01' '1203' 'Second failed login from unfamiliar modeled source'
    New-Event 'lin-0005' '2026-11-02T13:04:02Z' 'authentication' 'ssh.accepted' 'ops-runner' '203.0.113.77' '' 'sshd' 'SUCCESS' 'sess-unfamiliar-01' '1205' 'Successful login; authorization not independently established'
    New-Event 'lin-0006' '2026-11-02T13:04:03Z' 'authentication' 'ssh.session_open' 'ops-runner' '203.0.113.77' '' 'sshd' 'SUCCESS' 'sess-unfamiliar-01' '1205' 'Modeled SSH session opened'
    New-Event 'lin-0007' '2026-11-02T13:06:25Z' 'authentication' 'sudo.authorization' 'ops-runner' '' '' 'root' 'DENIED' 'sess-unfamiliar-01' '1205' 'Privilege request denied in modeled policy'
    New-Event 'lin-0008' '2026-11-02T13:09:15Z' 'authentication' 'ssh.accepted' 'analyst-admin' '203.0.113.88' '' 'sshd' 'SUCCESS' 'sess-admin-review-01' '1308' 'Modeled approved administrative inspection'
    New-Event 'lin-0009' '2026-11-02T13:12:00Z' 'authentication' 'ssh.session_close' 'ops-runner' '203.0.113.77' '' 'sshd' 'SUCCESS' 'sess-unfamiliar-01' '1205' 'Modeled session ended'
)

Write-Output "Authentication records: $($auth.Count)"

Write-Output "=== BUILD EXECUTION AND PERSISTENCE SCENARIO ==="

$process = @(
    New-Event 'lin-0010' '2026-11-02T12:50:12Z' 'process' 'process.started' 'ops-admin' '' '' '/opt/reporting/jobs/check_health.py' 'SUCCESS' 'sess-normal-01' '1100' 'Routine health-check process'
    New-Event 'lin-0011' '2026-11-02T13:05:59Z' 'persistence' 'user_crontab.modified' 'ops-runner' '' '' '/var/spool/cron/crontabs/ops-runner' 'SUCCESS' 'sess-unfamiliar-01' '1210' 'Modeled user-level cron entry invoking telemetry_diag.py; approval unknown'
    New-Event 'lin-0012' '2026-11-02T13:06:00Z' 'persistence' 'file.metadata_changed' 'ops-runner' '' '' '/var/spool/cron/crontabs/ops-runner' 'SUCCESS' 'sess-unfamiliar-01' '1210' 'Modeled metadata event corroborating cron-file change'
    New-Event 'lin-0013' '2026-11-02T13:07:00Z' 'process' 'cron.job_started' 'ops-runner' '' '' '/opt/reporting/jobs/telemetry_diag.py' 'SUCCESS' 'cron-ops-runner-01' '1413' 'Scheduled process started in synthetic scenario'
    New-Event 'lin-0014' '2026-11-02T13:07:02Z' 'process' 'process.exited' 'ops-runner' '' '' '/opt/reporting/jobs/telemetry_diag.py' 'SUCCESS' 'cron-ops-runner-01' '1413' 'Synthetic process exit; behavior and intent unverified'
    New-Event 'lin-0015' '2026-11-02T13:10:30Z' 'persistence' 'systemd_timer.inspected' 'analyst-admin' '' '' 'systemd timers' 'SUCCESS' 'sess-admin-review-01' '1315' 'Modeled authorized inspection; no timer modification'
)

Write-Output "Process/persistence records: $($process.Count)"

Write-Output "=== BUILD NETWORK SCENARIO ==="

$network = @(
    New-Event 'lin-0016' '2026-11-02T12:50:21Z' 'network' 'tcp.connect' 'ops-admin' '' '192.0.2.40' '192.0.2.40:443' 'ALLOWED' 'sess-normal-01' '1100' 'Modeled routine maintenance connection'
    New-Event 'lin-0017' '2026-11-02T13:07:01Z' 'network' 'tcp.connect' 'ops-runner' '' '203.0.113.77' '203.0.113.77:443' 'ALLOWED' 'cron-ops-runner-01' '1413' 'Shared IP is deliberately modeled; no content or transfer proof'
    New-Event 'lin-0018' '2026-11-02T13:09:20Z' 'network' 'tcp.connect' 'analyst-admin' '' '192.0.2.40' '192.0.2.40:443' 'ALLOWED' 'sess-admin-review-01' '1308' 'Modeled routine administrative network activity'
)

Write-Output "Network records: $($network.Count)"

Write-Output "=== VERIFY SCENARIO INTEGRITY ==="

$all = @($auth) + @($process) + @($network)
$ids = @($all | ForEach-Object { $_.eventId })
$uniqueIds = @($ids | Sort-Object -Unique)

if (
    $auth.Count -ne 9 -or
    $process.Count -ne 6 -or
    $network.Count -ne 3 -or
    $all.Count -ne 18 -or
    $uniqueIds.Count -ne 18
) {
    throw "Synthetic event counts or identifiers are invalid."
}

foreach ($event in $all) {
    if (
        $event.datasetType -ne "SYNTHETIC_LABORATORY_DATA" -or
        $event.sourceSystem -ne "linux-synthetic" -or
        $event.hostName -ne "linux-reporting-01" -or
        -not $event.eventTime.StartsWith("2026-11-02T") -or
        -not $event.eventTime.EndsWith("Z")
    ) {
        throw "Invalid synthetic event: $($event.eventId)"
    }

    $parsed = [DateTimeOffset]::MinValue

    if (-not [DateTimeOffset]::TryParse(
        $event.eventTime,
        [ref]$parsed
    )) {
        throw "Invalid timestamp: $($event.eventId)"
    }
}

Write-Output "Total distinct synthetic events: 18"
Write-Output "Event classifications: VERIFIED"

Write-Output "=== SAVE DATASETS ==="

$utf8 = New-Object System.Text.UTF8Encoding($false)

$sets = [ordered]@{
    "linux-auth-synthetic.jsonl" = $auth
    "linux-process-persistence-synthetic.jsonl" = $process
    "linux-network-synthetic.jsonl" = $network
}

foreach ($name in $sets.Keys) {
    $path = Join-Path $linuxDir $name

    if (Test-Path -LiteralPath $path) {
        throw "Refusing overwrite: $path"
    }

    $lines = @(
        $sets[$name] |
        Sort-Object eventTime |
        ForEach-Object {
            ConvertTo-Json -InputObject $_ -Depth 5 -Compress
        }
    )

    [System.IO.File]::WriteAllLines(
        $path, [string[]]$lines, $utf8
    )

    Write-Output "Saved: $name ($($lines.Count) events)"
}

Write-Output "=== SAVE DATASET PROVENANCE ==="

$awsHash = (
    Get-FileHash -LiteralPath $awsPath -Algorithm SHA256
).Hash

$kubeHash = (
    Get-FileHash -LiteralPath $kubePath -Algorithm SHA256
).Hash

$generatorHash = (
    Get-FileHash -LiteralPath $GeneratorPath -Algorithm SHA256
).Hash

$timestamp = [DateTimeOffset]::UtcNow.ToString("o")

$provenance = @"
# Linux Dataset Provenance - Ticket 011

## Classification

SYNTHETIC LABORATORY EVIDENCE

These 18 Linux events were deliberately authored
for a training scenario. They are not collected
SSH logs, auditd logs, cron logs, or network captures
from any real Linux system.

Generated UTC: $timestamp
Scenario date: 2026-11-02
Event timestamp timezone: UTC
Modeled host: linux-reporting-01

## Generated Files

- linux-auth-synthetic.jsonl: 9 events
- linux-process-persistence-synthetic.jsonl: 6 events
- linux-network-synthetic.jsonl: 3 events

Generator: generate-linux-synthetic-8b.ps1
Generator SHA256: $generatorHash

## Existing Source Anchors

AWS timeline SHA256: $awsHash
Kubernetes provenance SHA256: $kubeHash

These existing sources supplied investigation
context. The Linux events themselves were newly
created, not extracted from those source records.

## Synthetic Scenario

- Routine administrative SSH activity
- Two failed SSH attempts from 203.0.113.77
- A subsequent successful SSH session for ops-runner
- One denied sudo authorization
- A user-level cron modification
- A modeled cron process execution
- An outbound connection to 203.0.113.77
- Later administrative inspection
- Routine network and process events

The source-IP and destination-IP overlap with
other synthetic datasets is intentional.

It does not prove a common operator, credential
theft, exfiltration, or causal linkage.

The user-level cron event is not a real installed
scheduled task. No persistence mechanism was
installed on any host.

203.0.113.0/24, 198.51.100.0/24, and 192.0.2.0/24
are documentation-only network ranges.

## Interpretation Boundaries

A successful modeled SSH authentication is not
proof that access was unauthorized.

A modeled cron modification is not proof of
malicious persistence.

A modeled allowed TCP connection does not prove
data transfer or exfiltration.

Event timestamps alone cannot establish causation.

No AWS access-key use is attributed to the Linux
processes by these event records.

The 09:05 containment stop gate is not modeled
as an actual containment action.

## Reproduction

Run the saved PowerShell generator with its
ProjectRoot and GeneratorPath arguments in a
clean copy of the Ticket 011 project.

The generator intentionally refuses to overwrite
existing dataset files.

## Safety

No live Linux host was accessed.
No SSH connection was initiated.
No cron entry, systemd unit, or service was changed.
No Kubernetes, Helm, Docker, or AWS resources
were modified.
"@

$provenancePath = Join-Path $linuxDir "DATASET-PROVENANCE.md"

[System.IO.File]::WriteAllText(
    $provenancePath, $provenance, $utf8
)

Write-Output "Dataset provenance: SAVED"

Write-Output "=== VERIFY GENERATED JSONL ==="

$totalValidated = 0

foreach ($name in $sets.Keys) {
    $path = Join-Path $linuxDir $name

    $lines = @(
        [System.IO.File]::ReadAllLines($path)
    )

    foreach ($line in $lines) {
        $item = $line | ConvertFrom-Json -ErrorAction Stop

        if (
            $item.datasetType -ne "SYNTHETIC_LABORATORY_DATA" -or
            $item.sourceSystem -ne "linux-synthetic"
        ) {
            throw "Invalid saved dataset record."
        }

        $totalValidated++
    }
}

if ($totalValidated -ne 18) {
    throw "Saved JSONL record count mismatch."
}

Write-Output "Validated saved events: $totalValidated"
Write-Output "STEP 8B GENERATOR: PASS"