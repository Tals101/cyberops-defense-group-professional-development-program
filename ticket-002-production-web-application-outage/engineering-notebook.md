# Engineering Notebook

## Internal Web Application Outage Investigation

**Purpose:** Informal investigation scratchpad showing how the reasoning developed, changed, and was tested.

**Note:** This notebook was reconstructed from the investigation evidence after the lab was completed. Future notebooks should be updated live during troubleshooting.

---

## Initial Thoughts

Users reported that the internal web application was unavailable.

The ticket did not identify which component had failed. Possible causes included:

- Client-side issue
- Network connectivity
- Firewall filtering
- DNS failure
- Nginx failure
- Backend application failure
- Server infrastructure failure
- Docker or Kubernetes issues
- Configuration error
- Administrative or security-related activity

Normal request path:

`User browser → Network → TCP port 80 → Nginx → Flask backend on port 5050`

The first objective was to confirm the symptom and test each layer independently.

---

## Hypothesis 1: Complete Server Failure

### Initial Thought

The Ubuntu server may have crashed, shut down, or become unreachable.

### Evidence For

- Multiple users could not access the application.
- Browser access failed completely.

### Evidence Against

- The Ubuntu host remained reachable.
- SSH on TCP port 22 remained available.
- Other services continued running.
- The operating system remained operational.

### Status

**Ruled out.**

The server itself was still functioning.

---

## Hypothesis 2: Broad Network Failure

### Initial Thought

The network path between users and the Ubuntu server may have failed.

### Evidence For

- Users could not reach the web application.
- TCP port 80 was unavailable.

### Evidence Against

- The Ubuntu host responded to network testing.
- SSH on TCP port 22 remained reachable.
- Other network services remained available.
- Only the web application path was affected.

### Next Test

- Test host reachability.
- Test TCP ports 22 and 80 separately.
- Review listening ports on the Ubuntu server.

### Status

**Ruled out.**

The general network path remained operational.

---

## Hypothesis 3: Firewall Blocking TCP Port 80

### Initial Thought

A host or network firewall may have started blocking HTTP traffic.

### Evidence For

- TCP port 80 could not be reached externally.
- Other ports remained reachable.

### Evidence Against

- Listening-port inspection showed that nothing was listening on TCP port 80.
- Nginx was inactive.
- No firewall change was required during recovery.
- Starting Nginx restored TCP port 80 immediately.

### Next Test

- Inspect listening ports with `ss`.
- Review firewall status and rules if port 80 is listening locally.
- Compare local and remote HTTP tests.

### Status

**Ruled out.**

Port 80 was unavailable because Nginx was stopped, not because traffic was filtered.

---

## Hypothesis 4: DNS Failure

### Initial Thought

Users may have been unable to resolve the application hostname.

### Evidence For

- Browser access failed.
- DNS problems can appear to users as application outages.

### Evidence Against

- Direct testing by IP address also failed.
- Requests using `127.0.0.1` bypassed DNS completely.
- No DNS change was required during recovery.

### Next Test

- Access the application directly by IP address.
- Test the local service through the loopback address.
- Compare hostname and IP-based results.

### Status

**Ruled out.**

The outage remained present when DNS was bypassed.

---

## Hypothesis 5: Backend Application Failure

### Initial Thought

The Flask backend may have crashed or stopped responding.

### Evidence For

- Users could not access application content.
- A failed backend could make the complete application appear unavailable.

### Evidence Against

- `company-web.service` remained active.
- The backend remained listening on `127.0.0.1:5050`.
- Direct requests to port 5050 returned HTTP 200.
- No backend restart or code change was required.

### Next Test

- Check `company-web.service` status.
- Inspect whether port 5050 is listening.
- Send an HTTP request directly to port 5050.

### Status

**Ruled out.**

The backend application remained healthy throughout the outage.

---

## Hypothesis 6: Nginx Failure

### Initial Thought

Nginx may have crashed, stopped, or failed to accept connections.

### Evidence For

- TCP port 80 was not listening.
- `systemctl status nginx` showed Nginx inactive.
- The backend remained healthy.
- Users depended on Nginx to reach the backend.

### Evidence Against

- No evidence contradicted Nginx being the immediate failed component.

### Next Test

- Review Nginx service status.
- Review the Nginx systemd journal.
- Validate the configuration.
- Determine whether Nginx crashed or received a stop command.

### Status

