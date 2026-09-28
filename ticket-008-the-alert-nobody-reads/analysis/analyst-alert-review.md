# Ticket #008 - Analyst Alert Review

## Purpose

Review representative baseline alerts from the perspective of a SOC analyst and determine whether the alerts support meaningful investigation decisions.

The review focuses on:

- analyst decision quality;
- missing context;
- required follow-up lookups;
- actionability;
- duplication;
- likely investigation behavior; and
- operational consequences.

---

# Representative Alert 1 - Ordinary Password Mistake

Scenario:

LEG-02 - Ordinary Password Mistakes

Observed Alert:

Failed Authentication

Example:

User: asmith

Source:

10.20.10.11

Observed behavior:

Two failed authentication attempts occur from the user's familiar workstation.

A successful authentication follows shortly afterward, but the baseline failure alert does not include that context.

## What Decision Can the Analyst Make?

Very little from the individual alert alone.

The analyst can determine that a password failure occurred, but cannot determine whether the event represents:

- a mistyped password;
- forgotten credentials;
- unauthorized password guessing;
- credential stuffing;
- account compromise; or
- another authentication problem.

## What Context Is Missing?

The alert does not show:

- whether authentication later succeeded;
- how many recent failures occurred;
- whether this is normal behavior for the user;
- whether the source is normally associated with the user;
- whether other users are being targeted from the same source;
- whether risk increased after the alert.

## Additional Lookup Required

The analyst would need to review:

- authentication history for the user;
- recent source activity;
- subsequent authentication success or failure;
- potentially endpoint or identity telemetry.

## Is It Actionable?

Low actionability by itself.

## Is It Duplicative?

Not necessarily for the first failure, but repeated isolated failures create multiple low-value investigation units.

## Would an Analyst Reasonably Investigate It?

An analyst receiving hundreds of similar alerts would probably triage it quickly unless additional context suggested higher risk.

## Likely Outcome After Opening

The analyst would perform additional authentication-history lookup and likely determine that the user successfully authenticated shortly afterward.

The alert itself does not provide that conclusion.

---

# Representative Alert 2 - Stale Service Credentials

Scenario:

LEG-03 - Stale Service Credentials

User:

svc_inventory

Source:

10.20.30.25

Observed behavior:

Repeated failed authentication occurs every five minutes.

Beginning with the third failure, individual events may generate:

- Failed Authentication
- Repeated Failures

## What Decision Can the Analyst Make?

The analyst can determine that persistent authentication failure is occurring.

However, the alert does not establish whether the cause is:

- stale stored credentials;
- service misconfiguration;
- unauthorized automation;
- credential attack;
- application failure; or
- another operational problem.

## What Context Is Missing?

The alert does not summarize:

- how long the pattern has continued;
- how often attempts occur;
- whether timing is regular;
- whether the source is a known application server;
- whether the account normally authenticates from this source;
- whether activity is changing or escalating.

## Additional Lookup Required

The analyst would need to review:

- service-account ownership;
- application configuration;
- authentication history;
- asset ownership;
- account behavior over time.

## Is It Actionable?

The pattern is operationally relevant but individual repeated alerts are poorly actionable.

## Is It Duplicative?

Yes.

The same continuing condition repeatedly generates new alerts.

Some events create more than one alert.

## Would an Analyst Reasonably Investigate It?

The first occurrence may deserve investigation.

Dozens of subsequent alerts containing essentially the same information provide diminishing value.

## Likely Outcome After Opening

The analyst may discover stale service credentials and close repeated alerts as known operational activity.

Continued identical alerts may then be skimmed rather than investigated deeply.

---

# Representative Alert 3 - Concentrated Brute Force

Scenario:

SUS-01 - Concentrated Brute-Force Activity

User:

mjohnson

Source:

203.0.113.201

Observed behavior:

Rapid authentication failures occur from one unfamiliar source.

Individual events produce combinations of:

- Failed Authentication
- Unfamiliar Source Failure
- Repeated Failures

## What Decision Can the Analyst Make?

The sequence strongly supports investigation.

However, the individual alerts do not clearly present the sequence as one attack.

## What Context Is Missing?

The alert does not immediately summarize:

- total attempts;
- attack duration;
- velocity;
- whether attempts remain active;
- whether authentication eventually succeeded;
- whether other accounts were targeted.

## Additional Lookup Required

The analyst must reconstruct the behavior from multiple alerts or query the authentication data directly.

## Is It Actionable?

Yes, once correlated.

Individual alerts are less useful than the combined behavior.

## Is It Duplicative?

Highly duplicative.

The same attack creates many overlapping alerts.

## Would an Analyst Reasonably Investigate It?

Yes.

The pattern deserves investigation.

## Likely Outcome After Opening

The analyst would probably pivot to authentication logs to reconstruct the attack and determine whether access succeeded.

The detector should perform more of this correlation before presenting the alert.

---

# Representative Alert 4 - Privileged Failures Followed by Success

Scenario:

SUS-02 - Failures Followed by Privileged Success

User:

admin.backup

Source:

198.51.100.88

Observed behavior:

Eight failed authentications from an unfamiliar source are followed by a successful privileged authentication.

One failure event generated four separate alerts:

- Failed Authentication
- Repeated Failures
- Unfamiliar Source Failure
- Privileged Account Failure

The following successful authentication generated no baseline alert.

## What Decision Can the Analyst Make?

The failure alerts establish that risky privileged authentication attempts are occurring.

