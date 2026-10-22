# A02 — Freshness Metadata Forgery Finding

## Test Objective

Determine whether an attacker or faulty upstream source can cause V3 to trust stale secondary evidence by labeling it `current`.

## Attack

The secondary context for `nora.hayes` was modified to contain:

- source freshness label: `current`
- source confidence: `high`
- observation timestamp: `2025-01-01T00:00:00Z`

The evidence therefore contained a direct contradiction:

`freshness label = current`

while the underlying observation timestamp was stale.

The test used an isolated integrity baseline matching the A02 test file so that the A01 source-integrity control would pass and the freshness logic itself could be evaluated.

## Observed Result

Execution completed successfully with exit code:

`0`

V3 produced:

- Decision confidence: `HIGH`
- Evidence trust: `TRUSTED`
- Evidence trust reason: `Required primary and secondary evidence is sufficiently corroborated.`
- Recommendation: `DISABLE`
- Authority: `AUTO_REMEDIATE`
- Approval required: `NO`
- Actual action: `NO_ACTION_DRY_RUN`

## Result

**FAIL — FRESHNESS-VALIDATION WEAKNESS**

V3 trusted the source-provided freshness designation without independently validating the age of the underlying observation.

## Security Impact

The current design allows stale evidence to participate in unattended destructive authority when the source labels that evidence as current.

This demonstrates:

`source says current != evidence is actually current`

An attacker or faulty upstream process that can manipulate freshness metadata may cause outdated identity context to appear suitable for automatic remediation.

## Why Existing Controls Failed

V3 currently evaluates the source freshness field as a declared status.

It does not independently calculate evidence age from an observation timestamp.

Therefore the engine did not detect that:

`observed_at_utc = 2025-01-01T00:00:00Z`

was inconsistent with:

`source_freshness = current`

## Safety Boundary That Prevented State Change

The test was executed in dry-run mode.

Therefore:

- unsafe `AUTO_REMEDIATE` authority was produced;
- no actual account state change occurred.

Dry-run containment prevented operational impact but does not correct the authority weakness.

## Required Corrective Control

Freshness must be derived from an independently evaluated timestamp rather than trusted only as a source-provided label.

At minimum V3 should:

1. require a parseable observation timestamp for evidence used in unattended destructive decisions;
2. calculate evidence age;
3. compare the age against a defined maximum freshness threshold;
4. mark evidence stale when the calculated age exceeds that threshold;
5. degrade automation authority when timestamps are missing, invalid, or stale.

## Required Authority Rule

A safe model should enforce:

`declared current + stale timestamp -> STALE evidence trust`

and:

`STALE evidence trust -> no AUTO_REMEDIATE`

## Production Implication

Full unattended destructive identity remediation remains prohibited until evidence freshness is independently validated.

## Evidence

- `simulation/v3-a02-forged-freshness-secondary.json`
- `tests/v3-a02-source-integrity-baseline.json`
- `tests/v3-decision-engine-a02-test.py`
- `evidence/v3-a02-decisions.csv`
- `evidence/v3-a02.log`

## Conclusion

A02 successfully demonstrated that V3 can be misled by forged freshness metadata.

The failure will be preserved before implementing timestamp-based freshness validation.
