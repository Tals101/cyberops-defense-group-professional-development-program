# Ticket #009 — Bad-Data / Emergency Payroll Account Analysis

## Scenario

Security Engineering created a test identity with the following characteristics:

- not marked as a service account;
- not privileged;
- technically inactive according to IAM data;
- still enabled;
- owned by a current employee.

V2 determined that the identity met the criteria for remediation.

The test was stopped before remediation occurred.

Security Engineering then disclosed that the identity was actually an emergency payroll integration account that had been manually created approximately two years earlier and had never been classified correctly in IAM.

The automation interpreted the available data correctly.

The available data was wrong.

---

# Did V2 Fail?

## Answer

**Yes, at the system-design level, but not because its decision code malfunctioned.**

V2 processed the attributes it was given according to its documented logic.

Based on those attributes, the remediation recommendation was internally consistent.

However, V2 still allowed potentially destructive authority to depend on identity attributes whose accuracy had not been independently established.

Therefore:

- the V2 logic did not suffer a conventional coding failure;
- the V2 trust model was still insufficient for destructive remediation.

A system can execute its rules correctly and still be unsafe.

---

# Did IAM Data Fail?

## Answer

**Yes.**

The IAM record did not accurately represent the identity's actual business purpose.

The emergency payroll integration account was not correctly identified as a service or integration identity.

As a result, important context was absent or incorrect.

The automation therefore received a technically valid but operationally misleading identity record.

---

# Did Both Fail?

## Answer

**Yes, but in different ways.**

IAM failed by supplying inaccurate classification data.

V2 failed by treating those data attributes as sufficiently trustworthy to support automatic destructive remediation.

The incident therefore represents both:

- an IAM governance/data-quality failure; and
- an automation authority/trust-design failure.

---

# Is Technically Correct Automation Safe When Its Source Data Is Wrong?

## Answer

**No.**

Correct logic cannot compensate for materially incorrect evidence.

An automated decision can be perfectly consistent with its programmed policy and still create an unsafe production outcome when the source data misrepresents reality.

Destructive automation therefore requires assurance not only that:

- the logic is correct;

but also that:

- the evidence is trustworthy enough for the consequence of the action.

---

# Which Identity Attributes Can Be Trusted Enough to Authorize Destructive Action?

No single identity attribute should independently authorize destructive remediation when the operational consequence may be significant.

Higher-confidence destructive action should require corroborating evidence.

Potential evidence includes:

- authoritative workforce lifecycle state;
- identity type;
- known owner;
- documented business purpose;
- recent interactive activity;
- recent non-interactive authentication;
- application or service dependencies;
- privilege;
- approval state;
- account creation source;
- CMDB or application inventory linkage;
- service ownership records;
- PAM records where applicable;
- recent successful authentication telemetry;
- dependency or health-check evidence.

The reliability of each source must also be known.

A field being present in IAM does not automatically make it authoritative for every decision.

---

# How Should Missing or Conflicting Context Affect Confidence?

Missing, stale, or conflicting context must reduce confidence.

It must never be silently interpreted in favor of destructive action.

Examples:

- unknown owner;
- uncertain business purpose;
- disagreement between IAM and application inventory;
- missing authentication telemetry;
- unknown identity type;
- stale lifecycle data;
- incomplete dependency information.

For destructive remediation, material uncertainty should result in:

`REQUIRE_APPROVAL`

or:

`DO_NOT_AUTOMATE`

depending on potential impact.

---

# Should Critical Facts Be Verified Using More Than One Source?

## Answer

**Yes, when practical and when the consequence justifies it.**

Critical identity facts that influence destructive authority should be corroborated where possible.

For example:

IAM may identify an account as an employee account, while:

- CMDB identifies it as an application dependency;
- authentication telemetry shows automated use;
- service ownership data links it to Payroll;
- an application registry identifies it as an integration credential.

Conflicting evidence should lower confidence rather than be resolved automatically in favor of the IAM label.

---

# What Should Happen When Identity Purpose Cannot Be Established Confidently?

The automation must preserve the current production state.

The identity should be:

- marked for investigation;
- prevented from unattended destructive remediation;
- assigned a confidence level reflecting the uncertainty;
- routed to the appropriate owner or approver.

Default behavior:

**Do not disable when material purpose is unknown.**

This is not equivalent to declaring the account safe.

It means the evidence is insufficient to authorize the destructive action.

---

# Is This Primarily an IAM Governance Problem, an Automation Problem, or Both?

## Answer

**Both.**

## IAM Governance Problem

IAM failed to maintain accurate classification and purpose information for a production identity.

The inaccurate record could affect:

- lifecycle management;
- access reviews;
- remediation;
- reporting;
- security investigations.

## Automation Problem

V2 relied too heavily on a single logical view of identity context.

It lacked sufficient corroboration for destructive action when the authoritative data itself was incorrect.

The automation therefore had more authority than the reliability of its source evidence justified.

---

# Security Significance

The emergency payroll identity exposes a different failure mode than the original Finance incident.

The original incident demonstrated:

> Correct execution of oversimplified logic.

The payroll scenario demonstrates:

> Correct execution of improved logic using incorrect source data.

This matters because adding better rules does not solve unreliable evidence.

If an attacker or operational error can manipulate the data the automation trusts, then the remediation system can become a mechanism for causing production impact.

---

# Required Change

The appropriate response is **not another hard-coded payroll exception**.

The trust model for destructive automation must change.

Destructive automatic remediation should require sufficient corroboration of critical identity facts before authority is granted.

At minimum, high-confidence automatic disablement should require:

1. a recognized identity type;
2. sufficiently complete and current evidence;
3. authoritative lifecycle evidence;
4. known ownership or documented disposition;
5. no known high-impact dependency;
6. no conflicting evidence from secondary sources;
7. confidence above the defined destructive-action threshold.

Where critical context cannot be verified, the system must reduce authority to:

`REQUIRE_APPROVAL`

or:

`DO_NOT_AUTOMATE`

---

# Conclusion

The emergency payroll account demonstrates that:

**correct automation can still make an unsafe decision when trusted source data is wrong.**

The lesson is not to add another exception.

The lesson is that automation authority must be proportional not only to the decision logic, but also to the demonstrated reliability and corroboration of the evidence on which that decision depends.

This finding requires evaluation of the V2 architecture before broader unattended remediation authority can be approved.