They do not tell the analyst that the authentication later succeeded.

## What Context Is Missing?

The most important missing context is the successful login.

The alerts also fail to summarize:

- failure count;
- attempt duration;
- source risk;
- privileged status;
- final successful outcome

as one coherent security event.

## Additional Lookup Required

The analyst must manually inspect subsequent authentication events.

## Is It Actionable?

The activity is highly actionable.

However, the baseline presentation is inefficient and incomplete.

## Is It Duplicative?

Yes.

One authentication event produced four alerts.

## Would an Analyst Reasonably Investigate It?

Yes, assuming alert fatigue has not already reduced analyst attention.

## Likely Outcome After Opening

A careful analyst should discover the later successful privileged authentication and escalate the activity.

The detector itself fails to emphasize that transition.

---

# Representative Alert 5 - Distributed Password Spray

Scenario:

SUS-03 - Distributed Password Spray

Observed behavior:

Multiple unfamiliar sources generate failures against many different users.

Each individual event appears relatively ordinary.

The detector generates:

- Failed Authentication
- Unfamiliar Source Failure

for many events.

## What Decision Can the Analyst Make?

From an individual alert, the analyst cannot easily identify the distributed attack.

The security significance becomes clear only when events are aggregated across users and sources.

## What Context Is Missing?

The alert lacks:

- number of targeted users;
- number of involved sources;
- time range;
- total failure count;
- cross-user relationship;
- cross-source relationship.

## Additional Lookup Required

The analyst must aggregate authentication activity across multiple users and sources.

## Is It Actionable?

Individual alerts have limited actionability.

The aggregate pattern is highly actionable.

## Is It Duplicative?

Yes.

Many events generate separate failure and unfamiliar-source alerts.

## Would an Analyst Reasonably Investigate It?

An individual event may be dismissed as routine unfamiliar-source failure.

The larger campaign could therefore be obscured by the volume of individual alerts.

## Likely Outcome After Opening

Unless the analyst performs broader correlation, the password-spray pattern may not be immediately recognized.

---

# Representative Alert 6 - Compromised Familiar Source

Scenario:

SUS-05 - Compromised Familiar Source

User:

payroll.manager

Source:

10.20.10.18

Observed behavior:

Repeated failures occur from a familiar internal workstation and are followed by successful authentication.

Because the source is familiar, the baseline relies primarily on individual failure and repeated-failure alerts.

The subsequent successful authentication does not alert.

## What Decision Can the Analyst Make?

The repeated failures justify investigation.

However, familiar-source status may make the activity appear less concerning than activity from an unfamiliar external source.

## What Context Is Missing?

The baseline fails to highlight:

- the later successful authentication;
- that the failure pattern changed into success;
- account sensitivity;
- whether the behavior is unusual for the user;
- whether the familiar source itself may be compromised.

## Additional Lookup Required

The analyst must review:

- later authentication events;
- endpoint telemetry;
- user history;
- source behavior;
- potentially account-risk information.

## Is It Actionable?

Yes when viewed as a sequence.

## Is It Duplicative?

Repeated failures generate overlapping alerts while the important success generates none.

## Would an Analyst Reasonably Investigate It?

Possibly, but alert fatigue and familiar-source context could reduce perceived urgency.

## Likely Outcome After Opening

A careful analyst should discover the successful login and investigate possible account or workstation compromise.

---

# Alert Review Findings

## Finding 1 - Alert Count Does Not Equal Investigation Count

597 alerts do not represent 597 independent investigations.

Related events frequently describe the same behavior.

---

## Finding 2 - Risk Context Is Fragmented

Privileged status and unfamiliar-source status often generate separate alerts instead of enriching one investigation record.

---

## Finding 3 - Analysts Must Reconstruct Behavior Manually

The detector presents events.

The analyst must determine the sequence.

This increases investigation time and creates opportunities to miss relationships.

---

## Finding 4 - Success After Failure Is a Major Blind Spot

The baseline missed the successful authentication event in both:

- SUS-02
- SUS-05

These events may represent the most security-significant transition in each scenario.

---

## Finding 5 - Distributed Behavior Is Hard to See

Password spraying and distributed attacks appear as many individual authentication failures instead of one correlated attack pattern.

---

## Finding 6 - Benign Repetition Trains Analysts to Expect Noise

LEG-03 repeatedly presents essentially the same service-account condition.

Repeated exposure to low-value alerts makes future alerts from the same detector less likely to receive full analyst attention.

---

# Why Analysts Might Start Ignoring This Detector

The problem is not simply that the detector produces many alerts.

The problem is that opening an alert often does not answer the analyst's main question:

"Do I need to act?"

Instead, the analyst must repeatedly perform additional lookups to determine:

- whether the activity continued;
- whether authentication succeeded;
- whether other users were involved;
- whether other sources were involved;
- whether the activity is normal for the entity;
- whether several alerts represent the same behavior.

At the same time, the detector repeatedly presents benign and duplicate activity.

This combination creates poor signal per unit of analyst attention.

---

# Engineering Implication

The next detector version should not merely increase thresholds.

V1 should test whether better correlation and alert grouping can:

- reduce redundant alerts;
- preserve attack visibility;
- improve visibility into successful authentication after suspicious failures;
- improve visibility into distributed activity;
- retain meaningful privileged and unfamiliar-source context; and
- present a smaller number of more actionable investigation units.

No V1 implementation has been performed yet.
