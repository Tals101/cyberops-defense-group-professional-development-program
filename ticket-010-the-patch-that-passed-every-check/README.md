# Ticket #010 - The Patch That Passed Every Check

## Project Overview

This project investigates a security-control failure
in the release process for a synthetic ledger-api
application.

The incident scenario describes a production Deployment
that passed existing checks despite unsafe container
and Kubernetes security settings.

The engineering work evaluates how layered DevSecOps
controls can detect and prevent similar releases.

**Final production-readiness decision: NOT READY.**

Laboratory success does not authorize production deployment.

## Incident Scenario

Application: ledger-api

Namespace in the reported incident: production

Reported deployment:
October 22, 2026, 21:47

Reported security finding:
October 23, 2026, 08:15

The baseline configuration included:

- A mutable image tag.
- Privileged container execution.
- Root execution.
- Privilege escalation enabled.
- Insufficient release-security enforcement.

The production incident details are the supplied
investigation scenario. This repository does not
establish that production recovery was performed.

## Engineering Objectives

1. Preserve and investigate the unsafe baseline.
2. Identify gaps in existing validation and scanning.
3. Test policy and pipeline release gates.
4. Evaluate Kubernetes admission enforcement.
5. Test image-integrity and signer-trust decisions.
6. Verify relevant adversarial scenarios.
7. Demonstrate a controlled laboratory rollback.
8. Document remaining risks and production requirements.

## Engineering Workstreams

### Baseline Investigation

The initial Kubernetes server-side validation accepted
the unsafe workload configuration.

Independent security scanning identified additional
configuration and image-vulnerability findings.

These results demonstrate that Kubernetes schema
validation alone is not a security approval.

See:

- investigation/initial-investigation.md
- investigation/stop-gate-1-report.md
- notebook/engineering-notebook.md

### V1 - Policy and Pipeline Validation

The V1 workstream evaluates configuration security,
scanner behavior, and release decisions.

A scanner finding must be evaluated separately
from evidence that a release gate actually blocked
the corresponding fixture.

See:

- investigation/v1-security-control-assessment.md
- policies/
- pipeline/
- evidence/

### V2 - Kubernetes Admission Controls

The V2 workstream evaluates restricted Pod Security
Admission and custom image-reference validation.

Tests include workload admission, image-reference
decisions, and relevant subresource behavior.

The custom image-reference policy in the original
laboratory was scoped to ticket-010-lab.

Do not assume that policy protects every namespace.

See:

- investigation/v2-admission-security-assessment.md
- admission/
- kubernetes/
- evidence/

### V3 - Artifact Integrity and Release Decisions

The V3 workstream evaluates release-image identity,
signing, signer trust, vulnerability decisions,
and supporting release-control behavior.

Results are limited to the trust configuration
and artifacts actually tested.

Laboratory signature verification does not prove
production provenance or deployment authorization.

See:

- investigation/v3-engineering-assessment.md
- supply-chain/
- pipeline/
- evidence/v3-final-release-regression.csv

## Adversarial Test Results

The consolidated matrix contains 13 scenarios.

- 12 scenarios have verified supporting outcomes.
- 1 scenario remains under review.

The unresolved scenario is A02.

The available record does not independently prove
that the exact A02 fixture was blocked by the
release gate, despite scanner findings.

See:

- tests/adversarial-test-matrix.csv
- tests/adversarial-test-matrix.md

## Recovery and Rollback Rehearsal

On November 1, 2026, a dedicated laboratory
namespace was used to rehearse Deployment rollback.

The initial application returned HTTP 200 from
its /health endpoint.

A new Deployment revision deliberately changed
the readiness port from 8080 to 18081.

The new Pod failed readiness, and the updated
rollout timed out.

The original healthy Pod remained available.

A kubectl rollout undo command succeeded.

The restored configuration was assigned revision 3.

The application again returned HTTP 200.

An independent verification confirmed the healthy
configuration and unchanged Minikube runtime image ID.

The dedicated rollback namespace was subsequently
deleted and its removal verified.

### Recovery Limitations

- This was a configuration rollback, not an
  image-version rollback.
- Production rollback was not performed.
- Database restoration was not tested.
- Docker Desktop and Minikube image IDs differed.
- Complete image provenance was not established.
- The separate rollback namespace was outside
  the custom V2 image-reference policy binding.
- A kubectl rollout undo warning identified a
  last-applied-configuration annotation concern.

