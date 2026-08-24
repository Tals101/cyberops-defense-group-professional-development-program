# Ticket #004 - Hunt Findings

## Summary

The hunt found several scheduled execution mechanisms that looked different enough from the normal Ubuntu background jobs to justify a closer look. The most notable was a root-level configuration backup that ran every five minutes and wrote archives to `/var/tmp`.

After correlating cron execution, script contents, sudo records, SSH history, and systemd configuration, the activity was better explained as legitimate lab and administrative work than as unauthorized persistence.

**Disposition:** Close - Benign  
**Confidence:** Medium

---

## Finding 1 - Two recent cron jobs deserved attention

Two files in `/etc/cron.d` were recent compared with the older system entries.

### `dev-health-check`

- Runs every 15 minutes as root.
- Executes `/usr/local/bin/dev-health-check.sh`.
- Records hostname, uptime, and filesystem usage.
- Writes to `/var/log/dev-health-check.log`.

The script's purpose and output location were straightforward and consistent with routine monitoring.

### `config-backup`

- Runs every five minutes as root.
- Executes `/usr/local/bin/config-backup.sh`.
- Archives `/etc/hosts` and `/etc/ssh/sshd_config`.
- Writes timestamped `.tar.gz` files to `/var/tmp`.

This job warranted more scrutiny. Its frequency, root privileges, collection of SSH configuration, and temporary-directory destination were all reasonable hunting signals even though none of them proved malicious intent.

---

## Finding 2 - The backup job was actively executing

Cron journal events confirmed that `config-backup.sh` ran on schedule. The resulting files under `/var/tmp` provided a second source of confirmation that the job was active rather than simply configured and dormant.

That distinction mattered because the hunt was evaluating actual recurring behavior, not just a suspicious-looking file on disk.

---

## Finding 3 - Sudo records tied the recent jobs to the analyst session

Privilege telemetry showed the `analyst` account creating both scripts and both cron entries, changing permissions, and manually running the configuration backup before cron took over.

This was a major change in the assessment. Instead of an unexplained background process or unknown account creating persistence, the changes were tied to a visible interactive administrative session.

---

## Finding 4 - The session source matched historical access

The active analyst SSH session came from `192.168.56.1`. Login history showed the same source repeatedly associated with prior analyst sessions.

That pattern supported a benign explanation, but it was not treated as proof of authorization. A familiar source can still be compromised, and no formal change record was available.

---

## Hunt Pivot - An unexpected root cron task

While reviewing cron execution, I noticed `/usr/local/bin/detect-ssh-bruteforce.sh` running every minute as root. It had not appeared in the original `/etc/cron.d` review, so I traced its scheduling source.

The root crontab contained:

`* * * * * /usr/local/bin/detect-ssh-bruteforce.sh`

The script checks recent SSH logs, counts failed-password events by source IP, and writes an `auth.warning` message when five failures occur within five minutes.

This was important because the mechanism itself looked persistent and privileged, but the behavior was consistent with a defensive SSH monitor. The pivot therefore weakened, rather than strengthened, the original unauthorized-persistence hypothesis.

---

## Finding 5 - Systemd did not reveal another unexplained persistence mechanism

The systemd timer review showed expected Ubuntu maintenance jobs. The one custom service that stood out was `company-web.service`.

It predated the current hunt, ran as `analyst`, launched `/home/analyst/internal-web-outage-lab/app.py`, and was consistent with an existing Flask lab application. Nothing in the reviewed systemd data pointed to a new hidden persistence mechanism.

---

## Fact, Inference, and Assumption

### Facts

- The analyst account used sudo to create the two recent cron tasks.
- `config-backup.sh` archives `/etc/hosts` and `/etc/ssh/sshd_config`.
- Cron executed the backup job automatically.
- The active analyst session came from `192.168.56.1`.
- Historical analyst sessions repeatedly came from that same source.
- The root crontab runs `detect-ssh-bruteforce.sh` every minute.
- The systemd review did not uncover another unexplained recent persistence mechanism.

### Inferences

- `dev-health-check.sh` is consistent with routine system monitoring.
- `config-backup.sh` is most consistent with authorized lab or administrative activity.
- `detect-ssh-bruteforce.sh` appears to be a defensive monitoring control.
- `company-web.service` appears to be a legitimate application service.

### Assumptions

- The analyst session was formally authorized.
- The scheduled-task changes were formally approved.
- Historical consistency reflects expected administrative access.

Those assumptions could not be independently confirmed because a change ticket or separate administrator approval record was not available.

---

## Final Disposition

**Close - Benign**

The evidence consistently tied the unusual scheduled activity to an established analyst session and to scripts with understandable lab or defensive purposes. Nothing collected showed account compromise, malicious code, command-and-control activity, exfiltration, or another basis for incident escalation.

## Confidence

**Medium**

The conclusion is supported by several independent sources: cron configuration, cron execution, sudo telemetry, SSH authentication, historical login records, file metadata, script contents, and systemd configuration.

Confidence remains Medium because the technical evidence shows what happened but does not independently prove that the changes were formally approved.

---

## Why I Stopped

By the end of the hunt, the original hypothesis and the main benign alternatives had been tested. Cron, root crontab, systemd, scripts, file artifacts, authentication, privilege use, session origin, and historical access had all been reviewed, and the required pivot had been resolved.

No remaining finding pointed to a specific next step likely to change the disposition, so continuing to collect data would have added volume without improving the decision.
