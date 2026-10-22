# Ticket #009 — V1/V2/V3 Engineering Comparison

## Purpose

Compare the original identity-remediation automation with the V2 and V3 redesigns.

This comparison documents engineering improvements, observed failures, corrective testing, and remaining production limitations.

## 1. Executive Comparison

| Area | V1 | V2 | V3 |
|---|---|---|---|
| Primary approach | Interactive-login inactivity | Identity-aware decisions | Identity context plus evidence trust |
| Identity classification | Inadequate | Explicitly evaluated | Evaluated with corroborating context |
| Business dependencies | Insufficiently considered | Dependency-aware decisions | Secondary-source conflict detection |
| Decision confidence | Not adequately established | Confidence assessment | Confidence separated from evidence trust |
| Source integrity | Not established | Limited | SHA256 baseline validation |
| Evidence freshness | Insufficient | Freshness considered | Independent observation-age validation |
| Automation authority | Excessive destructive authority | Bounded authority classifications | Authority adjusted for evidence trust |
| Approval protection | Inadequate | Approval boundaries introduced | Signed approval tested separately |
| Audit and failure handling | Limited | Fail-safe controls tested | Additional failure injection |
| Rollback | Inadequate | Laboratory rollback tested | Recovery and rollback-failure testing |
| Execution | Unsafe disable reproduced | Bounded laboratory enforcement | Canonical implementation dry-run only |
| Production status | Unsafe | Not approved | Not approved |

## 2. V1 — Original Automation

### Objective

Disable identities appearing inactive under a 90-day interactive-login threshold.

### Observed Result

The synthetic V1 execution disabled five identities, including svc_finance_batch.

The account supported Finance LedgerBridge and Finance Settlement Processor.

The subsequent synthetic Finance application-health check reported:

APPLICATION_STATUS=FAILED

### Root Cause

The automation treated interactive inactivity as equivalent to lack of business use.

It possessed destructive authority without sufficient identity classification, dependency awareness, or independent approval controls.

### Disposition

FAIL — Unsafe for unattended destructive remediation.

## 3. V2 — Authority and Execution Redesign

### Improvements

V2 introduced:

- Identity classification and contextual evaluation
- Decision confidence
- AUTO_REMEDIATE, REQUIRE_APPROVAL, and DO_NOT_AUTOMATE
- Protected identity treatment
- Approval boundaries
- Per-run action limits
- Dry-run execution
- Structured decision and audit records
- Prechange snapshots
- Rollback and service-health validation
- Emergency-stop behavior
- Persistent deferred-action controls

### Significant Discovery

The original run limit did not adequately restrict repeated executions.

A subsequent run could automatically disable an account that had been deferred during the first run.

This T12 failure was preserved, corrected, and retested.

### Result

V2 demonstrated improved authority boundaries and execution safety in the laboratory.

However, stronger execution safeguards did not establish the trustworthiness of the underlying identity evidence.

### Disposition

Safer in the tested laboratory scenarios; not approved for unattended destructive production remediation.

## 4. V3 — Evidence Trust Redesign

### Objective

Prevent unreliable, conflicting, altered, or stale evidence from granting excessive remediation authority.

### Improvements

V3 introduced:

- Secondary-source corroboration
- Separate decision-confidence and evidence-trust assessments
- Conflicting evidence classifications
- Source-integrity validation
- Observation-timestamp freshness checks
- Fail-closed processing
- Expanded failure-injection testing

### Payroll Scenario

The primary record for payroll.emergency suggested an inactive employee identity.

Secondary evidence identified a critical payroll integration.

The historical decision demonstrated:

- Confidence: HIGH
- Evidence trust: CONFLICTING
- Authority: REQUIRE_APPROVAL
- Actual action: NO_ACTION_DRY_RUN

High decision confidence therefore did not override conflicting business evidence.

## 5. V3 Failure-Injection Testing

Ten scenarios were documented:

- F01 — Missing identity data
- F02 — Corrupted input
- F03 — Unavailable logging
- F04 — Duplicate execution
- F05 — Interrupted execution
- F06 — Failed remediation
- F07 — Failed rollback
- F08 — Approval timeout
- F09 — Unsupported identity type
- F10 — Missing secondary corroboration

Original failures and subsequent corrective tests were preserved.

These results demonstrate laboratory behavior, not complete production integration.

## 6. Adversarial Testing

### A01 — Evidence Poisoning

Original weakness:

An altered secondary source could produce TRUSTED evidence and AUTO_REMEDIATE authority.

Correction:

Validate secondary-source integrity against a protected SHA256 baseline.

### A02 — Freshness Forgery

Original weakness:

Stale observations labeled current could receive excessive trust.

Correction:

Independently validate observed_at_utc against a 24-hour freshness threshold.

### A03 — Approval Forgery and Replay

Original weakness:

A locally asserted APPROVED value and reusable generic approval permitted unsafe synthetic enforcement.

Correction:

An isolated test implementation introduced signed, scoped, expiring, one-time-use approval verification.

This corrective approval workflow is not integrated into canonical V3 production enforcement.

## 7. Rollback and Recovery

V2 demonstrated restoration of synthetic identity state and application health.

V3 testing introduced additional failure scenarios, including a failed rollback requiring manual escalation.

Recovery must therefore be independently verified.

A documented rollback plan alone does not guarantee recovery.

## 8. Remaining Risks

The following remain unresolved for production:

1. Canonical V3 does not perform production enforcement.
2. Approval verification requires protected integration.
3. Production least-privilege permissions are unvalidated.
4. Integrity baselines require independent administration.
5. Evidence must be refreshed through authoritative sources.
6. Protected audit logging is not fully integrated.
7. Emergency stop and rollback require end-to-end testing.
8. Formal production authorization has not been granted.

Historical evidence dated October 16, 2026 has also exceeded the 24-hour freshness threshold.

Historical passing tests do not provide current execution authorization.

## 9. Final Engineering Assessment

V1 demonstrated that technically correct execution of an unsafe rule can disrupt legitimate business services.

V2 improved the separation between detection, decision, authorization, and execution.

V3 strengthened the evidence-trust boundary and exposed additional adversarial and operational risks.

The engineering evolution demonstrates improvement without concealing original failures.

**Final production recommendation: NO-GO for unattended destructive identity remediation.**

Continue advisory automation, dry-run evaluation, and separately authorized human-reviewed remediation.

## Supporting Evidence

- testing/v1-v2-comparison.md
- testing/bad-data-analysis.md
- testing/rollback-test.md
- testing/failure-injection.md
- testing/idempotency-test.md
- testing/adversarial-testing.md
- v2/test-results/t12-repeated-execution-finding.md
- v2/test-results/t12-corrective-validation.md
- v3/test-results/v3-failure-injection-results.md
- v3/test-results/v3-adversarial-test-results.md
