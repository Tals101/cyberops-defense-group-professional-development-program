# Ticket #006 — Evolving Incident

## The 9:17 A.M. Alert

This project documents a staged cybersecurity incident investigation involving unusual outbound HTTPS activity from a simulated Finance workstation, `FIN-WS17`.

The exercise focuses on professional incident response under uncertainty: triage, evidence correlation, containment judgment, business continuity, executive communication, and the ability to revise an assessment as new evidence emerges.

## Scenario

At 09:17, Security received a high-severity alert for unusual outbound HTTPS activity from `FIN-WS17`, associated with Finance user `mreynolds`.

The investigation progressed through multiple timed phases. Early evidence supported both legitimate and malicious explanations. Later evidence established that Finance files were transmitted externally through recently introduced, unapproved software whose observed behavior did not match its represented data-conversion purpose.

## Final Classification

**Confirmed Security Incident — unauthorized external transmission of Finance data through unapproved and unverified software, with malware status and ultimate root cause unresolved.**

The investigation did not establish that:

- The employee acted maliciously.
- The software was definitively malware.
- The known vendor sent the original email.
- The vendor was compromised.
- An external attacker controlled the workstation.

## Key Investigation Findings

- Confirmed outbound HTTPS communication from `FIN-WS17`.
- Correlated network activity with endpoint process execution.
- Confirmed external transmission of two synthetic Finance files.
- Verified transmitted files against originals with SHA-256.
- Distinguished an approved `finance_sync.sh` workflow from `document_cache.sh`.
- Identified recurring communications from the same recently introduced process.
- Determined that the questioned utility performed no observable data conversion.
- Determined that the receiving server also performed no observable conversion.
- Identified a self-signed TLS certificate and disabled certificate validation.
- Found no associated cron or systemd persistence during the scoped investigation.
- Preserved uncertainty regarding phishing, vendor compromise, impersonation, or Trojanized software.

## Decision Progression

| Time | Decision |
|---|---|
| 09:30 | Continue investigation without immediately disrupting Finance. |
| 10:15 | Use targeted containment and increased monitoring. |
| 11:00 | Escalate to network containment while keeping the workstation powered on. |
| 12:30 | Maintain containment and move Finance work to a clean trusted system. |
| 13:30 | Classify as a confirmed security incident with root cause unresolved. |

## Business Continuity

Security did not treat containment as the end of the problem.

Finance was provided a safer continuity strategy:

- Use a clean trusted workstation.
- Recover only validated business data.
- Use an approved conversion method.
- Independently verify the vendor through a known contact channel.
- Keep `FIN-WS17` isolated while investigation and remediation continue.

## Repository Structure

    ticket-006-evolving-incident/
    ├── README.md
    ├── Final_Investigation_Report.pdf
    ├── lessons-learned.md
    ├── engineering-notebook.md
    ├── communications/
    ├── decisions/
    ├── evidence/
    │   ├── logs/
    │   ├── network/
    │   ├── endpoint/
    │   └── screenshots/
    ├── timeline/
    │   └── incident-timeline.csv
    └── diagrams/

## Evidence

This repository contains a **sanitized portfolio evidence set** from a controlled lab.

The public GitHub version intentionally excludes:

- Private keys.
- Credentials.
- Tokens.
- Pretest artifacts.
- Raw received Finance-data bodies.
- Other unnecessary sensitive or lab-only material.

The full closure package retains the complete evidence set separately.

## Skills Demonstrated

- Incident triage
- Hypothesis-driven investigation
- Linux audit analysis
- Network packet analysis
- Process and file correlation
- SHA-256 integrity validation
- Static script analysis
- TLS certificate analysis
- Containment decision-making
- Business continuity planning
- Executive communication
- Confidence calibration
- Timeline reconstruction
- Evidence preservation

## Git History Note

The investigation artifacts were originally preserved during the staged lab exercise before later phases were opened.

The Git commits in this repository were created afterward when the completed investigation was organized for GitHub. The commit sequence preserves the investigation's logical phase order, but commit timestamps are not represented as original incident timestamps.

See `timeline/incident-timeline.csv` for event times and the times Security learned about each event.

## Lab Notice

All systems, users, Finance data, network addresses, and incident activity in this project are part of a controlled cybersecurity lab simulation.