Residual risk R06 remains OPEN.

See:

- recovery/recovery-and-rollback-assessment.md
- recovery/rollback-rehearsal-evidence.txt
- recovery/rollback-final-verification.txt
- recovery/rollback-cleanup-verification.txt

## Repository Organization

| Directory | Purpose |
| --- | --- |
| investigation/ | Incident findings and engineering assessments |
| notebook/ | Original notebook and supplemental work records |
| application/ | Synthetic application and container build files |
| pipeline/ | Release-gate and pipeline materials |
| kubernetes/ | Kubernetes configuration and test workloads |
| policies/ | Policy-as-code materials |
| admission/ | Kubernetes admission-control materials |
| supply-chain/ | Artifact integrity and trust controls |
| tests/ | Adversarial scenarios and validation results |
| evidence/ | Preserved test outputs and technical artifacts |
| recovery/ | Rollback assessment, tests, and cleanup evidence |
| operations/ | Operating runbook and residual risk register |
| closure/ | Closure reports and engineering lessons |

## Laboratory Environment

The work used local development tools including:

- Windows PowerShell
- Docker Desktop
- Minikube
- kubectl
- Trivy
- Git
- Supporting security and supply-chain tools

Exact installed versions and test-specific limitations
should be verified in the underlying evidence.

No production credentials or production environment
are required to review the preserved results.

## Review and Reproduction Guide

### 1. Review the Baseline

Read the original engineering notebook and
incident assessment before running any tools.

Compare the unsafe configuration with the
recorded Kubernetes validation and Trivy results.

Do not deploy the unsafe baseline to production.

### 2. Verify Local Tool Availability

From PowerShell, confirm the available tools:

    docker version
    kubectl version --client
    minikube version
    trivy --version
    git --version

These commands identify local capabilities.
They do not reproduce historical test outcomes.

### 3. Verify Kubernetes Target

Before any new laboratory test, run:

    kubectl config current-context
    kubectl get namespaces

Use a disposable Minikube environment and
a dedicated laboratory namespace.

Never assume that the current Kubernetes
context points to Minikube.

### 4. Review V1 and V2 Controls

Review the policy and admission manifests,
associated assessments, and their evidence.

Test only in a disposable environment.

Confirm the scope of any ValidatingAdmissionPolicy
binding and the applicable Pod Security Admission
labels before interpreting admission outcomes.

Do not weaken an existing security policy merely
to make an unsafe workload deploy successfully.

### 5. Review V3 Release-Gate Evidence

Review the integrity, trust, scanner, and
release-regression records.

Use the stored negative controls to distinguish
successful detection from verified release blocking.

Do not assume that local trust material establishes
a production-approved signing identity.

### 6. Review the Adversarial Matrix

Open:

    tests/adversarial-test-matrix.csv

Compare each scenario with the cited evidence.

A02 remains unresolved until the exact
release-gate result is independently established.

### 7. Review the Rollback Rehearsal

Read the initial baseline, controlled-failure,
rollback, independent-verification, and cleanup
records in recovery/.

The original rollback namespace has already
been deleted.

A new rehearsal requires an explicitly isolated
namespace and separate preflight validation.

Do not blindly reapply historical manifests.

### 8. Confirm Closure Limitations

Review the residual risk register and
operational runbook before considering
any future deployment.

Production readiness must be established through
additional controlled tests and explicit approval.

## Evidence and Record Integrity

Original investigation evidence is preserved.

Newer assessments and supplemental notes are
separate from the original historical records.

The original engineering notebook remains unchanged.

Actual working hours were not fully recorded.
No durations were inferred from Git commits or
evidence timestamps.

See:

- notebook/engineering-notebook-supplement.md
- notebook/session-time-ledger.csv

## Operational Documentation

The operating runbook is located at:

- operations/operational-runbook.md

The residual risk register is located at:

- operations/residual-risk-register.csv

The final recovery assessment is located at:

- recovery/recovery-and-rollback-assessment.md

The earlier V3 closure report is located at:

- closure/v3-ticket-closure-report.md

## Final Engineering Assessment

The project demonstrates several working layers
of laboratory security testing and an independently
verified configuration rollback.

It does not demonstrate complete production-grade
release provenance, production rollback, or final
resolution of every adversarial scenario.

**Production readiness: NOT ESTABLISHED.**

**Recommendation: Do not approve production deployment
until outstanding controls, recovery testing,
and operational approvals are completed.**
