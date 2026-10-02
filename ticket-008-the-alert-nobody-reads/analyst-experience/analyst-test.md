# Ticket #008 — Analyst Alert Usability Test

## Objective

Evaluate the final analyst-facing alert from the perspective of a SOC analyst who did not design or implement the authentication detection.

The analyst should be able to understand within approximately 60 seconds:

- why the alert requires attention;
- what account and source are involved;
- whether privilege is involved;
- whether authentication succeeded;
- what behavior caused the alert;
- what should be investigated first.

---

# Test Alert

Alert type:

Authentication Attack Sequence

Case ID:

V2C-0006

Severity:

High

Primary user:

admin.backup

Account context:

Privileged

Primary source:

198.51.100.77

Source familiarity:

Unfamiliar

Failure count:

8

Successful authentication:

Yes

Success account:

admin.backup

Detection signals:

V1-01, V1-02, V1-05

Plain-language reason:

Eight failed authentication attempts against privileged account admin.backup from unfamiliar source 198.51.100.77 were followed by a successful authentication within the same attack sequence.

---

# 60-Second Analyst Review

## Question 1 — Why Did This Alert Fire?

Clear.

The analyst can immediately see that repeated failed authentications were followed by a successful login.

The alert does not require reconstruction from individual authentication records.

Result:

PASS

---

## Question 2 — Is the Account Sensitive?

Clear.

The account is explicitly labeled as privileged.

Result:

PASS

---

## Question 3 — Did Authentication Succeed?

Clear.

Successful Authentication is explicitly shown as Yes.

The successful account and timestamp are also available.

Result:

PASS

---

## Question 4 — What Source Was Involved?

Clear.

The source address is shown and identified as unfamiliar.

Result:

PASS WITH CONTEXT ISSUE

The analyst can understand that the source is unfamiliar, but the alert does not state:

- how familiarity was determined;
- what historical period was evaluated.

This could cause the analyst to overestimate the confidence of the familiarity label.

---

## Question 5 — How Large and How Long Was the Activity?

Mostly clear.

The alert provides:

- failure count;
- first observed;
- last observed;
- duration.

Result:

PASS

---

## Question 6 — What Should the Analyst Do First?

Clear.

The alert provides immediate investigation checks, including:

- validate whether the activity was authorized;
- review the successful session;
- identify the associated device;
- examine surrounding authentication activity;
- check privilege or account changes;
- search for related activity.

Result:

PASS

---

# Confusion Identified

## 1. Severity Inconsistency

The example alert is labeled:

High

However, the severity guidance states that suspicious activity involving a successful privileged authentication may qualify as:

Critical

The example therefore does not fully match the documented severity model.

This could create uncertainty about how severity is assigned.

### Recommended Revision

Change the example severity to:

Critical

Or document a specific reason why the example remains High.

The simpler and more internally consistent change is to make this example Critical.

---

## 2. Source Familiarity Needs Qualification

The alert says:

Unfamiliar

But it does not explain the reference period used to determine familiarity.

### Recommended Revision

Display familiarity with a concise qualification.

Example:

`Unfamiliar — no successful authentication from this source for this account during the available 30-day history.`

If the historical period is unavailable, state:

`Unfamiliar based on available authentication history.`

---

## 3. Destination Context Is Missing From the Example

The analyst knows the user and source but does not immediately know:

- destination system;
- authentication application;
- identity provider.

These may materially affect triage.

### Recommended Revision

Where telemetry supports it, display:

- destination system;
- authentication application or service;
- identity provider.

These fields should be contextual and should not be required when the telemetry does not provide them.

---

## 4. Detection Signal IDs Are Secondary Information

The alert includes:

V1-01, V1-02, V1-05

These are useful for engineering provenance but may mean little to a frontline analyst.

### Recommended Revision

Keep the signal IDs, but place them below the plain-language explanation rather than making them a primary triage field.

The analyst should encounter:

1. behavior;
2. risk;
3. success context;
4. investigation priority;

before internal rule identifiers.

---

# Information That Was Immediately Useful

The following information materially improved analyst comprehension:

- behavioral alert title;
- severity;
- privileged-account context;
- primary user;
- primary source;
- source familiarity;
- failure count;
- successful-authentication indicator;
- success timestamp;
- plain-language explanation;
- short analyst summary;
- recommended initial checks.

---

# Information That Should Remain in the Playbook

The analyst did not need detailed procedures within the alert itself.

The following should remain in the investigation playbook:

- complete SIEM queries;
- endpoint commands;
- identity-provider search procedures;
- containment procedures;
- password-reset workflow;
- token revocation procedure;
- host isolation procedure;
- evidence-preservation workflow;
- detailed escalation criteria.

This supports keeping the alert concise.

---

# 60-Second Test Result

Overall result:

PASS WITH REVISIONS

The analyst can determine within approximately 60 seconds:

- why the alert fired;
- that the account is privileged;
- that authentication succeeded;
- the source involved;
- the approximate scale and duration;
- the immediate investigation path.

The alert does not require reconstruction from raw authentication events.

However, three presentation improvements should be made:

1. align the example severity with the documented severity model;
2. qualify the source-familiarity label;
3. add destination/application context when telemetry supports it.

Detection signal IDs should also be visually secondary to the plain-language explanation.

---

# Security Impact of the Usability Findings

None of the identified issues require changing V1 or V2 detection logic.

The findings affect:

- alert presentation;
- analyst interpretation;
- context quality;
- triage consistency.

They do not change detection coverage.

---

# Recommended Action

Revise the final alert design without changing detection logic.

The revised alert should:

- label the privileged-success example Critical;
- qualify source familiarity with the available historical period;
- add destination/application context when available;
- move engineering rule identifiers below the analyst-facing explanation.

After these changes, the alert design can be considered ready for the production-readiness phase.

---

# Phase 8 Analyst Test Status

60-second analyst usability test completed.

Overall result:

PASS WITH REVISIONS

No detection logic changes are recommended from this usability test.
