# Ticket #004 - Hypothesis-Driven Linux Threat Hunt

## Overview

This repository documents a Linux threat hunt that began with an open question rather than an alert or known IOC: **was someone using scheduled execution to maintain unauthorized persistence on the host?**

The investigation started with cron and systemd, then followed the evidence into script behavior, file artifacts, sudo activity, SSH session history, and an unexpected root-level cron job. Several findings looked suspicious when viewed alone, but the combined context supported a benign explanation.

**Final disposition:** Close - Benign  
**Confidence:** Medium

---

## What I Was Looking For

The working hypothesis was that unauthorized persistence would likely leave recent or unexplained cron or systemd changes tied to unusual commands, users, file locations, or execution patterns.

I deliberately kept benign explanations in play from the beginning. Scheduled jobs are common on Linux, and root execution or frequent scheduling can be completely legitimate. The purpose of the hunt was to determine which explanation best fit the evidence, not to make the evidence fit the hypothesis.

See [hunt/hypothesis.md](hunt/hypothesis.md) and [hunt/hunt-plan.md](hunt/hunt-plan.md).

---

## How the Hunt Unfolded

### 1. Two recent cron jobs stood out

The initial `/etc/cron.d` review identified two recent entries.

`dev-health-check` ran every 15 minutes and collected basic system-health information. Its purpose was easy to explain.

`config-backup` ran every five minutes as root, archived `/etc/hosts` and `/etc/ssh/sshd_config`, and wrote timestamped `.tar.gz` files under `/var/tmp`.

That second job had enough unusual characteristics to justify a closer look, but not enough to label it malicious.

### 2. The backup job was actually running

Script inspection showed exactly what the job collected, and the files under `/var/tmp` confirmed repeated archive creation. Cron journal events independently showed the job executing on schedule.

This moved the investigation from "an unusual cron file exists" to "an unusual scheduled behavior is actively occurring."

### 3. Sudo telemetry changed the context

The sudo records tied creation of both recent scripts and cron files to the `analyst` account. The same session also manually ran the backup script before cron began executing it.

That was an important shift. The persistence mechanism was no longer unexplained; it was associated with a visible interactive administrative session.

### 4. The SSH source matched prior analyst activity

The active analyst session originated from `192.168.56.1`. Historical login records showed repeated analyst sessions from the same source on earlier dates.

That pattern supported a benign explanation, although I did not treat it as proof of authorization. A familiar source can still be compromised, and no formal change ticket was available.

---

## Hunt Pivot

Cron execution logs revealed another task that had not appeared in the original `/etc/cron.d` review:

`/usr/local/bin/detect-ssh-bruteforce.sh`

It ran every minute as root. Tracing the scheduling source led to the root user's crontab, and reading the script showed that it monitored failed SSH logins and generated warnings when a threshold was reached.

The mechanism itself looked like persistence, but its behavior was consistent with a defensive control. This pivot weakened the original hypothesis and reinforced the need to evaluate execution context rather than judge a task by privilege level or frequency alone.

See [hunt/findings.md](hunt/findings.md).

---

## Systemd Review

The systemd review did not reveal another unexplained persistence path. Standard Ubuntu timers looked normal. The custom `company-web.service` predated the hunt, ran as `analyst`, and launched an existing Flask lab application from `/home/analyst/internal-web-outage-lab`.

---

## Reasoning Discipline

Throughout the hunt I separated what the evidence directly showed from what I inferred from it.

### Facts

- The analyst account used sudo to create the two recent cron jobs.
- `config-backup.sh` archives `/etc/hosts` and `/etc/ssh/sshd_config`.
- Cron executed the backup automatically.
- The analyst SSH session came from `192.168.56.1`.
- Prior analyst logins repeatedly used that same source.
- The root crontab runs `detect-ssh-bruteforce.sh` every minute.
- No new unexplained systemd persistence mechanism was found.

### Inferences

- `dev-health-check.sh` is consistent with routine monitoring.
- `config-backup.sh` is most consistent with lab or administrative activity.
- `detect-ssh-bruteforce.sh` appears to be a defensive monitoring control.
- `company-web.service` appears to be a legitimate application service.

### Assumptions

- The analyst session was formally authorized.
- The changes were formally approved.

Those assumptions are the main reason confidence stayed at Medium instead of High.

---

## Final Assessment

**Disposition: Close - Benign**

The evidence did not show account compromise, unauthorized login, malware execution, external command-and-control activity, data exfiltration, hidden malicious systemd persistence, or another condition that would justify incident escalation.

The strongest supporting correlation was between the analyst SSH session, the sudo commands that created the tasks, and the history of the same source address.

**Confidence: Medium** because the technical telemetry explained the activity well, but no independent change-management or administrator approval record was available to prove formal authorization.

---

## Why the Hunt Stopped

By the end of the investigation, the original hypothesis and the main competing explanations had been tested across cron, root crontab, systemd, scripts, file artifacts, authentication, sudo activity, session origin, and historical login behavior. The required pivot had also been resolved.

There was no remaining evidence-driven lead likely to change the disposition. Continuing to collect logs simply because more data existed would not have improved the decision.

---

## Repository Structure

    ticket-004-threat-hunt/
    |-- README.md
    |-- Threat_Hunt_Report.pdf
    |-- management-update.md
    |-- lessons-learned.md
    |-- engineering-notebook.md
    |-- technical-timeline.csv
    |-- interview-preparation.txt
    |-- mitre-attack-mapping.md
    |
    |-- hunt/
    |   |-- hypothesis.md
    |   |-- hunt-plan.md
    |   `-- findings.md
    |
    |-- evidence/
    |   |-- logs/
    |   |-- screenshots/
    |   |-- command-output/
    |   `-- artifacts/
    |
    |-- scenario/
    |   `-- scenario-documentation.md
    |
    `-- diagrams/
        `-- hunt-flow.mmd

The `evidence/command-output/` directory is intentionally separate from operating-system logs so collected terminal output is easy to distinguish from native log sources.

---

## Evidence and Supporting Material

- [Raw logs](evidence/logs/)
- [Command output](evidence/command-output/)
- [Screenshots](evidence/screenshots/)
- [Sanitized artifacts](evidence/artifacts/)
- [Engineering Notebook](engineering-notebook.md)
- [Technical Timeline](technical-timeline.csv)
- [Management Update](management-update.md)
- [Lessons Learned](lessons-learned.md)
- [Scenario Documentation](scenario/scenario-documentation.md)
- [Interview Preparation](interview-preparation.txt)
- [MITRE ATT&CK Mapping](mitre-attack-mapping.md)

The evidence package intentionally excludes passwords, credentials, private keys, tokens, and other secrets.

---

## Skills Demonstrated

- Hypothesis-driven threat hunting
- Linux cron and systemd analysis
- Authentication and sudo correlation
- Evidence classification and timeline building
- Script and artifact review
- Hunt pivoting
- Confirmation-bias control
- Incident disposition and confidence assessment
- Executive communication
- MITRE ATT&CK behavioral mapping
- Evidence preservation and SHA-256 hashing

---

## Key Takeaway

The cron job that looked most suspicious at first was not the final answer. The useful conclusion came from correlating **what ran, who created it, where the session came from, how that source compared with history, and whether other evidence supported a malicious explanation**.

That is the central lesson from this hunt: suspicious characteristics are leads. Context turns them into findings.
