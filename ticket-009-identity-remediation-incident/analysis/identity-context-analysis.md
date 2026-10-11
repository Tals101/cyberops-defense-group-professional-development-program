# Ticket #009 — Identity Context Analysis

## Purpose

This document defines the identity information that a security automation should consider before making a production remediation decision.

No single field should be treated as sufficient proof that an identity is safe, unsafe, stale, abandoned, or ready for remediation.

The purpose of these fields is to reduce the risk that incomplete or misleading context becomes an irreversible production action.

---

## Identity Fields

### 1. Identity Type

Examples:

- employee
- contractor
- service account
- privileged account
- shared technical account
- unknown

### Why This Makes the Decision Safer

Different identity types have different lifecycle patterns and operational risks.

A human user who has not logged in for 90 days may be inactive.

A service account that has not performed an interactive login for 90 days may still be actively used by an application.

### Risk if Missing or Wrong

The automation may apply employee-account assumptions to a non-human identity.

---

## 2. Employment or Workforce Status

Examples:

- active
- leave
- terminated
- contractor expired
- not applicable
- unknown

### Why This Makes the Decision Safer

Termination or workforce status can provide strong evidence that an employee identity should no longer retain access.

### Risk if Missing or Wrong

An active employee could be disabled because stale HR data incorrectly shows termination.

A terminated employee might remain active if workforce data is unavailable.

---

## 3. Account Owner

Examples:

- individual employee
- application owner
- business unit
- infrastructure team
- unknown

### Why This Makes the Decision Safer

An identifiable owner provides a source for validating business purpose and expected account state.

### Risk if Missing or Wrong

An important technical identity may appear abandoned simply because ownership metadata is incomplete.

---

## 4. Last Interactive Login

### Why This Makes the Decision Safer

This field can help determine whether a human identity appears inactive.

### Risk if Missing or Wrong

Interactive login is weak evidence for service accounts, API identities, scheduled processes, or certificate-based authentication.

It must not be treated as universal proof of inactivity.

---

## 5. Last Non-Interactive Authentication

Examples:

- API authentication
- scheduled job authentication
- service-to-service login
- application authentication

### Why This Makes the Decision Safer

This distinguishes technically active identities from identities that merely lack interactive user logins.

### Risk if Missing or Wrong

A legitimate application account could be classified as stale even while actively supporting production services.

---

## 6. Privilege Level

Examples:

- standard
- elevated
- administrator
- domain-level privilege
- application administrator

### Why This Makes the Decision Safer

Higher privilege increases both security risk and the consequences of an incorrect automated decision.

### Risk if Missing or Wrong

Automation may either ignore a dangerous privileged identity or automatically modify a critical privileged account without sufficient review.

---

## 7. Business Purpose

Examples:

- employee access
- payroll integration
- finance reporting
- backup processing
- monitoring
- unknown

### Why This Makes the Decision Safer

Business purpose helps determine whether an account that looks unusual is actually required.

### Risk if Missing or Wrong

A necessary identity may appear unnecessary because its purpose was never documented.

---

## 8. Service Dependencies

Examples:

- application name
- scheduled job
- integration
- database
- API
- downstream service

### Why This Makes the Decision Safer

Dependency information reveals whether changing an identity could interrupt a business service.

### Risk if Missing or Wrong

The automation may disable an identity without understanding that production systems rely on it.

---

## 9. Authentication Behavior

Examples:

- normal interactive activity
- normal non-interactive activity
- no recent activity
- unusual source
- suspicious login pattern
- failed authentication spike

### Why This Makes the Decision Safer

Behavior adds security context beyond simple age or last-login measurements.

### Risk if Missing or Wrong

A dormant compromised account may be overlooked, or legitimate automation activity may be misclassified as suspicious.

---

## 10. Account Age

### Why This Makes the Decision Safer

Account age can help identify recently created identities, legacy identities, and lifecycle anomalies.

### Risk if Missing or Wrong

Age alone can produce misleading conclusions.

An old account can still be legitimate and critical.

---

## 11. Approval Status

Examples:

- approved
- pending review
- expired approval
- not required
- unknown

### Why This Makes the Decision Safer

Approval state can distinguish authorized exceptions or temporary access from unmanaged access.

### Risk if Missing or Wrong

An identity could be remediated while an approval is still valid or retained after authorization has expired.

---

## 12. Lifecycle State

Examples:

- provisioned
- active
- inactive
- pending disable
- disabled
- pending deletion
- decommissioned
- unknown

### Why This Makes the Decision Safer

Lifecycle state shows where the identity is expected to be within an established identity-management process.

### Risk if Missing or Wrong

Automation may duplicate, reverse, or conflict with an existing lifecycle action.

---

## 13. Data Freshness

Examples:

- source timestamp
- last synchronization time
- age of HR data
- age of CMDB data
- age of authentication data

### Why This Makes the Decision Safer

A decision is only as reliable as the information used to make it.

### Risk if Missing or Wrong

Correct logic can still produce an incorrect decision when the input data is stale.

---

## 14. Evidence Completeness

Examples:

- complete
- partial
- conflicting
- missing critical fields

### Why This Makes the Decision Safer

Automation should know when it does not have enough information to make a high-impact decision.

### Risk if Missing or Wrong

Missing evidence may silently be interpreted as evidence of inactivity or abandonment.

---

# Decision Principle

Identity remediation should not ask only:

> Does this account match the rule?

It should also ask:

> Is the evidence complete enough and reliable enough to justify the consequence of this action?

The greater the operational impact of the proposed action, the stronger the required evidence and approval controls should be.

---

# Fail-Safe Principle

Missing or contradictory information should not automatically be interpreted in the most aggressive way.

For high-impact actions such as disabling:

- critical service identities;
- privileged identities;
- identities with known production dependencies;
- identities with incomplete ownership or lifecycle information;

the safer default may be to:

- log;
- flag;
- recommend;
- request review;
- or delay execution;

rather than automatically enforce the change.

This principle will be tested against V1 and the redesigned system.
