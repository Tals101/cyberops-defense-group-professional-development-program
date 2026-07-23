# CyberOps Defense Group Professional Development Program

## About This Repository

This repository documents my work in the CyberOps Defense Group Professional Development Program.

Each week, I complete a technical ticket based on a realistic cybersecurity or systems-engineering scenario. I use this repository to show not only the final result, but also how I approached the problem, what evidence I reviewed, which challenges I encountered, and what I learned.

My goal is to document each ticket clearly enough that another engineer can understand the project without needing additional explanation.

All investigations and security tests documented here were completed in isolated and authorized lab environments.

## My Goals

Through this program, I am working to improve my ability to:

- Investigate security incidents methodically
- Analyze logs and connect related events
- Build accurate technical timelines
- Validate alerts using multiple evidence sources
- Apply containment controls safely
- Create practical security detections
- Preserve and verify evidence
- Troubleshoot technical issues independently
- Write clear technical documentation
- Use Git and GitHub as part of a professional workflow
- Explain findings to technical and nontechnical audiences

## Technologies and Tools Used

This section includes only the technologies and tools I have used in the program so far. I will update it as I complete additional tickets.

### Operating Systems

- Windows 11
- Ubuntu Linux
- Kali Linux

### Security Monitoring and Investigation

- Wazuh Manager
- Wazuh Dashboard
- Wazuh Linux Agent
- Linux SSH authentication logs
- `journalctl`
- `last`
- `lastb`

### Remote Access and Authentication

- OpenSSH
- Windows OpenSSH client
- `scp`
- `sshpass`

### Linux Administration and Containment

- Bash
- Cron
- `systemctl`
- `passwd`
- Linux user-management commands
- nftables

### Detection Engineering

- Custom Bash detection scripts
- Threshold-based SSH failure detection
- Wazuh rule 5551
- Wazuh rule 40112
- MITRE ATT&CK mappings

### Evidence and Documentation

- SHA-256 hashing
- `sha256sum`
- PowerShell `Get-FileHash`
- Evidence inventories
- Technical timelines
- Markdown
- CSV
- PDF
- Microsoft Word
- SVG diagrams
- Screenshots

### Version Control

- Git
- GitHub
- PowerShell
- `.gitignore`
- `.gitattributes`

## Repository Organization

Each weekly folder is treated as its own technical project.

    cyberops-defense-group-professional-development-program/
    |
    |-- README.md
    |
    |-- Week-01-Ticket-001/
    |   |-- README.md
    |   |-- Incident_Report.pdf
    |   |-- engineering_log.md
    |   |-- lessons_learned.md
    |   |-- configs/
    |   |-- diagrams/
    |   |-- evidence/
    |   `-- screenshots/
    |
    |-- Week-02-Ticket-002/
    |-- Week-03-Ticket-003/
    `-- ...

Each ticket folder may include:

- A project overview
- The objective and investigation scope
- Environment and tool details
- Supporting evidence
- Configuration files or scripts
- Screenshots
- Architecture or workflow diagrams
- An engineering log
- Lessons learned
- A final report

## Completed Tickets

| Week | Ticket | Project | Status |
|---|---|---|---|
| Week 01 | Ticket 001 | SSH Authentication Investigation | Complete |

This table will be updated as I complete new tickets.

## Ticket 001 — SSH Authentication Investigation

For Ticket 001, I investigated repeated SSH password failures against an Ubuntu server.

The failed attempts were followed by a successful login from the same source system. My responsibility was to determine what happened, identify the account and source IP involved, verify whether the login led to activity on the server, preserve the supporting evidence, and apply appropriate containment.

My work included:

- Reviewing native Linux authentication records
- Identifying the source system and targeted account
- Confirming the successful SSH session
- Correlating failed and successful login activity
- Reviewing Wazuh alerts
- Verifying post-login activity
- Locking the affected account
- Testing a temporary network block
- Building a custom SSH brute-force detector
- Scheduling the detector with cron
- Creating an evidence inventory
- Generating SHA-256 hashes
- Preparing a formal incident report

The completed project is located in:

    Week-01-Ticket-001/

## Skills Developed

Ticket 001 gave me practical experience with:

- SSH incident investigation
- Linux log analysis
- Event correlation
- Timeline development
- Wazuh alert validation
- Evidence preservation
- Evidence hashing
- Linux account containment
- Network containment
- Bash scripting
- Cron scheduling
- Detection engineering
- Technical troubleshooting
- Incident reporting
- Git commit organization
- Portfolio documentation

## How I Document My Work

For each ticket, I try to answer five important questions:

1. What problem was I solving?
2. Why did I choose this approach?
3. What other approaches did I consider?
4. What evidence supports my conclusion?
5. What would I improve if I repeated the work?

This approach makes the repository more than a collection of finished files. It also shows how I worked through the problem and how my decisions were supported.

## Git Practices

I use focused commits so the repository history reflects the progress of the investigation.

Examples from Ticket 001 include:

- `Initialize professional development portfolio`
- `Document Ticket 001 investigation process`
- `Collect SSH authentication evidence`
- `Add Wazuh detection evidence and screenshots`
- `Add SSH containment and custom detection controls`
- `Add Ticket 001 incident report and architecture diagram`
- `Add validated evidence inventory and SHA256 manifest`

This makes it easier to review how the project developed instead of seeing only one large final commit.

## Protecting Sensitive Information

Before committing files, I review the repository for:

- Passwords
- API keys
- Authentication tokens
- AWS credentials
- SSH private keys
- Personal information
- Production logs
- Webhook URLs
- Secrets of any kind

When a credential is needed in an example, I use a placeholder such as:

    YOUR_API_KEY_HERE
    YOUR_PASSWORD_HERE
    YOUR_SSH_KEY_PATH

Raw evidence is included only when it comes from an authorized lab environment and has been reviewed for sensitive information.

## Professional Standard

I write each project with the assumption that it may be reviewed by another engineer, a technical manager, a recruiter, or a hiring manager.

My goal is to keep the work:

- Clear
- Accurate
- Organized
- Reproducible
- Easy to navigate
- Supported by evidence
- Honest about challenges and limitations

## Continuing Progress

I will update this README as I complete new tickets, use additional technologies, and develop new technical skills.

The purpose of this repository is to show steady improvement over time—not just completed assignments, but the development of my investigation, engineering, documentation, and problem-solving abilities.
