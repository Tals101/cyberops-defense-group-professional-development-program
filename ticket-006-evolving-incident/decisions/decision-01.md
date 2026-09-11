# Ticket #006 — Decision Point #1

## Decision

C — Take another defensible action.

Implement targeted containment rather than immediately isolating FIN-WS17.

The preferred action is to restrict the suspicious data-transfer path associated with document_cache.sh and increase monitoring while allowing the workstation to remain operational for necessary Finance work.

## Evidence Supporting the Decision

- Two Finance files were confirmed to have been transmitted externally.
- document_cache.sh performed the archive-and-transfer activity.
- document_cache.sh is not documented as the authorized Finance business workflow.
- FIN-WS17 continues communicating with the destination.
- The external infrastructure is used by legitimate organizations as well as having a history of abuse.
- finance_sync.sh also uses the same infrastructure for a documented business function.
- No antivirus alert has been generated.
- No cron or systemd persistence mechanism has been identified.
- The workstation remains operational.
- The user has reported no unusual behavior.

## Strongest Argument Against the Decision

The strongest argument against targeted containment is that confirmed Finance data has already left the workstation and communications are continuing.

If document_cache.sh is malicious, allowing FIN-WS17 to remain connected could permit additional data loss or other attacker activity that has not yet been identified.

Immediate isolation would provide stronger assurance that no further network-based exposure occurs.

## Security Risk

Security risk remains High.

Targeted containment reduces the immediate risk of repeating the identified transfer while preserving the ability to collect additional evidence.

Residual risk remains because broader compromise has not been ruled out.

## Operational Risk

Full isolation could interrupt time-sensitive Finance reporting and other legitimate business activity.

Targeted containment reduces this operational impact by allowing Mark to continue necessary work while Security monitors the system.

## What Would Cause the Decision to Change

Immediately isolate FIN-WS17 if any of the following occur:

- Another unauthorized Finance-file transfer is observed.
- document_cache.sh executes again.
- Communication expands to additional suspicious destinations.
- Evidence of credential theft, persistence, lateral movement, or command-and-control appears.
- Additional sensitive Finance data is staged for transfer.
- Antivirus or other security tooling generates a corroborating alert.
- The destination or document_cache.sh is confirmed to be unauthorized.
- Targeted controls cannot reliably prevent further data transfer.
