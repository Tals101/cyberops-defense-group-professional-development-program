# Ticket #007 — How My Priorities Changed

The order below records what needed my attention at each point in the **scenario timeline**, not a retrospective severity rating.

| Time | First | Second | Third | Reason at that moment |
|---|---|---|---|---|
| 09:00 | B | A | C | The Word-to-PowerShell alert involved a connected endpoint; A had unresolved authorization, while Operations could work C in parallel. |
| 09:25 | C | A | B | Customers still faced portal failures and Operations needed a rollback answer. B's decoded lab command appeared harmless, and A's session remained under review. |
| 09:40 | B | C | A | The Word document came from email, PowerShell had run before a child-process block, and HR-LT-44 remained connected. |
| 10:05 | B | C | A | Successful outbound communication strengthened the B incident hypothesis. Rollback improved C, and A was confirmed as maintenance. |
| 10:50 | B | C | A | HR-LT-51 contacted the same destination, requiring targeted scope work without proving a second compromise. |
| Final | B | C | A | HR-LT-44 remains the primary incident system; C is operational with a security follow-up; A is likely benign with a process gap. |

## Hardest call

The 09:25 switch to C required the most careful distinction between **security severity** and **the need for a decision right now**. A privileged session was still unresolved and B had not received a complete endpoint review, but Operations could not leave customers experiencing errors while waiting for Security to finish both investigations.

## Decision with the greatest downside if mistaken

The 09:40 return to B mattered most for possible security impact. Underestimating the email-to-execution chain while HR-LT-44 was still online could have left time for additional execution, credential abuse, or network movement. Those outcomes were risks I was trying to prevent, not findings the investigation established.
