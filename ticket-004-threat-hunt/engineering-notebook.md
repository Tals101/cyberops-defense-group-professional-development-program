# Ticket #004 - Engineering Notebook

## Investigation Start

### Question

What scheduled activity exists on the host, and is any of it unusual enough to justify a deeper look?

### Expected Evidence

If unauthorized scheduled persistence is present, I would expect to find recent cron or systemd changes, unfamiliar scripts, unusual execution intervals, unexpected locations, or jobs that do not fit routine administration.

If the hypothesis is wrong, the scheduled activity should be explainable by normal system or administrative functions.

### Observed Evidence

No evidence had been collected yet.

### Interpretation

The hypothesis was still open.

### Next Step

Enumerate cron configuration and identify anything recent, unfamiliar, or otherwise worth investigating.

---

## Investigation Step 1 - Cron Enumeration

### Question

Are there recent cron changes that stand out from the normal system jobs?

### Expected Evidence

I expected a potentially meaningful finding to show up as a recent modification, an unfamiliar command, an unusual frequency, an unexpected user, or a script that needed more context.

### Observed Evidence

Cron configuration was enumerated at `2026-08-23T17:58:22+00:00`.

Two entries were notably recent:

- `/etc/cron.d/dev-health-check`
  - Modified: 2026-08-23 17:51 UTC
  - Owner: root
  - Permissions: 644
  - Runs `/usr/local/bin/dev-health-check.sh` every 15 minutes

- `/etc/cron.d/config-backup`
  - Modified: 2026-08-23 17:55 UTC
  - Owner: root
  - Permissions: 644
  - Runs `/usr/local/bin/config-backup.sh` every five minutes

Older entries such as `e2scrub_all` and `sysstat` had recognizable system purposes and did not stand out in the same way.

Evidence: `evidence/command-output/01-cron-enumeration.txt`

### Interpretation

**Fact:** Two cron files were modified within minutes of the hunt timeframe.  
**Fact:** `config-backup` runs every five minutes as root.  
**Inference:** The backup job deserves more attention because it is recent, frequent, and privileged.  
**Assumption:** It could represent unauthorized persistence, but authorization and intent are still unknown.

This was enough to continue the hunt, not enough to call the activity malicious.

### Next Step

Read both scripts and determine what they do, where they write data, and whether either has an obvious administrative purpose.

---

## Investigation Step 2 - Script Inspection

### Question

What do the recent cron jobs actually execute?

### Expected Evidence

If the hypothesis is gaining support, I would expect at least one script to perform activity that is difficult to explain as routine administration, such as collecting sensitive configuration, writing to an odd location, or using an unusual execution pattern.

### Observed Evidence

The scripts were inspected at `2026-08-23T18:01:21+00:00`.

`/usr/local/bin/dev-health-check.sh`:

- Owned by root
- Mode 755
- Records hostname, timestamp, uptime, and root filesystem usage
- Writes to `/var/log/dev-health-check.log`

`/usr/local/bin/config-backup.sh`:

- Owned by root
- Mode 755
- Creates timestamped `.tar.gz` archives
- Writes them under `/var/tmp`
- Archives `/etc/hosts`
- Archives `/etc/ssh/sshd_config`
- Sets archive permissions to 600

Evidence: `evidence/command-output/02-script-inspection.txt`

### Interpretation

**Fact:** The health-check script collects ordinary system-health information and writes it to a normal log location.  
**Fact:** The backup script collects host and SSH configuration and stores compressed copies in `/var/tmp`.  
**Fact:** Both scripts are root-owned and executable.  
**Inference:** The health-check has a clear administrative purpose.  
**Inference:** The backup job deserves further review because of its five-minute schedule, SSH configuration collection, and temporary-directory destination.  
**Assumption:** The backup may be unauthorized, but I still do not know who created it or whether it was approved.

At this point the hypothesis had more support, but there was still no evidence of malicious intent.

### Next Step

Inspect `/var/tmp` for the resulting archives and confirm whether the backup job has actually executed more than once.

---

## Hunt Pivot - Unexpected SSH Detection Cron Job

### What I Found

While reviewing cron execution, I noticed another script running every minute as root:

`/usr/local/bin/detect-ssh-bruteforce.sh`

It had not appeared in the original `/etc/cron.d` review. Tracing the scheduling source showed the following entry in the root user's crontab:

`* * * * * /usr/local/bin/detect-ssh-bruteforce.sh`

