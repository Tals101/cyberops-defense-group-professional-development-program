# F08 — Approval Timeout Validation

## Test Objective

Verify that an approval-gated destructive remediation cannot proceed when approval remains pending beyond the allowed approval window.

## Test Identity

- Username: `payroll.emergency`
- Initial enabled state: `True`
- Intended action: `DISABLE`
- Approval status: `PENDING`

## Approval Conditions

Approval age:

`180 minutes`

Configured approval timeout:

`60 minutes`

The approval therefore exceeded the allowed window.

## Observed Result

Execution exited with code:

`1`

The automation reported:

- Result: `APPROVAL_TIMEOUT`
- Approval status: `PENDING`
- Approval age: `180`
- Approval timeout: `60`
- Enabled before: `True`
- Enabled after: `True`
- State change committed: `False`
- Required operator action: `ESCALATE_APPROVAL_TIMEOUT`

## Result

**PASS**

The approval-gated remediation did not proceed after the approval window expired.

The identity remained unchanged.

## Fail-Safe Behavior

Expired or unresolved approval does not default to authorization.

Instead:

`pending approval + expired approval window -> no destructive action`

This prevents stale, abandoned, or forgotten approval requests from becoming implicit authorization.

## Known State After Timeout

After the timeout condition:

- `payroll.emergency` remained enabled;
- no destructive state change occurred;
- the approval remained unresolved;
- operator escalation was required.

## Operator Signal

The timeout produced:

- a nonzero exit code;
- explicit `APPROVAL_TIMEOUT` result;
- approval age and timeout threshold;
- before and after state;
- explicit `state_change_committed = False`;
- required action `ESCALATE_APPROVAL_TIMEOUT`.

## Safe Resume

Automation must not automatically continue using the expired approval request.

A safe retry requires:

1. review of the current identity evidence;
2. confirmation that the requested remediation is still appropriate;
3. a new or renewed valid approval;
4. revalidation of account state before execution.

## Repeated-Damage Assessment

Repeated execution while approval remains expired must continue to block the destructive action.

No account change should occur until valid human approval exists.

## Evidence

- `tests/v3-f08-approval-timeout.py`
- `simulation/v3-f08-approval-timeout-working.json`
- `evidence/v3-f08-approval-timeout-log.csv`

## Conclusion

F08 demonstrates that approval timeout fails closed.

Destructive remediation cannot proceed on stale pending approval, the account remains unchanged, and the operator receives a clear escalation signal before any future action.
