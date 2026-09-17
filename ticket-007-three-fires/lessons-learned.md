# Ticket #007 — Lessons Learned

## 1. What did you initially prioritize and why?
I initially prioritized Issue B because Word launched encoded PowerShell, EDR blocked a child process, and the workstation remained online. It had the strongest combination of suspicious behavior, urgency, and reversible containment.

## 2. Which issue looked most dangerous but ultimately was not?
Issue A. Privileged access to a production server appeared high risk, but later evidence showed the login was authorized maintenance from a newly provisioned administrator workstation.

## 3. Which issue became more serious than it first appeared?
Issue B. It initially looked suspicious but uncertain. The email attachment, successful PowerShell execution, and subsequent external communication substantially increased concern.

## 4. When did you first change priorities?
At 09:18, when Issue A was reported to have an active sysadmin session executing privileged commands.

## 5. Was switching investigations costly?
Yes. Each switch required rebuilding context and delayed unfinished work, but the switches were justified by higher-value new information.

## 6. Did you spend time collecting evidence that did not affect a decision?
Some evidence confirmed existing conclusions rather than changing them. The lesson is to favor evidence that could actually change containment, scope, or priority.

## 7. What evidence had the highest decision value?
The decoded PowerShell command, confirmation of Issue A's administrator source, the portal rollback result, the email origin, and successful external communication from HR-LT-44.

## 8. What did you delegate well?
Issue A source validation, Issue C operational rollback work, and bounded HR-LT-51 triage.

## 9. What should you have delegated sooner?
Environment-wide network searching and confirmation of Issue A's maintenance activity could have been assigned earlier.

## 10. What did you keep ownership of and why?
I retained prioritization, containment decisions, incident scope, and coordination because those decisions required integrating evidence and business impact across all workstreams.

## 11. Did you continue investigating anything because you had already invested time in it?
No. Issue A was deliberately deprioritized once evidence supported authorized maintenance. Issue C moved to security follow-up after rollback restored service.

## 12. When did you know an issue could be deprioritized?
Issue A could be deprioritized after the administrator confirmed the login and commands matched routine maintenance. Issue C could be reduced after rollback rapidly improved the errors.

## 13. How did business impact influence your ranking?
Customer-facing portal degradation temporarily raised Issue C because an immediate operational decision was required even though security causation was uncertain.

## 14. How did potential security impact influence your ranking?
Potential privileged compromise and suspicious endpoint execution received high priority because either could lead to persistence, credential theft, lateral movement, or data exposure.

## 15. How did reversibility affect your decisions?
Reversible actions were easier to justify quickly. Endpoint isolation affected one user and could be reversed, while production-server containment carried greater operational risk.

## 16. What would change with five engineers?
I would assign parallel owners to Issues A, B, and C, plus environment-wide IOC searching and incident coordination. This would reduce context switching and shorten time to decision.

## 17. What would change with no additional engineers?
I would narrow evidence collection further, rely more heavily on bounded operational delegation, and explicitly accept greater residual risk in lower-priority workstreams.

## 18. What did this ticket teach you about urgency versus importance?
Urgency reflects how quickly a problem demands action. Importance reflects potential organizational impact. The highest-priority issue is not always the loudest or highest-severity alert; priority depends on current evidence, business impact, time sensitivity, reversibility, and the value of acting now.
