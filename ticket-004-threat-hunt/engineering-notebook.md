# Ticket #004 — Engineering Notebook

## Investigation Start

### Question

What scheduled tasks currently exist on the Linux system, and are any of them unusual enough to require further investigation?

### Expected Evidence

If the hunt hypothesis is correct, I may observe:

- Recently created or modified cron jobs.
- Scheduled execution of unfamiliar scripts.
- Tasks running at unusual frequencies.
- Tasks executing from unexpected locations.
- Scheduled activity requiring additional context.

If the hypothesis is incorrect, I would expect the scheduled tasks to be explainable as normal system or administrative activity.

### Observed Evidence

Not yet collected.

### Interpretation

Pending evidence collection.

### Next Step

Enumerate cron configuration and identify scheduled tasks that warrant further analysis.

---

## Investigation Step 1 — Cron Enumeration

### Question

Are there recently created or modified scheduled tasks that warrant additional investigation?

### Expected Evidence

If the hypothesis is correct, I would expect to identify one or more recently modified cron entries, unfamiliar scripts, unusual execution frequencies, or tasks requiring additional context.

### Observed Evidence

Cron configuration was enumerated at 2026-08-23T17:58:22+00:00.

The following notable entries were identified:

- /etc/cron.d/dev-health-check
  - Modified: 2026-08-23 17:51 UTC
  - Owner: root
  - Permissions: 644
  - Executes /usr/local/bin/dev-health-check.sh every 15 minutes

- /etc/cron.d/config-backup
  - Modified: 2026-08-23 17:55 UTC
  - Owner: root
  - Permissions: 644
  - Executes /usr/local/bin/config-backup.sh every 5 minutes

Existing system cron entries such as e2scrub_all and sysstat had older timestamps or recognizable system purposes.

Evidence file:

05-evidence/command-output/01-cron-enumeration.txt

### Interpretation

FACT: Two cron files were modified within several minutes of the hunt timeframe.

FACT: The config-backup task executes every five minutes as root.

INFERENCE: The config-backup task warrants additional investigation because it is recent, runs frequently, and executes with root privileges.

ASSUMPTION: The config-backup task may represent unauthorized persistence. Authorization and intent have not yet been established.

The evidence supports continuing the hunt but does not establish malicious activity.

### Next Step

Inspect the scripts referenced by the two recent cron jobs to determine what they execute, where they write data, and whether either task has a clear administrative purpose.

---

## Investigation Step 2 — Script Inspection

### Question

What do the scripts referenced by the recently modified cron jobs actually do, and does either script contain behavior that warrants further investigation?

### Expected Evidence

If the hypothesis is correct, I would expect at least one scheduled script to perform activity that is unusual for normal administration, such as accessing system configuration, writing data to an unusual location, or otherwise requiring additional context.

### Observed Evidence

Script inspection was performed at 2026-08-23T18:01:21+00:00.

The following was observed:

- /usr/local/bin/dev-health-check.sh
  - Owned by root
  - Executable permissions: 755
  - Records hostname, timestamp, uptime, and root filesystem usage
  - Writes results to /var/log/dev-health-check.log

- /usr/local/bin/config-backup.sh
  - Owned by root
  - Executable permissions: 755
  - Creates timestamped .tar.gz archives
  - Stores archives under /var/tmp
  - Archives /etc/hosts
  - Archives /etc/ssh/sshd_config
  - Sets archive permissions to 600

Evidence file:

05-evidence/command-output/02-script-inspection.txt

### Interpretation

FACT: The health-check script collects routine system-health information and writes it to a conventional log location.

FACT: The config-backup script collects system and SSH configuration files and stores compressed archives under /var/tmp.

FACT: Both scripts are owned by root and have executable permissions.

INFERENCE: The health-check script has a readily apparent administrative purpose.

INFERENCE: The config-backup script warrants further investigation because it collects SSH configuration, executes frequently, and stores archives in a temporary directory.

