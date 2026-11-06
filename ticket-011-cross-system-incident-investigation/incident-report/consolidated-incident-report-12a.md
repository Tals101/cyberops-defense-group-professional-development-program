# Ticket 011 - Consolidated Incident Investigation Report

Ticket: CYBEROPS-PDP-011

Prepared UTC: 2026-11-05T17:34:00.6180357+00:00

**Classification: SYNTHETIC INCIDENT INVESTIGATION
WITH SEPARATELY IDENTIFIED ISOLATED-LAB TESTING**

## 1. Executive Summary

Ticket 011 investigated a synthetic scenario
spanning AWS, Kubernetes, and Linux.

Seven original evidence sources contain 42
synthetic events dated November 2, 2026 UTC.

The correlation engine identified two shared-IP
groups and 37 cross-system event pairs within
five-minute observation windows.

These results support candidate relationships,
not a confirmed coordinated intrusion.

**Cross-system causation: NOT ESTABLISHED.**

**Real-world compromise: NOT ESTABLISHED.**

The root cause and actual business impact
cannot be determined from the synthetic dataset.

## 2. Investigation Scope

Investigated systems:

- AWS identity and CloudTrail activity
- Kubernetes audit, Falco, and network activity
- Linux authentication, process, persistence,
  and network activity

The 42-event incident dataset is synthetic.

Separately, isolated Minikube exercises
validated Kubernetes permission boundaries,
container restrictions, and Falco detections.

These evidence categories must not be combined
as though they independently prove one incident.

## 3. Evidence Integrity

Original source files: 7 VERIFIED.

Normalized timeline events: 42 VERIFIED.

Correlation engine unit tests: 20 PASSED.

| Source | Records | SHA256 |
|---|---:|---|
| evidence/aws/cloudtrail-synthetic.jsonl | 12 | 7F2CA74754DB29D78DBEE777F712BB74659D0A3FF895B77FF7114AF0A2CFAF78 |
| evidence/kubernetes/kubernetes-audit-synthetic.jsonl | 6 | 227E4A4A9173635A12566AF5246F3167BDCD968DFD44C9DE6566B9E12DC2F91F |
| evidence/kubernetes/falco-runtime-synthetic.jsonl | 4 | BA61A3976213C45E97316C4E1D22FFD77C17678E4B812C8CE60DDE13A4B30760 |
| evidence/kubernetes/network-flow-synthetic.jsonl | 2 | B8EDA9594E2765A1479F900A8B383B352F3721C7D0B333F0C6DD342DFD6577CA |
| evidence/linux/linux-auth-synthetic.jsonl | 9 | 71B513E1ED147187C8396591C1782E8A4215F14D4C6753B82FDB6EA7D89F3AAD |
| evidence/linux/linux-process-persistence-synthetic.jsonl | 6 | CBBE9708903F19FF8BA8CC495BDBC0A15441CFD8CB92D58C899F6A7F9E40A1A3 |
| evidence/linux/linux-network-synthetic.jsonl | 3 | 5FFDA3A5C614C0E53C10B5BA33EBAF875BF4FC58F9685775184CDE67E14044C5 |

Each timeline row retains the source file,
source line, source hash, and event key.

Full chronological timeline:

incident-report/cross-system-timeline-9d.csv

Detailed correlation findings:

incident-report/cross-system-evidence-assessment-9d.md

## 4. Cross-System Correlation

Shared-IP groups: 2.

Five-minute event pairs: 37.

| Address | Systems | Directional occurrences |
|---|---|---:|
| 203.0.113.77 | AWS, KUBERNETES, LINUX | 12 |
| 203.0.113.88 | AWS, LINUX | 2 |

A common IP and close timestamps do not
establish a shared operator or causal chain.

Source and destination roles must be
preserved when evaluating each association.

The two addresses are modeled scenario
indicators, not verified production endpoints.

## 5. Chronology and System Findings

The original event times are UTC on
November 2, 2026.

### AWS

Synthetic records show use of a reporting
identity from an unfamiliar source address.

A reporting-object access was modeled
as successful. Other sensitive-access and
privilege-related requests were denied.

Credential theft is not established.

Successful GetObject access does not,
by itself, establish data exfiltration.

### Kubernetes

Synthetic audit and runtime events
describe suspicious workload activity.

Synthetic network records provide
candidate address associations.

These records do not prove that Kubernetes
activity caused AWS identity activity.

### Linux

The synthetic sequence includes failed
SSH authentications followed by a successful
authentication, scheduled-task modification,
cron execution, and outbound network activity.

