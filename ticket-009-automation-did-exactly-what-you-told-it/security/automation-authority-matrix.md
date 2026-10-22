# Ticket #009 — Automation Authority Matrix

## Purpose

Define explicit limits on identity-remediation authority based on identity type, evidence confidence, evidence trust, business dependencies, and approval requirements.

## Core Principle

A remediation recommendation does not automatically grant permission to execute that remediation.

Authorization must be evaluated independently.

## Authority Classifications

| Classification | Meaning | Permitted Behavior |
|---|---|---|
| AUTO_REMEDIATE | Evidence and identity context satisfy bounded automation rules | Eligible for automatic authority in the laboratory decision model |
| REQUIRE_APPROVAL | Remediation requires additional investigation or human authorization | Stage recommendation; do not execute automatically |
| DO_NOT_AUTOMATE | Identity or circumstances are outside permitted automation scope | Block automated remediation and escalate |

All canonical V3 execution remains DRY_RUN_ONLY.

## Identity Authority Matrix

| Identity / Condition | Evidence Requirement | Authority Boundary | Operator Requirement |
|---|---|---|---|
| Standard employee, inactive, no dependencies | HIGH confidence, TRUSTED evidence | Potential AUTO_REMEDIATE classification | Verify execution is authorized in the deployed environment |
| Standard employee with conflicting evidence | Conflict investigation required | REQUIRE_APPROVAL | Reconcile evidence and obtain authorization |
| Service account | Validate owner, purpose, and service dependencies | No unattended destructive remediation | IAM and application-owner review |
| Privileged identity | Validate privilege and business purpose | No unattended destructive remediation | Authorized privileged-access review |
| Critical application dependency | Confirm business impact and dependency ownership | REQUIRE_APPROVAL or stricter restriction | Application-owner and IAM approval |
| Missing secondary corroboration | Additional authoritative evidence needed | REQUIRE_APPROVAL | Investigate missing evidence |
| Stale secondary evidence | Fresh evidence within 24-hour threshold | REQUIRE_APPROVAL | Refresh evidence from an authoritative source |
| Unsupported identity type | Identity classification must be established | DO_NOT_AUTOMATE | Manual investigation |
| Incomplete primary evidence | Missing fields must be resolved | No unattended destructive remediation | Validate required identity attributes |
| Source-integrity failure | Restore trusted source and protected baseline | FAIL_CLOSED | Investigate possible tampering |
| Unavailable audit logging | Restore required logging capability | FAIL_CLOSED | Restore logging before execution |
| Unverified or forged approval | Authentic authorization required | BLOCK | Obtain valid approval |
| Expired approval | New authorization required | BLOCK | Request a new approval |
| Previously consumed approval | New unique authorization required | BLOCK | Investigate replay and reauthorize if appropriate |

## Decision and Execution Separation

V3 evaluates four distinct questions:

1. What action is recommended?
2. How confident is the decision?
3. Can the supporting evidence be trusted?
4. What level of automation authority is appropriate?

Actual remediation execution is a separate control boundary.

An AUTO_REMEDIATE classification must not override the production execution policy.

## Approval Requirements

Approval-gated destructive operations must verify:

- authenticated approver;
- permitted approver role;
- exact target identity;
- exact requested action;
- unique approval ID;
- valid issuance and expiration timestamps;
- cryptographic integrity;
- unused approval status;
- protected approval-consumption record.

The A03 laboratory tests validated these controls in an isolated implementation.

They are not integrated into a production remediation service.

## Execution Safety Requirements

Before any destructive operation, the execution layer must verify:

1. Production execution is explicitly enabled.
2. The identity is inside the authorized scope.
3. Evidence satisfies the required trust threshold.
4. Business dependencies have been evaluated.
5. Required approval has been independently verified.
6. Execution limits are satisfied.
7. Audit logging is available.
8. Rollback prerequisites are satisfied.
9. Emergency-stop controls are available.

Failure of a mandatory prerequisite must prevent execution.

## Emergency Stop and Recovery

The automation must stop destructive operations when:

- integrity validation fails;
- audit logging becomes unavailable;
- an emergency stop is activated;
- execution limits are exceeded;
- unexpected identity types appear;
- required authorization is missing;
- recovery prerequisites cannot be met.

A failed rollback requires immediate escalation rather than continued remediation.

## Observed V3 Examples

### nora.hayes

Historical trusted-evidence regression:
- Confidence: HIGH
- Trust: TRUSTED
- Recommendation: DISABLE
- Authority: AUTO_REMEDIATE
- Actual action: NO_ACTION_DRY_RUN

This historical result does not establish current evidence freshness.

### payroll.emergency

- Confidence: HIGH
- Trust: CONFLICTING
- Recommendation: DISABLE
- Authority: REQUIRE_APPROVAL
- Actual action: NO_ACTION_DRY_RUN

The critical payroll integration prevents unattended destructive authority.

### A02 Stale Evidence

- Trust: STALE
- Authority: REQUIRE_APPROVAL
- Actual action: NO_ACTION_DRY_RUN

A current label cannot override an expired observation timestamp.

## Production Decision

Full unattended destructive remediation: NOT APPROVED.

Permitted near-term activities:
- read-only identity collection;
- evidence validation;
- dry-run decisions;
- remediation recommendations;
- human-reviewed and appropriately authorized actions through separate controlled procedures.

## Supporting Evidence

- design/automation-authority.md
- security/automation-credential-analysis.md
- operations/operator-experience.md
- tests/v3-failure-injection-results.md
- tests/v3-adversarial-test-results.md
- management/production-recommendation.md

## Conclusion

Automation authority must be limited by verified evidence, identity context, business impact, and independently enforced authorization.

No single inactivity threshold, confidence score, approval label, or recommendation may independently authorize destructive identity remediation.
