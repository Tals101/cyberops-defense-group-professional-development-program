# Ticket 011 - Enhancement 1 Negative Control

Classification: ACTUAL MINIKUBE LAB

Rule: Ticket011 Unexpected Shell In Reporting Image
Falco Helm revision: 2

Reporting Pod: reporting-api-598b9767f5-scfzw
Falco Pod: ticket011-falco-8zk5f

Test start UTC: 2026-11-03T17:49:58.0737548+00:00
Test end UTC: 2026-11-03T17:49:58.8011214+00:00

## Test

Executed Python directly with kubectl exec.
No shell launched; no terminal attached.

Application health: HTTP 200
Stimulus exit code: 0

## Falco Results

Prior positive control: DETECTED_AND_ATTRIBUTED
Custom-rule candidates: 0
Attributed alerts: 0
Log window truncated: False
Invalid event timestamps: 0
Sensor stable: True

Outcome: PASS_NO_CUSTOM_RULE_ALERT

## Interpretation

A PASS supports this specific benign control.
It does not establish a general false-positive rate.

Only attributed alert metadata was retained.
Unrelated Falco event bodies were not saved.

No Kubernetes resource specifications were changed.