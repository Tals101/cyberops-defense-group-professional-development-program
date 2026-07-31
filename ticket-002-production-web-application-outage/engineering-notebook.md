# Engineering Notebook

## Internal Web Application Outage Investigation

**Purpose:** This notebook records how my thinking changed throughout the investigation, including the possibilities I considered, the evidence I compared, and the reasons each theory was either supported or ruled out.

**Note:** I reconstructed this notebook from the evidence collected during the completed lab. In a live incident, I would document these observations as the investigation unfolds.

---

## Initial Thoughts

The only confirmed symptom at the beginning was that users could no longer reach the internal web application. The ticket did not identify which part of the environment had failed.

I started with a broad list of possibilities:

- A client-side issue
- Loss of network connectivity
- DNS failure
- A problem with TCP port 80
- Nginx failure
- Flask backend failure
- A larger server problem
- Firewall filtering
- Docker interference
- Kubernetes failure
- A configuration problem
- Administrative or security-related activity

Rather than choosing one explanation too early, I planned to test each layer separately.

The expected request path was:

`User browser -> Network -> TCP port 80 -> Nginx -> Flask backend on port 5050`

---

## Hypothesis 1: The Entire Web Server Failed

### Why I Considered It

Because multiple users had lost access to the application, the Ubuntu server may have crashed, powered off, or become unreachable.

### What Supported It

- Several users could not open the application.
- Browser access failed completely.

### What Did Not Fit

- The Ubuntu host still responded.
- SSH remained reachable on TCP port 22.
- Other services were still running.
- The operating system itself was functioning normally.

### Result

**Ruled out.**

The host was still online, so this was not a complete server failure.

---

## Hypothesis 2: A Broader Network Failure

### Why I Considered It

The path between the users and the Ubuntu server may have been interrupted.

### What Supported It

- Users could not reach the web application.
- TCP port 80 was unavailable.

### What Did Not Fit

- The server responded to network testing.
- SSH remained accessible.
- Other network services were available.
- The failure was limited to the web application path.

### Result

**Ruled out.**

The network was working. The issue was isolated to the web service.

---

## Hypothesis 3: A Firewall Was Blocking Port 80

### Why I Considered It

A host-based or network firewall might have started rejecting HTTP traffic while allowing other connections.

### What Supported It

- External connections to TCP port 80 failed.
- Other ports were still reachable.

### What Did Not Fit

- Port inspection showed that no process was listening on TCP port 80.
- Nginx was inactive.
- I did not need to change any firewall rules during recovery.
- Port 80 returned immediately after Nginx was started.

### Result

**Ruled out.**

Traffic was not being filtered. Port 80 was unavailable because Nginx was not running.

---

## Hypothesis 4: DNS Failed

### Why I Considered It

A hostname-resolution problem can make a healthy application appear unavailable.

### What Supported It

- Users could not open the application in a browser.
- DNS problems often look like application outages from the user side.

### What Did Not Fit

- Direct testing by IP address failed as well.
- Local requests to `127.0.0.1` bypassed DNS.
- No DNS changes were needed to restore access.

### Result

**Ruled out.**

The problem remained even when DNS was removed from the request path.

---

## Hypothesis 5: The Flask Backend Failed

### Why I Considered It

The backend may have crashed, stopped listening, or become unable to return application content.

### What Supported It

- Users could not retrieve any application content.
- A failed backend could prevent the reverse proxy from serving the application correctly.

### What Did Not Fit

- `company-web.service` remained active.
- The Flask application was still listening on `127.0.0.1:5050`.
- Direct requests to port 5050 returned HTTP 200.
- The backend did not need to be restarted.
- No application code had to be changed.

### Result

**Ruled out.**

The Flask backend remained healthy throughout the outage.

---

## Hypothesis 6: Nginx Was the Failed Layer

### Why I Considered It

Nginx was responsible for accepting user requests on port 80 and forwarding them to the Flask backend.

### What Supported It

- Nothing was listening on TCP port 80.
- `systemctl status nginx` showed the service as inactive.
- The backend remained healthy.
- Users depended on Nginx to reach the backend.

### What Did Not Fit

- Nothing contradicted Nginx being the immediate failed component.

### Result

**Confirmed as the immediate failed component.**

At this point, I knew what had failed, but not yet why.

The next question became:

**Why did Nginx stop?**

---

## Hypothesis 7: The Nginx Configuration Was Invalid

### Why I Considered It

A syntax error or incorrect reverse-proxy setting could have prevented Nginx from starting or remaining operational.

### What Supported It

- Configuration mistakes are a common reason for a web service to fail.
- Nginx was inactive.

### What Did Not Fit

- `sudo nginx -t` completed successfully.
- The same configuration had worked before the outage.
- Nginx restarted without any configuration changes.
- HTTP 200 responses returned after the restart.

### Result

**Ruled out as the root cause.**

The Nginx configuration was valid.

---

## Hypothesis 8: Nginx Crashed

### Why I Considered It

A software defect, resource problem, or process failure may have caused Nginx to terminate unexpectedly.

### What Supported It

- Nginx was inactive.
- Port 80 was no longer listening.

### What Did Not Fit

