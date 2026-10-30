# Ticket #010 - V3 Engineering Assessment

## Assessment Metadata

- Project: The Patch That Passed Every Check
- Application: ledger-api
- Assessment generated: 2026-10-29 15:13:29 -04:00
- Environment: Windows PowerShell, Ubuntu WSL2, Docker Desktop, local OCI registry
- Scope: Laboratory release-gate validation
- Status: Laboratory regression passed; production deployment not authorized

## 1. Executive Summary

Ticket #010 investigated a container release process in which successful deployment and basic checks did not establish that an application image was safe.

The V3 work introduced digest-pinned image references, CycloneDX software bills of materials, vulnerability scanning, database freshness checks, and Cosign signature verification.

The combined release gate was tested against four scenarios. Every scenario produced its expected decision.

The principal finding is that a valid cryptographic signature is not sufficient to authorize release. The vulnerable baseline image was correctly blocked even when signed by an identity explicitly trusted within an isolated test fixture.

## 2. Verified Image Security Findings

### Clean Alpine Candidate

- Image: 127.0.0.1:5500/ledger-api@sha256:47ef846c1cfb97f06eb12413ed6354f9a4e6ac41d6849af7f97d7ac64f0e507a
- HIGH vulnerabilities: 0
- CRITICAL vulnerabilities: 0
- Signature verification: Passed with the laboratory trusted key
- Release-gate decision: PASS

### Vulnerable Baseline

- Image: 127.0.0.1:5500/ticket010-vulnerable-step125@sha256:ee721dc86416dfd14bce41c1312674a2621b222f58a42312bb8e4d74f92334d3
- HIGH vulnerabilities: 44
- CRITICAL vulnerabilities: 0
- Cryptographic signature: Valid under isolated test identity
- Authorization by original trusted signer: Rejected
- Decision under isolated test trust: BLOCK due to vulnerabilities

Both vulnerability reports were checked against their respective immutable image references.

## 3. Final V3 Regression

| Scenario | Expected exit | Actual exit | Result |
|---|---:|---:|---|
| Signed clean Alpine | 0 | 0 | PASS |
| Unsigned image | 2 | 2 | PASS |
| Unauthorized vulnerable signer | 2 | 2 | PASS |
| Signed vulnerable isolated trust | 1 | 1 | PASS |

Exit-code convention:

- 0: All required release checks passed
- 1: Vulnerability policy blocked the image
- 2: Signature, scanning, or other gate error blocked authorization

All four tests passed. No unexpected release authorization occurred.

The regression also confirmed that the original pipeline scripts remained unchanged.

## 4. Implemented Security Controls

### Image Identity

Container images were published to a loopback-only OCI registry. Registry manifest digests were retrieved and independently checked against SHA-256 calculations.

### Software Bill of Materials

CycloneDX SBOMs were generated for both the baseline and Alpine container images using Syft.

### Vulnerability Policy

Trivy evaluated HIGH and CRITICAL vulnerabilities. The baseline demonstrated 44 HIGH findings, while the Alpine candidate had zero HIGH and zero CRITICAL findings in the final regression.

### Vulnerability Database Freshness

A database freshness policy rejects stale or invalid metadata. Earlier isolated negative testing confirmed that stale database metadata blocks an otherwise clean candidate.

### Signature Trust

Cosign verified container signatures against a pinned laboratory public key. An unsigned image and an image signed by an unauthorized key were both rejected.

### Combined Release Decision

The combined gate requires successful signature verification before running the vulnerability and database freshness checks.

The same digest-pinned image reference is passed between the signature and vulnerability controls.

## 5. Residual Risks and Limitations

1. The registry uses unauthenticated HTTP bound to loopback and is suitable only for this isolated laboratory.
2. Cosign transparency-log verification was intentionally bypassed for local testing.
3. Signing keys were temporary laboratory identities, not organization-managed production identities.
4. Pinning a public key hash inside a script is not an independently protected trust root.
5. The signature checks are not yet enforced through a deployed production CI/CD pipeline or admission controller.
6. The earlier Kubernetes admission policy validates allowed image-reference syntax; it does not independently verify Cosign signatures.
7. The earlier admission policy's illustrative registry allowlist differs from the local test-registry hostname.
8. The SBOMs provide inventory evidence but are not yet enforced as separate release-policy inputs.
9. Vulnerability findings depend on scanner version, vulnerability intelligence, and database freshness.
10. Local Docker image availability and local registry behavior do not prove production registry accessibility or production runtime readiness.
11. No production-grade image provenance or protected signing-key lifecycle has been established.

## 6. Engineering Decision

Laboratory V3 release-control validation: SUCCESSFUL.

Production release readiness: NOT ESTABLISHED.

The Alpine candidate passed the tested laboratory gate. The vulnerable baseline was blocked under an isolated trusted-signature scenario.

No production deployment is authorized by this assessment.

## 7. Recommended Follow-Up

- Integrate the release gate into the actual build and deployment workflow.
- Configure an authenticated TLS-protected production registry.
- Establish independently controlled and auditable signing identity management.
- Enforce signature and provenance policy at deployment admission.
- Align registry allowlists, image references, and deployment manifests.
- Test against the final production registry and immutable artifact.
- Preserve vulnerability reports, SBOMs, and policy decisions as release evidence.
- Retest rollback and failure-handling procedures in the target environment.

## 8. Evidence

Primary evidence:

- evidence/v3-final-release-regression.csv
- evidence/v3-final-release-regression.txt
- evidence/v3-signed-vulnerable-release-test.txt
- evidence/v3-cosign-unsigned-image-test.txt
- evidence/v3-final-vulnerability-regression.txt
- evidence/v3-evidence-inventory.csv

Supporting scripts and scanner artifacts are listed in the SHA-256 evidence inventory.
