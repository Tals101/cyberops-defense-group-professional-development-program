# CyberOps Defense Group Professional Development Program (AI-generated simulation; fictional company)

> **AI-generated simulation, fictional company.** CyberOps Defense Group is not a real organization. The program, its tickets, people and business data are an AI-generated training simulation.

Twelve technical tickets I completed as the assigned engineer, covering incident response, threat hunting, vulnerability management, detection engineering, security automation, DevSecOps and Kubernetes security. All work was done in isolated lab environments with simulated or synthetic systems and data. Decisions that would need organizational authority, such as production deployment or incident closure, are recorded as recommendations, and failed tests and open findings are kept in the record.

## Results

| # | Project | Technical focus | Result |
|---|---|---|---|
| 001 | [SSH Authentication Investigation](ticket-001-ssh-authentication-investigation/) | Linux auth logs, Wazuh alerts, account and network containment, Bash detector | Confirmed failed SSH logins followed by a successful login and post-login activity |
| 002 | [Production Web Application Outage](ticket-002-production-web-application-outage/) | Layered outage troubleshooting across Nginx, Flask and systemd; sudo and session correlation; recovery | Traced the outage to a command run from a specific account and session; service restored and verified from the user side |
| 003 | [Suspicious Account Activity Detection Engineering](ticket-003-detection-engineering/) | Python SSH detector, threshold tuning, known-source and success context | Version 2 removed the Version 1 false positive and passed every other test scenario |
| 004 | [Hypothesis-Driven Linux Threat Hunt](ticket-004-threat-hunt/) | Cron, root crontab and systemd persistence; sudo and SSH session correlation | Closed as benign with medium confidence |
| 005 | [Critical Vulnerability Risk Assessment](ticket-005-critical-vulnerability/) | CVE-2021-42013 in Apache 2.4.50, options analysis, controlled upgrade to 2.4.68 | Lab remediation validated; residual risk Low-Medium |
| 006 | [Evolving Incident](ticket-006-evolving-incident/) | Outbound HTTPS investigation, Linux audit logs, packet and TLS certificate analysis, containment and business continuity | Confirmed unauthorized transmission of synthetic Finance data; malware status and root cause not determined |
| 007 | [Three Fires, One Engineer](ticket-007-three-fires/) | Triage and prioritization across three concurrent alerts, delegation, stakeholder updates | Three separate dispositions, one confirmed incident in the scenario |
| 008 | [The Alert Nobody Reads](ticket-008-the-alert-nobody-reads/) | Detection tuning with synthetic data and ground truth, Purple Team and adversarial testing | Alerts reduced from 597 to 15 (V1) and 7 analyst cases (V2); three adversarial variations still missed |
| 009 | [The Automation Did Exactly What You Told It](ticket-009-automation-did-exactly-what-you-told-it/) | Identity remediation automation, authority model, failure injection, adversarial testing | Lab validation complete; production NO-GO for unattended destructive remediation |
| 010 | [The Patch That Passed Every Check](ticket-010-the-patch-that-passed-every-check/) | Release gates, Pod Security Admission, ValidatingAdmissionPolicy, Trivy, Syft, cosign, rollback rehearsal | 12 of 13 adversarial scenarios verified; production readiness not established |
| 011 | [Cross-System Incident Investigation](ticket-011-cross-system-incident-investigation/) | AWS, Kubernetes and Linux correlation engine; Falco rule development | Cross-system causation not established; acceptance and closure pending |
| 012 | [Final Capstone](ticket-012-final-capstone/) | Kubernetes incident lab, correlation detectors, containment and recovery testing | Investigation complete; remediation incomplete; production NO-GO |

Where a result says NO-GO or "not established", that is the recommendation the evidence supports, not unfinished work.

## Start Here

- [Ticket 010](ticket-010-the-patch-that-passed-every-check/): release gates, admission control and supply-chain checks (Trivy, Syft, cosign) ([diagrams](ticket-010-the-patch-that-passed-every-check/DIAGRAMS.md))
- [Ticket 012](ticket-012-final-capstone/): Kubernetes incident lab with two correlation detectors and 51 automated tests ([diagrams](ticket-012-final-capstone/DIAGRAMS.md))
- [Ticket 009](ticket-009-automation-did-exactly-what-you-told-it/): identity remediation automation with authority boundaries and failure injection
- [Ticket 011](ticket-011-cross-system-incident-investigation/): AWS, Kubernetes and Linux event correlation with custom Falco rules ([diagrams](ticket-011-cross-system-incident-investigation/DIAGRAMS.md))

Each ticket folder has its own README with the scenario, evidence, report and lessons learned. Some tests in Tickets 009 and 012 rewrite files in their evidence folders, so run them in a disposable copy; see [Ticket 009's warnings](ticket-009-automation-did-exactly-what-you-told-it/README.md#before-rerunning-tests-evidence-and-platform-warnings) and [Ticket 012's testing notes](ticket-012-final-capstone/TESTING-NOTES.md).

## Tools

Wazuh, Falco, Linux audit logs and packet captures; Docker, Minikube, kubectl, Helm, Pod Security Admission, ValidatingAdmissionPolicy, RBAC and NetworkPolicy; Trivy, Syft and cosign; Python, Bash and PowerShell; MITRE ATT&CK.

## Evidence Integrity and Privacy

- Evidence is kept as collected, with SHA-256 manifests so files can be checked. Any change after collection is documented.
- On November 22, 2026, my local Windows account and computer names were redacted from evidence files, screenshots and one PDF. The affected Ticket 010 manifests were updated, with a dated addendum in [`final-integrity-audit.md`](ticket-010-the-patch-that-passed-every-check/closure/final-integrity-audit.md).
- Three Ticket 002 evidence files whose line endings Git had changed were restored to their original bytes; see [`evidence-integrity-verification.md`](ticket-002-production-web-application-outage/evidence-integrity-verification.md).
- The repository and its full Git history were scanned for exposed credentials, and none were found.
