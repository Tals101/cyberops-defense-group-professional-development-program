# Ticket 011 - Eight-Case Adversarial Acceptance Review

Ticket: CYBEROPS-PDP-011

Reviewed UTC: 2026-11-05T01:24:55.8963435+00:00

**Classification: ACTUAL ISOLATED MINIKUBE LAB REVIEW**

## Executive Assessment

The provisional adversarial register contains eight
distinct cases, each marked PASS in that register.

These cases represent two different test classes:

- Authorization simulations: 4
- Executed runtime tests: 4

This distinction must remain visible in the
final acceptance and closure decisions.

## Eight-Case Evidence Matrix

| Case | Evidence class | Tested objective | Primary evidence file |
|---|---|---|---|
| AT-01 | AUTHORIZATION_SIMULATION | Reporting ServiceAccount secret-read authorization | live-lab-rbac-validation.json |
| AT-02 | AUTHORIZATION_SIMULATION | Reporting ServiceAccount deployment-patch authorization | live-lab-rbac-validation.json |
| AT-03 | AUTHORIZATION_SIMULATION | Reporting ServiceAccount Pod-creation authorization | live-lab-rbac-validation.json |
| AT-04 | AUTHORIZATION_SIMULATION | Reporting ServiceAccount pods/exec authorization | live-lab-rbac-validation.json |
| AT-05 | EXECUTED_RUNTIME_TEST | Interactive shell and Falco observation | live-lab-falco-shell-test.json |
| AT-06 | EXECUTED_RUNTIME_TEST | Noninteractive shell custom-rule detection | live-lab-falco-enhancement1-positive.json |
| AT-07 | EXECUTED_RUNTIME_TEST | Failed ServiceAccount token-path open detected | live-lab-falco-enhancement2-positive.json |
| AT-08 | EXECUTED_RUNTIME_TEST | Attempted setuid(0) denied by EPERM | live-lab-uid0-escalation-denial-7f.json |

All primary files reside in evidence/kubernetes.

The original case identifiers and test-result
labels are preserved in the Step 7G CSV register.

## Authorization Simulation Evidence

AT-01 through AT-04 correspond to recorded
SelfSubjectAccessReview authorization checks.

These checks evaluate Kubernetes permissions.
They are not evidence that the tested mutating
API operations were actually executed.

Do not count these as executed runtime attacks
without an explicit acceptance rule permitting
authorization simulations.

## Executed Runtime Test Evidence

AT-05:
An interactive shell test produced an attributed
Falco detection in the isolated Minikube lab.

AT-06:
A noninteractive shell stimulus produced a matching
custom Falco detection. Its recorded negative
control produced zero custom-rule alerts.

AT-07:
A ServiceAccount token-path access attempt produced
an attributed custom Falco alert.

The file open failed with ENOENT.
No token contents were obtained.

Its recorded negative control produced zero
custom-rule alerts.

AT-08:
An attempted UID 0 change through setuid(0)
was denied with EPERM.

The evidence records no unexpected privilege
gain and no change to the protected namespace.

## Detection Engineering Results

Falco enhancements assessed: 2.

Recorded positive controls validated: 2.

Recorded negative controls validated: 2.

These results do not establish production-wide
coverage or a statistical false-positive rate.

## Acceptance Decision

Eight provisional cases documented: YES.

Four authorization simulations documented: YES.

Four executed runtime tests documented: YES.

Eight executed runtime tests demonstrated: NO.

Formal eight-test acceptance:
**PENDING CRITERIA REVIEW**.

The case count by itself is insufficient to
confirm whether the ticket's acceptance criteria
are satisfied.

The acceptance authority must determine whether
authorization simulations count toward the
eight-case requirement.

## Investigation Boundaries

The test evidence is from an actual isolated
Minikube lab.

The AWS, Kubernetes, and Linux cross-system
incident timeline is a separate synthetic dataset.

The live-lab test observations do not establish
a real cross-system compromise.

No new tests, mutating Kubernetes requests,
containment actions, or recovery actions were
performed during this review.

## Next Required Action

Reconcile the eight test cases with the actual
ticket acceptance requirements and document
any remaining gaps before final closure.

The 09:05 formal containment gate also remains
pending date, timezone, and authorization review.

Final Ticket 011 closure: PENDING.