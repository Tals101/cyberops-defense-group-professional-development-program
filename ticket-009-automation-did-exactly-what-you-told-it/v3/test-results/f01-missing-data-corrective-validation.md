# Ticket #009 — F01 Missing Identity Data Corrective Validation

## Test

F01 — Missing Identity Data

## Prior Result

The original V3 implementation failed this test.

When `owner` and `business_purpose` were removed from `nora.hayes`, the record still claimed:

`evidence_completeness = complete`

V3 incorrectly produced:

- decision_confidence: HIGH
- evidence_trust: TRUSTED
- recommendation: DISABLE
- authority: AUTO_REMEDIATE

That result was preserved separately as a failed test.

---

# Corrective Control

The V3 decision engine was modified to independently validate required primary identity fields.

The engine now directly checks:

- identity_type;
- workforce_status;
- owner;
- business_purpose;
- lifecycle_state;
- data_freshness;
- evidence_completeness.

Values that are:

- missing;
- blank;
- unknown;
- null;

are treated as missing evidence.

The source-provided `evidence_completeness` label is no longer trusted by itself.

---

# Retest

The same F01 test dataset was reused.

Identity:

`nora.hayes`

Injected missing fields:

- owner
- business_purpose

Source-provided completeness value remained:

`complete`

---

# Corrected Result

V3 produced:

- decision_confidence: `INSUFFICIENT`
- evidence_trust: `INCOMPLETE`
- evidence_trust_reason: `Missing required primary fields: owner, business_purpose.`
- recommendation: `DISABLE`
- authority: `REQUIRE_APPROVAL`
- approval_required: `YES`
- actual_action: `NO_ACTION_DRY_RUN`

---

# Fail Open or Fail Closed?

**FAIL CLOSED for unattended destructive authority.**

The policy recommendation can still identify the account as remediation-eligible, but incomplete evidence prevents automatic destructive authority.

---

# Was This the Correct Behavior?

**Yes.**

The system does not erase the security recommendation.

Instead, it correctly reduces the authority that may be exercised automatically.

---

# Was the Environment Left in a Known State?

**Yes.**

No state-changing action occurred.

---

# Did the Operator Know Something Failed?

**Yes.**

The decision record explicitly identifies:

`Missing required primary fields: owner, business_purpose.`

This gives an operator actionable evidence rather than a generic failure.

---

# Can Execution Safely Resume?

Yes, after the missing evidence is corrected or supplied and the identity is reevaluated.

The prior decision must not simply be reused.

---

# Could Repeated Execution Cause Additional Damage?

No destructive action is authorized while the evidence remains incomplete.

Repeated dry-run evaluation produces the same bounded result.

---

# Result

**PASS AFTER CORRECTIVE CONTROL**

The F01 failure revealed a real unsafe assumption.

The corrected V3 implementation now validates actual required evidence rather than trusting source-provided completeness metadata.

---

# Evidence

- `tests/f01-missing-data-finding.md`
- `simulation/v3-f01-missing-data.json`
- `tests/v3-decision-engine-f01-fixed-test.py`
- `evidence/v3-f01-fixed-decisions.csv`
- `evidence/v3-f01-fixed.log`
- `automation/v3-decision-engine.py`
