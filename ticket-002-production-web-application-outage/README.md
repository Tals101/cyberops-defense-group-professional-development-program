# Ticket 002: Production Web Application Outage

## Project Summary

This project follows the investigation of an internal web application outage in a production-style lab environment. The initial ticket provided only the user-facing symptom: the application had been working earlier and was no longer accessible.

Because the cause was unknown, the investigation did not begin with assumptions about the server, network, firewall, reverse proxy, backend application, Docker, or Kubernetes. Each part of the request path was tested separately until the failed layer could be isolated.

The project shows how I approached an outage methodically, preserved evidence, compared several possible explanations, contained the identified risk, restored the service, and confirmed that the application remained available after a reboot.

## Environment

### Ubuntu Application Server

- Hostname: `ubuntu-soc-lab`
- Operating system: Ubuntu 24.04 LTS
- IP address: `192.168.56.121`
- User-facing web service: Nginx on TCP port 80
- Backend application: Flask on `127.0.0.1:5050`
- Backend systemd unit: `company-web.service`
- Remote administration: SSH on TCP port 22

### Windows Workstation

The Windows system represented the user side of the environment. It was used to:

- Reproduce the reported outage
- Test remote access to TCP port 80
- Open the restored application in a browser
- Organize and publish the completed project

### Kali Linux System

- IP address: `192.168.56.111`
- Used as the simulated remote administrative source in the lab

### Normal Request Path

`Windows workstation -> Nginx on port 80 -> Flask backend on port 5050`

## Scenario

Users reported that the internal application had become unavailable even though it had worked earlier in the day. No scheduled maintenance or approved change was included in the original ticket.

At the start of the investigation, several important questions were still unanswered:

- Was the Ubuntu server online?
- Was the network path working?
- Was TCP port 80 reachable?
- Was Nginx running?
- Was the Flask backend still healthy?
- Had a configuration change caused the outage?
- Was the event operational, administrative, or security-related?

The investigation was designed to answer those questions using system state, service records, authentication logs, network checks, and HTTP testing.

## Investigation Approach

The work was completed in a deliberate sequence:

1. Recorded a known-good baseline.
2. Reproduced the outage from the user side.
3. Confirmed that the Ubuntu host was still reachable.
4. Checked listening ports and service states.
5. Tested the Flask backend directly on port 5050.
6. Reviewed the Nginx systemd journal.
7. Examined SSH, sudo, and authentication records.
8. Compared account activity with the service shutdown time.
9. Preserved relevant evidence before recovery.
10. Contained the account involved in the event.
11. Validated the Nginx configuration.
12. Restored the user-facing service.
13. Confirmed access from Windows.
14. Rebooted the server and verified that recovery persisted.

The detailed findings and final analysis are available in `reports/Incident_Report.pdf`.

## Skills Demonstrated

- Linux outage investigation
- Incident response fundamentals
- Hypothesis-driven troubleshooting
- Service-layer isolation
- Network connectivity testing
- Nginx and Flask troubleshooting
- systemd service analysis
- Authentication and sudo-log review
- Timeline reconstruction
- Root-cause analysis
- Evidence preservation
- Account containment
- Recovery validation
- Technical report writing
- Git and GitHub project organization

## Technologies and Commands Used

### Platforms and Services

- Windows 11
- Ubuntu Linux
- Kali Linux
- Nginx
- Python
- Flask
- systemd
- SSH
- Git
- GitHub

### Investigation Commands

- `systemctl`
- `journalctl`
- `curl`
- `ss`
- `ping`
- `who`
- `w`
- `last`
- `lastb`
- `grep`
- `sha256sum`
- `Test-NetConnection`

## Deliverables

### Incident Report

`reports/Incident_Report.pdf`

The report includes:

- Executive summary
- Environment overview
- Investigation method
- Technical timeline
- Findings from each application layer
- Evidence analysis
- Root-cause determination
- Incident classification
- Business impact
- Containment and recovery actions
- Remaining risks
- Recommendations
- Final conclusion

### Interview Preparation Guide

`reports/Interview_Preparation.pdf`

The guide includes practical responses to questions about:

- The first troubleshooting hypothesis
- Why the investigation began with infrastructure checks
- Evidence that changed the direction of the investigation
- How other possible causes were eliminated
- How the technical cause was confirmed
- Why the account was contained before service restoration
- How the recovery was validated
- Monitoring and operational improvements

### Engineering Notebook

`engineering-notebook.md`

The notebook records:

- Initial observations
- Twelve investigated hypotheses
- Evidence supporting each possibility
- Evidence that contradicted each possibility
- Status changes as the investigation progressed
- The working conclusion
- Recovery notes
- Unanswered questions
- Ideas for improving future investigations

### Lessons Learned

`lessons-learned.md`

This document explains:

- What stood out during the investigation
- What should be checked earlier during a similar outage
- Which troubleshooting habits improved
- What parts of the process could be automated
- Which questions could not be answered from the available evidence

### Evidence

The `evidence` folder contains the records used to support the investigation, including:

- Healthy baseline results
- Outage-state service output
- Listening-port checks
- Backend HTTP tests
- Authentication and sudo activity
- Nginx journal entries
- Active-session details
- Account-locking evidence
- Recovery verification
- Reboot verification
- Configuration files
- Timeline files
- Evidence hashes
- Screenshots

### Scripts

The `scripts` folder contains the documented Flask backend application used during the lab.

### Diagrams

The `diagrams` folder contains Mermaid source files for:

- Application architecture
- Investigation workflow
- Incident timeline

## Key Lessons

### Start With the User Symptom, Not a Preferred Theory

An unavailable webpage does not automatically mean the backend application is down. The server, network, reverse proxy, and application should be tested as separate layers.

### Compare Independent Evidence Sources

The clearest explanation came from comparing service state, open ports, HTTP results, systemd records, authentication activity, sudo commands, and active-session information.

### Preserve Evidence Before Changing the System

Logs and session details can disappear after a service restart, logout, or reboot. Relevant information should be collected before recovery work begins whenever possible.

### Confirm Recovery From Outside the Server

A service showing as `active` is not enough. The application must also be tested through the same path used by the people who reported the problem.

### Avoid Claims the Evidence Cannot Support

The available records can show which account was used, where the session originated, which command ran, and when the service stopped. Those records do not automatically prove who controlled the account or whether the action was accidental or intentional.

## Repository Structure

    ticket-002-production-web-application-outage/
    ├── README.md
    ├── engineering-notebook.md
    ├── lessons-learned.md
    ├── reports/
    │   ├── Incident_Report.pdf
    │   └── Interview_Preparation.pdf
    ├── evidence/
    │   ├── screenshots/
    │   │   ├── 01-restored-application-browser.png
    │   │   └── 02-recovered-services.png
    │   ├── logs/
    │   ├── configs/
    │   ├── timeline/
    │   └── evidence-sha256.txt
    ├── scripts/
    │   └── internal_web_app.py
    └── diagrams/
        ├── application-architecture.mmd
        ├── investigation-flow.mmd
        └── incident-timeline.mmd

## Commit History

The project was organized through separate commits for the major stages of the work, including:

- Initial project structure
- Baseline evidence
- Outage-state evidence
- Authentication and service-event correlation
- Containment and recovery
- Application script and service configuration
- Engineering notebook and timeline
- Diagrams
- Final reports
- Screenshots
- Report-folder organization

The commits document how the completed investigation was organized for GitHub and do not claim to represent the exact timing of every action taken during the live lab.
