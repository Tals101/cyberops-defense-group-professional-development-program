# Ticket 011 - Eight-Case Adversarial Test Assessment

Ticket: CYBEROPS-PDP-011
Assessment UTC: 2026-11-03T18:46:18.3006969+00:00

Classification: EVIDENCE-BACKED ISOLATED LAB ASSESSMENT

## Test Register

| ID | Test case | Evidence classification | Result | Evidence source |
|---|---|---|---|---|
| AT-01 | Unauthorized Secret read | LIVE_AUTHORIZATION_SIMULATION | PASS | evidence\kubernetes\live-lab-rbac-validation.json |
| AT-02 | Unauthorized Deployment patch | LIVE_AUTHORIZATION_SIMULATION | PASS | evidence\kubernetes\live-lab-rbac-validation.json |
| AT-03 | Unauthorized Pod creation | LIVE_AUTHORIZATION_SIMULATION | PASS | evidence\kubernetes\live-lab-rbac-validation.json |
| AT-04 | Unauthorized exec-subresource creation | LIVE_AUTHORIZATION_SIMULATION | PASS | evidence\kubernetes\live-lab-rbac-validation.json |
| AT-05 | Interactive shell execution | LIVE_RUNTIME_STIMULUS | PASS | evidence\kubernetes\live-lab-falco-shell-test.json |
| AT-06 | Noninteractive shell execution | LIVE_RUNTIME_STIMULUS | PASS | evidence\kubernetes\live-lab-falco-enhancement1-positive.json |
| AT-07 | ServiceAccount token-path failed open | LIVE_RUNTIME_STIMULUS | PASS | evidence\kubernetes\live-lab-falco-enhancement2-positive.json |
| AT-08 | Attempted UID 0 privilege escalation | LIVE_RUNTIME_STIMULUS | PASS | evidence\kubernetes\live-lab-uid0-escalation-denial-7f.json |

## Evidence Summary

Distinct documented candidate cases: 8
Live authorization simulations: 4
Executed runtime test cases: 4
Recorded PASS outcomes: 8
Benign negative controls counted: 0

Original evidence source SHA256 hashes were
verified against the seven-case register.

AT-08 evidence SHA256: 19F4DD573F37F0AF0BFF3F14EE3348A83F2F839251677B784A8FC97EE074BD70

## AT-08 Finding

Initial UID: 10001
Attempted UID: 0
Operation: Python os.setuid(0)
Observed kernel denial: EPERM
Unexpected root access: NO
Reporting container stable: YES
Protected Ticket 010 namespace identity: UNCHANGED

AT-08 outcome: PASS_UID0_ESCALATION_DENIED

## Important Qualification

Eight distinct candidate cases are documented.

AT-01 through AT-04 are authorization simulations.
They demonstrate denied Kubernetes permissions,
not actual resource modification attempts.

AT-05 through AT-08 involved executed runtime
stimuli in the isolated Minikube environment.

Formal satisfaction of the eight-adversarial-test
requirement depends on whether the acceptance
criteria count authorization simulations.

No synthetic cloud records are represented as
real AWS execution.

## Remaining Investigation Work

- Linux authentication and persistence assessment
- Cross-system Python correlation engine
- AWS, Kubernetes, and Linux event correlation
- Containment decision and 09:05 stop gate
- Incident disposition and impact assessment
- Recovery runbook and operational readiness
- Final report, integrity review, and closure package

This register does not declare Ticket 011 closed.

No Kubernetes, Helm, Docker, or AWS changes
were made while consolidating this register.