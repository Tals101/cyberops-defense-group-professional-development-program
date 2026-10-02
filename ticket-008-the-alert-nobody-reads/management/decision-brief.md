# Ticket #008 — Detection Engineering Decision Brief

## Executive Decision

Proceed with the tuned V1/V2 authentication detection strategy for production-readiness review, with documented residual risk and continued development of complementary detections.

Do not restore the original alert-per-event approach and do not implement blanket suppression of familiar or internal sources.

---

## What Was Wrong?

The original authentication detector generated excessive alert volume and fragmented related activity into separate alerts.

Baseline results:

- 597 alerts from 1,000 authentication events;
- 248 known benign alerts;
- 289 duplicate, redundant, or additional alerts;
- approximately 49.75 analyst-hours at the lab assumption of 5 minutes per alert;
- two suspicious successful-authentication events were not explicitly detected.

The problem was not simply an overly low threshold.

The larger issue was that the detector generated event-level noise while forcing analysts to reconstruct attack behavior manually.

---

## What Changed?

V1 replaced the broad event-level approach with behavioral detections for:

- rapid repeated failures;
- suspicious success after failures;
- password spraying;
- distributed targeting;
- privileged low-and-slow activity;
- persistent service-account failures.

V2 then correlated related V1 alerts into analyst-facing cases.

No blanket familiar-source suppression or broad whitelisting was introduced.

---

## What Improved?

### Original

- 597 alerts
- approximately 49.75 analyst-hours
- 6 of 6 suspicious scenarios represented
- 143 of 145 suspicious events represented
- 0 of 2 suspicious successful authentications explicitly detected

### V1

- 15 alerts
- approximately 1.25 analyst-hours
- 6 of 6 suspicious scenarios represented
- 64 of 145 suspicious events represented
- 2 of 2 suspicious successful authentications explicitly detected

### V2

- 7 analyst-facing cases
- approximately 0.58 analyst-hours
- 6 of 6 original suspicious scenarios represented
- 64 of 145 suspicious events represented
- 2 of 2 suspicious successful authentications preserved
- password-spray activity consolidated from multiple signals into one campaign case

The reduction in unit count should not be interpreted as increased sensitivity. V2 improves correlation and analyst usability; it does not independently create new detection coverage.

---

## What Coverage Was Lost or Exposed?

Adversarial testing identified three important misses:

- threshold-skimming activity below individual rule thresholds;
- distributed many-user/many-source authentication activity;
- familiar-source failures followed by a sub-threshold successful authentication.

A privileged low-and-slow attack remained detectable.

These results demonstrate that V1/V2 should not be treated as the only authentication-abuse detection strategy.

---

## Why Familiar/Internal Suppression Was Rejected

Testing showed that a compromised familiar source can still produce malicious authentication activity.

Blanket familiar-address suppression would reduce alert volume but could also remove meaningful attack visibility.

Source familiarity should remain context, not trust.

---

## Remaining Risk

Known residual risk includes:

- threshold evasion;
- distributed credential attacks;
- sub-threshold suspicious successes;
- attacks visible only through broader historical analysis;
- dependence of V2 on V1 producing an initial signal;
- future detection drift caused by changes in workforce, infrastructure, identity technology, logging, and attacker behavior.

---

## How Will the Detection Be Monitored?

Detection health should be reviewed:

- monthly for operational health;
- quarterly for deeper coverage and drift review;
- immediately after major incidents, telemetry changes, or new blind spots.

Monitoring should include:

- alert and case volume;
- benign and suspicious dispositions;
- duplicate cases;
- successful-authentication detections;
- privileged-account detections;
- false-negative scenarios;
- analyst triage burden;
- data-quality failures;
- detection drift.

---

## Management Recommendation

Advance V1/V2 to production-readiness review with:

- version control and rollback;
- analyst feedback;
- false-negative tracking;
- periodic adversarial testing;
- detection-drift review;
- continued validation of telemetry and enrichment;
- development of complementary detection for distributed many-user/many-source campaigns and other documented blind spots.

The objective is not zero alerts or zero misses.

The objective is materially better signal per analyst attention while preserving known security coverage and making residual risk visible.
