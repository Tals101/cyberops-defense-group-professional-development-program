# Internal Web Application Outage – Technical Timeline

## Incident Information

- Affected system: ubuntu-soc-lab
- Server IP address: 192.168.56.121
- Suspected source system: Kali Linux at 192.168.56.111
- Affected service: Nginx web server on TCP port 80
- Backend service: Internal Company Web Application on 127.0.0.1:5050
- Incident classification: Security-related availability incident
- Time zone: UTC

## Technical Timeline

### July 27, 2026

- 19:30:36 — Nginx was installed and started successfully.
  Evidence: evidence/02-baseline-nginx-status.txt

- 19:41:34 — The healthy baseline time was recorded.
  Evidence: evidence/01-baseline-time.txt

- 20:16:01 — Nginx was reloaded with the reverse-proxy configuration forwarding requests to port 5050.
  Evidence: evidence/06-healthy-services.txt

- 20:24:23 — The internal backend application started as the company-web systemd service.
  Evidence: evidence/06-healthy-services.txt

- 20:26:31 — A successful HTTP request confirmed that Nginx and the backend application were healthy.
  Evidence: evidence/05-baseline-http-response.txt

- 20:37:32 — The webadmin account logged in through SSH from 192.168.56.111.
  Evidence: evidence/13-focused-incident-auth-events.txt

- 20:38:56 — A failed sudo authentication attempt occurred during the webadmin session.
  Evidence: evidence/13-focused-incident-auth-events.txt

- 20:39:33 — The webadmin account used sudo to run:
  /usr/bin/systemctl stop nginx
  Evidence: evidence/13-focused-incident-auth-events.txt

- 20:39:33 — Systemd began stopping the Nginx service.
  Evidence: evidence/14-nginx-incident-journal.txt

- 20:39:34 — Nginx was successfully deactivated and stopped.
  Evidence: evidence/08-outage-nginx-status.txt
  Evidence: evidence/14-nginx-incident-journal.txt

- Approximately 20:40 — Windows testing showed that the server still responded to ping, but TCP port 80 was unavailable.

- 20:42:05 — The outage investigation time was formally recorded.
  Evidence: evidence/07-outage-investigation-time.txt

- 20:43:26 — Direct testing of port 5050 returned HTTP 200, proving that the backend remained operational.
  Evidence: evidence/09-backend-still-operational.txt

- Approximately 20:44 — Listening-port evidence confirmed that port 80 was absent while ports 22 and 5050 remained available.
  Evidence: evidence/10-outage-listening-ports.txt

- Approximately 20:45 — The webadmin account was confirmed actively logged in from 192.168.56.111.
  Evidence: evidence/11-logged-in-users.txt
  Evidence: evidence/15-webadmin-login-history.txt

- During containment — The active webadmin shell and SSH network connection were preserved.
  Evidence: evidence/16-webadmin-active-session.txt
  Evidence: evidence/17-webadmin-active-network-connection.txt

- During containment — The webadmin account was locked to prevent additional password-based logins.
  Evidence: evidence/18-webadmin-account-locked.txt

- During containment — The active webadmin session was terminated and the connection from 192.168.56.111 was confirmed closed.

- During recovery preparation — The Nginx configuration passed syntax validation.

### July 28, 2026

- 19:26:22 — The enabled company-web service started automatically after the Ubuntu restart.
  Evidence: evidence/21-recovered-services.txt

- 19:26:24 — Nginx started automatically after the Ubuntu restart.
  Evidence: evidence/21-recovered-services.txt

- 19:31:43 — The restored application returned HTTP 200 through Nginx.
  Evidence: evidence/19-restored-http-response.txt

- Approximately 19:35 — Windows testing confirmed that TCP port 80 was reachable again.

- After recovery — The webadmin account remained locked.
  Evidence: evidence/20-webadmin-locked-after-reboot.txt

- 19:38 — SHA-256 hashes were generated for the evidence files.
  Evidence: evidence-sha256.txt

## Timeline Analysis

The evidence shows that the Ubuntu server and backend application did not fail. The outage occurred because Nginx, the user-facing reverse-proxy service, was deliberately stopped.

The webadmin account logged in from the Kali Linux system at 192.168.56.111. Approximately two minutes later, the account used sudo privileges to stop Nginx. Systemd recorded the service shutdown at the same time.

During the outage, the backend application continued to return HTTP 200 on port 5050, while port 80 was no longer listening. This proves that the failure was isolated to the Nginx web-service layer.

Because an administrative account remotely executed the command that caused the outage, the event is classified as a security incident affecting system availability rather than an ordinary operational failure.

Containment included locking the webadmin account and terminating its active SSH session. Nginx and the backend service started automatically after the server restart. Successful HTTP and Windows connectivity tests confirmed service restoration.
