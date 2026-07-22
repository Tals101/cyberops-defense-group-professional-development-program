# Ticket 001 — Lessons Learned

## What was the problem?

The Ubuntu SSH server received repeated failed password-authentication attempts against the `sshlab` account.

Eleven failed attempts from `192.168.56.111` were followed by a successful login from the same source IP. After authentication, the user created `/tmp/ticket001-access.txt`, confirming post-login activity.

## What evidence did I collect?

The investigation collected:

- Complete SSH service logs
- Failed password events
- Failed-attempt counts grouped by source IP
- Successful authentication and session records
- `last` successful-login history
- `lastb` failed-login history
- Post-login file metadata and content
- Wazuh agent-state information
- Wazuh alert findings
- Wazuh dashboard screenshots
- Custom detector alerts
- Cron execution evidence
- Account-lock evidence
- Temporary nftables rule evidence
- Technical timeline
- SHA-256 evidence hashes

The evidence established the source IP, target account, event sequence, successful login, post-login activity, detections, and containment actions.

## What incorrect assumption did I make?

I initially assumed the Wazuh agent was connected and collecting events throughout the test.

The agent was initially pending or disconnected, which created a temporary monitoring gap. Native Ubuntu logs still contained the authentication evidence, but Wazuh did not initially provide complete visibility.

I also assumed that a Windows `scp` destination ending with a trailing backslash would work correctly. The OpenSSH client interpreted the destination incorrectly, causing the first transfer attempt to fail.

## How did I solve it?

I checked the Wazuh agent state, confirmed its connection, and generated additional controlled authentication attempts so the Wazuh alerts could be validated.

I used native Linux logs, `last`, and `lastb` as independent evidence rather than relying only on the SIEM.

For the transfer issue, I changed into the Windows destination directory and used `.` as the `scp` destination. The complete project then transferred successfully.

I also:

- Locked the affected account
- Tested a temporary source-IP block
- Created a custom SSH brute-force detector
- Scheduled the detector through cron
- Preserved the evidence with SHA-256 hashes
- Verified the final ZIP contents before submission

## What will I do differently next time?

For future tickets, I will:

1. Confirm all monitoring agents are connected before testing.
2. Confirm logs are reaching the SIEM.
3. Record the test start time before generating activity.
4. Verify time synchronization across all systems.
5. Create the engineering log at the beginning of the ticket.
6. Record commands and findings as the work progresses.
7. Define expected results before each test.
8. Add persistent state and duplicate suppression to custom detectors.
9. Test transfer paths before the final handoff.
10. Review all closure requirements before creating the final ZIP.
11. Automate inventory, hashing, packaging, and verification.
12. Distinguish clearly between lab procedures and production recommendations.

## Key Technical Takeaway

A SIEM should not be treated as the only source of truth.

Native operating-system logs, authentication history, file metadata, network controls, and SIEM alerts should be correlated to build a reliable incident timeline.

## Professional Growth

This ticket improved my ability to:

- Investigate authentication incidents
- Correlate evidence from multiple sources
- Troubleshoot monitoring gaps
- Validate SIEM detections
- Apply account and network containment
- Create lightweight detection automation
- Preserve evidence integrity
- Produce reproducible technical documentation
- Prepare a professional ticket-closure package
