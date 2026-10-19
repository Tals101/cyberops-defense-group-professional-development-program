# Ticket #009 — Automation Operations Plan

## 1. Purpose

Define the operational procedures, responsibilities, monitoring, recovery requirements, and maintenance controls for V3 identity-remediation automation.

This plan describes the controls required before production deployment.

## 2. Current Operating Status

- Environment: Synthetic identity-remediation laboratory
- Canonical V3 mode: DRY_RUN_ONLY
- Production deployment: Not performed
- Full unattended destructive remediation: NOT APPROVED
- Human-approved destructive remediation: Permitted only through separately authorized procedures

Laboratory validation does not constitute production authorization.

## 3. Operational Ownership

| Role | Responsibility |
|---|---|
| SOC Manager | Security oversight and escalation decisions |
| IAM Manager | Identity ownership, authority boundaries, and remediation approval |
| Automation Engineer | Code maintenance, tests, and deployment controls |
| Application Owner | Business dependency and service-impact validation |
| Security Engineering | Independent safeguard and change validation |
| Recovery Operator | Authorized restoration and recovery verification |

Approval issuance, remediation execution, and recovery should have separate authority.

## 4. Pre-Execution Checklist

Before each evaluation or authorized remediation cycle:

1. Confirm the intended environment.
2. Verify that production destructive execution is disabled unless separately authorized.
3. Confirm the emergency-stop mechanism is available.
4. Validate primary identity data.
5. Validate secondary evidence integrity.
6. Verify evidence observation timestamps.
7. Check for missing, incomplete, or conflicting evidence.
8. Confirm audit logging is available.
9. Validate approved identity scope and execution limits.
10. Confirm rollback and recovery prerequisites.
11. Independently validate any required approval.
12. Record the execution ID and operator identity.

A failed mandatory check must prevent destructive execution.

## 5. Evidence Freshness Management

V3 requires secondary evidence observation timestamps.

Maximum age for trusted unattended authority:

24 hours.

Operational rules:

- Evidence older than 24 hours is STALE.
- Missing or malformed timestamps cannot establish TRUSTED evidence.
- Future timestamps require investigation.
- A current label does not override an expired observation timestamp.
- Evidence must be refreshed by the authoritative source.

The canonical laboratory timestamps from October 16, 2026 have exceeded the 24-hour threshold.

Operators must not simply change timestamps to manufacture freshness.

## 6. Source Integrity Management

Secondary evidence must be verified against a protected integrity baseline.

An integrity mismatch requires:

1. FAIL_CLOSED processing.
2. No destructive remediation.
3. Preservation of the observed and expected hashes.
4. Investigation of source provenance.
5. Escalation to the responsible evidence owner.

A baseline must never be automatically changed merely to match unexpected source contents.

Legitimate baseline rotation requires independent review, an approved change record, and validation.

## 7. Approval Operations

Approval-gated remediation requires:

- An authenticated and authorized approver
- A unique approval identifier
- Exact target identity binding
- Exact action binding
- An enforceable expiration
- Integrity verification
- Durable one-time-use protection

The A03 laboratory implemented these controls in an isolated test.

Production must provide an independent approval authority and protected approval-consumption service.

The remediation executor must not be able to issue its own approvals.

## 8. Routine Monitoring Schedule

### Before Every Run

- Validate integrity and freshness.
- Confirm logging availability.
- Check approval prerequisites.
- Verify emergency-stop readiness.
- Confirm execution scope.

### Daily

- Review failed evaluations and blocked actions.
- Investigate integrity failures.
- Identify stale or missing evidence.
- Review approval failures and replay attempts.
- Confirm no unauthorized destructive changes occurred.

### Weekly

- Review decision and authority distributions.
- Compare expected versus observed identity classifications.
- Review service-account and privileged-identity exclusions.
- Assess changes in business dependencies.
- Review failed or deferred remediation cases.

### Monthly

- Review credential permissions.
- Validate least-privilege controls.
- Test recovery procedures.
- Review safeguard exceptions.
- Examine automation drift.
- Review code and configuration changes.
- Confirm the production authorization posture.

