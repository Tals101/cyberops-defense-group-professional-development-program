# Ticket #008 — Phase 7 Adversarial Testing Report

## Objective

Test the current authentication detection strategy against attacker variations designed to operate near or outside the assumptions of the V1 and V2 detections.

V1 and V2 were not modified before or during testing.

The original frozen 1,000-event dataset was not changed.

A separate 25-event adversarial dataset was used.

---

# Test Summary

| Test | Strategy | V1 Result | V2 Result | Final Classification |
|---|---|---|---|---|
| AT-01 | Threshold skimming | No alert | No case | Missed |
| AT-02 | Distributed many-to-many campaign | No alert | No case | Missed |
| AT-03 | Familiar-source failures followed by success | No alert | No case | Missed |
| AT-04 | Privileged low-and-slow | V1-05 alert | V2-01 case | Detected |

Total adversarial events: 25

V1 alerts produced: 1

V2 cases produced: 1

Detected variations: 1 of 4

Missed variations: 3 of 4

---

# AT-01 — Threshold Skimming

## Attacker Strategy

One non-privileged account was targeted from one unfamiliar source.

The attacker generated:

- 4 failed authentications;
- same user;
- same source;
- approximately 9 minutes total duration;
- no successful authentication.

The attacker intentionally remained below the V1-01 threshold of 5 failures within 10 minutes.

## Expected Detector Behavior

V1-01 was expected not to fire.

No other V1 rule was expected to apply.

V2 was expected to receive no signal.

## Actual Detector Behavior

No V1 alert was generated.

No V2 case was generated.

## Classification

Missed.

## Why

The attacker remained immediately below the defined rapid-failure threshold.

The behavior did not meet another detection path.

## Security Significance

Moderate.

This is a realistic threshold-evasion technique, but automatically lowering the threshold could also increase alerts for ordinary password mistakes.

## Recommended Response

Do not automatically lower V1-01.

Evaluate whether additional context such as historical deviation, endpoint risk, device identity, or repeated sub-threshold behavior over longer periods can provide a complementary signal.

---

# AT-02 — Distributed Many-to-Many Campaign

## Attacker Strategy

The attacker generated 12 failures distributed across:

- 6 usernames;
- 4 unfamiliar source addresses;
- approximately 4 hours.

The test was intentionally constructed so that:

- no user/source pair reached 5 failures;
- no source targeted 5 distinct users within 120 minutes;
- no user received failures from 3 sources within 60 minutes;
- no privileged account was required.

## Expected Detector Behavior

V1-01 was expected not to fire.

V1-03 was expected not to fire.

V1-04 was expected not to fire.

V1-05 was expected not to fire.

V2 was expected to have no V1 signal to correlate.

## Actual Detector Behavior

No V1 alert was generated.

No V2 case was generated.

## Classification

Missed.

## Why

The malicious behavior was visible only at a broader campaign level.

No existing V1 entity relationship accumulated enough activity within its defined window.

V2 cannot recover activity that produces no V1 input signal.

## Security Significance

High.

This test confirms the Purple Team blind spot.

An attacker can distribute credential testing across multiple identities, sources, and time intervals to avoid concentrated threshold-based detections.

## Recommended Response

Treat this as an architectural detection gap.

Evaluate a complementary distributed-authentication campaign detector that examines many-user/many-source activity across a broader period.

Do not overload the existing V2 correlation logic with unrelated analytical objectives.

---

# AT-03 — Familiar-Source Failures Followed by Success

## Attacker Strategy

A familiar internal source targeted one non-privileged account.

The sequence contained:

- 4 failures within approximately 6 minutes;
- 1 successful authentication at approximately minute 8;
- same user;
- same familiar source.

## Expected Detector Behavior

V1-01 was expected not to fire because fewer than 5 failures occurred.

V1-02 was expected not to fire because the account was non-privileged and fewer than 5 failures preceded the success.

No unfamiliar-source condition applied.

V2 was expected to receive no V1 signal.

## Actual Detector Behavior

No V1 alert was generated.

No V2 case was generated.

The successful authentication was not explicitly detected.

## Classification

Missed.

## Why

The sequence remained below the success-after-failure threshold.

