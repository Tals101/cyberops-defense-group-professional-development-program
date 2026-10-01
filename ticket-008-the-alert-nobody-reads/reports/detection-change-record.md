# Ticket #008 — Detection Change Record

## Purpose

Document the evolution of the authentication detection from the Original detector through V1 and V2.

For each version, this record captures:

- detection logic;
- reason for change;
- expected effect;
- observed effect;
- coverage gained;
- coverage lost or exposed;
- rollback position.

This record is intended to support engineering review, auditability, and future tuning.

---

# Version Summary

| Version | Primary Purpose | Analyst Units | Estimated Workload | Suspicious Scenarios Represented | Suspicious Successes Explicitly Detected |
|---|---|---:|---:|---:|---:|
| Original | Broad event-level authentication detection | 597 alerts | 49.75 hours | 6/6 | 0/2 |
| V1 | Behavioral detection and threshold tuning | 15 alerts | 1.25 hours | 6/6 | 2/2 |
| V2 | Case-level correlation of V1 alerts | 7 cases | 0.58 hours | 6/6 | 2/2 |

The workload values use the lab assumption of 5 minutes per alert or case.

---

# Original Detector

## Version

Original / Baseline

## Logic

The original detector generated alerts using broad authentication-event logic.

Primary behaviors included:

- failed authentication;
- repeated failures for the same user;
- unfamiliar-source failures;
- privileged-account failures.

A single authentication event could contribute to multiple alerts.

The original design did not explicitly correlate successful authentication after suspicious failures.

---

## Reason for Original Design

The original detector prioritized broad visibility.

It was effective at surfacing authentication failures but did not sufficiently control duplication or analyst workload.

---

## Observed Effect

Baseline results:

- 1,000 authentication events;
- 597 alerts;
- 308 unique alerting events;
- 248 known benign alerts;
- 349 alerts associated with suspicious activity;
- 289 duplicate, redundant, or additional alerts;
- approximately 49.75 analyst-hours;
- 143 of 145 suspicious events represented;
- 6 of 6 suspicious scenarios represented;
- 0 of 2 suspicious successful-authentication events explicitly detected.

---

## Coverage Strengths

The original detector provided broad event-level visibility.

It represented nearly all suspicious failure events in the frozen dataset.

It detected activity associated with all six suspicious scenarios.

---

## Coverage Weaknesses

The original detector:

- fragmented related behavior into separate alerts;
- generated substantial benign noise;
- produced many redundant alerts;
- forced the analyst to perform manual correlation;
- did not explicitly detect the two suspicious successful authentications.

---

## Operational Problem

The detector produced too much output relative to analyst attention.

The primary problem was not simply a low threshold.

The larger issue was poor signal organization and excessive event-level alerting.

---

## Rollback Position

The Original detector remains preserved for historical comparison.

Rollback to the Original detector is not recommended under normal conditions because doing so would restore the high-noise operating model.

It may still be used as a temporary diagnostic comparison if future tuning causes unexpected loss of visibility.

---

# V1 Detector

## Version

V1

## Reason for Change

V1 was introduced to improve signal quality without disabling authentication monitoring.

The design goals were to:

- reduce event-level noise;
- reduce duplicate alerts;
- detect meaningful authentication behaviors;
- detect suspicious successful authentications;
- preserve meaningful attack coverage;
- avoid broad whitelisting or familiar-source suppression.

---

## V1 Logic

### V1-01 — Rapid Repeated Authentication Failures

Trigger when:

- same user;
- same source;
- at least 5 failures;
- within 10 minutes.

The rule alerts once per user/source relationship.

---

### V1-02 — Suspicious Success After Failures

Trigger when a successful authentication follows recent failures for the same user/source.

Conditions:

- at least 5 failures within 10 minutes;

or

- privileged account with at least 3 failures within 10 minutes.

This rule explicitly preserves successful-authentication context.

---

### V1-03 — Password Spray

Trigger when:

- one source;
- targets at least 5 distinct users;
- within 120 minutes.

---

### V1-04 — Distributed Targeting

Trigger when:

