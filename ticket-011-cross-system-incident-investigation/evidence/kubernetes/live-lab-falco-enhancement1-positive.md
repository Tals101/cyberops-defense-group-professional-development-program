# Ticket 011 - Enhancement 1 Positive Control

Classification: ACTUAL MINIKUBE LAB

Rule: Ticket011 Unexpected Shell In Reporting Image
Falco Helm revision: 2

Reporting Pod: reporting-api-598b9767f5-scfzw
Falco Pod: ticket011-falco-8zk5f

Start UTC: 2026-11-03T17:47:43.2872607+00:00
End UTC: 2026-11-03T17:47:43.4484701+00:00

## Stimulus

Noninteractive shell executed using kubectl exec.
TTY attached: No
Exit code: 0

## Observations

Custom-rule candidate events: 1
Attributed reporting-container alerts: 1
Log window truncated: False
Sensor stable during test: True

Outcome: DETECTED_AND_ATTRIBUTED

## Evidence Scope

Full node-wide Falco logs were inspected in memory
but were not saved.

Only structured metadata from attributed Ticket 011
rule events was retained.

## Limitations

A zero-match result is inconclusive until image
metadata, rule loading, and the event pipeline
have been investigated.

A matching negative control is still required.

This test does not establish cross-system compromise
or production readiness.

No Kubernetes resource specifications were changed.