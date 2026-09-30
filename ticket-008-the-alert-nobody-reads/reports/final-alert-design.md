# Ticket #008 — Final Analyst Alert Design

## Purpose

Define the analyst-facing authentication alert produced from the tuned detection strategy.

The alert must provide enough context for an analyst to quickly understand:

- what happened;
- why the activity was considered suspicious;
- who and what are involved;
- whether a successful authentication occurred;
- what makes the activity important;
- what should be checked next.

The alert should not require the analyst to manually reconstruct the detection logic from raw authentication events.

---

# Design Principle

The alert should answer three questions within approximately 60 seconds:

1. Why did this alert fire?
2. What is the potential security impact?
3. What should I investigate first?

---

# Recommended Alert Structure

## Alert Title

Use a short behavioral title rather than a generic authentication-failure label.

Examples:

- Authentication Attack Sequence
- Password Spray Campaign
- Distributed Account Targeting
- Persistent Service Authentication Failure

The title should describe the observed behavior, not merely the log event type.

---

# Severity

Severity should reflect contextual risk rather than failure count alone.

Recommended considerations include:

- privileged account involvement;
- successful authentication after suspicious failures;
- number of users targeted;
- number of sources involved;
- source familiarity;
- attack duration;
- repeated or related prior behavior;
- endpoint or identity risk context when available.

Suggested levels:

- Critical — suspicious sequence includes successful privileged authentication or other strong compromise evidence.
- High — privileged targeting, suspicious success, or broad distributed campaign.
- Medium — suspicious repeated activity requiring investigation but without confirmed success or privileged impact.
- Low — operationally relevant behavior with weak security indicators.

Severity should remain explainable to the analyst.

---

# Core Alert Fields

## 1. Alert / Case ID

Example:

`V2C-0006`

Purpose:

Provides a unique identifier for case management, evidence tracking, and analyst communication.

---

## 2. Detection Name

Example:

`Authentication Attack Sequence`

Purpose:

Describes the behavioral pattern that caused the alert.

---

## 3. Severity

Example:

`High`

Purpose:

Provides triage priority based on the observed risk context.

---

## 4. First Observed

Example:

`2026-09-30 10:14:00`

Purpose:

Shows when the suspicious activity began.

---

## 5. Last Observed

Example:

`2026-09-30 10:22:00`

Purpose:

Shows the most recent activity included in the case.

---

## 6. Duration

Example:

`8 minutes`

Purpose:

Allows the analyst to quickly understand whether the behavior was rapid, sustained, or low-and-slow.

---

## 7. Primary User

Example:

`admin.backup`

Purpose:

Identifies the primary account associated with the suspicious activity.

---

## 8. Account Context

Example:

`Privileged account`

Possible values may include:

- standard user;
- privileged user;
- service account;
- unknown.

Purpose:

Immediately communicates account sensitivity.

---

## 9. Primary Source

Example:

`198.51.100.77`

Purpose:

Identifies the principal source associated with the suspicious activity.

---

## 10. Source Familiarity

Example:

`Unfamiliar — based on available authentication history`

Possible values:

- familiar;
- unfamiliar;
- mixed;
- unknown.

Purpose:

Provides context without treating familiarity as proof of legitimacy.

Where possible, the alert should state the historical basis used to determine familiarity.

Example:

`Unfamiliar — no successful authentication from this source for this account during the available lookback period.`

If a precise lookback period is unavailable, state:

`Unfamiliar — based on available authentication history.`

---

## 11. Related Users

Example:

`admin.backup`

or for campaigns:

`user01; user02; user03; user04; user05`

Purpose:

Shows whether the behavior affects one identity or multiple identities.

---

## 12. Related Sources

Example:

`198.51.100.77`

or multiple sources for distributed behavior.

Purpose:

Shows whether activity originates from one source or distributed infrastructure.

---

## 13. Failure Count

Example:

`8`

Purpose:

Provides scale without forcing the analyst to count raw events.

---

## 14. Distinct User Count

Example:

`1`

Purpose:

Helps distinguish repeated targeting from spray behavior.

---

## 15. Distinct Source Count

Example:

`1`

Purpose:

Helps distinguish single-source behavior from distributed targeting.

---

## 16. Successful Authentication Observed

Example:

`Yes`

Purpose:

This field must be highly visible.

A suspicious success can materially change the urgency and investigation path.

---

## 17. Successful Account

Example:

`admin.backup`

Purpose:

Identifies the account associated with the suspicious success when applicable.

---

## 18. Success Timestamp

Example:

`2026-09-30 10:22:00`

Purpose:

Allows immediate correlation with endpoint, identity, and network activity.

---

## 19. Triggering Detection Signals

Example:

`V1-01; V1-02; V1-05`

Purpose:

Preserves detection provenance without requiring the analyst to understand implementation details.

---

## 20. Why This Alert Fired

This should be written in plain language.

Example:

`Eight failed authentications against privileged account admin.backup from unfamiliar source 198.51.100.77 were followed by a successful authentication within the same sequence.`

Purpose:

This is one of the most important alert fields.

The analyst should not have to interpret thresholds or source code to understand the reason for escalation.

