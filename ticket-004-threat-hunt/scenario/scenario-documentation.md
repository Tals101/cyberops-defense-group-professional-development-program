# Ticket #004 - Controlled Scenario Design

## Purpose

The scenario was created only after the hypothesis and hunt plan were documented. The goal was to generate two believable kinds of Linux scheduled activity: one clearly routine and one suspicious enough to deserve investigation without being obviously malicious.

The scenario notes are kept separate from the Engineering Notebook so the investigative record can follow the evidence as if the hunter did not already know how the activity was produced.

---

## Normal Activity

A routine health-check script was created at:

`/usr/local/bin/dev-health-check.sh`

It records the hostname, date, uptime, and disk usage, writes the results to `/var/log/dev-health-check.log`, and runs every 15 minutes through cron.

### Why it should look normal

The script has a clear monitoring purpose, lives in a typical administrative location, writes to a conventional log path, and performs no unusual collection or network activity.

---

## Suspicious-but-Ambiguous Activity

A second script was created at:

`/usr/local/bin/config-backup.sh`

It creates a compressed archive containing:

- `/etc/hosts`
- `/etc/ssh/sshd_config`

The archive is written under `/var/tmp` and the task runs every five minutes through cron.

No credentials, private SSH keys, passwords, malware, or destructive commands are involved.

### Why it should attract attention

The job has several characteristics worth investigating:

- Five-minute execution is frequent for a configuration backup.
- It runs persistently through cron.
- It collects SSH configuration.
- It writes the output to `/var/tmp` instead of a dedicated backup directory.

### Why it remains ambiguous

The same behavior can still be legitimate. Administrators routinely back up configuration files, the script uses ordinary Linux utilities, the data stays on the host, and there is no exfiltration, logging suppression, or security-control tampering.

The scenario therefore requires context - especially account, sudo, authentication, and execution history - before a disposition can be made.

---

## Questions the Hunt Should Answer

1. What scheduled tasks are present?
2. Which ones fit normal system or administrative activity?
3. Which ones deserve a closer look?
4. What do the referenced scripts actually do?
5. Where do they write data?
6. Who created or changed the tasks?
7. Was privileged access involved?
8. What authentication activity occurred around the same time?
9. Does the combined evidence support routine administration, uncertainty, or escalation?

---

## Expected Area for Deeper Review

The `/var/tmp` destination was intentionally chosen to create a reasonable reason to expand the hunt beyond the cron file itself. A deeper review could examine:

- Archive filenames and timestamps
- Ownership and permissions
- Archive contents
- Correlated sudo activity
- Correlated authentication activity

Any actual pivot, however, would be documented only if the collected evidence justified it.

---

## Safety and Scope

All scenario activity stays on the authorized `ubuntu-soc-lab` host.

The scenario does not:

- Contact external systems
- Exfiltrate data
- Change passwords
- Create malicious users
- Install malware
- Disable security controls
- Delete logs
- Modify SSH keys
- Change firewall rules
