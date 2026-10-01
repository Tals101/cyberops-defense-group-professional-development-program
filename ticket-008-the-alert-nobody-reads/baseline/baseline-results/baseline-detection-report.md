# Ticket #008 - Baseline Detection Report

## Executive Summary

The original authentication detector was evaluated against the frozen 1,000-event authentication dataset.

The detector generated 597 alerts from 308 unique authentication events.

Although the detector provided broad visibility into suspicious authentication activity, its operational efficiency was poor. Nearly half of all alerts were additional alerts generated for events that had already produced another alert, and 41.5% of all alerts were associated with known benign activity.

The detector also failed to alert on two suspicious successful authentications that followed sequences of failed authentication attempts.

The baseline therefore demonstrates two simultaneous problems:

1. excessive low-value and redundant alert volume; and
2. insufficient correlation of authentication behavior into meaningful security sequences.

The problem is not adequately explained by saying that the threshold is too low.

---

## Dataset

Total authentication events:

1,000

Ground-truth composition:

- 855 benign events
- 145 suspicious events

The dataset includes normal authentication, ordinary password mistakes, stale service credentials, unfamiliar legitimate sources, privileged administration, brute force, password spraying, low-and-slow activity, familiar-source compromise, and distributed authentication activity.

---

## Total Alerts

The original detector generated:

597 alerts

Rule contribution:

| Rule | Description | Alerts |
|---|---|---:|
| BASE-R1 | Failed Authentication | 308 |
| BASE-R2 | Repeated Failures | 119 |
| BASE-R3 | Unfamiliar Source Failure | 139 |
| BASE-R4 | Privileged Account Failure | 31 |

---

## Unique Entities Alerted

Unique users alerted:

36

Unique sources alerted:

30

Unique authentication events producing at least one alert:

308

---

## Repeat and Redundant Alerts

Total alerts:

597

Unique alerted events:

308

Additional alerts tied to events that had already generated an alert:

289

Redundancy rate:

48.4%

This means almost half of the detector's alert workload came from multiple rules independently alerting on authentication events that were already represented by another alert.

One event could produce several alerts describing overlapping aspects of the same behavior.

---

## Alerts Associated With Benign Activity

Benign alerts:

248

Percentage of all alerts associated with benign scenarios:

41.5%

Benign events that generated at least one alert:

165 of 855

Benign event alert rate:

19.3%

### Benign Scenario Contribution

| Scenario | Description | Events Alerted | Alerts |
|---|---|---:|---:|
| LEG-01 | Normal Business Authentication | 20 | 20 |
| LEG-02 | Ordinary Password Mistakes | 60 | 60 |
| LEG-03 | Stale Service Credentials | 72 | 142 |
| LEG-04 | Benign Unfamiliar Source | 8 | 16 |
| LEG-05 | Legitimate Privileged Administration | 5 | 10 |

The largest single benign source of alert volume was stale service credentials.

LEG-03 generated 142 alerts from only 72 authentication events.

That represents approximately 23.8% of every alert produced by the baseline detector.

---

## Alerts Associated With Suspicious Activity

Suspicious alerts:

349

Suspicious events generating at least one alert:

143 of 145

Suspicious event detection rate:

98.6%

All six suspicious scenarios generated at least one alert.

Therefore:

Suspicious scenarios completely missed:

0

However, scenario-level coverage overstates the quality of detection because it does not determine whether the detector identified the most important event within each attack sequence.

---

## Suspicious Scenario Results

| Scenario | Events | Alerted Events | Missed Events | Alerts |
|---|---:|---:|---:|---:|
| SUS-01 | 35 | 35 | 0 | 103 |
| SUS-02 | 9 | 8 | 1 | 30 |
| SUS-03 | 60 | 60 | 0 | 120 |
| SUS-04 | 18 | 18 | 0 | 54 |
| SUS-05 | 13 | 12 | 1 | 22 |
| SUS-06 | 10 | 10 | 0 | 20 |

---

## Missed Suspicious Activity

Two suspicious events did not generate alerts.

They occurred in:

- SUS-02 - Failures Followed by Privileged Success
- SUS-05 - Compromised Familiar Source

In both scenarios, the missed event was the successful authentication that followed the failed attempts.

The baseline detector only evaluates failed authentication events.

Therefore it detects the attempts leading to the success but does not alert when authentication ultimately succeeds.

This is an important security limitation because a successful authentication following suspicious failures can represent the transition from attempted credential abuse to possible account compromise.

---

## Distributed Attack Coverage

SUS-03 and SUS-06 both produced alerts.

However, their detection was largely incidental to the detector alerting on individual failures and unfamiliar sources.

The baseline does not explicitly correlate:

- one source attacking many users; or
- many sources attacking one user.

Therefore the detector provides event visibility without clearly communicating the distributed attack pattern.

---

## Low-and-Slow Coverage

SUS-04 generated 54 alerts from 18 suspicious events.

The scenario remained visible because every failure independently generated alerts and the account was privileged and the source unfamiliar.

The detector does not explicitly identify the long-duration behavioral pattern.

This produces high alert volume without necessarily giving the analyst the context that makes the activity suspicious.

---

## Analyst Workload Estimate

For comparison purposes, the lab assumes five minutes of analyst effort per alert.

This is a measurement assumption and not a claim about actual production SOC handling time.

597 alerts x 5 minutes:

2,985 minutes

Estimated analyst workload:

49.75 hours

The same workload assumption will be applied to V1 so that the comparison remains consistent.

---

## Why Is the Detector Noisy?

The detector is noisy because several design characteristics combine.

### Event-Level Alerting

Every failed authentication creates an alert regardless of surrounding context.

Routine mistakes and operational authentication failures therefore receive the same initial alert treatment as potentially malicious failures.

### Overlapping Rules

The same event may independently trigger:

- failed authentication;
- repeated failures;
- unfamiliar-source failure; and
- privileged-account failure.

This creates multiple alerts without creating multiple security incidents.

### Lack of Incident Grouping

Repeated failures continue generating alerts after the threshold has already been reached.

The detector does not consolidate related activity into an investigation unit.

### Context Used as Independent Alert Conditions

Unfamiliar-source and privileged-account attributes are useful risk context.

The baseline converts them into additional alerts instead of using them to improve the meaning or priority of an existing detection.

### Benign Repetitive Activity

Stale service credentials create behavior similar to automation or password guessing.

The detector cannot distinguish this pattern from an attack and repeatedly alerts on it.

### No Success Correlation

The detector does not examine successful authentication after suspicious failures.

Consequently, it can generate numerous alerts during attempted access while failing to emphasize the moment an attacker may actually gain access.

### Weak Behavioral Aggregation

Distributed and low-and-slow activity is represented as many individual alerts instead of being identified as a larger authentication pattern.

---

## What 597 Alerts Actually Means

The alert count demonstrates substantial operational workload.

It does not mean there were 597 independent security incidents.

Only 308 authentication events produced those 597 alerts, and many related events belong to the same behavioral scenario.

---

## Baseline Conclusion

The detector has strong event-level sensitivity but poor operational signal quality.

It is simultaneously:

- generating large quantities of benign alerts;
- producing substantial duplicate alert volume;
- failing to correlate related behavior;
- providing limited context for analyst decisions; and
- missing suspicious successful authentication transitions.

The baseline therefore requires improvement, but simply raising a threshold would not address the underlying problems.

The next phase must determine which alert volume can be safely reduced while preserving or improving visibility into meaningful authentication attacks.
