# CyberOps Defense Group Professional Development Program

## Overview

This repository documents my work throughout the CyberOps Defense Group Professional Development Program.

It is designed to reflect the investigation, troubleshooting, documentation, and review practices used by a professional security engineering team.

Each weekly ticket contains technical work, supporting evidence, lessons learned, and documentation demonstrating continued engineering growth.

## Program Objectives

This program develops practical skills in:

- Security operations
- Incident investigation
- Detection engineering
- Linux administration
- Cloud and container security
- Technical troubleshooting
- Evidence preservation
- Engineering documentation
- Professional communication
- Continuous improvement

## Technologies and Tools Used

The following technologies and tools have been used in the CyberOps Defense Group Professional Development Program so far.

### Operating Systems

- Windows 11 host system
- Ubuntu Linux SSH target
- Kali Linux security-testing system

### Security Monitoring and Investigation

- Wazuh manager
- Wazuh dashboard
- Wazuh Linux agent
- Linux SSH authentication logs
- systemd journal and `journalctl`
- `last` successful-login history
- `lastb` failed-login history

### Remote Access and Authentication

- OpenSSH
- SSH password authentication
- Windows OpenSSH client
- `scp`
- `sshpass`

### Linux Administration and Containment

- `systemctl`
- Linux user and account-management commands
- `passwd`
- nftables
- Cron
- Bash

### Detection Engineering

- Custom Bash SSH brute-force detector
- Wazuh rule 5551
- Wazuh rule 40112
- MITRE ATT&CK mappings
- Threshold-based authentication-failure detection

### Evidence Collection and Integrity

- SHA-256
- `sha256sum`
- PowerShell `Get-FileHash`
- Evidence inventories
- Incident timelines
- Log preservation
- Screenshot collection

### Documentation and Reporting

- Markdown
- CSV
- PDF
- Microsoft Word
- SVG architecture diagrams
- PowerShell here-strings

### Version Control and Portfolio Management

- Git
- GitHub
- PowerShell
- `.gitignore`

This section will be expanded only when additional tools are used in future program tickets.

## Repository Structure

    cyberops-defense-group-professional-development-program/
    |
    |-- README.md
    |
    |-- Week-01-Ticket-001/
    |   |-- README.md
    |   |-- Incident_Report.pdf
    |   |-- engineering_log.md
    |   |-- lessons_learned.md
    |   |-- screenshots/
    |   |-- configs/
    |   |-- evidence/
    |   `-- diagrams/
    |
    |-- Week-02-Ticket-002/
    |-- Week-03-Ticket-003/
    `-- ...

## Weekly Ticket Requirements

Each completed ticket should include:

- Incident report
- Executive summary
- Technical timeline
- Evidence collected
- Root cause analysis
- Recommendations
- Supporting screenshots
- Relevant logs
- Commands executed
- Configuration files
- Diagrams when applicable
- Engineering log
- Lessons learned
- Reproduction documentation

## Engineering Log

Each work session records:

- Date
- Time spent
- What was attempted
- What worked
- What failed
- Next step

The engineering log demonstrates the investigation and troubleshooting process, not only the final result.

## Engineering Reviews

Completed tickets are reviewed across the following areas:

- Investigation Process
- Troubleshooting Methodology
- Technical Accuracy
- Documentation Quality
- Communication
- Engineering Judgment
- Professionalism

Reviews identify both strengths and opportunities for continued growth.

The objective is continuous improvement, not perfection.

## Week 01 — Ticket 001

### SSH Authentication Investigation

Ticket 001 investigated repeated SSH authentication failures followed by a successful login to an Ubuntu server.

The investigation included:

- SSH log analysis
- Source-IP identification
- Successful-login validation
- Post-login activity confirmation
- Wazuh detection review
- Account containment
- Temporary network containment
- Custom SSH brute-force detection
- Evidence hashing
- Reproduction documentation
- Weekly ticket closure documentation

The completed ticket is located in:

    Week-01-Ticket-001/

## Evidence and Security Notice

All testing documented in this repository was performed in an isolated and authorized lab environment.

Credentials, IP addresses, hostnames, accounts, and artifacts shown in this repository are associated with controlled lab systems.

The techniques documented here must only be used on systems where explicit authorization has been granted.

## Professional Portfolio Purpose

This repository demonstrates my ability to:

- Investigate security events
- Correlate evidence across multiple systems
- Troubleshoot technical failures
- Develop and validate detections
- Apply containment controls
- Preserve evidence integrity
- Produce reproducible documentation
- Communicate technical conclusions
- Learn from mistakes
- Improve future engineering performance

## Current Progress

| Week | Ticket | Topic | Status |
|---|---|---|---|
| Week 01 | Ticket 001 | SSH Authentication Investigation | Complete |
| Week 02 | Ticket 002 | To be added | Pending |
| Week 03 | Ticket 003 | To be added | Pending |

## Repository Name

    cyberops-defense-group-professional-development-program
