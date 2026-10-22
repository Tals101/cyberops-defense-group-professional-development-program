# Ticket #009 — Automation Failure-Mode Register

## Purpose

Document known failure conditions, their potential security and business impact, expected automation behavior, and required operator response.

## Failure-Mode Register

| ID | Failure Mode | Potential Impact | Required Safe Behavior | Evidence |
|---|---|---|---|---|
| FM-01 | Missing identity attributes | Incorrect classification or destructive recommendation | Reduce confidence and require approval | F01 |
| FM-02 | Corrupted input data | Decisions based on invalid evidence | FAIL_CLOSED and log the input failure | F02 |
| FM-03 | Audit logging unavailable | Untraceable remediation | Stop before decision generation or execution | F03 |
| FM-04 | Duplicate remediation execution | Repeated or unnecessary identity changes | Detect already-completed action and perform no change | F04 |
| FM-05 | Interrupted execution | Partial remediation batch | Recover safely without repeating completed operations | F05 |
| FM-06 | Remediation write failure | Incomplete or failed state change | Record failure and preserve prior state | F06 |
| FM-07 | Rollback failure | Identity remains in an unsafe state | Stop and escalate to manual recovery | F07 |
| FM-08 | Approval timeout | Unauthorized action after approval delay | Block operation and escalate | F08 |
| FM-09 | Unsupported identity type | Automation affects an unknown identity class | DO_NOT_AUTOMATE | F09 |
| FM-10 | Missing secondary evidence | False confidence from incomplete corroboration | REQUIRE_APPROVAL | F10 |
| FM-11 | Secondary evidence poisoning | False corroboration authorizes destructive action | Reject altered source and FAIL_CLOSED | A01 |
| FM-12 | Forged freshness metadata | Stale evidence receives trusted authority | Classify STALE and prevent AUTO_REMEDIATE | A02 |
| FM-13 | Forged approval | Unauthorized destructive operation | Reject unverifiable approval | A03 |
| FM-14 | Approval replay | Repeated destructive operation using old authorization | Reject consumed approval ID | A03 |
| FM-15 | Approval target mismatch | Wrong identity is modified | Reject approval | A03 |
| FM-16 | Approval action mismatch | Unauthorized action is performed | Reject approval | A03 |
| FM-17 | Expired approval | Action occurs outside authorization window | Reject approval | A03 |
| FM-18 | Verification key unavailable | Authorization cannot be authenticated | Block operation | A03 |
| FM-19 | Approval ledger unavailable | Replay protection cannot be enforced | Block operation | A03 |
| FM-20 | Excessive automation privileges | Automation affects identities outside approved scope | Restrict credentials and block unauthorized operations | Production control required |

## Severity and Escalation

### Critical

Conditions:
- Unexpected destructive identity change
- Critical business dependency disruption
- Approval forgery or replay
- Failed rollback affecting a critical identity
- Unauthorized execution outside approved scope

Response:
1. Activate emergency stop.
2. Suspend destructive remediation.
3. Preserve execution logs and state snapshots.
4. Notify SOC, IAM, and affected service owners.
5. Initiate controlled recovery.
6. Require explicit authorization before resuming.

### High

Conditions:
- Source-integrity failure
- Audit logging unavailable
- Corrupted identity evidence
- Unverifiable authorization
- Incomplete execution with uncertain account state

Response:
1. Block further destructive execution.
2. Preserve evidence.
3. Investigate and restore the failed control.
4. Revalidate account state and authorization.
5. Escalate if integrity or recovery cannot be established.

### Moderate

Conditions:
- Stale evidence
- Missing corroboration
- Unsupported identity classification
- Approval timeout
- Already-completed remediation operation

Response:
1. Defer or block the affected operation.
2. Request updated evidence or authorization.
3. Record the reason and required operator action.
4. Resume only after applicable prerequisites are met.

## Failure Handling Principles

The automation must:

1. Fail closed when required controls are unavailable.
2. Never convert missing evidence into high confidence.
3. Never treat a recommendation as execution authorization.
4. Never bypass approval requirements to complete a batch.
5. Avoid repeating completed destructive operations.
6. Preserve available failure evidence.
7. Stop when rollback or recovery is uncertain.
8. Require explicit operator intervention for unresolved failures.

## Tested Versus Production Status

F01 through F10 were evaluated using laboratory failure-injection scenarios.

A01 and A02 corrective controls were validated in the V3 decision-engine testing workflow.

A03 approval-integrity and replay controls were validated in an isolated approval-execution test.

These results do not establish that every safeguard is integrated into one production-ready enforcement system.

## Known Operational Limitations

- Canonical V3 remains dry-run only.
- Approval enforcement is not integrated into a production identity platform.
- The local approval-consumption ledger is not a protected production service.
- Trusted secondary evidence requires regular refresh.
- Production credential restrictions remain unvalidated.
- Protected audit storage and recovery permissions require additional implementation.

## Operator Recovery Requirements

Before resuming after a major failure, the responsible operator must confirm:

- affected identity state;
- service availability;
- evidence integrity and freshness;
- valid authorization;
- functioning audit logging;
- rollback readiness;
- emergency-stop availability;
- appropriate management approval.

## Supporting Evidence

- tests/v3-failure-injection-results.md
- tests/v3-adversarial-test-results.md
- security/safeguard-register.md
- security/automation-authority-matrix.md
- security/automation-credential-analysis.md

## Conclusion

Failure modes must be anticipated, tested, observable, and recoverable.

The safest response to uncertain evidence, authorization, execution, or recovery is to withhold destructive authority and escalate.

Full unattended destructive remediation remains NOT APPROVED.
