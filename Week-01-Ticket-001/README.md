# Ticket 001 — SSH Authentication Investigation

## Ticket Number

**Ticket 001**

## Objective

For this ticket, I investigated repeated SSH login failures against an Ubuntu server to determine whether the activity eventually resulted in a successful login.

My goal was to identify the source system, confirm which account was targeted, determine what happened after authentication, preserve the supporting evidence, validate the related Wazuh alerts, and apply appropriate containment measures.

## Environment

I completed the investigation in an isolated and authorized lab environment.

| System | Purpose | Lab IP Address |
|---|---|---|
| Windows 11 | Administration, documentation, and evidence storage | 192.168.56.1 |
| Kali Linux | Simulated source of the SSH activity | 192.168.56.111 |
| Ubuntu Linux | SSH target and Wazuh-monitored endpoint | 192.168.56.121 |
| Wazuh server | Alert monitoring and event review | 192.168.56.122 |

## Tools Used

I used the following tools and technologies during the investigation:

- Wazuh Manager
- Wazuh Dashboard
- Wazuh Linux Agent
- OpenSSH
- Windows OpenSSH client
- `sshpass`
- `scp`
- Linux SSH authentication logs
- `journalctl`
- `last`
- `lastb`
- Bash
- Cron
- nftables
- Linux account-management commands
- PowerShell
- SHA-256 hashing
- PowerShell `Get-FileHash`
- Markdown
- CSV
- PDF
- Microsoft Word
- SVG diagrams
- Git
- GitHub

## Problem Being Investigated

The Ubuntu server recorded multiple failed SSH password attempts against the `sshlab` account.

The attempts came from the Kali Linux system at `192.168.56.111`. A successful login from the same source followed shortly afterward.

I needed to answer several questions:

1. How many failed login attempts occurred?
2. Which account was targeted?
3. Which system generated the activity?
4. Did the login eventually succeed?
5. Was any activity performed after the successful login?
6. Did Wazuh detect the event correctly?
7. What containment and detection improvements were needed?

## Investigation Approach

I began with the native Ubuntu authentication records because they provided the most direct evidence of the SSH activity.

I reviewed:

- SSH service logs
- Failed authentication records
- Successful authentication records
- `lastb` failed-login history
- `last` successful-session history
- Post-login file metadata
- Wazuh alert data
- Wazuh screenshots
- Account-containment evidence
- Firewall-containment evidence
- Custom detector results

I compared multiple evidence sources instead of relying on a single log or alert. This allowed me to confirm that the activity was consistent across the operating system and the security-monitoring platform.

## Investigation Summary

The investigation confirmed that the `sshlab` account received **11 failed SSH password attempts** from `192.168.56.111`.

The failed attempts were followed by a successful SSH login from the same source system.

After logging in, the user created:

    /tmp/ticket001-access.txt

The file confirmed that activity occurred after authentication. The incident therefore involved more than unsuccessful login attempts.

The investigation established the following sequence:

1. Repeated SSH password failures targeted the `sshlab` account.
2. The attempts originated from `192.168.56.111`.
3. A successful login followed the failures.
4. A file was created after authentication.
5. Wazuh generated alerts related to the activity.
6. The affected account was locked.
7. A temporary firewall block was tested.
8. A custom Bash detector was developed and scheduled with cron.

## Evidence Supporting the Conclusion

The conclusion was supported by:

- `complete-ssh-incident-log.txt`
- `failed-logins.txt`
- `failed-attempts-by-ip.txt`
- `lastb-failures.txt`
- `successful-login-session.txt`
- `last-successful-login.txt`
- `post-login-artifact.txt`
- `wazuh-alert-findings.txt`
- `wazuh-agent-state.txt`
- `containment-account-lock.txt`
- `containment-firewall-rule.txt`
- `custom-detection-alert.txt`
- `automatic-detection-alerts.txt`
- `cron-detector-execution.txt`
- `technical_timeline.csv`
- Wazuh alert screenshots
- The SHA-256 evidence manifest

The evidence inventory and SHA-256 manifest are located in the `evidence` folder.

## Wazuh Detection Results

Wazuh generated alerts related to the SSH activity.

I reviewed:

- **Wazuh rule 5551**, which identified repeated SSH authentication failures
- **Wazuh rule 40112**, which identified multiple failures followed by successful authentication

These alerts supported the findings from the native Ubuntu logs.

The investigation also demonstrated the importance of confirming agent connectivity before beginning a detection test. At one point, the Wazuh agent was pending or disconnected, which temporarily limited monitoring visibility.

## Containment Actions

### Account Containment

After confirming the successful login, I locked the `sshlab` account.

