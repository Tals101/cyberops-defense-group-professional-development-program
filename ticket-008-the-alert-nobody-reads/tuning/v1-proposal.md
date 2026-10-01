# Ticket #008 - Tuning Proposal V1

## Purpose

Define the first proposed detector improvement before implementation.

V1 is intended to reduce redundant and low-value authentication alerts while preserving or improving detection coverage.

The proposal is based on the frozen baseline dataset, baseline detector, noise analysis, and analyst alert review.

No V1 implementation has been performed yet.

---

# Baseline Problems Being Addressed

The baseline detector produced:

- 597 total alerts;
- 308 unique alerted events;
- 289 additional or redundant alerts;
- 48.4% alert redundancy;
- 248 benign alerts;
- 41.5% benign-alert share;
- an estimated 49.75 analyst hours using the lab workload assumption.

The baseline also failed to alert on the successful authentication event in:

- SUS-02 - Failures Followed by Privileged Success
- SUS-05 - Compromised Familiar Source

The baseline presents individual authentication events rather than coherent investigation units.

---

# V1 Design Principle

V1 will not attempt to solve noise by:

- globally increasing thresholds;
- excluding noisy users;
- whitelisting the service account;
- excluding familiar networks;
- excluding unfamiliar networks;
- suppressing all successful authentications;
- suppressing all ordinary authentication failures.

Instead, V1 will test whether alert correlation and grouping can improve analyst usefulness.

---

# Proposed Change 1 - Consolidate Overlapping Risk Signals

## Current Behavior

One failed authentication event may independently create:

- Failed Authentication
- Repeated Failures
- Unfamiliar Source Failure
- Privileged Account Failure

## V1 Change

A single authentication event will not create multiple independent alerts simply because several risk attributes are present.

Instead, privileged status and source familiarity will be attached as context to a correlated detection.

## Expected Noise Reduction

This should directly reduce cross-rule duplicate alerts.

The baseline generated 289 additional alerts beyond the first alert associated with an event.

## Security Risk

If consolidation is implemented incorrectly, meaningful risk indicators could become less visible.

## Compensating Signal

V1 alerts will explicitly include:

- privileged-account status;
- source familiarity;
- source zone;
- failure count;
- related users;
- related sources;
- successful-authentication status where relevant.

## Expected Metric Improvement

Redundancy rate should decrease substantially from the baseline value of 48.4%.

---

# Proposed Change 2 - Correlate Repeated Failures Into Investigation Units

## Current Behavior

Once the repeated-failure condition is met, additional failed events continue generating new alerts.

## V1 Change

Related failures involving the same user and source will be grouped into one investigation unit for a defined correlation window.

The alert will summarize the behavior rather than generating a new investigation for every failure.

## Expected Noise Reduction

This should reduce repeated alerts from:

- stale service credentials;
- concentrated brute force;
- repeated privileged failures;
- familiar-source compromise.

## Security Risk

Grouping could hide meaningful escalation if later activity materially changes.

## False-Negative Risk

A continuing attack could be represented by only one alert even if activity becomes more severe.

## Compensating Signal

V1 will create or escalate a separate higher-value detection when the pattern materially changes, including:

- successful authentication after suspicious failures;
- new privileged-account involvement;
- meaningful expansion across users;
- meaningful expansion across sources.

## Expected Metric Improvement

Total alert volume and estimated analyst workload should decrease while scenario coverage remains intact.

---

# Proposed Change 3 - Detect Failure Followed by Success

## Current Behavior

The baseline evaluates only failed authentication events.

The successful authentication in SUS-02 and SUS-05 generated no alert.

## V1 Change

V1 will correlate successful authentication with recent suspicious failures involving the same user.

A success following a suspicious failure pattern will generate a dedicated high-value alert.

## Expected Security Improvement

This should detect the transition from attempted access to possible successful compromise.

## Noise Risk

Ordinary password mistakes also involve failure followed by success.

If every retry sequence generates an alert, V1 could reproduce the original noise problem.

## Compensating Logic

Success-after-failure will require additional risk context.

Examples include:

- several failures before success;
- privileged account involvement;
- unusual source behavior;
- rapid repeated failures;
- known correlated suspicious activity.

A simple two-mistake-then-success sequence from a familiar workstation should not automatically become a high-priority alert.

## Expected Metric Improvement

Suspicious-event detection should increase from 143 of 145 toward 145 of 145 on the frozen dataset.

---

# Proposed Change 4 - Explicitly Detect One Source Targeting Many Users

## Current Behavior

Distributed password-spray activity appears as many unrelated failure alerts.

## V1 Change

V1 will correlate authentication failures by source over a broader time window.

A source that generates failures against multiple distinct users will create one password-spray investigation alert.

## Expected Security Improvement

The detector will explicitly describe:

- number of targeted users;
- total failures;
- source;
- time range.

## False-Negative Risk

A threshold that requires too many distinct users could miss smaller spray campaigns.

## Compensating Signal

The threshold will remain moderate and will be evaluated against the same dataset.

Individual high-risk activity will still be covered by other V1 correlation logic.

## Expected Metric Improvement

SUS-03 should remain detected while producing far fewer investigation units than the baseline 120 alerts.

---

# Proposed Change 5 - Explicitly Detect Many Sources Targeting One User

## Current Behavior

Distributed attacks against one account appear as separate failures from separate sources.

## V1 Change

