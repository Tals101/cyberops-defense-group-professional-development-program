# Ticket #004 — Hypothesis-Driven Linux Threat Hunt

## Overview

This project documents a hypothesis-driven threat hunt conducted against an Ubuntu Linux lab system after unusual activity was observed without a confirmed indicator of compromise.

Unlike incident response, this investigation did not begin with a known attacker, IOC, alert, or root cause. The hunt began with a hypothesis, collected evidence that both supported and weakened that hypothesis, followed an unexpected pivot, and stopped when additional investigation was unlikely to materially change the conclusion.

**Final Disposition:** Close — Benign

**Confidence:** Medium

---

## Hunt Objective

Determine whether unauthorized persistence was occurring through Linux scheduled execution mechanisms, including:

- Cron jobs
- User crontabs
- Systemd services
- Systemd timers

The investigation intentionally considered both malicious and benign explanations.

---

## Initial Hypothesis

If unauthorized persistence through scheduled tasks is occurring on the Linux system, I would expect to observe newly created or modified cron jobs or systemd services associated with unusual commands, users, files, or execution times because scheduled tasks are commonly used by both legitimate administrators and attackers to execute commands persistently.

Before collecting evidence, the hunt documented:

- Known facts
- Unknowns
- Assumptions
- Competing explanations
- Supporting evidence criteria
- Contradicting evidence criteria
- Escalation criteria
- Stopping criteria

See [hunt/hypothesis.md](hunt/hypothesis.md).

---

## How the Hunt Developed

### Stage 1 — Scheduled Task Enumeration

The investigation began by reviewing `/etc/cron.d`.

Two recently modified tasks stood out.

#### dev-health-check

Runs every 15 minutes as root and executes:

    /usr/local/bin/dev-health-check.sh

The script collects:

- Hostname
- Uptime
- Disk utilization

Results are written to:

    /var/log/dev-health-check.log

This behavior was readily explainable as legitimate administrative monitoring.

#### config-backup

Runs every five minutes as root and executes:

    /usr/local/bin/config-backup.sh

The script:

- Archives `/etc/hosts`
- Archives `/etc/ssh/sshd_config`
- Writes timestamped archives under `/var/tmp`

The frequency, root privileges, SSH configuration collection, and temporary-directory storage made this activity worthy of further investigation.

At this stage, the unauthorized-persistence hypothesis became more plausible, but the evidence did not establish malicious intent.

---

### Stage 2 — Script and Artifact Analysis

The scripts referenced by the cron jobs were inspected.

The configuration backup created files such as:

    /var/tmp/dev-config-20260823-175433.tar.gz

Artifact review showed:

- Root ownership
- Permission mode 600
- Multiple archive files
- Timestamps consistent with repeated execution

Journal telemetry independently confirmed that cron automatically executed the configuration backup.

This demonstrated active scheduled execution rather than simply the presence of a dormant cron entry.

---

### Stage 3 — Authentication and Privilege Correlation

The next question was:

**Who created the scheduled tasks?**

Sudo telemetry showed that the `analyst` account:

- Created `dev-health-check.sh`
- Created `config-backup.sh`
- Created both cron entries
- Set permissions
- Manually executed the configuration backup script

This weakened the hypothesis that an unexplained process or unknown account had established persistence.

The investigation then asked where the analyst session originated.

---

### Stage 4 — Session Origin

SSH telemetry showed that the analyst session originated from:

    192.168.56.1

Historical login records showed repeated previous analyst sessions from the same source address.

#### Fact

The current session originated from an address repeatedly associated with historical analyst logins.

#### Inference

The session was consistent with the account's normal historical access pattern.

#### Assumption

Historical consistency meant the activity was formally authorized.

That final point could not be independently proven because formal change-management records were not available.

---

## Hunt Pivot

During cron execution review, an additional scheduled script appeared:

    /usr/local/bin/detect-ssh-bruteforce.sh

It executed every minute as root but had not appeared during the initial `/etc/cron.d` enumeration.

This created a new question:

**Was this another unauthorized persistence mechanism?**

The script was inspected and found to:

- Review recent SSH events
- Search for failed password attempts
- Count failures by source IP
- Trigger after five failures within five minutes
- Generate an `auth.warning` message

The scheduling source was then located in the root user's personal crontab:

    * * * * * /usr/local/bin/detect-ssh-bruteforce.sh

### Pivot Result

The unexpected scheduled task was consistent with defensive SSH brute-force monitoring.

Instead of strengthening the original hypothesis, the pivot weakened it.

This demonstrated why scheduled execution must be evaluated in context rather than classified as malicious based solely on frequency or root privileges.

See [hunt/findings.md](hunt/findings.md).

---

## Systemd Review

The hunt also reviewed systemd services and timers.

Standard Ubuntu maintenance timers were observed.

One custom service was examined:

    company-web.service

The service:

- Predated the current hunt
- Ran as the `analyst` user
- Executed an internal Flask application
- Referenced an existing lab application directory

No additional unexplained systemd persistence mechanism was identified.

---

## Evidence Classification

### Facts

