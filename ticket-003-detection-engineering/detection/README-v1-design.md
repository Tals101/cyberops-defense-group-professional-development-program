# Phase 4 - Detection Design, Version 1

## Goal

The first detector was intentionally simple: identify a short burst of failed SSH password attempts against the same Linux account from the same source IP.

## Version 1 Rule

Generate an alert when all of the following are true:

- The service is SSH.
- Authentication failed.
- The same username is targeted.
- The same source IP produces the failures.
- At least 5 failed password attempts occur.
- The attempts fall within 120 seconds.

In short:

`same source + same user + 5 or more failed SSH passwords within 120 seconds`

## Why I Started at Five Failures

The baseline showed that a real user can mistype a password and then log in normally. Alerting on one failure would create obvious noise, and two failures would still be easy to reach through ordinary user error.

Five attempts in two minutes gave me a reasonable lab starting point: high enough to ignore a simple typo, but low enough to catch a short password-guessing burst. The threshold was treated as a testable assumption, not a production recommendation.

## Correlation Fields

The detector correlates on:

- Username
- Source IP
- Destination host
- Authentication service
- Timestamp
- Authentication result

## Which Event Counts as a Failure

The counted event is:

`Failed password for <user> from <source IP>`

I do not count the separate `pam_unix(sshd:auth): authentication failure` line as another attempt because the baseline confirmed that both records can describe the same password failure.

## Repeated-Message Handling

Ubuntu can compress identical events into records such as:

`message repeated 2 times`

The implementation needs to expand that count logically so repeated-message compression does not hide actual failed attempts.

## Expected Behavior

### Expected to alert

Five failed passwords from `192.168.56.111` against `soc-test` inside two minutes.

### Expected to stay quiet

One bad password followed by a successful login from `192.168.56.1`.

## What Testing Exposed

Version 1 caught the Kali test, but a more realistic legitimate-user test exposed a weakness. From the normal Windows source, the user generated five failed passwords in 29 seconds and then authenticated successfully. Version 1 alerted because the sequence met the threshold exactly as written.

That was a false positive.

The problem was not the counting logic; the rule simply had no way to distinguish an expected source with a successful recovery from an unusual source that never authenticated.

## Tuning Decision

Version 2 would keep the five-in-120 threshold and add context about the source and what happens after the failures.

The next version would distinguish between:

1. Repeated failures from an unusual source with no successful login.
2. Repeated failures from an established source followed by a successful login.

A successful login would not automatically make the activity safe. If failures are followed by success from an unusual source, that could represent successful credential guessing and should still receive attention.

## Evidence

- Version 1 false positive: `testing/false-positive/02-false-positive-v1.txt`
- Below-threshold test: `testing/boundary-tests/05-boundary-below-threshold-pass.txt`
- At-threshold test: `testing/boundary-tests/06-boundary-at-threshold-pass.txt`

## Boundary Check

The threshold behaved as expected in the lab:

- 4 failures: no alert
- 5 failures: alert

That confirmed the implementation was enforcing the configured boundary correctly.