Source familiarity did not suppress an alert; rather, no existing rule independently treated this specific sub-threshold successful sequence as suspicious.

## Security Significance

High.

A compromised familiar workstation or stolen session context could produce suspicious authentication behavior without looking unusual based only on source familiarity.

## Recommended Response

Do not suppress familiar internal sources.

Evaluate a complementary suspicious-success detection using additional risk context such as:

- prior authentication history;
- device identity;
- endpoint risk;
- unusual account/device pairing;
- unusual geography or network path;
- privilege changes;
- impossible or improbable behavioral transitions.

---

# AT-04 — Privileged Low-and-Slow Control Case

## Attacker Strategy

One privileged account was targeted from one unfamiliar source.

The attacker generated:

- 4 failed authentications;
- 30-minute spacing;
- same user;
- same source;
- all attempts within 120 minutes.

## Expected Detector Behavior

V1-01 was expected not to fire because the failures were too widely spaced for the rapid-failure threshold.

V1-05 was expected to fire because:

- the account was privileged;
- the source was unfamiliar;
- 4 failures occurred within 120 minutes.

V2 was expected to preserve the V1 signal as an Authentication Attack Sequence.

## Actual Detector Behavior

V1 produced:

- Alert: ADV-V1-0001
- Rule: V1-05
- User: sec.admin
- Source: 203.0.113.88
- Failure count: 4

V2 produced:

- Case: ADV-V2C-0001
- Case type: V2-01
- User: sec.admin
- Source: 203.0.113.88
- V1 rule: V1-05
- Failure count: 4

## Classification

Detected.

## Why

The scenario matched the explicitly designed privileged low-and-slow detection path.

## Security Significance

High.

The result confirms that the tuned detection retained coverage for slower privileged-account attacks that would not meet the rapid-failure rule.

## Recommended Response

Retain V1-05 and the V2 correlation path unless operational evidence later shows unacceptable false-positive behavior.

---

# Key Findings

## 1. V2 Does Not Create New Detection Sensitivity

V2 successfully correlates and consolidates signals that already exist in V1.

It does not identify malicious behavior when V1 generates no input alert.

This is expected behavior and should not be treated as a V2 implementation defect.

## 2. Threshold Evasion Remains Possible

AT-01 demonstrated that an attacker can remain immediately below a numeric threshold.

This is a tuning limitation inherent in threshold-based detections.

## 3. Multi-Entity Distribution Is the Most Important Architectural Gap

AT-02 demonstrated that distributed many-user/many-source campaigns can evade the current analytical model.

This is the most significant new adversarial finding.

## 4. Familiar Does Not Mean Safe

AT-03 confirms that internal or familiar source context must not be treated as proof of legitimacy.

Blanket familiar-address suppression would increase this risk.

## 5. Privileged Low-and-Slow Coverage Was Preserved

AT-04 confirms that V1-05 provides meaningful protection against slower privileged-account targeting.

---

# Detection Engineering Decision

Do not modify V2 in response to every adversarial miss.

The current V2 correlation layer remains useful for:

- rapid repeated failures;
- suspicious success sequences that meet V1 thresholds;
- password spray signals;
- distributed targeting signals;
- privileged low-and-slow attacks;
- persistent service-account authentication failures.

The adversarial exercise identified conditions that require complementary analytical perspectives rather than additional complexity inside V2.

Priority future evaluation areas are:

1. distributed many-user/many-source authentication campaigns;
2. repeated sub-threshold behavior over longer time periods;
3. suspicious successful authentications from familiar sources using contextual risk signals.

---

# Residual Risk

Known residual risk now includes:

- attackers deliberately staying below individual thresholds;
- many-user/many-source distributed credential attacks;
- sub-threshold suspicious successes;
- activity whose malicious significance becomes visible only over broader historical context.

These conditions must be recorded in the false-negative register and considered during production-readiness review.

---

# Final Phase 7 Status

Adversarial testing completed.

Four attacker variations were tested.

One variation was detected.

Three variations were missed.

The misses were preserved rather than hidden or immediately tuned away.

No V1 or V2 logic was changed during adversarial testing.

The results support the use of multiple complementary detections rather than one increasingly complex authentication rule.
