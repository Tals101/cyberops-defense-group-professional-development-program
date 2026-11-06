# Ticket 011 - Eight-Case Technical Evidence Matrix

Ticket: CYBEROPS-PDP-011
Prepared UTC: 2026-11-05T17:29:44.7757334+00:00

**Classification: ISOLATED MINIKUBE LAB EVIDENCE**

## Verified Test Matrix

| Case | Evidence class | Recorded outcome | Technical evidence |
|---|---|---|---|
| AT-01 | AUTHORIZATION_SIMULATION | AUTHORIZATION_DENIED_AS_EXPECTED | SUPPORTED_FOR_RECORDED_SCOPE |
| AT-02 | AUTHORIZATION_SIMULATION | AUTHORIZATION_DENIED_AS_EXPECTED | SUPPORTED_FOR_RECORDED_SCOPE |
| AT-03 | AUTHORIZATION_SIMULATION | AUTHORIZATION_DENIED_AS_EXPECTED | SUPPORTED_FOR_RECORDED_SCOPE |
| AT-04 | AUTHORIZATION_SIMULATION | AUTHORIZATION_DENIED_AS_EXPECTED | SUPPORTED_FOR_RECORDED_SCOPE |
| AT-05 | EXECUTED_RUNTIME_TEST | DETECTED_AND_ATTRIBUTED | SUPPORTED_FOR_RECORDED_SCOPE |
| AT-06 | EXECUTED_RUNTIME_TEST | DETECTED_AND_ATTRIBUTED | SUPPORTED_FOR_RECORDED_SCOPE |
| AT-07 | EXECUTED_RUNTIME_TEST | DETECTED_AND_ATTRIBUTED_FAILED_OPEN | SUPPORTED_FOR_RECORDED_SCOPE |
| AT-08 | EXECUTED_RUNTIME_TEST | PASS_UID0_ESCALATION_DENIED | SUPPORTED_FOR_RECORDED_SCOPE |

## Interpretation

Eight provisional test cases have supporting
technical evidence in the Ticket 011 repository.

AT-01 through AT-04:
Four Kubernetes authorization checks returned
the expected denial decisions.

They did not execute the underlying privileged
secret-read, deployment-patch, Pod-create,
or pods/exec operations.

AT-05 through AT-08:
Four executed runtime tests produced their
recorded observation results.

The ServiceAccount token-file open in AT-07
failed with ENOENT and read no token contents.

The UID 0 escalation attempt in AT-08
was denied with EPERM.

## Detection Controls

Two custom Falco enhancements have recorded
positive and negative control evidence.

Each positive test generated an attributed
custom-rule alert.

Each corresponding negative control generated
zero matching custom-rule alerts.

This does not establish statistical false-
positive rates or production-wide coverage.

## Acceptance Status

Technically supported provisional cases: 8.

Authorization simulations: 4.

Executed runtime tests: 4.

Eight executed runtime tests: NOT ESTABLISHED.

Authoritative eight-scenario rubric:
NOT VERIFIED.

Formal reviewer acceptance: PENDING.

A complete provisional evidence matrix is not
equivalent to authorized ticket acceptance.

## Containment and Recovery

09:05 stop-gate date and timezone:
NOT VERIFIED.

Formal containment authorization: PENDING.

Production recovery readiness:
NOT ESTABLISHED.

Cross-system incident causation:
NOT ESTABLISHED.

The 42-event cross-system incident dataset is
synthetic and separate from these live lab tests.

## Final Disposition

Technical evidence matrix: COMPLETE.

Formal Ticket 011 closure: PENDING.

No Kubernetes, Helm, Docker, AWS, or Linux
resources were modified by Step 11F.