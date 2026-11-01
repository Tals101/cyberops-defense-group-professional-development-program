# Ticket #010 - Production Readiness Recommendation

## Decision

**NOT READY - DO NOT APPROVE PRODUCTION DEPLOYMENT.**

Assessment date: November 1, 2026.

Application: ledger-api.

This is an engineering readiness recommendation
for the synthetic Ticket #010 incident scenario.
It is not evidence of an actual production change.

## Executive Assessment

The project demonstrates multiple successful
laboratory security tests and a verified
Kubernetes configuration rollback.

The evidence also identifies unresolved release,
provenance, and operational recovery requirements.

Accordingly, the project supports technical
closure of the documented laboratory activities
but not approval of a production release.

## Verified Laboratory Outcomes

### Baseline Investigation

The unsafe baseline configuration was accepted
by Kubernetes server-side validation.

Security scans identified additional configuration
and image-vulnerability issues.

These findings established a gap between ordinary
validation and release security.

### V1 - Policy and Pipeline Controls

Policy, scanner, and pipeline behavior was
evaluated using positive and negative scenarios.

The results demonstrate the need to verify
actual release decisions, not merely findings.

### V2 - Kubernetes Admission Controls

Restricted Pod Security Admission and custom
image-reference policy behavior were evaluated.

The original custom image-reference policy
was scoped to ticket-010-lab.

Evidence does not establish that this exact
policy protects an intended production namespace.

### V3 - Artifact and Trust Controls

Image integrity, trust, signing, and release
decisions were evaluated in the laboratory.

These results do not independently establish
production-approved signer identity,
provenance, or production authorization.

### Adversarial Testing

Total consolidated scenarios: 13.

Verified outcomes: 12.

Outstanding review outcomes: 1.

A02 requires direct evidence of the release-gate
decision for its exact fixture.

### Recovery Rehearsal

A deliberately unhealthy Deployment revision
was created in an isolated namespace.

The attempted rollout timed out.

The healthy prior configuration was restored
through an explicit rollback command.

The restored workload passed an independent
application-health check.

The isolated namespace was subsequently deleted.

This verifies configuration rollback only.

## Unresolved Release and Recovery Risks

### 1. Exact Fixture Enforcement

The A02 finding remains open for review.

Scanner detection does not substitute for
a proven failed release-gate result.

### 2. Artifact Identity and Provenance

The Docker Desktop image ID differed from the
image ID installed in Minikube.

The correct Minikube runtime identity was
observed through the rollback exercise, but
end-to-end image provenance remains unproven.

### 3. Production Admission Enforcement

The custom image-reference policy's original
namespace scope does not establish enforcement
for production.

The production policy scope, supported workload
paths, and failure behavior require validation.

### 4. Production-Equivalent Artifact Trust

Local signing or verification must not be treated
as production-approved signer trust.

Approved identity, immutable image references,
and an auditable provenance chain are required.

### 5. Recovery Completeness

The successful rehearsal restored a readiness
configuration without switching application
image versions.

Application image rollback, data restoration,
and production-equivalent recovery remain untested.

Residual risk R06 remains OPEN.

### 6. Configuration Management

kubectl rollout undo produced a
last-applied-configuration warning.

Future declarative updates require reconciliation
against the intended recovered configuration.

## Conditions for Reconsidering Production Approval

The following items require independently
recorded evidence and authorized review.

1. Verify blocking behavior for the exact A02
   fixture and document the gate's exit result.
2. Validate all required policy and admission
   controls in the intended deployment scope.
3. Establish immutable build-to-runtime image
   identity and approved artifact provenance.
4. Validate approved signing identities and
   fail-closed trust enforcement.
5. Demonstrate a production-equivalent release
   with preserved positive and negative tests.
6. Demonstrate application image-version rollback.
7. Validate backup and data restoration if the
   production application has persistent state.
8. Reconcile declarative configuration after
   rollback and test subsequent release behavior.
9. Assign owners and acceptance criteria to
   unresolved residual risks, including R06.
10. Obtain the required operational, security,
    and release approvals before deployment.

These conditions are acceptance criteria,
not claims of completed work.

## Operational Disposition

Laboratory technical work: DOCUMENTED.

Isolated configuration rollback: VERIFIED.

Isolated rollback namespace cleanup: VERIFIED.

Adversarial matrix: 12 VERIFIED, 1 REVIEW.

End-to-end artifact provenance: NOT ESTABLISHED.

Image-version rollback: NOT TESTED.

Production recovery: NOT TESTED.

Residual risk R06: OPEN.

Production release approval: WITHHELD.

## Final Recommendation

Maintain a production deployment hold.

Preserve the existing incident, engineering,
security, and rollback evidence.

Treat successful laboratory outcomes as evidence
of specific controls tested, not as proof that
the entire release and recovery process is secure.

Reassess production readiness only after the
outstanding acceptance criteria are satisfied
and formally approved.

**FINAL DECISION: NOT READY.**

## Supporting Evidence

- README.md
- tests/adversarial-test-matrix.csv
- investigation/stop-gate-1-report.md
- investigation/v1-security-control-assessment.md
- investigation/v2-admission-security-assessment.md
- investigation/v3-engineering-assessment.md
- evidence/v3-final-release-regression.csv
- recovery/recovery-and-rollback-assessment.md
- recovery/rollback-rehearsal-evidence.txt
- recovery/rollback-final-verification.txt
- recovery/rollback-cleanup-verification.txt
- operations/operational-runbook.md
- operations/residual-risk-register.csv
- closure/v3-ticket-closure-report.md
