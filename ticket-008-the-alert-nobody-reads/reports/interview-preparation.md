# Ticket #008 — Interview Preparation

## Purpose

Prepare concise talking points for explaining Ticket #008 — The Alert Nobody Reads — during a cybersecurity interview.

---

# 1. Give me the 30-second summary of the project.

I inherited a noisy authentication detection that generated 597 alerts from a 1,000-event dataset.

I measured the baseline before tuning it, identified duplication and benign noise, and redesigned the detection in two stages.

V1 changed the system from event-level alerts to behavioral detections.

V2 correlated related V1 alerts into analyst-facing cases.

The final design reduced 597 alerts to 7 correlated cases while preserving all six original suspicious scenarios and improving suspicious successful-authentication visibility from 0 of 2 to 2 of 2.

I also performed Purple Team and adversarial testing to document where the tuned detector could still fail.

---

# 2. What problem were you trying to solve?

The real problem was not simply high alert volume.

The problem was poor signal per analyst attention.

Analysts were receiving fragmented and repetitive authentication alerts, which increased the risk that meaningful alerts would be skimmed or ignored.

---

# 3. Why didn't you just raise the thresholds?

Because reducing alerts is not the same as improving detection.

A higher threshold may reduce noise but can also hide malicious activity.

I first measured:

- benign noise;
- duplication;
- suspicious-event coverage;
- suspicious-scenario coverage;
- successful-authentication visibility;
- estimated analyst workload.

Then I tuned based on evidence.

---

# 4. What were the baseline results?

The Original detector generated:

- 597 alerts;
- 248 known benign alerts;
- 349 suspicious-associated alerts;
- 289 duplicate, redundant, or additional alerts;
- approximately 49.75 analyst-hours at 5 minutes per alert.

It represented:

- 143 of 145 suspicious events;
- all 6 suspicious scenarios.

However, it explicitly detected:

- 0 of 2 suspicious successful authentications.

---

# 5. What was the biggest source of benign noise?

A stale service credential scenario.

The `svc_inventory` service account generated repeated failures and produced 142 baseline alerts.

That demonstrated how a detector can work exactly as written and still create poor analyst outcomes.

---

# 6. What did V1 change?

V1 moved from individual failure-event alerting to behavioral detection.

The behaviors included:

- rapid repeated failures;
- suspicious success after failures;
- password spraying;
- distributed targeting;
- privileged low-and-slow activity;
- persistent service-account failures.

---

# 7. What were the V1 results?

V1 reduced:

597 alerts

to:

15 alerts.

Estimated workload decreased from:

49.75 hours

to:

1.25 hours.

All six original suspicious scenarios remained represented.

V1 also explicitly detected both suspicious successful authentications.

---

# 8. What tradeoff did V1 introduce?

Suspicious event-level representation decreased from:

143 of 145

to:

64 of 145.

I documented that rather than hiding it.

The important distinction was that all six suspicious scenarios remained represented even though the detector stopped alerting on nearly every malicious event.

---

# 9. Why is event coverage different from scenario coverage?

Event coverage asks:

How many individual malicious events created detection evidence?

Scenario coverage asks:

Did the detector recognize the overall malicious behavior?

A behavioral detector can represent an attack with one meaningful alert rather than dozens of individual event alerts.

---

# 10. What did V2 do?

V2 was a correlation layer.

It took the 15 V1 alerts and grouped related signals into 7 analyst-facing cases.

Examples included:

- Authentication Attack Sequence;
- Password Spray Campaign;
- Distributed Targeting;
- Persistent Service Authentication Case.

---

# 11. Did V2 improve detection sensitivity?

No.

V2 improved correlation and analyst usability.

It did not inspect raw authentication events independently.

The architectural rule was:

`If V1 produces no signal, V2 has nothing to correlate.`

---

# 12. Why didn't you suppress familiar internal addresses?

Because familiar does not equal safe.

The dataset included a compromised familiar-source scenario.

Testing showed blanket suppression could remove suspicious alerts and reduce scenario coverage.

I treated source familiarity as context rather than trust.

---

# 13. How did you respond to the manager's suppression request?

I tested the proposal against the dataset instead of rejecting it based on opinion.

The estimated result was that V1 could fall from 15 alerts to about 12, but the change would remove only one benign alert while also removing suspicious signals from the familiar-source compromise scenario.

That evidence supported rejecting blanket suppression.

---

# 14. What did the Purple Team find?

The Purple Team distributed malicious authentication activity across:

- multiple users;
- multiple sources;
- longer time intervals.

No individual entity relationship crossed the V1 thresholds.

The expected alert did not fire.

---

# 15. Was the Purple Team miss a telemetry problem?

No.

The events existed in the telemetry.

The main problem was the analytical perspective.

The detector expected malicious behavior to concentrate around a user, source, or time-window relationship.

The attacker avoided that concentration.

---

# 16. How did you handle the Purple Team false negative?

I preserved it rather than immediately changing thresholds.

