# Ticket #008 - Authentication Detector V1

## Detector Version

V1 - Correlation and Investigation Units

## Purpose

Reduce redundant authentication alerts while preserving or improving meaningful attack visibility.

V1 does not whitelist users, accounts, hosts, or networks.

V1 does not use ground-truth scenario labels.

---

# Design Principle

The baseline generated multiple alerts for individual events.

V1 instead creates investigation-oriented alerts representing correlated behavior.

Risk attributes such as privileged status and source familiarity enrich an alert rather than automatically creating separate alerts.

---

# V1-01 - Rapid Repeated Authentication Failures

Create one investigation alert when:

- the same user;
- from the same source;
- generates at least 5 failed authentications;
- within 10 minutes.

Alert once per user/source pattern rather than once per subsequent failure.

Relevant context included:

- failure count;
- user;
- source;
- privileged status;
- source familiarity;
- time range.

Purpose:

Detect concentrated password guessing while avoiding alerts for ordinary two-attempt password mistakes.

---

# V1-02 - Suspicious Success After Failures

Create a dedicated alert when a successful authentication follows recent failures for the same user and source and either:

- at least 5 failures occurred within the previous 10 minutes; or
- the account is privileged and at least 3 failures occurred within the previous 10 minutes.

Purpose:

Identify the transition from attempted credential abuse to possible successful compromise.

A normal two-failure-then-success retry sequence does not meet this condition.

---

# V1-03 - Password Spray: One Source, Many Users

Create one investigation alert when:

- one source generates failed authentication against;
- at least 5 distinct users;
- within 120 minutes.

The source may be familiar or unfamiliar.

Source familiarity is retained as context rather than used as an exclusion.

Purpose:

Detect distributed password guessing that may remain below per-user thresholds.

---

# V1-04 - Distributed Targeting: Many Sources, One User

Create one investigation alert when:

- one user receives failed authentication from;
- at least 3 distinct sources;
- within 60 minutes.

Purpose:

Detect distributed attacks in which each source generates only a small number of attempts.

---

# V1-05 - Low-and-Slow Privileged Authentication Activity

Create one investigation alert when:

- a privileged account;
- receives at least 4 failed authentications;
- from the same source;
- within 120 minutes;
- and that source is unfamiliar.

Purpose:

Preserve visibility into higher-risk authentication activity intentionally spread over time.

The unfamiliar-source requirement prevents expected familiar administrative activity from automatically generating this long-duration alert while still retaining other telemetry for that activity.

---

# V1-06 - Persistent Service Authentication Failure

Create one investigation alert when:

- account_type is service;
- the same service account;
- from the same source;
- generates at least 3 failed authentications;
- within 15 minutes.

The service account is not whitelisted.

The alert represents the persistent condition as one investigation unit.

Purpose:

Preserve visibility into repeated service-account failures without generating dozens of identical alerts.

---

# Investigation Grouping

Each detection type creates one alert for the qualifying correlation pattern.

Once created, later matching events do not create another identical investigation alert for that same entity combination during the dataset evaluation period.

Materially different behavior may still create another alert type.

Examples:

- repeated failures followed by success can create V1-01 and later V1-02;
- distributed behavior can create V1-03 or V1-04;
- privileged low-and-slow activity can create V1-05.

These represent different security decisions rather than duplicate descriptions of one individual event.

---

# Alert Context

Each V1 alert will contain, where applicable:

- first observed time;
- last observed time;
- triggering event;
- related event IDs;
- user or users;
- source or sources;
- failure count;
- distinct-user count;
- distinct-source count;
- privileged context;
- familiar/unfamiliar context;
- successful-authentication status;
- detection reason.

---

# Explicit Non-Goals

V1 does not:

- exclude svc_inventory;
- whitelist internal sources;
- blacklist all external sources;
- exclude ordinary users;
- suppress all failures;
- treat unfamiliar as malicious;
- treat familiar as trusted;
- simply raise the baseline threshold globally.

---

# Known Risks

V1 may lose visibility when:

- an attack remains below every defined correlation condition;
- a password spray targets fewer than five users;
- distributed targeting uses fewer than three sources;
- low-and-slow activity exceeds the 120-minute correlation window;
- service-account abuse closely resembles the established persistent-failure pattern.

These risks must be evaluated after V1 runs.

---

# Required Test

V1 must run against the exact same frozen 1,000-event dataset used for the baseline.

The dataset must not be modified after observing V1 results.

---

# Current Status

V1 logic defined.

V1 has not been executed.

Baseline detector remains unchanged.
