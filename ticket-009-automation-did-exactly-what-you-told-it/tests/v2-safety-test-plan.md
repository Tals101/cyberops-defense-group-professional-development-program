# Ticket #009 — V2 Safety Test Plan

## Purpose

This plan defines the tests used to prove that V2 is safer than V1.

Testing must validate not only correct decisions, but also safe behavior when:

- evidence is incomplete;
- authority is insufficient;
- limits are reached;
- recovery is required;
- supporting controls fail.

A successful normal run alone is not sufficient proof of safety.

---

# Test Matrix

## T01 — Dry Run Does Not Modify Identity State

**Control Tested:** Dry-run capability

**Method:**

Run the V2 decision engine against the original identity dataset and compare SHA256 before and after.

**Expected Result:**

- decisions generated;
- identity state unchanged;
- hashes identical.

**Observed Result:** PASS

---

## T02 — Active Finance Service Account Is Not Automatically Disabled

**Control Tested:** Identity-type-aware logic and service-account context

**Method:**

Evaluate `svc_finance_batch`.

Relevant evidence:

- stale interactive login;
- current non-interactive authentication;
- known owner;
- active lifecycle;
- Finance dependencies.

**Expected Result:**

KEEP_ENABLED

No automatic disablement.

**Observed Result:** PASS

---

## T03 — Terminated Workforce Identity Is Detected

**Control Tested:** Context-aware workforce lifecycle logic

**Method:**

Evaluate `kevin.brooks`.

**Expected Result:**

DISABLE candidate with AUTO_REMEDIATE authority.

**Observed Result:** PASS

This corrects a false negative produced by V1.

---

## T04 — Privileged Identity Requires Approval

**Control Tested:** Privileged identity protection

**Method:**

Evaluate `admin.ops`.

**Expected Result:**

- REQUIRE_APPROVAL;
- no automatic disablement.

**Observed Result:** PASS

---

## T05 — Unknown Identity Fails Safely

**Control Tested:** Unknown identity fail-safe

**Method:**

Evaluate:

- `analytics.temp`;
- `ingest.bridge`.

**Expected Result:**

- DO_NOT_AUTOMATE;
- no unattended state change.

**Observed Result:** PASS

---

## T06 — Conflicting or Incomplete Evidence Reduces Authority

**Control Tested:** Evidence completeness and confidence classification

**Method:**

Evaluate identities with:

- conflicting evidence;
- stale evidence;
- incomplete evidence.

**Expected Result:**

LOW or INSUFFICIENT confidence.

Automatic remediation prohibited.

**Observed Result:** PASS

---

## T07 — Maximum Actions Per Run Is Enforced

**Control Tested:** Blast-radius limit

**Configured Limit:**

2 state-changing actions per run.

**Method:**

Provide three eligible AUTO_REMEDIATE / DISABLE candidates.

**Expected Result:**

- first two execute;
- third is staged;
- no third state change.

**Observed Result:** PASS

Observed third candidate:

`contractor.mills — RUN_LIMIT_REACHED`

---

## T08 — Finance Remains Healthy After Normal V2 Enforcement

**Control Tested:** Post-change health validation

**Method:**

Run Finance dependency health check after V2 enforcement.

**Expected Result:**

- `svc_finance_batch enabled=True`;
- Finance LedgerBridge remains healthy.

**Observed Result:** PASS

Observed:

`APPLICATION_STATUS=HEALTHY`

---

## T09 — Pre-Change Snapshot Supports Exact Recovery

**Control Tested:** Pre-change snapshot and rollback

**Method:**

Create rollback-test state from snapshot.

Deliberately disable `svc_finance_batch`.

Execute rollback.

Compare restored environment to original snapshot by SHA256.

**Expected Result:**

Hashes match exactly after restoration.

**Observed Result:** PASS

---

## T10 — Dependent Service Recovers After Rollback

**Control Tested:** Recovery validation

**Method:**

After rollback, validate Finance LedgerBridge dependency.

**Expected Result:**

- service identity restored;
- application health returns to healthy.

**Observed Result:** PASS

Observed:

`APPLICATION_STATUS=HEALTHY`

---

## T11 — Missing Pre-Change Snapshot Prevents Enforcement

**Control Tested:** Fail-safe snapshot requirement

**Method:**

Temporarily make the required snapshot unavailable and attempt enforcement in an isolated test.

**Expected Result:**

- enforcement refuses to start;
- no identity state changes.

**Status:** PASS

---

## T12 — Repeated Execution Is Safe

**Control Tested:** Idempotency

**Method:**

Execute the same approved state-changing workflow against an already-remediated state.

**Expected Result:**

- previously completed changes are not duplicated;
- no unexpected additional changes occur;
- run-level limits remain effective.

**Status:** PASS AFTER CORRECTIVE CONTROL

---

## T13 — Approval-Required Action Cannot Execute Without Approval

**Control Tested:** Approval boundary

**Method:**

Evaluate service and privileged identities without approval.

**Expected Result:**

- action staged only;
- identity remains unchanged.

**Observed Result:** PASS

Examples:

- `admin.ops`;
- `svc_records_archive`.

---

## T14 — Logging Failure Prevents State-Changing Enforcement

**Control Tested:** Audit fail-safe

**Method:**

Simulate inability to establish the required audit log before state changes begin.

**Expected Result:**

- enforcement stops;
- no identity is modified.

**Status:** PASS

---

## T15 — Emergency Stop Prevents Subsequent Changes

**Control Tested:** Emergency stop

**Method:**

Activate the stop mechanism during or before a simulated remediation run.

**Expected Result:**

- no subsequent identity writes;
- completed evidence remains preserved.

**Status:** PASS

---

# Current Evidence Summary

Tests currently passed:

- T01
- T02
- T03
- T04
- T05
- T06
- T07
- T08
- T09
- T10
- T11
- T12
- T13
- T14
- T15

Tests still requiring validation:

None.
---

# Testing Principle

V2 will not be considered safer merely because it makes better decisions on the original ten identities.

The redesign must also demonstrate that:

- authority remains bounded;
- missing safeguards stop enforcement;
- repeated execution does not create uncontrolled changes;
- recovery works;
- higher-impact identities remain protected;
- failures default toward preserving production state.

---

# Current Test Status

**Core V2 safety controls validated.**

**All planned V2 safety tests are complete.**




