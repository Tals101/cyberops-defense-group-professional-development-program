# Ticket #009 — V2 Enforcement and Rollback Validation

## Objective

Validate that V2:

- limits unattended remediation authority;
- bounds the number of changes in one run;
- protects higher-impact identities;
- preserves a known-good pre-change state;
- maintains Finance service health during normal enforcement;
- can recover from a simulated bad identity change.

---

# V2 Enforcement Test

## Configured Safety Limit

Maximum state-changing actions per run:

2

## Observed Result

V2 performed exactly two automatic state changes.

### Automatically Remediated

- nora.hayes — DISABLE — SUCCESS
- kevin.brooks — DISABLE — SUCCESS

### Run Limit Enforced

- contractor.mills — STAGE_ONLY — RUN_LIMIT_REACHED

Although contractor.mills qualified for automatic remediation, V2 did not perform a third state change.

This demonstrates that the blast radius was bounded by configuration rather than by the number of matching identities.

---

# Approval Boundary Validation

The following identities were not automatically changed:

## admin.ops

Authority:

REQUIRE_APPROVAL

Recommendation:

REVIEW

Result:

STAGE_ONLY — APPROVAL_REQUIRED

Reason:

Privileged identity.

---

## svc_records_archive

Authority:

REQUIRE_APPROVAL

Recommendation:

REVIEW

Result:

STAGE_ONLY — APPROVAL_REQUIRED

Reason:

Service identity with a documented dependency.

---

# No-Change Recommendation Validation

## svc_finance_batch

Authority:

REQUIRE_APPROVAL

Recommendation:

KEEP_ENABLED

Enforcement result:

NO_ACTION — RECOMMENDATION_NO_CHANGE

The account remained enabled.

V2 recognized that stale interactive activity did not establish inactivity because recent non-interactive activity showed active service use.

---

# Do-Not-Automate Validation

## analytics.temp

Authority:

DO_NOT_AUTOMATE

Result:

NO_ACTION — AUTOMATION_PROHIBITED

Relevant conditions:

- unknown identity type;
- conflicting evidence;
- service dependency;
- low confidence.

## ingest.bridge

Authority:

DO_NOT_AUTOMATE

Result:

NO_ACTION — AUTOMATION_PROHIBITED

Relevant conditions:

- unknown identity type;
- incomplete evidence;
- stale data;
- elevated privilege;
- service dependency;
- insufficient confidence.

---

# Post-Change Finance Health Validation

After V2 enforcement:

svc_finance_batch remained:

enabled=True

The Finance dependency health check reported:

APPLICATION_STATUS=HEALTHY

This demonstrates that normal V2 enforcement did not reproduce the Finance outage caused by V1.

---

# Rollback Test

A separate isolated rollback-test environment was created from the verified pre-change snapshot.

The Finance service identity was deliberately changed to:

svc_finance_batch enabled=False

This simulated a bad automated remediation decision.

The production-like successful V2 test state and preserved original dataset were not modified during this rollback test.

---

# Rollback Execution

The V2 rollback mechanism compared the bad state against the preserved pre-change snapshot.

Observed result:

Accounts restored: 1

Restored account:

svc_finance_batch

State before rollback:

enabled=False

State after rollback:

enabled=True

---

# Rollback Integrity Validation

The SHA256 hash of the restored rollback-test environment matched the SHA256 hash of the pre-change snapshot.

Expected and observed hash:

A90C324B953030B2C933CACC9FC104A2F5A29A15F6B02E1AB1420091640182D3

This demonstrates that the test identity environment was restored exactly to the preserved known-good state.

---

# Post-Rollback Service Validation

After rollback, the Finance dependency health check reported:

dependency_account=svc_finance_batch enabled=True

APPLICATION_STATUS=HEALTHY

This proves that recovery was validated at both:

- identity-state level;
- dependent-service level.

Restoring an account alone was not treated as proof of recovery.

---

# Comparison With V1

## V1

V1:

- had no run-level action limit;
- disabled service identities automatically;
- disabled an ambiguous identity;
- missed a terminated workforce identity;
- had no approval boundary;
- had no pre-change rollback snapshot;
- had no post-change health validation;
- reproduced a Finance outage.

## V2

V2:

- bounded automatic changes to two per run;
- correctly remediated two low-risk workforce identities;
- stopped the third eligible automatic action;
- protected service identities from unattended disablement;
- protected privileged identities behind approval;
- prohibited automation for unknown and low-confidence identities;
- maintained Finance health;
- preserved pre-change state;
- successfully restored a simulated bad change;
- verified service recovery after rollback.

---

# Recovery Finding

A bad automated decision must not rely on an operator remembering how to reverse it.

Recovery is an engineered control.

For V2, recovery requires:

1. preserve the pre-change state;
2. stop additional remediation;
3. restore the known-good identity state;
4. verify the restored state;
5. validate dependent service health;
6. escalate if rollback or validation fails.

---

# Current Implementation Limitation

The lab demonstrates the rollback mechanism and validates that it works.

The rollback script is currently exercised as a separate controlled recovery step.

A future production implementation should orchestrate:

enforcement → health validation → automatic halt → rollback → recovery validation

as one controlled workflow when policy permits automatic rollback.

Failure of rollback must always stop further remediation and require incident handling.

---

# Validation Result

**PASS**

The V2 controls materially reduce the probability that an incorrect identity classification becomes an uncontrolled production outage.

The tests demonstrate:

- bounded authority;
- approval boundaries;
- fail-safe handling of uncertainty;
- protected service and privileged identities;
- pre-change preservation;
- successful rollback;
- dependent-service recovery validation.
