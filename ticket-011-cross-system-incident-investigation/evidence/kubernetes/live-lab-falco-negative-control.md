# Ticket 011 - Falco Negative Control

Evidence classification: ACTUAL MINIKUBE LAB

## Previously Verified Positive Control

Rule: Terminal shell in container
Outcome: DETECTED_AND_ATTRIBUTED

## Negative-Control Stimulus

Application Pod: reporting-api-598b9767f5-scfzw
Falco Pod: ticket011-falco-kg6dz

Start UTC: 2026-11-03T01:54:11.2777175+00:00
End UTC: 2026-11-03T01:54:11.9745239+00:00

Executed Python directly through kubectl exec.
No terminal was attached and no shell was invoked.

The code performed a read-only HTTP GET /health.

Stimulus result: PASS
HTTP status: 200

## Falco Observations

Relevant rule: Terminal shell in container
Candidate events in observation window: 0
Attributed alerts: 0
Outcome: PASS_NO_TERMINAL_SHELL_ALERT

Only scoped alert metadata is retained.
Unrelated node-wide Falco event bodies are not saved.

## Interpretation

This is a negative control for terminal-shell
detection, not a test of every Falco rule.

A zero-alert result demonstrates no matching
attributed event in the observed log window.
It does not prove that all benign activity
will be ignored by Falco.

No Kubernetes resource specifications were changed.