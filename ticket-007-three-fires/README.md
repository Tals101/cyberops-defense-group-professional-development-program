# Ticket #007 — Three Fires, One Engineer

## Overview

Ticket #007 is a cybersecurity incident-response exercise focused on triage, prioritization, context switching, delegation, containment, scope management, and executive communication while multiple incidents compete for limited engineering attention.

Three simultaneous issues were investigated:

- **Issue A:** Unusual privileged SSH access to APP-PROD-02
- **Issue B:** Microsoft Word launching encoded PowerShell on HR-LT-44
- **Issue C:** Customer-facing portal degradation with unusual web requests

The exercise demonstrates how priorities changed as new evidence became available and how security severity, business impact, reversibility, uncertainty, and available resources influenced each decision.

## Final Dispositions

### Issue A
**Likely Benign / Operational Process Failure**

The sysadmin login was confirmed as authorized maintenance from a newly provisioned administrator workstation. No malicious commands were identified. The remaining issue was a maintenance-notification gap.

### Issue B
**Confirmed Security Incident**

HR-LT-44 opened a suspicious email attachment that resulted in Microsoft Word launching encoded PowerShell. PowerShell executed before EDR blocked a child process, and the workstation subsequently communicated with an external destination with no established business relationship.

No persistence, credential theft, lateral movement, or sensitive-data theft was confirmed.

### Issue C
**Operational Issue with Security Follow-Up**

Portal errors improved rapidly after rollback of a recent configuration change. Unusual web requests continued, but available evidence did not establish them as the cause of the outage or demonstrate successful exploitation.

## Priority History

The investigation deliberately preserved each priority decision rather than rewriting earlier decisions after new evidence appeared.

1. **09:00 — B > A > C**
2. **09:25 — C > A > B**
3. **09:40 — B > C > A**
4. **10:05 — B > C > A**
5. **10:50 — B > C > A**

This history demonstrates evidence-driven reprioritization rather than hindsight-based reconstruction.

## Repository Structure

    ticket-007-three-fires/
    ├── README.md
    ├── Final_Incident_Report.pdf
    ├── engineering-notebook.md
    ├── lessons-learned.md
    ├── triage/
    ├── decisions/
    ├── communications/
    ├── coordination/
    ├── evidence/
    └── dispositions/

## Key Skills Demonstrated

- Multi-incident triage
- Risk-based prioritization
- Windows process investigation
- Linux authentication investigation
- Network evidence analysis
- Incident containment decisions
- Scope determination
- Delegation and resource management
- Stakeholder coordination
- Executive communication
- Evidence preservation
- Business-impact analysis
- Incident documentation
- Lessons-learned analysis

## Evidence Handling

This lab combines real operating-system telemetry with clearly labeled simulated enterprise evidence.

Simulated records were used where enterprise systems such as corporate EDR, email telemetry, or asset-management platforms were not available in the home lab.

Investigation conclusions distinguish observed evidence, simulated scenario evidence, and limitations.

## Primary Incident

The primary confirmed incident involved **HR-LT-44**.

A second HR workstation, **HR-LT-51**, contacted the same destination and was investigated. Additional triage did not identify the same Word-to-PowerShell execution chain or other supporting compromise indicators, demonstrating that shared infrastructure alone does not establish a shared root cause.

## Key Lesson

The highest-severity alert is not automatically the highest-priority task.

Effective incident response requires continuously reassessing:

- Security impact
- Business impact
- Time sensitivity
- Evidence quality
- Reversibility
- Cost of waiting
- Cost of interruption
- Available resources
- Value of the next investigative action
