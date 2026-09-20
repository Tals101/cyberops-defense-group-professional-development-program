# Ticket #007 — Lessons Learned

## 1. Why did I start with B?

Word starting encoded PowerShell on a still-connected HR workstation gave me an immediate question I could answer: what actually ran, and did anything follow it? EDR had blocked a child process, but I could not treat that as proof the whole activity was stopped. The likely impact of isolating one workstation was also easier to reverse than interrupting a production server.

## 2. Which issue initially looked threatening but proved less concerning?

A. An unfamiliar privileged login to APP-PROD-02 is not something I could dismiss at intake. Source identification, owner confirmation, and the reviewed commands eventually pointed to legitimate maintenance. The alert also exposed a real notification gap, even though I did not find an intrusion.

## 3. Which issue grew more concerning?

B. The benign decoded marker command initially lowered my concern. The email origin, incomplete EDR prevention, and later external connection made the wider event harder to explain away. One harmless test command did not answer every question about the document-driven activity.

## 4. When did I first interrupt my plan?

At **09:18**, after hearing that the `sysadmin` session on APP-PROD-02 was still active and issuing privileged commands. That information mattered more than completing the next routine B check at that moment.

## 5. What did the switches cost?

They interrupted the flow of each investigation and forced me to rebuild context. Saving the current question, observation, and next action kept that cost manageable. I would make the switches again because the new information could change the consequences of waiting.

## 6. Did I collect evidence with limited decision value?

Yes. Some checks reinforced a conclusion instead of changing it. Next time I would ask before each command: if this comes back positive or negative, will it affect containment, priority, or scope?

## 7. Which findings made the biggest difference?

Decoding the PowerShell command; mapping the SSH source; seeing the portal's response to rollback; establishing the email attachment as the trigger; and confirming external communication from HR-LT-44. Each finding changed what I was prepared to do next.

## 8. What delegation worked?

The SOC analyst's source check on A, Operations' portal-restoration work, and the additional engineer's bounded HR-LT-51 investigation all answered concrete questions without requiring me to switch away from the primary task for every data point.

## 9. What could I have handed off sooner?

Network-wide destination searching and direct confirmation of A's maintenance activity. Assigning those in parallel would have given me useful answers sooner.

## 10. What stayed with me?

I kept ownership of the priority calls, incident scope, containment recommendations, and coordination. Those choices depended on evidence from multiple workstreams and could not be delegated as isolated technical checks.

## 11. Did I chase an issue just because I had invested time in it?

No. Once A had administrator confirmation and routine command evidence, I reduced it to a process follow-up. I also stepped away from C as the primary security question once rollback improved the outage. More investigation is not automatically better investigation.

## 12. What evidence allowed me to reduce attention?

For A, it was source ownership plus the administrator's confirmation and maintenance-consistent commands. For C, it was the error trend after rollback and the fact that unusual requests continued independently of the service failures.

## 13. Where did business impact change my approach?

At 09:25, C temporarily moved to first because Operations needed an answer while customers were affected. That was an urgent service decision, not a conclusion that C had become the most serious security threat.

## 14. Where did potential security impact matter most?

An unauthorized privileged session could affect a production server. A malicious document on an HR endpoint could expose credentials or sensitive files. I considered those possible consequences even before evidence established whether they had occurred.

## 15. How did reversibility factor in?

Isolating one endpoint could be undone after validation, while terminating a legitimate privileged session or disrupting a production server might create a wider business problem. I considered both the cost of a false positive and the cost of waiting.

## 16. What would I do with five engineers?

I would assign an owner to each issue, a fourth to environment-wide indicator searches, and a fifth to incident coordination and communication. Parallel work would reduce the number of context switches without removing the need to reconcile findings centrally.

## 17. What if no additional engineer were available?

I would narrow each request to its highest-decision-value check, lean on Operations for their own service work, and document the risk I was leaving unexamined while focusing on B.

## 18. What is my main takeaway about urgency and importance?

Urgency asks how long a decision can wait; importance asks what happens if I get it wrong. Those are not always the same. This ticket reinforced the need to revisit the order when evidence, customer impact, or the cost of interruption changes, instead of working alerts mechanically from their original severity labels.
