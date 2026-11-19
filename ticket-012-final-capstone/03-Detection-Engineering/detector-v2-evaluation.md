# Ticket 012 - Detector Version 2 Evaluation

Date: 2026-11-16
Environment: Controlled synthetic Kubernetes laboratory

## Automated Testing

40 automated tests passed.
No test failures were reported.

## Comparison Dataset

24 labeled synthetic scenarios:
- 12 benign
- 12 suspicious

## Results

| Metric | Baseline | Version 1 | Version 2 |
|---|---:|---:|---:|
| True Positives | 10 | 5 | 12 |
| False Positives | 3 | 1 | 5 |
| True Negatives | 9 | 11 | 7 |
| False Negatives | 2 | 7 | 0 |
| Precision | 76.9% | 83.3% | 70.6% |
| Recall | 83.3% | 41.7% | 100.0% |
| False Positive Rate | 25.0% | 8.3% | 41.7% |

## Engineering Findings

Version 2 detects unapproved destinations without requiring
a recent deployment change.

This eliminates the seven Version 1 false negatives in
the constructed evaluation dataset.

Version 2 produces five false positives:

- B04: Inconsistent claimed identity metadata.
- B09: Unknown workload.
- B10: Authorized diagnostic exception outside change window.
- B11: Authorized exception with unrelated deployment.
- B12: Authorized exception following deployment.

Authorized exceptions are synthetic ground-truth assumptions,
not independently verified authorization records.

The detector must not automatically trust authorization claims
supplied by the requesting workload.

## Decision

Production deployment: NO-GO.

Continued isolated laboratory validation: CONDITIONAL GO.

Conditions for further evaluation:

1. Execute at least eight adversarial and resilience tests.
2. Add independently verified exception or authorization evidence.
3. Distinguish missing telemetry from confirmed safe activity.
4. Evaluate clock skew, identity ambiguity, and policy bypass.
5. Evaluate containment and rollback failures.
6. Reassess false positives, false negatives, and alert explanations.

## Evaluation Limitations

The dataset is small and intentionally constructed.

A measured recall of 100% does not demonstrate that the detector
will identify all suspicious activity in a real environment.

Claimed identities are not independently authenticated.

No production deployment or real compromise is claimed.

## Evidence

- 07-Evidence/supporting-outputs/detector-v1-v2-comparison.json
- 07-Evidence/supporting-outputs/detector-v1-v2-predictions.csv
- 07-Evidence/supporting-outputs/detector-v1-v2-comparison.txt
- 07-Evidence/supporting-outputs/detector-automated-test-results-v2.txt
