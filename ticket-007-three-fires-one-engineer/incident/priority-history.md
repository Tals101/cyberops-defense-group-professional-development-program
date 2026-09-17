# Ticket #007 — Priority History

| Scenario Time | Priority 1 | Priority 2 | Priority 3 | Why Ranking Changed |
|---|---|---|---|---|
| 09:00 | Issue B | Issue A | Issue C | Word launched encoded PowerShell, EDR blocked a child process, and the endpoint remained online. Issue A was serious but more ambiguous. Issue C had a credible configuration-change explanation. |
| 09:25 | Issue C | Issue A | Issue B | Customer-facing errors required an immediate rollback decision. Issue B evidence had become less urgent after the encoded command decoded as benign. Issue A remained under review for active privileged activity. |
| 09:40 | Issue B | Issue C | Issue A | The suspicious Word document was confirmed to come from an email attachment, PowerShell executed before the EDR block, and HR-LT-44 remained online. |
| 10:05 | Issue B | Issue C | Issue A | HR-LT-44 successfully communicated with an external destination. Portal errors improved after rollback. Issue A was confirmed as authorized maintenance. |
| 10:50 | Issue B | Issue C | Issue A | A second workstation contacted the same destination, expanding Issue B scope for targeted investigation, while no evidence raised A or C above it. |
| Final | Issue B | Issue C | Issue A | Issue B was confirmed as a security incident on HR-LT-44. Issue C was operational with security follow-up. Issue A was likely benign with an operational process failure. |

## Which Priority Decision Was Hardest?

The 09:25 decision was the hardest because Issue C had active customer impact while Issue A involved privileged production activity and Issue B was still unresolved. The decision required separating business urgency from security severity and allowing Operations to restore service without waiting for Security to complete every investigation.

## Which Decision Could Have Produced the Greatest Harm If Wrong?

The 09:40 decision to return Issue B to Priority 1 had the greatest potential consequence. If the suspicious email-driven execution and continued network connectivity had been underestimated, additional execution, credential theft, lateral movement, or data exposure could have occurred while attention remained elsewhere.
