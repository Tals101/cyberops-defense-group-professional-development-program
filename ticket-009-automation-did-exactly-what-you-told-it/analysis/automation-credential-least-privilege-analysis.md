# Ticket #009 — Automation Credential and Least-Privilege Analysis

## Purpose

Define the minimum privileges required for V3 identity-remediation automation while preventing the excessive authority that contributed to the original incident.

## Security Objective

The automation must not possess more authority than its approved responsibilities require.

A recommendation to disable an identity must never be treated as automatic authorization to execute that action.

## Recommended Credential Model

Separate the automation into distinct security functions:

1. Identity evidence collection
2. Decision evaluation
3. Approval issuance and verification
4. Remediation execution
5. Audit logging
6. Emergency recovery

These functions should not share unrestricted administrative credentials.

## Least-Privilege Authority Matrix

| Function | Required Permission | Prohibited Permission |
|---|---|---|
| Evidence collector | Read approved IAM and secondary identity context | Disable accounts or alter evidence |
| Decision engine | Read evidence and generate recommendations | Modify identities or approve its own actions |
| Source-integrity validator | Read protected integrity baseline | Modify trusted baseline |
| Approval authority | Issue authenticated, scoped approvals | Execute remediation |
| Approval verifier | Validate approvals and consumption status | Issue or alter approvals |
| Remediation executor | Perform narrowly authorized identity-state changes | Create accounts, grant privileges, or modify protected identities outside scope |
| Audit service | Append security events | Delete or rewrite previous records |
| Recovery operator | Restore approved identity state through controlled recovery | Perform unrestricted identity administration |

## Evidence Access

The decision engine requires read-only access to:

- primary IAM identity records;
- authoritative workforce lifecycle records;
- secondary application dependency context;
- identity ownership records;
- protected source-integrity metadata.

The automation must not be able to modify evidence to manufacture confidence or corroboration.

## Approval Separation

Approval issuance must be independent of remediation execution.

The remediation credential must not be permitted to:

- issue its own approvals;
- change approver identities;
- change approval expiration;
- modify approval targets or actions;
- reset consumed approval identifiers;
- access approval-signing secrets.

Production should use a protected approval service with authenticated approvers, transaction binding, expiration, and durable replay protection.

## Remediation Permissions

If destructive remediation is eventually authorized, the execution credential should support only explicitly permitted operations.

Required boundaries include:

- approved identity classes;
- approved identity scope;
- approved action type;
- verified approval when required;
- dependency and business-criticality checks;
- execution limits;
- logging and recovery prerequisites.

Service accounts, privileged identities, unsupported identity types, and critical dependencies must not receive unattended destructive authority.

## Credential Protection

Production credentials should use:

- managed workload identity or equivalent short-lived credentials;
- secure secret storage when secrets are unavoidable;
- restricted credential access;
- credential rotation;
- monitored authentication activity;
- separation of production and laboratory credentials;
- immediate revocation capability.

Credentials must not be hard-coded into source files or committed to Git.

## Audit and Recovery

The remediation account must not be able to erase evidence of its own operations.

Audit records should be protected against modification and retained according to organizational requirements.

Recovery authority should be separately controlled and tested.

Emergency-stop capability must revoke or suspend execution authority without destroying audit evidence.

## Lessons From Adversarial Testing

### A01 — Evidence Poisoning

The remediation credential must not be able to modify both secondary evidence and its trusted integrity baseline.

### A02 — Freshness Forgery

Evidence timestamps must originate from trustworthy collection systems. The remediation engine must independently evaluate their age.

### A03 — Approval Forgery and Replay

The remediation credential must not control approval issuance, signing secrets, or the approval-consumption ledger.

The A03 SQLite ledger and HMAC configuration demonstrate laboratory controls, not a production-grade authorization system.

## Monitoring Requirements

Monitor for:

- unexpected credential use;
- unauthorized permission changes;
- source-integrity failures;
- stale evidence;
- repeated approval failures;
- attempted approval replay;
- operations outside authorized scope;
- missing audit records;
- unusual remediation volume.

## Production Readiness Assessment

Status: NOT APPROVED FOR FULL UNATTENDED DESTRUCTIVE REMEDIATION.

The current V3 decision engine remains a laboratory implementation.

Its adversarial corrections demonstrate improved safety, but production credential boundaries, approval-service integration, protected logging, and operational enforcement have not been validated.

## Recommendation

Continue read-only collection, dry-run evaluation, and recommendation generation.

Permit destructive changes only through appropriately controlled human-approved procedures until the complete production security model is implemented and independently tested.

## Conclusion

Least privilege must be enforced through identity-platform permissions and independent authorization controls, not merely through application logic.

The automation should have the smallest possible permission set, with separation of duties between evidence collection, decision-making, approval, execution, and recovery.
