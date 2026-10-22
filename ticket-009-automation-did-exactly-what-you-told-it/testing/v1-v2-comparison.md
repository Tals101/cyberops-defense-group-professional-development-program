# Ticket #009 — V1 vs. V2 Automation Comparison

## Purpose

This comparison evaluates V1 and V2 using the same baseline identity environment.

The conclusion is not based merely on V2 performing fewer actions.

V2 is evaluated on:

- decision correctness;
- explainability;
- authority boundaries;
- protection of high-impact identities;
- recoverability;
- blast-radius control;
- safe failure behavior.

---

# Metric Definitions

## Correct Remediation

An actual state-changing remediation supported by the full baseline identity context.

## Incorrect Remediation

An actual state-changing remediation that should not have occurred when the available identity context is considered.

## Actions Requiring Approval

Actions staged rather than executed because the identity or potential consequence requires human authorization.

## Protected High-Impact Identity

A privileged or service identity explicitly prevented from unattended state-changing remediation by the authority model.

## Unexplained Decision

A decision record that does not provide a complete per-identity evidence and rationale chain sufficient for an auditor to understand:

Identity → Evidence → Decision → Authority → Action → Result

## Recoverable Change

An executed state change backed by an engineered recovery mechanism, including a pre-change snapshot and tested rollback path.

## Baseline False Negative

An identity requiring remediation that the decision logic failed to identify.

---

# Automation Comparison

| Metric | V1 | V2 |
|---|---:|---:|
| Correct Remediations | 2 | 2 |
| Incorrect Remediations | 3 | 0 |
| Actions Requiring Approval | 0 | 2 staged actions |
| Protected High-Impact Identities | 0 explicitly protected | 3 |
| Unexplained Decisions | 10 | 0 |
| Recoverable Changes | 0 with engineered recovery | 2 of 2 executed changes |
| Failed Rollbacks | N/A — rollback absent | 0 |
| Maximum Actions Per Run | Unbounded | 2 |
| Baseline False Negatives | 1 | 0 |

### V2 Authority Note

Three identities were classified within the `REQUIRE_APPROVAL` authority category:

- `admin.ops`
- `svc_finance_batch`
- `svc_records_archive`

Two of those identities produced staged review actions:

- `admin.ops`
- `svc_records_archive`

`svc_finance_batch` received `KEEP_ENABLED`, so no state-changing action required approval.

---

# Correct Remediations

## V1

V1 executed five disable actions.

Correct state-changing remediations:

1. `nora.hayes`
2. `contractor.mills`

Total:

**2**

## V2

V2 executed two disable actions during the baseline enforcement run:

1. `nora.hayes`
2. `kevin.brooks`

Both were supported by the available identity context.

Total:

**2**

The third supported automatic-remediation candidate, `contractor.mills`, was staged because the configured two-action run limit had been reached.

Therefore, V2 did not improve safety merely by executing fewer changes. It correctly identified more relevant lifecycle context while respecting its blast-radius limit.

---

# Incorrect Remediations

## V1

V1 incorrectly disabled:

1. `svc_finance_batch`
2. `svc_records_archive`
3. `analytics.temp`

### svc_finance_batch

The account was an active service identity with:

- current non-interactive authentication;
- known ownership;
- active lifecycle;
- documented business purpose;
- Finance service dependencies.

Interactive inactivity alone was insufficient justification for automatic disablement.

### svc_records_archive

The account was a service identity with ownership and a service dependency.

Its condition required additional review rather than unattended disablement.

### analytics.temp

The account had:

- unknown identity type;
- conflicting evidence;
- uncertain context.

The uncertainty should have reduced automation authority rather than producing a state change.

Total incorrect V1 remediations:

**3**

## V2

V2 performed no unsupported automatic state-changing remediation in the baseline run.

Total:

**0**

---

# Actions Requiring Approval

## V1

V1 had no approval boundary between classification and enforcement.

Total:

**0**

## V2

Two review actions were explicitly staged rather than executed:

- `admin.ops`
- `svc_records_archive`

Both returned:

`APPROVAL_REQUIRED`