- one user;
- receives failures from at least 3 distinct sources;
- within 60 minutes.

---

### V1-05 — Low-and-Slow Privileged Authentication

Trigger when:

- account is privileged;
- source is unfamiliar;
- same user/source;
- at least 4 failures;
- within 120 minutes.

---

### V1-06 — Persistent Service Authentication Failure

Trigger when:

- service account;
- same user/source;
- at least 3 failures;
- within 15 minutes.

---

## Expected Effect

Expected improvements:

- major alert-volume reduction;
- less benign noise;
- fewer duplicate alerts;
- improved behavioral meaning;
- explicit successful-authentication detection;
- preserved visibility into privileged and distributed attacks.

Expected cost:

- lower event-level representation;
- possible threshold-evasion gaps;
- continued need for correlation between related alerts.

---

## Observed Effect

V1 results:

- 15 alerts;
- 14 suspicious-only alerts;
- 1 benign-only alert;
- approximately 1.25 analyst-hours;
- 64 of 145 suspicious events represented;
- 3 of 855 benign events represented;
- 6 of 6 suspicious scenarios represented;
- 0 suspicious scenarios missed;
- 2 of 2 suspicious successful-authentication events explicitly detected.

---

## Coverage Gained

V1 gained:

- explicit success-after-failure detection;
- clearer password-spray visibility;
- distributed-targeting visibility;
- privileged low-and-slow detection;
- better service-account grouping;
- much stronger signal-per-alert.

---

## Coverage Reduced

Event-level representation decreased:

- Original: 143 of 145 suspicious events;
- V1: 64 of 145 suspicious events.

This was an intentional consequence of grouping and threshold-based behavioral detection.

The reduction does not mean the six original suspicious scenarios were lost.

All six remained represented.

---

## Blind Spots Exposed

Later adversarial testing confirmed V1 can miss:

- threshold-skimming behavior;
- distributed many-user/many-source campaigns;
- sub-threshold suspicious successes from familiar sources;
- activity outside defined correlation windows.

---

## Rollback Position

If V1 produces unacceptable false positives, misses known required scenarios, or becomes incompatible with telemetry, rollback should restore the previous validated detection version while the problem is investigated.

Rollback to the Original detector should be temporary and should not be treated as the desired long-term state.

---

# V2 Correlation Layer

## Version

V2

## Reason for Change

V1 substantially reduced noise but still produced multiple alerts that could describe one underlying attack.

V2 was introduced to reduce manual analyst correlation.

V2 does not replace V1 detection logic.

It consumes V1 alerts and groups them into behavioral cases.

---

## V2 Logic

### V2-01 — Authentication Attack Sequence

Correlates:

- V1-01;
- V1-02;
- V1-05.

Primary relationship:

- same user;
- same source.

Signals are grouped when their time ranges overlap or when the next signal begins within 120 minutes of the existing sequence.

---

### V2-02 — Password Spray Campaign

Correlates related V1-03 password-spray alerts.

Signals are merged when their time ranges overlap or remain within the defined campaign correlation window.

---

### V2-03 — Distributed Targeting

Groups V1-04 alerts by targeted user.

---

### V2-04 — Persistent Service Authentication Case

Groups V1-06 alerts by service user/source relationship.

---

## Expected Effect

Expected improvements:

- fewer analyst-facing units;
- less duplicate investigation;
- campaign-level context;
- preserved V1 provenance;
- preserved suspicious-success information;
- faster analyst comprehension.

Expected limitation:

V2 cannot detect malicious raw events that do not first create a V1 alert.

---

## Observed Effect

V2 results:

- 7 cases created from 15 V1 alerts;
- 53.3% reduction from V1 alert count;
- 6 suspicious-only cases;
- 1 benign-only case;
- 0 mixed cases;
- approximately 0.58 analyst-hours;
- 64 of 145 suspicious events represented;
- 6 of 6 suspicious scenarios represented;
- 2 of 2 suspicious successful-authentication events preserved.

---

## Coverage Gained

V2 improved:

- case-level correlation;
- password-spray campaign grouping;
- attack-sequence grouping;
- analyst comprehension;
- reduction of repeated investigation work.

