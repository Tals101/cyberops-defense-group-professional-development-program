# Ticket #008 - V1 Evaluation Report

## Evaluation Question

Did V1 make the authentication detector better, or merely quieter?

## Decision

V1 made the detector better on the frozen Ticket #008 dataset.

The conclusion is based on both operational and security measurements, not alert reduction alone.

---

# Evidence Supporting Improvement

## 1. Suspicious Scenario Coverage Was Preserved

Original:

6 of 6 suspicious scenarios detected.

V1:

6 of 6 suspicious scenarios detected.

No seeded suspicious scenario became completely invisible.

---

## 2. Important Security Visibility Improved

The original detector failed to alert on two suspicious successful authentication events.

They occurred in:

- SUS-02 - privileged failures followed by success;
- SUS-05 - familiar-source compromise followed by success.

V1 explicitly detected:

2 of 2

through the Suspicious Success After Failures correlation.

This is a direct improvement in security visibility.

---

## 3. Benign Alert Burden Decreased

Original benign-alert share:

41.5%

V1 benign-only alert share:

6.7%

Only one V1 alert was benign-only.

That alert represented persistent stale service credentials and was intentionally retained because the service account was not whitelisted.

---

## 4. Repetitive Service Noise Was Controlled Without Exclusion

Original LEG-03 alert count:

142

V1 LEG-03 alert count:

1

The service-account activity remains visible.

The detector therefore reduced repetitive noise without hiding the account or source.

---

## 5. Distributed Behavior Became Explicit

V1 added explicit behavioral detections for:

- one source targeting many users;
- many sources targeting one user.

The baseline primarily produced individual authentication alerts and required analysts to reconstruct these relationships manually.

---

## 6. Analyst Workload Improved

Using the same five-minute-per-alert assumption:

Original:

49.75 hours

V1:

1.25 hours

This represents a substantial reduction in repetitive investigation work.

---

# Why This Is Not Merely a Quieter Detector

A detector that reduced 597 alerts to 15 but lost attack visibility would not satisfy the ticket.

V1 retained all six seeded suspicious scenarios and added detection of the two successful compromise transitions missed by the original.

The reduced volume was achieved primarily by:

- consolidating overlapping signals;
- correlating repeated events;
- grouping continuing authentication conditions;
- aggregating across users and sources;
- treating risk attributes as context; and
- alerting on meaningful state changes.

Therefore the reduced volume is accompanied by improved security signal.

---

# Important Limitation

V1 represented only:

64 of 145 suspicious events

inside its investigation units.

The original produced alerts for:

143 of 145 suspicious events.

These values are not directly equivalent because the detectors operate differently.

The baseline alerts on individual events.

V1 alerts on correlated investigation units.

Nevertheless, the reduced event-level representation creates a real visibility tradeoff.

An attack that remains below all V1 correlation thresholds may fail to create an investigation alert.

---

# False-Negative Risks Remaining

V1 could miss or delay detection of:

- fewer than five rapid failures;
- password spraying against fewer than five users;
- distributed attacks involving fewer than three sources;
- extremely slow authentication attacks;
- service-account abuse that resembles the established pattern;
- attack variants not represented in the current dataset.

The current test establishes performance against this dataset only.

It does not establish universal detection effectiveness.

---

# V1 Disposition

V1 passes the Ticket #008 evaluation against the frozen baseline dataset because:

- alert quality improved;
- redundant workload decreased;
- benign-only alert share decreased;
- all seeded suspicious scenarios remained visible;
- suspicious success-after-failure coverage improved from 0 of 2 to 2 of 2;
- distributed authentication behavior became explicit;
- service-account visibility was retained without whitelisting.

V1 should therefore be considered an improvement over the original detector for this test environment.

---

# STOP Boundary

The original detector has been preserved.

V1 has been implemented and tested against the same frozen dataset.

V1 has now been evaluated.

No V2 tuning should begin until the Ticket #008 STOP boundary is released.
