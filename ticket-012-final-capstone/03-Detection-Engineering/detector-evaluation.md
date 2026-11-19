# Ticket 012 - Detection Engineering Evaluation

Date: 2026-11-16
Status: Baseline comparison completed
Environment: Synthetic Kubernetes incident laboratory

## 1. Evaluation Scope

Evaluated 24 labeled synthetic scenarios:

- 12 benign scenarios
- 12 suspicious scenarios

Compared two detection approaches:

1. Destination-only baseline: alert on any unapproved destination.
2. Correlation detector: alert when an unapproved destination follows
   a deployment change affecting the same workload within five minutes.

## 2. Results

| Metric | Destination Baseline | Correlation Detector |
|---|---:|---:|
| True Positives | 10 | 5 |
| False Positives | 3 | 1 |
| True Negatives | 9 | 11 |
| False Negatives | 2 | 7 |
| Precision | 76.9% | 83.3% |
| Recall | 83.3% | 41.7% |
| False Positive Rate | 25.0% | 8.3% |

## 3. Findings

The correlation detector reduced false positives from three to one.

However, false negatives increased from two to seven.

The detector missed suspicious activity involving:

- Network requests outside the five-minute deployment window.
- Network requests preceding deployment changes.
- Unrelated or unavailable deployment events.
- Identity mismatches involving approved destinations.
- Previously unknown workloads.

The current detector compares claimed and observed identity fields,
but this comparison does not independently authenticate the requester.

The synthetic dataset also contains authorized exceptions absent
from the static destination allowlist. In particular, benign case
B12 and suspicious cases with equivalent telemetry cannot be reliably
distinguished without additional authorization evidence.

## 4. Decision

Decision: NO-GO for deployment as a standalone security detector.

Reason: The correlation rule's 41.7% recall is insufficient for
reliable detection within this synthetic evaluation.

This decision does not prohibit continued controlled laboratory work.

## 5. Recommended Improvements

1. Detect unapproved destinations independently of deployment timing.
2. Use deployment correlation to increase investigation priority.
3. Incorporate verified authorization or approved-exception telemetry.
4. Add separate handling for identity mismatches and unknown workloads.
5. Flag missing telemetry rather than treating missing evidence as safe.
6. Reevaluate precision, recall, false positives, and false negatives
   after implementation.

## 6. Limitations

All scenarios and ground-truth labels are synthetic.

The evaluation dataset is small and intentionally constructed.
Results cannot establish production detection performance.

The existing 31 passing unit tests confirm expected software
behavior but do not establish sufficient detection effectiveness.

## 7. Evidence

- 03-Detection-Engineering/synthetic-data/labeled-correlation-scenarios.json
- 07-Evidence/supporting-outputs/baseline-comparison-results.json
- 07-Evidence/supporting-outputs/baseline-comparison-predictions.csv
- 07-Evidence/supporting-outputs/baseline-comparison-report.txt
- 07-Evidence/supporting-outputs/detector-automated-test-results.txt
