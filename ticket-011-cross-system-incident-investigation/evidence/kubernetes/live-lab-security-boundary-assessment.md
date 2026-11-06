# Ticket 011 - Live Kubernetes Security Boundary Assessment

Classification: ACTUAL ISOLATED MINIKUBE LAB

Verification timestamp: 2026-11-02T20:26:10.3222706-05:00

Namespace: ticket-011-lab
Pod: reporting-api-598b9767f5-scfzw
Pod UID: f2c5a54d-7174-4f06-ab16-1c21df762003
ServiceAccount: reporting-api

## Runtime Security

- UID/GID: 10001/10001 - VERIFIED
- ServiceAccount token file: ABSENT
- Named AWS credential environment variables: ABSENT
- Effective Linux capabilities: ZERO
- NoNewPrivs: ENABLED
- Seccomp filtering: ENABLED

## RBAC Authorization

- get secrets: DENIED
- patch deployments: DENIED
- create pods: DENIED
- create pods/exec: DENIED

Total: 4 expected denials verified.

These checks impersonated the reporting-api
ServiceAccount using Kubernetes authorization review.

## Evidence

- kubernetes-lab/tests/runtime_security_probe.py
- evidence/kubernetes/live-lab-runtime-security.json
- evidence/kubernetes/live-lab-rbac-validation.json

Runtime probe SHA256: A840E3F3F6AE86A9EF55D2747DEB8FC7A588D18B2E4C7AD49389F4631D033F3C

## Limitations

These findings apply to the observed laboratory Pod.

Only specific environment variable names were checked.
This is not a complete credential inventory.

The synthetic Kubernetes scenario included a token read,
but the actual hardened Pod has no mounted ServiceAccount
token at the checked path.

This supports the token-automount restriction but does
not prove that all possible credential exposure is absent.

Seccomp filtering mode was verified; policy completeness
was not assessed.

No real credentials were read or displayed.
No Kubernetes resource specifications were changed.
Falco alert detection remains untested.

Cross-system compromise: NOT ESTABLISHED.
Production readiness: NOT ESTABLISHED.