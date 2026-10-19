# F09 — Unrecognized Identity Type Validation

## Test Objective

Verify that V3 does not guess or assume remediation authority when an identity has an unsupported or unrecognized identity type.

## Test Identity

- Username: `nora.hayes`
- Original identity type: `employee`
- Injected identity type: `robot_account`
- Enabled state: `True`
- Lifecycle state: `inactive`

## Test Method

A copy of the canonical V3 identity dataset was modified so that `nora.hayes` used the unsupported identity type:

`robot_account`

The isolated V3 decision engine was then executed against the modified dataset.

## Observed Result

The decision engine produced:

- Decision confidence: `HIGH`
- Evidence trust: `TRUSTED`
- Recommendation: `REVIEW`
- Authority: `DO_NOT_AUTOMATE`
- Approval required: `NO`
- Actual action: `NO_ACTION_DRY_RUN`

## Result

**PASS**

The automation did not infer destructive authority for an unsupported identity type.

## Safety Interpretation

High-confidence and trusted evidence alone are not sufficient to grant destructive automation authority.

Identity type must also be explicitly supported by policy.

Conceptually:

`trusted evidence + unsupported identity type -> DO_NOT_AUTOMATE`

This prevents the system from applying employee, contractor, service-account, or privileged-account rules to an identity category it does not understand.

## Known State

The test was performed in dry-run mode.

No identity state was changed.

## Operator Signal

The result clearly indicates:

- recommendation requires review;
- automation authority is denied;
- no remediation action occurred.

The operator can therefore distinguish an unsupported type from a normal auto-remediation candidate.

## Safe Resume

Automation should resume only after:

1. the identity type is correctly classified; or
2. policy is formally extended to support the new identity class;
3. safeguards and authority rules for that identity class are reviewed and tested.

## Repeated-Damage Assessment

Repeated execution against the same unsupported identity type continues to produce `DO_NOT_AUTOMATE`.

No destructive action is authorized.

## Evidence

- `simulation/v3-f09-unrecognized-type.json`
- `tests/v3-decision-engine-f09-test.py`
- `evidence/v3-f09-decisions.csv`
- `evidence/v3-f09.log`

## Conclusion

F09 demonstrates that V3 treats unknown or unsupported identity classes as an authority boundary.

The engine refuses unattended remediation instead of guessing which policy should apply.
