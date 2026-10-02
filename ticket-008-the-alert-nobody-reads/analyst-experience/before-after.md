# Ticket #008 — Before / After Analyst Experience

## Purpose

Document how the analyst experience changed from the original authentication detector to the tuned V1/V2 strategy.

The goal of Ticket #008 was not simply to reduce alert volume.

The goal was to improve the amount of useful security information delivered for each unit of analyst attention.

---

# Before — Original Detector

## Analyst View

The original detector produced:

- 597 alerts;
- 248 known benign alerts;
- 349 alerts associated with suspicious activity;
- 289 duplicate, redundant, or additional alerts;
- approximately 49.75 hours of analyst workload using the lab assumption of 5 minutes per alert.

Many individual authentication events produced multiple alerts.

Related activity was fragmented across separate detections.

The analyst was responsible for determining whether separate alerts were actually part of the same behavior.

---

# Typical Original Analyst Experience

An analyst could receive separate alerts for:

- a failed authentication;
- repeated failures;
- an unfamiliar source;
- a privileged-account failure.

These alerts could all describe the same underlying authentication sequence.

The analyst then had to manually determine:

- whether the alerts involved the same user;
- whether they involved the same source;
- whether they occurred close together;
- whether the account was privileged;
- whether a successful authentication later occurred;
- whether the behavior represented one incident or several unrelated events.

---

# Original Alert Weaknesses

The original experience created several operational problems.

## High Alert Volume

597 alerts were created from 1,000 authentication events.

The amount of output competed directly for analyst attention.

## Redundant Alerts

289 alerts represented additional or redundant signaling beyond the unique alerting events.

This increased workload without proportionally increasing understanding.

## Benign Noise

248 alerts were associated with known benign activity.

The stale service credential scenario alone produced 142 alerts.

## Fragmented Context

The analyst had to reconstruct relationships between events manually.

## Missed Success Context

Two suspicious successful-authentication events were not explicitly detected by the original logic.

This meant the analyst could receive many failure alerts while missing the event that potentially represented account compromise.

## Alert Fatigue Risk

Repeated low-value or redundant alerts increased the likelihood that analysts would skim, rapidly close, or ignore authentication alerts.

---

# After — V1 Detection Strategy

## Analyst View

V1 reduced the output to:

- 15 alerts;
- approximately 1.25 analyst-hours;
- 14 suspicious-only alerts;
- 1 benign-only alert;
- 6 of 6 original suspicious scenarios represented;
- both suspicious successful-authentication events explicitly detected.

Instead of alerting on nearly every failed authentication, V1 focused on behavioral patterns.

---

# V1 Analyst Improvement

The analyst received alerts describing:

- rapid repeated failures;
- suspicious success after failures;
- password spraying;
- distributed targeting;
- privileged low-and-slow activity;
- persistent service-account failures.

This reduced the need to interpret isolated authentication failures.

However, multiple V1 alerts could still describe related parts of the same attack.

For example, one attack could generate:

- rapid-failure alert;
- privileged-activity alert;
- suspicious-success alert.

V1 substantially improved signal quality, but correlation work remained.

---

# After — V2 Case Correlation

## Analyst View

V2 reduced the 15 V1 alerts to:

- 7 analyst-facing cases;
- approximately 0.58 analyst-hours under the same 5-minute-per-unit assumption.

V2 grouped related authentication signals into behavioral cases.

Examples included:

- Authentication Attack Sequence;
- Password Spray Campaign;
- Distributed Targeting;
- Persistent Service Authentication Case.

---

# Typical V2 Analyst Experience

Instead of receiving several separate alerts for the same behavior, the analyst receives one case containing:

- primary user;
- account context;
- primary source;
- source familiarity;
- related users;
- related sources;
- failure count;
- first observed time;
- last observed time;
- successful-authentication context;
- plain-language reason;
- recommended initial checks.