The script reviews recent SSH logs, counts failed-password attempts by source IP, and writes an `auth.warning` message when five or more failures occur within five minutes.

### Why It Mattered

This was another persistent scheduled execution mechanism, and it ran with root privileges. The security-related filename was not enough reason to trust it, so it needed its own review.

### New Question

Was this an additional persistence mechanism, or an expected defensive control?

### Additional Evidence

- The script is root-owned.
- Its timestamp is 2026-07-20 19:36.
- It searches SSH logs for failed passwords.
- It uses `logger` to generate an alert when the threshold is met.
- The root crontab explicitly schedules it every minute.
- Journal records confirm repeated execution.

Evidence:

- `evidence/command-output/05-hunt-pivot-ssh-detection.txt`
- `evidence/command-output/06-root-crontab.txt`
- `evidence/logs/04-cron-execution.log`

### Interpretation

**Fact:** The root crontab runs `detect-ssh-bruteforce.sh` every minute.  
**Fact:** The script detects repeated SSH authentication failures and generates warnings.  
**Fact:** The task existed before the current scenario.  
**Inference:** Its behavior is consistent with defensive SSH monitoring.  
**Assumption:** It was intentionally installed by an authorized administrator; that authorization was not independently verified.

The pivot weakened the original hypothesis. It also reinforced an important point: persistence-like behavior must be interpreted in context.

### Next Step

Return to the recent backup task and determine which account created it by correlating its timestamps with authentication and sudo activity.

---

## Investigation Step 3 - Authentication and Privilege Correlation

### Question

Who created the recent scripts and cron entries, and how was privilege used?

### Expected Evidence

Unauthorized persistence might correlate with an unexpected account, unusual authentication, or unexplained privilege escalation. Legitimate administration should be traceable to an identifiable user and normal sudo activity.

### Observed Evidence

Authentication and sudo events from 17:48 through 17:57 UTC showed:

- 17:50:04 - one sudo authentication failure for `analyst`
- 17:50:09 - `analyst` used sudo to create `/usr/local/bin/dev-health-check.sh`
- 17:50:14 - `analyst` made the health-check script executable
- 17:51:34 - `analyst` created `/etc/cron.d/dev-health-check`
- 17:52:35 - `analyst` created `/usr/local/bin/config-backup.sh`
- 17:52:39 - `analyst` made `config-backup.sh` executable
- 17:54:33 - `analyst` manually ran `config-backup.sh` with sudo
- 17:55:47 - `analyst` created `/etc/cron.d/config-backup`
- 17:55:50 - `analyst` set permissions on the backup cron file

The commands came from TTY `pts/0`. No SSH login event fell inside the narrower 17:48-17:57 window.

Evidence: `evidence/logs/07-auth-sudo-correlation.log`

### Interpretation

**Fact:** The analyst account created both recent scripts and cron entries using sudo.  
**Fact:** The analyst manually ran the backup script before cron began running it.  
**Fact:** One failed sudo authentication occurred before successful sudo activity.  
**Fact:** The commands came from `pts/0`.  
**Inference:** The changes came from an identifiable interactive session rather than an unexplained background process.  
**Inference:** This weakens the idea that an unknown account established the persistence.  
**Assumption:** The analyst account and session were authorized; I still needed to establish where that session came from.

The isolated sudo failure had little weight because successful authenticated sudo activity followed within seconds.

### Next Step

Identify the source of the analyst session and compare it with prior login behavior.

---

## Investigation Step 4 - Session Origin and Historical Baseline

### Question

Did the privileged changes come from an unusual or previously unseen source?

### Expected Evidence

If the account were being used unexpectedly, I might see a new source address or a login pattern that did not match prior activity. A familiar source would support, but not prove, a benign explanation.

### Observed Evidence

The active analyst `pts/0` session began around 17:36 UTC and originated from `192.168.56.1`.

SSH telemetry showed:

- 17:35:59 - Accepted password for `analyst` from `192.168.56.1`
- The SSH session opened immediately afterward

Login history showed prior analyst sessions from `192.168.56.1` on August 12, August 11, August 10, July 30, July 29, July 28, July 27, July 22, July 21, and July 20.

Evidence: `evidence/logs/08-session-origin.log`

### Interpretation

**Fact:** The analyst authenticated from `192.168.56.1` immediately before the scenario activity.  
**Fact:** The same source appears repeatedly in earlier analyst login records.  
**Fact:** The privileged commands were issued from the `pts/0` session associated with that login.  
**Inference:** The source matches the analyst account's established access pattern.  
**Inference:** This further weakens the idea that an unknown external account created the recent jobs.  
**Assumption:** A historically familiar source means the activity was authorized. That remains an assumption because historical consistency is not the same as formal approval.

