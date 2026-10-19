# Ticket #009 — Identity Remediation Incident Closure Report

## Executive Summary

Ticket #009 investigated an identity-remediation incident in which an automated remediation job disabled an identity supporting a Finance application.

The investigation determined that the primary failure was not that the original automation failed to execute its programmed rule. The automation executed the rule as designed.

The failure was that the rule used insufficient identity context while possessing direct authority to make a high-impact production state change.

V1 treated stale interactive-login activity as sufficient evidence for disabling an enabled identity. That assumption was unsafe for service identities whose legitimate activity may be primarily non-interactive.

The simulated reconstruction demonstrated the failure against `svc_finance_batch`, an active Finance service account with current non-interactive authentication and known application dependencies.

V2 was redesigned to separate:

- detection;
- evidence collection;
- confidence assessment;
- authority classification;
- recommendation;
- approval;
- enforcement;
- validation;
- rollback.

The redesigned system was then tested through fifteen safety scenarios.

All planned V2 safety tests passed, including one test that initially exposed a cross-run remediation weakness. That weakness was preserved as evidence, corrected with a persistent deferred-action ledger, and successfully retested.

---

# Incident Timeline

Known incident milestones supplied for the exercise:

- 08:52 — identity-remediation job executed.
- 08:57 — Finance Operations began experiencing failures.
- 09:07 — SOC assumed incident ownership.
- IAM reported that a service account had been disabled during remediation.

The supplied incident timeline did not establish the exact pre-08:52 identity state, full production blast radius, or all production remediation actions.

Those items were treated as unknown rather than assumed.

---

# Immediate Response Priorities

The response strategy prioritized:

1. restore affected business service;
2. suspend unsafe automated writes;
3. preserve evidence;
4. determine what identities could have been affected;
5. reconstruct the decision logic;
6. determine why the automation possessed sufficient authority to execute the change;
7. redesign the control boundary;
8. prove safer failure and recovery behavior before re-enablement.

---

# V1 Reconstruction

V1 used a simple rule:

If an identity was enabled and its interactive-login age was at least 90 days, disable it.

V1 did not adequately consider:

- identity type;
- non-interactive authentication;
- service dependencies;
- business purpose;
- owner;
- privilege;
- lifecycle state;
- approval status;
- evidence completeness;
- data freshness;
- remediation confidence.

The simulated V1 run disabled five identities.

One of those identities was:

`svc_finance_batch`

Relevant context showed that the account:

- was a service account;
- had a known Finance owner;
- had active business purpose;
- had current non-interactive authentication;
- supported Finance LedgerBridge;
- supported Finance Settlement Processor;
- remained in an active lifecycle state.

Despite those facts, V1 disabled it because its interactive-login age exceeded the configured threshold.

The simulated Finance health check then returned:

`APPLICATION_STATUS=FAILED`

---

# Root Cause

## Technical Root Cause

V1 generalized interactive-login inactivity into overall identity inactivity.

That assumption was invalid for identities that authenticate through non-interactive processes.

## Control Root Cause

The same automation path performed:

- detection;
- decision;
- authorization;
- remediation.

There was no independent authority boundary proportional to the confidence or impact of the decision.

## Recovery Root Cause

V1 did not include an engineered pre-change snapshot, validation gate, or controlled rollback path.

## Process Root Cause

The original workflow lacked explicit requirements for:

- identity context;
- evidence quality;
- approval boundaries;
- dry-run validation;
- blast-radius limits;
- dependency awareness;
- privileged identity handling;
- failure-safe behavior.

---

# Blast Radius

The effective V1 blast radius was broader than the Finance service account alone.

Any enabled identity inside the automation's writable scope that met the simplistic inactivity rule could potentially be disabled.

The reconstruction demonstrated both types of decision failure:

## False Positive

`svc_finance_batch`

The service identity was active in a legitimate non-interactive role but was disabled.

## False Negative

`kevin.brooks`

The identity represented a terminated workforce user but remained enabled because the interactive-login age alone did not meet the V1 threshold.

Therefore, V1 was capable of both:

- disabling identities that should remain enabled; and
- retaining identities that should be disabled.

---

# Automation Authority Model

V2 introduced three authority categories.

## AUTO-REMEDIATE

Permitted only when evidence is sufficiently complete and current, identity context is understood, impact is bounded, and the decision meets the defined low-risk criteria.

## REQUIRE APPROVAL

Used when the identity or action has increased impact or ambiguity, including:

- service identities;
- privileged identities;
- known dependencies;
- conflicting evidence;
- moderate or high operational impact.

## DO NOT AUTOMATE

Used when unattended remediation is unsafe, including:

- unknown identity type;
- critically incomplete evidence;
- untrusted evidence;
- uncertain rollback;
- recovery identities;
- break-glass identities;
- core IAM identities.

The core principle is:

**Detection is not authorization.**

---

# V2 Safety Controls

V2 incorporated controls for:

