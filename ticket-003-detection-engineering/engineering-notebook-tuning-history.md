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