The modeled cron execution has process-linked
network activity within the Linux dataset.

That internal linkage does not independently
establish authorization, malicious purpose,
or a cross-system operator.

### Timeline Limitations

The complete 42-event timeline is preserved
in the existing Step 9D CSV.

Clock synchronization, network ownership,
identity attribution, and independent
authorization records remain unverified.

## 6. Investigation Hypotheses

H01 - Related cross-system activity:
UNPROVEN.

H02 - AWS-only activity:
NOT EXCLUDED.

H03 - Kubernetes-only activity:
NOT EXCLUDED.

H04 - Linux-only activity:
NOT EXCLUDED.

H05 - Independent or benign activity:
NOT EXCLUDED.

Root cause: UNDETERMINED.

Real-world incident impact: NOT ESTABLISHED.

## 7. Isolated-Lab Security Validation

Eight provisional adversarial scenarios have
supporting technical evidence.

| Case | Evidence type | Recorded result |
|---|---|---|
| AT-01 | AUTHORIZATION_SIMULATION | AUTHORIZATION_DENIED_AS_EXPECTED |
| AT-02 | AUTHORIZATION_SIMULATION | AUTHORIZATION_DENIED_AS_EXPECTED |
| AT-03 | AUTHORIZATION_SIMULATION | AUTHORIZATION_DENIED_AS_EXPECTED |
| AT-04 | AUTHORIZATION_SIMULATION | AUTHORIZATION_DENIED_AS_EXPECTED |
| AT-05 | EXECUTED_RUNTIME_TEST | DETECTED_AND_ATTRIBUTED |
| AT-06 | EXECUTED_RUNTIME_TEST | DETECTED_AND_ATTRIBUTED |
| AT-07 | EXECUTED_RUNTIME_TEST | DETECTED_AND_ATTRIBUTED_FAILED_OPEN |
| AT-08 | EXECUTED_RUNTIME_TEST | PASS_UID0_ESCALATION_DENIED |

AT-01 through AT-04 are actual Kubernetes
authorization checks that returned the
expected denial decisions.

They did not execute the privileged actions
whose authorization was being tested.

AT-05 through AT-08 are four executed
runtime tests.

The token-file access test was detected,
but the open failed with ENOENT.

No token content was obtained.

The UID 0 escalation attempt was denied
with EPERM.

## 8. Falco Detection Engineering

Two Falco enhancements were validated in
the isolated Minikube lab:

1. Unexpected shell in reporting image
2. Reporting ServiceAccount token access attempt

Recorded positive controls: 2 PASSED.

Recorded negative controls: 2 PASSED.

These tests support detection only for
the recorded stimuli and observation windows.

Production-wide detection coverage and
statistical false-positive rates are
not established.

## 9. Containment Decision

Required decision gate: 09:05.

Gate date: NOT VERIFIED.

Gate timezone: NOT VERIFIED.

Authorized decision-maker: NOT VERIFIED.

Documented analyst recommendation:
HOLD DISRUPTIVE PRODUCTION CONTAINMENT
PENDING AUTHORIZED REVIEW.

Formal containment authorization: PENDING.

Actual containment by these documentation
steps: NONE.

The original 09:05 timed decision gate
cannot be declared satisfied.

## 10. Recovery

A recovery runbook and readiness assessment
were documented in Step 10B.

Recovery planning: COMPLETE.

Production recovery authorization:
NOT ESTABLISHED.

Production recovery execution:
NOT PERFORMED.

Post-recovery validation:
NOT PERFORMED.

Production recovery readiness:
NOT READY FOR PRODUCTION ACTION.

## 11. Outstanding Investigation Gaps

- Verify the authoritative acceptance rubric.
- Obtain formal adversarial test sign-off.
- Confirm the 09:05 date and timezone.
- Identify containment decision authority.
- Establish independent credential attribution.
- Determine network and endpoint ownership.
- Verify legitimate scheduled-task ownership.
- Obtain independent exfiltration evidence.
- Assess service dependencies and recovery.
- Obtain documented closure approval.

## 12. Disposition

Technical investigation documentation:
CONSOLIDATED.

Synthetic event integrity: VERIFIED.

Cross-system attack causation:
NOT ESTABLISHED.

Real-world breach: NOT ESTABLISHED.

Formal acceptance: PENDING.

Containment stop gate: PENDING.

Production recovery: NOT PERFORMED.

**FINAL TICKET CLOSURE: PENDING.**

No Kubernetes, Helm, AWS, Docker, or Linux
resources were changed by Step 12A.