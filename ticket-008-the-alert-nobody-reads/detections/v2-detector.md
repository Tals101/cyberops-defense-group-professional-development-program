# Ticket #008 — V2 Detector Specification

## Version

V2 — Case-Level Correlation

## Purpose

V2 converts V1 investigation alerts into higher-level investigation cases.

V2 does not suppress familiar or internal sources.

V2 does not use ground-truth labels.

V2 uses:

- the preserved V1 alert output;
- the frozen authentication telemetry for case enrichment.

Ground truth is used only later during evaluation.

---

# Input

Primary signal input:

analysis/v1-alerts.csv

Telemetry enrichment input:

dataset/authentication-events.csv

V2 must not read:

dataset/authentication-ground-truth.csv

---

# V2-01 — Authentication Attack Sequence

Eligible V1 signals:

- V1-01 Rapid Repeated Authentication Failures
- V1-02 Suspicious Success After Failures
- V1-05 Low-and-Slow Privileged Authentication Activity

Signals are candidates for the same V2-01 case when they share the exact same:

- primary user; and
- primary source.

Signals for that user/source are merged when their time ranges overlap or when the next signal begins no more than 120 minutes after the previous signal ends.

The case must preserve all contributing V1 rule IDs.

If a V1-02 signal is included, the case must explicitly record that a successful authentication occurred.

A familiar source does not prevent case creation.

---

# V2-02 — Password Spray Campaign

Eligible V1 signals:

- V1-03 Password Spray — One Source, Many Users

Source-specific spray alerts are merged into one campaign when their alert time ranges:

- overlap; or
- are separated by no more than 120 minutes.

The campaign case must preserve:

- all participating sources;
- all targeted users;
- all contributing V1 alert IDs;
- all unique related authentication events;
- first observed time;
- last observed time;
- failure count;
- source familiarity context;
- privileged-account context.

This correlation is based on temporal campaign behavior.

No source is excluded because it is familiar or internal.

---

# V2-03 — Distributed Targeting Case

Eligible V1 signal:

- V1-04 Distributed Targeting — Many Sources, One User

Each qualifying targeted user remains represented as a distributed-targeting investigation case.

The case must preserve all participating sources and all related authentication events.

If more than one V1-04 signal exists for the same user and the signals overlap or occur within 120 minutes, they may be consolidated into one case.

---

# V2-04 — Persistent Service Authentication Case

Eligible V1 signal:

- V1-06 Persistent Service Authentication Failure

Signals sharing the same service account and source are represented as one persistent-service case when their time ranges overlap or occur within 120 minutes.

The account or source must not be whitelisted.

The case must preserve the related authentication events and source familiarity context.

---

# Case Construction

For every V2 case, related authentication event IDs are the deduplicated union of all related_event_ids from the contributing V1 signals.

Failure counts are calculated from unique authentication events, not by summing V1 alert failure counts.

This prevents duplicate counting when several V1 signals reference the same event.

Case fields must include:

- case_id;
- rule_id;
- case_name;
- first_observed;
- last_observed;
- primary_user;
- primary_source;
- related_users;
- related_sources;
- unique_failure_count;
- distinct_user_count;
- distinct_source_count;
- any_privileged;
- source_familiarity;
- successful_authentication;
- contributing_v1_alert_ids;
- contributing_v1_rule_ids;
- related_event_ids;
- reason.

---

# Familiar/Internal Source Guardrail

V2 must not:

- suppress familiar sources;
- suppress internal sources;
- whitelist familiar workstations;
- assume familiar means benign;
- assume internal means trusted.

Source familiarity remains case context only.

This is required to preserve visibility of compromised familiar-source behavior such as that represented in SUS-05.

---

# Case Priority

V2 does not assign a case as benign or suspicious.

No ground-truth classification is available to the detector.

Evaluation classification occurs only after V2 output is frozen.

---

# Expected Structural Change

V1:

15 investigation alerts.

V2 expectation:

fewer than 15 cases through correlation.

Expected consolidation includes:

- related V1-01, V1-02, and V1-05 signals for the same attack sequence;
- multiple V1-03 source alerts participating in one password-spray campaign.

V2 is not successful merely because the output count is lower.

---

# Known Risks

Case-level correlation may:

- merge unrelated attacks that occur close together;
- separate a single campaign that exceeds the correlation window;
- preserve underlying V1 threshold blind spots;
- reduce apparent alert volume without improving coverage if correlation is poorly justified.

These risks must be evaluated after testing.

---

# Required Test

V2 must be tested against the exact same frozen 1,000-event dataset used by the original detector and V1.

V2 results must be compared with both earlier versions.

No detector logic or dataset changes may be made after V2 results are observed without documenting a new tuning iteration.

---

# Pre-Implementation Status

V2 logic is defined.

V2 is not implemented.

V2 has not been executed.

Original and V1 remain unchanged.
