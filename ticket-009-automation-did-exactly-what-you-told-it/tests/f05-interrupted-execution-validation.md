# F05 — Interrupted Execution Validation

## Test Objective

Verify that an approved V3 remediation batch can be safely resumed after interruption without repeating completed destructive actions or losing track of remaining work.

## Test Identities

### nora.hayes
- Initial enabled state: `True`
- Lifecycle state: `inactive`
- Days since interactive login: `135`

### kevin.brooks
- Initial enabled state: `True`
- Lifecycle state: `pending_disable`
- Days since interactive login: `18`

## Test Method

A two-account approved remediation batch was executed with a simulated interruption after the first successful state change.

The same operation was then restarted against the persisted working state.

## First Execution

Observed:

- `nora.hayes`
  - Enabled before: `True`
  - Action: `DISABLE`
  - Result: `SUCCESS`
  - Enabled after: `False`

Execution then stopped with simulated interruption exit code `2`.

At interruption:

- `nora.hayes = False`
- `kevin.brooks = True`

This confirmed that the completed change was persisted while the second identity remained untouched.

## Restart Execution

The same remediation operation was executed again.

Observed:

### nora.hayes
- Enabled before: `False`
- Action: `NO_ACTION`
- Result: `ALREADY_DISABLED`
- Enabled after: `False`

### kevin.brooks
- Enabled before: `True`
- Action: `DISABLE`
- Result: `SUCCESS`
- Enabled after: `False`

## Result

**PASS**

The interrupted operation could be safely restarted.

The restart:

- preserved the already completed Nora remediation;
- did not issue another destructive action against Nora;
- resumed processing the remaining Kevin remediation;
- reached the intended final state for both identities.

## Failure-State Visibility

After interruption, the environment remained in a known state:

- completed changes were persisted;
- untouched identities retained their previous state;
- the execution log identified exactly which actions had completed.

## Safe Resume Behavior

Recovery does not depend on blindly replaying commands.

Each identity is evaluated against the desired state:

`enabled != desired state -> perform change`

`enabled == desired state -> no action`

This allows execution to resume after interruption without duplicating previously completed remediation.

## Repeated-Damage Assessment

No repeated destructive impact occurred.

Nora was disabled once only.

On restart, the completed action was identified as `ALREADY_DISABLED`, and processing continued to Kevin.

## Operator Signal

The execution log provides sufficient information to distinguish:

- successful remediation;
- already-completed remediation;
- remaining work.

This supports controlled operator recovery after an interrupted run.

## Evidence

- `tests/v3-f05-interrupted-execution.py`
- `simulation/v3-f05-interrupted-working.json`
- `evidence/v3-f05-execution-log.csv`

## Conclusion

F05 demonstrates that the V3 remediation pattern can recover safely from an interrupted execution.

Completed changes remain durable, repeated execution is idempotent, and remaining approved work can continue without reapplying completed destructive actions.
