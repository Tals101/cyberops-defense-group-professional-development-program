# Bonus Challenge - MITRE ATT&CK Mapping

## Approach

The mappings below describe how behavior observed during the hunt aligns with ATT&CK techniques. They are behavioral mappings, not claims that an attacker performed the activity. The hunt's final disposition remains **Close - Benign** with **Medium** confidence.

---

## T1053.003 - Scheduled Task/Job: Cron

### Observed behavior

The host had several recurring cron jobs. Two recent entries were `/etc/cron.d/dev-health-check` and `/etc/cron.d/config-backup`, running every 15 minutes and every five minutes respectively. The hunt pivot also uncovered `/usr/local/bin/detect-ssh-bruteforce.sh` running every minute from the root user's crontab.

### Why the mapping fits

T1053.003 covers cron-based scheduled execution on Unix-like systems. Each of these jobs used cron to launch a command repeatedly without an interactive user session. That is the same mechanism an adversary could use for persistence or recurring execution, even though the surrounding evidence in this case supported legitimate administrative or defensive use.

### Supporting evidence

- `evidence/command-output/01-cron-enumeration.txt`
- `evidence/logs/04-cron-execution.log`
- `evidence/command-output/06-root-crontab.txt`
- `evidence/artifacts/config-backup.cron`
- `evidence/artifacts/dev-health-check.cron`
- `evidence/artifacts/root-crontab.txt`

The journal confirmed that the jobs were actually executing, not merely present in configuration files.

### Mapping confidence

**High.** The cron configuration and recurring execution are directly observable. High confidence here applies to the technique mapping, not to malicious intent.

---

## T1560.001 - Archive Collected Data: Archive via Utility

### Observed behavior

`/usr/local/bin/config-backup.sh` used standard Linux archiving tools to create timestamped `.tar.gz` files under `/var/tmp`. The archive contained `/etc/hosts` and `/etc/ssh/sshd_config`, and multiple archive files were observed.

### Why the mapping fits

T1560.001 describes the use of utilities such as `tar` and `gzip` to package or compress data. The script did exactly that. An attacker could use the same technique to stage collected information before exfiltration, but the hunt found no evidence that these archives left the host or were used for a malicious purpose.

### Supporting evidence

- `evidence/command-output/02-script-inspection.txt`
- `evidence/command-output/03-var-tmp-artifacts.txt`
- `evidence/artifacts/config-backup.sh`
- `evidence/artifacts/config-backup-archive-contents.txt`

The file timestamps also lined up with manual and scheduled execution of the backup script.

### Mapping confidence

**High.** The script and resulting `.tar.gz` artifacts directly show archive creation through a standard utility. The confidence applies to the behavior-to-technique mapping; the broader evidence still supports a benign explanation.

---

## T1543.002 - Create or Modify System Process: Systemd Service

### Observed behavior

The systemd review identified the custom `company-web.service`. It contained an `ExecStart` directive, ran as `analyst`, launched a Python Flask application from `/home/analyst/internal-web-outage-lab`, and was active on the system.

### Why the mapping fits

T1543.002 covers the use of systemd services for persistent or repeatable execution on Linux. A custom unit file gives the operating system a defined way to start and manage a process, which is the same mechanism an adversary could abuse. Here, however, the service predated the hunt and matched an existing internal lab application.

### Supporting evidence

- `evidence/command-output/09-systemd-review.txt`
- `evidence/command-output/10-company-web-review.txt`

Those files show both the unit configuration and the application context behind it.

### Mapping confidence

**Medium.** The systemd mechanism clearly aligns with T1543.002, but the hunt observed an existing service rather than its creation. The available context strongly supported legitimate application hosting.

---

## Additional Data Source - Linux auditd

The single data source that would most improve visibility into all three behaviors is Linux `auditd` telemetry.

With appropriate audit rules, I could see:

- Process execution and command-line arguments
- Executing and effective users
- Parent-child process relationships
- Creation or modification of cron files
- Changes to systemd unit files
- Execution of `tar` or related archive utilities
- File creation associated with those commands

For cron, audit rules could watch `/etc/crontab`, `/etc/cron.d/`, and user crontab locations. For systemd, they could monitor `/etc/systemd/system/`, `/usr/lib/systemd/system/`, and relevant `systemctl` activity. For archive behavior, `execve` records would show the exact `tar` command, the account that launched it, and its process ancestry.

That would provide stronger attribution than relying mainly on cron journals, sudo logs, script contents, and file timestamps.

---

## Takeaway

ATT&CK is useful for naming the behavior, but it does not determine intent. This hunt contained several actions that line up with techniques attackers can use - cron scheduling, archive creation, and systemd-based execution - yet the surrounding account, sudo, historical login, script, and application context supported a benign disposition.

The technique mapping explains **how** the behavior works. The evidence determines **what it means in this case**.
