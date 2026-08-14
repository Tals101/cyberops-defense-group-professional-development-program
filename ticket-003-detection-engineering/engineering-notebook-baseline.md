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
