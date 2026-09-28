# Ticket #008 - Noise Analysis

## Purpose

Identify the major causes of baseline authentication alert volume and determine which noise may be reduced without creating unacceptable detection blind spots.

---

## Baseline Volume

Total authentication events:

1,000

Total alerts:

597

Unique authentication events producing alerts:

308

Additional or redundant alerts:

289

Redundancy rate:

48.4%

Benign alerts:

248

Benign-alert share:

41.5%

---

## Major Noise Sources

### 1. Cross-Rule Alert Duplication

Additional alerts beyond the first alert associated with an authentication event:

289

Percentage of total alert volume:

48.4%

This is the largest cross-cutting operational problem.

The additional alerts arise because several rules can independently fire on the same authentication event.

This category overlaps with both benign and suspicious scenarios and therefore must not be added to the scenario percentages below.

### 2. Stale Service Credentials - LEG-03

Authentication events:

72

Alerts:

142

Percentage of total detector alerts:

approximately 23.8%

Classification:

Benign

Cause:

A service account repeatedly authenticates with outdated credentials.

Each failure creates a base alert, and after the repeated-failure condition is reached the same activity creates additional alerts.

Security consideration:

The account should not simply be whitelisted. Repeated service-account failures could also indicate a credential problem, misconfiguration, unauthorized use, or attack activity.

### 3. Ordinary Password Mistakes - LEG-02

Authentication events:

90

Failed events alerted:

60

Alerts:

60

Percentage of total alerts:

approximately 10.1%

Classification:

Benign

Cause:

Users make two ordinary password mistakes and then successfully authenticate.

Security consideration:

The successful login provides context that may help distinguish ordinary retry behavior, but a failure-then-success sequence can also occur during credential compromise.

The behavior should therefore be correlated rather than blindly suppressed.

### 4. Normal Business Authentication Failures - LEG-01

Alerts:

20

Percentage of total alerts:

approximately 3.4%

Classification:

Benign

Cause:

Isolated authentication failures occurring within otherwise normal business activity.

Security consideration:

A single failure has weak security significance but may become meaningful when combined with other risk factors or later activity.

### 5. Benign Unfamiliar Sources - LEG-04

Failed authentication events:

8

Alerts:

16

Percentage of total alerts:

approximately 2.7%

Classification:

Benign

Cause:

Each failed authentication creates both:

- Failed Authentication
- Unfamiliar Source Failure

Security consideration:

Unfamiliar source is useful risk context but should not automatically be treated as proof of malicious activity.

SUS-02, SUS-03, SUS-04, and SUS-06 demonstrate why unfamiliar-source information still matters.

### 6. Legitimate Privileged Administration - LEG-05

Failed authentication events:

5

Alerts:

10

Percentage of total alerts:

approximately 1.7%

Classification:

Benign

Cause:

Each privileged failure creates both:

- Failed Authentication
- Privileged Account Failure

Security consideration:

Privileged-account activity cannot safely be excluded because the potential impact of credential compromise is high.

Privileged status should influence risk and priority rather than automatically creating a second independent alert.

---

## Noise That Can Potentially Be Reduced Safely

### Duplicate Alerts

Multiple rule hits describing the same authentication event can potentially be consolidated into one enriched alert.

This reduces analyst workload without discarding the underlying telemetry.

### Repeated Alerts From One Continuing Pattern

Once related failures form a recognizable behavior, subsequent events can potentially update or escalate the same detection rather than opening another independent alert every time.

### Context-Only Alerts

Privileged status and source familiarity can potentially become alert context or severity modifiers instead of generating additional independent alerts.

### Routine Retry Sequences

Ordinary user failures followed quickly by successful authentication can potentially be treated differently from sustained failure patterns.

Any such logic must retain visibility when the sequence includes risk indicators suggesting credential compromise.

---

## Apparently Noisy Behavior That Still Deserves Visibility

### Service Account Failures

The LEG-03 pattern is benign in this dataset but resembles automated authentication abuse.

Suppressing the account entirely would create a blind spot.

### Privileged Authentication Failures

Legitimate administrative mistakes generate noise, but privileged authentication attacks have higher potential impact.

### Unfamiliar Sources

LEG-04 proves unfamiliar does not equal malicious.

However, several suspicious scenarios also rely on unfamiliar infrastructure.

### Familiar Sources

SUS-05 demonstrates that familiar sources cannot be automatically trusted.

### Low-Rate Authentication Failures

SUS-04 demonstrates that low-and-slow activity may avoid short-window thresholds.

### Small Counts Across Distributed Entities

SUS-03 and SUS-06 demonstrate that individually ordinary-looking events may become suspicious only after cross-entity aggregation.

---

## Why Analysts May Start Ignoring the Detector

Analysts repeatedly receive alerts that:

- describe routine behavior;
- duplicate another alert they have already seen;
- provide insufficient behavioral context;
- do not clearly identify whether the activity is escalating;
- require additional manual lookup before a decision can be made;
- treat risk attributes as separate alerts instead of useful context; and
- emphasize individual failures while failing to highlight successful authentication after suspicious failures.

Over time, repeated low-value alerts reduce confidence that opening another alert will produce useful information.

This creates an alert-fatigue risk.

---

## Root Cause

The detector's primary problem is not simply threshold selection.

The root cause is the combination of:

1. event-level alerting;
2. overlapping rules;
3. insufficient correlation;
4. weak entity aggregation;
5. lack of state or incident grouping;
6. missing success-after-failure logic; and
7. insufficient distinction between risk context and independent alert conditions.

---

## Current Decision

No suppression, exception, threshold change, or whitelist has been approved yet.

The next step is to review representative alerts from the analyst's perspective before designing Tuning Proposal V1.
