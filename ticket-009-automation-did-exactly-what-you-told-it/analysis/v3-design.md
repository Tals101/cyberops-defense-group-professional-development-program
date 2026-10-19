# Ticket #009 — V3 Design
## Corroborated Evidence Authority

## Purpose

V3 addresses the bad-data failure exposed by the emergency payroll integration account.

V2 improved:

- identity context;
- authority boundaries;
- approval gates;
- rollback;
- blast-radius controls;
- fail-safe behavior.

However, V2 still assumed that sufficiently complete-looking IAM data was trustworthy enough to support destructive action.

V3 adds a separate evidence-trust layer.

The design principle is:

**Correct decision logic is not enough. Destructive authority also requires trustworthy evidence.**

---

# Architecture

V3 decision flow:

Identity
→ Primary IAM Evidence
→ Secondary Context Evidence
→ Evidence Corroboration
→ Evidence Trust Classification
→ Decision Confidence
→ Remediation Recommendation
→ Authority Classification
→ Approval Gate
→ Enforcement
→ Health Validation
→ Rollback / Recovery
→ Audit Record

Detection, authority, and enforcement remain separate stages.

---

# Primary Evidence Source

The existing synthetic IAM dataset remains the primary source.

Primary evidence includes:

- identity type;
- workforce status;
- owner;
- business purpose;
- interactive-login age;
- non-interactive authentication age;
- privilege;
- lifecycle state;
- approval status;
- data freshness;
- evidence completeness;
- enabled state.

V3 does not assume that these fields are independently sufficient for destructive authority.

---

# Secondary Evidence Source

V3 will introduce a synthetic secondary context source representing systems such as:

- CMDB;
- application inventory;
- service registry;
- ownership registry;
- HR lifecycle source;
- dependency registry;
- PAM inventory.

The secondary source will contain fields such as:

- username;
- authoritative identity role;
- application dependency;
- business criticality;
- registered owner;
- expected authentication pattern;
- lifecycle status;
- source freshness;
- source confidence.

---

# Emergency Payroll Test Identity

V3 must include the Security Engineering payroll test case.

Primary IAM data will indicate that the account appears to be:

- non-service;
- non-privileged;
- inactive;
- enabled;
- owned by a current employee.

Secondary evidence will identify that the same account:

- supports emergency payroll integration;
- has a critical application dependency;
- is operationally sensitive.

Expected V3 result:

- evidence conflict detected;
- automatic destructive authority denied;
- decision reduced to REQUIRE_APPROVAL or DO_NOT_AUTOMATE;
- no automatic disablement.

---

# Evidence Trust Classification

V3 will classify evidence trust separately from remediation confidence.

Possible evidence-trust states:

## TRUSTED

Required critical fields agree across authoritative sources.

Evidence is:

- complete enough;
- current enough;
- internally consistent;
- corroborated.

## CONFLICTING

Two or more trusted sources materially disagree.

Examples:

- IAM says employee account;
- application inventory says payroll integration account.

Result:

Destructive automation prohibited.

## INCOMPLETE

Required corroborating evidence is missing.

Result:

Destructive automation prohibited or approval required depending on impact.

## STALE

Evidence exists but is older than the acceptable freshness threshold.

Result:

Authority reduced.

## UNKNOWN

Evidence trust cannot be established.

Result:

DO_NOT_AUTOMATE for destructive changes.

---

# Corroboration Rules

Automatic destructive remediation requires corroboration of critical facts.

At minimum:

1. Identity type must be recognized.
2. Lifecycle state must support remediation.
3. Ownership must be known or authoritative disposition must exist.
4. Primary evidence must be current.
5. Secondary evidence must be available.
6. No high-impact application dependency may be present.
7. No material conflict may exist between sources.
8. Evidence completeness must meet the destructive-action threshold.
9. Rollback capability must be available.
10. Audit logging must be available.

Failure of any required trust condition reduces authority.

---

# V3 Authority Model

## AUTO_REMEDIATE

Allowed only when:

- remediation recommendation is destructive;
- decision confidence is HIGH;
- evidence trust is TRUSTED;
- critical sources agree;
- identity is not privileged;
- identity has no high-impact dependency;
- identity type is supported;
- pre-change snapshot is available;
- rollback is available;
- audit logging is operational;
- action limits permit enforcement;
- emergency stop is not active.

---

## REQUIRE_APPROVAL

Used when:

- evidence is mostly complete but requires human judgment;
- sources disagree but ownership and context are identifiable;
- the identity has moderate operational impact;
- a service or dependency relationship exists;
- confidence is insufficient for unattended destructive action.

Automation may:

- detect;
- explain;
- recommend;
- stage.

Automation may not execute the destructive change without approval.

---

## DO_NOT_AUTOMATE

