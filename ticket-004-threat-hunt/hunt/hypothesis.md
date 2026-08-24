# Ticket #004 - Threat Hunt Hypothesis

## Working Hypothesis

If someone has established unauthorized persistence through Linux scheduling mechanisms, I should find recent or unexplained cron or systemd changes that launch unusual commands or scripts, involve unexpected users or file locations, or run on a pattern that does not fit normal administration.

The goal is not to prove the hypothesis. It is to test it against the available evidence and be willing to reject it if a better explanation emerges.

---

## What I Knew at the Start

- An analyst noticed activity in the development environment that seemed unusual.
- No high-confidence alert had fired.
- No incident had been confirmed.
- There was no starting IOC.
- The activity had not yet been tied to a specific account, process, or persistence method.
- The SOC Manager requested a proactive, hypothesis-driven hunt.
- The work would take place on an authorized Ubuntu lab host.
- The scenario would be created only after the hypothesis and plan were documented.
- Any final disposition would need to be supported by evidence rather than by the appearance of a command or file.

---

## What I Did Not Know

At the outset, several basic questions were still open:

- What behavior originally raised concern?
- Which account performed it?
- Was the activity approved?
- Had any cron jobs, crontabs, systemd services, or timers changed recently?
- Was the activity manual or scheduled?
- Were unusual scripts or processes involved?
- Did authentication or sudo activity occur before the changes?
- Did the activity originate locally or over SSH?
- Was this limited to one host?
- Could normal maintenance, monitoring, backups, or application automation explain it?
- Was enough historical telemetry available to establish a useful baseline?

---

## Assumptions to Test

I began with several assumptions, but treated them as provisional:

- The host was healthy enough to provide usable logs and configuration data.
- Relevant logs had not been intentionally deleted or materially altered.
- Cron and systemd activity would leave enough evidence to reconstruct recent changes.
- Legitimate administrators may create scheduled tasks that look suspicious when viewed without context.
- A recent or frequent root-level job is not automatically malicious.
- Changes to scheduled execution should leave traces in files, metadata, logs, process activity, or command history.
- Persistence was only one possible explanation for the original concern.
- Current account and system behavior could be treated as an approximate baseline unless evidence showed otherwise.

These assumptions would be revisited as the hunt progressed.

---

## Competing Explanations

### 1. Routine Administration

An administrator may have added or changed a scheduled job for monitoring, maintenance, backups, updates, or automation.

Evidence that would support this explanation includes a known administrative account, a recognizable script, expected file locations, normal privilege use, and no related suspicious access.

### 2. Legitimate Change With Weak Documentation

A developer or administrator may have made a valid change without recording it through a formal change process.

I would expect to see activity that makes technical sense, uses normal tools and directories, and lacks signs of concealment or unauthorized access, even if a change ticket is missing.

### 3. Unauthorized Persistence

An unauthorized user may have created or modified a cron job or systemd unit so a command continues to run after the original session ends.

That explanation would become more plausible if I found an unexplained scheduled task, scripts in temporary or hidden locations, unexpected users, unusual privilege activity, suspicious authentication, or attempts to disguise the mechanism.

### 4. Application or Package Automation

Installed software, monitoring tools, package updates, or application components may have created scheduled execution automatically.

Package history, recognized ownership, expected commands, and documented application behavior would support this explanation.

---

## Initial Hunt Focus

I planned to start with cron and systemd because they are common Linux scheduling and persistence mechanisms. From there, I would follow the evidence into authentication, sudo activity, file metadata, process execution, or other areas as needed.

The first questions were:

1. What scheduled execution mechanisms are present?
2. Which ones are recent or unusual?
3. Who created or modified them?
4. What do they execute?
5. Do the commands actually run?
6. What authentication, privilege, file, or process evidence provides context?
7. Does the evidence support a benign explanation, an inconclusive result, or escalation?

---

## Evidence That Would Strengthen the Hypothesis

The unauthorized-persistence hypothesis would become stronger if I found:

- A recently created or modified cron job or systemd service with no clear business or administrative purpose.
- Scheduled execution from `/tmp`, `/var/tmp`, a hidden directory, or another unexpected location.
- An unexpected account associated with the change.
- Suspicious SSH activity shortly before the change.
- Sudo or root activity that could not be explained.
- File creation or modification that matched the schedule.
- Repeated execution consistent with the persistence mechanism.
- Attempts to conceal or disguise the task.
- Several related suspicious behaviors occurring in the same timeframe.

---

## Evidence That Would Weaken the Hypothesis

The hypothesis would lose support if:

- Scheduled jobs mapped cleanly to known system or administrative functions.
- No recent unexplained changes were present.
- Package or application activity explained the configuration.
- Authentication and sudo activity matched expected users and sources.
- Referenced scripts had understandable purposes and normal file locations.
- No related suspicious process, file, account, or network behavior appeared.
- Another explanation fit the evidence better.

---

## Escalation Criteria

I would consider formal incident escalation if multiple findings pointed in the same direction, for example:

- An unexplained scheduled task plus suspicious authentication.
- A task executing an unknown script from an unusual directory.
- An unexpected account creating or modifying persistence.
- Privilege escalation closely tied to the change.
- Evidence of concealment, unauthorized modification, network activity, or additional persistence.

One odd-looking cron job or service by itself would not be enough to declare an incident.

---

## Closure Criteria

The hunt could close as **Benign** if the activity was adequately explained by the evidence.

It could close as **Insufficient Evidence** if the available telemetry could not establish authorization or malicious intent and further collection was unlikely to change that.

It would move to formal investigation only if correlated evidence supported unauthorized or malicious activity.