ASSUMPTION: The config-backup activity may be unauthorized. No evidence collected so far establishes who created it or whether the activity was approved.

The original hypothesis is strengthened because a recently created persistence mechanism is performing unusual scheduled activity, but malicious intent has not been established.

### Next Step

Examine /var/tmp for artifacts created by the config-backup script and determine whether the scheduled task has actually executed repeatedly.

---

## Hunt Pivot — Unexpected SSH Detection Cron Job

### What I Discovered

While reviewing cron execution telemetry, I identified an unexpected scheduled script:

/usr/local/bin/detect-ssh-bruteforce.sh

The script was executing every minute as root even though it had not appeared in the original /etc/cron.d enumeration.

Further investigation showed that the task was configured in the root user's personal crontab:

* * * * * /usr/local/bin/detect-ssh-bruteforce.sh

The script itself checks recent SSH logs for repeated failed password attempts and generates an auth.warning message when five or more failures from the same source IP occur within five minutes.

### Why It Mattered

The task represented an additional persistent scheduled execution mechanism that was not identified during the original /etc/cron.d review.

Because it ran every minute as root, it could not be ignored simply because its filename appeared security-related.

### New Question

Was this unexpected scheduled task another persistence mechanism, or was it a legitimate defensive monitoring control?

### Additional Evidence Collected

- The script is owned by root.
- The script timestamp is 2026-07-20 19:36.
- The script searches SSH logs for failed password attempts.
- It generates alerts using logger when a threshold is exceeded.
- The root crontab explicitly schedules the script every minute.
- Journal evidence confirms repeated execution.

Evidence files:

- 05-evidence/command-output/05-hunt-pivot-ssh-detection.txt
- 05-evidence/command-output/06-root-crontab.txt
- 05-evidence/logs/04-cron-execution.log

### Evidence Classification

FACT: The root crontab schedules /usr/local/bin/detect-ssh-bruteforce.sh every minute.

FACT: The script examines SSH authentication failures and generates alerts when a threshold is exceeded.

FACT: The task existed before the current hunt scenario.

INFERENCE: The script is likely a defensive SSH brute-force monitoring control.

ASSUMPTION: The script was intentionally installed by an authorized administrator. Authorization has not yet been independently demonstrated.

### Effect on Original Hypothesis

The pivot weakened the original hypothesis.

Although an additional persistence mechanism was discovered, its behavior is consistent with defensive monitoring rather than unauthorized persistence.

The finding also demonstrated why scheduled execution alone is insufficient to classify activity as malicious.

### Next Step

Return to the recently created config-backup task and correlate its creation with authentication and sudo activity to determine which account created or modified it.

---

## Investigation Step 3 — Authentication and Privilege Correlation

### Question

Which account created the recently identified scheduled tasks, and was privileged access involved?

### Expected Evidence

If unauthorized persistence were occurring, I might expect an unexpected account, unusual authentication activity, or unexplained privilege escalation near the creation of the scheduled task.

If the activity were legitimate administration, I would expect the changes to correlate with an identifiable administrative account and normal sudo activity.

### Observed Evidence

Authentication and sudo telemetry from 17:48 through 17:57 UTC was reviewed.

The following events were identified:

- 17:50:04 — one sudo authentication failure occurred for the analyst account.
- 17:50:09 — analyst used sudo to create /usr/local/bin/dev-health-check.sh.
- 17:50:14 — analyst used sudo to make the health-check script executable.
- 17:51:34 — analyst used sudo to create /etc/cron.d/dev-health-check.
- 17:52:35 — analyst used sudo to create /usr/local/bin/config-backup.sh.
- 17:52:39 — analyst used sudo to make config-backup.sh executable.
- 17:54:33 — analyst manually executed config-backup.sh with sudo.
- 17:55:47 — analyst used sudo to create /etc/cron.d/config-backup.
- 17:55:50 — analyst set permissions on the config-backup cron file.