Used when:

- identity type is unknown;
- critical evidence is unavailable;
- evidence trust is UNKNOWN;
- rollback cannot be established;
- critical dependency cannot be evaluated;
- evidence integrity is questionable;
- the identity is break-glass, recovery, or core IAM infrastructure;
- logging cannot be established.

The system must preserve production state.

---

# Decision Confidence vs. Evidence Trust

V3 keeps these concepts separate.

## Decision Confidence

Answers:

> Given the available facts, how strongly does the policy support this recommendation?

## Evidence Trust

Answers:

> How strongly can the system trust that those facts reflect reality?

A HIGH-confidence decision based on CONFLICTING evidence must not receive AUTO_REMEDIATE authority.

Example:

Policy conclusion:

`DISABLE`

Decision confidence:

`HIGH`

Evidence trust:

`CONFLICTING`

Final authority:

`REQUIRE_APPROVAL` or `DO_NOT_AUTOMATE`

---

# Safe Failure Behavior

## Missing Secondary Evidence

Do not assume the primary source is correct.

Result:

`REQUIRE_APPROVAL`

or:

`DO_NOT_AUTOMATE`

depending on impact.

---

## Conflicting Sources

Do not choose one source automatically.

Result:

`REQUIRE_APPROVAL`

or:

`DO_NOT_AUTOMATE`

No destructive automatic action.

---

## Stale Secondary Source

Reduce evidence trust.

Do not authorize destructive automation solely from stale corroboration.

---

## Unknown Identity Type

Result:

`DO_NOT_AUTOMATE`

---

## Unknown Business Purpose

Preserve current state.

Route for investigation.

---

## Logging Failure

Stop enforcement.

No destructive action.

---

## Snapshot Failure

Stop enforcement.

No destructive action.

---

## Rollback Unavailable

Destructive automatic remediation prohibited.

---

## Emergency Stop Active

No further destructive changes.

---

# Blast-Radius Controls

V3 retains:

- maximum two state-changing actions per run;
- persistent deferred-action ledger;
- emergency stop;
- approval boundaries;
- pre-change snapshots.

Evidence corroboration does not replace blast-radius controls.

---

# Audit Requirements

Every V3 decision record must contain:

- identity;
- primary evidence;
- secondary evidence;
- source freshness;
- source agreement;
- evidence-trust classification;
- decision confidence;
- recommendation;
- authority;
- approval requirement;
- proposed action;
- actual action;
- result;
- rollback availability;
- recovery method.

An auditor must be able to understand the decision without reading source code.

---

# V3 Test Requirements

V3 must test at minimum:

1. normal active employee;
2. clearly terminated employee with corroborating evidence;
3. legitimate service account;
4. privileged identity;
5. ambiguous identity;
6. incomplete primary evidence;
7. missing secondary evidence;
8. conflicting primary and secondary evidence;
9. emergency payroll integration account;
10. unknown identity type;
11. stale secondary evidence;
12. malformed input;
13. logging failure;
14. rollback availability failure;
15. repeated execution.

---

# Emergency Payroll Expected Result

For the payroll test identity:

Primary evidence:

- ordinary non-service identity;
- inactive;
- enabled.

Secondary evidence:

- payroll integration dependency;
- critical business purpose.

Evidence trust:

`CONFLICTING`

Decision policy may still recommend:

`DISABLE`

Final authority must be reduced to:

`REQUIRE_APPROVAL`

or:

`DO_NOT_AUTOMATE`

Actual automatic action:

`NO_ACTION`

The conflict itself becomes evidence.

---

# What V3 Does Not Protect Against

V3 does not eliminate:

- correlated bad data across multiple systems;
- compromise of multiple trusted sources;
- undocumented dependencies;
- incorrect owner attestations;
- stale inventories;
- human approval errors;
- new identity categories;
- business changes not yet reflected in source systems.

These remain residual risks.

---

# Implementation Boundaries

V3 implementation must:

- preserve all V1 and V2 files;
- create new V3-specific datasets and evidence;
- avoid overwriting V2 evidence;
- keep V3 implementation in separate files;
- create separate test evidence;
- be committed separately from the V3 decision and design.

---

# Production Authority Position

V3 design does not justify immediate full unattended remediation.

Until V3 implementation and testing are complete:

**Destructive production remediation remains limited.**

The final operating model will be determined after V3 testing and the later production-readiness phases.

---

# Design Conclusion

V3 adds a new architectural requirement:

**Evidence must be corroborated before destructive authority is granted.**

The system will no longer treat correct-looking IAM data as sufficient by itself.

Automatic remediation will require both:

- a supported security decision; and
- sufficiently trustworthy evidence.

This directly addresses the failure revealed by the emergency payroll integration account without adding another hard-coded exception.
