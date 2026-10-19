# Ticket #009 — V2 Safer Automation Design

## Purpose

V2 is designed to separate risk detection from remediation authority.

The goal is not to prevent every possible incorrect decision.

The goal is to ensure that:

- weak evidence cannot directly cause high-impact changes;
- automation authority is proportional to confidence;
- blast radius is bounded;
- rollback exists before enforcement;
- service health is validated after change;
- incomplete or conflicting data fails safely;
- operators can stop remediation immediately.

V2 is not a modified version of V1's single-rule approach.

It is a controlled remediation workflow.

---

# Architecture Overview

V2 separates the workflow into:

1. identity ingestion;
2. evidence validation;
3. risk detection;
4. context enrichment;
5. confidence classification;
6. authority classification;
7. recommendation;
8. approval where required;
9. pre-change snapshot;
10. enforcement;
11. post-change validation;
12. rollback if validation fails;
13. audit logging.

No detection result automatically implies permission to enforce a change.

---

# Safeguard 1 — Dry-Run Capability

## Risk Addressed

V1 could convert an untested rule directly into production changes.

## Control

V2 supports a dry-run mode where decisions are generated but identity state is not changed.

## How It Works

Dry-run mode produces:

- proposed action;
- reason;
- identity context;
- confidence;
- authority category;
- expected impact;
- rollback requirements.

No write operation is permitted.

## What It Does Not Protect Against

Dry-run does not prove that the decision logic is correct.

It only prevents the decision from becoming a production change during testing.

## Failure Mode

If dry-run and enforcement logic diverge, testing could provide false confidence.

Therefore both modes must use the same decision engine.

## Evidence That It Works

Tests must show:

- decisions are generated;
- no identity state changes;
- logs record DRY_RUN;
- before and after states remain identical.

---

# Safeguard 2 — Evidence Completeness Gate

## Risk Addressed

V1 could act using incomplete or misleading data.

## Control

V2 evaluates whether required identity evidence is complete and current before assigning remediation authority.

## How It Works

Required fields depend on identity type and action impact.

Examples:

- identity type;
- owner;
- lifecycle status;
- authentication activity;
- privilege;
- data freshness;
- evidence completeness.

Missing critical evidence prevents automatic enforcement.

## What It Does Not Protect Against

Complete data may still be incorrect.

## Failure Mode

A source system may incorrectly report complete information.

## Evidence That It Works

Tests must demonstrate that identities with:

- missing fields;
- stale data;
- conflicting evidence;

are not automatically remediated.

---

# Safeguard 3 — Identity-Type-Aware Logic

## Risk Addressed

V1 applied human interactive-login assumptions to service identities.

## Control

V2 evaluates behavior according to identity type.

## How It Works

Examples:

Human identities may use:

- workforce status;
- interactive activity;
- lifecycle state.

Service identities may use:

- non-interactive authentication;
- owner;
- business purpose;
- service dependencies;
- approval state.

Privileged identities receive additional safeguards regardless of activity.

## What It Does Not Protect Against

Incorrect identity-type classification.

## Failure Mode

A service identity incorrectly labeled as an employee could enter the wrong decision path.

## Evidence That It Works

Tests must include:

- human identities;
- service identities;
- privileged identities;
- unknown identities.

Each must follow its intended decision path.

---

# Safeguard 4 — Unknown Identity Fail-Safe

## Risk Addressed

Unrecognized identities could receive inappropriate remediation.

## Control

Unknown identity types cannot receive unattended high-impact remediation.

## How It Works

If identity type is unknown or unsupported:

- gather evidence;
- log the condition;
- produce a recommendation;
- require review.

## What It Does Not Protect Against

An identity may be incorrectly classified as a known type.

## Failure Mode

Poor source data may cause false classification.

## Evidence That It Works

Tests must demonstrate that unknown identities are never automatically disabled.

---

# Safeguard 5 — Service Dependency Awareness

## Risk Addressed

V1 disabled an identity supporting Finance LedgerBridge.

## Control

V2 checks documented service dependencies before enforcement.

## How It Works

Any identity with a known production dependency is elevated to REQUIRE APPROVAL or DO NOT AUTOMATE depending on criticality.

The proposed action includes dependency information for the approver.

## What It Does Not Protect Against

Undocumented dependencies.

## Failure Mode

An incomplete dependency inventory could understate impact.

## Evidence That It Works

Tests must show that identities with recorded production dependencies cannot be automatically disabled.

---

# Safeguard 6 — Privileged Identity Protection

## Risk Addressed

V1 could disable privileged identities if they crossed the inactivity threshold.

## Control

Privileged identities cannot be automatically disabled.