This reduced the possibility that the same credentials could be used again while the investigation continued.

### Network Containment

I applied a temporary nftables rule to block the source IP address.

The rule successfully prevented additional SSH access from the Kali Linux system. I later removed it so authorized testing could continue.

In a production environment, I would coordinate this type of network block with the appropriate security or operations team.

## Custom Detection

I created a Bash script to identify repeated SSH authentication failures within a rolling time window.

The detector:

- Reviewed recent SSH authentication events
- Counted failures by source IP
- Compared the count with a defined threshold
- Generated an alert when the threshold was reached
- Recorded the alert for later review

I scheduled the script with cron so it could run automatically.

Testing confirmed that the detector worked. It also revealed that the same activity could generate repeated alerts because the script did not maintain state between executions.

A production-ready version should include:

- Duplicate-alert suppression
- Persistent event state
- Configurable thresholds
- Improved error handling
- Centralized alert delivery
- Automated testing

## Technical Challenges

### Wazuh Connectivity

The Wazuh agent was initially pending or disconnected.

This created a temporary monitoring gap, and some early activity was not immediately visible in the dashboard.

I used native Ubuntu logs as an independent source of evidence. After confirming that the agent was connected, I repeated controlled activity to validate Wazuh detection.

### Repeated Custom Alerts

The custom detector reviewed a rolling five-minute window.

Because it did not track which events had already been processed, it could generate more than one alert for the same activity.

I documented this limitation and identified persistent state and duplicate suppression as the main improvements needed.

### Firewall Rule Interrupted Testing

The temporary nftables rule worked as expected, but it also blocked additional authorized SSH testing.

I removed the rule before continuing. This reinforced the importance of defining the expected effect and rollback process before applying containment.

### Windows File-Transfer Path

The first `scp` transfer failed because the Windows destination path ended with a trailing backslash.

I resolved the issue by changing into the destination directory and using `.` as the transfer destination.

## Alternatives Considered

### Relying Only on Wazuh

I could have based the investigation only on Wazuh alerts.

I decided against that approach because the agent experienced a temporary connectivity problem. Native operating-system logs provided a reliable primary source and allowed me to validate the Wazuh findings independently.

### Blocking the Source Immediately

I could have blocked the source IP before completing the initial investigation.

Instead, I first collected enough evidence to understand the activity. This reduced the risk of interfering with the investigation before the important details were recorded.

### Using Only Manual Log Review

I could have continued reviewing the authentication logs manually.

I created a Bash detector because automation makes repeated checks more consistent and provides a foundation for future detection improvements.

## Lessons Learned

This ticket reinforced several important lessons:

- Confirm monitoring-agent connectivity before generating test activity.
- Verify that events are reaching the SIEM before relying on its alerts.
- Use native operating-system logs as an independent evidence source.
- Correlate multiple records before reaching a conclusion.
- Define the expected result before applying containment.
- Plan a rollback method before applying temporary controls.
- Record commands and findings during the investigation.
- Add state tracking and duplicate suppression to automated detectors.
- Test file-transfer paths before the final handoff.
- Automate evidence inventories, hashing, and validation when possible.
- Keep authorized lab procedures separate from production recommendations.

## What I Would Improve

If I repeated this project, I would:

- Verify Wazuh connectivity before generating any test activity
- Begin recording the technical timeline earlier
- Automate more of the evidence-collection process
- Add duplicate suppression to the detector
- Store detector state between cron executions
- Produce structured alert output
- Document the firewall rollback command before applying the block
- Validate the evidence package with one repeatable script
- Prepare the executive summary earlier in the reporting process

## Project Files

### Documentation

- `README.md`
- `engineering_log.md`
- `lessons_learned.md`
- `Incident_Report.pdf`

### Configuration

- `configs/detect-ssh-bruteforce.sh`
- `configs/root-crontab.txt`

### Evidence

The `evidence` folder contains authentication records, Wazuh findings, containment results, detector output, the technical timeline, the evidence inventory, and the SHA-256 manifest.

### Screenshots

The `screenshots` folder contains Wazuh alert screenshots that support the investigation findings.

### Diagram

The `diagrams` folder contains an SVG overview of the lab environment and evidence flow.

## Final Conclusion

The investigation confirmed that repeated SSH password failures against the `sshlab` account were followed by a successful login from the same source system.

Post-login file creation confirmed that activity occurred on the Ubuntu server after authentication.

I supported the conclusion with native Linux logs, Wazuh alerts, login-history records, screenshots, containment evidence, custom detector output, and SHA-256 validation.

The account was contained, a temporary network block was tested, and a custom automated detector was created to improve future monitoring visibility.