**Confirmed as the immediate failed component.**

### Reasoning Update

The investigation narrowed from a general application outage to one question:

**Why did Nginx stop?**

---

## Hypothesis 7: Nginx Configuration Error

### Initial Thought

A syntax error or incorrect reverse-proxy setting may have prevented Nginx from operating.

### Evidence For

- Configuration errors can prevent Nginx from starting.
- Nginx was inactive.

### Evidence Against

- `sudo nginx -t` passed.
- The same configuration worked before the outage.
- Nginx restarted successfully without configuration changes.
- HTTP 200 responses returned after the restart.

### Next Test

- Run `sudo nginx -t`.
- Review recent configuration modifications.
- Restart Nginx without changing the configuration.
- Retest the application.

### Status

**Ruled out as the root cause.**

The existing Nginx configuration was valid.

---

## Hypothesis 8: Nginx Software Crash

### Initial Thought

The Nginx process may have terminated unexpectedly because of a software defect, resource issue, or process failure.

### Evidence For

- Nginx was inactive.
- TCP port 80 was no longer listening.
- Users lost access without advance warning.

### Evidence Against

- The systemd journal showed an orderly shutdown sequence.
- No segmentation fault, crash, or resource-exhaustion message was found.
- Nginx received a normal service-stop request.
- The service restarted successfully without repair or reinstallation.

### Next Test

- Review `journalctl -u nginx`.
- Search system logs for crash or out-of-memory events.
- Compare the shutdown time with authentication and sudo activity.

### Status

**Ruled out.**

### Reasoning Update

Nginx did not crash. The orderly shutdown indicated that a user or automated process had requested the service stop.

---

## Hypothesis 9: Docker Failure

### Initial Thought

Docker workloads on the server may have interfered with the application or taken over a required port.

### Evidence For

- Docker was installed on the Ubuntu server.
- Other lab services were running in containers.
- Container problems can affect web applications.

### Evidence Against

- Nginx and the Flask backend were host-based systemd services.
- Docker was not part of the application request path.
- Docker workloads continued operating on separate ports.
- No Docker restart or configuration change was required.
- Restarting Nginx alone restored the application.

### Next Test

- Review listening ports and associated processes.
- Confirm whether Nginx or the backend runs inside a container.
- Review active Docker containers and published ports.

### Status

**Ruled out.**

Docker was unrelated to the affected application path.

---

## Hypothesis 10: Kubernetes Failure

### Initial Thought

A Kubernetes pod, service, ingress, or cluster failure may have caused the application outage.

### Evidence For

- Kubernetes was present in the broader lab environment.
- Kubernetes failures can make applications unavailable.

### Evidence Against

- The affected application was not deployed in Kubernetes.
- No pod, service, ingress, or cluster dependency was identified.
- The application used Nginx and Flask directly on the Ubuntu host.
- No Kubernetes action was required during recovery.
- Restarting the host-based Nginx service restored access.

### Next Test

- Confirm the application deployment architecture.
- Check whether any Kubernetes resources expose the application.
- Compare the affected ports with Kubernetes services and NodePorts.

### Status

**Ruled out.**

Kubernetes was not part of the affected application architecture.

---

## Hypothesis 11: Administrative Action Stopped Nginx

### Initial Thought

Because the Nginx journal showed an orderly shutdown, a user or automated process may have executed a service-control command.

### Evidence For

- Authentication logs showed that `webadmin` logged in through SSH.
- The SSH connection originated from `192.168.56.111`.
- A failed sudo authentication event occurred during the session.
- Sudo records showed that the account executed:

`/usr/bin/systemctl stop nginx`

- The command timestamp matched the Nginx shutdown timestamp.
- The `webadmin` session remained active during the investigation.
- No approved maintenance was known at the time.

### Evidence Against

- No evidence contradicted the command and service-log correlation.
- The logs identify the account but do not prove which person operated it.

### Next Test

- Review focused SSH and sudo events.
- Compare the privileged-command timestamp with the Nginx journal.
- Review login history and active sessions.
- Correlate the SSH connection with its source IP address.

### Status

**Confirmed as the direct technical cause.**

### Reasoning Update

An authenticated privileged session stopped Nginx. This explained why the service shut down normally and why TCP port 80 disappeared while the backend remained healthy.

---

## Hypothesis 12: Confirmed Malicious Compromise

### Initial Thought

