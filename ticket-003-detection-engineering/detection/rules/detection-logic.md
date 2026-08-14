# SSH Repeated Authentication Failure Detection

## Core Condition

Group SSH authentication events by username and source IP, then evaluate the failures within a rolling time window.

Raise a suspicious-authentication alert when:

- The authentication result is failed.
- The username is the same.
- The source IP is the same.
- At least 5 failed password attempts occur.
- The attempts fall within 120 seconds.

Correlation should retain the timestamp, username, source IP, destination host, and authentication result.

## Context Used for Tuning

Before assigning high severity, consider what surrounds the failure burst:

- Is the source normally associated with the account?
- Does the same source successfully authenticate afterward?
- Is the account privileged?
- How important is the destination asset?
- Is the source attempting other accounts?
- Is similar activity appearing on other hosts?

## Version 2 Lab Behavior

In this lab, the high-priority alert is suppressed only when both conditions are met:

1. The source is already established as normal for the account.
2. The same account successfully logs in from that source within 60 seconds after the failures.

## Caveat

A successful login does not automatically make the preceding failures benign. A failure burst followed by success from an unusual source may represent successful credential guessing and should still be investigated.
