# Ticket #004 — Threat Hunt Plan

## Hunt Objective

Determine whether evidence exists on the Linux system indicating unauthorized persistence through cron jobs, systemd services, or related scheduled execution mechanisms.

The hunt will focus on identifying unusual scheduled activity and determining whether the activity is legitimate, suspicious, or requires further investigation.

---

## System to Examine

Primary system:

- Host: ubuntu-soc-lab
- Operating System: Ubuntu Linux
- Role: Authorized cybersecurity lab system

The investigation will initially remain limited to this Linux host.

The hunt will expand only if evidence indicates activity involving another system, account, network source, or related resource.

---

## Hunt Timeframe

The initial hunt will examine:

- Current system state.
- Recent scheduled-task configuration.
- Recent authentication and privilege activity.
- Recent system and service logs.
- Recent file modifications relevant to scheduled execution.

The exact event timeframe will be refined once suspicious or relevant timestamps are identified.

---

## Data Source 1 — Cron Configuration

### Locations

- /etc/crontab
- /etc/cron.d/
- /etc/cron.daily/
- /etc/cron.hourly/
- /etc/cron.weekly/
- /etc/cron.monthly/
- User crontabs

### Why This Data Source Was Selected

Cron is a legitimate Linux scheduling mechanism that can also be used for persistence.

Examining cron configuration can reveal:

- Newly created scheduled jobs.
- Modified scheduled jobs.
- Commands running at unusual intervals.
- Scripts executing from unusual locations.
- Jobs associated with unexpected users.

### What I Am Looking For

- Recently modified cron files.
- Unfamiliar commands.
- Jobs running from /tmp, /var/tmp, or hidden directories.
- Unexpected users.
- Unusually frequent execution.
- Scripts with unclear administrative purpose.

---

## Data Source 2 — Systemd Services and Timers

### Locations

- /etc/systemd/system/
- /usr/lib/systemd/system/
- /lib/systemd/system/
- systemctl service listings
- systemctl timer listings
- systemd journal

### Why This Data Source Was Selected

Systemd services and timers can provide persistent or scheduled execution.

Both administrators and attackers can create services, making context important.

### What I Am Looking For

- Recently created or modified services.
- Recently created or modified timers.
- Services running unexpected commands.
- Executables or scripts in unusual locations.
- Services with misleading names.
- Unexpected enabled services.

---

## Data Source 3 — Authentication Logs

### Locations

- /var/log/auth.log
- SSH service logs
- systemd journal authentication events

### Why This Data Source Was Selected

Authentication telemetry can help establish who accessed the system before a suspicious configuration change.

This may help determine whether scheduled activity followed:

- A normal administrative login.
- An unusual remote login.
- Repeated authentication failures.
- Access by an unexpected account.

### What I Am Looking For

- Successful SSH logins.
- Failed SSH logins.
- Unexpected source IP addresses.
- Unexpected accounts.
- Authentication events occurring near suspicious configuration changes.

---

## Data Source 4 — Sudo and Privilege Activity

### Locations

- /var/log/auth.log
- systemd journal
- available shell history

### Why This Data Source Was Selected

Creating or modifying system-level cron jobs and systemd services often requires elevated privileges.

Privilege activity near the creation of a suspicious persistence mechanism could provide important context.

### What I Am Looking For

- sudo commands.
- Root sessions.
- Privilege escalation near suspicious timestamps.
- Commands involving cron or systemd configuration.
- Unexpected users using administrative privileges.

---

## Data Source 5 — File Metadata

### Locations

Relevant files discovered during the hunt, particularly:

- /etc/cron*
- /etc/systemd/system/
- /tmp/
- /var/tmp/
- User home directories

### Why This Data Source Was Selected

File metadata can help establish when a file was created or modified and whether its timestamp correlates with authentication, privilege, or scheduled execution events.

### What I Am Looking For

- Recent modification timestamps.
- Unexpected ownership.
- Unusual permissions.
- Scripts in temporary directories.
- Hidden files.
- Files referenced by suspicious scheduled tasks.

---

## Data Source 6 — Process and Execution Evidence

### Sources

- ps
- systemctl
- journalctl
- process information available during the hunt

### Why This Data Source Was Selected

A persistence mechanism becomes more significant if there is evidence that the configured command actually executed.

### What I Am Looking For

- Processes matching suspicious scheduled commands.
- Repeated execution.
- Unexpected parent-child relationships.
- Processes launched by cron or systemd.
- Processes running under unexpected accounts.

---

## Behaviors Being Hunted

The hunt will focus on:

1. Creation or modification of cron jobs.
2. Creation or modification of systemd services or timers.
3. Scheduled execution from unusual filesystem locations.
4. Scheduled execution by unexpected users.
5. Privilege escalation associated with scheduled-task changes.
6. Authentication events preceding suspicious changes.
7. Execution of files related to suspicious scheduled tasks.
8. Attempts to make persistence appear like normal administrative activity.

---

## Evidence Supporting the Hypothesis

The hypothesis will be strengthened if I identify:

- A recently created or modified scheduled task.
- A task with no clear legitimate purpose.
- Execution from an unusual location.
- An unexpected user associated with the activity.
- Related authentication activity.
- Related privilege escalation.
- A correlated file creation or modification.
- Evidence that the suspicious command actually executed.
- Multiple related suspicious events within the same timeframe.

---

## Evidence Contradicting the Hypothesis

The hypothesis will be weakened if:

- Scheduled tasks are consistent with normal system configuration.
- No unexplained scheduled tasks are identified.
- Changes can be tied to legitimate package installation or administration.
- Authentication activity is consistent with expected users and sources.
- No suspicious privilege escalation is identified.
- Referenced scripts and executables have legitimate purposes.
- No related suspicious execution occurs.

---

## Conditions That Would Cause the Hunt to Expand

The hunt will expand beyond the original plan if evidence identifies:

- An unexpected user account.
- An unusual SSH source address.
- A suspicious script or executable.
- An unexplained systemd service.
- Evidence of privilege escalation.
- A suspicious network connection.
- Additional persistence mechanisms.
- Evidence involving another host.

Any expansion will be documented as a Hunt Pivot if the new area was not part of the original investigation plan.

---

## Escalation Threshold

Escalation will be considered when multiple correlated findings indicate unauthorized activity.

Examples:

- Suspicious scheduled task plus unusual authentication.
- Suspicious scheduled task plus unexpected privilege escalation.
- Suspicious scheduled task plus an unexplained script.
- Evidence of repeated execution from an unusual directory.
- Evidence showing an unauthorized account established persistence.

A single unusual artifact without supporting context will not automatically justify escalation.

---

## Hunt Closure Conditions

### Close — Benign

Use when the evidence adequately demonstrates legitimate activity.

### Close — Insufficient Evidence

Use when suspicious activity cannot be confirmed and available telemetry is insufficient to establish authorization or malicious intent.

### Escalate for Investigation

Use when correlated evidence indicates activity that warrants formal incident response.

### Confirmed Security Incident

Use only when available evidence establishes that unauthorized or malicious activity occurred.

---

## Initial Stopping Criteria

The hunt may stop when:

- The original hypothesis has been adequately tested.
- Major competing explanations have been evaluated.
- Significant findings have been correlated across available telemetry.
- Required pivots have been investigated.
- Additional available evidence is unlikely to materially change the disposition.
- The conclusion can be defended using collected evidence.

The hunt will not continue solely because additional logs or systems could theoretically be examined.
