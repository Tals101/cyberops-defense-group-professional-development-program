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
