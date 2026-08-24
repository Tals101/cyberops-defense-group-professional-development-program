# Ticket #004 — Threat Hunt Hypothesis

## Hunt Hypothesis

If unauthorized persistence through scheduled tasks is occurring on the Linux system, I would expect to observe newly created or modified cron jobs or systemd services associated with unusual commands, users, files, or execution times because scheduled tasks are commonly used by both legitimate administrators and attackers to execute commands persistently.

---

## Known Facts

- A security analyst observed activity in the development environment that appeared unusual.
- The activity did not trigger a high-confidence security alert.
- No confirmed security incident has been declared.
- There is no known indicator of compromise (IOC).
- The analyst could not determine whether the activity was normal administrative behavior, a configuration change, unauthorized activity, persistence, or another type of activity.
- The SOC Manager requested a proactive, hypothesis-driven threat hunt.
- The hunt will be performed against a Linux system in an authorized cyber lab.
- The investigation must begin with a hypothesis rather than with simulated suspicious activity.
- The final conclusion must be based on evidence rather than assumptions.

---

## Unknowns

- What specific activity caused the analyst's concern.
- Which user account performed the activity.
- Whether the activity was authorized.
- Whether any scheduled tasks were recently created or modified.
- Whether cron, systemd, or another persistence mechanism was involved.
- Whether the observed activity was performed manually or automatically.
- Whether unusual processes or scripts are currently executing.
- Whether files associated with scheduled tasks were recently modified.
- Whether authentication activity occurred before the suspicious behavior.
- Whether privilege escalation occurred.
- Whether the activity originated locally or through a remote connection.
- Whether additional systems are affected.
- Whether the activity is part of routine administrative maintenance.
- Whether sufficient historical telemetry exists to establish a reliable baseline.

---

## Assumptions

- The Linux system is functioning normally enough to provide usable telemetry.
- Relevant system logs have not been deleted or significantly altered.
- Cron and systemd logs are available for the selected timeframe.
- Legitimate administrative activity may occur on the system.
- Scheduled tasks may be used by legitimate administrators.
- A scheduled task that appears unusual is not automatically malicious.
- Changes to scheduled tasks should leave evidence in configuration files, timestamps, logs, process activity, or command history.
- The analyst's observation may be related to persistence, but other explanations remain possible.
- The current user accounts and system configuration represent an approximately normal baseline unless evidence indicates otherwise.

These assumptions will be reevaluated as evidence is collected.

---

## Competing Explanations

### Explanation 1 — Legitimate Administrative Activity

A system administrator may have created or modified a cron job or systemd service as part of normal maintenance, automation, backups, monitoring, software updates, or application management.

This is a benign explanation.

Evidence supporting this explanation could include:

- A known administrative account performing the change.
- A scheduled task executing a legitimate system or maintenance script.
- Configuration consistent with other approved administrative tasks.
- Activity occurring during a normal maintenance period.
- No additional suspicious authentication, privilege escalation, or file activity.

### Explanation 2 — Legitimate Configuration Change With Poor Documentation

A developer or administrator may have changed a scheduled task for a legitimate purpose without properly documenting the change.

Evidence supporting this explanation could include:

- A recently modified cron or systemd configuration.
- Commands associated with development, testing, monitoring, or automation.
- Files located in expected application or administrative directories.
- No evidence of suspicious access or attempts to conceal the activity.

### Explanation 3 — Unauthorized Persistence

An unauthorized user may have created or modified a cron job or systemd service so that a command or script continues executing after the original access session ends.

Evidence supporting this explanation could include:

- A newly created or modified scheduled task with no clear administrative purpose.
- Execution from unusual locations such as /tmp, /var/tmp, or a user's hidden directory.
- A script or executable associated with an unexpected user.
- Scheduled execution at unusual or frequent intervals.
- Authentication or privilege escalation events shortly before the task was created.
- File modifications that correlate with the scheduled task.
- Attempts to disguise the task as a legitimate service.

### Explanation 4 — Application or Software Automation

An installed application, package, monitoring tool, or update process may have automatically created or modified a scheduled task.

Evidence supporting this explanation could include:

- Package installation or upgrade activity occurring near the same time.
- A scheduled task associated with a recognized package or application.
- Files owned by a legitimate package.
- Similar configuration documented by the installed software.

---

## Initial Hunt Focus

The hunt will initially focus on determining whether cron jobs or systemd services exist that are unusual when compared with expected administrative activity.

The investigation will not assume that an unusual scheduled task is malicious.

The objective will be to determine:

1. Whether scheduled persistence mechanisms are present.
2. Whether any were recently created or modified.
3. Which user or process is associated with them.
4. What commands or scripts they execute.
5. Whether related authentication, privilege escalation, process, or file activity provides additional context.
6. Whether the available evidence supports a benign explanation or warrants escalation.

---

## Evidence That Would Support the Hypothesis

- A recently created or modified cron job or systemd service.
- A scheduled task whose purpose cannot be explained by normal system administration.
- A scheduled task executing a script from an unusual location.
- A scheduled task associated with an unexpected or low-privileged user.
- Authentication activity shortly before the task was created.
- Use of sudo or another privilege escalation mechanism before the change.
- File creation or modification that correlates with the scheduled task.
- Repeated process execution matching the schedule.
- Attempts to hide or disguise the scheduled task.
- Multiple related suspicious behaviors occurring within the same timeframe.

---

## Evidence That Would Weaken or Disprove the Hypothesis

- All scheduled tasks can be linked to legitimate system or administrative functions.
- No recent cron or systemd changes are identified.
- Configuration files match known system defaults.
- Scheduled commands execute recognized applications from expected locations.
- Package installation or update records explain the configuration changes.
- Authentication and privilege activity are consistent with legitimate administrators.
- No related suspicious processes, files, or account activity are identified.
- The analyst's observation is better explained by another source of activity.

---

## Initial Escalation Criteria

The hunt may be escalated for formal investigation if multiple pieces of evidence indicate unauthorized persistence or related unauthorized activity.

Examples include:

- An unexplained persistence mechanism combined with suspicious authentication activity.
- A scheduled task executing an unknown script from an unusual directory.
- Evidence that an unexpected account created or modified the task.
- Privilege escalation associated with creation of the persistence mechanism.
- Evidence of concealment, unauthorized modification, or additional suspicious activity.

A single unusual cron job or systemd service will not automatically be treated as a confirmed incident.

---

## Initial Closure Criteria

The hunt may be closed as benign if available evidence demonstrates that the observed activity was legitimate and adequately explained.

The hunt may be closed as insufficient evidence if:

- Suspicious activity cannot be confirmed.
- Available telemetry does not provide enough evidence to determine authorization or intent.
- Additional investigation is unlikely to materially change the conclusion.

The final disposition will be determined only after the hunt is completed.
