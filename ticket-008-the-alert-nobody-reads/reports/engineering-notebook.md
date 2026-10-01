# Ticket #008 — Engineering Notebook

## Ticket

Ticket #008 — The Alert Nobody Reads

Priority:

High

Role:

Junior Security Engineer

Objective:

Reduce authentication-alert noise while preserving meaningful security coverage and producing evidence that the revised detection strategy provides better signal per analyst attention.

---

# Engineering Principles Used

Throughout Ticket #008, the following principles were maintained:

- preserve evidence before tuning;
- measure the baseline before proposing changes;
- separate operational telemetry from ground truth;
- do not suppress alerts merely because analysts dislike the volume;
- do not use broad whitelists as the primary tuning strategy;
- treat familiar/internal sources as context rather than proof of legitimacy;
- define expected outcomes before testing revisions;
- preserve false negatives rather than tuning them away immediately;
- distinguish alert-volume reduction from detection coverage;
- keep V1 detection and V2 correlation conceptually separate;
- document rollback and residual risk.

---

# Phase 1 — Detection Health Assessment

## Initial Problem

The authentication detector generated more than 600 alerts in the operating scenario.

Analysts reported that routine noise caused authentication alerts to be skimmed or ignored.

The engineering task was therefore not simply:

`reduce alerts`

The actual problem was:

`increase useful signal per unit of analyst attention without creating unacceptable coverage loss.`

---

# Phase 2 — Dataset and Scenario Design

A deterministic authentication dataset was created using:

`generate_auth_dataset.py`

Random seed:

`8008`

The dataset contained:

- 1,000 authentication events;
- 855 benign events;
- 145 suspicious events.

Operational telemetry was stored separately from ground truth.

Operational dataset:

`dataset/authentication-events.csv`

Ground truth:

`dataset/authentication-ground-truth.csv`

This prevented detector logic from using scenario labels during detection.

---

# Benign Scenarios

## LEG-01 — Normal Business Authentication

600 events

Purpose:

Represent ordinary authentication behavior.

---

## LEG-02 — Ordinary Password Mistakes

90 events

Composition:

- 60 failures;
- 30 successes.

Purpose:

Represent normal user password-entry mistakes.

---

## LEG-03 — Stale Service Credentials

72 failures

Account:

`svc_inventory`

Source:

`10.20.30.25`

System:

`APP-SRV-25`

Pattern:

Repeated failures approximately every five minutes.

Purpose:

Create benign activity that looks operationally suspicious.

---

## LEG-04 — Benign Unfamiliar Source

48 events

Purpose:

Demonstrate that unfamiliar source does not automatically mean malicious.

---

## LEG-05 — Legitimate Privileged Administration

45 events

Purpose:

Ensure privileged context does not automatically create malicious ground truth.

---

# Suspicious Scenarios

## SUS-01 — Concentrated Brute Force

35 failures

Purpose:

Test concentrated repeated-failure detection.

---

## SUS-02 — Failures Followed by Privileged Success

9 events

Composition:

- 8 failures;
- 1 success.

Account:

`admin.backup`

Context:

Privileged and unfamiliar source.

Purpose:

Test whether the detector recognizes the successful authentication that may represent compromise.

---

## SUS-03 — Distributed Password Spray

60 failures

Pattern:

Approximately 30 users across multiple unfamiliar sources.

Purpose:

Test source-to-many-user behavior.

---

## SUS-04 — Low-and-Slow Attack

18 failures

Target:

`finance.admin`

Duration:

Approximately six hours.

Purpose:

Test lower-rate privileged targeting.

---

## SUS-05 — Compromised Familiar Source

13 events

Composition:

- 12 failures;
- 1 success.

Target:

`payroll.manager`

Source:

`WS-018`

Context:

Familiar source.

Purpose:

Test the assumption that familiar/internal sources are not automatically safe.

---

## SUS-06 — Distributed Attack Against One Account

10 failures

Target:

`vp.operations`

Pattern:

Multiple sources against one account.

Purpose:

Test many-source/one-user behavior.

---

# Phase 3 — Original Detector Baseline

The original detector implemented four broad rules.

## BASE-R1

Every failed authentication generated an alert.

## BASE-R2

Repeated failures for the same user generated additional alerts.

Threshold:

At least 3 failures in the prior 10 minutes.

## BASE-R3

Unfamiliar-source failures generated additional alerts.

## BASE-R4

Privileged-account failures generated additional alerts.

---

# Baseline Results

Total alerts:

597

Rule counts:

