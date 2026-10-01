# Ticket #008 — Measurement Summary

## Purpose

Provide a concise quantitative comparison of the Original, V1, and V2 authentication detection strategies.

This summary focuses on:

- alert or case volume;
- analyst workload;
- benign noise;
- suspicious coverage;
- successful-authentication visibility;
- correlation improvement;
- adversarial-test outcomes.

The measurements should be interpreted together rather than using alert count alone as a measure of detection quality.

---

# Frozen Dataset

Total authentication events:

1,000

Known benign events:

855

Known suspicious events:

145

Suspicious scenarios:

6

Suspicious successful-authentication events:

2

---

# Primary Comparison

| Metric | Original | V1 | V2 |
|---|---:|---:|---:|
| Analyst units | 597 alerts | 15 alerts | 7 cases |
| Estimated workload | 49.75 hours | 1.25 hours | 0.58 hours |
| Known benign alerts / cases | 248 alerts | 1 alert | 1 case |
| Known suspicious alerts / cases | 349 alerts | 14 alerts | 6 cases |
| Suspicious scenarios represented | 6/6 | 6/6 | 6/6 |
| Suspicious scenarios missed | 0 | 0 | 0 |
| Suspicious events represented | 143/145 | 64/145 | 64/145 |
| Suspicious successful authentications explicitly detected | 0/2 | 2/2 | 2/2 |
| Duplicate / redundant / consolidatable units | 289 | 8 | 0 identified after correlation |
| Password-spray analyst units | 120 baseline alerts | 6 source-level alerts | 1 campaign case |

---

# Alert / Case Volume Reduction

## Original to V1

Original:

597 alerts

V1:

15 alerts

Reduction:

582 alerts

Percentage reduction:

97.5%

Calculation:

`(597 - 15) / 597 × 100`

---

## V1 to V2

V1:

15 alerts

V2:

7 cases

Reduction:

8 analyst-facing units

Percentage reduction:

53.3%

Calculation:

`(15 - 7) / 15 × 100`

---

## Original to V2

Original:

597 alerts

V2:

7 cases

Reduction:

590 analyst-facing units

Percentage reduction:

98.8%

Calculation:

`(597 - 7) / 597 × 100`

---

# Estimated Analyst Workload

Lab assumption:

5 minutes per analyst unit.

## Original

597 × 5 minutes:

2,985 minutes

49.75 hours

## V1

15 × 5 minutes:

75 minutes

1.25 hours

## V2

7 × 5 minutes:

35 minutes

Approximately 0.58 hours

---

# Estimated Workload Reduction

## Original to V1

49.75 hours → 1.25 hours

Reduction:

48.50 hours

Approximately:

97.5%

---

## V1 to V2

1.25 hours → 0.58 hours

Reduction:

approximately 0.67 hours

Approximately:

53.6%

The small difference from the 53.3% unit-count reduction results from rounding 35 minutes to 0.58 hours.

---

## Original to V2

49.75 hours → 0.58 hours

Reduction:

approximately 49.17 hours

Approximately:

98.8%

---

# Benign Noise

## Original

Known benign alerts:

248

Known benign share of alerts:

41.5%

The stale service-credential scenario alone produced:

142 alerts

---

## V1

Known benign-only alerts:

1

Benign events represented:

3 of 855

Benign-only alert share:

6.7%

---

## V2

Known benign-only cases:

1

Benign events represented:

3 of 855

Benign-only case share:

14.3%

Important interpretation:

The percentage increased from V1 to V2 because the denominator decreased from 15 alerts to 7 cases.

The absolute benign analyst-unit count remained:

1

Therefore the percentage alone should not be interpreted as increased benign noise.

---

# Suspicious Scenario Coverage

Original:

6 of 6

V1:

6 of 6

V2:

6 of 6

No original suspicious scenario was lost during V1 tuning or V2 correlation.

---

# Suspicious Event Representation

Original:

143 of 145 suspicious events

98.6%

V1:

64 of 145 suspicious events

44.1%

V2:

64 of 145 suspicious events

44.1%

This is an important tradeoff.

The tuned system intentionally represents suspicious behavior through grouped behavioral signals rather than alerting on nearly every suspicious event.

