# Ticket #004 - Lessons Learned

## 1. What was the original hypothesis?

I started with the possibility that someone had established unauthorized persistence through Linux scheduling mechanisms. If that were true, I expected to find recent or unexplained cron or systemd changes tied to unusual commands, users, locations, or execution patterns.

---

## 2. What assumption turned out to be incomplete?

Early in the hunt, a new root-level cron job running every five minutes looked like a strong warning sign. That was useful as a lead, but not as a conclusion.

The hunt reinforced that frequency, root privileges, and temporary storage can all appear in legitimate administration. I needed authentication, sudo history, script contents, and historical access patterns before the activity could be interpreted responsibly.

---

## 3. What evidence changed the assessment the most?

The biggest shift came from correlating three things: the analyst SSH session from `192.168.56.1`, the sudo commands that created the scripts and cron files, and the repeated history of analyst logins from the same source.

That combination turned the configuration backup from an unexplained persistence mechanism into activity with a credible administrative context.

---

## 4. What was the most useful pivot?

The strongest pivot came from `/usr/local/bin/detect-ssh-bruteforce.sh`.

Cron logs showed it running every minute as root, but it was not in `/etc/cron.d`. Tracing the job to the root user's crontab and then reading the script showed that it was checking failed SSH logins and generating warnings when a threshold was reached.

The pivot was valuable because it challenged the tendency to equate privileged persistence with malicious persistence.

---

## 5. What evidence did not materially affect the final decision?

Most of the standard systemd timers - `apt`, `logrotate`, `sysstat`, `fstrim`, and similar Ubuntu maintenance jobs - were expected and did not move the hunt forward.

The isolated sudo authentication failure at 17:50:04 also had little weight. It was followed within seconds by successful sudo activity from the same established session, so it did not meaningfully support an unauthorized-access explanation.

---

## 6. How did I decide to stop?

I stopped after the main hypothesis and competing explanations had been tested across the available telemetry. By that point I had correlated cron configuration with actual execution, inspected the scripts, reviewed the resulting artifacts, traced the changes through sudo, identified the SSH session source, compared it with historical access, completed the unexpected root-cron pivot, and reviewed systemd for another persistence path.

There was no remaining lead with a clear chance of changing the disposition. More collection was possible, but it was no longer likely to improve the decision.

---

## 7. What would I change in an enterprise environment?

I would rely much more heavily on centralized and authoritative context. In particular, I would:

- Search a SIEM across multiple Linux hosts instead of working host by host.
- Compare cron and systemd changes against an approved baseline.
- Use EDR or audit telemetry to reconstruct parent-child process relationships.
- Correlate SSH activity with identity-provider and privileged-access data.
- Check change-management records before relying on historical behavior as a proxy for authorization.
- Validate the source address against known administrative workstations.
- Use file-integrity monitoring for cron, systemd, and administrative script paths.
- Search enterprise-wide for the same filenames, hashes, commands, and schedules.
- Review network telemetry for outbound activity related to scheduled jobs.
- Confirm asset ownership and administrative responsibility through authoritative records.

Those sources would make it easier to distinguish a technically normal action from an actually authorized one and would support a higher-confidence conclusion.
