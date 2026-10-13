# Ticket #009 — Phase 9 V3 Decision

## Decision

**V3 is justified.**

V2 is not sufficient for broader unattended destructive remediation because the Security Engineering payroll test demonstrated that correct decision logic can still produce an unsafe recommendation when trusted IAM source data is materially wrong.

The required response is an architectural modification to the automation trust model.

V2 will be preserved.

---

# Problem

V2 evaluates identity context more safely than V1, but it still assumes that the identity attributes it receives are sufficiently accurate to authorize remediation.

The emergency payroll integration account exposed a failure mode in which:

- IAM classified the identity incorrectly;
- the account appeared to be an ordinary inactive identity;
- the account was not marked as a service account;
- the account was not privileged;
- the identity record met V2 remediation criteria;
- the account actually supported a critical payroll integration.

V2 interpreted the available evidence correctly.

The evidence itself was wrong.

---

# Security Significance

The consequence is significant because destructive automation can become unsafe without any code defect.

If an incorrect, stale, incomplete, or manipulated source record satisfies the automation's policy, the automation may convert bad information directly into a production change.

This creates risk from:

- IAM governance failures;
- stale classifications;
- undocumented service dependencies;
- manually created identities;
- inconsistent source systems;
- attacker manipulation of trusted attributes;
- synchronization errors;
- incomplete ownership information.

The payroll test demonstrates that V2's authority can still exceed the reliability of its evidence.

---

# Possible Responses

## Option 1 — Keep V2 and Add an Operational Warning

Continue using V2 and instruct operators to review unusual cases.

### Benefit

Minimal engineering change.

### Weakness

The automation can still automatically disable an incorrectly classified identity before a person notices.

This does not address the control failure.

**Rejected.**

---

## Option 2 — Add a Payroll-Specific Exception

Exclude the discovered payroll identity or payroll-related accounts.

### Benefit

Prevents this exact test account from being disabled.

### Weakness

Creates another allowlist and treats the symptom rather than the trust problem.

Other misclassified critical identities would remain vulnerable.

**Rejected.**

---

## Option 3 — Disable All Automatic Remediation Permanently

Use the system only for detection and recommendations.

### Benefit

Strong reduction in destructive automation risk.

### Weakness

Eliminates automation even for low-impact cases where evidence is sufficiently strong and independently corroborated.

This is safer but unnecessarily restrictive if authority can be bounded appropriately.

**Not selected as the target architecture.**

---

## Option 4 — Address Only IAM Governance

Require IAM teams to improve classification quality while leaving V2 unchanged.

### Benefit

Improves source-data quality.

### Weakness

No production data source can be assumed perfect.

Automation should not rely on governance alone when the action is destructive.

**Insufficient by itself.**

---

## Option 5 — Architect V3 With Evidence Corroboration

Require destructive automatic remediation to satisfy both:

1. decision-policy requirements; and
2. evidence-trust requirements.

Critical identity facts must be corroborated before unattended destructive authority is granted.

Conflicting, missing, stale, or uncorroborated evidence reduces authority.

**Selected.**

---

# Selected Response

Implement **V3 — Corroborated Evidence Authority**.

V3 will preserve the V2 decision architecture but add an independent evidence-trust gate before destructive remediation may occur.

The decision path becomes:

**Identity  
→ Primary Evidence  
→ Secondary Evidence  
→ Evidence Agreement  
→ Confidence  
→ Decision  
→ Authority  
→ Action  
→ Validation  
→ Recovery**

The key architectural change is:

> A remediation decision being logically correct is no longer sufficient for automatic destructive authority.

The system must also establish that the critical facts supporting that decision are trustworthy enough for the potential consequence.

---

# V3 Core Requirements

V3 should require corroboration for destructive automatic actions.

At minimum, V3 should evaluate:

- identity classification;
- workforce lifecycle state;
- ownership;
- business purpose;
- service/application dependency;
- activity evidence;
- privilege;
- evidence freshness;
- evidence completeness;
- source agreement.

Where a secondary source is unavailable, conflicting, or materially incomplete, V3 must reduce authority.

---

# Proposed Evidence Sources for the Lab

Because Ticket #009 uses a synthetic environment, V3 will simulate a secondary authoritative context source.

The secondary source should represent information such as:

- CMDB;
- application inventory;
- service ownership registry;
- HR lifecycle source;
- PAM inventory;
- dependency registry.

The lab should include the emergency payroll identity with:

- misleading IAM classification;
- secondary evidence identifying a critical payroll dependency.

This allows the architecture to demonstrate that the discrepancy is detected before destructive action.

---

# V3 Authority Rule

An identity may receive `AUTO_REMEDIATE` authority for a destructive action only when:

1. the identity type is recognized;
2. required evidence is complete;
3. evidence is current;
4. the lifecycle state supports remediation;
5. ownership is known or authoritative disposition exists;
6. no high-impact dependency is known;
7. required primary and secondary evidence agree;
8. no critical contradictory evidence exists;
9. confidence meets the destructive-action threshold;
10. rollback capability is available.

If critical evidence disagrees:

`REQUIRE_APPROVAL`

or:

`DO_NOT_AUTOMATE`

depending on impact and uncertainty.

---

# Why V3 Is Required

The payroll scenario invalidates an important V2 assumption:

> Accurate-looking identity context is sufficiently trustworthy to authorize destructive action.

That assumption is no longer defensible.

V3 is justified because the required protection changes the architecture of the decision process rather than merely changing a threshold or adding an exception.

The system now needs an explicit evidence-trust layer.

---

# What V3 Does Not Solve

V3 will not guarantee that every identity record is correct.

Multiple sources can:

- share the same bad upstream data;
- become stale simultaneously;
- be compromised;
- contain incomplete dependency information.

Corroboration reduces risk but does not eliminate it.

High-impact or uncertain cases must still retain human approval boundaries.

---

# Residual Risk

Even with V3:

- two sources may agree and still be wrong;
- undocumented dependencies may remain unknown;
- data synchronization can introduce delay;
- attackers may attempt to manipulate multiple trusted sources;
- owners may incorrectly attest to purpose;
- new identity types may appear;
- business criticality may change faster than inventories.

Therefore V3 must continue to use:

- bounded automation authority;
- approval gates;
- action limits;
- pre-change snapshots;
- rollback;
- health validation;
- audit logging;
- emergency stop;
- deferred-action controls.

---

# V2 Preservation

V2 must remain preserved as the previous architecture and evidence baseline.

V3 implementation must be committed separately.

No V2 evidence should be overwritten to make V3 appear safer.

---

# Phase 9 Decision

**V3 REQUIRED — ARCHITECTURAL MODIFICATION**

Reason:

The newly discovered risk cannot be adequately addressed by:

- another exception;
- a warning;
- IAM governance alone;
- or unchanged V2 logic.

V3 will add corroborated evidence as a prerequisite for unattended destructive remediation.

The objective is not to make the automation more aggressive.

The objective is to ensure that automation authority is proportional to both:

- decision confidence; and
- evidence trustworthiness.
