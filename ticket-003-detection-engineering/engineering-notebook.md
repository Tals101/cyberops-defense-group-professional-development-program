# Ticket #003 - Phase 1: Problem Definition

## Starting Point

At the beginning of the investigation, the SOC had several authentication events tied to the same Linux account, but the events were being viewed one at a time. That made it difficult to tell whether the activity was a normal login problem or something that deserved escalation.

What was known at that point:

- Several authentication-related events involved the same Linux user account.
- The events occurred fairly close together.
- At least some of the activity could have been legitimate.
- Unauthorized access had not been confirmed.
- The available monitoring showed individual events but did not provide enough correlation to explain the sequence.

## Questions I Needed to Answer

Before writing a rule, I needed more context:

- Which Linux account was involved?
- How many failed logins actually occurred?
- How quickly did they happen?
- Which source IPs were responsible?
- Did any of the attempts eventually succeed?
- Was the source normal for that account?
- What does an ordinary login sequence look like for the user?
- Did the activity occur during an expected time period?
- Is the account privileged or administrative?
- Were different authentication methods involved?
- Did the same source target other accounts?
- Had the source communicated with the Linux host before?

## Working Hypotheses

### 1. Ordinary password mistakes

A legitimate user may have typed the wrong password several times and then logged in normally.

### 2. Password guessing

Someone without authorization may have tried a series of passwords against a valid account over a short period.

### 3. Credentials eventually worked

The failed attempts may have been followed by a successful login because the correct password was guessed or obtained.

### 4. Legitimate administrative activity

An administrator could have connected from another authorized system and generated failures during troubleshooting, a password change, or another routine task.

## Initial Detection Goal

The first goal was to identify repeated failed SSH authentication against the same Linux account in a short window, then use source and login-sequence context to decide whether the pattern looked more like user error or attempted unauthorized access.

An isolated password mistake should not be enough to create a high-priority SOC alert.

---

# Phase 2 - Normal Behavior Baseline

## Establishing Normal SSH Activity

I started by confirming what a normal SSH login looked like in the lab. The Ubuntu host recorded a successful password authentication for the `analyst` account from `192.168.56.1`, followed by a normal SSH session opening.

Baseline event details:

- User: `analyst`
- Source IP: `192.168.56.1`
- Authentication method: password
- Result: successful
- Service: SSH
- Destination port: 22

## Initial Baseline Assumptions

For this lab, I treated the following behavior as normal unless other context suggested otherwise:

1. A successful SSH login from an expected lab source.
2. One or two isolated password failures caused by a typo.
3. A failed login followed shortly by a successful login from the same expected source.
4. Normal SSH session creation after successful authentication.
5. Routine administrative activity without a burst of repeated failures.

## Why a Single Failure Is Not Enough

One bad password is common and does not say much by itself. To make the detector useful, I needed to consider the number of failures, how quickly they happened, the target account, the source IP, and what happened next.

The original baseline was small, so I added a controlled user-error test before deciding on the final logic.

## Benign Password Mistake Test

Using the `soc-test` account from `192.168.56.1`, I entered one wrong password and then the correct password.

The log sequence showed:

1. An authentication failure for `soc-test`.
2. A `Failed password` event from `192.168.56.1`.
3. A successful password login about five seconds later.
4. A normal SSH session opening.

This sequence should not create a high-priority alert. It looks like an ordinary password typo followed by a successful retry from the expected source.

## Logging Detail That Mattered

The single bad password produced both of these records:

- `pam_unix(sshd:auth): authentication failure`
- `Failed password for soc-test`

They describe the same failed login attempt. Counting both would double the failure total, so the detector uses the `Failed password` record as the event to count.

## Evidence

- `testing/baseline/02-normal-soc-test-login.log`
- `testing/baseline/03-benign-single-password-mistake.log`

---

# Phase 3 - Suspicious Authentication Scenario

## Scenario Setup

Next, I generated a controlled burst of failed SSH logins from the Kali Linux lab VM at `192.168.56.111`. The target was the `soc-test` account on `ubuntu-soc-lab`.

The activity stayed entirely inside the authorized lab environment.

## Activity Generated

- Target account: `soc-test`
- Destination host: `ubuntu-soc-lab`
- Destination IP: `192.168.56.121`
- Source system: Kali Linux
- Source IP: `192.168.56.111`
- Service: SSH
- Failed password attempts: 5
- Successful login from Kali: No

The five failures occurred within 67 seconds.

## Why This Looked Different From the Baseline

The normal test had one bad password, came from the expected Windows source, and was followed almost immediately by a successful login.

The Kali test was different in several useful ways: there were five failures, all were aimed at the same account, they happened close together, they came from a source outside the established baseline, and no successful login followed.

That combination provided much stronger grounds for investigation than a single failed login.

## Evidence

`testing/true-positive/04-suspicious-five-failures.log`

## Unexpected Finding: Repeated-Message Compression

One issue appeared while reviewing the logs. Five failed attempts did not produce five separate `Failed password` lines. Ubuntu compressed repeated records and wrote:

`message repeated 2 times`

The visible entries represented:

- 1 failed attempt
- 2 failures represented by the repeated-message entry
- 1 failed attempt
- 1 failed attempt

Actual total: 5 failed logins.

## Impact on the Detector

A rule that only counts matching lines would undercount this sequence. I therefore added handling for repeated-message compression so the detector uses the number of represented failures rather than the number of visible log lines.

---

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

---

# Phase 6 - Detection Tuning History

## Version 1: What Worked and What Did Not

The first version used one rule:

- Failed SSH password authentication
- Same username
- Same source IP
- 5 or more failures
- Within 120 seconds

It worked against the suspicious Kali test. The `soc-test` account received five failed passwords from `192.168.56.111` in 67 seconds, and the detector alerted.

The weakness appeared during the legitimate retry test. The same account received five bad passwords from the normal Windows source `192.168.56.1` in 29 seconds, followed by a successful login. Version 1 alerted on that sequence too.

At that point, the false positive made it clear that frequency alone was not enough.

## Version 2: Added Context

I kept the original threshold but added two checks:

- Whether the source is already known for the account
- Whether the same user successfully logs in from the same source within 60 seconds after the failures

For this lab:

- `192.168.56.1` is the established normal source for `soc-test`.
- `192.168.56.111` is treated as unusual.

When the threshold is reached, Version 2 asks whether the source is known and whether a successful login follows. The high-priority alert is suppressed only when both are true. If the source is unusual, or there is no successful login, the alert still fires.

## Validation Results

### True positive

Kali source `192.168.56.111` produced five failures with no successful login.

Result: ALERT - PASS.

### True negative

The normal source produced one bad password followed by a successful login.

Result: NO ALERT - PASS.

### False-positive retest

The normal source produced five failures followed by a successful login.

- Version 1: ALERT - false positive
- Version 2: NO HIGH-PRIORITY ALERT - PASS

### Boundary test

- 4 failures: no alert
- 5 failures: alert

Result: PASS.

## Tuning Outcome

Version 2 kept the tested true-positive behavior while eliminating the false positive from the legitimate retry scenario. The important lesson was that the login sequence and source history added information that the failure count could not provide by itself.

## Limitation to Keep in Mind

A successful login after repeated failures is not automatically harmless. An attacker might eventually guess the password or use credentials obtained another way.

That is why the suppression used here depends on both a known source and a successful follow-up login. In a production SOC, I would want stronger context such as device identity, account privilege, MFA status, geolocation, asset criticality, and historical login behavior before lowering severity.