The analyst no longer needs to reconstruct the basic detection story before beginning triage.

---

# Before / After Comparison

| Analyst Experience | Original | V1 | V2 |
|---|---:|---:|---:|
| Analyst units | 597 alerts | 15 alerts | 7 cases |
| Estimated workload | 49.75 hours | 1.25 hours | 0.58 hours |
| Known benign units | 248 alerts | 1 alert | 1 case |
| Suspicious scenarios represented | 6/6 | 6/6 | 6/6 |
| Suspicious successful authentications explicitly detected | 0/2 | 2/2 | 2/2 |
| Manual correlation burden | High | Moderate | Low |
| Duplicate / redundant burden | High | Reduced | Consolidated |
| Plain-language behavioral context | Limited | Improved | Strong |
| Success context | Missing | Explicit | Preserved |
| Analyst investigation starting point | Raw alerts | Behavioral alerts | Correlated case |

---

# Important Interpretation

The lower number of V2 cases does not mean V2 detects more malicious events.

V2 improves how existing V1 signals are presented and grouped.

V1 represented 64 of 145 suspicious events compared with 143 of 145 under the original detector.

The improvement is therefore primarily:

- signal quality;
- correlation;
- success visibility;
- reduced redundant workload;
- improved analyst comprehension.

It is not an increase in event-level sensitivity.

---

# Example — Privileged Authentication Attack

## Before

The analyst might receive several separate alerts:

1. failed authentication;
2. repeated failures;
3. unfamiliar-source failure;
4. privileged-account failure;
5. additional repeated-failure alert.

The analyst would need to manually determine whether these alerts belonged together.

A later successful authentication might not create an alert at all.

## After

The analyst receives one Authentication Attack Sequence containing:

- privileged user;
- unfamiliar source;
- failure count;
- sequence timeframe;
- successful authentication;
- success timestamp;
- plain-language explanation;
- recommended investigation steps.

The analyst can immediately focus on whether the successful session was authorized.

---

# Example — Password Spray

## Before

A distributed password spray generated many individual alerts.

The analyst had to manually recognize that the alerts represented a broader campaign.

## V1

The detector produced multiple source-level spray alerts.

This made the campaign easier to identify but still required some correlation.

## V2

The related spray signals were consolidated into one Password Spray Campaign case.

The analyst receives the campaign-level view instead of multiple fragments.

---

# What Improved Most?

The largest improvement was not simply fewer alerts.

The most important improvements were:

- behavioral grouping;
- explicit suspicious-success detection;
- reduced duplication;
- clearer account and source context;
- less manual reconstruction;
- better prioritization of privileged activity;
- more useful investigation starting points.

---

# What Did Not Improve?

The tuned design still has known limitations.

Adversarial testing showed that the current strategy can miss:

- threshold-skimming activity;
- distributed many-user/many-source campaigns;
- familiar-source sub-threshold failures followed by success.

V2 also cannot detect activity that never produces a V1 signal.

The improved analyst experience therefore does not eliminate residual detection risk.

---

# Analyst Usability Result

The final alert design was tested from the perspective of an analyst who did not build the detection.

The usability result was:

PASS WITH REVISIONS

The analyst could determine within approximately 60 seconds:

- why the alert fired;
- whether the account was privileged;
- whether authentication succeeded;
- the source involved;
- the scale and duration;
- the immediate investigation path.

The final alert presentation was then revised to:

- align severity with risk;
- qualify source familiarity;
- include destination/application context when available;
- move engineering rule IDs below the analyst-facing explanation.

---

# Final Before / After Assessment

Before Ticket #008, the analyst experience emphasized alert volume.

After V1/V2, the analyst experience emphasizes behavioral meaning.

The original detector asked the analyst to assemble the story.

The tuned strategy attempts to present the story first so the analyst can spend attention investigating the security question rather than reconstructing the detector output.

---

# Status

Before / After Analyst Experience artifact completed.
