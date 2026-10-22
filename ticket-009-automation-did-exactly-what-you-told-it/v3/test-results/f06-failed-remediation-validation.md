# F06 — Failed Remediation Validation

## Test Objective

Verify that a failed approved remediation does not leave a partially committed identity state and that the failure is clearly visible to the operator.

## Test Identity

- Username: `nora.hayes`
- Initial enabled state: `True`
- Intended action: `DISABLE`
- Approval status: `APPROVED`

## Failure Injection

The remediation harness:

1. loaded the current working identity state;
2. prepared the intended disabled state;
3. wrote the proposed new state to a temporary file;
4. injected an `OSError` before atomic replacement of the working file;
5. removed the temporary file;
6. re-read the persisted working state;
7. logged the failure.

Injected error:

`Simulated remediation write failure before atomic replace.`

## Observed Result

Execution exited with code:

`1`

Audit evidence recorded:

- Result: `FAILED_REMEDIATION`
- Error type: `OSError`
- Enabled before: `True`
- Enabled after: `True`
- State change committed: `False`

## Result

**PASS**

The failed remediation did not modify the persisted identity state.

The account remained enabled after the simulated write failure.

## Fail-Safe Behavior

The remediation process failed closed.

The proposed change was prepared separately and was not allowed to replace the authoritative working state after the failure occurred.

This avoided a partial or ambiguous identity state.

## Known State After Failure

After the failed remediation:

- `nora.hayes` remained enabled;
- no destructive identity change was committed;
- the temporary state file was removed;
- the failure was recorded in the remediation failure log.

## Operator Signal

The failure generated:

- a nonzero exit code;
- explicit `FAILED_REMEDIATION` status;
- error type and error message;
- before and after identity state;
- explicit `state_change_committed = False`.

This prevents the operator from interpreting the failed operation as successful.

## Safe Resume

The remediation may be retried only after the underlying write failure is corrected.

Because the original state was preserved, retry begins from a known state rather than from a partially modified identity.

## Repeated-Damage Assessment

No repeated damage occurred.

Because the first remediation attempt committed no change, a later approved retry would evaluate the same original enabled state.

## Evidence

- `tests/v3-f06-failed-remediation.py`
- `simulation/v3-f06-failed-remediation-working.json`
- `evidence/v3-f06-remediation-failure-log.csv`

## Conclusion

F06 demonstrates that a remediation write failure fails closed and preserves the original identity state.

The operator receives clear failure evidence, no partial state is committed, and recovery can begin from a known state.