I classified the root cause and determined that a complementary campaign-level detector was more appropriate than continuously expanding V2.

---

# 17. What adversarial tests did you perform?

I created four deliberately evasive variations:

- AT-01 Threshold Skimming;
- AT-02 Distributed Many-to-Many;
- AT-03 Familiar-Source Failures Followed by Success;
- AT-04 Privileged Low-and-Slow.

AT-01, AT-02, and AT-03 were missed.

AT-04 was detected.

---

# 18. Doesn't detecting only 1 of 4 adversarial tests mean the detector is poor?

No.

The adversarial dataset was intentionally designed to probe the detector's weaknesses.

It was not representative production traffic.

The result should be interpreted as evidence of known blind spots, not as an overall 25% production detection rate.

---

# 19. What is the biggest remaining blind spot?

Distributed many-user/many-source authentication activity that remains below individual user, source, and time-window thresholds.

That requires a broader campaign-level analytical perspective.

---

# 20. What complementary detection would you build next?

I would evaluate a campaign-level detector using features such as:

- total failures;
- distinct users;
- distinct sources;
- user/source relationship density;
- privilege involvement;
- successful-authentication context;
- historical deviation;
- broader observation windows.

---

# 21. What did you learn about suspicious successful authentication?

A successful login can be more security-significant than the failures that came before it.

The Original detector generated many failure alerts but did not explicitly detect the two suspicious successes.

V1 corrected that.

---

# 22. How did you test alert usability?

I evaluated the final alert from the perspective of an analyst who did not build the detector.

The analyst needed to understand the core story within approximately 60 seconds.

The test result was:

PASS WITH REVISIONS.

---

# 23. What changes came from the usability test?

I revised the alert to:

- align severity with the demonstrated risk;
- qualify source familiarity;
- include destination/application/identity-provider context when available;
- move internal rule IDs below the plain-language explanation.

---

# 24. How much workload reduction did you achieve?

Using the lab assumption of five minutes per analyst unit:

Original:

49.75 hours.

V1:

1.25 hours.

V2:

0.58 hours.

The Original-to-V2 reduction was approximately 98.8% in analyst-facing units.

That percentage describes workload units, not detection accuracy.

---

# 25. Give an example of the correlation improvement.

The password-spray scenario produced:

- 120 Original alerts;
- 6 V1 source-level alerts;
- 1 V2 Password Spray Campaign case.

That clearly shows the progression from event-level noise to behavioral detection to campaign correlation.

---

# 26. How did you prevent over-tuning?

I froze versions and preserved evidence before further testing.

I also separated:

- Original logic;
- V1 detection;
- V2 correlation.

Purple Team and adversarial testing were performed against preserved versions rather than continuously modifying the detector after every result.

---

# 27. How would you operate this detector in production?

I documented:

- monthly detection-health review;
- quarterly coverage review;
- event-driven review;
- telemetry-quality monitoring;
- analyst feedback;
- false-negative tracking;
- adversarial retesting;
- change control;
- rollback;
- exception expiration;
- drift analysis.

---

# 28. What is detection drift?

Detection drift occurs when the rule stays the same but the environment changes.

Examples include:

- VPN adoption;
- remote-work changes;
- identity-provider changes;
- MFA or passwordless authentication;
- new service-account behavior;
- cloud migration;
- logging schema changes;
- changing attacker techniques.

---

# 29. What would make you roll back V2?

I would roll V2 back to V1 presentation if correlation caused:

- incorrect case merging;
- loss of useful distinctions;
- inaccurate context;
- analyst confusion.

V1 detection output is preserved as the preferred V2 rollback point.

---

# 30. What is your strongest takeaway from this project?

Detection engineering is not about making alerts disappear.

It is about producing useful, measurable security signal while understanding what visibility is gained, lost, or still missing.

Ticket #008 taught me to measure the baseline, test changes, preserve false negatives, validate analyst usability, and treat detection as an operational lifecycle rather than a one-time rule adjustment.

---

# Key Numbers to Memorize

Original alerts:

597

V1 alerts:

15

V2 cases:

7

Original workload:

49.75 hours

V1 workload:

1.25 hours

V2 workload:

0.58 hours

Original suspicious-event representation:

143 / 145

V1/V2 suspicious-event representation:

64 / 145

Original suspicious-scenario coverage:

6 / 6

V1 suspicious-scenario coverage:

6 / 6

V2 suspicious-scenario coverage:

6 / 6

Original suspicious successes:

0 / 2

V1/V2 suspicious successes:

2 / 2

Baseline benign alerts:

248

Baseline redundant/additional alerts:

289

Largest benign scenario:

LEG-03 — 142 alerts

Adversarial variations:

4

Detected:

1

Missed:

3

---

# One-Sentence Interview Answer

I redesigned a noisy authentication detection from 597 fragmented alerts into 7 correlated analyst cases while preserving all six original attack scenarios, explicitly detecting suspicious successes, and documenting the residual blind spots through Purple Team and adversarial testing.

---

# Status

Ticket #008 Interview Preparation completed.
