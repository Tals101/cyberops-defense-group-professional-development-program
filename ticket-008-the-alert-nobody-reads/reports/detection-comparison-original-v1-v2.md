# Ticket #008 - Detection Comparison

## Original vs V1 vs V2

All three versions were evaluated using the same frozen 1,000-event authentication dataset.

| Metric | Original | V1 | V2 |
|---|---:|---:|---:|
| Total Alerts / Investigation Units | 597 | 15 | 7 |
| Known Benign Alerts / Cases | 248 | 1 | 1 |
| Known Suspicious Alerts / Cases | 349 | 14 | 6 |
| Suspicious Scenarios Detected | 6 of 6 | 6 of 6 | 6 of 6 |
| Suspicious Scenarios Missed | 0 | 0 | 0 |
| Duplicate / Redundant / Consolidatable Units | 289 | 8 | 0 identified after V2 correlation |
| Estimated Analyst Workload | 49.75 hours | 1.25 hours | 0.58 hours |
| Suspicious Success Transitions Explicitly Represented | 0 of 2 | 2 of 2 | 2 of 2 |
| Suspicious Events Represented | 143 of 145 | 64 of 145 | 64 of 145 |
| Password-Spray Investigation Units | 120 baseline alerts | 6 source alerts | 1 campaign case |

## Metric Interpretation

The three versions do not produce identical types of output.

The Original detector produces event-level alerts.

V1 produces correlated investigation alerts.

V2 produces higher-level investigation cases.

Therefore raw alert counts cannot be interpreted as directly equivalent security coverage.

The Original detector's 289 duplicate/redundant alerts were measured as alerts beyond the 308 unique alerting authentication events.

For V1, the value of 8 represents V1 investigation alerts that were subsequently consolidated when V2 formed 7 cases from 15 V1 alerts.

For V2, no additional duplicate case units were identified during this test, but this does not prove that future datasets could not contain redundant cases.

---

# Original

## Strengths

- Detected all 6 seeded suspicious scenarios.
- Alerted on 143 of 145 suspicious events.
- Retained broad event-level visibility.

## Weaknesses

- Produced 597 alerts.
- 248 alerts were benign.
- 289 alerts were additional or redundant.
- Analysts had to manually reconstruct relationships.
- Failed to explicitly detect both suspicious successful-authentication transitions.
- Estimated workload was 49.75 hours.

---

# V1

## Strengths

- Reduced alerts from 597 to 15.
- Retained all 6 suspicious scenarios.
- Explicitly detected both suspicious success-after-failure events.
- Reduced benign-only output to 1 investigation alert.
- Added explicit password-spray and distributed-targeting behavior.
- Preserved compromised familiar-source visibility.

## Weaknesses

- Represented only 64 of 145 suspicious events.
- Produced six separate alerts for one password-spray campaign.
- SUS-02 required three related investigation alerts.
- SUS-05 required two related investigation alerts.
- Analysts could still need to reconstruct one incident from several V1 alerts.

---

# V2

## Strengths

- Reduced V1's 15 investigation alerts to 7 cases.
- Retained all 6 suspicious scenarios.
- Retained both suspicious successful-authentication transitions.
- Preserved the same 64 of 145 suspicious-event representation as V1.
- Preserved malicious familiar-source visibility.
- Consolidated six password-spray alerts into one campaign case.
- Consolidated related SUS-02 signals into one case.
- Consolidated related SUS-05 signals into one case.
- Kept the benign service-account condition visible without whitelisting it.
- Estimated workload decreased to 0.58 hours.

## Weaknesses

- V2 inherits V1's underlying threshold blind spots.
- V2 does not restore the suspicious events that V1 did not represent.
- Case correlation can over-merge unrelated activity.
- Long-running campaigns could still be split by the correlation window.
- The benign-only percentage rises to 14.3% because one benign case remains among only seven total cases, even though the absolute benign case count did not increase.

---

# Familiar Internal Address Decision

V2 does not implement the SOC Manager's proposed blanket familiar/internal suppression.

This was intentional.

SUS-05 remained visible as a suspicious case containing familiar-source context.

Had familiar sources been treated as automatically benign, that attack behavior could have been hidden.

Internal does not mean trusted.

Familiar does not mean benign.

Source familiarity remains investigative context rather than an exclusion rule.

---

# V2 Assessment

V2 should not be considered better merely because it produced the lowest number of investigation units.

The stronger justification is that V2 reduced investigation fragmentation while preserving the security properties already demonstrated by V1.

Compared with V1:

- suspicious scenario coverage remained 6 of 6;
- suspicious scenarios missed remained 0;
- suspicious success coverage remained 2 of 2;
- suspicious-event representation remained 64 of 145;
- familiar-source malicious activity remained visible;
- benign-only investigation count remained 1;
- password-spray investigation units decreased from 6 to 1;
- total investigation units decreased from 15 to 7.

Therefore V2 improved case organization and analyst efficiency on the frozen Ticket #008 dataset without demonstrating additional loss of V1 security coverage.

V2 did not materially improve underlying detection sensitivity.

Its improvement is primarily better correlation and presentation of already-detected security signals.

---

# Residual Risk

V2 continues to depend on the underlying V1 detection conditions.

Potential false negatives remain for:

- rapid attacks below five failures;
- password sprays against fewer than five users;
- distributed attacks involving fewer than three sources;
- activity occurring outside correlation windows;
- very slow attacks;
- malicious behavior resembling stable service authentication failures;
- attack types not represented in the frozen dataset.

V2 also introduces correlation-specific risks:

- unrelated activity may be merged;
- a long campaign may be divided into multiple cases;
- one case may contain enough information to require more analyst review than the five-minute workload assumption suggests.

These limitations should remain part of the final Ticket #008 assessment.

---

# Conclusion

On the frozen Ticket #008 dataset, V2 is better justified than blanket suppression and improves operational usability over V1.

The result is not based solely on lower volume.

V2 retained all seeded suspicious scenarios, both suspicious successful-authentication transitions, familiar-source compromise visibility, and the same suspicious-event representation as V1 while reducing unnecessary investigation fragmentation.

The main security limitation remains the underlying V1 detection sensitivity rather than V2 case correlation.
