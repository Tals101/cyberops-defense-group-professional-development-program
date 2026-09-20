# Ticket #007 — Incident Action Plan

This plan assigns the work that follows the HR-LT-44 incident decision. Deadlines are relative to the exercise's response timeline, not evidence that each task has already been completed.

## Now — contain, preserve, find related activity

| Action | Lead | Target | Needs | Escalate if |
|---|---|---|---|---|
| Keep HR-LT-44 isolated from the network | Security / Endpoint Support | Immediate | Endpoint containment access | The host reconnects or isolation fails |
| Save Windows, EDR, email, and network records | SOC | Immediate | Telemetry and retention access | Records are missing or could be overwritten |
| Preserve the email, attachment, and sender details | SOC analyst | Immediate | Mail search access | Other employees received the message |
| Search for the destination and related indicators | SOC / Network Engineering | Immediate | Network visibility | Another endpoint shows related suspicious activity |

## First hour — determine reach and potential impact

| Action | Lead | Target | Needs | Escalate if |
|---|---|---|---|---|
| Identify all recipients and openers of the message | Email Administration / SOC | Within 1 hour | Message-trace and mailbox search | Other recipients opened the attachment |
| Check HR-LT-44 for persistence and credential access | Security | Within 1 hour | Endpoint evidence | A persistence or credential-access indicator is found |
| Review HR user's sign-ins and sessions | IAM | Within 1 hour | Identity telemetry | Unexpected sign-ins or token use appears |
| Decide whether destination blocking is safe and warranted | Network Engineering / Security | Within 1 hour | Destination and collateral-impact review | Further malicious communication is observed |

## Same day — remediate without losing evidence

| Action | Lead | Target | Needs | Escalate if |
|---|---|---|---|---|
| Decide whether HR-LT-44 needs reimaging | Endpoint Support / Security | Today | Investigation and preservation complete | System integrity cannot be verified |
| Determine whether sensitive HR data was accessed | Security / HR | Today | File and endpoint review | Exposure becomes credible or confirmed |
| Assign the undocumented maintenance process gap | Infrastructure Operations | Today | Admin confirmation | Unrecorded changes are recurring |
| Continue portal traffic review separately | SOC | Today | Preserved web logs | Evidence of exploitation emerges |

## After containment — validate and close

| Action | Lead | Timing | Needs | Escalate if |
|---|---|---|---|---|
| Remove identified malicious artifacts, if any | Endpoint Support | After preservation | Security approval | Cleanup could destroy evidence |
| Validate a clean state before returning HR-LT-44 | Endpoint Support / Security | After remediation | Endpoint checks | Suspicious behavior continues |
| Consolidate the timeline and incident record | Security | Before closure | All workstream findings | New evidence changes impact or scope |
| Review the incident and improve controls | SOC Manager / Security | After stabilization | Findings and follow-up owners | A systemic control gap is identified |
