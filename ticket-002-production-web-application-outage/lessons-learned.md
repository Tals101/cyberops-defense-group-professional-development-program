# Lessons Learned

## What Surprised You?

The most surprising part of this investigation was that users experienced a complete application outage even though the Ubuntu server and Flask backend remained operational.

The server still responded to network testing, SSH remained available, and the backend continued returning HTTP 200 on port 5050. The loss of one user-facing component prevented users from reaching an otherwise healthy application.

It was also surprising how clearly the incident could be reconstructed by correlating several ordinary Linux data sources:

- Authentication logs
- Sudo records
- Systemd service journals
- Listening-port output
- Active-session information
- HTTP test results

No single log contained the entire explanation. The conclusion became clear only after the timestamps and events were compared.

## What Would You Investigate Sooner Next Time?

I would test the complete application path and its individual layers sooner:

`Client → Network → Web listener → Reverse proxy → Backend`

My earliest checks would be:

1. Confirm whether the host is reachable.
2. Test the user-facing TCP port.
3. Check the reverse-proxy service.
4. Test the backend directly.
5. Review the service journal.
6. Review recent sudo and authentication activity.

Once a service journal shows an orderly shutdown rather than a crash, I would immediately investigate who or what requested the service stop.

I would also check active administrative sessions earlier because live-session evidence can disappear when a user disconnects or the system is restarted.

## What Engineering Habit Improved During This Ticket?

The most important habit developed during this ticket was hypothesis-driven troubleshooting.

Instead of selecting one likely cause and attempting repairs, I documented each possibility using:

- Initial thought
- Evidence for
- Evidence against
- Next test
- Test result
- Status
- Reasoning update

This made the investigation more disciplined and prevented unrelated systems from being changed.

The Engineering Notebook also helped separate facts from assumptions. It showed why each possibility was considered, what evidence changed the direction of the investigation, and why a hypothesis was ultimately confirmed or rejected.

Another improved habit was preserving evidence before recovery. Authentication records, active sessions, listening ports, and service journals were collected before making unnecessary system changes.

## What Would You Automate?

### External Application Health Checks

I would automate an HTTP test against the complete user-facing path rather than monitoring only the backend process.

The check should validate:

- TCP connectivity
- Expected HTTP status
- Expected page content
- Response time
- Multiple consecutive failures before alerting

### Critical Service Monitoring

I would monitor:

- Nginx service state
- Backend service state
- TCP port 80
- TCP port 5050
- Unexpected service restarts or stops

### Privileged Command Detection

I would generate alerts for commands that control critical services, including:

- `systemctl stop nginx`
- `systemctl disable nginx`
- `systemctl stop company-web`
- Changes to Nginx configuration
- Changes to systemd unit files

Alerts should include the account, source address, command, timestamp, and hostname.

### Evidence Collection

I would create an incident-response script that automatically collects:

- Current time and host information
- Service status
- Listening ports
- Recent systemd journals
- Authentication and sudo events
- Logged-in users
- Active network sessions
- HTTP validation results
- SHA-256 evidence hashes

### Recovery Validation

I would automate post-recovery checks that confirm:

- Required services are active
- Required ports are listening
- HTTP requests succeed
- Expected content is returned
- External access works
- Services recover after reboot

## What Remains Unanswered?

The technical evidence identifies the account, source address, privileged command, affected service, and incident sequence.

It does not establish:

- Whether the legitimate account owner operated the session
- Whether credentials were shared
- Whether credentials were stolen
- Whether the action was accidental or intentional
- Whether an undocumented change had been approved
- Whether the Kali source system was compromised
- Whether similar activity occurred on other systems
- Whether other accounts have excessive privileges

Answering these questions would require additional sources, including:

- Identity-provider records
- VPN or bastion logs
- Endpoint detection telemetry
- Firewall and network-device logs
- SSH key inventories
- Change-management records
- Interviews with the account owner and administrators

## Final Lesson

The largest lesson from this ticket is that the user-visible symptom does not identify the technical cause.

A reliable investigation must:

1. Test each system layer independently.
2. Record competing hypotheses.
3. Correlate multiple evidence sources.
4. Preserve volatile evidence.
5. Avoid unsupported conclusions.
6. Contain risk before restoring service.
7. Validate recovery from the user perspective.
8. Document what remains unknown.
