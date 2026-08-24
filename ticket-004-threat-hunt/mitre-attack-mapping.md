# Bonus Challenge — MITRE ATT&CK Mapping

## Purpose

This section maps behaviors observed during the threat hunt to relevant MITRE ATT&CK techniques.

An ATT&CK mapping describes how observed system behavior corresponds to a technique that an adversary could abuse. It does not establish that the observed activity was malicious.

The final hunt disposition remains:

**Close — Benign**

**Confidence: Medium**

---

## T1053.003 — Scheduled Task/Job: Cron

### Observed Behavior

Multiple recurring Linux cron jobs were identified during the hunt.

The recently created tasks included:

- `/etc/cron.d/dev-health-check`
- `/etc/cron.d/config-backup`

The health-check task executed every 15 minutes as root.

The configuration-backup task executed every 5 minutes as root.

The hunt pivot also identified a root crontab entry that executed:

`/usr/local/bin/detect-ssh-bruteforce.sh`

every minute.

### Why the Technique Applies

MITRE ATT&CK T1053.003 describes the use of cron to schedule recurring execution on Unix-like operating systems.

The observed jobs caused scripts to execute automatically at defined intervals. From a behavioral perspective, this is the same scheduling mechanism an adversary could abuse to establish persistence or recurring execution.

The mapping describes the mechanism being used, not the intent behind it.

### Supporting Evidence

Relevant evidence includes:

- `evidence/command-output/01-cron-enumeration.txt`
- `evidence/logs/04-cron-execution.log`
- `evidence/command-output/06-root-crontab.txt`
- `evidence/artifacts/config-backup.cron`
- `evidence/artifacts/dev-health-check.cron`
- `evidence/artifacts/root-crontab.txt`

Cron journal telemetry confirmed that the tasks were not merely configured on disk; they were executing according to their schedules.

### Mapping Confidence

**High**

There is direct evidence of cron configuration and recurring cron execution.

This is High confidence in the ATT&CK technique mapping, not High confidence that the activity was malicious.

The investigation ultimately found evidence supporting legitimate administrative and defensive purposes for the scheduled jobs.

---

## T1560.001 — Archive Collected Data: Archive via Utility

### Observed Behavior

The script:

`/usr/local/bin/config-backup.sh`

created compressed configuration archives under `/var/tmp`.

The archive contained:

- `/etc/hosts`
- `/etc/ssh/sshd_config`

Timestamped files were created in the form:

`/var/tmp/dev-config-TIMESTAMP.tar.gz`

Multiple archives were observed during the hunt.

### Why the Technique Applies

MITRE ATT&CK T1560.001 describes the use of utilities such as `tar`, `gzip`, and similar tools to package or compress collected data.

The configuration-backup script used the standard Linux archive mechanism to package multiple configuration files into a compressed archive.

An adversary could use the same behavior to consolidate collected information before staging or exfiltration.

In this investigation, however, no evidence of exfiltration or malicious staging was identified.

### Supporting Evidence

Relevant evidence includes:

- `evidence/command-output/02-script-inspection.txt`
- `evidence/command-output/03-var-tmp-artifacts.txt`
- `evidence/artifacts/config-backup.sh`
- `evidence/artifacts/config-backup-archive-contents.txt`

Artifact timestamps also correlated with manual and scheduled execution of the backup script.

### Mapping Confidence

**High**

The script contents and resulting `.tar.gz` artifacts directly demonstrate use of an archiving utility.

The technique mapping is therefore strong.

The malicious interpretation is not supported because the broader evidence showed the script was created during the analyst session and no subsequent exfiltration behavior was identified.

---

## T1543.002 — Create or Modify System Process: Systemd Service

### Observed Behavior

During the systemd persistence review, the hunt identified the custom service:

`company-web.service`

The service:

- Was installed as a systemd service
- Contained an `ExecStart` directive
- Started a Python Flask application
- Ran as the `analyst` user
- Referenced `/home/analyst/internal-web-outage-lab`
- Was active on the system

### Why the Technique Applies

MITRE ATT&CK T1543.002 describes adversary use of systemd service unit files to provide repeated or persistent execution on Linux systems.

A custom systemd service provides a mechanism through which a process can be automatically managed and executed by the operating system.

The observed service therefore resembles the persistence mechanism described by the ATT&CK technique.

Context was critical in this case.

The service predated the current hunt and was consistent with an existing internal web-application lab. No evidence showed that it had been created or modified as part of malicious persistence.

### Supporting Evidence

Relevant evidence includes:

- `evidence/command-output/09-systemd-review.txt`
- `evidence/command-output/10-company-web-review.txt`

The evidence showed both the systemd configuration and the legitimate application associated with the service.

### Mapping Confidence

**Medium**

The systemd mechanism clearly corresponds to T1543.002.

Confidence is Medium rather than High because the hunt was reviewing an existing service rather than directly observing its creation during the investigation.

The evidence nevertheless strongly supported the conclusion that this particular service was legitimate.

---

# Additional Data Source

## Linux Audit Framework — auditd

One additional data source that would materially improve visibility across these behaviors is **Linux auditd telemetry**.

Auditd could provide detailed records of:

- Process execution
- Executing user
- Effective user and privilege context
- Parent and child process relationships
- Command-line arguments
- File creation
- File modification
- Changes to cron configuration
- Changes to systemd unit files
- Execution of archive utilities such as `tar`

For the cron behavior, audit rules could monitor changes to locations such as:

- `/etc/crontab`
- `/etc/cron.d/`
- User crontab locations

For systemd behavior, audit rules could monitor:

- `/etc/systemd/system/`
- `/usr/lib/systemd/system/`
- Relevant `systemctl` execution

For archive behavior, process telemetry could show the exact execution of `tar`, its parent process, account context, command-line arguments, and resulting file creation.

MITRE's current cron detection guidance specifically identifies auditd file-modification and `execve` process telemetry as useful for detecting cron creation/modification followed by execution.

This would provide stronger attribution than relying primarily on cron journals, sudo logs, script contents, and file timestamps.

---

# Analytical Conclusion

The ATT&CK mappings demonstrate an important threat-hunting principle:

**A behavior can match an adversary technique without being adversary activity.**

The hunt observed mechanisms that attackers could abuse:

- Scheduled execution through cron
- Data archiving with standard Linux utilities
- Persistent execution through systemd

However, correlation with authentication, sudo activity, historical session origin, script contents, and application context produced a benign final disposition.

ATT&CK helped classify the behaviors.

The evidence determined the conclusion.
