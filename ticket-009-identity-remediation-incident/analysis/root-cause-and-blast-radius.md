# Ticket #009 — Root-Cause and Blast-Radius Analysis

## Executive Finding

The incident was not caused by a programming error.

V1 executed its configured rule correctly.

The engineering failure occurred because a low-context inactivity signal was treated as sufficient evidence for a high-impact identity change, and the automation had direct authority to enforce that decision without an approval boundary, dependency check, or pre-change safety control.

The service account was disabled because V1 interpreted lack of recent interactive login as evidence of inactivity even though the account was actively authenticating non-interactively and supporting Finance services.

---

# Root-Cause Analysis

## Trigger

The account entered V1's decision path because it was:

- enabled; and
- present in the remediation input dataset.

V1 evaluated every enabled identity in scope.

There was no identity-type filtering before evaluation.

Therefore, ordinary employee accounts, service identities, privileged identities, ambiguous identities, and other account types were all subjected to the same inactivity logic.

The trigger itself was not necessarily incorrect.

Evaluating the account was reasonable.

The failure occurred in what V1 did with the available evidence after evaluation.

---

## Decision Logic

V1 used one principal decision signal:

`days_since_interactive_login >= 90`

For `svc_finance_batch`:

- interactive login age = 240 days;
- threshold = 90 days;
- account enabled = true.

V1 therefore classified the account as stale and issued a DISABLE decision.

The code performed exactly what the rule specified.

However, V1 ignored relevant available information including:

- identity type = service account;
- days since non-interactive authentication = 0;
- business purpose = Finance posting and settlement integration;
- owner = Finance Applications Team;
- service dependencies = Finance LedgerBridge and Finance Settlement Processor;
- approval status = approved;
- lifecycle state = active;
- evidence completeness = complete.

The classification was therefore logically consistent with the narrow rule but inconsistent with the full identity context.

---

## Technical Failure

The central technical failure was an invalid generalization:

> Lack of recent interactive login is equivalent to account inactivity.

That assumption may be useful for some human identities.

It is not universally valid for:

- service accounts;
- API identities;
- scheduled jobs;
- application identities;
- certificate-based identities;
- machine-to-machine authentication.

V1 had access to contextual fields capable of contradicting the stale-account conclusion, but its decision model did not use them.

Specifically, it failed to reconcile:

- stale interactive activity;

against:

- current non-interactive activity;
- active lifecycle state;
- known business purpose;
- production dependencies.

The system therefore treated one signal as dispositive when the broader evidence contradicted it.

---

## Control Failure

The incorrect classification became an operational change because V1 combined:

1. detection;
2. classification;
3. authorization;
4. remediation;

inside one unattended execution path.

There was no independent control between:

> "This account matches the rule"

and:

> "Disable this identity."

V1 had direct authority to change the enabled state of every account in its writable scope.

There was no:

- approval gate;
- protected-identity control;
- dependency check;
- privilege boundary;
- confidence threshold;
- maximum-actions limit;
- pre-change validation;
- service-health gate.

The automation's authority exceeded the confidence justified by its evidence.

---

## Recovery Failure

The simulation provides a straightforward manual recovery path because identity state is stored locally and the pre-change state is preserved.

However, V1 itself provides no built-in recovery capability.

It does not create:

- an automated rollback transaction;
- a restoration package;
- a rollback command;
- a dependency-aware recovery procedure;
- automatic service validation after restoration.

In production, recovery could be more difficult if:

- identity changes propagate to multiple systems;
- tokens or sessions are invalidated;
- credentials require reprovisioning;
- cached authorization state persists;
- multiple identities were changed;
- the pre-change state is not recorded accurately.

The failure is therefore not simply whether a change is technically reversible.

The failure is that V1 does not make reversal an engineered part of remediation.

---

## Process Failure

Several engineering safeguards should have existed before V1 received unattended production authority.

At minimum:

- identity-context requirements;
- authority classification based on action impact;
- dry-run validation;
- blast-radius testing;
- review of service-account behavior;
- privileged-identity protections;
- dependency analysis;
- change limits;
- rollback testing;
- production health validation;
- defined operational ownership.

The process allowed a convenient rule to move from detection logic to production enforcement without proving that its evidence, authority, and recovery model were appropriate for the possible consequences.

---

# Impact

Observed simulated impact:

- `svc_finance_batch` was disabled;
- Finance LedgerBridge lost its required authentication identity;
- authentication failed;
- the simulated Finance application entered FAILED state.

V1 also disabled:

- `svc_records_archive`, a legitimate service identity;
- `analytics.temp`, an ambiguous identity with recent non-interactive activity;
- `nora.hayes`;
- `contractor.mills`.

At the same time, V1 left `kevin.brooks`, a terminated employee account, enabled because the account had recent interactive activity.

The incident therefore demonstrates both:

- false-positive remediation;
- false-negative remediation.

---

# Potential Impact

If circumstances were slightly different, V1 could have caused significantly greater impact.

Examples include:

- multiple application outages;
- interrupted payroll or settlement processing;
- failed scheduled jobs;
- unavailable administrative accounts;
- disabled emergency-access identities;
- interrupted monitoring;
- integration failures;
- delayed financial processing;
- loss of access to recovery systems.

If many identities crossed the 90-day threshold simultaneously, multiple failures could occur before operators recognized that one remediation run was the common cause.

---

# Blast-Radius Analysis

## What Could V1 Change?

V1 can modify the enabled state of every identity supplied within its writable input scope.

It has no intrinsic restriction based on:

- identity type;
- business unit;
- privilege;
- application criticality;
- dependency;
- ownership;
- lifecycle status.

---

## How Many Identities Could It Change in One Run?

There is no configured maximum.

V1 can disable every enabled identity that meets its interactive-login threshold during one execution.

In the simulation:

- identities evaluated: 10;
- identities disabled: 5;
- percentage changed: 50%.

The theoretical run-level limit is therefore the number of identities in scope that satisfy the condition.

---

## Could It Modify Privileged Identities?

Yes.

V1 has no privileged-account protection.

The simulated `admin.ops` account remained enabled only because its interactive login was recent.

If that same privileged account had exceeded the 90-day threshold, V1 would have attempted to disable it.

---

## Could It Modify Service Identities?

Yes.

This was demonstrated directly.

V1 disabled:

- `svc_finance_batch`;
- `svc_records_archive`.

There is no service-account-specific decision boundary.

---

## Could It Modify Multiple Accounts Before Anyone Noticed?

Yes.

V1 processes identities sequentially during the same unattended run.

There is no pause or approval between actions.

There is no maximum-action threshold.

Multiple changes can therefore occur before the first operational symptom is reported.

This behavior occurred in the simulation, where five identities were disabled in one execution.

---

## What Permissions Does the Automation Require?

V1 requires write permission sufficient to change identity enabled/disabled state across its remediation scope.

In a production IAM system, equivalent authority could represent significant control over account availability.

The automation itself therefore becomes a privileged security principal.

Its permissions must be treated as sensitive administrative access rather than ordinary application access.

---

## What Happens If Its Logic Is Wrong?

If the logic is wrong, V1 converts the incorrect conclusion directly into identity changes.

Consequences can include:

- user lockout;
- service outages;
- administrator lockout;
- application failures;
- failed integrations;
- business interruption.

There is no independent mechanism that limits the consequence of an incorrect classification.

---

## What Happens If Its Input Data Is Wrong?

Correct code operating on incorrect data can still produce an incorrect remediation.

Examples:

- stale HR status;
- missing owner;
- missing dependency;
- incorrect lifecycle status;
- incomplete authentication telemetry;
- delayed synchronization.

V1 does not evaluate input freshness or evidence completeness before changing state.

Incorrect data can therefore become an incorrect production change.

---

## What Happens If Its Credentials Are Compromised?

An attacker obtaining V1's production credentials could potentially gain the same identity-changing authority granted to the automation.

Depending on the IAM platform, the attacker could potentially:

- disable accounts;
- disrupt business services;
- target privileged identities;
- target monitoring or security accounts;
- cause widespread denial of service.

The automation's credential therefore represents a high-value privileged credential.

Its scope should be limited independently of application logic.

---

## What Happens If the Script Crashes Halfway Through Remediation?

V1 has no transaction-like behavior.

If it crashes after modifying several identities:

- completed actions remain completed;
- later identities remain unchanged;
- the environment may enter a partially remediated state.

There is no automatic rollback of previously completed changes.

This makes the final state dependent on the exact point of failure.

---

## What Happens If It Runs Twice?

V1 is partially idempotent for accounts already disabled because it does not disable them again.

However, repeated execution still presents risk.

A second run may:

- process newly stale identities;
- operate on updated or inconsistent data;
- repeat evaluation without knowing whether the prior run completed safely.

Idempotent state-setting does not make the overall workflow operationally safe.

---

# Authority Assessment

## Was V1's Authority Proportional to the Confidence of Its Decisions?

No.

V1 made a high-impact decision using a narrow signal with known limitations.

Its confidence model was effectively binary:

- threshold matched;
- threshold not matched.

Yet its authority allowed immediate account disablement across the entire writable identity population.

The evidence quality did not justify the consequence.

A weak or incomplete classification signal was given strong administrative authority.

That mismatch between decision confidence and remediation authority is the central control failure.

---

# Decision Point #1 — IAM Manager Service-Account Exclusion

## Proposal

Exclude all identities marked as service accounts from the inactivity-remediation rule and restore unattended execution.

## Problem the Proposal Solves

The proposal would prevent V1's interactive-login rule from disabling identities correctly labeled as service accounts.

It would likely prevent recurrence of the specific Finance failure reproduced in this simulation.

## Assumption

The proposal assumes:

- service-account classification is accurate;
- every legitimate service account should be exempt from inactivity remediation;
- classification cannot be manipulated;
- service accounts do not require automated security intervention.

Those assumptions are not universally safe.

## Remaining Risks

A broad exclusion could:

- protect abandoned service accounts;
- protect compromised service accounts;
- make misclassified identities invisible to remediation;
- encourage attackers to seek or abuse a protected designation;
- treat critical and low-risk service identities identically.

The classification itself may also be incomplete, stale, or incorrect.

---

# Recommendation to IAM Manager

The Finance incident shows that interactive-login inactivity is not sufficient evidence to disable a service identity, so I agree that V1 should not continue automatically disabling service accounts under the current rule. I do not recommend a blanket permanent exclusion, however.

A broad service-account exemption would prevent this specific failure but introduce another blind spot: abandoned, compromised, or incorrectly classified service accounts could become effectively immune from remediation. It also assumes the service-account designation is complete and trustworthy.

Instead, service identities should follow a separate decision path. The automation may identify risk and collect evidence automatically, but disablement should require service ownership, non-interactive authentication history, dependency information, lifecycle status, and an approval appropriate to the account's impact.

Until those controls exist, service-account matches should be staged for review rather than disabled automatically.

I recommend keeping unattended V1 enforcement suspended while we implement the narrower authority model.