Scenario coverage remained 6 of 6, but event-level representation declined.

---

# Suspicious Successful-Authentication Coverage

Suspicious successful-authentication events in ground truth:

2

## Original

Explicitly detected:

0 of 2

## V1

Explicitly detected:

2 of 2

## V2

Preserved:

2 of 2

This is one of the most important coverage improvements.

The tuned strategy reduced overall alert volume while adding explicit visibility into the successful authentications most likely to require immediate investigation.

---

# Duplicate and Correlation Improvement

## Original

Additional or redundant alerts:

289

Redundant-share estimate:

48.4%

The analyst frequently had to manually determine whether multiple alerts described the same activity.

---

## V1

Alerts:

15

Consolidatable into V2 cases:

8 alerts beyond the final 7 cases

V1 substantially reduced duplication but still left correlation work.

---

## V2

Cases:

7

No additional consolidatable units were identified after V2 correlation in the frozen evaluation.

V2 therefore reduced the remaining manual correlation burden.

---

# Password-Spray Comparison

The suspicious password-spray scenario produced:

## Original

120 alerts

## V1

6 source-level alerts

## V2

1 Password Spray Campaign case

This illustrates the difference between:

- event-level alerting;
- behavioral alerting;
- campaign-level correlation.

---

# V1 Rule Distribution

V1 produced:

- V1-01: 3 alerts
- V1-02: 2 alerts
- V1-03: 6 alerts
- V1-04: 1 alert
- V1-05: 2 alerts
- V1-06: 1 alert

Total:

15 alerts

---

# V2 Case Distribution

V2 produced:

- V2-01 Authentication Attack Sequence: 4 cases
- V2-02 Password Spray Campaign: 1 case
- V2-03 Distributed Targeting: 1 case
- V2-04 Persistent Service Authentication Case: 1 case

Total:

7 cases

---

# Adversarial Test Measurements

Separate adversarial dataset:

25 suspicious events

Test variations:

4

## AT-01 — Threshold Skimming

Events:

4

V1 alerts:

0

V2 cases:

0

Result:

Missed

---

## AT-02 — Distributed Many-to-Many Campaign

Events:

12

V1 alerts:

0

V2 cases:

0

Result:

Missed

---

## AT-03 — Familiar-Source Failures Followed by Success

Events:

5

V1 alerts:

0

V2 cases:

0

Result:

Missed

---

## AT-04 — Privileged Low-and-Slow

Events:

4

V1 alerts:

1

V2 cases:

1

Result:

Detected

---

# Adversarial Test Summary

Variations tested:

4

Detected:

1

Missed:

3

Detection rate across these deliberately evasive test variations:

25%

This percentage should not be generalized as an overall production detection rate.

The adversarial set was intentionally designed to probe known boundaries and is not representative of normal authentication traffic.

---

# Measurement Interpretation

The strongest improvements were:

- 97.5% reduction in analyst units from Original to V1;
- 98.8% reduction from Original to V2;
- suspicious scenario coverage preserved at 6 of 6 on the frozen baseline dataset;
- suspicious successful-authentication visibility improved from 0 of 2 to 2 of 2;
- campaign-level correlation reduced remaining V1 alerts from 15 to 7 cases;
- password-spray workload collapsed from 120 baseline alerts to 1 V2 campaign case.

The primary cost was:

- suspicious event-level representation decreased from 143 of 145 to 64 of 145.

The primary residual risk demonstrated through adversarial testing was:

- behavior that remains below existing user/source/time-window thresholds.

---

# Final Measurement Conclusion

Ticket #008 produced a substantial improvement in signal per analyst attention.

The tuned strategy should not be described as universally more sensitive than the Original detector.

Instead, the evidence supports the following conclusion:

V1/V2 materially reduced noise, duplication, and analyst workload while preserving all six original suspicious scenarios and adding explicit suspicious-success visibility.

The tradeoff is lower event-level representation and documented adversarial blind spots that require complementary detection strategies.

---

# Status

Measurement Summary completed.

Original, V1, V2, and adversarial-test measurements are consolidated in one quantitative artifact.
