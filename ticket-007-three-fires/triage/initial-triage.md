# Ticket #007 — Initial Triage Assessment

*Assessment made before rapid triage and later escalations.*

## Issue A — Privileged SSH access

**What I know:** A `sysadmin` login succeeded on APP-PROD-02 from an unfamiliar internal address. The alert did not come with a failed-login burst, a maintenance notice, or related detections.

**What I still need:** The source host and its owner, authorization for the session, whether the user is still connected, and a reliable account of the commands run.

**Security exposure:** If unauthorized, this is privileged access to a production server; persistence, lateral movement, and access to application data are plausible consequences, not established findings.

**Operational exposure:** APP-PROD-02 serves an internal application. Disabling the account or terminating the session could interrupt legitimate administration or service.

**Urgency and reversibility:** High urgency if the session is hostile. A session or account restriction can be reversed, but production impact must be considered.

**Confidence at intake:** Low to moderate; the event is real, but intent and authorization are unknown.

## Issue B — Word launching PowerShell

**What I know:** Word started encoded PowerShell on HR-LT-44. EDR reported that it blocked a child process, while the workstation remained online.

**What I still need:** The decoded command, the document that triggered it, the blocked process, other execution, network activity, and signs of persistence.

**Security exposure:** The process chain could represent malicious document execution, with possible follow-on credential access or lateral movement. None of that is confirmed yet.

**Operational exposure:** Network isolation would mainly interrupt one HR user's work, rather than an entire production application.

**Urgency and reversibility:** High while the endpoint remains connected. Isolation is comparatively easy to undo if the evidence changes.

**Confidence at intake:** Moderate to high that rapid investigation is warranted; low confidence about the command's purpose.

## Issue C — Portal errors

**What I know:** Customers are encountering increased errors following a configuration change. Unusual web requests have also appeared.

**What I still need:** An error timeline, a traffic sample, the precise change window, and the portal's response to rollback.

**Security exposure:** Scanning or attempted exploitation is possible, but there is no proof the requests caused the failures.

**Operational exposure:** Customer-facing service is already degraded.

**Urgency and reversibility:** The availability issue needs attention now. Operations is engaged, and a known-good configuration can be restored if the change is at fault.

**Confidence at intake:** Low that the outage is a security incident.

## Initial order: B → A → C

I will start with B because it combines an unusual execution chain with a still-connected endpoint and a relatively contained response option. A follows because privileged production access has a high potential cost, even though the evidence is ambiguous. C is third **for my direct investigative time**, not third in business importance: Operations can work the service-restoration decision in parallel.

## Work assigned immediately

- **SOC analyst, Issue A:** Identify the source, confirm ownership and expected access, and look for other alerts tied to the session.
- **IT Operations, Issue C:** Save the relevant logs, compare the deployment with the error increase, review representative requests, and have rollback ready.

## First five minutes

| Issue | First question | Why it is worth asking |
|---|---|---|
| B | What does the encoded command actually execute, and what spawned from it? | The answer could change the containment decision immediately. |
| A | Who owns the source address, and was access approved? | This distinguishes an administrative session from a potentially unauthorized one. |
| C | Did errors follow the change or the unusual requests? | Timing helps decide whether Security should affect the rollback decision. |