Nothing collected at this point showed account compromise or an anomalous login source.

### Next Step

Finish the planned persistence review by examining systemd services and timers for another unexplained mechanism.

---

## Investigation Step 5 - Systemd Review

### Question

Is there another recent systemd service or timer that could represent unexplained persistence?

### Expected Evidence

If the original hypothesis extends beyond cron, I would expect to find a recent service or timer with an unusual command, unexpected user, or questionable filesystem path.

### Observed Evidence

The timer review showed expected Ubuntu maintenance activity, including:

- `apt-daily`
- `apt-daily-upgrade`
- `logrotate`
- `fstrim`
- `sysstat`
- `dpkg-db-backup`
- `systemd-tmpfiles-clean`
- `fwupd-refresh`

One custom service stood out:

`/etc/systemd/system/company-web.service`

The service:

- Was modified on 2026-07-27
- Is described as `Internal Company Web Application`
- Runs as `analyst`
- Executes `/usr/bin/python3 /home/analyst/internal-web-outage-lab/app.py`
- Is enabled and active
- Serves locally at `127.0.0.1:5050`
- Shows normal Flask startup messages

Evidence:

- `evidence/command-output/09-systemd-review.txt`
- `evidence/command-output/10-company-web-review.txt`

### Interpretation

**Fact:** No new systemd timer tied to the current hunt timeframe was identified.  
**Fact:** `company-web.service` predates the current hunt and runs an identifiable internal application as `analyst`.  
**Inference:** The service is consistent with legitimate application hosting rather than unexplained persistence.  
**Inference:** The systemd review further weakens the unauthorized-persistence hypothesis.  
**Assumption:** The application was formally authorized; the service configuration itself cannot prove that.

No additional unexplained systemd persistence mechanism was found.

### Next Step

Decide whether the collected evidence is sufficient for a disposition and whether any remaining lead is likely to change it.

---

## Stop-Hunting Decision

### Question

Do I have enough evidence for a defensible disposition, or is there a specific unanswered question that would materially change the result?

### Evidence Considered

By this point the hunt had established that:

- Two recent cron tasks existed.
- The analyst account created both through sudo.
- The backup script ran manually and then repeatedly through cron.
- It collected configuration files but showed no external communication or destructive behavior.
- The analyst SSH session came from `192.168.56.1`.
- Historical analyst logins repeatedly used the same source.
- The root-crontab pivot led to a defensive SSH brute-force monitor.
- No additional unexplained systemd persistence was found.
- `company-web.service` predated the hunt and had a recognizable application purpose.

### Interpretation

**Fact:** Scheduled persistence mechanisms exist on the host.  
**Fact:** The recent cron tasks were created from an interactive analyst session using sudo.  
**Fact:** The analyst session came from a source repeatedly seen in historical logins.  
**Fact:** The systemd review did not reveal another unexplained persistence mechanism.  
**Inference:** The activity is most consistent with legitimate administrative or lab work.  
**Assumption:** The changes were formally authorized; no independent change record was available to confirm that.

### Disposition

**Close - Benign**

The unusual activity had a coherent administrative explanation, and the hunt found no evidence of account compromise, malicious persistence, malware execution, external command-and-control activity, or another condition requiring incident response.

### Confidence

**Medium**

Several independent sources support the same conclusion: cron configuration, execution logs, sudo telemetry, SSH authentication, historical login records, file metadata, script contents, and systemd configuration.

The strongest correlation is between the analyst SSH session, the sudo commands that created the jobs, and the history of the same source address.

The primary limitation is that no change ticket, administrator confirmation, or other authoritative record independently proves formal approval. Confidence could rise to High with that confirmation and would fall if new evidence showed compromised credentials, an anomalous source, hidden persistence, or related malicious activity.

---

## Why I Stopped Investigating

The hunt had covered the major telemetry sources in the plan and resolved the most important alternative explanations. I had reviewed cron configuration and execution, the referenced scripts, file artifacts, authentication, privilege use, session origin, historical login behavior, the root crontab pivot, systemd services, and systemd timers.

More data was available in theory, but there was no remaining evidence-driven lead. Continuing solely to collect additional logs would have been unlikely to change the disposition and would no longer have been a proportionate, hypothesis-driven use of time.
