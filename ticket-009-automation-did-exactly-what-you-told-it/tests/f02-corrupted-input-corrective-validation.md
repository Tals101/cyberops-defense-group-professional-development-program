# Ticket #009 — F02 Corrupted Input Corrective Validation

## Test

F02 — Corrupted Input

## Prior Result

The original V3 corrupted-input test failed safely but did not create controlled audit evidence.

Observed prior behavior:

- JSON parsing failed;
- exit code was 1;
- no decision file was created;
- no remediation occurred;
- no structured failure log was created.

That result was preserved separately.

---

# Corrective Control

The canonical V3 decision engine was modified to use controlled JSON source loading.

The engine now catches:

- JSON parsing failures;
- source read failures.

When input cannot be safely read, it:

- fails closed;
- identifies the failed source;
- records the error type;
- records the error message;
- records zero decision records;
- records that no remediation occurred;
- tells the operator whether retry is safe after correction;
- exits with a non-zero status.

---

# Retest

Test input:

`simulation/v3-f02-corrupted-input.json`

The file contained deliberately invalid JSON.

---

# Corrected Result

Console result:

`FAIL: PRIMARY_IDENTITY_SOURCE input could not be read or parsed. No decisions or remediation occurred.`

Exit code:

`1`

Decision output created:

`False`

Failure log created:

`True`

The failure log recorded:

- `status=FAIL_CLOSED`
- `failure_type=INPUT_READ_OR_PARSE_FAILURE`
- `source=PRIMARY_IDENTITY_SOURCE`
- `error_type=JSONDecodeError`
- `decision_records=0`
- `remediation_performed=False`
- `safe_to_retry_after_input_correction=True`

---

# Fail Open or Fail Closed?

**FAIL CLOSED**

Malformed identity data cannot reach the decision or remediation path.

---

# Was This the Correct Behavior?

**Yes.**

The system stops before any remediation decision is generated and produces durable operator evidence explaining why processing stopped.

---

# Was the Environment Left in a Known State?

**Yes.**

No decision record was created.

No remediation occurred.

The canonical identity dataset remained unchanged.

---

# Did the Operator Know Something Failed?

**Yes.**

The operator receives both:

- a concise terminal message; and
- a structured failure log.

The failed input source and failure type are explicit.

---

# Can Execution Safely Resume?

Yes, after:

1. correcting or restoring the malformed input;
2. validating the repaired source;
3. rerunning the decision engine from the beginning.

No rollback is required because no remediation occurred.

---

# Could Repeated Execution Cause Additional Damage?

No destructive change occurs while the input remains malformed.

Repeated execution would continue to fail closed.

Operational alerting should still prevent uncontrolled retry loops.

---

# Result

**PASS AFTER CORRECTIVE CONTROL**

V3 now combines safe failure behavior with usable operator evidence.

---

# Evidence

- `tests/f02-corrupted-input-finding.md`
- `simulation/v3-f02-corrupted-input.json`
- `tests/v3-decision-engine-f02-fixed-test.py`
- `evidence/v3-f02-fixed.log`
- `automation/v3-decision-engine.py`
