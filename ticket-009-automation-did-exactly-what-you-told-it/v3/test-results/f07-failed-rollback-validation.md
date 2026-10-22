# F07 — Failed Rollback Validation

## Test Objective

Verify that when rollback itself fails, the system does not falsely report recovery and instead leaves the environment in a known unrecovered state with explicit operator escalation.

## Test Scenario

A pre-change snapshot was created from the canonical V3 identity dataset.

The working copy was then intentionally modified so that:

- `payroll.emergency`
- original state: `enabled = True`
- bad working state: `enabled = False`

The snapshot and working state had different SHA256 hashes before rollback.

## Failure Injection

The rollback harness:

1. copied the known-good snapshot to a temporary restore file;
2. injected an `OSError` before replacing the authoritative working file;
3. removed the temporary restore file;
4. recalculated the working-state hash;
5. compared it with the snapshot hash;
6. logged the failed recovery;
7. required manual escalation.

Injected error:

`Simulated rollback failure before authoritative state replacement.`

## Observed Result

Execution exited with code:

`1`

Snapshot hash:

`788A284E00CE8EB711ADD003B908082B804FE9434E85B5AF0E7B50A22F39F7CB`

Working-state hash before rollback:

`E9A6044B3E12E0BA28C901AB62CDB3FBE3A02E4321F6E3775D83A5DE009C56DC`

Working-state hash after failed rollback:

`E9A6044B3E12E0BA28C901AB62CDB3FBE3A02E4321F6E3775D83A5DE009C56DC`

Rollback result:

`FAILED_ROLLBACK`

Restored:

`False`

Required operator action:

`ESCALATE_MANUAL_RECOVERY`

## Identity State After Failure

`payroll.emergency` remained:

`enabled = False`

The system did not claim that the account had been restored.

## Result

**PASS**

The failed rollback was detected and clearly reported.

The system did not:

- overwrite the working state with an incomplete restore;
- falsely report rollback success;
- mark the environment as recovered;
- silently continue automation.

## Fail-Safe Behavior

Rollback failure left the system in a known unrecovered state.

Because the working file was not partially replaced, the post-failure state remained deterministic and could be independently inspected.

## Operator Signal

The failure produced:

- a nonzero exit code;
- explicit `FAILED_ROLLBACK` status;
- snapshot hash;
- before and after working hashes;
- explicit `restored = False`;
- error type and message;
- required action `ESCALATE_MANUAL_RECOVERY`.

## Escalation Path

When rollback fails:

1. stop further automated remediation;
2. preserve current evidence;
3. activate emergency stop;
4. escalate to a human operator;
5. perform controlled manual recovery from the known-good snapshot;
6. validate identity and dependent application state;
7. resume automation only after recovery is verified.

## Safe Resume

Automation must not resume merely because a rollback was attempted.

Resume requires verified recovery and confirmation that:

- authoritative identity state matches the intended snapshot;
- dependent services are healthy;
- audit evidence is intact;
- the failure cause has been corrected.

## Repeated-Damage Assessment

Repeated automatic rollback attempts should not continue indefinitely.

After a rollback failure, authority must transfer to human-controlled recovery rather than repeated destructive automation.

## Evidence

- `evidence/v3-f07-prechange-snapshot.json`
- `simulation/v3-f07-rollback-working.json`
- `evidence/v3-f07-rollback-failure-log.csv`
- `tests/v3-f07-failed-rollback.py`

## Conclusion

F07 demonstrates that rollback failure is treated as a distinct high-severity automation failure.

The system preserves a known state, refuses to claim successful recovery, and requires explicit manual escalation before automation can safely resume.
