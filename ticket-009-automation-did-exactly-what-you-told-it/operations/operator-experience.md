# Ticket #009 — V3 Operator Experience Examples

## Purpose

Demonstrate how an operator interprets V3 identity-remediation decisions, safety controls, approval requirements, and failures.

These examples are based on the synthetic Ticket #009 test evidence. Canonical V3 decisions are dry-run only. Approved execution and failure scenarios were tested separately in isolated simulation workflows.

## Example 1 — Trusted Evidence and Automatic Authority

### Identity
nora.hayes

### Observed Decision
- Decision confidence: HIGH
- Evidence trust: TRUSTED
- Recommendation: DISABLE
- Authority: AUTO_REMEDIATE
- Approval required: NO
- Actual action: NO_ACTION_DRY_RUN

### Operator Interpretation

The identity satisfies the laboratory decision rules for automatic authority.

However, AUTO_REMEDIATE is a decision classification, not proof that production execution is authorized.

### Operator Action

Review the recommendation and confirm production execution remains disabled.

### Supporting Evidence
evidence/v3-dry-run-decisions.csv

## Example 2 — Conflicting Evidence Requires Approval

### Identity
payroll.emergency

### Observed Decision
- Decision confidence: HIGH
- Evidence trust: CONFLICTING
- Recommendation: DISABLE
- Authority: REQUIRE_APPROVAL
- Approval required: YES
- Actual action: NO_ACTION_DRY_RUN

### Operator Interpretation

The primary IAM record conflicts with secondary application context indicating a critical payroll integration.

The identity must not be disabled without investigation and appropriate authorization.

### Operator Action

1. Contact Payroll Operations and the application owner.
2. Validate dependencies and the account's business purpose.
3. Reconcile the conflicting records.
4. Obtain appropriately scoped approval before considering remediation.

### Supporting Evidence
evidence/v3-dry-run-decisions.csv

## Example 3 — Source Integrity Failure

### Scenario
A01 secondary evidence poisoning.

### Observed Result
- Status: FAIL_CLOSED
- Failure: SECONDARY_SOURCE_INTEGRITY_FAILURE
- Decision records: 0
- Remediation performed: False

### Operator Interpretation

The secondary evidence source failed integrity verification. Its contents cannot be trusted for remediation decisions.

### Operator Action

Stop processing, preserve the failure log, investigate the source, verify provenance, and restore trusted evidence before rerunning.

### Supporting Evidence
evidence/v3-a01-fixed.log

## Example 4 — Stale Evidence Blocks Automatic Authority

### Scenario
A02 freshness metadata forgery.

### Observed Decision
- Evidence trust: STALE
- Recommendation: DISABLE
- Authority: REQUIRE_APPROVAL
- Actual action: NO_ACTION_DRY_RUN

### Operator Interpretation

The evidence was labeled current, but its observation timestamp exceeded the 24-hour freshness threshold.

### Operator Action

Request freshly collected authoritative evidence. Do not treat an updated label alone as proof of freshness.

### Supporting Evidence
evidence/v3-a02-fixed-decisions.csv

## Example 5 — Approval Replay Rejected

### Scenario
A03 approval replay.

### Observed Result
- Approval ID: APR-A03-001
- Verification: Successful
- Replay check: BLOCKED
- Reason: Approval ID already consumed
- Target: nora.hayes
- Identity state after rejected attempt: Enabled

### Operator Interpretation

A previously consumed approval cannot authorize another remediation operation.

### Operator Action

Investigate unexpected replay attempts. Require a new independently authorized approval for any subsequent operation.

### Supporting Evidence
tests/a03-approval-forgery-replay-corrective-validation.md

## Example 6 — Failed Rollback Requires Escalation

### Scenario
F07 failed rollback injection.

### Observed Result
- Result: FAILED_ROLLBACK
- Restoration successful: False
- Required response: Manual recovery escalation

### Operator Interpretation

The system could not restore the prior identity state automatically.

### Operator Action

Stop further remediation, preserve snapshots and logs, escalate to authorized recovery personnel, and independently validate the restored account state.

### Supporting Evidence
tests/v3-failure-injection-results.md

## Operator Experience Requirements

A production operator interface should always show:

1. Identity and requested action
2. Decision confidence
3. Evidence trust classification
4. Conflicting or missing evidence
5. Recommended action
6. Authorized action classification
7. Approval requirements and verification status
8. Actual execution result
9. Recovery status
10. Required next operator action

## Conclusion

V3 provides more explainable decisions and stronger safety boundaries than V1.

However, production operators must be able to distinguish recommendations from execution authority, recognize fail-closed conditions, and escalate unresolved approval, evidence, or recovery failures.

Full unattended destructive remediation remains prohibited.
