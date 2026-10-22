# Ticket #009 — IAM Manager Allowlist Recommendation

## 1. Purpose

Evaluate whether service accounts and other sensitive identities should be permanently excluded from automated inactivity remediation.

Provide an IAM recommendation that protects business operations without allowing unused, compromised, or improperly maintained accounts to remain active indefinitely.

## 2. Incident Context

The original V1 automation relied primarily on interactive-login inactivity.

It disabled an identity supporting Finance LedgerBridge, contributing to application disruption.

The incident demonstrated that a service identity may appear inactive while continuing to support legitimate noninteractive application activity.

The underlying problem was insufficient identity context and overly broad remediation authority.

## 3. IAM Manager Proposal

A permanent allowlist could prevent specified accounts from being disabled by the inactivity-remediation job.

Potential benefits:

- Reduced risk of disrupting known critical applications
- Simple implementation
- Immediate protection for identified service accounts

However, permanent exclusions introduce significant security risks.

## 4. Risks of Permanent Allowlisting

### Stale Exceptions

Accounts may remain excluded long after their original business purpose disappears.

### Compromised Accounts

An allowlisted account could remain active despite suspicious activity or other security concerns.

### Unverified Ownership

Service ownership may change without the exclusion being reviewed.

### Expanding Exclusion Scope

Additional accounts may be added until the automation provides little meaningful remediation coverage.

### Hidden Dependencies

An allowlist can conceal inaccurate identity classification rather than correcting it.

### Lack of Accountability

Permanent exclusions without review dates, ownership, or justification weaken governance.

## 5. Recommendation

**Do not implement an unrestricted permanent allowlist.**

Instead, establish a controlled, time-bound exception process for identities requiring protection from unattended destructive remediation.

An exception should restrict automation authority without exempting the account from monitoring, investigation, or periodic access review.

## 6. Required Exception Record

Every exception should include:

- Unique exception ID
- Exact identity identifier
- Identity type
- Business purpose
- Registered owner
- Application or service dependencies
- Business criticality
- Reason for the exception
- Approving IAM authority
- Application-owner confirmation when applicable
- Effective date
- Expiration or scheduled review date
- Last validation date
- Current exception status

Exceptions without an identifiable owner or valid business justification must be escalated.

## 7. Recommended Authority Boundaries

| Identity Condition | Recommended Treatment |
|---|---|
| Standard employee with trustworthy evidence and no dependencies | Evaluate under bounded automation rules |
| Service account | No unattended destructive remediation; require IAM and owner review |
| Privileged identity | No unattended destructive remediation; require privileged-access review |
| Critical application dependency | Require investigation and appropriate approval |
| Incomplete or conflicting identity evidence | Defer remediation and resolve the evidence issue |
| Unsupported identity type | DO_NOT_AUTOMATE pending classification |
| Approved temporary exception | Block unattended disable while retaining monitoring and scheduled review |
| Expired or unowned exception | Suspend automatic authority and escalate for review |

An exception is not an instruction to ignore the identity.

## 8. Exception Lifecycle

### Request

The identity or application owner submits a documented justification.

### Validation

IAM verifies identity type, ownership, authentication pattern, dependencies, and business purpose.

### Approval

Authorized IAM management approves the narrowest necessary exception.

### Enforcement

The automation prevents unattended destructive action against the protected identity.

### Monitoring

Security monitoring, lifecycle controls, and periodic access reviews remain active.

### Expiration and Review

The exception is reassessed before renewal.

If its purpose, owner, or dependency changes, the exception requires reevaluation.

### Removal

Unnecessary exceptions are retired through a controlled change process.

Expiration must not independently trigger an automatic disable.

## 9. Finance LedgerBridge Application

The identity supporting Finance LedgerBridge should not be disabled merely because interactive authentication is absent.

IAM should verify:

1. The identity's actual account classification.
2. Noninteractive authentication activity.
3. Application dependencies.
4. Registered service owner.
5. Business criticality.
6. Whether the account is still required.

Until those facts are established, destructive remediation requires investigation and authorization.

A temporary controlled exception may be appropriate while the records are corrected.

## 10. Payroll Emergency Scenario

The synthetic payroll.emergency identity demonstrates why static primary identity records are insufficient.

Primary evidence suggests an inactive standard employee account.

Secondary evidence identifies a critical payroll integration with conflicting identity and lifecycle information.

The correct V3 authority classification is REQUIRE_APPROVAL, not unattended disable.

The conflicting records must be reconciled rather than permanently hiding the identity behind an allowlist.

## 11. Monitoring and Governance

IAM and SOC should monitor:

- Exceptions approaching expiration
- Missing or changed owners
- Changes in service dependencies
- Privilege increases
- Unusual authentication activity
- Inactive applications retaining service accounts
- Exceptions without recent validation
- Unauthorized exception modifications

Exception changes must be logged and independently reviewable.

## 12. Production Requirements

Before implementing exception enforcement in production:

- Define the authoritative exception repository.
- Restrict who may create, modify, or approve exceptions.
- Prevent remediation credentials from altering exceptions.
- Integrate exception status with the authorization decision.
- Establish expiration and review workflows.
- Test unauthorized modifications and stale exceptions.
- Verify that protected identities remain subject to security monitoring.

## 13. Final IAM Recommendation

**Reject unrestricted permanent allowlisting.**

Adopt an owner-verified, justified, narrowly scoped, time-bound exception system.

Protect service accounts, privileged identities, and critical business dependencies from unattended destructive remediation while maintaining monitoring and lifecycle accountability.

This recommendation does not constitute production authorization.

Full unattended destructive identity remediation remains NOT APPROVED.

## Supporting Evidence

- incident/incident-response-record.md
- environment/identity-context-analysis.md
- incident/root-cause-analysis.md
- testing/bad-data-analysis.md
- security/automation-authority-matrix.md
- management/production-recommendation.md

## Conclusion

The correct response to the V1 incident is not to permanently ignore sensitive accounts.

It is to improve identity classification, verify business dependencies, constrain destructive authority, and govern exceptions throughout their lifecycle.
