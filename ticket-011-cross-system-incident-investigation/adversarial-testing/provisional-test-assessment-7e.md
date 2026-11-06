# Ticket 011 - Provisional Adversarial Test Assessment

Reviewed UTC: 2026-11-03T18:37:51.0205465+00:00
Classification: EVIDENCE-BACKED LAB ASSESSMENT

## Test Register

| ID | Test case | Evidence classification | Result | Source |
|---|---|---|---|---|
| AT-01 | Unauthorized Secret read | LIVE_AUTHORIZATION_SIMULATION | PASS | `evidence\kubernetes\live-lab-rbac-validation.json` |
| AT-02 | Unauthorized Deployment patch | LIVE_AUTHORIZATION_SIMULATION | PASS | `evidence\kubernetes\live-lab-rbac-validation.json` |
| AT-03 | Unauthorized Pod creation | LIVE_AUTHORIZATION_SIMULATION | PASS | `evidence\kubernetes\live-lab-rbac-validation.json` |
| AT-04 | Unauthorized exec-subresource creation | LIVE_AUTHORIZATION_SIMULATION | PASS | `evidence\kubernetes\live-lab-rbac-validation.json` |
| AT-05 | Interactive shell execution | LIVE_RUNTIME_STIMULUS | PASS | `evidence\kubernetes\live-lab-falco-shell-test.json` |
| AT-06 | Noninteractive shell execution | LIVE_RUNTIME_STIMULUS | PASS | `evidence\kubernetes\live-lab-falco-enhancement1-positive.json` |
| AT-07 | ServiceAccount token-path failed open | LIVE_RUNTIME_STIMULUS | PASS | `evidence\kubernetes\live-lab-falco-enhancement2-positive.json` |

## Summary

Documented candidate cases: 7
Authorization simulations: 4
Executed runtime stimuli: 3
Benign negative controls counted: 0
Synthetic incident events counted as live tests: 0

Eight-test requirement: NOT YET COMPLETE.

## Interpretation

AT-01 through AT-04 are live Kubernetes
authorization reviews using ServiceAccount
impersonation, not attempted Kubernetes mutations.

AT-05 through AT-07 involved controlled runtime
execution. Falco attributed an alert to each
relevant reporting container.

AT-07 returned ENOENT. The token file was absent
and no credential was read.

A small timestamp-ordering discrepancy exists
between some Falco event times and recorded test
start times. This requires care during correlation.

Container identities and Falco Pod identities
also changed between some historical tests.
Do not describe them as one uninterrupted runtime.

## Remaining Requirement

At least one additional distinct adversarial
test case with observed outcome and evidence
is needed to reach eight documented candidates.

Final compliance with the eight-test requirement
requires reviewing whether authorization-only
checks qualify under the ticket acceptance criteria.

No synthetic AWS or production activity was
represented as real-world execution.

No Kubernetes, Helm, or AWS changes were made
during creation of this register.