The privileged action may indicate that the application, server, or administrative account was compromised.

### Evidence For

- A privileged account disrupted a user-facing service.
- The SSH session originated from `192.168.56.111`.
- The action was not associated with known maintenance.
- A failed sudo authentication attempt occurred before the successful command.

### Evidence Against

- No application files were shown to have been modified.
- No malicious backend process was identified.
- No data theft or data alteration was detected.
- No persistence mechanism was found.
- The backend continued operating normally.
- Logs identify the account used, but not the person controlling it.
- The technical evidence cannot determine whether the action was accidental or intentional.

### Next Test

- Review application and system files for unexpected changes.
- Review persistence locations and scheduled tasks.
- Review endpoint telemetry from the source system.
- Check whether the credentials or SSH keys were shared or exposed.
- Compare the activity with approved change records.

### Status

**Not proven.**

### Reasoning Update

The incident was security-related because privileged activity caused an outage. However, the available evidence did not prove malicious intent, credential theft, server compromise, or backend application compromise.

---

## Working Conclusion

The immediate outage occurred because Nginx was stopped.

The direct technical sequence was:

`webadmin → SSH session from 192.168.56.111 → sudo systemctl stop nginx`

This removed the listener from TCP port 80 and prevented users from reaching the healthy Flask backend.

### Incident Classification

**Security-related availability incident caused by privileged administrative activity.**

### Confidence

- **High confidence** in the direct technical cause
- **Undetermined** whether the activity was accidental, intentional, or performed by the legitimate account owner

---

## Recovery Notes

- Preserved authentication, sudo, session, service, port, and HTTP evidence.
- Locked the `webadmin` account.
- Terminated the active SSH session.
- Validated the Nginx configuration.
- Restarted Nginx.
- Confirmed TCP port 80 was listening.
- Confirmed HTTP 200 through Nginx.
- Confirmed connectivity from Windows.
- Confirmed browser access.
- Confirmed services started automatically after reboot.
- Confirmed `webadmin` remained locked after reboot.

### Recovery Result

Service was restored without changing:

- The Flask backend
- Application code
- Docker
- Kubernetes
- DNS
- Firewall rules
- Network configuration

---

## Questions Still Open

- Was the legitimate account owner operating the SSH session?
- Were the credentials shared, stolen, or otherwise misused?
- Was the service-stop action accidental or intentional?
- Was there an approved change that was not documented?
- Was the Kali source system compromised?
- Do other accounts have excessive sudo permissions?
- Were any SSH keys or passwords exposed?
- Was similar privileged activity performed on other systems?

These questions could not be answered from the available server logs alone.

---

## Improvements Identified During Investigation

- Add external HTTP health monitoring.
- Alert when Nginx becomes inactive.
- Alert when TCP port 80 stops responding.
- Alert on privileged service-control commands.
- Centralize authentication, SSH, sudo, and systemd logs.
- Require individual administrative accounts.
- Require multifactor authentication.
- Restrict sudo permissions using least privilege.
- Use a controlled bastion or privileged access platform.
- Record administrative sessions.
- Establish formal change-control procedures.
- Review privileged access regularly.
- Add endpoint monitoring to administrative systems.
- Create a web-outage investigation runbook.
- Add reverse-proxy redundancy to remove the single point of failure.

---

## Habit for Future Investigations

For each new possibility, record the following while the investigation is still active.

### Hypothesis

What might be happening?

### Why It Is Plausible

What observation caused this hypothesis to be considered?

### Evidence For

What facts currently support it?

### Evidence Against

What facts contradict it?

### Next Test

What command, log, measurement, or experiment will test it?

### Test Result

What happened when the test was performed?

### Status

Choose one:

- New
- Investigating
- Supported
- Ruled out
- Confirmed
- Unable to determine

### Reasoning Update

What did the latest evidence change about the investigation?

### Timestamp

When was this entry or update made?

---

## Blank Hypothesis Template

### Hypothesis

[Describe the possible cause.]

### Why It Is Plausible

[Explain why this possibility is being considered.]

### Evidence For

- [Supporting evidence]

### Evidence Against

- [Contradicting evidence]

### Next Test

- [Next command, log, or validation step]

### Test Result

[Record the result.]

### Status

**Investigating**

### Reasoning Update

[Explain how the result changed the investigation.]

### Timestamp

[YYYY-MM-DD HH:MM Time Zone]
