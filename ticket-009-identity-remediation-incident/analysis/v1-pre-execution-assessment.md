# Ticket #009 — V1 Pre-Execution Assessment

## Purpose

This assessment documents the expected behavior, assumptions, authority, and potential failure modes of V1 before execution.

The predictions in this document must not be changed after V1 runs.

---

## What Is V1 Trying to Accomplish?

V1 is intended to reduce risk from stale identities.

Its goal is to identify enabled accounts that appear unused and disable them automatically.

The rule assumes that an account with no recent interactive login is likely stale and therefore represents unnecessary access.

---

## What Evidence Does V1 Use?

V1 uses only:

- whether the account is currently enabled;
- days since the last interactive login.

V1 does not use:

- non-interactive authentication activity;
- identity type;
- employment status;
- account ownership;
- privilege;
- business purpose;
- service dependencies;
- approval status;
- lifecycle state;
- data freshness;
- evidence completeness.

---

## What Decision Does V1 Make?

For each enabled identity:

- if `days_since_interactive_login` is 90 days or greater, V1 disables the account;
- if the value is below 90 days, V1 leaves the account enabled;
- if interactive-login data is unavailable, V1 leaves the account enabled.

---

## What Authority Does V1 Have?

Within the simulation, V1 has direct authority to change the `enabled` state of any account supplied in its input dataset.

There is:

- no human approval step;
- no identity-type restriction;
- no privilege boundary;
- no service-dependency check;
- no business-owner confirmation;
- no remediation limit;
- no separate recommendation mode;
- no rollback performed before the action becomes effective.

This means a decision produced by the rule becomes a state change immediately.

---

# Pre-Execution Predictions

## Predicted to Remain Enabled

### emma.reed

Predicted decision: KEEP ENABLED

Reason:

- interactive login age is 1 day;
- below the 90-day threshold.

---

### samir.patel

Predicted decision: KEEP ENABLED

Reason:

- interactive login age is 12 days;
- below the threshold.

---

### kevin.brooks

Predicted decision: KEEP ENABLED

Reason:

- interactive login age is only 18 days.

This is an important expected V1 weakness.

The account belongs to a terminated employee and is already in a pending-disable lifecycle state, but V1 does not consider those facts.

---

### admin.ops

Predicted decision: KEEP ENABLED

Reason:

- interactive login age is 3 days.

V1 will leave the account alone because it does not meet the stale-login threshold.

---

### ingest.bridge

Predicted decision: KEEP ENABLED

Reason:

- interactive login age is unavailable;
- V1 does not treat missing activity data as a match.

The account has elevated privilege, stale data, incomplete evidence, and unclear approval status, but V1 does not evaluate those fields.

---

## Predicted to Be Disabled

### nora.hayes

Predicted decision: DISABLE

Reason:

- interactive login age is 135 days;
- exceeds the 90-day threshold.

This may be a reasonable remediation candidate because the account is also marked inactive.

---

### svc_finance_batch

Predicted decision: DISABLE

Reason:

- interactive login age is 240 days;
- exceeds the threshold.

This is predicted to be an incorrect and operationally dangerous decision.

The account:

- is a legitimate service account;
- has current non-interactive authentication activity;
- supports Finance production services;
- has an identified owner;
- has an approved business purpose;
- is in an active lifecycle state.

V1 ignores all of this context.

This account is expected to reproduce the simulated Finance outage.

---

### svc_records_archive

Predicted decision: DISABLE

Reason:

- interactive login age is 400 days;
- exceeds the threshold.

This is also predicted to be an incorrect decision.

The account is a legitimate approved service identity supporting a quarterly archival process.

Its infrequent use makes interactive-login age a poor measure of whether the account is still required.

---

### contractor.mills

Predicted decision: DISABLE

Reason:

- interactive login age is 160 days;
- exceeds the threshold.

This appears likely to be an appropriate remediation because:

- the contractor engagement has expired;
- approval has expired;
- recent activity is absent.

However, V1 does not know or use those facts.

It reaches the decision only because of interactive-login age.

---

### analytics.temp

Predicted decision: DISABLE

Reason:

- interactive login age is 105 days;
- exceeds the threshold.

This is predicted to be unsafe.

The account has:

- recent non-interactive activity;
- an application dependency;
- unresolved ownership;
- conflicting evidence;
- pending review status.

The available information is ambiguous.

A high-impact automated action should not be taken solely because interactive-login activity is old.

---

# Predicted V1 Outcome Summary

Predicted accounts disabled:

1. nora.hayes
2. svc_finance_batch
3. svc_records_archive
4. contractor.mills
5. analytics.temp

Predicted accounts left enabled:

1. emma.reed
2. samir.patel
3. kevin.brooks
4. admin.ops
5. ingest.bridge

Predicted total disabled: **5**

Predicted total left enabled: **5**

---

# Assumptions Built Into V1

V1 implicitly assumes:

1. interactive login activity is a reliable measure of account use;
2. accounts without recent interactive use are safe to disable;
3. the same inactivity rule is appropriate for human and non-human identities;
4. business purpose does not need to be checked before remediation;
5. service dependencies do not need to be checked;
6. privilege does not change the required approval level;
7. ownership information is unnecessary;
8. non-interactive authentication is irrelevant;
9. a matching rule provides sufficient evidence for direct enforcement;
10. every correct rule match is safe to convert directly into a production change.

These assumptions are reasonable enough to appear operationally convenient, but several are unsafe.

---

# What Could Go Wrong?

V1 could:

- disable a legitimate service account;
- interrupt a production application;
- disable an account that is active through non-interactive authentication;
- disable an ambiguous account despite incomplete evidence;
- miss a terminated employee because the employee logged in recently;
- leave an elevated account untouched because activity data is missing;
- disrupt scheduled or infrequent business processes;
- make several incorrect changes in the same execution;
- create an outage before a human has an opportunity to review the decision.

---

# Maximum Damage of One Incorrect Decision

One incorrect decision could disable an identity required by a critical production service.

Potential consequences include:

- application outage;
- failed financial processing;
- scheduled job failure;
- integration failure;
- authentication failure;
- delayed business operations;
- emergency recovery activity.

The impact of one incorrect identity decision therefore may be much larger than the account itself.

---

# Maximum Run-Level Blast Radius

V1 evaluates every enabled identity supplied to it and can directly disable every account that meets the threshold.

There is no per-run remediation limit.

Therefore, the theoretical blast radius is not one account.

It is every account in the automation's writable scope that satisfies the rule.

In this simulation, V1 is predicted to disable 5 of 10 identities in a single execution.

In a production environment with broader scope, the same design could affect many identities and multiple dependent services before an operator notices the problem.

---

# Pre-Execution Assessment

V1 is expected to demonstrate that a technically correct implementation of an overly narrow rule can still produce unsafe security outcomes.

The likely failure is not that Python executes the rule incorrectly.

The likely failure is that:

1. insufficient evidence is treated as sufficient evidence;
2. decision logic ignores identity context;
3. a low-confidence classification has direct production authority;
4. there is no approval boundary proportional to the potential consequence;
5. one bad decision can immediately become an operational outage.

These predictions are recorded before V1 execution and will not be revised after the results are observed.
