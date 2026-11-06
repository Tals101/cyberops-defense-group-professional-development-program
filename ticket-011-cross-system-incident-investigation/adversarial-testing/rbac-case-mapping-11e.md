# Ticket 011 - Kubernetes RBAC Case Mapping

Reviewed UTC: 2026-11-05T17:26:01.1506486+00:00

**Classification: ACTUAL ISOLATED MINIKUBE LAB EVIDENCE**

## Recorded SelfSubjectAccessReview Checks

| Check | Proposed case | Verb | Resource | Expected | Actual | Recorded result |
|---|---|---|---|---|---|---|
| 1 | AT-01 | get | secrets | no | no | PASS |
| 2 | AT-02 | patch | deployments | no | no | PASS |
| 3 | AT-03 | create | pods | no | no | PASS |
| 4 | AT-04 | create | pods/exec | no | no | PASS |

## Case-Level Evidence Assessment

| Case | Original objective | Evidence status |
|---|---|---|
| AT-01 | Reporting ServiceAccount secret-read authorization | DECISION_MATCH_RECORDED |
| AT-02 | Reporting ServiceAccount deployment-patch authorization | DECISION_MATCH_RECORDED |
| AT-03 | Reporting ServiceAccount Pod-creation authorization | DECISION_MATCH_RECORDED |
| AT-04 | Reporting ServiceAccount pods/exec authorization | DECISION_MATCH_RECORDED |

## Summary

Authorization checks examined: 4

Cases with matching decisions: 4

Unmapped source checks: 0

All four case mappings confirmed: True

The checks queried Kubernetes authorization.
They did not execute the underlying
secret-read, deployment-patch, Pod-create,
or pods/exec operations.

A recorded match between expected and actual
authorization decisions supports the tested
permission boundary only.

It does not establish that an attempted
privileged action was executed or succeeded.

## Acceptance Limits

The original README identifies adversarial
testing as a project workstream but does not
establish the quantitative acceptance rubric.

The four RBAC cases remain authorization
simulations even where the mapped permission
decisions are supported by lab evidence.

Formal eight-scenario acceptance remains pending
the authoritative rubric and reviewer sign-off.

The synthetic cross-system incident evidence
remains separate from this Minikube assessment.

## Disposition

Case-level RBAC mapping: DOCUMENTED.

Formal acceptance: PENDING.

09:05 containment gate: PENDING.

Cross-system causation: NOT ESTABLISHED.

Ticket closure: PENDING.

No AWS, Kubernetes, Helm, Docker, or Linux
resources were modified.