- BASE-R1: 308
- BASE-R2: 119
- BASE-R3: 139
- BASE-R4: 31

Unique alerting events:

308

Known benign alerts:

248

Known suspicious alerts:

349

Additional / redundant alerts:

289

Redundant-share estimate:

48.4%

Estimated analyst workload:

49.75 hours

Assumption:

5 minutes per alert.

---

# Baseline Coverage

Suspicious events represented:

143 of 145

Suspicious scenarios represented:

6 of 6

Suspicious successful-authentication events explicitly detected:

0 of 2

The two missed suspicious events were successful authentications:

- SUS-02 `admin.backup`
- SUS-05 `payroll.manager`

---

# Baseline Noise Finding

The largest benign noise source was LEG-03.

LEG-03 produced:

142 alerts

This showed that the noise problem could not be explained only as an incorrect threshold.

The original architecture created repeated alerts for the same underlying operational behavior.

---

# Baseline Engineering Conclusion

The detector had broad failure-event visibility but poor analyst usability.

Primary weaknesses:

- excessive event-level alerting;
- duplicate signaling;
- benign service-account noise;
- limited behavioral context;
- missing success-after-failure correlation;
- significant analyst reconstruction burden.

---

# Phase 4 — V1 Tuning Proposal

The V1 proposal was documented before implementation.

Design goals:

- reduce redundant event-level alerts;
- create behavioral detections;
- preserve meaningful suspicious scenarios;
- explicitly detect suspicious successes;
- avoid broad exclusions and whitelists.

---

# V1 Detection Logic

## V1-01 — Rapid Repeated Authentication Failures

Trigger:

- same user;
- same source;
- at least 5 failures;
- within 10 minutes.

---

## V1-02 — Suspicious Success After Failures

Trigger on successful authentication when:

- same user/source;
- at least 5 failures within 10 minutes;

or:

- account is privileged;
- at least 3 failures within 10 minutes.

---

## V1-03 — Password Spray

Trigger:

- one source;
- at least 5 distinct users;
- within 120 minutes.

---

## V1-04 — Distributed Targeting

Trigger:

- one user;
- failures from at least 3 distinct sources;
- within 60 minutes.

---

## V1-05 — Low-and-Slow Privileged Authentication

Trigger:

- privileged account;
- unfamiliar source;
- same user/source;
- at least 4 failures;
- within 120 minutes.

---

## V1-06 — Persistent Service Authentication Failure

Trigger:

- service account;
- same user/source;
- at least 3 failures;
- within 15 minutes.

---

# V1 Results

Total V1 alerts:

15

Rule distribution:

- V1-01: 3
- V1-02: 2
- V1-03: 6
- V1-04: 1
- V1-05: 2
- V1-06: 1

Known suspicious-only alerts:

14

Known benign-only alerts:

1

Estimated workload:

1.25 hours

---

# V1 Coverage

Suspicious events represented:

64 of 145

Benign events represented:

3 of 855

Suspicious scenarios represented:

6 of 6

Suspicious scenarios missed:

0

Suspicious successful-authentication events explicitly detected:

2 of 2

---

# V1 Engineering Conclusion

V1 significantly improved signal per analyst alert.

However, event-level representation decreased from:

143 of 145

to:

64 of 145

This was accepted as an explicit tradeoff rather than hidden.

Scenario coverage remained:

6 of 6

V1 also restored visibility into the two suspicious successful authentications.

---

# Decision Point #1 — Familiar/Internal Source Suppression

The SOC Manager proposed suppressing familiar internal addresses because they were likely employee mistakes.

The proposed shortcut was evaluated against the frozen dataset.

Estimated effect:

- V1 alerts could decrease from 15 to approximately 12;
- only 1 benign alert would be removed;
- 2 suspicious alerts from SUS-05 could also be removed;
- scenario coverage could decrease from 6 of 6 to 5 of 6.

Decision:

Reject blanket familiar/internal suppression.

Engineering principle:

`familiar does not equal trusted`

A compromised workstation, stolen credentials, or lateral movement may originate from familiar infrastructure.

---

# Phase 5 — V2 Correlation Design

V1 improved detection quality but still generated multiple alerts for some underlying attack sequences.

V2 was designed as a correlation layer.

V2 does not independently inspect raw authentication events.

It consumes V1 alerts.

---

# V2 Logic

## V2-01 — Authentication Attack Sequence

Correlates:

- V1-01
- V1-02
- V1-05

Relationship:

same primary user and source.

Correlation window:

overlap or next signal beginning within 120 minutes.

---

## V2-02 — Password Spray Campaign

