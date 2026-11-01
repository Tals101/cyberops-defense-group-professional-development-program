# Ticket #010 - Adversarial Testing Matrix

## Scope and Status

Thirteen baseline, V1, V2 and V3 laboratory test scenarios.
Twelve recorded outcomes are verified against supporting evidence.

A01 demonstrates unsafe baseline acceptance, not secure deployment.
A02 remains under review: 14 Trivy findings were recorded,
but the exact privileged-init fixture gate decision is unconfirmed.

A03 records an explicit laboratory allowlist PASS while retaining
the separate Trivy untrusted-registry finding.

## Test Results

| ID | Phase | Scenario | Actual | Status |
|---|---|---|---|---|
| A01 | Baseline | Unsafe Deployment accepted by baseline validation | Unsafe Deployment accepted by server dry-run; exit 0 | PASS - VERIFIED |
| A02 | V1 | Privileged init-container attack | Trivy detected 14 misconfigurations; release-gate enforcement not established by cited JSON | REVIEW - DETECTION ONLY |
| A03 | V1 | Approved registry positive control | V1 explicit registry allowlist passed; separate Trivy untrusted-registry finding retained | PASS - VERIFIED |
| A04 | V2 | Unsafe Pod Security Admission request | Unsafe Pod rejected by restricted Pod Security Admission; exit 1 | PASS - VERIFIED |
| A05 | V2 | Unapproved container registry | Unapproved registry rejected by ValidatingAdmissionPolicy; exit 1 | PASS - VERIFIED |
| A06 | V2 | Unapproved ephemeral container | Unapproved ephemeral-container patch denied by admission policy | PASS - VERIFIED |
| A07 | V2 | Approved ephemeral container positive control | Approved ephemeral-container patch accepted | PASS - VERIFIED |
| A08 | V3 | Stale vulnerability database | Stale vulnerability database rejected; exit 2 | PASS - VERIFIED |
| A09 | V3 | Vulnerability scanner failure | Scanner failure blocked release; exit 2 | PASS - VERIFIED |
| A10 | V3 | Signed clean Alpine | Exit 0 | PASS - VERIFIED |
| A11 | V3 | Unsigned image | Exit 2 | PASS - VERIFIED |
| A12 | V3 | Unauthorized vulnerable signer | Exit 2 | PASS - VERIFIED |
| A13 | V3 | Signed vulnerable isolated trust | Exit 1 | PASS - VERIFIED |

## Evidence References

### A01 - Unsafe Deployment accepted by baseline validation

- Expected: Acceptance demonstrates the original control gap
- Actual: Unsafe Deployment accepted by server dry-run; exit 0
- Input: kubernetes/ledger-api-unsafe-lab.yaml
- Evidence: evidence/baseline-server-dry-run.txt
- Status: PASS - VERIFIED

### A02 - Privileged init-container attack

- Expected: BLOCK
- Actual: Trivy detected 14 misconfigurations; release-gate enforcement not established by cited JSON
- Input: tests/v1-privileged-init-attack.yaml
- Evidence: evidence/v1-preflight-privileged-init.json
- Status: REVIEW - DETECTION ONLY

### A03 - Approved registry positive control

- Expected: ALLOW when other policy conditions pass
- Actual: V1 explicit registry allowlist passed; separate Trivy untrusted-registry finding retained
- Input: tests/v1-approved-registry-test.yaml
- Evidence: evidence/v1-integrated-approved.txt
- Status: PASS - VERIFIED

### A04 - Unsafe Pod Security Admission request

- Expected: BLOCK
- Actual: Unsafe Pod rejected by restricted Pod Security Admission; exit 1
- Input: tests/v2-psa-unsafe-pod.json
- Evidence: evidence/v2-psa-unsafe-pod-rejection.txt
- Status: PASS - VERIFIED

### A05 - Unapproved container registry

- Expected: BLOCK
- Actual: Unapproved registry rejected by ValidatingAdmissionPolicy; exit 1
- Input: tests/v2-unapproved-registry-pod.json
- Evidence: evidence/v2-unapproved-registry-rejection.txt
- Status: PASS - VERIFIED

### A06 - Unapproved ephemeral container

- Expected: BLOCK
- Actual: Unapproved ephemeral-container patch denied by admission policy
- Input: tests/v2-unapproved-ephemeral-patch.json
- Evidence: evidence/v2-ephemeral-subresource-test.txt
- Status: PASS - VERIFIED

### A07 - Approved ephemeral container positive control

- Expected: ALLOW when other conditions pass
- Actual: Approved ephemeral-container patch accepted
- Input: tests/v2-approved-ephemeral-patch.json
- Evidence: evidence/v2-ephemeral-positive-test.txt
- Status: PASS - VERIFIED

### A08 - Stale vulnerability database

- Expected: BLOCK
- Actual: Stale vulnerability database rejected; exit 2
- Input: tests/v3-stale-db-fixture/evidence/v3-gate-stale-fixture.json
- Evidence: evidence/v3-stale-database-gate-test.txt
- Status: PASS - VERIFIED

### A09 - Vulnerability scanner failure

- Expected: BLOCK
- Actual: Scanner failure blocked release; exit 2
- Input: pipeline/v3-vulnerability-gate.ps1
- Evidence: evidence/v3-scanner-failure-test.txt
- Status: PASS - VERIFIED

### A10 - Signed clean Alpine

- Expected: Exit 0
- Actual: Exit 0
- Input: pipeline/v3-release-gate.ps1
- Evidence: evidence/v3-release-regression-clean.txt
- Status: PASS - VERIFIED

### A11 - Unsigned image

- Expected: Exit 2
- Actual: Exit 2
- Input: pipeline/v3-release-gate.ps1
- Evidence: evidence/v3-release-regression-unsigned.txt
- Status: PASS - VERIFIED

### A12 - Unauthorized vulnerable signer

- Expected: Exit 2
- Actual: Exit 2
- Input: pipeline/v3-release-gate.ps1
- Evidence: evidence/v3-release-regression-untrusted.txt
- Status: PASS - VERIFIED

### A13 - Signed vulnerable isolated trust

- Expected: Exit 1
- Actual: Exit 1
- Input: pipeline/v3-release-gate.ps1
- Evidence: tests/v3-step127-isolated-trust/evidence/v3-release-regression-vulnerable.txt
- Status: PASS - VERIFIED

## Scope Limitation

The results demonstrate laboratory behavior only.
Production deployment and rollback remain unverified.
