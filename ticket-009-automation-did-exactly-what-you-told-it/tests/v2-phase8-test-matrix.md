# Ticket #009 — Phase 8 V2 Test Matrix

## Purpose

V2 was tested against the same baseline identity environment used for the incident reconstruction.

The baseline identities were not altered to make V2 produce more favorable results.

Each test records:

- Expected Behavior
- Actual Behavior
- PASS / FAIL
- Security Significance
- Recovery Method
- Evidence

---

# Test 1 — Clearly Terminated Employee

## Identity

`kevin.brooks`

## Expected Behavior

The terminated workforce identity should be identified as requiring remediation.

Because the evidence is complete and current and the identity is a standard workforce account, V2 should classify it as eligible for automatic remediation.

## Actual Behavior

- Confidence: HIGH
- Authority: AUTO_REMEDIATE
- Recommendation: DISABLE
- Actual action: DISABLE
- Result: SUCCESS

## PASS / FAIL

**PASS**

## Security Significance

V2 identified a terminated identity that V1 failed to disable.

This demonstrates that V2 does not depend solely on interactive-login age and can use lifecycle context to detect risk.

## Recovery Method

Restore the account's enabled state from the pre-change snapshot if the remediation is later determined to be incorrect.

Validate downstream access after restoration.

## Evidence

- `simulation/identities-original.json`
- `evidence/v2-dry-run-decisions.csv`
- `evidence/v2-enforcement-results.csv`
- `evidence/v2-prechange-snapshot.json`

---

# Test 2 — Normal Active Employee

## Identity

`emma.reed`

## Expected Behavior

A normal active employee with recent activity and no remediation indicators should remain enabled.

## Actual Behavior

- Confidence: HIGH
- Authority: AUTO_REMEDIATE
- Recommendation: NO_ACTION
- Actual action: NO_ACTION
- Result: RECOMMENDATION_NO_CHANGE

## PASS / FAIL

**PASS**

## Security Significance

The test demonstrates that V2 does not create unnecessary changes when the identity evidence does not support remediation.

## Recovery Method

No recovery required because no state change occurred.

## Evidence

- `simulation/identities-original.json`
- `evidence/v2-dry-run-decisions.csv`
- `evidence/v2-enforcement-results.csv`

---

# Test 3 — Privileged Account

## Identity

`admin.ops`

## Expected Behavior

A privileged account must not be automatically disabled solely because automation identifies a concern.

The identity should be staged for human review.

## Actual Behavior

- Confidence: HIGH
- Authority: REQUIRE_APPROVAL
- Recommendation: REVIEW
- Actual action: STAGE_ONLY
- Result: APPROVAL_REQUIRED

## PASS / FAIL

**PASS**

## Security Significance

A mistaken unattended action against a privileged identity can create disproportionate operational or security impact.

V2 limits automation authority for this class of identity.

## Recovery Method

No rollback required because no identity state change occurred.

## Evidence

- `simulation/identities-original.json`
- `evidence/v2-dry-run-decisions.csv`
- `evidence/v2-enforcement-results.csv`

---

# Test 4 — Legitimate Service Account

## Identity

`svc_finance_batch`

## Expected Behavior

The account should not be disabled merely because interactive-login activity is stale.

Current non-interactive authentication, known ownership, active lifecycle, business purpose, and Finance dependencies should be considered.

## Actual Behavior

- Interactive-login age: 240 days
- Non-interactive authentication age: 0 days
- Confidence: HIGH
- Authority: REQUIRE_APPROVAL
- Recommendation: KEEP_ENABLED
- Actual action: NO_ACTION
- Result: RECOMMENDATION_NO_CHANGE

Finance validation remained:

`APPLICATION_STATUS=HEALTHY`

## PASS / FAIL

**PASS**

## Security Significance

This directly addresses the failure demonstrated by V1.

V2 distinguishes interactive inactivity from actual service inactivity and considers dependency context before remediation.

## Recovery Method

No rollback required because no identity state change occurred.

If an incorrect change had occurred, restore from the pre-change snapshot and validate Finance dependencies.

## Evidence

- `simulation/identities-original.json`
- `evidence/v2-dry-run-decisions.csv`
- `evidence/v2-enforcement-results.csv`
- `evidence/v2-postchange-health.log`
- `evidence/v2-automation-decision-record.csv`

---

# Test 5 — Stale but Legitimate Account

## Identity

`svc_records_archive`

## Expected Behavior

A stale service identity with a legitimate owner and business dependency should not be automatically disabled when its context requires additional review.

## Actual Behavior

- Confidence: HIGH
- Authority: REQUIRE_APPROVAL
- Recommendation: REVIEW
- Actual action: STAGE_ONLY
- Result: APPROVAL_REQUIRED

## PASS / FAIL

**PASS**

## Security Significance

Staleness alone is not treated as sufficient authorization for a potentially disruptive service-account change.

V2 distinguishes detection from permission to remediate.

## Recovery Method

No rollback required because the identity was staged only.

