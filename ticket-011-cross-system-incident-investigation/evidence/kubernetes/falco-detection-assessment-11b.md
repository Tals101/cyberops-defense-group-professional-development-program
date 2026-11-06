# Ticket 011 - Falco Detection Engineering Assessment

Ticket: CYBEROPS-PDP-011
Prepared UTC: 2026-11-05T01:19:36.9801333+00:00

**Evidence classification: ACTUAL ISOLATED MINIKUBE LAB TESTS**

## Executive Assessment

Two Falco detection enhancements were validated
against their recorded positive and negative tests.

The source evidence inventory contains 35 verified
files. Original SHA256 hashes were checked.

These are actual isolated Minikube lab results.
They are separate from the 42 synthetic incident
events used by the cross-system correlation engine.

## Enhancement 1 - Unexpected Shell

Rule: Ticket011 Unexpected Shell In Reporting Image

Positive test: FALCO_CUSTOM_RULE_NONINTERACTIVE_SHELL
Outcome: DETECTED_AND_ATTRIBUTED

Candidate rule alerts: 1
Attributed events: 1

Negative test: CUSTOM_RULE_NEGATIVE_CONTROL
Outcome: PASS_NO_CUSTOM_RULE_ALERT
Negative candidate rule alerts: 0

Assessment:
The unexpected-shell detection was observed and
attributed for the tested noninteractive shell stimulus.

The recorded negative control produced no matching
custom-rule alert.

This does not establish coverage for every shell
execution technique or future software configuration.

## Enhancement 2 - ServiceAccount Token Access

Rule: Ticket011 Reporting ServiceAccount Token Access Attempt

Positive test: SERVICEACCOUNT_TOKEN_FAILED_OPEN
Outcome: DETECTED_AND_ATTRIBUTED_FAILED_OPEN

Candidate rule alerts: 1
Attributed events: 1

File-open result: ENOENT
Token contents read: False
Token automount enabled: False

Negative test: SERVICEACCOUNT_ACCESS_NEGATIVE_CONTROL
Outcome: PASS_NO_TOKEN_ACCESS_ALERT
Negative candidate rule alerts: 0

Assessment:
Falco detected the attempted token-path access
even though the file open failed.

No token contents were read in this test.
There is no evidence here of successful credential
theft, token exfiltration, or AWS key exposure.

The recorded negative control produced no matching
custom-rule alert.

## Detection Quality

Positive controls verified: 2
Negative controls verified: 2

The recorded sensor-stability checks passed,
and the observation windows were not truncated.

The negative controls establish only that these
specific benign stimuli did not generate matching
alerts during the recorded test windows.

They do not establish a statistical false-positive
rate or production-wide detection reliability.

## Residual Risks

1. Untested shell techniques may evade this rule.
2. Other credential files or access methods may
   fall outside the token-path detection.
3. A detected file-open attempt does not establish
   credential access or exfiltration.
4. Alert attribution depends on sensor availability
   and correct workload metadata.
5. The small test sample does not quantify noise
   during sustained production operations.
6. Kubernetes RBAC and container hardening remain
   essential preventive controls.
7. Live Minikube findings do not prove a connection
   among the synthetic AWS, Kubernetes, and Linux
   incident datasets.

## Recommended Follow-Up

- Expand benign control coverage.
- Add additional authorized adversarial variants.
- Test rule behavior across deployments and restarts.
- Measure alert volume over a representative period.
- Preserve rule version, Helm revision, and evidence
  identifiers with each future detection test.
- Review prevention and detection coverage separately.

## Disposition

Enhancement 1 recorded positive test: VERIFIED.
Enhancement 1 recorded negative test: VERIFIED.

Enhancement 2 recorded positive test: VERIFIED.
Enhancement 2 recorded negative test: VERIFIED.

Production detection coverage: NOT ESTABLISHED.
Cross-system causation: NOT ESTABLISHED.
Final Ticket 011 closure: PENDING.

No Kubernetes, Helm, Docker, AWS, or Linux
resources were modified by Step 11B.