- The systemd journal showed a clean, orderly shutdown.
- I found no segmentation fault, crash, or resource-exhaustion message.
- The service received a normal stop request.
- Nginx restarted without repairs or software changes.

### Result

**Ruled out.**

Nginx did not crash. It was stopped through a normal service-control action.

---

## Hypothesis 9: Docker Interfered With the Application

### Why I Considered It

Docker was installed on the host, and another workload could have interfered with ports or system resources.

### What Supported It

- Docker was present on the server.
- Other lab services were listening on separate ports.

### What Did Not Fit

- Nginx and Flask were running directly on the host as systemd services.
- Docker was not part of the application request path.
- Docker workloads continued operating independently.
- Recovery did not require any Docker changes.

### Result

**Ruled out.**

Docker was unrelated to this outage.

---

## Hypothesis 10: Kubernetes Caused the Failure

### Why I Considered It

The wider lab environment included Kubernetes, and a cluster, ingress, service, or workload issue can affect web applications.

### What Supported It

- Kubernetes existed elsewhere in the lab environment.
- Kubernetes failures can disrupt application traffic.

### What Did Not Fit

- This application was not deployed in Kubernetes.
- No pod, service, ingress, or cluster dependency was involved.
- The application ran directly on Ubuntu using Nginx and Flask.
- Recovery did not require any Kubernetes action.

### Result

**Ruled out.**

Kubernetes was not part of this application architecture.

---

## Hypothesis 11: An Administrative Action Stopped Nginx

### Why I Considered It

The Nginx journal showed an orderly shutdown rather than a crash. That suggested that a person or automated process may have issued a service-control command.

### What Supported It

- Authentication logs showed that `webadmin` logged in through SSH.
- The connection came from `192.168.56.111`.
- A failed sudo authentication event occurred.
- Sudo records showed the following command:

`/usr/bin/systemctl stop nginx`

- The command time matched the Nginx shutdown time.
- The `webadmin` session was still active during the investigation.

### What Did Not Fit

- I found no evidence that contradicted the relationship between the SSH session, sudo command, and Nginx shutdown.

### Result

**Confirmed as the direct technical cause.**

An authenticated session with elevated privileges stopped Nginx.

---

## Hypothesis 12: The Server or Application Was Maliciously Compromised

### Why I Considered It

A privileged account had interrupted a user-facing service, so I had to consider the possibility of unauthorized access or deliberate disruption.

### What Supported It

- A privileged account caused an availability impact.
- The SSH source required further review.
- The action was not tied to known maintenance.

### What Did Not Fit

- I found no evidence that application files were modified.
- No malicious backend process was identified.
- There was no evidence of data theft or data alteration.
- I found no persistence mechanism.
- The logs identified the account used, but not the person operating it.
- The technical records could not establish whether the action was accidental or intentional.

### Result

**Not proven.**

The event was security-related because privileged account activity caused the outage. However, the available evidence did not prove malicious intent or a compromise of the Flask backend.

---

## Working Conclusion

The application became unavailable because Nginx was stopped.

The evidence supported the following sequence:

`webadmin -> SSH session from 192.168.56.111 -> sudo systemctl stop nginx`

Once Nginx stopped, the listener on TCP port 80 disappeared. Users could no longer reach the application even though the Flask backend remained healthy on port 5050.

I classified the event as:

**A security-related availability incident caused by privileged administrative activity.**

---

## Recovery Notes

Before restoring service, I preserved the available authentication, sudo, session, service, port, and HTTP evidence.

The recovery process included:

- Locking the `webadmin` account
- Ending the active session
- Validating the Nginx configuration
- Restarting Nginx
- Confirming that TCP port 80 was listening
- Confirming an HTTP 200 response through Nginx
- Confirming access from Windows
- Rebooting the server
- Confirming both services started after reboot
- Confirming `webadmin` remained locked after reboot

---

## Questions That Remain Open

The collected evidence answered the technical question of how the outage occurred, but it could not answer every identity or intent question.

The following items remain unresolved:

- Was the legitimate account owner using the SSH session?
- Were the credentials shared?
- Were the credentials stolen?
- Was the command entered accidentally or intentionally?
- Was there an approved change that had not been documented?
- Was the Kali source system itself compromised?
- Do other accounts have unnecessary sudo privileges?

Additional identity-provider, endpoint, network, change-management, and interview evidence would be needed to answer those questions.

---

## Improvements Identified During the Investigation

This incident highlighted several improvements that would reduce detection and recovery time:

- External HTTP health monitoring
- Alerts when Nginx becomes inactive
- Alerts for privileged service-control commands
- Centralized authentication and sudo logs
- Individual administrator accounts
- Multifactor authentication
- More restrictive sudo permissions
- Formal change control
- Administrative session recording
- Reverse-proxy redundancy

---

## Investigation Habit to Carry Forward

For each new possibility, I should record the following information while the investigation is still active.

### Hypothesis

What may be happening?

### Evidence For

Which observations support the possibility?

### Evidence Against

Which observations contradict it?

### Next Test

Which command, log, or measurement would provide the clearest answer?

### Status

- New
- Investigating
- Supported
- Ruled out
- Confirmed
- Unable to determine

### Reasoning Update

How did the latest evidence change the direction of the investigation?