## Evidence

- `simulation/identities-original.json`
- `evidence/v2-dry-run-decisions.csv`
- `evidence/v2-enforcement-results.csv`

---

# Test 6 — Ambiguous Account

## Identity

`analytics.temp`

## Expected Behavior

Conflicting or ambiguous evidence should reduce confidence and prevent unattended remediation.

## Actual Behavior

- Evidence state: conflicting
- Confidence: LOW
- Authority: DO_NOT_AUTOMATE
- Recommendation: REVIEW
- Actual action: NO_ACTION
- Result: AUTOMATION_PROHIBITED

## PASS / FAIL

**PASS**

## Security Significance

V2 fails safely when evidence does not support a reliable remediation decision.

Ambiguity reduces automation authority rather than increasing the chance of an incorrect change.

## Recovery Method

No rollback required because no state change occurred.

The identity requires investigation and evidence reconciliation.

## Evidence

- `simulation/identities-original.json`
- `evidence/v2-dry-run-decisions.csv`
- `evidence/v2-enforcement-results.csv`

---

# Test 7 — Incomplete Identity Record

## Identity

`ingest.bridge`

## Expected Behavior

An identity with incomplete evidence must not be automatically remediated.

## Actual Behavior

- Evidence completeness: incomplete
- Data freshness: stale
- Confidence: INSUFFICIENT
- Authority: DO_NOT_AUTOMATE
- Recommendation: REVIEW
- Actual action: NO_ACTION
- Result: AUTOMATION_PROHIBITED

## PASS / FAIL

**PASS**

## Security Significance

Missing evidence cannot be interpreted as evidence that an identity is safe to modify.

V2 defaults toward preserving production state when critical context is unavailable.

## Recovery Method

No rollback required because no state change occurred.

Required identity evidence must be collected before reevaluation.

## Evidence

- `simulation/identities-original.json`
- `evidence/v2-dry-run-decisions.csv`
- `evidence/v2-enforcement-results.csv`

---

# Test 8 — Malformed Input

## Input

`simulation/v2-malformed-input.json`

## Expected Behavior

Malformed input must prevent decision processing.

No remediation decisions or downstream actions should be generated from structurally invalid data.

## Actual Behavior

The V2 decision engine terminated while parsing the malformed JSON.

Observed exception:

`json.decoder.JSONDecodeError`

Observed:

- Exit code: 1
- Decision output created: False
- Test log created: False

No enforcement path was reached.

## PASS / FAIL

**PASS**

## Security Significance

Corrupt or malformed identity data does not silently produce remediation decisions.

The system fails before state-changing enforcement can occur.

## Recovery Method

Correct or restore the input dataset and rerun validation before allowing remediation.

No identity rollback is required because no decision or state change occurred.

## Evidence

- `simulation/v2-malformed-input.json`
- `tests/v2-decision-engine-malformed-input-test.py`
- terminal test output

## Operational Improvement

The current lab implementation returns the native JSON parsing exception.

A production implementation should catch malformed-input exceptions and produce a controlled audit event such as:

`FAIL: identity input could not be parsed.`

It must still fail closed and produce no remediation decisions.

---

# Test 9 — Unknown Identity Type

## Identity

`analytics.temp` and `ingest.bridge`

## Expected Behavior

An identity type not recognized by the V2 authority model must not receive unattended remediation authority.

## Actual Behavior

Both identities were classified:

`DO_NOT_AUTOMATE`

Observed actions:

`NO_ACTION`

Observed result:

`AUTOMATION_PROHIBITED`

## PASS / FAIL

**PASS**

## Security Significance

New, unexpected, or incorrectly classified identity types cannot inherit automatic remediation authority by default.

This prevents silent expansion of automation authority when the identity taxonomy changes.

## Recovery Method

No rollback required because no state change occurred.

The identity type must be investigated, classified, and explicitly incorporated into the authority model before automation may act.

## Evidence

- `simulation/identities-original.json`
- `evidence/v2-dry-run-decisions.csv`
- `evidence/v2-enforcement-results.csv`

---

# Phase 8 Minimum-Test Summary

| Test | Result |
|---|---|
| Clearly terminated employee | PASS |
| Normal active employee | PASS |
| Privileged account | PASS |
| Legitimate service account | PASS |
| Stale but legitimate account | PASS |
| Ambiguous account | PASS |
| Incomplete identity record | PASS |
| Malformed input | PASS |
| Unknown identity type | PASS |

## Conclusion

All minimum Phase 8 identity and input cases were exercised.

V2 demonstrated that it can:

- remediate a clearly supported workforce case;
- preserve normal active identities;
- restrict authority for privileged identities;
- preserve legitimate service identities;
- stage stale high-impact identities for review;
- fail safely when evidence is ambiguous or incomplete;
- reject malformed input before generating remediation decisions;
- prohibit automation for unknown identity types.

The test results demonstrate safer behavior through evidence quality, explainability, bounded authority, and recoverability rather than merely through performing fewer actions.
