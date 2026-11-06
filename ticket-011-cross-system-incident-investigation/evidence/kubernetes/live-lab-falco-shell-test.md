# Ticket 011 - Live Falco Shell-Detection Test

Classification: ACTUAL MINIKUBE LAB

Application namespace: ticket-011-lab
Application Pod: reporting-api-598b9767f5-scfzw
Monitoring namespace: ticket-011-monitoring
Falco Pod: ticket011-falco-kg6dz

Test start UTC: 2026-11-03T01:51:53.3235134+00:00
Test end UTC: 2026-11-03T01:51:53.4730811+00:00

## Controlled Stimulus

A shell was executed through kubectl exec -it
with terminal verification.

Stimulus exit code: 0

The command made no application-file changes
and used no production credentials.

## Detection Results

Falco rule: Terminal shell in container

Candidate events: 1
Events attributable to Ticket 011: 1

Outcome: DETECTED_AND_ATTRIBUTED

## Privacy and Evidence Scope

Only structured metadata for events attributed to
the Ticket 011 Pod is retained.

Full node-wide Falco alert logs, command lines,
and unrelated workload details are not saved.

## Limitations

A ready Falco Pod does not prove event capture.

An inconclusive result requires further diagnosis;
it must not be reported as successful detection.

This test does not establish Kubernetes audit logging,
cross-system compromise, or production readiness.

The interactive exec was issued using the lab
operator's Kubernetes credentials, not through
the reporting application's ServiceAccount.