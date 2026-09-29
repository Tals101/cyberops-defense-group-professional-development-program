# Ticket #008 - V2 Evaluation Report

## Evaluation Question

Did V2 improve the detector, or did it merely make the alert count smaller?

## Decision

V2 improved investigation quality and analyst usability on the frozen Ticket #008 dataset.

The improvement is specifically in correlation and case presentation.

V2 did not demonstrate greater underlying event-level detection sensitivity than V1.

---

# Evidence

V1 produced:

15 investigation alerts.

V2 produced:

7 investigation cases.

This is a 53.3% reduction in investigation units.

However, alert reduction alone is not the basis for the decision.

V2 also retained:

- 6 of 6 suspicious scenarios;
- 0 completely missed suspicious scenarios;
- 2 of 2 suspicious successful-authentication transitions;
- 64 of 145 suspicious events represented;
- malicious familiar-source visibility;
- one persistent benign service-account case without whitelisting.

---

# Important V2 Improvements

## Password Spray

V1:

6 separate source-level spray alerts.

V2:

1 password-spray campaign case.

The underlying suspicious-event representation remained intact.

## SUS-02

V1 required three related investigation alerts.

V2 correlated them into one authentication attack sequence containing:

- privileged authentication risk;
- repeated failures;
- successful authentication.

## SUS-05

V1 required two related investigation alerts.

V2 correlated them into one case while preserving the suspicious successful authentication from a familiar source.

---

# SOC Manager Suppression Request

The manager's familiar/internal suppression proposal was not implemented.

The decision was validated by V2 testing.

V2 retained one suspicious case containing familiar-source context.

Therefore treating familiar internal sources as automatically benign would have created unnecessary coverage risk.

---

# Cost

V2 requires additional state and correlation logic.

The detector must determine when alerts represent one incident and when they represent separate incidents.

This introduces risks of over-correlation and under-correlation.

Cases may also take longer than five minutes to review because each case can contain more evidence than an individual V1 alert.

---

# Coverage Change

Compared with V1:

Suspicious scenarios:

6 of 6 -> 6 of 6

Suspicious successes:

2 of 2 -> 2 of 2

Suspicious events represented:

64 of 145 -> 64 of 145

Benign-only investigation units:

1 -> 1

No additional measured detection coverage was lost during V2 correlation.

---

# Residual Risk

V2 inherits the underlying V1 false-negative risks.

It can still miss attacks that remain below the V1 correlation thresholds.

V2 additionally risks:

- merging unrelated attacks;
- separating long campaigns;
- hiding useful distinctions inside overly broad cases.

These risks require future testing on additional datasets and attack variations.

---

# Success Metric Review

1. Fewer than 15 investigation cases:
PASS - 7

2. All 6 suspicious scenarios detected:
PASS - 6 of 6

3. Suspicious scenarios missed remain 0:
PASS - 0

4. Both suspicious successful-authentication transitions represented:
PASS - 2 of 2

5. Benign-only cases do not exceed V1's 1:
PASS - 1

6. No familiar/internal source or account globally suppressed:
PASS

7. Password-spray fragmentation reduced:
PASS - 6 V1 alerts consolidated into 1 V2 campaign

8. Related attack-sequence signals consolidated:
PASS

9. Estimated workload below V1's 1.25 hours:
PASS - 0.58 hours

10. Coverage limitations documented:
PASS

---

# Final V2 Disposition

V2 passes the defined Ticket #008 success criteria on the frozen dataset.

The strongest improvement is not lower volume by itself.

The improvement is that related V1 security signals are presented as fewer, better-organized investigation cases without measurable loss of V1 scenario coverage, success-transition visibility, familiar-source visibility, or suspicious-event representation.

V2 should therefore be considered an operational correlation improvement over V1 for this test environment.

It should not be interpreted as proof that the underlying detector is universally more sensitive or that the documented residual false-negative risks have been eliminated.

---

# STOP Boundary

V2 implementation is complete.

V2 testing is complete.

Original, V1, and V2 are preserved.

No additional tuning should occur before the next ticket instruction or review.
