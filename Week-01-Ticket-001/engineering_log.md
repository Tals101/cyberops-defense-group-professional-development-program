# Ticket 001 Engineering Log

## Project Overview

This engineering log records how I worked through Ticket 001, including the investigation steps, technical decisions, problems I encountered, and changes I made along the way.

The ticket involved repeated SSH password failures against an Ubuntu server, followed by a successful login from the same source system.

All testing and investigation activity took place in an isolated and authorized lab environment.

## Initial Objective

My original objective was to determine:

- Which account was being targeted
- Where the SSH activity originated
- How many failed login attempts occurred
- Whether any login attempt succeeded
- Whether activity occurred after authentication
- Whether Wazuh detected the event
- What containment actions were appropriate
- Whether a repeatable detection method could be created

## Lab Environment

| System | Role | IP Address |
|---|---|---|
| Windows 11 | Administration and evidence storage | 192.168.56.1 |
| Kali Linux | Simulated source system | 192.168.56.111 |
| Ubuntu Linux | SSH target and Wazuh endpoint | 192.168.56.121 |
| Wazuh server | Monitoring and alert review | 192.168.56.122 |

## Investigation Record

### 1. Established the Investigation Start Time

I recorded the beginning of the investigation so that later log searches could be limited to the correct time range.

This helped separate the Ticket 001 activity from older SSH events already present on the systems.

Supporting evidence:

- `evidence/lab-start-time.txt`

### 2. Generated Controlled SSH Activity

From the Kali Linux system, I generated repeated failed SSH password attempts against the `sshlab` account on the Ubuntu server.

I used an intentionally incorrect test password during the failure phase.

After the failures were recorded, I completed a successful SSH login from the same source system.

This created a controlled sequence that could be investigated across several evidence sources.

### 3. Reviewed Native Ubuntu SSH Logs

I began the investigation with native Ubuntu authentication records rather than depending entirely on Wazuh.

This decision became especially important because the Wazuh agent experienced a temporary connectivity problem.

The Ubuntu logs showed:

- Repeated failed password attempts
- The targeted `sshlab` account
- The source IP address `192.168.56.111`
- A successful SSH login from the same source
- Session activity associated with the successful login

Supporting evidence:

- `evidence/complete-ssh-incident-log.txt`
- `evidence/failed-logins.txt`
- `evidence/failed-attempts-by-ip.txt`
- `evidence/successful-login-session.txt`

### 4. Confirmed Failed and Successful Login History

I used `lastb` to review failed login history and `last` to review successful sessions.

These records provided an additional source of confirmation beyond the SSH service logs.

The failed-login history matched the repeated authentication failures, and the successful-login history confirmed that access was eventually gained.

Supporting evidence:

- `evidence/lastb-failures.txt`
- `evidence/last-successful-login.txt`

### 5. Verified Post-Login Activity

During the successful SSH session, a file named `ticket001-access.txt` was created in `/tmp`.

I collected the file metadata to confirm that activity occurred after authentication.

This was important because it showed that the event was not limited to unsuccessful login attempts.

Supporting evidence:

- `evidence/post-login-artifact.txt`

### 6. Reviewed Wazuh Agent Status

The Wazuh agent was initially pending or disconnected.

This created a temporary visibility gap and explained why some early activity was not immediately visible in the Wazuh dashboard.

Instead of stopping the investigation, I continued using the native Ubuntu records as the primary evidence source.

After confirming that the agent was connected, I repeated controlled activity so Wazuh detection could be tested properly.

Supporting evidence:

- `evidence/wazuh-agent-state.txt`
- `evidence/wazuh-detection-test-start.txt`

### 7. Validated Wazuh Alerts

Once agent connectivity was restored, Wazuh generated alerts related to the SSH activity.

I reviewed the alert findings and captured screenshots showing the detection results.

The relevant detections included:

- Wazuh rule 5551 for repeated authentication failures
- Wazuh rule 40112 for multiple failures followed by successful authentication

The Wazuh alerts supported the conclusions already established through native Linux logs.

Supporting evidence:

- `evidence/wazuh-alert-findings.txt`
- `evidence/wazuh-test-failed-logins.txt`
- `screenshots/wazuh-ssh-bruteforce-alert.png`
- `screenshots/wazuh-failures-followed-by-success.png`

### 8. Locked the Affected Account

After confirming that the login had succeeded, I locked the `sshlab` account.

This was the most direct account-level containment action because it prevented the same account credentials from being used again during the investigation.

Supporting evidence:

- `evidence/containment-account-lock.txt`

### 9. Tested a Temporary Network Block

I created a temporary nftables rule to block the source IP address.

The block worked and prevented additional SSH access from the Kali Linux system.

However, it also interrupted further authorized testing. I removed the rule so the lab work could continue.

This showed the importance of planning both the expected impact and rollback procedure before applying a containment control.

Supporting evidence:

- `evidence/containment-firewall-rule.txt`

### 10. Developed a Custom SSH Detector

I created a Bash script that reviewed recent SSH authentication failures and counted the number of failures associated with each source IP.

The detector generated an alert when the configured threshold was reached.

The script demonstrated a practical way to automate repeated review of authentication logs.

Configuration:

- `configs/detect-ssh-bruteforce.sh`

Supporting evidence:

- `evidence/custom-detection-alert.txt`

### 11. Scheduled the Detector with Cron

I added the detector to the root crontab so it could run automatically.

The scheduled execution worked and generated alert output.

Configuration:

- `configs/root-crontab.txt`

Supporting evidence:

- `evidence/automatic-detection-alerts.txt`
- `evidence/cron-detector-execution.txt`

### 12. Identified a Duplicate-Alert Limitation

Testing showed that the detector could generate repeated alerts for the same SSH events.

This happened because the script searched a rolling time window but did not store information about events it had already processed.

I documented this as a design limitation rather than hiding it.

A stronger version should include:

- Persistent state
- Duplicate-alert suppression
- Configurable thresholds
- Structured output
- Better error handling
- Centralized alert delivery

### 13. Built the Technical Timeline

I organized the important investigation events into a timeline.

The timeline connects the failed authentication attempts, successful login, post-login activity, Wazuh detection, containment, and custom detection work.

Supporting evidence:

- `evidence/technical_timeline.csv`

### 14. Prepared the Final Documentation

I created the following project documentation:

- Weekly project README
- Engineering log
- Lessons learned
- Formal incident report
- Architecture and evidence-flow diagram

Final documentation:

- `README.md`
- `engineering_log.md`
- `lessons_learned.md`
- `Incident_Report.pdf`
- `diagrams/ticket-001-architecture.svg`

### 15. Created and Validated the Evidence Manifests

I generated an inventory of the evidence files and recorded a SHA-256 hash for every evidence item included in the final portfolio.

I then recalculated each hash and compared it with the manifest.

All 19 validation checks passed.

Supporting evidence:

- `evidence/evidence-inventory.txt`
- `evidence/evidence-hashes.txt`

## Technical Decisions

### Native Logs as the Primary Evidence Source

I chose to begin with native Ubuntu logs because they were closest to the system where the SSH activity occurred.

This approach also protected the investigation from being dependent on Wazuh agent availability.

### Multiple Sources for Correlation

I compared service logs, login-history records, Wazuh findings, screenshots, and post-login file metadata.

Using several sources reduced the risk of drawing a conclusion from one incomplete record.

### Evidence Before Containment

I collected the key authentication and session evidence before applying the temporary source-IP block.

This preserved the sequence of events and prevented containment from disrupting the initial investigation.

### Temporary and Reversible Controls

The nftables block was intended as a temporary test rather than a permanent configuration change.

I removed it after validating its effect so the authorized lab work could continue.

### Automation Instead of Only Manual Review

Manual log review was useful during the investigation, but it would not be efficient as an ongoing monitoring method.

The Bash detector provided a repeatable starting point for automated SSH failure detection.

## Problems Encountered

### Wazuh Agent Connectivity

The Wazuh agent was not fully connected during part of the testing.

Resolution:

- Used native Ubuntu logs to continue the investigation
- Confirmed agent connectivity
- Repeated controlled activity
- Verified that Wazuh generated the expected alerts

### Firewall Rule Blocked Further Testing

The nftables rule prevented the authorized source system from reconnecting.

Resolution:

- Confirmed that the block worked
- Removed the temporary rule
- Continued the remaining lab tests

### Repeated Detector Alerts

The custom detector alerted on events that had already been counted during an earlier execution.

Resolution:

- Documented the limitation
- Identified persistent state and duplicate suppression as future improvements

### Windows `scp` Destination Error

The first transfer attempt failed because the destination path ended with a trailing backslash.

Resolution:

- Changed into the intended Windows destination directory
- Used `.` as the `scp` destination
- Confirmed that the files transferred successfully

### PowerShell Session Variables

Some PowerShell variables were lost after changing directories or working in a different session.

Resolution:

- Recreated paths from the current location
- Used `Test-Path` before rerunning validation commands
- Confirmed the evidence directory and hash manifest existed

## Results

The investigation established that:

- The `sshlab` account received 11 failed SSH password attempts
- The attempts originated from `192.168.56.111`
- A successful login followed the failed attempts
- A file was created after the successful login
- Wazuh detected the authentication activity after agent connectivity was confirmed
- The affected account was locked
- A temporary source-IP block was tested successfully
- A custom Bash detector was created and scheduled
- The detector worked but required duplicate-alert suppression
- The final evidence package passed SHA-256 validation

## Future Improvements

If I repeated the project, I would:

- Confirm Wazuh connectivity before generating any activity
- Begin the timeline at the start of the investigation
- Automate evidence collection earlier
- Add persistent state to the custom detector
- Suppress duplicate alerts
- Produce structured JSON or CSV alert output
- Document rollback commands before applying containment
- Create one validation script for inventory and hashing
- Add automated tests for the detector
- Prepare a shorter executive summary earlier

## Final Reflection

The most valuable part of this ticket was learning how several small pieces of evidence can be combined into one defensible conclusion.

The SSH service logs showed the authentication sequence, the login-history records confirmed the sessions, the file metadata confirmed post-login activity, and Wazuh provided an additional detection layer.

The technical problems were also useful. The Wazuh connectivity issue, firewall interruption, repeated alerts, and file-transfer error required troubleshooting rather than following a perfect sequence.

Documenting those issues made the project more realistic and gave me a clearer understanding of what I would improve in a production-ready investigation and detection process.
