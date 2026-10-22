# Ticket #009 — Automation Safeguard Register

## Purpose

Maintain a traceable register of safeguards introduced or proposed during the redesign of identity-remediation automation.

## Status Definitions

- TESTED — Implemented and validated in the laboratory.
- ISOLATED TEST — Validated in a separate test workflow but not integrated into canonical V3 enforcement.
- REQUIRED — Necessary for production but not yet independently validated.

## Safeguard Register

| ID | Safeguard | Risk Addressed | Status | Evidence |
|---|---|---|---|---|
| SG-01 | Identity-type classification | Service accounts treated as inactive employees | TESTED | F09 unsupported identity test |
| SG-02 | Secondary evidence corroboration | Misleading primary IAM records | TESTED | V3 decision records and payroll conflict |
| SG-03 | Dependency and criticality checks | Business application disruption | TESTED | payroll.emergency decision |
| SG-04 | Evidence completeness validation | Missing data creating false confidence | TESTED | F01 missing-data correction |
| SG-05 | Protected source-integrity baseline | Secondary evidence poisoning | TESTED | A01 corrective validation |
| SG-06 | Independent observation-timestamp validation | Forged evidence freshness | TESTED | A02 corrective validation |
| SG-07 | Audit logging preflight | Actions without reliable audit evidence | TESTED | F03 logging failure correction |
| SG-08 | Fail-closed invalid input handling | Unobservable input-processing failures | TESTED | F02 corrupted-input correction |
| SG-09 | Dry-run default | Unintended destructive execution | TESTED | Canonical V3 dry-run decisions |
| SG-10 | Emergency stop | Continued execution during unsafe conditions | TESTED IN V2 | V2 emergency-stop tests |
| SG-11 | Idempotent execution | Duplicate remediation | ISOLATED TEST | F04 duplicate execution |
| SG-12 | Interrupted-run recovery | Unsafe restart behavior | ISOLATED TEST | F05 interrupted execution |
| SG-13 | Remediation failure handling | Partial or failed state changes | ISOLATED TEST | F06 failed remediation |
| SG-14 | Rollback and escalation | Inability to restore account state | ISOLATED TEST | F07 failed rollback |
| SG-15 | Approval timeout handling | Stale pending approvals | ISOLATED TEST | F08 approval timeout |
| SG-16 | Signed and transaction-bound approvals | Forged or mismatched authorization | ISOLATED TEST | A03 corrective validation |
| SG-17 | One-time-use approval ledger | Approval replay | ISOLATED TEST | A03 consumption evidence |
| SG-18 | Production credential separation | Excessive automation privileges | REQUIRED | Least-privilege analysis |
| SG-19 | Protected approval and audit infrastructure | Unauthorized alteration of authorization or evidence | REQUIRED | A03 production limitations |
| SG-20 | Continuous evidence refresh and drift monitoring | Stale decisions and changing identity context | REQUIRED | Phase 13 operations planning |

## Safeguard Dependencies

Several safeguards depend on other controls.

For example:

- Source-integrity verification depends on protecting the expected hash from unauthorized changes.
- Freshness verification depends on trustworthy observation timestamps.
- Approval signature verification depends on independent signing-key custody.
- Replay protection depends on a durable, protected consumption ledger.
- Rollback depends on trustworthy snapshots and separately authorized recovery access.
- Audit logging must remain available before destructive execution is considered.

A successful unit test does not establish that these external dependencies are secure in production.

## Safeguard Failure Policy

When a mandatory safeguard fails:

1. Do not perform destructive remediation.
2. Preserve available evidence.
3. Record the failed safeguard and reason.
4. Notify the appropriate operator.
5. Require investigation and explicit authorization before resuming.

The system must not silently downgrade safety requirements to keep remediation running.

## Known Limitations

Canonical V3 is a dry-run decision engine.

The approval, remediation-execution, replay-protection, and recovery tests use isolated laboratory workflows.

The controls have not been integrated and validated as one production enforcement system.

The canonical secondary evidence timestamps dated October 16, 2026 are also subject to the 24-hour freshness threshold and require authoritative refresh.

## Production Acceptance Criteria

Before enabling destructive automation:

- All REQUIRED safeguards must be implemented.
- Isolated safeguards must be integrated into the enforcement path.
- Production credentials must enforce least privilege.
- Approval issuance and remediation execution must have separate authority.
- Source integrity and evidence freshness must be validated.
- Audit and rollback controls must be tested together.
- Emergency-stop behavior must be verified.
- Independent security approval must be recorded.

## Current Recommendation

Full unattended destructive remediation remains NOT APPROVED.

Continue dry-run analysis, recommendations, and appropriately controlled human-approved procedures.

## Supporting Documents

- security/automation-authority-matrix.md
- security/automation-credential-analysis.md
- tests/v3-failure-injection-results.md
- tests/v3-adversarial-test-results.md
- management/production-recommendation.md
