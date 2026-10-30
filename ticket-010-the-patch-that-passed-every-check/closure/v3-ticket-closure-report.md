# Ticket #010 - V3 Closure Report

## 1. Closure Information

- Ticket: #010 - The Patch That Passed Every Check
- Application: ledger-api
- Date: 2026-10-29 15:16:52 -04:00
- Environment: Windows PowerShell, Ubuntu WSL2, Docker Desktop, Minikube
- Closure scope: Laboratory engineering validation
- Laboratory status: COMPLETED
- Production deployment authorization: NOT GRANTED

## 2. Incident Summary

The Ticket #010 scenario examined a deployment in which routine acceptance checks were insufficient to establish container security.

The documented scenario identified a ledger-api deployment dated October 22, 2026, followed by a security finding on October 23, 2026.

The original unsafe manifest included:

- Privileged container execution
- Execution as root
- Privilege escalation enabled
- Mutable container image tag

The investigation demonstrated that successful Kubernetes manifest acceptance does not, by itself, establish workload safety.

This report describes a controlled laboratory investigation. It does not establish the occurrence or resolution of a production incident.

## 3. Root Cause and Contributing Factors

### Engineering Assessment

The laboratory scenario exposed a release-assurance gap: deployment validation did not initially provide sufficient independent enforcement of runtime privileges, image integrity, vulnerability policy, and authorized signing identity.

Contributing weaknesses included:

- Excessive container privileges
- Mutable image identity
- Reliance on deployment or admission acceptance as evidence of safety
- Lack of integrated signature and vulnerability authorization
- Insufficient distinction between scanner success and policy compliance

These findings describe the laboratory failure model, not a forensically proven production root cause.

## 4. Implemented Laboratory Controls

### Kubernetes Controls

Pod Security Admission and image-reference ValidatingAdmissionPolicy testing provided independent checks for restricted workload settings and approved image-reference syntax.

### Software Supply Chain

Syft generated CycloneDX SBOMs for baseline and Alpine candidate images.

Registry manifest digests were independently verified using SHA-256.

### Vulnerability Enforcement

Trivy assessed HIGH and CRITICAL vulnerability findings.

A freshness control prevented acceptance when the vulnerability database metadata failed laboratory requirements.

### Cryptographic Signature Enforcement

Cosign verified image signatures against a pinned laboratory public key.

Unsigned images and images with unauthorized signing identities were rejected.

### Combined Release Authorization

The final release gate required signature verification, vulnerability evaluation, and database freshness for the same digest-pinned image reference.

## 5. Final Regression Results

| Scenario | Exit code | Test result |
|---|---:|---|
| Signed clean Alpine | 0 | PASS |
| Unsigned image | 2 | PASS |
| Unauthorized vulnerable signer | 2 | PASS |
| Signed vulnerable isolated trust | 1 | PASS |

Clean Alpine candidate: 0 HIGH, 0 CRITICAL findings.

Vulnerable baseline: 44 HIGH, 0 CRITICAL findings.

All four scenarios produced the expected decisions.

The vulnerable baseline was blocked even when its signature was valid under an isolated test trust identity.

## 6. Evidence and Integrity

- SHA-256 evidence inventory entries verified: 24
- Final regression cases verified: 4
- Primary assessment: investigation/v3-engineering-assessment.md
- Evidence inventory: evidence/v3-evidence-inventory.csv
- Regression report: evidence/v3-final-release-regression.txt

The full evidence map is provided in closure/v3-evidence-index.md.

## 7. Residual Risks

The following are not established by laboratory success:

- Production CI/CD enforcement
- Production-managed signing identities and key custody
- An authenticated, TLS-protected production registry
- Transparency-log-backed production verification
- Signature-verifying Kubernetes admission enforcement
- Complete production provenance and SBOM policy
- Production deployment, runtime health, and rollback validation

The existing admission policy checks image-reference syntax rather than independently verifying Cosign signatures.

## 8. Corrective Recommendations

1. Integrate the release gate into an actual CI/CD deployment workflow.
2. Protect signing identities and establish independent signer authorization.
3. Use a production registry with authentication and TLS.
4. Enforce signed-artifact provenance at deployment admission.
5. Require immutable image identity throughout build, scan, and deploy.
6. Preserve vulnerability and SBOM reports as release evidence.
7. Validate the deployment and rollback process in the target environment.
8. Recheck vulnerability intelligence before any future release decision.

## 9. Engineering Closure Decision

LABORATORY VALIDATION: SUCCESSFUL.

FINAL REGRESSION: 4 OF 4 PASSED.

PRODUCTION RELEASE: NOT AUTHORIZED.

The laboratory work demonstrated that the configured release gate can reject unsigned, unauthorized, and vulnerable images while accepting the tested signed Alpine candidate.

Ticket #010 V3 laboratory validation may be closed with documented residual production requirements.