## How It Works

V2 checks privilege before authority is granted.

Privileged-account remediation requires approval.

Critical recovery or break-glass identities are classified DO NOT AUTOMATE.

## What It Does Not Protect Against

Incorrect privilege metadata.

## Failure Mode

A privileged identity incorrectly marked standard could receive insufficient protection.

## Evidence That It Works

Tests must demonstrate that administrator and protected identities cannot enter AUTO-REMEDIATE.

---

# Safeguard 7 — Confidence Classification

## Risk Addressed

V1 treated rule match as sufficient confidence for enforcement.

## Control

V2 assigns a confidence level based on evidence quality and agreement.

## How It Works

Possible classifications:

- HIGH;
- MEDIUM;
- LOW;
- INSUFFICIENT.

Automatic remediation requires HIGH confidence plus low impact.

High confidence alone does not authorize high-impact actions.

## What It Does Not Protect Against

Multiple incorrect data sources may agree.

## Failure Mode

Bad correlated data could create artificially high confidence.

## Evidence That It Works

Tests must demonstrate that:

- conflicting sources reduce confidence;
- missing critical fields produce INSUFFICIENT confidence;
- low confidence cannot result in automatic enforcement.

---

# Safeguard 8 — Approval Gate

## Risk Addressed

V1 had no independent control between classification and enforcement.

## Control

Moderate- and high-impact actions require explicit approval.

## How It Works

V2 stages the proposed action with:

- reason;
- evidence;
- confidence;
- dependencies;
- expected impact;
- rollback plan.

Only authorized approval changes the action from staged to executable.

## What It Does Not Protect Against

A human approver can still make an incorrect decision.

## Failure Mode

Approvers may approve without reviewing evidence.

## Evidence That It Works

Tests must show that approval-required actions cannot execute without valid approval.

---

# Safeguard 9 — Maximum Actions Per Run

## Risk Addressed

V1 could remediate every matching identity in one execution.

## Control

V2 enforces a configurable maximum number of state-changing actions per run.

## How It Works

Once the limit is reached:

- additional actions are staged;
- remediation stops;
- the event is logged;
- operator review is required.

## What It Does Not Protect Against

A single permitted action may still cause severe impact.

## Failure Mode

The configured limit may still be too large.

## Evidence That It Works

Tests must show that actions beyond the configured limit are not executed.

---

# Safeguard 10 — Pre-Change Snapshot

## Risk Addressed

V1 had no engineered rollback state.

## Control

V2 records the relevant pre-change identity state before enforcement.

## How It Works

The snapshot contains enough state to restore the identity to its previous known condition.

If snapshot creation fails, enforcement does not proceed.

## What It Does Not Protect Against

Some downstream effects may not be captured in the identity snapshot.

## Failure Mode

The snapshot itself may be incomplete or corrupted.

## Evidence That It Works

Tests must verify:

- snapshot exists before state change;
- snapshot matches original state;
- failed snapshot creation prevents enforcement.

---

# Safeguard 11 — Rollback

## Risk Addressed

V1 had no built-in recovery mechanism.

## Control

V2 defines rollback before enforcement.

## How It Works

When post-change validation fails:

1. halt additional remediation;
2. restore the preserved state;
3. verify restoration;
4. record rollback outcome;
5. escalate if rollback fails.

## What It Does Not Protect Against

Rollback may not reverse every downstream consequence.

## Failure Mode

Rollback itself may fail.

## Evidence That It Works

Tests must intentionally create a bad remediation and verify restoration.

---

# Safeguard 12 — Post-Change Health Check

## Risk Addressed

V1 had no mechanism to detect that remediation broke a dependent service.

## Control

V2 validates affected identity and service health immediately after enforcement.

## How It Works

Validation may include:

- identity state;
- authentication success;
- application health;
- dependent workflow health.

Failure stops additional changes and initiates rollback when available.

## What It Does Not Protect Against

Delayed failures that occur after the validation window.

## Failure Mode

Health checks may themselves be incomplete or unavailable.

## Evidence That It Works

Tests must reproduce the V1 Finance failure and demonstrate that V2 stops and initiates recovery.

---

# Safeguard 13 — Audit Logging

## Risk Addressed

Incident reconstruction is difficult when decision and action evidence is incomplete.

## Control

V2 logs each stage of the decision and remediation process.

## How It Works

Logs include:

- run identifier;
- identity;
- evidence used;
- confidence;
- authority classification;
- proposed action;
- approval;
- before state;
- after state;
- result;
- health validation;
- rollback result.

## What It Does Not Protect Against

Logging does not prevent an incorrect decision.

## Failure Mode

