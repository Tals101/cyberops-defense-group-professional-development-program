# Ticket #010 - Operational Security Runbook

## 1. Purpose and Scope

Application: ledger-api

This runbook documents the laboratory release-security controls
developed during Ticket #010.

Environment: Windows PowerShell, Ubuntu WSL2, Docker Desktop,
Minikube, Trivy, Syft, Cosign, and a local OCI registry.

Status: LABORATORY VALIDATED.

This document does not authorize production deployment.

## 2. Security Objectives

The release process should:

1. Identify the intended container by immutable digest.
2. Reject unsigned or unauthorized image signatures.
3. Block HIGH and CRITICAL vulnerability findings under
   the tested laboratory policy.
4. Reject invalid or stale vulnerability database metadata.
5. Preserve scanner reports and release-gate decisions.
6. Prevent unsafe workload settings through Kubernetes controls.

All relevant controls must pass for authorization.

## 3. Operational Preconditions

Before evaluating an artifact:

- Confirm the intended Docker and Kubernetes environments.
- Confirm the exact image digest and registry identity.
- Verify availability of the laboratory scanner and signing tools.
- Confirm that the approved signing public key is unchanged.
- Confirm the Trivy database is within the required freshness limit.
- Review the effective Kubernetes security policies.
- Confirm the intended deployment namespace.

Safe environment-inspection commands:

    kubectl config current-context
    kubectl cluster-info
    kubectl get namespace ticket-010-lab
    docker version
    trivy --version

These commands do not deploy or modify workloads.

Do not use the laboratory signing key or registry configuration
as production approval.

## 4. Release-Gate Procedures

Primary scripts:

- pipeline/v3-release-gate.ps1
- pipeline/v3-image-signature-gate.ps1
- pipeline/v3-vulnerability-gate.ps1
- pipeline/v3-trivy-db-freshness.ps1

Before rerunning, inspect the scripts and their documented
parameter requirements. Do not substitute a mutable image tag
for the recorded digest.

Expected exit-code interpretation for the tested gate:

- 0: All tested requirements passed.
- 1: Vulnerability policy blocked release.
- 2: Verification, scanning, or other gate error blocked release.

Unexpected errors must not be treated as release approval.

## 5. Release Decision Workflow

1. Verify the target digest and registry.
2. Validate authorized signing identity.
3. Validate vulnerability database freshness.
4. Run vulnerability evaluation.
5. Review the combined decision.
6. Preserve the exact image reference, tool outputs, and exit code.
7. Deploy only when independently authorized in the target environment.

A valid signature alone is insufficient.

## 6. Known Regression Tests

The final V3 regression is documented in:

- evidence/v3-final-release-regression.csv
- evidence/v3-final-release-regression.txt

Tested scenarios:

- Signed clean Alpine image: accepted.
- Unsigned image: rejected.
- Unauthorized vulnerable signer: rejected.
- Signed vulnerable image under isolated trust: blocked.

The vulnerable baseline had 44 HIGH findings in the
recorded regression. The tested clean candidate had
0 HIGH and 0 CRITICAL findings.

These results are historical laboratory observations,
not guarantees about future vulnerability intelligence.

## 7. Kubernetes Admission Controls

Reference implementation and evidence:

- admission/
- investigation/v2-admission-security-assessment.md
- evidence/v2-final-admission-audit.txt

Pod Security Admission addresses restricted workload settings.

The custom image-reference policy addresses image-reference
requirements. It does not independently verify Cosign signatures.

Verify actual policy enforcement in the target cluster before
relying on admission protection.

## 8. Failure Response

If signature verification fails:

- Stop the release.
- Check the approved signing identity and exact digest.
- Preserve the original failure output.
- Do not replace the trusted key merely to make the test pass.

If vulnerability policy fails:

- Stop the release.
- Preserve the Trivy JSON and gate output.
- Review affected components and available remediation.
- Rebuild and scan a new immutable candidate if required.

If the vulnerability database is stale:

- Stop the release.
- Refresh vulnerability intelligence through an approved process.
- Repeat all required checks on the intended artifact.

If deployment or admission fails:

- Preserve Kubernetes events and policy rejection messages.
- Verify context, namespace, and intended manifests.
- Do not disable the security policy solely to achieve deployment.

## 9. Recovery and Rollback

Existing baseline cleanup evidence:

- evidence/baseline-cleanup-verification.txt
- investigation/stop-gate-1-report.md

V2 cleanup observations are separately recorded in evidence/.

These records do not establish a complete rollback to a
previously verified application release.

Before any rollback in a target environment:

1. Identify the previously approved immutable image digest.
2. Confirm that a restore point or prior deployment state exists.
3. Obtain the required operational authorization.
4. Preserve the pre-recovery state and incident evidence.
5. Apply the authorized recovery procedure.
6. Verify workload health, security context, and image digest.
7. Record restoration evidence and final disposition.

A controlled rollback rehearsal must be completed before
claiming production rollback readiness.

## 10. Evidence Preservation

Primary records:

- investigation/v3-engineering-assessment.md
- evidence/v3-final-release-regression.csv
- evidence/v3-evidence-inventory.csv
- closure/v3-ticket-closure-report.md
- closure/v3-evidence-index.md

Do not edit historical command output merely to pass
formatting or whitespace checks.

Use SHA-256 verification to detect evidence changes.

Never place private signing keys or credentials in Git.

## 11. Escalation and Release Authority

A BLOCK or ERROR decision requires engineering investigation.

Production authorization requires independent approval,
a production-grade signing and registry configuration,
appropriate admission enforcement, and verified deployment
and rollback procedures.

Responsible production owners have not been assigned
within this laboratory project.

## 12. Current Disposition

Laboratory release-gate validation: PASSED.

Production deployment readiness: NOT ESTABLISHED.

Refer to operations/residual-risk-register.csv for open
risks and required closure evidence.