- The analyst account created the two recent cron tasks through sudo.
- Cron automatically executed `config-backup.sh`.
- The backup script archived `/etc/hosts` and `/etc/ssh/sshd_config`.
- The analyst session originated from `192.168.56.1`.
- Historical analyst logins repeatedly used the same source.
- The root crontab scheduled `detect-ssh-bruteforce.sh` every minute.
- No unexplained new systemd persistence mechanism was identified.

### Inferences

- `dev-health-check.sh` was legitimate administrative monitoring.
- `detect-ssh-bruteforce.sh` was a defensive security control.
- The configuration backup activity was most consistent with legitimate lab administration.
- `company-web.service` was consistent with legitimate application hosting.

### Assumptions

- The analyst session was formally authorized.
- The scheduled configuration changes were formally approved.

Formal change-management evidence was not available to independently verify those assumptions.

---

## Final Assessment

### Disposition

**Close — Benign**

The collected evidence most strongly supported legitimate administrative and lab activity.

The hunt did not identify evidence demonstrating:

- Account compromise
- Unauthorized login
- Malware execution
- External command and control
- Data exfiltration
- Unauthorized account creation
- Hidden malicious systemd persistence
- Security-control disabling

---

## Confidence Assessment

**Confidence: Medium**

Multiple independent sources supported the final conclusion:

- Cron configuration
- Cron execution telemetry
- Sudo logs
- SSH authentication
- Historical login records
- Script contents
- File metadata
- Systemd configuration

### Strongest Evidence

The strongest evidence was the correlation between:

1. The analyst SSH session
2. The sudo commands used to create the scheduled tasks
3. Historical login activity from the same source address

### Missing Evidence

The hunt did not have:

- Formal change-management records
- Enterprise identity-provider telemetry
- Centralized SIEM data
- EDR process telemetry
- Authoritative asset ownership information

These sources could increase or decrease confidence in the final assessment.

---

## Why the Hunt Stopped

The investigation stopped when:

- The original hypothesis had been tested
- Competing explanations had been evaluated
- Cron configuration and execution had been correlated
- Suspicious scripts had been inspected
- Authentication and sudo activity had been reviewed
- Session origin had been established
- Historical access behavior had been compared
- The required hunt pivot had been completed
- Root crontab activity had been investigated
- Systemd persistence had been reviewed
- No remaining lead was likely to materially change the disposition

Continuing to collect logs without a specific unanswered question would no longer have been hypothesis-driven.

---

## Repository Structure

    ticket-004-threat-hunt/
    +-- README.md
    +-- Threat_Hunt_Report.pdf
    +-- management-update.md
    +-- lessons-learned.md
    +-- engineering-notebook.md
    +-- technical-timeline.csv
    +-- interview-preparation.txt
    ¦
    +-- hunt/
    ¦   +-- hypothesis.md
    ¦   +-- hunt-plan.md
    ¦   +-- findings.md
    ¦
    +-- evidence/
    ¦   +-- logs/
    ¦   +-- screenshots/
    ¦   +-- command-output/
    ¦   +-- artifacts/
    ¦
    +-- scenario/
    ¦   +-- scenario-documentation.md
    ¦
    +-- diagrams/

The additional `evidence/command-output/` directory separates raw investigative command output from operating-system logs.

---

## Evidence

### Logs

[evidence/logs/](evidence/logs/)

Includes:

- Cron execution telemetry
- Authentication and sudo correlation
- Session-origin evidence

### Command Output

[evidence/command-output/](evidence/command-output/)

Includes:

- Cron enumeration
- Script inspection
- `/var/tmp` artifact review
- Hunt-pivot investigation
- Root crontab review
- Systemd review
- Company web service review

### Screenshots

[evidence/screenshots/](evidence/screenshots/)

Contains screenshots of significant investigative evidence.

### Sanitized Artifacts

[evidence/artifacts/](evidence/artifacts/)

Contains sanitized copies of:

- Cron configurations
- Investigation scripts
- Root crontab
- Archive-content listing
- SHA-256 hashes

No passwords, credentials, private keys, tokens, or other secrets are intentionally included.

---

## Documentation

- [Hunt Hypothesis](hunt/hypothesis.md)
- [Hunt Plan](hunt/hunt-plan.md)
- [Hunt Findings](hunt/findings.md)
- [Engineering Notebook](engineering-notebook.md)
- [Technical Timeline](technical-timeline.csv)
- [Management Update](management-update.md)
- [Lessons Learned](lessons-learned.md)
- [Scenario Documentation](scenario/scenario-documentation.md)
- [Interview Preparation](interview-preparation.txt)

---

## Skills Demonstrated

- Hypothesis-driven threat hunting
- Linux security investigation
- Cron persistence analysis
- Systemd persistence analysis
- Authentication-log analysis
- Sudo telemetry analysis
- Evidence correlation
- Timeline development
- Hunt pivoting
- Fact / inference / assumption classification
- Confirmation-bias avoidance
- Evidence preservation
- SHA-256 hashing
- Incident disposition
- Confidence assessment
- Executive communication
- Investigative stopping criteria

---

## Key Takeaway

The most suspicious-looking artifact was not automatically the most important evidence.

The investigation became useful when scheduled-task behavior was correlated with:

- User activity
- Authentication
- Privilege use
- Historical context
- Script behavior
- Actual execution
- Competing explanations

Threat hunting is not about finding the most alarming command.

It is about building the most defensible explanation from the available evidence.
