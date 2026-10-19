# A03 — Approval Forgery / Replay Finding

## Test Objective
Determine whether V3 remediation can be authorized using an unverified or forged approval value.

## Attack
An isolated copy of the approved-operation workflow was used.

The operation relied on:

`APPROVAL_STATUS = "APPROVED"`

No independent approval artifact was provided.

The workflow did not validate:
- approval request ID
- approver identity
- target identity binding
- requested action binding
- approval timestamp
- expiration
- cryptographic integrity
- one-time-use status
- prior consumption or replay

## Initial State
Target identity:

- Username: `nora.hayes`
- Enabled: `True`

## Observed Result
The forged approval value was accepted.

Execution result:

- Approval: `APPROVED`
- Enabled before: `True`
- Action: `DISABLE`
- Result: `SUCCESS`
- Enabled after: `False`

## Result
**FAIL — APPROVAL TRUST-BOUNDARY WEAKNESS**

The remediation path trusted a locally asserted approval status rather than independently verifying an authoritative approval artifact.

The effective control was:

`string says APPROVED -> destructive action permitted`

This means an attacker, faulty script, or unauthorized operator able to alter the execution context could potentially manufacture approval.

## Security Impact
Approval-gated remediation cannot be considered a reliable safety boundary if approval can be represented only by an unverified local value.

The same design also provides no replay protection. A previously valid approval could potentially be reused because no unique approval identifier or consumption ledger is checked.

## Required Corrective Control
Approval-gated destructive remediation must require a structured approval artifact containing at minimum:

- unique approval ID
- target username
- requested action
- approver identity
- approval status
- issued timestamp
- expiration timestamp
- integrity protection
- one-time-use enforcement

The remediation operation must independently verify that:

1. the approval artifact is authentic,
2. the approval is for the exact target,
3. the approval is for the exact requested action,
4. the approval has not expired,
5. the approval has not previously been consumed.

Authority rule:

`unverified approval -> BLOCK`

`expired approval -> BLOCK`

`replayed approval -> BLOCK`

`valid bound unused approval -> remediation may proceed`

## Evidence
- `simulation/v3-a03-approval-forgery-working.json`
- `tests/v3-a03-approval-forgery-test.py`
- `evidence/v3-a03-approval-forgery-log.csv`

## Conclusion
A03 demonstrated that the existing approval mechanism is not a trustworthy authorization boundary.

The failure must be preserved before implementing the corrective control.

## Replay Validation

The same approval artifact was executed twice using the identical approval reference:

`GENERIC-APPROVAL-A03`

### First Execution
- Target: `payroll.emergency`
- Enabled before: `True`
- Action: `DISABLE`
- Result: `SUCCESS`
- Enabled after: `False`

### Second Execution
The working identity state was restored, but the approval artifact was not changed or reissued.

The same approval reference was submitted again.

- Target: `payroll.emergency`
- Approval reference: `GENERIC-APPROVAL-A03`
- Enabled before: `True`
- Action: `DISABLE`
- Result: `SUCCESS`
- Enabled after: `False`

The execution log therefore contains two successful destructive operations using the same approval reference.

## Replay Result
**FAIL — APPROVAL REPLAY PROTECTION ABSENT**

There is no consumed-approval ledger or one-time-use validation preventing an already used approval from authorizing another destructive operation.

This confirms that approval must be both authenticated and transaction-bound, with explicit replay protection.