- dry-run execution;
- evidence completeness;
- identity-type-aware decisions;
- unknown-identity fail-safe behavior;
- dependency awareness;
- privileged identity protection;
- confidence classification;
- approval boundaries;
- maximum state changes per run;
- pre-change snapshot;
- rollback;
- post-change health validation;
- audit logging;
- idempotency;
- emergency stop;
- persistent deferred actions across repeated runs.

---

# V2 Dry-Run Validation

The original identity dataset was hashed before and after dry-run execution.

SHA256 before:

`A90C324B953030B2C933CACC9FC104A2F5A29A15F6B02E1AB1420091640182D3`

SHA256 after:

`A90C324B953030B2C933CACC9FC104A2F5A29A15F6B02E1AB1420091640182D3`

The hashes matched.

This proved that decision generation could occur without modifying identity state.

---

# V2 Enforcement Validation

The configured maximum was:

`2 state-changing actions per run`

Observed automatic changes:

- nora.hayes — disabled;
- kevin.brooks — disabled.

A third eligible candidate:

`contractor.mills`

was initially staged because the run limit had been reached.

Service and privileged identities requiring additional authority were not automatically remediated.

Unknown identities were not automatically remediated.

Finance remained healthy after V2 enforcement:

`APPLICATION_STATUS=HEALTHY`

---

# Rollback Validation

A deliberate bad state was created in an isolated rollback test by disabling the Finance dependency identity.

Rollback restored the pre-change snapshot.

The restored state matched the original snapshot by SHA256.

Post-rollback Finance validation returned:

`APPLICATION_STATUS=HEALTHY`

This demonstrated that the known-good state could be restored exactly in the simulated environment.

---

# T12 Cross-Run Safety Finding

Repeated execution testing identified an additional design weakness.

The original V2 run limit applied only to a single execution.

On a second run:

- nora.hayes was recognized as already disabled;
- kevin.brooks was recognized as already disabled;
- contractor.mills was automatically disabled.

This showed that repeated executions could gradually exceed the intended remediation campaign boundary.

The failure was preserved in Git before correction.

---

# T12 Corrective Control

V2 was updated with a persistent deferred-action ledger.

An identity deferred because the safety limit was reached now remains deferred across subsequent runs.

Explicit review or release is required before later enforcement.

After the correction, the second execution produced:

- nora.hayes — ALREADY_DISABLED;
- kevin.brooks — ALREADY_DISABLED;
- contractor.mills — DEFERRED_REVIEW_REQUIRED.

Changes made during the second run:

`0`

T12 therefore passed after corrective control.

---

# Audit Logging Fail-Safe

The audit logging path was deliberately made unavailable in an isolated test.

Execution failed with a non-zero exit code before state-changing enforcement occurred.

Identity-state SHA256 before and after remained identical.

No enforcement output state was generated.

Result:

**PASS**

The current implementation relies on the underlying file-open failure. A production implementation should convert that failure into a controlled operational error while preserving the same fail-safe behavior.

---

# Emergency Stop Validation

The emergency-stop mechanism was tested in two conditions.

## Pre-Run

With the emergency-stop flag active before execution:

- enforcement refused to begin;
- exit code was non-zero;
- identity state remained unchanged;
- no output state was produced.

## Mid-Run

The stop was activated immediately after the first successful automatic state change.

Observed:

- nora.hayes — DISABLE — SUCCESS;
- kevin.brooks — STAGE_ONLY — EMERGENCY_STOP_ACTIVE;
- contractor.mills — STAGE_ONLY — EMERGENCY_STOP_ACTIVE.

Changes made:

`1`

The remaining automatic changes were prevented.

Result:

**PASS**

---

# Safety Test Summary

The V2 safety test matrix contained fifteen tests.

Final status:

- T01 — PASS
- T02 — PASS
- T03 — PASS
- T04 — PASS
- T05 — PASS
- T06 — PASS
- T07 — PASS
- T08 — PASS
- T09 — PASS
- T10 — PASS
- T11 — PASS
- T12 — PASS AFTER CORRECTIVE CONTROL
- T13 — PASS
- T14 — PASS
- T15 — PASS

No planned safety tests remain pending.

---

# IAM Recommendation

The incident should not be resolved by excluding every service account from remediation.

A blanket exemption would remove one failure path while creating a long-term lifecycle and security gap.

Service identities should instead follow a context-aware decision path using:

- known ownership;
- business purpose;
- non-interactive authentication;
- service dependencies;
- lifecycle state;
- privilege;
- evidence quality;
- approval proportional to operational impact.

V1 unattended enforcement should remain retired.

---

# Re-Enable Criteria

Production-style remediation should not be re-enabled unless the implementation can demonstrate:

- reliable identity classification;
- current and complete evidence;
- bounded authority;
- approval for high-impact identities;
- working audit logging;
- pre-change recovery state;
- post-change service validation;
- tested rollback;
- emergency stop;
- cross-run deferred-action protection;
- documented ownership and escalation paths.

---

# Residual Limitations

The Ticket #009 environment is a controlled simulation.

The tests prove the behavior of the local implementation and synthetic identity dataset.

They do not prove behavior against a specific production IAM platform.

