# A01 — Secondary Evidence Poisoning Corrective Validation

## Test Objective

Validate the corrective source-integrity control added after A01 demonstrated that poisoned secondary evidence could manufacture trusted corroboration.

## Original Failure

The initial A01 test showed that a maliciously altered secondary evidence source could be made to agree with the misleading primary IAM record.

The original V3 engine then produced:

- Decision confidence: `HIGH`
- Evidence trust: `TRUSTED`
- Recommendation: `DISABLE`
- Authority: `AUTO_REMEDIATE`
- Approval required: `NO`

This demonstrated that content agreement alone was insufficient to establish trustworthy corroboration.

## Corrective Control

A separate integrity baseline was created for the canonical secondary identity-context source.

Control components:

- algorithm: `SHA256`
- trusted canonical secondary file:
  `simulation/v3-secondary-context.json`
- expected canonical hash:
  `A2413FFEC3AE18A8573205588EC4E2EBDF692E7B6C7563C588B31808FDC21E24`
- integrity validation occurs before decision generation
- integrity failure terminates processing
- no decisions are generated after integrity failure

The lab baseline is stored at:

`automation/v3-source-integrity-baseline.json`

Production design requires this reference to be stored outside the automation account's writable boundary.

## Corrected Adversarial Retest

The corrected V3 engine was executed against the previously poisoned secondary source.

Poisoned source hash:

`3F23D57B9B6DE48379898B025CD2C59C6C90C015020A2D9D3D9D4B7C61F2B366`

Expected trusted hash:

`A2413FFEC3AE18A8573205588EC4E2EBDF692E7B6C7563C588B31808FDC21E24`

## Observed Result

Execution produced:

- Exit code: `1`
- Status: `FAIL_CLOSED`
- Failure type: `SECONDARY_SOURCE_INTEGRITY_FAILURE`
- Decision records: `0`
- Remediation performed: `False`
- Required operator action: `INVESTIGATE_SOURCE_INTEGRITY`

No decision CSV was created.

## Result

**PASS AFTER CORRECTIVE CONTROL**

The poisoned source was rejected before its contents could influence identity-remediation authority.

## Safety Improvement

The corrected model no longer assumes:

`source agreement = source trust`

Instead, destructive authority now depends on both:

1. evidence content; and
2. validated source integrity.

A secondary source whose contents differ from the protected baseline cannot participate in automated authority decisions.

## Canonical Regression

The unmodified canonical secondary source was also retested.

Observed:

- Exit code: `0`
- Primary identities: `11`
- Secondary records: `11`
- Decision records: `11`

For `payroll.emergency`:

- Decision confidence: `HIGH`
- Evidence trust: `CONFLICTING`
- Recommendation: `DISABLE`
- Authority: `REQUIRE_APPROVAL`
- Approval required: `YES`
- Actual action: `NO_ACTION_DRY_RUN`

The integrity control therefore blocked tampered evidence without breaking the normal V3 corroboration workflow.

## Operator Signal

On integrity failure the operator receives:

- explicit integrity-failure status;
- trusted expected hash;
- observed source hash;
- zero decision count;
- confirmation that no remediation occurred;
- required action `INVESTIGATE_SOURCE_INTEGRITY`.

## Safe Resume

Automation must not resume until:

1. the secondary source is investigated;
2. the source is restored from a trusted version;
3. the source hash matches the protected baseline;
4. provenance and ownership are confirmed;
5. the automation is re-run from the beginning.

## Production Requirement

The integrity baseline itself must be protected from the same automation identity that reads the secondary source.

If an attacker can modify both:

- the secondary evidence source; and
- its expected integrity baseline,

the control can be bypassed.

Therefore production deployment requires separation of write authority and protected integrity metadata.

## Evidence

- `automation/v3-source-integrity-baseline.json`
- `automation/v3-decision-engine.py`
- `tests/v3-decision-engine-a01-fixed-test.py`
- `evidence/v3-a01-fixed.log`
- `simulation/v3-a01-poisoned-secondary.json`
- `tests/a01-secondary-evidence-poisoning-finding.md`

## Conclusion

A01 now passes after corrective control.

V3 rejects altered secondary evidence before decision generation and fails closed instead of allowing poisoned corroboration to create unattended destructive authority.
