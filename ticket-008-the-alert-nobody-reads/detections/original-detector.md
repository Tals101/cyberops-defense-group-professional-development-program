# Ticket #008 - Original Authentication Detector

## Detector Version

Original / Baseline

## Purpose

Represent the existing authentication detector before tuning.

This detector is intentionally simple and operationally noisy. It attempts to identify authentication failures and repeated failed authentication but lacks sufficient context, aggregation discipline, and alert suppression.

## Detection Logic

The baseline detector evaluates authentication telemetry chronologically.

### Rule 1 - Failed Authentication

Generate an alert for every failed authentication event.

Reason:

Authentication failures can indicate password guessing, credential abuse, user error, stale credentials, or other authentication problems.

Limitation:

A single failed authentication event provides very little evidence that malicious activity is occurring.

---

### Rule 2 - Repeated Failures

For each failed authentication event, examine the previous 10 minutes for the same user.

If at least three failures for that user have occurred within the rolling 10-minute window, generate an additional repeated-failure alert.

Important:

The detector produces another repeated-failure alert for each subsequent failed event while the condition remains true.

It does not group those events into one incident.

---

### Rule 3 - Unfamiliar Source Failure

Generate an additional alert whenever a failed authentication originates from a source marked unfamiliar.

Reason:

An unfamiliar source may increase authentication risk.

Limitation:

The detector treats unfamiliar-source context as independently alert-worthy rather than as supporting evidence.

---

### Rule 4 - Privileged Account Failure

Generate an additional alert whenever a failed authentication involves a privileged account.

Reason:

Authentication activity involving privileged accounts carries higher potential impact.

Limitation:

The detector does not distinguish expected administrative behavior from suspicious behavior.

---

## Alert Generation Behavior

One authentication event may therefore create multiple alerts.

For example, a failed privileged authentication from an unfamiliar source after several previous failures could generate:

1. Failed Authentication
2. Repeated Failures
3. Unfamiliar Source Failure
4. Privileged Account Failure

This creates overlapping alerts describing the same underlying activity.

## Context Not Used

The baseline detector does not correlate:

- a later successful authentication;
- source behavior across multiple users;
- multiple sources targeting the same user;
- familiar-source compromise;
- service-account patterns;
- expected administrative activity;
- long-duration low-and-slow activity;
- related alerts into one investigation unit.

## Suppression

None.

## Exceptions

None.

## Whitelisting

None.

## Expected Operational Weakness

The detector is expected to create substantial alert duplication because individual authentication events may independently satisfy several overlapping rules.

It may also miss suspicious behavior when:

- each individual user has too few failures;
- each source generates only a small number of attempts;
- activity is spread over a long period;
- successful authentication is the most important part of the sequence.

## Baseline Principle

This detector will be measured exactly as written before any tuning is performed.

No threshold, suppression, exception, or contextual logic will be changed until the baseline results have been preserved.