The commands originated from TTY pts/0.

No SSH login event was identified within the selected 17:48–17:57 UTC window.

Evidence file:

05-evidence/logs/07-auth-sudo-correlation.log

### Interpretation

FACT: The analyst account created both recently identified scripts and cron entries using sudo.

FACT: The analyst account manually executed config-backup.sh before the cron entry began executing it automatically.

FACT: One failed sudo authentication occurred before subsequent successful sudo activity.

FACT: The commands were executed from TTY pts/0.

INFERENCE: The creation of the config-backup task is associated with an identifiable interactive administrative session rather than an unexplained background process.

INFERENCE: This evidence weakens the hypothesis that an unknown account established persistence.

ASSUMPTION: The analyst account and its session were authorized. Authorization and the origin of the interactive session have not yet been independently established.

The sudo authentication failure alone is insufficient to indicate malicious activity because it was immediately followed by successful authenticated administrative activity.

### Next Step

Determine how the analyst session originated and whether the account's login activity is consistent with expected access.

---

## Investigation Step 4 — Session Origin and Historical Baseline

### Question

Did the analyst account's privileged activity originate from an unusual or previously unseen login source?

### Expected Evidence

If unauthorized access were involved, I might expect an unfamiliar source address, unusual login pattern, unexpected account, or authentication activity inconsistent with prior usage.

If the activity were consistent with normal administration, I would expect the session source and account to match historical access patterns.

### Observed Evidence

The current analyst pts/0 session began at approximately 17:36 UTC and originated from 192.168.56.1.

SSH telemetry showed:

- 17:35:59 — Accepted password for analyst from 192.168.56.1.
- An SSH session was opened for analyst immediately afterward.

Login history showed repeated prior analyst sessions from 192.168.56.1 on multiple dates, including August 12, August 11, August 10, July 30, July 29, July 28, July 27, July 22, July 21, and July 20.

Evidence file:

05-evidence/logs/08-session-origin.log

### Interpretation

FACT: The analyst account authenticated successfully through SSH from 192.168.56.1 immediately before the hunt scenario activity.

FACT: The same source address appears repeatedly in historical analyst login records.

FACT: The privileged commands that created the scheduled tasks were executed from the pts/0 session associated with that login.

INFERENCE: The session origin is consistent with the analyst account's historical access pattern.

INFERENCE: The evidence further weakens the hypothesis that an unknown external account established the recently identified persistence.

ASSUMPTION: Historical consistency means the activity was authorized. Historical consistency alone cannot prove authorization or intent.

No evidence collected so far demonstrates account compromise or an anomalous login source.

### Next Step

Complete the originally planned persistence review by examining recently modified systemd services and timers for additional unexplained persistence mechanisms.

---

## Investigation Step 5 — Systemd Persistence Review

### Question

Are there additional recently modified systemd services or timers that could represent unexplained persistence?

### Expected Evidence

If the original hypothesis were correct beyond the identified cron activity, I might expect to find recently created or modified systemd services or timers executing unusual commands, using unexpected accounts, or referencing suspicious filesystem locations.

### Observed Evidence

Systemd timers were reviewed and appeared consistent with normal Ubuntu maintenance functions, including:

- apt-daily
- apt-daily-upgrade
- logrotate
- fstrim
- sysstat
- dpkg-db-backup
- systemd-tmpfiles-clean
- fwupd-refresh

One recently modified service was identified:

/etc/systemd/system/company-web.service

The service:

- Was modified on 2026-07-27.
- Is named Internal Company Web Application.
- Runs as the analyst user.
- Executes /usr/bin/python3 /home/analyst/internal-web-outage-lab/app.py.
- Is enabled and active.
- Listens locally through the application at 127.0.0.1:5050.
- Shows normal Flask application startup messages.

Evidence files:

