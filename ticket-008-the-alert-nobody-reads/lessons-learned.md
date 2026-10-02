# Ticket #008 — Lessons Learned

## Purpose

Capture the most important engineering lessons from Ticket #008 in a question-and-answer format suitable for closure review and interview preparation.

---

## 1. What was the main problem with the original detector?

The main problem was not simply that the detector had low thresholds.

The deeper problem was that it produced too many event-level alerts and too much duplicate signaling for the amount of useful context delivered to the analyst.

The original detector generated 597 alerts from 1,000 authentication events, including 248 benign alerts and 289 duplicate, redundant, or additional alerts.

---

## 2. Why was reducing alert count alone not enough?

A lower alert count does not automatically mean a better detector.

A detector could reduce alerts by suppressing legitimate warning signs or by missing malicious activity.

The correct objective was to improve signal per analyst attention while measuring what coverage was preserved or lost.

---

## 3. Why was ground truth kept separate from operational telemetry?

Ground truth was separated so the detector could not use labels such as benign or suspicious during detection.

The detector had to make decisions from the same type of data an operational system would see.

Ground truth was used only afterward for evaluation.

---

## 4. What did the baseline measurement reveal?

The baseline showed that the original detector had broad suspicious-event visibility but poor operational efficiency.

Key findings included:

- 597 alerts;
- 49.75 estimated analyst-hours;
- 248 known benign alerts;
- 289 redundant or additional alerts;
- 143 of 145 suspicious events represented;
- 6 of 6 suspicious scenarios represented;
- 0 of 2 suspicious successful authentications explicitly detected.

---

## 5. What was the biggest benign noise source?

The stale service credential scenario, LEG-03, was the largest benign noise source.

It produced 142 alerts.

This demonstrated that repetitive benign operational behavior can dominate an alert queue even when the underlying detector is technically functioning as designed.

---

## 6. Why was blanket familiar/internal-source suppression rejected?

Because familiar does not mean safe.

The dataset included a compromised familiar-source scenario.

Suppressing familiar sources could have reduced alert count but also removed suspicious activity and potentially reduced scenario coverage from 6 of 6 to 5 of 6.

Source familiarity should be treated as context, not proof of legitimacy.

---

## 7. What was the main improvement introduced by V1?

V1 changed the detection approach from broad event-level alerting to behavioral detection.

Instead of alerting on nearly every failure, V1 focused on patterns such as:

- rapid repeated failures;
- suspicious success after failures;
- password spraying;
- distributed targeting;
- privileged low-and-slow activity;
- persistent service-account failures.

---

## 8. What important coverage did V1 add?

V1 explicitly detected both suspicious successful-authentication events.

The original detector detected 0 of 2 suspicious successes.

V1 detected 2 of 2.

This was important because a successful authentication after suspicious failures may represent the actual point of compromise.

---

## 9. What tradeoff did V1 introduce?

V1 reduced suspicious event-level representation.

Original:

143 of 145 suspicious events represented.

V1:

64 of 145 suspicious events represented.

However, all 6 original suspicious scenarios remained represented.

This showed the difference between event-level coverage and scenario-level behavioral coverage.

---

## 10. Why was V2 created?

V1 substantially reduced alert volume, but several V1 alerts could still describe the same underlying attack.

V2 was created to correlate related V1 alerts into analyst-facing behavioral cases.

Its purpose was to reduce manual reconstruction, not to create new raw-event sensitivity.

---

## 11. What is the most important limitation of V2?

V2 only correlates V1 alerts.

It does not independently inspect raw authentication events.

Therefore:

If V1 produces no signal, V2 has nothing to correlate.

This is a key architectural limitation.

---

## 12. What did the Purple Team exercise reveal?

The Purple Team demonstrated that malicious authentication activity could be distributed across:

- multiple users;
- multiple sources;
- longer time periods.

Because no individual relationship crossed the existing thresholds, the expected alert did not fire.

This exposed a gap in analytical perspective, not simply a missing threshold.

---

## 13. Why was the Purple Team miss not immediately fixed by changing thresholds?

Changing a threshold after every miss can create unstable detection logic and new false positives.

The better response was to preserve the false negative, classify why it occurred, and determine whether the problem required:

- tuning;
- a complementary detector;
- better telemetry;
- broader historical analysis.

For the Purple Team miss, a complementary campaign-level detector was the more appropriate direction.

---

## 14. What did adversarial testing add beyond the baseline test?

The baseline dataset tested known scenarios.

Adversarial testing deliberately tested the detector's boundaries.

It showed that the tuned design could miss:

- threshold skimming;
- distributed many-user/many-source attacks;
- familiar-source sub-threshold failures followed by success.

This provided stronger evidence of where the detector could fail.

---

## 15. What was learned from AT-04, the privileged low-and-slow test?

AT-04 confirmed that V1-05 successfully preserved detection of privileged low-and-slow behavior.

The test produced:

- one V1 alert;
- one V2 case.

This demonstrated that tuning had not removed all low-rate attack visibility.

---

## 16. Why is the 25% adversarial detection result not an overall detector accuracy score?

The adversarial test set was intentionally designed to probe known weaknesses.

It contained only four deliberately evasive variations.

It was not sampled to represent normal production traffic.

Therefore, the 1-of-4 result is useful for identifying blind spots but should not be generalized into an overall production detection rate.

---

## 17. What did the analyst usability test show?

The alert design was understandable, but improvements were needed.

The result was:

PASS WITH REVISIONS

The analyst could determine within approximately 60 seconds:

- why the alert fired;
- whether privilege was involved;
- whether authentication succeeded;
- the source involved;
- the scale and duration;
- the first investigation steps.

---

## 18. What alert-design changes improved analyst usability?

The final alert design was revised to:

- align severity with the risk shown in the example;
- qualify source familiarity using available history;
- include destination, application, or identity-provider context when available;
- move engineering rule IDs below the plain-language explanation.

The lesson was that detection quality includes presentation quality.

---

## 19. Why does detection drift matter?

A detection can remain technically unchanged while the environment changes around it.

Drift can come from:

- workforce changes;
- remote work;
- VPN changes;
- cloud migration;
- new identity providers;
- MFA or passwordless adoption;
- new service-account patterns;
- schema changes;
- attacker tradecraft.

Detection engineering therefore requires ongoing review, not one-time deployment.

---

## 20. What is the most important overall lesson from Ticket #008?

Detection engineering is a lifecycle.

A successful tuning effort must measure more than alert reduction.

It must examine:

- noise;
- duplication;
- scenario coverage;
- event coverage;
- successful-authentication visibility;
- analyst usability;
- false negatives;
- architecture;
- telemetry dependencies;
- drift;
- rollback;
- residual risk.

The strongest outcome from Ticket #008 was the transition from event-level alert accumulation to behavioral detection and correlated analyst cases while keeping the tradeoffs visible.

---

# Final Lessons-Learned Summary

Ticket #008 demonstrated that effective detection tuning requires balancing three goals:

1. reduce unnecessary analyst workload;
2. preserve meaningful security visibility;
3. document what the tuned system still cannot detect.

The final V1/V2 strategy materially improved analyst efficiency, but the project intentionally preserved known blind spots rather than hiding them.

That transparency is part of the engineering result.

---

# Status

Lessons Learned — 20 Questions completed.