## 9. Operational Metrics

Track:

| Metric | Purpose |
|---|---|
| Total identities evaluated | Establish processing coverage |
| TRUSTED / CONFLICTING / INCOMPLETE / STALE decisions | Monitor evidence quality |
| AUTO_REMEDIATE classifications | Monitor proposed automation authority |
| REQUIRE_APPROVAL classifications | Measure human-review workload |
| DO_NOT_AUTOMATE classifications | Confirm protected identity handling |
| Integrity failures | Detect possible evidence tampering |
| Freshness failures | Identify outdated sources |
| Approval verification failures | Detect invalid authorization |
| Replay attempts | Detect reused approvals |
| Failed remediation operations | Monitor execution reliability |
| Failed rollback attempts | Monitor recovery risk |
| Unlogged or unexplained actions | Detect audit-control failures |

Alert thresholds must be established from validated operating baselines.

## 10. Emergency Stop Procedure

Trigger emergency stop when:

- Unauthorized remediation is suspected.
- Critical application disruption occurs.
- Source integrity cannot be established.
- Audit logging becomes unavailable.
- Approval verification fails unexpectedly.
- Execution exceeds authorized boundaries.
- Recovery or rollback becomes unreliable.

Required response:

1. Stop destructive execution.
2. Prevent additional identity-state changes.
3. Preserve available logs and state snapshots.
4. Notify SOC and IAM leadership.
5. Identify affected applications and identities.
6. Begin controlled investigation and recovery.

## 11. Recovery Procedure

Following an unsafe or failed operation:

1. Identify affected identities.
2. Preserve pre-change and post-change evidence.
3. Confirm current identity state.
4. Identify business dependencies.
5. Obtain recovery authorization.
6. Restore the approved prior state.
7. Validate identity access.
8. Validate dependent application health.
9. Confirm audit evidence is complete.
10. Document the outcome.

Failed rollback requires manual escalation.

Do not continue destructive remediation while recovery status is uncertain.

## 12. Safe Restart Requirements

Automation may resume only after:

- The triggering failure has been resolved.
- Evidence integrity has been revalidated.
- Evidence freshness is acceptable.
- Logging is operational.
- Affected identity states are reconciled.
- Approval and execution boundaries are confirmed.
- Recovery capability is available.
- Responsible management authorizes resumption.

Previously consumed approvals must not be reused.

## 13. Change Management

Any change to the following requires review:

- Identity classification rules
- Inactivity thresholds
- Evidence trust rules
- Freshness limits
- Integrity baselines
- Approval requirements
- Execution scope
- Automation credentials
- Logging behavior
- Rollback procedures

Changes must include test evidence, a rollback plan, and approval appropriate to their impact.

## 14. Required Production Controls

Before destructive production execution:

1. Independent credential and permission validation
2. Protected evidence sources and integrity metadata
3. Authoritative evidence refresh
4. Production approval-service integration
5. Durable replay protection
6. Tamper-resistant audit logging
7. Enforced execution limits
8. Tested emergency stop
9. Tested rollback and recovery
10. Independent security review
11. Formal production change authorization

## 15. Current Operational Recommendation

Operate V3 only for:

- Read-only evidence collection
- Evidence validation
- Dry-run decision evaluation
- Recommendation generation
- Human review and escalation

Destructive remediation must use appropriately controlled and separately authorized procedures.

## 16. Supporting Evidence

- analysis/soc-manager-production-recommendation.md
- analysis/automation-authority-matrix.md
- analysis/automation-safeguard-register.md
- analysis/automation-failure-mode-register.md
- analysis/automation-credential-least-privilege-analysis.md
- tests/v3-failure-injection-results.md
- tests/v3-adversarial-test-results.md

## Conclusion

Reliable security automation requires operational controls throughout its lifecycle, not only correct decision logic.

V3 demonstrates improved laboratory safeguards but remains unsuitable for full unattended destructive production execution.
