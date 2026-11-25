# CyberOps Defense Group Professional Development Program

This repository contains my completed work from the CyberOps Defense Group Professional Development Program: twelve technical tickets covering incident response, threat hunting, vulnerability management, detection engineering, security automation, DevSecOps and Kubernetes security.

All investigations and security tests were performed in isolated, authorized laboratory environments. Systems, users, business data and incidents are simulated or synthetic unless a ticket states otherwise. Nothing in this repository describes work on a production system.

## My Role

I completed all twelve tickets as the assigned engineer. For each one I set up or operated the lab environment, collected and preserved the evidence, wrote the scripts, detectors and tests, recorded the technical decisions and their reasons, and wrote the reports, briefs and lessons learned.

Decisions that would need organizational authority, such as production deployment, production containment or formal incident closure, are recorded as recommendations. They are not presented as actions I was authorized to take. Failed tests, wrong first assumptions and unresolved findings are kept in the record rather than removed.

## Skills Demonstrated

- **Incident investigation:** log analysis, event correlation, technical timelines, separating facts from inferences and assumptions
- **Threat hunting:** hypothesis-driven hunts across cron, systemd, sudo and SSH activity, with MITRE ATT&CK mapping
- **Detection engineering:** building, measuring and tuning detections; false-positive and false-negative analysis; Purple Team and adversarial testing
- **Vulnerability and risk management:** CVE research, exposure validation, risk-based decisions, change and rollback planning
- **Security automation:** identity remediation with authority boundaries, approvals, dry-run, rollback, fail-closed handling and failure injection
- **DevSecOps and supply-chain security:** release gates, admission control, SBOMs, vulnerability gating and image signature verification
- **Kubernetes security:** Pod Security Admission, admission policies, RBAC review, ServiceAccount controls, NetworkPolicy testing and Falco runtime detection
- **Evidence handling:** SHA-256 manifests, evidence inventories and documented corrections
- **Communication:** incident reports, executive briefs, decision records and lessons learned

## Tickets

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

## Featured Projects

- **[Ticket 010: DevSecOps release controls](ticket-010-the-patch-that-passed-every-check/).** A Deployment with a mutable image tag and a privileged root container had passed existing checks. I built PowerShell release gates, Kubernetes admission controls and supply-chain checks with Syft, Trivy and cosign. Twelve of thirteen adversarial scenarios are verified; A02 is still under review, and production readiness is not established.
- **[Ticket 012: Final capstone](ticket-012-final-capstone/).** I built a Kubernetes incident lab, two correlation detectors and a command-line tool with 51 automated tests. On 24 labeled synthetic cases, V2 detected all 12 positive cases with 5 false positives. The egress NetworkPolicy was not enforced by Minikube's network plugin, so the recommendation is NO-GO.
- **[Ticket 009: Security automation](ticket-009-automation-did-exactly-what-you-told-it/).** I reproduced an identity-automation failure and built two Python redesigns with authority boundaries, rollback, and integrity and freshness checks. They were tested with 28 safety, failure-injection and adversarial tests, with every failed result kept. The final version remains dry-run only.
- **[Ticket 011: Cross-system investigation](ticket-011-cross-system-incident-investigation/).** I correlated 42 synthetic AWS, Kubernetes and Linux events and found 2 shared IP addresses and 37 cross-system event pairs, without establishing causation. Two custom Falco rules passed their positive and negative controls. Acceptance and closure are pending.

## Laboratory Work, Open Findings and Production Decisions

I keep these three things separate throughout the repository.

| Ticket | Completed in the lab | Still open | Production decision |
|---|---|---|---|
| 008 | Baseline, V1, V2, Purple Team and adversarial tests | Three adversarial variations missed | Recommended for a production-readiness review only |
| 009 | V1–V3 design and testing | V3 dry-run only; signed approvals tested in isolation | NO-GO for unattended destructive remediation |
| 010 | Release gates, admission controls, supply-chain checks, rollback rehearsal | A02 under review; residual risk R06 open | Not established |
| 011 | Correlation engine, Falco rules, eight documented adversarial cases | Formal acceptance; 09:05 containment decision undated | Closure pending authorization |
| 012 | Detectors, 51 tests, containment and recovery tests | Egress isolation not enforced | NO-GO; closure not authorized |

Earlier tickets (001–007) are investigations and assessments completed in the lab. Their reports state their own limitations, such as Ticket 004's medium confidence and Ticket 006's undetermined root cause.

## Tools and Technologies

These are the tools that appear in the evidence for at least one ticket.

- **Operating systems and virtualization:** Windows 11, Ubuntu 24.04, Kali Linux, VirtualBox, Docker Desktop
- **Monitoring and investigation:** Wazuh, `journalctl`, `last`, `lastb`, Linux audit logs, packet captures, Falco, Kubernetes audit logs, synthetic AWS CloudTrail
- **Linux and networking:** OpenSSH, `systemctl`, cron, sudo logs, nftables, `curl`
- **Web and application stack:** Nginx, Flask, Apache HTTP Server
- **Containers and Kubernetes:** Docker, Minikube, kubectl, Helm, Pod Security Admission, ValidatingAdmissionPolicy, RBAC, NetworkPolicy
- **Supply-chain security:** Trivy, Syft, cosign
- **Languages and data:** Python, Bash, PowerShell, JSON, CSV, SQLite
- **Integrity:** SHA-256 (`sha256sum`, `Get-FileHash`), HMAC-SHA256
- **Frameworks:** MITRE ATT&CK
- **Documentation and version control:** Markdown, Mermaid, SVG, PDF, Git, GitHub

## How Each Ticket Is Organized

Every ticket folder has its own README, which is the place to start. Most tickets also include:

- an engineering notebook recording observations and decisions in order
- an `evidence/` folder with raw output, logs and, where used, SHA-256 manifests
- source code, scripts or configuration used in the lab
- a final report, and for later tickets an executive brief or decision record
- lessons learned

Where a ticket includes runnable code, its README explains how to run the tests and what results to expect. Some tests in Tickets 009 and 012 rewrite files in their evidence folders, so run them in a disposable copy; see [Ticket 009's README](ticket-009-automation-did-exactly-what-you-told-it/README.md#before-rerunning-tests-evidence-and-platform-warnings) and [Ticket 012's testing notes](ticket-012-final-capstone/TESTING-NOTES.md).

## Evidence Integrity and Privacy

Evidence is preserved as collected wherever possible, and hash manifests are included so files can be checked. When a file had to change after collection, the change is documented rather than hidden.

- On November 22, 2026, I redacted my local Windows account and computer names from evidence files, screenshots and one PDF. The affected Ticket 010 hash manifests were updated and re-verified, and a dated addendum explains the change in [`final-integrity-audit.md`](ticket-010-the-patch-that-passed-every-check/closure/final-integrity-audit.md).
- In the same cleanup, three Ticket 002 evidence files whose line endings Git had changed on commit were restored to their original bytes. They now match the original manifest; see [`evidence-integrity-verification.md`](ticket-002-production-web-application-outage/evidence-integrity-verification.md).

The repository, including its full Git history, was scanned for exposed credentials such as passwords, API keys, access tokens and private keys, and none were identified. Credentials in examples are placeholders, and data that resembles business data is synthetic.