---

# Recommended Analyst Summary

Every case should contain a short summary near the top.

Example:

`High-severity authentication attack sequence involving privileged account admin.backup. Eight failures from unfamiliar source 198.51.100.77 were followed by a successful authentication. Review the successful session and associated endpoint activity immediately.`

The summary should contain:

- behavior;
- account risk;
- source context;
- success context;
- immediate investigation priority.

---

# Prior Behavior Context

When reliable historical data is available, include concise context such as:

- first observed source for this account;
- source previously used successfully by this user;
- recent similar alerts;
- recent password-reset activity;
- previous failed-authentication baseline;
- prior successful login frequency;
- recent privilege changes.

Example:

`No successful authentication from this source was observed for this account during the available historical period.`

Historical context must clearly state the period being evaluated.

---

# Related Entity Context

Where available, the alert may include:

- hostname;
- device identity;
- business unit;
- identity provider;
- authentication application;
- destination system;
- geographic or network context;
- endpoint risk state.

These fields should improve investigation speed rather than simply add more data.

When available in telemetry, the following should be promoted into the main analyst-facing context:

- destination system;
- authentication application or service;
- identity provider.

If the telemetry does not provide these values, do not invent them.

---

# Recommended Initial Checks

The alert should provide a short set of immediate checks.

Example:

1. Confirm whether the user recognizes the authentication activity.
2. Review the successful session, if present.
3. Check endpoint activity associated with the source device.
4. Review authentication activity immediately before and after the case timeframe.
5. Check for privilege changes or unusual account activity.
6. Search for related attempts involving the same source or account.
7. Escalate if the success is unauthorized or additional compromise indicators are found.

These should be concise and directly relevant to the alert.

---

# What Belongs in the Alert?

The alert should contain information required for immediate triage.

Include:

- case ID;
- detection name;
- severity;
- first and last observed timestamps;
- duration;
- primary user;
- privilege/account context;
- primary source;
- familiarity context;
- related users;
- related sources;
- failure count;
- successful authentication status;
- successful account and timestamp when applicable;
- triggering signal names;
- plain-language firing reason;
- concise analyst summary;
- limited historical context;
- immediate recommended checks.

The goal is fast comprehension.

---

# What Belongs in the Investigation Playbook?

Detailed investigative procedures should remain outside the alert.

The playbook should contain:

- detailed identity-provider queries;
- endpoint investigation commands;
- SIEM searches;
- network investigation procedures;
- user validation procedures;
- escalation criteria;
- containment options;
- evidence-preservation instructions;
- account disablement procedures;
- password reset procedures;
- token and session revocation procedures;
- host isolation procedures;
- communications templates;
- incident-classification guidance.

The alert tells the analyst what happened and where to begin.

The playbook explains how to perform a full investigation.

---

# What Should Not Be in the Alert?

Avoid filling the alert with:

- raw detection source code;
- long threshold explanations;
- every authentication event;
- large log excerpts;
- full investigation procedures;
- unnecessary internal implementation details;
- unexplained numeric scores;
- generic recommendations unrelated to the observed behavior.

Too much information recreates the analyst-attention problem the tuning effort was intended to solve.

---

# Example Final Alert

## Authentication Attack Sequence

**Case ID:** V2C-0006  
**Severity:** Critical  
**First Observed:** 2026-09-30 10:14:00  
**Last Observed:** 2026-09-30 10:22:00  
**Duration:** 8 minutes  

**Primary User:** admin.backup  
**Account Context:** Privileged  
**Primary Source:** 198.51.100.77  
**Source Familiarity:** Unfamiliar — based on available authentication history  

**Related Users:** admin.backup  
**Related Sources:** 198.51.100.77  
**Failure Count:** 8  
**Successful Authentication:** Yes  
**Success Account:** admin.backup  
**Success Time:** 2026-09-30 10:22:00  

### Why This Alert Fired

Eight failed authentication attempts against privileged account admin.backup from unfamiliar source 198.51.100.77 were followed by a successful authentication within the same attack sequence.

**Detection Signals:** V1-01, V1-02, V1-05

### Analyst Summary

Critical authentication attack sequence involving a privileged account. Repeated failures from an unfamiliar source were followed by a successful login. Investigate the successful session and associated endpoint activity immediately.

### Recommended Initial Checks

1. Confirm whether admin.backup activity was authorized.
2. Review activity performed during the successful session.
3. Identify the device associated with 198.51.100.77.
4. Review surrounding authentication events.
5. Check for privilege or account changes.
6. Search for related activity involving the same source.
7. Escalate if the successful login cannot be validated.

---

# Alert Quality Goal

An analyst who did not build the detector should be able to determine within approximately 60 seconds:

- why the alert fired;
- whether a privileged account is involved;
- whether authentication succeeded;
- which user and source are involved;
- whether the source is familiar;
- how large and how long the sequence was;
- what initial checks should be performed.

The analyst should not need to reconstruct the detection from raw logs before beginning triage.

---

# Phase 8 Status

Final analyst-facing alert structure defined.

The next step is an analyst usability test to identify confusion, missing context, or unnecessary information before the design is considered final.

