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