- 05-evidence/command-output/09-systemd-review.txt
- 05-evidence/command-output/10-company-web-review.txt

### Interpretation

FACT: No newly created systemd timer related to the current hunt timeframe was identified.

FACT: company-web.service predates the current hunt and runs an identifiable internal web application from the analyst user's home directory.

FACT: The service runs as analyst rather than root.

INFERENCE: The company-web service is consistent with legitimate application hosting rather than unauthorized persistence.

INFERENCE: The systemd review weakens the original unauthorized-persistence hypothesis.

ASSUMPTION: The company-web application is authorized. The service configuration alone cannot independently prove authorization.

No additional unexplained systemd persistence mechanism was identified.

### Next Step

Assess whether the collected evidence is sufficient to determine disposition and whether additional investigation is likely to materially change the conclusion.

---

## Stop-Hunting Decision

### Question

Has sufficient evidence been collected to determine a defensible disposition, or would additional investigation materially change the conclusion?

### Evidence Considered

The hunt established the following:

- Two recently created cron tasks were identified.
- Both tasks were created through sudo by the analyst account.
- The config-backup task executed repeatedly as configured.
- The config-backup script collected configuration files but did not communicate externally or perform destructive activity.
- The analyst session originated from 192.168.56.1.
- Historical login records showed repeated prior analyst access from the same source address.
- No anomalous SSH source associated with the activity was identified.
- The hunt pivot identified an additional root cron task running every minute.
- The pivoted task was determined to perform SSH brute-force detection.
- No additional unexplained systemd persistence mechanism was identified.
- The company-web service predates the hunt and has an identifiable application purpose.

### Interpretation

FACT: Scheduled persistence mechanisms exist on the system.

FACT: The recently identified cron tasks were created through an interactive analyst session using sudo.

FACT: The analyst session originated from a source address repeatedly observed in historical login records.

FACT: No additional unexplained persistence mechanism was identified during the systemd review.

INFERENCE: The activity is most consistent with legitimate administrative or lab activity rather than unauthorized persistence.

ASSUMPTION: The analyst activity was formally authorized. No external change ticket or administrator approval record was available to independently verify authorization.

### Disposition

**Close — Benign**

The available evidence provides a reasonable explanation for the unusual scheduled activity and does not indicate account compromise, unauthorized persistence, malware execution, external command-and-control activity, or another condition requiring incident response.

The original hypothesis was therefore not supported strongly enough to justify escalation.

### Confidence Assessment

**Confidence: Medium**

Medium confidence was selected because multiple independent telemetry sources support the same explanation:

- Cron configuration
- Cron execution logs
- Sudo telemetry
- SSH authentication telemetry
- Historical login records
- File metadata
- Script contents
- Systemd configuration

The strongest evidence was the correlation between the analyst SSH session, the sudo commands that created the scheduled tasks, and the historical use of the same source address.

The primary missing evidence is independent confirmation that the administrative changes were formally approved.

Confidence could increase to High if a change ticket, administrator confirmation, or other authoritative record confirmed that the analyst activity was authorized.

Confidence would decrease if additional evidence showed account compromise, an anomalous source address, unauthorized credential use, or hidden persistence not identified during the hunt.

---

## How Did I Know When to Stop Investigating?

The hunt stopped when the original hypothesis had been tested using the major telemetry sources identified in the hunt plan and the most significant alternative explanations had been evaluated.

The investigation examined:

- Cron configuration
- Cron execution
- Referenced scripts
- File artifacts
- Authentication
- Privilege escalation
- Session origin
- Historical login behavior
- Root user cron
- Systemd services
- Systemd timers

The required hunt pivot was also completed and did not identify additional suspicious activity.

Additional logs or systems could always be examined, but no current evidence pointed to another meaningful lead.

Further investigation was therefore unlikely to materially change the disposition.

Continuing solely to collect more data would not have been a proportionate use of investigative effort.
