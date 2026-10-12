# Ticket #009 — T12 Repeated Execution Corrective Validation

## Original Finding

The first T12 test identified a cross-run blast-radius weakness.

V2 correctly avoided repeating changes to identities already disabled, but the per-run action counter reset on the next execution.

As a result, `contractor.mills`, which had been deferred when the first run reached its two-action limit, was automatically disabled during the second run.

Original result:

**FAIL — DESIGN GAP IDENTIFIED**

---

# Corrective Control

V2 was updated with a persistent deferred-action ledger.

When an identity is prevented from automatic remediation because the configured action limit has been reached, V2 now records:

- username;
- deferral timestamp;
- reason;
- authority classification;
- recommendation;
- requirement for explicit release.

A deferred identity cannot automatically become eligible merely because another scheduled execution begins.

---

# Corrective Test — First Run

The corrected test began from the original identity state.

Observed:

- Changes made: 2
- Maximum allowed: 2
- Deferred identities: 1

Automatic changes:

- nora.hayes — DISABLE
- kevin.brooks — DISABLE

Deferred:

- contractor.mills — RUN_LIMIT_REACHED

The deferred ledger recorded:

- username: contractor.mills
- reason: RUN_LIMIT_REACHED
- release_required: true

---

# Corrective Test — Second Run

The first run's resulting identity state was used as input for the second run.

Observed:

- Changes made: 0
- Maximum allowed: 2
- Deferred identities: 1

Results:

- nora.hayes — NO_ACTION — ALREADY_DISABLED
- kevin.brooks — NO_ACTION — ALREADY_DISABLED
- contractor.mills — STAGE_ONLY — DEFERRED_REVIEW_REQUIRED

No additional identity was automatically disabled.

---

# Persistent Deferred State

The second run loaded the existing deferred-action ledger.

The ledger continued to contain:

contractor.mills

with:

release_required=true

This demonstrates that the safety boundary persists across executions.

---

# Engineering Conclusion

The corrected V2 implementation now provides two distinct protections:

1. **Per-run limit** — prevents more than the configured number of state-changing actions in one execution.
2. **Cross-run deferred-action control** — prevents identities stopped by the safety limit from automatically becoming new changes during the next execution.

A deferred identity must be explicitly reviewed or released before later enforcement.

This converts the action limit from a purely execution-level safeguard into a broader remediation-campaign boundary.

---

# T12 Final Result

**PASS AFTER CORRECTIVE CONTROL**

The initial failure was preserved as evidence.

The corrected implementation demonstrates:

- individual-action idempotency;
- no duplicate remediation;
- persistent deferred state;
- zero additional automatic changes during the second run;
- explicit review requirement before deferred remediation may proceed.