In addition, `svc_finance_batch` belonged to the `REQUIRE_APPROVAL` authority class, although its recommendation was `KEEP_ENABLED` and therefore no approval-triggering state change was proposed.

---

# Protected High-Impact Identities

For this comparison, high-impact identities are privileged or service identities in the baseline:

1. `admin.ops`
2. `svc_finance_batch`
3. `svc_records_archive`

## V1

V1 did not contain an explicit high-impact identity protection control.

`admin.ops` happened not to meet the stale-login rule, but it was not protected by an authority boundary.

Both service identities were automatically disabled.

Explicitly protected:

**0**

## V2

All three high-impact identities were prevented from unattended state-changing remediation.

Protected:

**3**

---

# Explainability

## V1

The V1 decision file recorded:

- identity;
- identity type;
- interactive-login age;
- decision;
- action result.

It did not provide a complete per-identity rationale or evidence chain explaining why the action was safe.

Under the structured audit definition used for this comparison:

**10 V1 decisions lacked complete decision-chain evidence.**

## V2

The V2 Automation Decision Record contains:

- identity context;
- activity evidence;
- privilege;
- service dependencies;
- lifecycle;
- approval state;
- evidence quality;
- confidence;
- decision;
- decision reason;
- authority;
- proposed action;
- actual action;
- result;
- recovery method.

Unexplained decisions:

**0**

---

# Recoverability

## V1

V1 did not create an engineered pre-change snapshot or provide a tested rollback workflow before state changes.

Recoverable changes under the engineered-recovery definition:

**0**

## V2

Both executed baseline changes were protected by:

- pre-change snapshot;
- rollback tooling;
- post-recovery validation.

Recoverable executed changes:

**2 of 2**

Rollback testing restored the known-good state and Finance health validation returned:

`APPLICATION_STATUS=HEALTHY`

Failed rollback tests:

**0**

---

# Blast-Radius Control

## V1

V1 had no maximum number of actions per execution.

Maximum actions per run:

**Unbounded within the writable input scope**

## V2

Configured maximum:

**2 state-changing actions per run**

Testing also discovered that a per-run limit alone did not prevent cumulative changes across repeated runs.

That weakness was corrected with the persistent deferred-action ledger.

An identity deferred because the run limit was reached now requires explicit review before a later run may automatically act on it.

---

# Baseline False Negatives

## V1

`kevin.brooks` represented a terminated workforce identity.

V1 left the account enabled because its interactive-login age did not exceed the 90-day threshold.

Baseline false negatives:

**1**

## V2

V2 used lifecycle context and correctly recommended:

`DISABLE`

The remediation executed successfully.

Baseline false negatives:

**0**

---

# Why V2 Is Safer

V2 is not considered safer because it performed only two state changes while V1 performed five.

The safety improvement comes from the engineering controls surrounding the decisions.

V2 demonstrated:

- richer identity context;
- explicit confidence;
- separation of detection from authorization;
- approval boundaries;
- protection of service and privileged identities;
- fail-safe treatment of ambiguity;
- fail-safe treatment of incomplete evidence;
- rejection of malformed input;
- explicit handling of unknown identity types;
- bounded actions per run;
- persistent cross-run deferral;
- pre-change snapshots;
- tested rollback;
- post-change health validation;
- audit logging requirements;
- emergency-stop capability;
- structured decision evidence.

V1 could execute a technically correct rule while still producing an unsafe operational result.

V2 reduces that risk by making automation authority proportional to decision confidence and potential impact.

---

# Conclusion

The same baseline environment demonstrated materially different safety characteristics.

V1 produced:

- unsafe service-account remediation;
- remediation of an ambiguous unknown identity;
- a terminated-user false negative;
- no approval boundary;
- no engineered rollback;
- unbounded per-run authority.

V2 produced:

- supported workforce remediation;
- protection of high-impact identities;
- explicit review boundaries;
- no unsupported baseline state changes;
- complete decision evidence;
- tested recovery;
- bounded and persistent blast-radius controls.

**V2 is safer because its decisions are more contextual, explainable, bounded, and recoverable—not simply because it performs fewer actions.**
