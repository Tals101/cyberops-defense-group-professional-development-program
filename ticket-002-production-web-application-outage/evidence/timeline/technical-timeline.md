# Production Web Application Outage - Technical Timeline

## Incident Details

- Affected system: `ubuntu-soc-lab`
- Server IP address: `192.168.56.121`
- Source system under review: Kali Linux at `192.168.56.111`
- Affected service: Nginx on TCP port 80
- Backend service: Internal Company Web Application on `127.0.0.1:5050`
- Classification: Security-related availability incident
- Time zone: UTC

## Timeline

### July 27, 2026

- **19:30:36** - Nginx was installed and started successfully.
  Evidence: `evidence/02-baseline-nginx-status.txt`

- **19:41:34** - I recorded the healthy baseline time.
  Evidence: `evidence/01-baseline-time.txt`

- **20:16:01** - Nginx was reloaded with the reverse-proxy configuration that forwarded requests to port 5050.
  Evidence: `evidence/06-healthy-services.txt`

- **20:24:23** - The Flask backend started under `company-web.service`.
  Evidence: `evidence/06-healthy-services.txt`

- **20:26:31** - A successful HTTP request confirmed that Nginx and the Flask backend were both working.
  Evidence: `evidence/05-baseline-http-response.txt`

- **20:37:32** - The `webadmin` account logged in through SSH from `192.168.56.111`.
  Evidence: `evidence/13-focused-incident-auth-events.txt`

- **20:38:56** - A sudo authentication attempt failed during the `webadmin` session.
  Evidence: `evidence/13-focused-incident-auth-events.txt`

- **20:39:33** - The `webadmin` account used sudo to run:

  `/usr/bin/systemctl stop nginx`

  Evidence: `evidence/13-focused-incident-auth-events.txt`

- **20:39:33** - Systemd began stopping Nginx.
  Evidence: `evidence/14-nginx-incident-journal.txt`

- **20:39:34** - Nginx completed a normal shutdown and became inactive.
  Evidence: `evidence/08-outage-nginx-status.txt`
  Evidence: `evidence/14-nginx-incident-journal.txt`

- **Approximately 20:40** - Windows testing showed that the server still responded to ping, but TCP port 80 could not be reached.

- **20:42:05** - I formally recorded the start of the outage investigation.
  Evidence: `evidence/07-outage-investigation-time.txt`

- **20:43:26** - A direct request to port 5050 returned HTTP 200, confirming that the Flask backend was still working.
  Evidence: `evidence/09-backend-still-operational.txt`

- **Approximately 20:44** - Listening-port output showed that port 80 was missing while ports 22 and 5050 were still available.
  Evidence: `evidence/10-outage-listening-ports.txt`

- **Approximately 20:45** - I confirmed that `webadmin` still had an active session from `192.168.56.111`.
  Evidence: `evidence/11-logged-in-users.txt`
  Evidence: `evidence/15-webadmin-login-history.txt`

- **During containment** - I preserved details of the active `webadmin` shell and SSH connection.
  Evidence: `evidence/16-webadmin-active-session.txt`
  Evidence: `evidence/17-webadmin-active-network-connection.txt`

- **During containment** - I locked the `webadmin` account to prevent additional password-based logins.
  Evidence: `evidence/18-webadmin-account-locked.txt`

- **During containment** - I ended the active `webadmin` session and confirmed that the connection from `192.168.56.111` had closed.

- **During recovery preparation** - The Nginx configuration passed syntax validation.

### July 28, 2026

- **19:26:22** - The enabled `company-web.service` started automatically after the Ubuntu server restarted.
  Evidence: `evidence/21-recovered-services.txt`

- **19:26:24** - Nginx started automatically after the restart.
  Evidence: `evidence/21-recovered-services.txt`

- **19:31:43** - The restored application returned HTTP 200 through Nginx.
  Evidence: `evidence/19-restored-http-response.txt`

- **Approximately 19:35** - Windows testing confirmed that TCP port 80 was reachable again.

- **After recovery** - The `webadmin` account remained locked.
  Evidence: `evidence/20-webadmin-locked-after-reboot.txt`

- **19:38** - SHA-256 hashes were generated for the evidence files.
  Evidence: `evidence-sha256.txt`

## Timeline Analysis

The Ubuntu server and Flask backend stayed operational throughout the outage. The user-facing application became unavailable because Nginx had been stopped.

The `webadmin` account logged in from the Kali Linux system at `192.168.56.111`. About two minutes later, the account used sudo privileges to stop Nginx. The systemd journal recorded the service shutdown at the same time as the privileged command.

While Nginx was down, the Flask backend continued returning HTTP 200 on port 5050. Port 80, however, was no longer listening. This narrowed the failure to the Nginx layer rather than the server, network, or backend application.

Because a remote administrative session used elevated privileges to interrupt the user-facing service, I classified the event as a security-related incident affecting availability.

I contained the immediate risk by locking the `webadmin` account and ending its active SSH session. After recovery, Nginx and the Flask backend started automatically following a reboot. Successful HTTP, browser, and Windows connectivity checks confirmed that access had been restored.
