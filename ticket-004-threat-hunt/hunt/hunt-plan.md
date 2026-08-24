# Ticket #004 - Threat Hunt Plan

## Objective

Test whether the Ubuntu lab host shows evidence of unauthorized persistence through cron, user crontabs, systemd services, systemd timers, or closely related scheduled execution.

The hunt will begin with scheduled-task configuration and expand only when a finding creates a specific new question.

---

## Target System

- **Host:** `ubuntu-soc-lab`
- **Operating system:** Ubuntu Linux
- **Role:** Authorized cybersecurity lab system

The initial scope is this host only. I will widen the hunt if the evidence points to another account, source address, host, process, or persistence mechanism.

---

## Timeframe

I will start with the current system state and recent activity, then narrow the timeframe around any meaningful timestamps that emerge. The initial review will include:

- Recent cron and systemd configuration
- Authentication activity
- Sudo and other privileged activity
- Relevant journal events
- File metadata
- Evidence of actual scheduled execution

---

## Data Sources

### Cron Configuration

**Where I will look**

- `/etc/crontab`
- `/etc/cron.d/`
- `/etc/cron.daily/`
- `/etc/cron.hourly/`
- `/etc/cron.weekly/`
- `/etc/cron.monthly/`
- User crontabs

**Why it matters**

Cron is widely used for legitimate administration, but it also gives an attacker a simple way to schedule repeat execution. I will look for recent changes, unfamiliar commands, unusual frequencies, unexpected users, and scripts launched from questionable locations.

### Systemd Services and Timers

**Where I will look**

- `/etc/systemd/system/`
- `/usr/lib/systemd/system/`
- `/lib/systemd/system/`
- `systemctl` service and timer listings
- systemd journal events

**Why it matters**

A service or timer can provide both persistence and recurring execution. I will pay attention to recently modified units, misleading names, unexpected accounts, unusual `ExecStart` values, and scripts outside normal application paths.

### Authentication Telemetry

**Sources**

- `/var/log/auth.log`
- SSH service logs
- Authentication events in the journal

**Why it matters**

If a suspicious change followed an interactive login, the source account and source address can help separate expected administration from unexplained access.

### Sudo and Privileged Activity

**Sources**

- `/var/log/auth.log`
- systemd journal
- Available shell history when relevant

**Why it matters**

System-level cron and systemd changes usually require elevated privileges. I will correlate sudo or root activity with the timestamps of any suspicious configuration changes.

### File Metadata

**Likely locations**

- `/etc/cron*`
- `/etc/systemd/system/`
- `/tmp/`
- `/var/tmp/`
- User home directories
- Any paths referenced by scheduled tasks

**Why it matters**

Ownership, permissions, timestamps, and file locations can show when an artifact appeared and whether it lines up with login or sudo activity.

### Process and Execution Evidence

**Sources**

- `ps`
- `journalctl`
- `systemctl`
- Other process information available during the hunt

**Why it matters**

A suspicious configuration is more meaningful if the command actually ran. I will look for repeated execution, cron or systemd parentage, and processes running under unexpected accounts.

---

## Behaviors of Interest

I am specifically looking for:

1. New or modified cron jobs.
2. New or modified systemd services or timers.
3. Scheduled scripts running from unusual filesystem locations.
4. Jobs owned by or executed as unexpected users.
5. Privileged changes associated with scheduled execution.
6. Authentication events immediately before those changes.
7. Files or processes that match the schedule.
8. Attempts to make persistence resemble ordinary administration.

---

## What Would Strengthen the Hypothesis

The hypothesis becomes more credible if several of these appear together:

- A recent scheduled task with no clear legitimate purpose.
- Execution from an unusual directory.
- An unexpected account or source address.
- Unexplained sudo or root activity.
- Correlated file creation or modification.
- Confirmed repeated execution.
- Multiple suspicious events in the same timeframe.

---

## What Would Weaken the Hypothesis

I will reduce confidence in unauthorized persistence if:

- The jobs match expected system or administrative behavior.
- Legitimate package or application activity explains the changes.
- Authentication comes from expected accounts and familiar sources.
- Privilege use is consistent with normal administration.
- The referenced scripts have clear, benign purposes.
- No related suspicious execution or file activity appears.

---

## When I Will Pivot

I will expand beyond the original path when a finding raises a concrete new question. Examples include:

- An unfamiliar user account
- An unusual SSH source
- A script that does not match the job's apparent purpose
- An unexpected systemd unit
- Unexplained privilege escalation
- Suspicious network activity
- Another persistence mechanism
- Evidence involving another host

Any such expansion will be documented as a hunt pivot.

---

## Disposition Thresholds

### Close - Benign

Use when the evidence gives a credible and adequately supported legitimate explanation.

### Close - Insufficient Evidence

Use when the activity cannot be confidently classified and available telemetry is not enough to resolve authorization or intent.

### Escalate for Investigation

Use when multiple correlated findings indicate potentially unauthorized activity that merits incident-response procedures.

### Confirmed Security Incident

Use only when the evidence establishes unauthorized or malicious activity.

---

## Stopping Criteria

I will stop when the original hypothesis and major competing explanations have been tested, relevant findings have been correlated across the available telemetry, required pivots have been completed, and no remaining lead is likely to materially change the disposition.

The hunt will not continue simply because more logs or systems could theoretically be examined.
