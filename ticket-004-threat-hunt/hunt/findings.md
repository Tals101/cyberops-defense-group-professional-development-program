# Ticket #004 — Hunt Findings

## Summary

The threat hunt examined whether unauthorized persistence was occurring on the Ubuntu Linux lab system through cron jobs, systemd services, or related scheduled execution mechanisms.

The hunt identified suspicious-looking scheduled activity, but additional context showed the behavior was most consistent with legitimate administrative and lab activity.

## Key Finding 1 — Recently Created Cron Jobs

Two recently created cron jobs were identified:

### dev-health-check

- Runs every 15 minutes.
- Executes as root.
- Calls `/usr/local/bin/dev-health-check.sh`.
- Records hostname, uptime, and filesystem usage.
- Writes to `/var/log/dev-health-check.log`.

Assessment:

The task had a clear administrative monitoring purpose.

### config-backup

- Runs every 5 minutes.
- Executes as root.
- Calls `/usr/local/bin/config-backup.sh`.
- Archives `/etc/hosts` and `/etc/ssh/sshd_config`.
- Writes timestamped archives to `/var/tmp`.

Assessment:

The task warranted additional investigation because of its frequency, root execution, collection of SSH configuration, and use of a temporary directory.

## Key Finding 2 — Confirmed Scheduled Execution

Cron journal telemetry confirmed that `config-backup.sh` executed automatically at the expected schedule.

Artifacts under `/var/tmp` also confirmed repeated execution.

This established that the task was active persistence, not merely a dormant cron configuration.

## Key Finding 3 — User and Privilege Correlation

Sudo telemetry showed that the `analyst` account:

- Created `dev-health-check.sh`.
- Created `config-backup.sh`.
- Created both cron entries.
- Manually executed the configuration backup script.
- Set permissions on the scripts and cron files.

This weakened the hypothesis that an unknown account created the scheduled tasks.

## Key Finding 4 — Session Origin

The analyst SSH session originated from:

`192.168.56.1`

Historical login records showed repeated prior analyst sessions from the same source address.

Assessment:

The session source was consistent with historical access patterns.

This did not independently prove authorization, but it weakened the unauthorized-access explanation.

## Hunt Pivot — Unexpected Root Cron Task

During cron execution review, an additional script was discovered:

`/usr/local/bin/detect-ssh-bruteforce.sh`

The task executed every minute as root.

It was not found in `/etc/cron.d`, which led to a review of the root user's crontab.

The root crontab contained:

`* * * * * /usr/local/bin/detect-ssh-bruteforce.sh`

Script inspection showed that it:

- Reviews recent SSH logs.
- Searches for failed password attempts.
- Counts attempts by source IP.
- Uses a threshold of five failures in five minutes.
- Generates an `auth.warning` alert when the threshold is exceeded.

Assessment:

The task was consistent with defensive SSH brute-force monitoring rather than unauthorized persistence.

This pivot weakened the original hypothesis.

## Key Finding 5 — Systemd Review

Systemd services and timers were reviewed.

No unexplained newly created persistence mechanism was identified.

The only notable custom service was:

`company-web.service`

It:

- Predated the current hunt.
- Ran as the `analyst` user.
- Executed an internal Flask application.
- Used `/home/analyst/internal-web-outage-lab/app.py`.
- Was consistent with an existing lab application.

## Evidence Classification

### Facts

- The analyst account created the two recent cron tasks through sudo.
- `config-backup.sh` archives `/etc/hosts` and `/etc/ssh/sshd_config`.
- Cron executed the configuration backup automatically.
- The analyst session originated from `192.168.56.1`.
- Historical analyst sessions repeatedly used the same source.
- The root crontab schedules `detect-ssh-bruteforce.sh` every minute.
- No unexplained new systemd persistence mechanism was identified.

### Inferences

- `dev-health-check.sh` is legitimate administrative monitoring.
- `config-backup.sh` is most consistent with authorized lab activity.
- `detect-ssh-bruteforce.sh` is a defensive monitoring control.
- `company-web.service` is legitimate application hosting.

### Assumptions

- The analyst session was formally authorized.
- The configuration changes were formally approved.
- Historical consistency indicates expected administrative access.

Formal change-management evidence was not available to independently prove these assumptions.

## Final Disposition

**Close — Benign**

## Confidence

**Medium**

The strongest evidence supporting this conclusion was the correlation between the analyst SSH session, sudo activity, historical login source, script contents, cron execution, and systemd review.

Confidence remains Medium because no independent change-management or administrator approval record was available.

## Why the Hunt Stopped

The hunt stopped after:

- The original hypothesis was tested.
- Cron configuration and execution were reviewed.
- Suspicious scripts were inspected.
- File artifacts were analyzed.
- Authentication and sudo activity were correlated.
- Session history was reviewed.
- The required hunt pivot was completed.
- Root crontab activity was investigated.
- Systemd persistence was reviewed.

At that point, no remaining evidence pointed toward another meaningful lead that was likely to materially change the disposition.