If required audit logging is unavailable, enforcement stops.

## Evidence That It Works

Tests must verify that every state-changing action has a complete audit trail.

---

# Safeguard 14 — Idempotency

## Risk Addressed

Repeated runs may repeat or conflict with prior remediation.

## Control

V2 checks current state and prior action status before changing an identity.

## How It Works

An already completed action is not performed again unless a new valid decision exists.

## What It Does Not Protect Against

A repeated decision may still be wrong.

## Failure Mode

Incorrect action-state tracking may create duplicate or skipped work.

## Evidence That It Works

Running the same approved remediation twice must not cause duplicate state changes.

---

# Safeguard 15 — Emergency Stop

## Risk Addressed

Multiple harmful actions could occur before operators intervene.

## Control

V2 includes an immediate remediation stop mechanism.

## How It Works

The emergency stop prevents additional writes while preserving:

- logs;
- decisions;
- pending actions;
- current evidence.

## What It Does Not Protect Against

It cannot undo actions already completed.

## Failure Mode

Operators may discover the incident only after damage has occurred.

## Evidence That It Works

Tests must demonstrate that activating the stop prevents all subsequent state changes in the run.

---

# V2 Design Review

## What Can V2 Do Automatically?

V2 may automatically:

- ingest identity data;
- validate evidence completeness;
- detect risk;
- collect context;
- calculate confidence;
- classify authority;
- create recommendations;
- create snapshots;
- execute explicitly low-impact AUTO-REMEDIATE actions;
- perform post-change validation;
- stop remediation on safety failure;
- initiate tested rollback where authorized.

---

## What Can V2 Only Recommend?

V2 may only recommend or stage:

- service-account disablement;
- privileged-account disablement;
- changes involving production dependencies;
- changes involving conflicting evidence;
- changes where business ownership requires confirmation;
- high-impact entitlement changes.

Human approval is required before enforcement.

---

## What Can V2 Never Do Unattended?

V2 must never unattendedly:

- delete identities destructively;
- disable break-glass identities;
- disable core IAM recovery identities;
- exceed the configured action limit;
- execute when required logging is unavailable;
- execute a high-impact change without rollback capability;
- remediate an unrecognized identity type;
- perform high-impact remediation when critical evidence is missing.

---

## What Happens When Data Is Incomplete?

The system fails closed with respect to enforcement.

It may:

- collect evidence;
- log;
- recommend;
- request review.

It does not automatically perform the high-impact action.

---

## What Happens When Two Data Sources Disagree?

Confidence is reduced.

The disagreement is logged.

The action moves out of AUTO-REMEDIATE.

Human review is required when the disagreement could materially change the remediation decision.

---

## What Happens When Confidence Is Low?

The system does not perform the high-impact action.

It records the recommendation and evidence for review.

---

## What Happens When Rollback Fails?

V2:

1. stops additional remediation;
2. records rollback failure;
3. raises an incident;
4. preserves current state;
5. requires manual recovery.

The system must not continue changing other identities after failed rollback.

---

## What Happens If Logging Fails?

No new state-changing remediation is permitted.

Detection and evidence collection may continue if safe.

The system fails closed for enforcement because an unlogged production change is unacceptable.

---

## What Happens If Approval Cannot Be Obtained?

The action remains pending.

The identity is not automatically changed merely because approval is delayed or unavailable.

If the risk is urgent, the issue must follow a separate documented emergency process.

---

## What Happens If the System Encounters an Identity Type It Does Not Recognize?

The identity receives no unattended high-impact remediation.

V2:

- logs the unknown type;
- collects available evidence;
- generates a review item;
- requires human classification.

Unknown does not mean safe.

Unknown also does not automatically mean dangerous.

---

# Safe Failure Behavior

V2 defaults to preserving production state when:

- critical evidence is missing;
- identity type is unknown;
- sources materially disagree;
- logging is unavailable;
- rollback preparation fails;
- approval is required but absent;
- run-level limits are reached;
- post-change health validation fails.

The default response to uncertainty is not:

> Disable first and investigate later.

The default response is:

> Stop enforcement, preserve evidence, and escalate according to impact.

---

# Expected V2 Security Improvement

V2 addresses the central failures demonstrated by V1:

V1 combined weak detection evidence with broad enforcement authority.

V2 separates:

- evidence;
- confidence;
- authorization;
- enforcement;
- validation;
- recovery.

A wrong decision may still occur.

The redesigned system is safer because a wrong decision has fewer opportunities to become an uncontrolled production change.

---

# Implementation Gate

V2 implementation must not begin until this design and authority model are preserved in Git as a separate design checkpoint.

The preserved V1 commit remains unchanged.
