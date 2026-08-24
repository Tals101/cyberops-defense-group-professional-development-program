# Ticket #004 — Controlled Scenario Design

## Purpose

This scenario is being created only after the hunt hypothesis and hunt plan were completed.

The purpose is to generate both normal and suspicious-but-ambiguous Linux activity that can later be investigated without relying on an obvious malicious command.

The scenario design is documented separately from the Engineering Notebook so that investigative notes can be written as though the investigator did not already know what occurred.

---

## Normal Activity

A legitimate administrative health-check script will be created.

The script will:

- Run from /usr/local/bin/dev-health-check.sh
- Record the hostname, date, uptime, and disk usage
- Write results to /var/log/dev-health-check.log
- Execute through cron every 15 minutes

### Expected Interpretation

This represents normal administrative monitoring.

Although it creates a scheduled task, the command location, purpose, output location, and behavior should be consistent with legitimate administration.

---

## Suspicious-but-Ambiguous Activity

A second scheduled administrative-looking task will be created.

The task will:

- Run from /usr/local/bin/config-backup.sh
- Create a compressed archive containing selected system configuration files
- Store the archive under /var/tmp/
- Execute through cron every 5 minutes

The archive will contain copies of:

- /etc/hosts
- /etc/ssh/sshd_config

No passwords, private SSH keys, credentials, malware, or destructive commands will be used.

### Why This Activity Is Suspicious

The activity may warrant investigation because:

- The task runs more frequently than a normal configuration backup may require.
- The archive is written to /var/tmp instead of a dedicated backup directory.
- SSH configuration is being collected.
- The task is persistent through cron.

### Why This Activity Is Ambiguous

The activity is not automatically malicious because:

- Administrators may legitimately back up configuration files.
- The script will use ordinary Linux utilities.
- The destination remains on the local host.
- No external network connection or data exfiltration occurs.
- No attempt is made to disable logging or security controls.

Additional context will therefore be required before determining whether the activity is authorized or suspicious.

---

## Intended Hunt Questions

During the investigation, the hunter should determine:

1. What scheduled tasks exist?
2. Which scheduled tasks appear normal?
3. Which scheduled tasks deserve additional investigation?
4. What scripts do the tasks execute?
5. Where do those scripts write data?
6. Who created or modified the tasks?
7. Was elevated privilege involved?
8. Was there relevant authentication activity?
9. Does the evidence indicate legitimate administration or activity requiring escalation?

---

## Planned Hunt Pivot

The unusual destination under /var/tmp is expected to justify expanding the hunt into an area not originally central to the scheduled-task review.

The pivot will investigate:

- The archive stored in /var/tmp
- File ownership
- File permissions
- File modification timestamps
- Archive contents
- Correlated sudo or authentication activity

The actual Hunt Pivot will only be documented during the investigation if the collected evidence justifies it.

---

## Safety and Scope

All activity will occur only on the authorized ubuntu-soc-lab system.

The scenario will not:

- Contact external systems.
- Exfiltrate data.
- Modify passwords.
- Create malicious users.
- Install malware.
- Disable security controls.
- Delete logs.
- Modify SSH keys.
- Alter firewall rules.
