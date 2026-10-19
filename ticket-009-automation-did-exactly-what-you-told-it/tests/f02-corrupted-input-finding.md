# Ticket #009 — F02 Corrupted Input Finding

## Test

F02 — Corrupted Input

## Objective

Determine whether V3 safely handles malformed primary identity input and whether the failure is visible to an operator through controlled evidence.

---

# Failure Injection

Test input:

`simulation/v3-f02-corrupted-input.json`

The canonical V3 identity dataset was copied to a test-only file.

Invalid content was appended:

`THIS_IS_NOT_VALID_JSON`

The canonical V3 dataset remained unchanged.

---

# Expected Behavior

The system should:

- reject malformed input;
- perform no remediation decision;
- perform no destructive action;
- return a non-zero exit code;
- leave the environment in a known state;
- create controlled failure evidence for the operator.

---

# Actual Behavior

The V3 test engine terminated with:

`json.decoder.JSONDecodeError`

Error detail:

`Extra data: line 207 column 1`

Exit code:

`1`

Decision output created:

`False`

Audit log created:

`False`

No remediation decision or state-changing action occurred.

---

# Fail Open or Fail Closed?

For destructive action:

**FAIL CLOSED**

The parser failed before any decision or remediation path could execute.

---

# Was This the Correct Behavior?

Partially.

The security behavior was correct because malformed input could not reach remediation.

However, the operational behavior was incomplete because the engine emitted only an unhandled Python traceback.

A production automation system should create a controlled failure record that tells an operator:

- which source failed;
- why processing stopped;
- that no remediation occurred;
- whether it is safe to rerun after correction.

---

# Was the Environment Left in a Known State?

**Yes.**

No decision file was created.

No state-changing action occurred.

The canonical V3 dataset was not modified.

---

# Did the Operator Know Something Failed?

**Yes, but only through the Python traceback.**

This is insufficient for production operations.

The expected control is a concise and durable audit record rather than reliance on terminal output.

---

# Can Execution Safely Resume?

Yes, after:

1. correcting or restoring the malformed input;
2. validating the repaired JSON;
3. rerunning the decision process from the beginning.

No rollback is required because no state change occurred.

---

# Could Repeated Execution Cause Additional Damage?

With the same malformed input:

No destructive state change is expected.

Repeated runs would continue failing during parsing.

However, repeated uncontrolled failures could create operational noise and obscure the underlying issue.

---

# Result

**PARTIAL PASS — SAFETY PASS / OBSERVABILITY GAP**

V3 correctly prevented malformed data from reaching destructive automation.

However, it did not generate controlled failure evidence.

---

# Required Corrective Control

The canonical V3 decision engine should:

- catch JSON parsing failures;
- identify whether the primary or secondary source failed;
- write a controlled failure log;
- explicitly state that no decision or remediation occurred;
- exit with a non-zero status.

The system must continue to fail closed.

---

# Evidence

- `simulation/v3-f02-corrupted-input.json`
- `tests/v3-decision-engine-f02-test.py`
- terminal-observed `JSONDecodeError`
- exit code `1`
- decision output absent
- audit log absent

---

# Disposition

Preserve this result before applying the corrective observability control.
