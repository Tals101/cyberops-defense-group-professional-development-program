# Lessons Learned

## What Surprised Me

The biggest surprise was that users experienced a complete outage even though the Ubuntu server and Flask application were still working.

The server remained reachable, SSH was available, and the backend continued returning HTTP 200 on port 5050. The outage occurred because the user-facing layer was no longer available. That single failure prevented users from reaching an otherwise healthy application.

I was also surprised by how much of the incident could be reconstructed using standard Linux records. No single log explained everything. The sequence became clear only after I compared:

- Authentication activity
- Sudo commands
- Nginx service records
- Listening ports
- Active user sessions
- HTTP test results

This reinforced the value of checking several independent sources instead of relying on one command or log file.

## What I Would Check Earlier Next Time

During a similar outage, I would test the complete request path sooner:

`Client -> Network -> Port 80 -> Nginx -> Flask backend`

My first checks would be:

1. Confirm that the host is reachable.
2. Test the user-facing port.
3. Check the Nginx service state.
4. Test the backend directly.
5. Review the service journal.
6. Review recent SSH, sudo, and authentication activity.

Once the Nginx journal showed an orderly shutdown rather than a crash, the investigation shifted from software failure to service-control activity. In the future, I would make that shift earlier.

I would also check active administrative sessions sooner. Session information is temporary and can disappear when someone logs out or the server is restarted.

## Engineering Habits That Improved

The strongest habit I developed during this investigation was documenting each theory before acting on it.

For every possibility, I recorded:

- Why it seemed possible
- Evidence that supported it
- Evidence that did not fit
- The next useful test
- The result
- The updated conclusion

This prevented me from making unnecessary changes or focusing too heavily on the first explanation that seemed likely.

The engineering notebook also helped separate confirmed facts from assumptions. It provided a clear record of why certain possibilities were ruled out and why the investigation changed direction.

Another habit that improved was collecting evidence before restoring service. I preserved authentication records, session details, port information, and service logs before making changes that could have removed useful information.

## What I Would Automate

### User-Facing Health Checks

I would monitor the full application path instead of checking only whether the backend process is running.

The health check should confirm:

- TCP port 80 is reachable
- The expected HTTP status is returned
- The expected page content is present
- Response time remains acceptable
- An alert is triggered after repeated failures

### Critical Service Monitoring

I would monitor:

- Nginx service state
- Flask backend service state
- TCP port 80
- TCP port 5050
- Unexpected service stops
- Repeated service restarts

### Privileged Command Alerts

Commands that stop or change critical services should generate alerts.

Examples include:

- `systemctl stop nginx`
- `systemctl disable nginx`
- `systemctl stop company-web`
- Changes to Nginx configuration
- Changes to systemd service files

The alert should include:

- Username
- Source IP address
- Command
- Hostname
- Timestamp

### Incident Evidence Collection

A collection script could automatically gather:

- Current date and time
- Host information
- Service status
- Listening ports
- Recent systemd logs
- Authentication and sudo activity
- Logged-in users
- Active network connections
- HTTP test results
- SHA-256 hashes for collected evidence

### Recovery Checks

Post-recovery testing could also be automated to verify that:

- Required services are active
- Expected ports are listening
- HTTP requests succeed
- The correct content is returned
- External access works
- Services return after reboot

## What Remains Unanswered

The technical records established which account was used, where the session originated, which command was executed, and when Nginx stopped.

The available evidence did not establish:

- Whether the legitimate account owner used the session
- Whether the credentials were shared
- Whether the credentials were stolen
- Whether the command was accidental
- Whether the action was intentional
- Whether an undocumented change had been approved
- Whether the Kali system was compromised
- Whether similar activity occurred elsewhere
- Whether other users have more privilege than they need

Answering those questions would require additional sources, such as:

- Identity-provider records
- VPN or bastion logs
- Endpoint security telemetry
- Firewall and network-device logs
- SSH key inventories
- Change-management records
- Interviews with the account owner and administrators

## Final Takeaway

The user-facing symptom did not reveal the actual failed component.

A reliable investigation requires me to:

1. Test each layer separately.
2. Keep more than one explanation open.
3. Compare evidence from different sources.
4. Preserve temporary evidence before making changes.
5. Avoid conclusions that the records cannot support.
6. Contain risk before restoring service.
7. Test recovery from the user side.
8. Clearly document what is still unknown.
