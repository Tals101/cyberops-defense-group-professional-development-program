# Ticket #008 - Original to V1 Comparison

## Purpose

Compare the preserved original authentication detector with V1 using the exact same frozen 1,000-event authentication dataset.

No dataset changes were made between baseline and V1 testing.

---

# Executive Comparison

| Metric | Original | V1 |
|---|---:|---:|
| Total authentication events | 1,000 | 1,000 |
| Total alerts | 597 | 15 |
| Alert reduction | - | 582 |
| Alert reduction percentage | - | 97.5% |
| Benign-alert share | 41.5% | 6.7% benign-only |
| Suspicious scenarios detected | 6 of 6 | 6 of 6 |
| Suspicious scenarios completely missed | 0 | 0 |
| Suspicious success-after-failure transitions explicitly detected | 0 of 2 | 2 of 2 |
| Estimated analyst workload | 49.75 hours | 1.25 hours |

The workload estimate uses the same laboratory assumption of five minutes per alert for both versions.

---

# Alert Volume

## Original

597 alerts

## V1

15 alerts

## Change

582 fewer alerts

97.5% reduction

The reduction alone is not considered proof of improvement.

The security-coverage results must be considered at the same time.

---

# Alert Quality

## Original

Benign alerts:

248

Benign-alert share:

41.5%

## V1

Benign-only alerts:

1

Total V1 alerts:

15

Benign-only alert share:

6.7%

Fourteen of the fifteen V1 alerts contained suspicious activity.

The remaining alert represented the persistent stale service-account credential condition.

This means the noisy service-account behavior remained visible rather than being whitelisted or removed.

---

# Duplicate and Redundant Alerting

## Original

597 alerts were produced from only 308 authentication events.

Additional or redundant alerts:

289

Redundancy rate:

48.4%

Individual events could generate several independent alerts for:

- authentication failure;
- repeated failure;
- unfamiliar source;
- privileged account.

## V1

V1 uses investigation-oriented correlation.

Risk attributes are presented as context instead of automatically creating separate alerts.

V1 therefore substantially reduces the repeated presentation of the same underlying activity.

---

# Suspicious Scenario Retention

Original:

6 of 6 suspicious scenarios detected.

V1:

6 of 6 suspicious scenarios detected.

V1 therefore retained 100% scenario-level coverage on the frozen dataset.

Detected scenarios:

- SUS-01 - Concentrated Brute-Force Activity
- SUS-02 - Failures Followed by Privileged Success
- SUS-03 - Distributed Password Spray
- SUS-04 - Low-and-Slow Authentication Attack
- SUS-05 - Compromised Familiar Source
- SUS-06 - Distributed Attack Against One Account

---

# Success-After-Failure Visibility

## Original

The original detector missed the successful authentication event in:

- SUS-02
- SUS-05

Explicit suspicious success detections:

0 of 2

## V1

V1-02 explicitly detected both suspicious successful-authentication transitions.

Explicit suspicious success detections:

2 of 2

This is a security-coverage improvement, not merely an alert-volume improvement.

---

# Concentrated Brute Force

## Original

SUS-01 produced:

103 alerts

The analyst was required to reconstruct the attack from many overlapping alerts.

## V1

SUS-01 produced one correlated investigation alert through V1-01.

The investigation unit identifies the repeated authentication-failure pattern without producing an alert for every attempt.

---

# Distributed Password Spray

## Original

SUS-03 produced:

120 alerts

The detector did not explicitly describe the distributed password-spray pattern.

## V1

SUS-03 produced six V1-03 alerts.

Each alert represents one source reaching the five-distinct-user correlation threshold.

This is substantially less volume than the baseline and gives the analyst explicit cross-user context.

However, V1 still creates one investigation unit per qualifying source rather than one campaign-level alert for the entire distributed spray.

This remains a potential future improvement.

---

# Low-and-Slow Privileged Activity

## Original

SUS-04 produced:

54 alerts from 18 events.

Its visibility was largely the result of individual failure, unfamiliar-source, and privileged-account alerts.

## V1

SUS-04 remained detected through V1-05.

V1 explicitly identifies long-duration privileged authentication activity rather than relying on large quantities of individual event alerts.

---

# Compromised Familiar Source

## Original

SUS-05 produced:

22 alerts

The familiar source did not create unfamiliar-source alerts.

The successful authentication following the failures was missed.

## V1

SUS-05 remained visible through repeated-failure correlation.

V1 also explicitly detected the later successful authentication through V1-02.

This demonstrates that V1 does not treat a familiar source as automatically safe.

---

# Distributed Targeting

## Original

SUS-06 produced:

20 alerts

The baseline did not explicitly identify that several sources were targeting the same user.

## V1

V1-04 generated one investigation alert describing the many-sources-to-one-user pattern.

This improves analyst context while reducing alert volume.

---

# Service-Account Noise

## Original

LEG-03 generated:

142 alerts from 72 benign events.

## V1

LEG-03 generated:

1 persistent service-authentication-failure investigation alert.

The service account was not whitelisted.

The authentication problem remained visible while repetitive alerting was removed.

---

# Event-Level Visibility Tradeoff

The original detector generated alerts for 143 of 145 suspicious events.

V1 alerts referenced 64 of 145 suspicious events.

This difference must not be hidden.

V1 intentionally does not create an investigation alert for every suspicious event.

Instead, qualifying events are grouped into investigation units.

For example:

- SUS-01: 5 of 35 events represented
- SUS-02: 9 of 9 events represented
- SUS-03: 30 of 60 events represented
- SUS-04: 4 of 18 events represented
- SUS-05: 13 of 13 events represented
- SUS-06: 3 of 10 events represented

Therefore V1 sacrifices per-event alert representation in exchange for behavioral correlation.

The underlying telemetry remains available even when an individual event does not create an alert.

---

# Security Visibility Potentially Lost

V1 may be less sensitive to authentication activity that does not reach one of its correlation conditions.

Potential risks include:

- brute-force activity that remains below five failures in ten minutes;
- password spraying against fewer than five users;
- distributed targeting involving fewer than three sources;
- privileged low-and-slow activity extending beyond the 120-minute window;
- service-account abuse that closely resembles an existing persistent failure pattern.

These risks remain important even though all six seeded suspicious scenarios were retained.

The current dataset does not prove that V1 detects every possible variation of these attacks.

---

# Analyst Workload

Using the same five-minute-per-alert laboratory assumption:

## Original

597 alerts

49.75 estimated analyst hours

## V1

15 alerts

1.25 estimated analyst hours

Reduction:

48.5 estimated analyst hours

The workload improvement results primarily from correlation and grouping rather than blanket exclusions.

---

# Comparison Conclusion

V1 produced substantially fewer alerts while retaining all six known suspicious scenarios.

More importantly, V1 added security visibility that the baseline did not provide by explicitly detecting both suspicious successful-authentication transitions.

The result therefore shows more than simple alert suppression.

V1 produced fewer investigation units with substantially greater behavioral context.

The primary remaining concern is reduced per-event representation and the possibility that attacks staying below the defined correlation thresholds may be missed.

Those risks should remain documented and should be tested in future detector iterations.
