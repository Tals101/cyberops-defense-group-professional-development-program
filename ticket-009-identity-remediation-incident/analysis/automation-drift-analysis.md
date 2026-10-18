# Ticket #009 — Automation Drift Analysis

## 1. Purpose

Identify how changes in identity data, evidence sources, automation rules, authorization, and production configuration could cause V3 identity-remediation automation to behave differently over time.

## 2. Drift Definition

Automation drift occurs when the assumptions, inputs, permissions, or controls used to authorize an automated decision no longer match the current operating environment.

A previously successful test does not guarantee that the same decision remains safe.

## 3. Current Drift Finding

The canonical secondary identity dataset contains observation timestamps dated October 16, 2026.

V3 enforces a maximum secondary evidence age of 24 hours for trusted unattended authority.

As of October 18, 2026, those previously current observations exceed the permitted age.

Therefore, historical TRUSTED and AUTO_REMEDIATE results cannot be assumed to remain valid today.

This is an identified freshness-drift condition, not evidence that the canonical engine has been rerun today.

The correct response is to obtain freshly observed evidence from the authoritative sources.

Do not manually advance timestamps or automatically rotate integrity baselines merely to restore favorable automation decisions.

## 4. Drift Categories

| ID | Drift Category | Risk | Detection Method | Required Response |
|---|---|---|---|---|
| DR-01 | Evidence freshness drift | Old evidence receives excessive authority | Compare observed_at_utc against current UTC time | Classify STALE and require review |
| DR-02 | Identity classification drift | Service or privileged accounts become misclassified | Compare IAM records against authoritative identity inventory | Block unsafe remediation |
| DR-03 | Business dependency drift | New critical dependencies remain undiscovered | Reconcile application and owner records | Reassess authority |
| DR-04 | Source-integrity drift | Secondary evidence changes unexpectedly | Verify protected SHA256 baseline | FAIL_CLOSED and investigate |
| DR-05 | Approval-policy drift | Unauthorized approvals become acceptable | Review approver roles and approval rules | Block and escalate |
| DR-06 | Credential-permission drift | Automation gains excessive privileges | Periodic permission comparison | Revoke unauthorized permissions |
| DR-07 | Decision-rule drift | Updated thresholds increase destructive scope | Version comparison and regression tests | Require approved change |
| DR-08 | Audit-control drift | Logs become incomplete or modifiable | Audit preflight and independent review | Stop destructive execution |
| DR-09 | Execution-volume drift | Unexpected increase in remediation candidates | Compare decisions and actions against historical baselines | Investigate and restrict scope |
| DR-10 | Recovery-capability drift | Rollback no longer functions reliably | Scheduled recovery testing | Suspend destructive authority |

## 5. Historical V3 Decision Baseline

Earlier V3 laboratory testing evaluated 11 synthetic identities.

The historical authority distribution was:

- AUTO_REMEDIATE: 5
- REQUIRE_APPROVAL: 4
- DO_NOT_AUTOMATE: 2

The earlier evidence-trust distribution was:

- TRUSTED: 8
- CONFLICTING: 1
- INCOMPLETE: 2

These figures are historical reference values, not current operational measurements.

Changes in the distribution require investigation, not automatic rejection, because legitimate business changes can alter expected classifications.

## 6. Evidence Freshness Drift

### Detection

For each secondary evidence record:

1. Confirm observed_at_utc exists.
2. Parse the timestamp as timezone-aware UTC.
3. Compare the observation time against the evaluation time.
4. Calculate evidence age.
5. Mark evidence STALE if its age exceeds 24 hours.
6. Reject missing, invalid, or unacceptable future timestamps from trusted unattended authority.

### Response

STALE evidence must not qualify for AUTO_REMEDIATE.

The operator must obtain fresh evidence from the authoritative provider and repeat the decision evaluation.

Updating a freshness label without collecting new evidence is prohibited.

## 7. Integrity Baseline Drift

The trusted secondary dataset was intentionally updated during A02 testing.

That authorized change required rotation of the source-integrity SHA256 baseline.

Unexpected changes must not automatically update the expected hash.

A legitimate baseline rotation requires:

- documented reason;
- authorized source owner;
- independent review;
- preserved previous hash;
- approved replacement hash;
- regression testing;
- recorded change history.

If verification fails, processing must fail closed.

## 8. Authorization and Credential Drift

The automation's effective permissions must be reviewed against the least-privilege authority matrix.

Indicators of unsafe drift include:

- New ability to disable protected identity classes
- New ability to change approval artifacts
- Access to approval-signing secrets
- Ability to reset consumed approval IDs
- Write access to protected source-integrity metadata
- Ability to delete or rewrite audit history
- Unauthorized expansion of identity scope

Any unauthorized privilege expansion requires containment and investigation.

## 9. Monitoring Schedule

### Every Run

Check:

- Evidence integrity
- Observation timestamps
- Missing or conflicting context
- Approval validity
- Audit logging
- Authorized execution scope

### Daily

Review:

- STALE and INCOMPLETE evidence
- Integrity failures
- Approval failures
- Unexpected automation classifications
- Blocked or failed operations

### Weekly

Compare:

- Authority classifications
- Protected identity counts
- Application dependencies
- Service-account inventories
- Recommended versus executed actions

### Monthly

Review:

- Credential permissions
- Automation rules and thresholds
- Baseline rotations
- Approval authority
- Recovery readiness
- Regression and failure-injection results

## 10. Drift Response Procedure

When meaningful drift is detected:

1. Identify the affected source, identity, or control.
2. Determine whether destructive authority is affected.
3. Block or suspend unsafe execution.
4. Preserve evidence and configuration versions.
5. Contact the responsible data or system owner.
6. Investigate the cause.
7. Apply an independently reviewed correction.
8. Repeat relevant regression and adversarial tests.
9. Document the change and authorization.
10. Resume only after required safeguards are validated.

## 11. Proposed Drift Indicators

The following are proposed operational triggers, not production-validated alert thresholds:

- Any integrity mismatch: immediate investigation
- Any attempted approval replay: security alert
- Any unauthorized privilege increase: immediate escalation
- Any destructive action without a verified approval where one is required: critical incident
- Any failure of mandatory audit logging: suspend destructive execution
- Any critical business dependency unexpectedly removed from context: investigate before remediation

Statistical thresholds for changes in decision distributions must be established using an operational baseline.

## 12. Regression Testing Requirements

After a significant data-source, rule, credential, or approval change, rerun relevant tests for:

- Missing evidence
- Conflicting evidence
- Unsupported identities
- Service and privileged accounts
- Stale observation timestamps
- Source-integrity failures
- Approval forgery and replay
- Logging failures
- Duplicate execution
- Interrupted execution
- Remediation failure
- Rollback failure

Historical test success must not substitute for current evidence.

## 13. Current Production Readiness

Status: NOT APPROVED FOR FULL UNATTENDED DESTRUCTIVE REMEDIATION.

Reasons include:

1. Canonical secondary observations have become stale.
2. Approval enforcement is demonstrated only in an isolated laboratory workflow.
3. Production credential boundaries are unvalidated.
4. Protected approval and audit infrastructure is not integrated.
5. Destructive production execution and recovery have not been validated as one system.

## 14. Recommendations

Continue:

- Read-only evidence collection
- Dry-run decisions
- Evidence-trust monitoring
- Drift detection
- Human review of remediation recommendations

Require independent authorization and operational validation before enabling destructive execution.

## 15. Supporting Evidence

- analysis/automation-operations-plan.md
- analysis/automation-authority-matrix.md
- analysis/automation-safeguard-register.md
- analysis/automation-credential-least-privilege-analysis.md
- tests/a01-secondary-evidence-poisoning-corrective-validation.md
- tests/a02-freshness-metadata-forgery-corrective-validation.md
- tests/a03-approval-forgery-replay-corrective-validation.md
- tests/v3-adversarial-test-results.md

## Conclusion

Automation safety is not a permanent property established by a single successful test.

Identity context, evidence age, application dependencies, credentials, and authorization controls must be continuously reassessed.

When evidence or authority becomes uncertain, destructive remediation must remain blocked.