V1 will correlate authentication failures by target user across multiple sources.

A user targeted by several sources within the correlation window will create one distributed-targeting alert.

## Expected Security Improvement

SUS-06 will be identified as a coordinated pattern rather than a collection of unrelated failures.

## False-Negative Risk

Very slow attacks spread across a longer time period may fall outside the correlation window.

## Compensating Signal

V1 will retain separate low-and-slow logic for sustained activity involving higher-risk accounts.

## Expected Metric Improvement

SUS-06 should remain detected while requiring fewer alerts.

---

# Proposed Change 6 - Preserve Low-and-Slow Visibility

## Current Behavior

SUS-04 remains visible largely because every individual failure alerts and because the account is privileged and the source unfamiliar.

## V1 Change

V1 will maintain a longer-duration correlation view for higher-risk authentication behavior.

Repeated failures involving privileged accounts over a longer period will remain detectable even when no short burst threshold is exceeded.

## Expected Security Improvement

The detector should preserve visibility into attacks intentionally designed to stay below short-window thresholds.

## False-Negative Risk

If V1 focuses only on short bursts, low-and-slow activity could disappear.

## Compensating Signal

A long-duration privileged-account failure pattern will remain a supported detection condition.

## Expected Metric Improvement

SUS-04 must remain detected.

---

# Proposed Change 7 - Handle Service-Account Noise Without Whitelisting

## Current Behavior

LEG-03 generated:

- 72 benign authentication events;
- 142 alerts.

## V1 Change

The service account will not be excluded.

Instead, repeated failures from the same service account and same source will be grouped into one persistent authentication-problem investigation unit.

## Expected Noise Reduction

The same continuing condition should no longer generate dozens of nearly identical alerts.

## Security Risk

An attacker abusing the service account could hide inside the grouped activity.

## Compensating Signals

V1 should create additional or escalated visibility if the pattern changes, including:

- authentication from a new source;
- successful authentication after failures;
- privileged-context change;
- distributed source behavior;
- significant change in frequency.

## Expected Metric Improvement

LEG-03 alert volume should decrease substantially from the baseline value of 142 alerts without fully suppressing visibility.

---

# V1 Alert Types

V1 is expected to produce investigation-oriented alerts such as:

1. Repeated Authentication Failure Pattern
2. Suspicious Success After Failures
3. Password Spray - One Source, Many Users
4. Distributed Targeting - Many Sources, One User
5. Low-and-Slow Privileged Authentication Activity
6. Persistent Service Authentication Failure

These are investigation units rather than per-event notifications.

---

# What V1 Will Not Do

V1 will not:

- whitelist svc_inventory;
- exclude familiar internal systems;
- exclude unfamiliar external systems;
- ignore privileged activity;
- classify every unfamiliar source as malicious;
- classify every familiar source as benign;
- suppress all successful authentication;
- merely increase the baseline three-failure threshold.

---

# V1 False-Negative Risks

Potential false-negative risks include:

1. grouping may reduce visibility into escalation within an existing alert;
2. password-spray thresholds may miss smaller distributed campaigns;
3. correlation windows may miss very slow attacks;
4. ordinary retry suppression could conceal a real compromise if context is incomplete;
5. persistent service-account grouping could conceal attacker behavior if the pattern does not visibly change.

These risks must be measured during V1 testing.

---

# Required Compensating Signals

V1 must preserve or add visibility for:

- successful authentication after suspicious failures;
- privileged-account activity;
- unfamiliar-source activity as context;
- familiar-source compromise;
- one source targeting many users;
- many sources targeting one user;
- low-and-slow authentication patterns;
- material changes in service-account behavior.

---

# V1 Success Metrics

V1 will be compared against the exact same frozen dataset.

## Alert Volume

Baseline:

597 alerts

Target:

Meaningful reduction without sacrificing suspicious scenario coverage.

No arbitrary minimum reduction percentage is required.

---

## Redundancy

Baseline:

48.4%

Target:

Substantially lower.

---

## Benign Alert Share

Baseline:

41.5%

Target:

Lower than baseline.

---

## Suspicious Scenario Retention

Baseline:

6 of 6 suspicious scenarios detected.

Target:

6 of 6 suspicious scenarios must remain detected.

---

## Suspicious Event Visibility

Baseline:

143 of 145 suspicious events produced alerts.

Target:

The two suspicious successful-authentication transitions must become explicitly visible.

Because V1 groups events into investigation units, event-level alert count alone will not be treated as the primary coverage metric.

---

## Success-After-Failure Coverage

Baseline:

0 of 2 suspicious successful-authentication transitions alerted.

Target:

2 of 2 explicitly detected.

---

## Analyst Workload

Baseline lab estimate:

49.75 hours

Target:

Lower than baseline using the same five-minute-per-alert assumption.

---

## Actionability

V1 alerts should include enough context to explain:

- what pattern occurred;
- which users were involved;
- which sources were involved;
- failure count;
- relevant risk context;
- whether authentication succeeded;
- why the alert requires analyst attention.

---

# Evaluation Question

After V1 is tested, the engineering decision will answer:

"Did V1 improve security signal and analyst actionability while preserving meaningful attack coverage, or did it merely reduce alert volume?"

---

# Current Status

Tuning Proposal V1 documented.

Original detector preserved.

Baseline dataset preserved.

Baseline results preserved.

No V1 implementation has been performed.
