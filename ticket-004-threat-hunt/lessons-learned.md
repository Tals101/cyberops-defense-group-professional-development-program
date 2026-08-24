# Ticket #004 — Lessons Learned

## 1. What was your original hypothesis?

My original hypothesis was:

If unauthorized persistence through scheduled tasks is occurring on the Linux system, I would expect to observe newly created or modified cron jobs or systemd services associated with unusual commands, users, files, or execution times because scheduled tasks are commonly used by both legitimate administrators and attackers to execute commands persistently.

---

## 2. What assumption turned out to be incorrect or incomplete?

An early assumption was that a recently created cron job running frequently as root might indicate unauthorized persistence.

That assumption was incomplete.

The investigation showed that scheduled execution, root privileges, and unusual file locations can be suspicious indicators, but they are not sufficient by themselves to establish malicious activity.

Additional context from sudo logs, SSH session history, script contents, and historical login patterns was necessary.

---

## 3. What evidence caused the most significant change in your thinking?

The most significant evidence was the correlation between the analyst account, the interactive SSH session from 192.168.56.1, and the sudo commands used to create the scripts and cron entries.

The login source also appeared repeatedly in historical analyst sessions.

This shifted the investigation away from an unexplained persistence scenario and toward legitimate administrative or lab activity.

---

## 4. What was your most valuable hunt pivot?

The most valuable pivot occurred when cron execution logs revealed:

/usr/local/bin/detect-ssh-bruteforce.sh

This task was running every minute but did not appear in the initial /etc/cron.d review.

Investigating the root crontab showed where the task was scheduled.

Reviewing the script showed that it was designed to detect repeated failed SSH authentication attempts and generate warnings.

This pivot demonstrated that even an unexpected root-level persistence mechanism may have a legitimate defensive purpose.

---

## 5. What evidence was available but ultimately not useful?

Several systemd timers were available for review, including apt, logrotate, sysstat, fstrim, and other normal Ubuntu maintenance tasks.

These did not materially contribute to the final conclusion because their functions were consistent with expected system behavior.

The single sudo authentication failure at 17:50:04 also did not materially support the unauthorized activity hypothesis because it was immediately followed by successful authenticated sudo activity from the same interactive session.

---

## 6. How did you decide when to stop hunting?

I stopped hunting when:

- The original hypothesis had been tested across the planned telemetry sources.
- Cron configuration and actual execution had been correlated.
- The scripts referenced by suspicious tasks had been inspected.
- Authentication and sudo activity had been correlated with the changes.
- The source of the analyst session had been identified.
- Historical login behavior had been reviewed.
- The required hunt pivot had been completed.
- Systemd services and timers had been examined for additional persistence.
- No new evidence pointed toward another meaningful investigative lead.

At that point, additional investigation was unlikely to materially change the disposition.

---

## 7. If you repeated this hunt in an enterprise environment, what would you do differently?

In an enterprise environment, I would improve the hunt by using centralized telemetry and formal authorization records.

I would:

- Query a SIEM across multiple Linux hosts.
- Compare scheduled tasks against an established baseline.
- Review EDR process ancestry for cron and systemd execution.
- Correlate authentication events with identity-provider telemetry.
- Check formal change-management records.
- Compare source addresses against known administrative workstations.
- Review file integrity monitoring data for cron and systemd changes.
- Search for the same scripts, filenames, hashes, or behaviors across other systems.
- Review network telemetry for outbound connections associated with scheduled tasks.
- Use asset ownership and administrator records to confirm whether activity was authorized.

This would provide stronger evidence for determining authorization and would allow higher-confidence conclusions.
