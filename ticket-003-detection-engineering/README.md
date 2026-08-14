# Ticket #003 - Suspicious Account Activity Detection Engineering

## Project Summary

This project focuses on a common SOC problem: failed logins are easy to see, but deciding which ones are actually worth investigating is much harder.

I built and tested an SSH authentication detector for a Linux host, starting with a simple threshold and then tuning it after a legitimate user scenario produced a false positive. The final lab version still catches the suspicious test activity, but it uses source familiarity and the authentication sequence to avoid treating every burst of password failures the same way.

## What the Detection Looks For

The detector watches SSH password failures and groups them by account and source IP. The base alert condition is:

- Same username
- Same source IP
- 5 or more failed SSH password attempts
- Within 120 seconds

That threshold is only the starting point. Version 2 also checks whether the source is already known for the account and whether a successful login follows the failures from that same source.

## Lab Environment

- Linux host: Ubuntu 24.04.4 LTS
- Hostname: `ubuntu-soc-lab`
- Authentication service: OpenSSH
- Authentication log: `/var/log/auth.log`
- Detector: Python 3
- Test account: `soc-test`
- Normal lab source: `192.168.56.1`
- Suspicious lab source: `192.168.56.111`

All activity in this repository was generated in an authorized lab.

## Why Two Versions Were Needed

### Version 1

The first version relied on count, source, account, and timing. It correctly alerted on five failed logins from the Kali system, but it also alerted when the legitimate Windows source produced five bad passwords and then logged in successfully.

### Version 2

The second version kept the original threshold and added two pieces of context:

- Is this source already expected for the account?
- Did the same user successfully authenticate from that source shortly after the failures?

In this lab, the high-priority alert is suppressed only when both conditions are true. A successful login by itself is not treated as proof that the activity is harmless.

## Test Results

| Scenario | Expected | Outcome |
|---|---|---|
| One legitimate password mistake | No alert | PASS |
| 5 suspicious failures in 67 seconds | Alert | PASS |
| Legitimate 5-failure sequence in Version 1 | No alert | FALSE POSITIVE |
| Same legitimate sequence in Version 2 | No alert | PASS |
| 4 failures | No alert | PASS |
| 5 failures | Alert | PASS |

## Main Takeaway

The threshold worked, but the testing showed why a threshold by itself is not enough. The most useful improvement came from looking at the surrounding login sequence instead of treating failed-password events in isolation.

## Repository Contents

- `Detection_Engineering_Report.md` - full investigation report
- `Detection_Engineering_Report.pdf` - PDF version of the report
- `engineering-notebook.md` - investigation notes from baseline through tuning
- `management-update.md` - concise management summary
- `lessons-learned.md` - reflection on the detection and tuning decisions
- `detection/scripts/` - Version 1, Version 2, and current detector
- `detection/rules/detection-logic.md` - platform-independent rule logic
- `detection/configs/known-sources.example.json` - sanitized lab configuration example
- `testing/` - baseline, positive, negative, false-positive, and boundary tests
- `evidence/` - raw logs, screenshots, and alert output
- `diagrams/detection-flow.mmd` - Mermaid detection flow

## Limitations

This is a lab proof of concept, not a production-ready control. The current implementation uses a static known-source mapping, reads one host's SSH authentication log, and can miss low-and-slow or distributed guessing attempts. A production version would need centralized telemetry, historical baselining, identity and device context, and testing against real alert volume.

## Repository Safety

The repository contains lab-only data. Passwords, credentials, tokens, private keys, and other secrets are not included and should never be committed.