V2 did not create new raw-event sensitivity.

---

## Coverage Lost

No original V1 scenario coverage was lost during V2 correlation.

V2 preserved:

- 6 of 6 suspicious scenarios;
- 2 of 2 suspicious successful-authentication events.

However, V2 inherits all V1 false negatives.

---

## Architectural Limitation

V2 is a correlation layer.

If V1 produces no signal:

V2 has nothing to correlate.

This was confirmed during adversarial testing.

---

## Rollback Position

If V2 grouping causes:

- over-merging;
- broken correlation;
- incorrect case context;
- analyst confusion;
- loss of useful V1 distinctions;

the system can roll back to V1 alerts while preserving V1 detection coverage.

This is the preferred V2 rollback path.

---

# Manager Suppression Decision

## Proposed Change

Suppress or broadly exclude familiar internal addresses.

## Decision

Rejected.

## Reason

Testing demonstrated that malicious authentication activity can originate from familiar sources.

A compromised workstation or stolen session context can remain internal or familiar.

Familiarity is therefore contextual evidence, not proof of legitimacy.

---

## Expected Effect of Suppression

Estimated V1 impact:

- 15 alerts could fall to approximately 12;
- only 1 benign alert would be removed;
- 2 suspicious alerts associated with the familiar-source compromise scenario could also be removed;
- suspicious scenario coverage could fall from 6 of 6 to 5 of 6.

---

## Final Position

No blanket familiar-source suppression was implemented.

---

# Purple Team / Adversarial Findings

Adversarial testing did not immediately trigger new V1 or V2 logic changes.

This was intentional.

Confirmed misses included:

- AT-01 threshold skimming;
- AT-02 distributed many-user/many-source activity;
- AT-03 familiar-source sub-threshold failure-to-success activity.

Detected control case:

- AT-04 privileged low-and-slow activity.

---

# Post-Adversarial Decision

Do not continuously expand V2 to handle every observed attack pattern.

Use complementary detections when a different analytical perspective is required.

Priority complementary area:

Distributed many-user/many-source authentication campaigns.

---

# Alert Presentation Revision

Following the analyst usability test, the analyst-facing alert design was revised.

Changes included:

- privileged successful-authentication example severity changed from High to Critical;
- source familiarity qualified with historical context;
- destination/application/identity-provider context promoted when available;
- internal rule identifiers moved below the plain-language explanation.

These changes affected presentation only.

No V1 or V2 detection logic changed.

---

# Change Summary Table

| Change | Reason | Observed Effect | Coverage Gained | Coverage Lost / Exposed | Rollback |
|---|---|---|---|---|---|
| Original → V1 | Excessive noise, duplication, weak success context | 597 alerts → 15 alerts; workload 49.75h → 1.25h | Explicit suspicious success, behavioral detections, stronger analyst signal | Event-level suspicious representation decreased from 143/145 to 64/145; threshold blind spots exposed | Restore prior detector temporarily for diagnostic comparison if required |
| V1 → V2 | Analysts still had to correlate related behavioral alerts | 15 alerts → 7 cases; workload 1.25h → 0.58h | Case-level correlation, consolidated spray and attack sequences | No new sensitivity; inherits V1 misses | Return to V1 alert presentation |
| Familiar-source suppression proposal | Manager requested reduced internal-address noise | Not implemented | None | Testing showed possible loss of suspicious familiar-source activity | Not applicable |
| Alert presentation revision | Analyst usability test identified presentation ambiguity | Improved severity consistency and context | Faster analyst comprehension | No detection coverage change | Restore prior alert template if required |

---

# Current Approved State

Current operational design:

- V1 remains the behavioral detection layer;
- V2 remains the correlation layer;
- familiar/internal sources are not broadly suppressed;
- analyst-facing alerts use the revised Phase 8 design;
- known false negatives remain documented;
- complementary detections should be developed separately for major unresolved gaps.

---

# Status

Detection Change Record completed.

Original, V1, V2, the rejected familiar-source suppression proposal, adversarial findings, and alert-presentation revision are documented with rollback positions.