Correlates related V1-03 source-level spray alerts into campaign cases.

---

## V2-03 — Distributed Targeting

Groups V1-04 signals by targeted user.

---

## V2-04 — Persistent Service Authentication Case

Groups V1-06 signals by service user/source.

---

# V2 Results

V1 alerts consumed:

15

V2 cases:

7

Case distribution:

- V2-01: 4
- V2-02: 1
- V2-03: 1
- V2-04: 1

Reduction from V1:

53.3%

Estimated analyst workload:

0.58 hours

---

# V2 Coverage

Suspicious-only cases:

6

Benign-only cases:

1

Mixed cases:

0

Suspicious events represented:

64 of 145

Suspicious scenarios represented:

6 of 6

Suspicious successful-authentication events preserved:

2 of 2

---

# V2 Engineering Conclusion

V2 improved:

- correlation;
- analyst presentation;
- campaign grouping;
- reduction of repeated investigation effort.

V2 did not increase raw-event detection sensitivity.

Important architectural principle:

`If V1 produces no signal, V2 has nothing to correlate.`

---

# V2 STOP Boundary

After V2 evaluation:

- Original logic was preserved;
- V1 logic was preserved;
- V2 logic was preserved;
- V2 evaluation results were documented;
- no further tuning was performed before Purple Team testing.

This ensured subsequent adversarial testing evaluated a frozen detection strategy.

---

# Decision Point #2 — Purple Team Blind Spot

Purple Team testing showed that the detector caught straightforward repeated-failure activity.

A second simulated attacker distributed activity across:

- multiple usernames;
- multiple source addresses;
- longer time intervals.

No individual user/source relationship exceeded the existing thresholds.

Expected alert:

Did not fire.

---

# Purple Team Analysis

Detector assumption:

Meaningful attacks would eventually concentrate around a measurable user, source, or time-window relationship.

Attacker response:

Spread activity so that no one relationship accumulated enough evidence.

Classification:

Primary:

Detection architecture / analytical perspective gap.

Secondary:

Tuning limitation.

Not primarily:

Telemetry failure.

The raw events existed.

---

# Purple Team Decision

Do not immediately modify V2.

Preserve the miss.

Evaluate a complementary campaign-level detection using a different analytical perspective.

---

# Phase 7 — Adversarial Testing

A separate adversarial dataset was created.

Original 1,000-event dataset:

Unchanged.

Adversarial events:

25

Variations:

4

---

# AT-01 — Threshold Skimming

Behavior:

- 4 failures;
- one non-privileged user;
- one unfamiliar source;
- approximately 9 minutes.

Expected:

Missed.

Actual:

- V1 alerts: 0
- V2 cases: 0

Classification:

Missed.

---

# AT-02 — Distributed Many-to-Many Campaign

Behavior:

- 12 failures;
- 6 users;
- 4 unfamiliar sources;
- approximately 4 hours.

Constraints intentionally kept every V1 relationship below threshold.

Actual:

- V1 alerts: 0
- V2 cases: 0

Classification:

Missed.

Primary finding:

Campaign-level architecture gap.

---

# AT-03 — Familiar-Source Failures Followed by Success

Behavior:

- 4 failures;
- 1 success;
- same non-privileged user;
- same familiar source.

Actual:

- V1 alerts: 0
- V2 cases: 0

Classification:

Missed.

Primary finding:

Sub-threshold suspicious-success gap.

---

# AT-04 — Privileged Low-and-Slow Control

Behavior:

- privileged user `sec.admin`;
- unfamiliar source `203.0.113.88`;
- 4 failures;
- 30-minute spacing;
- all within 120 minutes.

V1 result:

`ADV-V1-0001`

Rule:

`V1-05`

V2 result:

`ADV-V2C-0001`

Case type:

`V2-01`

Classification:

Detected.

---

# Adversarial Testing Conclusion

Detected variations:

1 of 4

Missed:

3 of 4

The adversarial dataset was intentionally evasive.

The resulting 25% variation-detection rate must not be interpreted as a production detection rate.

Primary lesson:

The tuned detector has meaningful boundaries, and those boundaries must remain documented.

---

# Phase 8 — Alert Quality

A final analyst-facing alert structure was designed.

The alert includes:

- behavioral title;
- case ID;
- severity;
- user;
- privilege context;
- source;
- source familiarity;
- timeframe;
- failure count;
- related users;
- related sources;
- successful-authentication context;
- plain-language firing reason;
- recommended initial checks.

---

# 60-Second Analyst Test

