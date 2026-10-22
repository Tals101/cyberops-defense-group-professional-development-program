# Ticket #009 — Phase 11 Adversarial Automation Test Results

## Purpose

Assess whether V3 identity remediation can be manipulated through
untrusted evidence, false freshness metadata, or forged approvals.

All testing used synthetic identities and isolated lab artifacts.

## Test Summary

| Test | Original Result | Corrective Result |
|---|---|---|
| A01 — Secondary Evidence Poisoning | FAIL | PASS |
| A02 — Freshness Metadata Forgery | FAIL | PASS |
| A03 — Approval Forgery and Replay | FAIL | PASS in isolated corrected test |

## A01 — Secondary Evidence Poisoning

### Original Weakness

Poisoned secondary context was made to agree with misleading
primary IAM evidence.

V3 incorrectly produced:

- Confidence: HIGH
- Evidence trust: TRUSTED
- Recommendation: DISABLE
- Authority: AUTO_REMEDIATE

### Corrective Control

V3 validates the secondary source against a protected SHA256
integrity baseline before generating decisions.

### Corrective Result

- Status: FAIL_CLOSED
- Failure: SECONDARY_SOURCE_INTEGRITY_FAILURE
- Decision records: 0
- Remediation performed: False

Result: PASS.

The original A01 report records the integrity baseline used at
that time. The canonical baseline was subsequently rotated during
A02 after the trusted secondary dataset was updated.

## A02 — Freshness Metadata Forgery

### Original Weakness

Secondary evidence observed on 2025-01-01 was falsely labeled
current.

V3 incorrectly classified the evidence as TRUSTED and granted
AUTO_REMEDIATE authority.

### Corrective Control

V3 now independently validates observed_at_utc and enforces
a maximum secondary evidence age of 24 hours for trusted
unattended destructive authority.

Missing, malformed, stale, or future timestamps cannot qualify
for trusted unattended authority.

### Corrective Result

- Evidence trust: STALE
- Recommendation: DISABLE
- Authority: REQUIRE_APPROVAL
- Actual action: NO_ACTION_DRY_RUN

Result: PASS.

The canonical lab timestamps dated 2026-10-16 require refresh
before they can satisfy the 24-hour freshness threshold again.
This will be addressed in Phase 13 operations and drift analysis.

## A03 — Approval Forgery and Replay

### Original Weakness

An unverified APPROVED value authorized a synthetic disable.

The generic approval reference GENERIC-APPROVAL-A03 was then
accepted twice for payroll.emergency after the working
identity state was reset.

Result: FAIL.

### Corrective Controls

The isolated corrected A03 workflow includes:

- structured approval artifact
- unique approval ID
- target identity binding
- requested action binding
- approved-by validation
- issuance and expiration checks
- HMAC-SHA256 integrity verification
- SQLite one-time-use approval ledger
- fail-closed behavior for missing verification key or ledger

### Corrective Validation

- Valid signed approval: PASS
- Approval replay blocked: PASS
- Signature tampering rejected: PASS
- Wrong identity rejected: PASS
- Action mismatch rejected after correction: PASS
- Expired approval rejected: PASS
- Missing signing key rejected: PASS
- Unavailable consumption ledger rejected: PASS

Approval APR-A03-001 was consumed once for nora.hayes.

Result: PASS for tested isolated scenarios.

The approval checks are not yet integrated into a production
identity-remediation enforcement service.

## Overall Security Findings

The adversarial tests demonstrated three independent trust-boundary
problems:

1. Corroboration does not prove source integrity.
2. A current freshness label does not prove evidence is recent.
3. An APPROVED value does not prove authentic, transaction-bound,
   single-use authorization.

Each original failure was preserved before correction.

## Remaining Risks

- Protected source-integrity metadata requires independent custody.
- Evidence timestamps must be refreshed by trustworthy sources.
- The lab HMAC signing arrangement is not a production approval service.
- The local SQLite consumption ledger is not tamper-resistant.
- Approval enforcement must be integrated with identity authority,
  dependency checks, audit logging, and recovery safeguards.
- Production permissions and operational controls remain unvalidated.

## Production Recommendation

Do not enable full unattended destructive identity remediation.

Continue with detection, recommendations, dry-run analysis,
and appropriately controlled human-approved remediation while
production-grade authorization and operations controls are developed.

## Supporting Evidence

### A01
- tests/a01-secondary-evidence-poisoning-finding.md
- tests/a01-secondary-evidence-poisoning-corrective-validation.md

### A02
- tests/a02-freshness-metadata-forgery-finding.md
- tests/a02-freshness-metadata-forgery-corrective-validation.md

### A03
- tests/a03-approval-forgery-replay-finding.md
- tests/a03-approval-forgery-replay-corrective-validation.md
- evidence/v3-a03-approval-consumption.csv

## Conclusion

Phase 11 adversarial testing reproduced and corrected the
tested evidence-integrity, freshness, and approval weaknesses.

These lab results do not establish production readiness.
Full unattended destructive remediation remains prohibited.
