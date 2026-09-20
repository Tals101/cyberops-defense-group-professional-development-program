# Ticket #007 — 10:05 Reassessment

## B — Likely Incident; Priority 1

**New evidence:** HR-LT-44 successfully connected to an external destination shortly after the suspicious Word-to-PowerShell activity. No established business relationship explains that destination.

**What it changes:** I now have a chain that crosses email delivery, process execution, incomplete prevention, and external communication. Possible purposes include command-and-control, payload retrieval, or data transfer, but the connection alone does not establish which occurred.

**Next move:** Start a deeper HR-LT-44 investigation with network/process correlation, then work through persistence, identity, data-access, and scope questions.

## C — Operational Issue with Security Follow-Up; Priority 2

Operations reverted the configuration change and the portal's error rate quickly moved toward baseline. The unusual requests did not stop. That split is important: service recovery supports the change as the likely outage cause but does not make every incoming request benign.

I am moving C out of the primary investigation. IT Operations owns stability; Security will keep reviewing the web traffic and reopen the issue if exploitation evidence or renewed service impact appears. **Confidence:** Moderate to high that the service degradation was operational.

## A — Likely Benign; Priority 3

The unfamiliar address is a newly provisioned administrator workstation. The `sysadmin` account owner has confirmed the login, and the reviewed commands fit routine maintenance. I have no current finding that justifies further primary investigative time.

The missing SOC-calendar entry still needs correction by Infrastructure Operations. That visibility problem should not be confused with proof of an attack. **Confidence:** High in the likely-benign assessment.

## Order and reasoning

The order remains **B → C → A** from Decision #3, but my confidence has shifted: the external connection strengthens B; successful rollback reduces C's immediate service risk; and owner confirmation resolves A's main authorization question.

## The stop decision

I am stopping the primary security investigation of A rather than continuing because I have already spent time on it. The correct follow-up is a maintenance-notification improvement, not more low-value hunting absent new evidence.