In addition:

- rollback is currently implemented as a controlled recovery step rather than a fully orchestrated enforcement-to-validation-to-rollback transaction;
- audit logging failure currently produces a native Python exception rather than a polished operational error;
- explicit deferred-action release workflow remains a future production-control implementation;
- production IAM permissions, transaction semantics, race conditions, and external dependencies would require platform-specific validation.

These limitations do not invalidate the demonstrated safety improvements but must be addressed before production deployment.

---

# Final Disposition

**V1: UNSAFE — RETIRED**

**V2 simulated design: SAFER — VALIDATED FOR THE TICKET #009 LAB**

V2 demonstrated materially improved protection through:

- contextual identity decisions;
- bounded automation authority;
- approval gates;
- fail-safe defaults;
- blast-radius controls;
- persistent cross-run deferral;
- validation;
- rollback;
- audit fail-safe behavior;
- emergency stop.

The original incident was therefore treated as an automation-governance and engineering-control failure, not merely an incorrect account classification.

Ticket #009 simulation and safety validation are complete.

---

# Final Engineering Closure Addendum — October 18, 2026

## Scope of This Addendum

The preceding report documents the original incident investigation and the V1/V2 engineering work.

The statement that the simulation and safety validation were complete referred to that earlier V2 scope.

Subsequent engineering work extended Ticket #009 to V3 evidence-trust validation, failure injection, adversarial testing, operations planning, and production readiness assessment.

This addendum records those later results without replacing the original evidence.

## V3 Evidence-Trust Engineering

V3 added secondary-source corroboration, explicit evidence-trust classifications, source-integrity verification, and independent observation-timestamp freshness checks.

The canonical V3 decision engine remains dry-run only.

Its AUTO_REMEDIATE classification does not grant authorization to modify production accounts.

The synthetic payroll.emergency scenario demonstrated why decision confidence and evidence trust must be evaluated separately.

Conflicting business-dependency evidence resulted in REQUIRE_APPROVAL rather than unattended remediation.

## Failure-Injection Results — F01 Through F10

Ten failure-injection scenarios were documented.

F01–F03 exposed weaknesses involving missing identity attributes, corrupted input handling, and unavailable audit logging. Corrective implementations were tested.

F04–F10 evaluated duplicate execution, interruption, remediation failure, rollback failure, approval timeout, unsupported identity types, and missing secondary corroboration.

The results demonstrate laboratory control behavior, not integrated production readiness.

Supporting record:

tests/v3-failure-injection-results.md

## Adversarial Results — A01 Through A03

A01 demonstrated that poisoned secondary evidence could initially produce TRUSTED evidence and AUTO_REMEDIATE authority.

Correction: validate source integrity against a separately protected SHA256 baseline before decision generation.

A02 demonstrated that an attacker-controlled freshness label could make old evidence appear current.

Correction: independently evaluate observation timestamps against a 24-hour freshness threshold.

A03 demonstrated approval forgery and reuse of an unbound authorization reference in isolated synthetic enforcement tests.

Correction: an isolated approval-verification workflow using HMAC-SHA256 signatures, identity and action binding, expiration, and one-time-use consumption.

Corrective tests passed for their documented scenarios.

The A03 approval controls remain separate from canonical V3 enforcement and are not production-ready.

Supporting record:

tests/v3-adversarial-test-results.md

## Current Evidence Freshness

The canonical V3 secondary observations are dated October 16, 2026.

As of October 18, they exceed the 24-hour freshness threshold.

Historical TRUSTED or AUTO_REMEDIATE outcomes must not be interpreted as currently valid authorization.

Evidence must be refreshed from authoritative sources. Timestamps must not be artificially advanced.

## Final Production Readiness Assessment

The following production capabilities remain incomplete or unvalidated:

- Integrated authorization and destructive enforcement
- Independently protected approval issuance and replay prevention
- Production IAM least-privilege enforcement
- Protected integrity-baseline administration
- Authoritative evidence refresh
- Tamper-resistant audit logging
- Integrated emergency stop, rollback, and service-health recovery
- Formal operational and change-management authorization

The laboratory evidence supports improvement over V1, but does not establish readiness for unattended destructive production operations.

## Final Engineering Disposition

**V1:** UNSAFE — RETIRED.

**V2:** Improved authority and execution safeguards, validated within the laboratory.

**V3:** Improved evidence-trust safeguards, validated within the documented laboratory scope; canonical implementation remains dry-run only.

**Production decision:** NO-GO for full unattended destructive identity remediation.

Continue read-only evidence collection, dry-run analysis, remediation recommendations, and separately authorized human-approved changes.

The incident investigation and laboratory engineering documentation may be closed while production authorization remains explicitly withheld.

## Final References

- analysis/final-security-automation-engineering-report.md
- analysis/security-automation-decision-brief.md
- analysis/automation-operations-plan.md
- analysis/automation-drift-analysis.md
- analysis/iam-manager-allowlist-recommendation.md
- notebook/engineering-notebook.md
- lessons/lessons-learned.md
