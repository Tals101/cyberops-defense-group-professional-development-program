# Ticket 002: Production Web Application Outage

## Project Summary

This project documents a structured investigation of a production-style internal web application outage. The original ticket intentionally contained limited information, requiring the investigation to begin without assuming that the web server, application, network, DNS, firewall, Docker, or Kubernetes was responsible.

The project demonstrates how an engineer can validate user symptoms, isolate application layers, test competing hypotheses, preserve technical evidence, restore service, and document the investigation for both technical and business audiences.

## Environment

### Ubuntu Application Server

- Hostname: `ubuntu-soc-lab`
- Operating system: Ubuntu 24.04 LTS
- IP address: `192.168.56.121`
- Web listener: Nginx on TCP port 80
- Backend application: Flask on `127.0.0.1:5050`
- Backend service: `company-web.service`
- Remote administration: SSH on TCP port 22

### Windows Workstation

- Used to reproduce the reported user experience
- Used for remote TCP connectivity testing
- Used for browser-based recovery validation
- Used to collect, organize, and publish project artifacts

### Kali Linux System

- IP address: `192.168.56.111`
- Used as the simulated remote administrative source during the investigation

### Application Request Path

`Windows workstation → Nginx TCP 80 → Flask backend TCP 5050`

## Scenario

Users reported that the internal company web application had become unavailable after working normally earlier in the day.

The ticket did not specify:

- What component had failed
- Whether the server was reachable
- Whether the backend application was healthy
- Whether a recent configuration change had occurred
- Whether the event was operational or security-related

The investigation tested each layer independently and documented evidence both for and against multiple possible causes.

The investigation included:

1. Establishing a healthy application baseline
2. Reproducing and validating the outage
3. Testing host and network availability
4. Inspecting listening ports and service status
5. Testing the backend directly
6. Reviewing Nginx and systemd logs
7. Reviewing SSH, authentication, and sudo activity
8. Correlating account, command, and service timestamps
9. Preserving evidence before recovery
10. Containing the involved account
11. Restoring and validating application access
12. Testing service recovery after reboot

Detailed conclusions and supporting analysis are provided in `reports/Incident_Report.pdf`.

## Skills Demonstrated

- Incident investigation
- Linux system administration
- Service-layer troubleshooting
- Network connectivity testing
- Log analysis and event correlation
- Authentication and sudo auditing
- Root cause analysis
- Hypothesis-driven troubleshooting
- Evidence preservation
- Incident classification
- Account containment
- Service recovery and validation
- Technical documentation
- Business-impact analysis
- Git-based engineering workflow

## Technologies Used

- Ubuntu Linux
- Windows PowerShell
- Kali Linux
- Nginx
- Python
- Flask
- systemd
- SSH and SCP
- Git and GitHub
- `systemctl`
- `journalctl`
- `curl`
- `ss`
- `ping`
- `last`
- `lastb`
- `who`
- `w`
- `grep`
- `sha256sum`
- Mermaid diagrams

## Deliverables

### Incident Report

- `reports/Incident_Report.pdf`
- Executive summary
- Environment description
- Investigation methodology
- Timeline
- Technical findings
- Evidence review
- Root cause analysis
- Incident classification
- Business impact
- Recovery actions
- Remaining risks
- Recommendations

### Interview Preparation Guide

- `reports/Interview_Preparation.pdf`
- `reports/Interview_Preparation.md`
- Structured interview questions and answers
- Investigation methodology explanations
- Root-cause confirmation discussion
- Containment and recovery reasoning
- Monitoring and production-improvement recommendations
### Engineering Notebook

- `engineering-notebook.md`
- Initial thoughts
- Twelve investigated hypotheses
- Evidence for and against each hypothesis
- Planned tests
- Status updates
- Reasoning changes
- Open questions
- Reusable investigation template

### Evidence

The `evidence` directory contains:

- Baseline service and HTTP records
- Outage-state service records
- Listening-port output
- Authentication and sudo events
- Nginx service journal
- Login and active-session evidence
- Account-containment evidence
- Recovery and external validation results
- Nginx and systemd configuration files
- Evidence integrity hashes
- Technical timeline

### Scripts

The `scripts` directory contains the documented Flask backend used in the investigation.

### Diagrams

The `diagrams` directory contains Mermaid source files for:

- Application architecture
- Investigation workflow
- Incident timeline

### Lessons Learned

The separate `lessons-learned.md` file addresses:

- What was surprising
- What should be investigated sooner next time
- What engineering habit improved
- What should be automated
- What remains unanswered

## Evidence Organization

- `evidence/screenshots/` — browser and terminal screenshots
- `evidence/logs/` — exported logs, terminal output, monitoring results, and validation records
- `evidence/configs/` — Nginx and systemd configuration files
- `evidence/timeline/` — baseline time records and reconstructed technical timeline

## Key Lessons Learned

### Test Every Layer Independently

A browser outage does not identify the failed component. Host availability, network access, reverse proxy status, and backend health must be tested separately.

### Follow Evidence Instead of Assumptions

The investigation considered networking, DNS, firewall rules, backend failure, configuration errors, Docker, Kubernetes, software failure, and privileged activity. Each possibility was accepted or rejected using direct evidence.

### Correlate Multiple Sources

The strongest conclusions came from correlating service status, listening ports, HTTP results, authentication logs, sudo records, session data, and systemd timestamps.

### Preserve Evidence Before Recovery

Authentication records, active-session details, network connections, and service logs were collected before performing unnecessary system changes.

### Validate from the User Perspective

A service showing `active` does not guarantee that the application works. Recovery was confirmed using HTTP responses, external TCP checks, browser access, and post-reboot testing.

### Separate Technical Facts from Human Intent

Logs can identify the account, source address, command, and timestamp. They may not prove who controlled the account or whether the action was accidental or intentional.

## Repository Structure

    ticket-002-production-web-application-outage/
    ├── README.md
    ├── Incident_Report.pdf
    ├── engineering-notebook.md
    ├── lessons-learned.md
    ├── evidence/
    │   ├── screenshots/
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

## Commit History Note

This GitHub package was assembled from preserved investigation evidence using multiple meaningful commits rather than one final bulk upload.

The commits represent logical project stages, including:

- Project initialization
- Baseline capture
- Outage-state documentation
- Authentication and service-event correlation
- Containment and recovery
- Script documentation
- Configuration collection
- Engineering notebook and timeline
- Diagram creation
- Final documentation

These commits were created during repository packaging and were not backdated to imply that they occurred during the original live investigation.