The alert was reviewed from the perspective of an analyst who did not build the detector.

Result:

PASS WITH REVISIONS

The analyst could determine within approximately 60 seconds:

- why the alert fired;
- whether privilege was involved;
- whether authentication succeeded;
- the source involved;
- scale and duration;
- initial investigation path.

---

# Analyst-Test Revisions

The final alert design was revised to:

- change the privileged successful-authentication example from High to Critical;
- qualify source familiarity with historical context;
- promote destination/application/identity-provider context when telemetry supports it;
- move internal rule identifiers below the analyst-facing explanation.

No V1 or V2 detection logic changed.

---

# Phase 9 — Production Readiness

A Detection Operations Plan was created.

It defined:

- owner;
- review frequency;
- health metrics;
- change triggers;
- data dependencies;
- failure conditions;
- exception approval;
- exception expiration;
- versioning;
- rollback;
- analyst feedback;
- false-negative review;
- retirement criteria.

---

# Detection Drift Analysis

Detection performance may change because of:

- workforce changes;
- remote-work changes;
- VPN changes;
- identity-provider changes;
- MFA changes;
- passwordless authentication;
- service-account changes;
- cloud migration;
- network redesign;
- schema changes;
- source-familiarity drift;
- threshold drift;
- attacker tradecraft;
- analyst behavior;
- business-process changes.

Key conclusion:

A technically unchanged rule can become operationally poor if the environment changes around it.

---

# Phase 10 — Management Decision

The Detection Engineering Decision Brief recommended:

Advance V1/V2 to production-readiness review with documented residual risk.

Do not:

- restore the original alert-per-event operating model;
- broadly suppress familiar/internal sources.

Continue:

- health measurement;
- false-negative tracking;
- analyst feedback;
- adversarial testing;
- drift review;
- complementary detection development.

---

# Quantitative Final Comparison

| Metric | Original | V1 | V2 |
|---|---:|---:|---:|
| Analyst units | 597 alerts | 15 alerts | 7 cases |
| Estimated workload | 49.75h | 1.25h | 0.58h |
| Suspicious scenarios represented | 6/6 | 6/6 | 6/6 |
| Suspicious events represented | 143/145 | 64/145 | 64/145 |
| Suspicious successful authentications detected | 0/2 | 2/2 | 2/2 |
| Benign analyst units | 248 | 1 | 1 |

---

# Final Engineering Assessment

Ticket #008 achieved a substantial reduction in analyst workload while preserving the six original suspicious scenarios.

Original to V1:

597 alerts → 15 alerts

Original to V2:

597 alerts → 7 cases

Suspicious success visibility:

0 of 2 → 2 of 2

The primary cost was lower event-level representation.

The primary unresolved architectural gap is:

distributed many-user/many-source authentication activity that remains below existing entity and timing thresholds.

---

# Current Known Residual Risks

Known residual risks include:

- threshold skimming;
- distributed many-user/many-source attacks;
- sub-threshold suspicious successes;
- attacks visible only over broader historical windows;
- V2 dependence on V1 signal generation;
- telemetry degradation;
- future detection drift.

---

# Current Engineering Position

V1 should remain the behavioral detection layer.

V2 should remain the correlation layer.

Familiar/internal sources should remain contextual signals rather than blanket exclusion criteria.

Major new analytical problems should be addressed with complementary detections instead of continuously expanding V2.

---

# Evidence Preservation

The repository preserves:

- frozen dataset;
- ground truth;
- original detector logic;
- baseline output;
- baseline scoring;
- V1 proposal;
- V1 specification;
- V1 implementation;
- V1 output;
- V1 evaluation;
- V2 proposal;
- V2 specification;
- V2 implementation;
- V2 output;
- V2 evaluation;
- Purple Team analysis;
- adversarial dataset;
- adversarial harnesses;
- adversarial outputs;
- alert design;
- analyst usability test;
- operations plan;
- drift analysis;
- decision brief;
- false-negative register;
- detection change record;
- measurement summary.

---

# Notebook Conclusion

The strongest result of Ticket #008 is not simply that alert volume was reduced.

The engineering improvement was the transition from:

event-level alert accumulation

to:

behavioral detection and correlated analyst cases.

The work also demonstrated that tuning is not complete when alert volume falls.

A detection must also be tested for:

- missed attack behavior;
- usability;
- architectural assumptions;
- telemetry dependency;
- drift;
- rollback;
- residual risk.

Ticket #008 therefore treats detection engineering as a measurable lifecycle rather than a one-time threshold adjustment.

---

# Status

Engineering Notebook completed.
