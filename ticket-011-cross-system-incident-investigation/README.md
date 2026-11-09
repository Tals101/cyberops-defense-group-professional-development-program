# Ticket #011 - Cross-System Incident Investigation

Ticket ID: CYBEROPS-PDP-011

Classification: HIGH - Security Incident / Cloud Infrastructure

Engineer: Naftali Wodinsky

Environment: Authorized, isolated laboratory

Status: TECHNICAL INVESTIGATION COMPLETE - TECHNICAL REVIEW ACCEPTANCE AND FORMAL DISPOSITION PENDING

## Mission

Investigate AWS CloudTrail, Kubernetes security monitoring,
and Linux host events to determine whether their activity
is related, unrelated, or inconclusive.

Do not infer causation from timestamps alone.

## Investigation Components

- AWS identity and S3 activity investigation
- Kubernetes runtime and workload investigation
- Linux authentication and persistence investigation
- Python cross-system event correlation engine
- Adversarial test scenarios
- Containment stop-gate decision
- Detection engineering
- Recovery and operational readiness
- Final incident disposition

## Repository Structure

- incident-report/
- evidence/aws/
- evidence/kubernetes/
- evidence/linux/
- correlation-engine/src/
- correlation-engine/tests/
- correlation-engine/sample-data/
- detection-engineering/detection-rules/
- detection-engineering/validation-results/
- adversarial-testing/
- operations/
- closure/
- notebook/

## Safety and Evidence Rules

1. Use only synthetic or explicitly authorized data.
2. Never include live credentials or sensitive personal data.
3. Keep observed events separate from interpretations.
4. Preserve event identifiers and source timestamps.
5. Preserve original evidence when issuing corrections.
6. Document alternative incident hypotheses.
7. Do not perform destructive containment in real systems.
8. Label untested claims and unsupported relationships.
9. Record actual session durations; do not estimate hours
   from file timestamps.
10. Keep production-readiness conclusions evidence-based.

## Technical investigation status and disposition

**Technical investigation:** COMPLETE for the documented synthetic-evidence review and authorized isolated-laboratory validation. The GitHub project is a technical portfolio artifact, not evidence that a production incident was confirmed or formally closed. Shared IP addresses and timing are leads; they do not establish a single causal AWS/Kubernetes/Linux attack chain.

**Technical review acceptance:** PENDING. The investigation materials and engineering validations are available for review; acceptance by an authorized technical reviewer has not been established.

**Formal incident disposition and closure:** PENDING AUTHORIZED DECISION. Technical completeness or technical-review acceptance must not be conflated with formal incident closure. No production containment, production recovery, or final incident closure authorization has been documented or executed.

## Reproduction - correlation-engine unit tests

Use Python 3 from the **Ticket #011 project directory**. The test file requires the project-root path as its first positional argument; running unittest discovery without that argument is not an equivalent invocation. Only Python standard-library modules are needed for this recorded test suite.

```powershell
$projectRoot = (Get-Location).Path
python -B .\correlation-engine\tests\test_ticket011_correlate_9c.py "$projectRoot"
```

Expected result: `Ran 20 tests` followed by `OK`. The `-B` switch suppresses Python bytecode cache generation. The separately recorded historical result is at `correlation-engine/tests/unit-test-results-9c.txt`. These 20 engineering unit tests are **not** the eight-case adversarial acceptance rubric.

## Eight-case acceptance evidence - provisional

Eight adversarial cases (AT-01 through AT-08) are documented. The evidence distinguishes **four authorization simulations** (Kubernetes SelfSubjectAccessReview checks recording permission decisions) from **four actually executed isolated-laboratory runtime tests** with observed outcomes. An authorization simulation is not an executed privileged attack, and execution does not imply success. The technical matrix, RBAC mapping, and associated security evidence document the individual outcomes and limitations.

**Formal eight-case acceptance remains PROVISIONAL / PENDING** until the authoritative acceptance rubric is supplied and the cases are reviewed against it. Do not report eight successful runtime attacks or treat technical documentation as reviewer sign-off.

## Containment decision gate - unresolved 09:05 reference

The recorded **09:05** containment decision reference has **no confirmed calendar date, timezone, or authorized decision-maker approval**. It must not be promoted to a full timestamp, converted to UTC, or represented as an approved production action without independent documentation. Disruptive production containment remains withheld pending authorization. The recovery plan is a runbook, not proof of an executed production recovery.

See `incident-report/containment-decision-memorandum-10a.md`, `incident-report/closure-readiness-12a.json`, and `incident-report/submission-readiness-12b.md` for the supporting decision and readiness records.
