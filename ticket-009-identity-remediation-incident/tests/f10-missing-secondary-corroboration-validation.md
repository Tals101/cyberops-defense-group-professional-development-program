# F10 — Missing Secondary Corroboration Validation

## Test Objective

Verify that V3 reduces automation authority when required secondary corroborating evidence is missing.

## Test Identity

- Username: `nora.hayes`
- Primary identity record: present
- Secondary corroborating record: removed
- Enabled state: `True`
- Lifecycle state: `inactive`

## Test Method

A copy of the canonical V3 secondary-context dataset was created.

The secondary corroboration record for `nora.hayes` was removed while the primary IAM record remained unchanged.

The isolated V3 decision engine was then executed against:

- canonical primary identity data; and
- the modified secondary-context dataset.

## Observed Result

The decision engine produced:

- Decision confidence: `HIGH`
- Evidence trust: `INCOMPLETE`
- Evidence trust reason: `No secondary corroborating record exists.`
- Recommendation: `DISABLE`
- Authority: `REQUIRE_APPROVAL`
- Approval required: `YES`
- Actual action: `NO_ACTION_DRY_RUN`

## Result

**PASS**

The absence of secondary corroboration reduced automation authority.

The engine did not allow unattended destructive remediation.

## Safety Interpretation

Decision confidence and evidence trust are separate control dimensions.

The primary evidence was sufficient for the policy logic to produce a high-confidence disable recommendation.

However, missing secondary evidence prevented the recommendation from becoming automatic execution authority.

Conceptually:

`HIGH decision confidence + INCOMPLETE evidence trust -> REQUIRE_APPROVAL`

This prevents a single source of truth from independently authorizing destructive action when corroboration is required.

## Known State

The test was performed in dry-run mode.

No identity state was changed.

## Operator Signal

The decision record clearly reports:

- missing secondary corroboration;
- `INCOMPLETE` evidence trust;
- `REQUIRE_APPROVAL` authority;
- no automatic action.

This gives the operator an explicit reason for the reduced authority.

## Safe Resume

Unattended remediation should resume only after:

1. secondary corroborating evidence becomes available;
2. the evidence is current and trustworthy;
3. the secondary record agrees with the primary identity context;
4. the decision is re-evaluated under the full V3 evidence model.

A human may separately review and approve the action if policy permits approval-gated remediation.

## Repeated-Damage Assessment

Repeated execution while secondary evidence remains absent continues to require approval.

No unattended destructive change is authorized.

## Evidence

- `simulation/v3-f10-missing-secondary-context.json`
- `tests/v3-decision-engine-f10-test.py`
- `evidence/v3-f10-decisions.csv`
- `evidence/v3-f10.log`

## Conclusion

F10 demonstrates that V3 does not treat missing corroboration as equivalent to trusted evidence.

A high-confidence recommendation cannot become unattended destructive authority when required secondary context is absent.
