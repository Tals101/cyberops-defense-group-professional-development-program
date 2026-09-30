# Ticket #008 — Phase 7 Adversarial Test Plan

## Purpose

Attempt to defeat the current authentication detection strategy without changing V2 first.

The goal is not to force every variation into the same detector.

Each variation will be evaluated to determine whether the gap:

- belongs in V2;
- belongs in a complementary detection;
- should be covered by another control; or
- is acceptable residual risk.

---

# Test Guardrails

- V2 remains unchanged before testing.
- Existing thresholds remain unchanged.
- Existing V1 and V2 results remain preserved.
- Adversarial tests use synthetic authentication events.
- Ground truth is used only for evaluation.
- A miss does not automatically require a new rule.

---

# Variation AT-01 — Threshold Skimming

## Attacker Strategy

Target one non-privileged account from one unfamiliar source.

Generate:

- 4 failed authentications;
- same user;
- same source;
- failures spread across approximately 9 minutes;
- no successful authentication.

The attacker intentionally stops below the V1-01 threshold of 5 failures in 10 minutes.

## Dimensions Varied

- Rate
- Failure count
- Timing

## Expected Detector Behavior

V1-01 should not fire because the sequence remains below 5 failures.

V1-05 should not fire because the account is not privileged.

V2 should therefore receive no V1 signal to correlate.

## Actual Detector Behavior

TBD after test execution.

## Preliminary Classification

Expected: Missed

## Why

The behavior deliberately remains below the primary same-user/same-source threshold.

## Security Significance

Moderate.

A small number of failures may be ordinary user behavior, but an attacker can exploit this ambiguity to probe credentials without crossing the threshold.

## Recommended Response

Do not automatically lower the threshold.

Evaluate whether additional risk context, historical anomaly detection, or complementary controls should cover this behavior.

---

# Variation AT-02 — Distributed Many-to-Many Campaign

## Attacker Strategy

Distribute authentication failures across:

- 6 usernames;
- 4 unfamiliar source addresses;
- approximately 4 hours.

Generate 12 total failures.

Constraints:

- no user/source pair receives 5 failures;
- no single source targets 5 distinct users within 120 minutes;
- no single user receives failures from 3 distinct sources within 60 minutes;
- no privileged account is required.

This models the Purple Team blind spot.

## Dimensions Varied

- Entity distribution
- Source behavior
- Timing
- Rate

## Expected Detector Behavior

V1-01 should not fire.

V1-03 should not fire.

V1-04 should not fire.

V1-05 should not fire.

V2 should have no V1 signal to correlate.

## Actual Detector Behavior

TBD after test execution.

## Preliminary Classification

Expected: Missed

## Why

The malicious behavior exists at the campaign level rather than within one V1 entity relationship.

## Security Significance

High.

This is a deliberate evasion technique that can hide password spraying or credential testing across multiple users and infrastructure nodes.

## Recommended Response

Evaluate a complementary many-user/many-source campaign detection over a broader observation window.

Do not force this behavior into V2 unless testing shows the additional complexity is justified.

---

# Variation AT-03 — Familiar-Source Failures Followed by Success

## Attacker Strategy

Use a familiar internal source against one non-privileged account.

Generate:

- 4 failures within approximately 8 minutes;
- followed by 1 successful authentication;
- same user;
- same familiar source.

The activity intentionally remains below the 5-failure success-after-failure condition.

## Dimensions Varied

- Source familiarity
- Authentication outcome
- Rate
- Success context

## Expected Detector Behavior

V1-01 should not fire because there are fewer than 5 failures.

V1-02 should not fire because the account is non-privileged and fewer than 5 failures precede the success.

No unfamiliar-source condition applies.

V2 should receive no V1 signal.

## Actual Detector Behavior

TBD after test execution.

## Preliminary Classification

Expected: Missed

## Why

The sequence exploits both the numeric threshold and the fact that familiar sources remain contextual rather than independently suspicious.

## Security Significance

High.

A compromised employee workstation could attempt several credentials and obtain a successful login without crossing the current thresholds.

## Recommended Response

Preserve familiar-source visibility.

Consider a complementary suspicious-success detection that incorporates historical behavior, device identity, impossible changes, or other risk signals rather than blindly lowering thresholds.

---

# Variation AT-04 — Privileged Low-and-Slow Control Case

## Attacker Strategy

Target one privileged account from one unfamiliar source.

Generate:

- 4 failed authentications;
- same user;
- same source;
- approximately 30 minutes between attempts;
- all 4 failures occurring within 120 minutes.

## Dimensions Varied

- Privilege
- Timing
- Low rate
- Source familiarity

## Expected Detector Behavior

V1-01 should not fire because the attempts are too far apart for 5 failures in 10 minutes.

V1-05 should fire because:

- the account is privileged;
- the source is unfamiliar;
- 4 failures occur within 120 minutes.

V2 should preserve the activity as an Authentication Attack Sequence case.

## Actual Detector Behavior

TBD after test execution.

## Preliminary Classification

Expected: Detected

## Why

This variation falls within the explicitly preserved low-and-slow privileged detection path.

## Security Significance

High.

The test confirms that slower privileged-account attacks remain visible even when the rapid-failure threshold is not reached.

## Recommended Response

Retain this detection path unless operational data demonstrates unacceptable false positives.

---

# Test Success Criteria

The adversarial exercise is successful if it reveals and documents detector boundaries honestly.

The objective is not zero misses.

For every test variation we must record:

- actual V1 behavior;
- actual V2 behavior;
- detected / partially detected / missed;
- reason;
- security significance;
- recommended response;
- whether the gap belongs in V2 or a complementary detection/control.

---

# Pre-Test Status

Adversarial variations are defined.

Actual behavior has not yet been measured.

V2 has not been changed in response to these variations.
