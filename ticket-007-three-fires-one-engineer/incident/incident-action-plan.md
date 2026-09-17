# Ticket #007 — Incident Action Plan

## Immediate Actions

| Action | Owner | Deadline | Dependency | Escalation Condition |
|---|---|---|---|---|
| Keep HR-LT-44 contained from the network | Security / Endpoint Team | Immediate | Endpoint containment capability | Containment fails or host reconnects |
| Preserve EDR, Windows, email, and network evidence | SOC | Immediate | Log and EDR access | Evidence is unavailable or at risk of loss |
| Validate and preserve the suspicious email and attachment | SOC Analyst | Immediate | Mail telemetry | Same message found in additional mailboxes |
| Search environment for the external destination and related indicators | SOC / Network Engineering | Immediate | Network telemetry | Additional suspicious endpoints identified |

## Within One Hour

| Action | Owner | Deadline | Dependency | Escalation Condition |
|---|---|---|---|---|
| Determine whether other users received the same email | SOC / Email Admin | 1 hour | Mail search capability | Multiple recipients opened attachment |
| Review HR-LT-44 for persistence and credential-access indicators | Security | 1 hour | Endpoint telemetry | Persistence or credential theft identified |
| Review identity activity for the HR user | IAM | 1 hour | Identity logs | Unusual logins or token use identified |
| Evaluate whether destination blocking is appropriate | Network Engineering + Security | 1 hour | Destination validation | Additional malicious communication observed |

## Later Today

| Action | Owner | Deadline | Dependency | Escalation Condition |
|---|---|---|---|---|
| Determine remediation or reimage requirements for HR-LT-44 | Endpoint Team / Security | Today | Investigation findings | System integrity cannot be established |
| Review whether sensitive HR data was accessed | Security + HR | Today | File and endpoint evidence | Confirmed sensitive-data access |
| Document Issue A maintenance-process failure | Infrastructure Operations | Today | Administrator confirmation | Repeated undocumented maintenance identified |
| Continue lower-priority review of unusual portal traffic | SOC | Today | Web logs | Exploitation evidence appears |

## After Containment

| Action | Owner | Deadline | Dependency | Escalation Condition |
|---|---|---|---|---|
| Remove malicious artifacts if confirmed | Endpoint Team | After evidence preservation | Forensic preservation complete | Removal risks destroying evidence |
| Restore HR-LT-44 to service only after validation | Endpoint Team / Security | After remediation | Clean-state validation | Suspicious activity remains |
| Complete incident timeline and final report | Security | Before closure | All workstreams report back | Significant new evidence changes scope |
| Conduct lessons learned and control improvements | SOC Manager / Security | After incident stabilization | Incident facts finalized | Systemic control gaps identified |
