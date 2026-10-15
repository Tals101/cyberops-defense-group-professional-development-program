# A01 — Secondary Evidence Poisoning Finding

## Test Objective

Determine whether an attacker who can manipulate a supposedly independent secondary evidence source can defeat V3 corroboration and obtain unattended destructive authority.

## Attack

The secondary record for `payroll.emergency` was changed from its real integration context to values that falsely agreed with the misleading primary IAM record.

Poisoned secondary values included:

- authoritative identity role: `employee`
- lifecycle status: `inactive`
- business criticality: `low`
- application dependency: empty
- authentication pattern: `interactive`
- source freshness: `current`
- source confidence: `high`

The poisoned secondary evidence therefore appeared to corroborate the incorrect primary record.

## Observed Result

V3 produced:

- Decision confidence: `HIGH`
- Evidence trust: `TRUSTED`
- Evidence trust reason: `Required primary and secondary evidence is sufficiently corroborated.`
- Recommendation: `DISABLE`
- Authority: `AUTO_REMEDIATE`
- Approval required: `NO`
- Actual action: `NO_ACTION_DRY_RUN`

## Result

**FAIL — SOURCE-INTEGRITY TRUST-BOUNDARY WEAKNESS**

The engine treated agreement between two inputs as sufficient corroboration even though one trusted source had been maliciously manipulated.

## Security Impact

The current V3 model proves that:

`agreement between sources != proof that the sources are trustworthy`

If an attacker can alter a secondary source while preserving apparently valid metadata, the attacker can manufacture corroboration and elevate destructive automation authority.

In this test, the poisoned evidence would have converted the protected payroll integration account from:

`REQUIRE_APPROVAL`

to:

`AUTO_REMEDIATE`

## Why Existing Controls Failed

V3 currently evaluates:

- evidence completeness;
- freshness labels;
- confidence labels;
- agreement between primary and secondary fields.

It does not yet independently verify:

- source provenance;
- source integrity;
- source authentication;
- tamper evidence;
- cryptographic or equivalent integrity controls;
- whether the source is independently administered;
- whether the same actor can manipulate both evidence paths.

Therefore, syntactically valid and mutually consistent poisoned evidence can be classified as `TRUSTED`.

## Safety Boundary That Prevented State Change

The adversarial test ran through the dry-run decision engine.

Therefore:

- unsafe authority was produced;
- no destructive identity state change occurred.

Dry-run containment prevented operational impact, but it does not correct the authority flaw.

## Required Corrective Control

Before V3 can treat secondary evidence as trusted for unattended destructive action, the evidence model must include source-integrity and provenance validation.

At minimum, the decision engine must require explicit source-integrity attributes such as:

- trusted source identifier;
- provenance validation status;
- integrity validation status;
- independent-source status.

If integrity or provenance cannot be validated, evidence trust must degrade and unattended destructive authority must be prohibited.

## Required Authority Rule

A safe model should enforce:

`corroborated content + unverified source integrity -> REQUIRE_APPROVAL or DO_NOT_AUTOMATE`

and only permit:

`AUTO_REMEDIATE`

when both content agreement and source integrity requirements are satisfied.

## Production Implication

Full unattended destructive identity remediation remains prohibited.

This finding confirms that evidence corroboration alone is insufficient without trusted-source integrity controls.

## Evidence

- `simulation/v3-a01-poisoned-secondary.json`
- `tests/v3-decision-engine-a01-test.py`
- `evidence/v3-a01-decisions.csv`
- `evidence/v3-a01.log`

## Conclusion

A01 successfully demonstrated that V3 can be manipulated through secondary evidence poisoning.

The failure will be preserved before implementing corrective source-integrity controls.
