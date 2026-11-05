# Ticket 011 - Cross-System Evidence Assessment

Ticket: CYBEROPS-PDP-011
Assessment UTC: 2026-11-05T01:02:53.1012307+00:00

**Classification: SYNTHETIC LABORATORY INVESTIGATION**

## Executive Finding

Seven synthetic source datasets contain 42 events
across AWS, Kubernetes, and Linux.

The correlation engine identified two shared-IP
groups and 37 cross-system event pairs within five
minutes of each other.

These are candidate associations, not 37 attacks
or 37 independently confirmed compromises.

Cross-system causation: **NOT ESTABLISHED**.

## Evidence Integrity

Seven original source files passed SHA-256 verification.
All 42 normalized events were matched to their
source event IDs, timestamps, files, and line numbers.

The Step 9C correlation engine passed 20 unit tests.

## Cross-System Address Associations

| IP address | Systems | Directional occurrences |
|---|---|---:|
| 203.0.113.77 | AWS, KUBERNETES, LINUX | 12 |
| 203.0.113.88 | AWS, LINUX | 2 |

Source and destination IP roles are preserved
in the association JSON. Equal IP strings do not
establish a common operator, credential,
network route, or execution environment.

## Complete Synthetic Timeline

All event timestamps use UTC on November 2, 2026.

| Timestamp UTC | System | Event reference | Action | Outcome |
|---|---|---|---|---|
| 2026-11-02T12:40:00Z | AWS | AWS_CLOUDTRAIL:aws-0001 | GetCallerIdentity | SUCCESS |
| 2026-11-02T12:40:20Z | AWS | AWS_CLOUDTRAIL:aws-0002 | ListBuckets | SUCCESS |
| 2026-11-02T12:41:10Z | AWS | AWS_CLOUDTRAIL:aws-0003 | GetObject | SUCCESS |
| 2026-11-02T12:50:00Z | LINUX | LINUX_AUTH:lin-0001 | ssh.accepted | SUCCESS |
| 2026-11-02T12:50:01Z | LINUX | LINUX_AUTH:lin-0002 | ssh.session_open | SUCCESS |
| 2026-11-02T12:50:12Z | LINUX | LINUX_PROCESS:lin-0010 | process.started | SUCCESS |
| 2026-11-02T12:50:21Z | LINUX | LINUX_NETWORK:lin-0016 | tcp.connect | ALLOWED |
| 2026-11-02T12:59:50Z | KUBERNETES | K8S_AUDIT:k8s-0001 | get | SUCCESS |
| 2026-11-02T13:00:05Z | KUBERNETES | K8S_FALCO:k8s-0002 | application_process | OBSERVED |
| 2026-11-02T13:01:00Z | KUBERNETES | K8S_NETWORK:k8s-0003 | outbound_connection | ALLOWED |
| 2026-11-02T13:03:10Z | LINUX | LINUX_AUTH:lin-0003 | ssh.failed_password | DENIED |
| 2026-11-02T13:03:17Z | LINUX | LINUX_AUTH:lin-0004 | ssh.failed_password | DENIED |
| 2026-11-02T13:04:02Z | LINUX | LINUX_AUTH:lin-0005 | ssh.accepted | SUCCESS |
| 2026-11-02T13:04:03Z | LINUX | LINUX_AUTH:lin-0006 | ssh.session_open | SUCCESS |
| 2026-11-02T13:04:15Z | KUBERNETES | K8S_AUDIT:k8s-0004 | create | SUCCESS |
| 2026-11-02T13:04:32Z | KUBERNETES | K8S_FALCO:k8s-0005 | shell_spawn | OBSERVED |
| 2026-11-02T13:04:52Z | KUBERNETES | K8S_FALCO:k8s-0006 | file_read | OBSERVED |
| 2026-11-02T13:05:09Z | KUBERNETES | K8S_NETWORK:k8s-0007 | outbound_connection | ALLOWED |
| 2026-11-02T13:05:41Z | AWS | AWS_CLOUDTRAIL:aws-0004 | GetCallerIdentity | SUCCESS |
| 2026-11-02T13:05:55Z | KUBERNETES | K8S_AUDIT:k8s-0008 | get | DENIED |
| 2026-11-02T13:05:59Z | LINUX | LINUX_PROCESS:lin-0011 | user_crontab.modified | SUCCESS |
| 2026-11-02T13:06:00Z | LINUX | LINUX_PROCESS:lin-0012 | file.metadata_changed | SUCCESS |
| 2026-11-02T13:06:09Z | AWS | AWS_CLOUDTRAIL:aws-0005 | ListBuckets | SUCCESS |
| 2026-11-02T13:06:20Z | KUBERNETES | K8S_AUDIT:k8s-0009 | patch | DENIED |
| 2026-11-02T13:06:25Z | LINUX | LINUX_AUTH:lin-0007 | sudo.authorization | DENIED |
| 2026-11-02T13:06:49Z | KUBERNETES | K8S_FALCO:k8s-0010 | process_exit | OBSERVED |
| 2026-11-02T13:07:00Z | LINUX | LINUX_PROCESS:lin-0013 | cron.job_started | SUCCESS |
| 2026-11-02T13:07:01Z | LINUX | LINUX_NETWORK:lin-0017 | tcp.connect | ALLOWED |
| 2026-11-02T13:07:02Z | LINUX | LINUX_PROCESS:lin-0014 | process.exited | SUCCESS |
| 2026-11-02T13:07:12Z | AWS | AWS_CLOUDTRAIL:aws-0006 | GetObject | SUCCESS |
| 2026-11-02T13:07:13Z | KUBERNETES | K8S_AUDIT:k8s-0011 | patch | DENIED |
| 2026-11-02T13:07:55Z | AWS | AWS_CLOUDTRAIL:aws-0007 | GetObject | DENIED |
| 2026-11-02T13:08:33Z | AWS | AWS_CLOUDTRAIL:aws-0008 | AssumeRole | DENIED |
| 2026-11-02T13:09:04Z | AWS | AWS_CLOUDTRAIL:aws-0009 | GetCallerIdentity | SUCCESS |
| 2026-11-02T13:09:15Z | LINUX | LINUX_AUTH:lin-0008 | ssh.accepted | SUCCESS |
| 2026-11-02T13:09:20Z | LINUX | LINUX_NETWORK:lin-0018 | tcp.connect | ALLOWED |
| 2026-11-02T13:09:31Z | AWS | AWS_CLOUDTRAIL:aws-0010 | GetObject | SUCCESS |
| 2026-11-02T13:09:31Z | KUBERNETES | K8S_AUDIT:k8s-0012 | get | SUCCESS |
| 2026-11-02T13:10:20Z | AWS | AWS_CLOUDTRAIL:aws-0011 | GetCallerIdentity | SUCCESS |
| 2026-11-02T13:10:30Z | LINUX | LINUX_PROCESS:lin-0015 | systemd_timer.inspected | SUCCESS |
| 2026-11-02T13:11:06Z | AWS | AWS_CLOUDTRAIL:aws-0012 | GetObject | SUCCESS |
| 2026-11-02T13:12:00Z | LINUX | LINUX_AUTH:lin-0009 | ssh.session_close | SUCCESS |

## Analytical Assessment

### AWS

The synthetic reporting identity was used from
an unfamiliar source. Reporting-object access
was modeled as successful, while sensitive-object
access and an elevated-role request were denied.

Credential compromise and data exfiltration
are not established.

### Kubernetes

Synthetic Kubernetes audit, runtime, and network
events provide suspicious workload activity and
candidate network relationships.

The separately performed live Minikube detection
tests are not part of this 42-event synthetic timeline.

### Linux

The synthetic Linux sequence includes unsuccessful
and successful SSH authentication, a crontab
modification, cron execution, and an outbound
connection with modeled process linkage.

Unauthorized access and malicious persistence
are not independently established.

## Incident Hypotheses

H01 - Related cross-system compromise: UNPROVEN.

H02 - AWS-only incident: NOT EXCLUDED.

H03 - Kubernetes-only incident: NOT EXCLUDED.

H04 - Linux-only incident: NOT EXCLUDED.

H05 - Benign or independent activity: NOT EXCLUDED.

The synthetic scenario demonstrates suspicious
sequences, but the datasets are not independent
corroboration of a real-world incident.

## Required 09:05 Containment Decision

Specified gate time: 09:05.

Gate date and timezone: NOT VERIFIED.

Documented authorization to execute
disruptive containment: NOT VERIFIED.

Containment execution status outside this
analysis: NOT ESTABLISHED.

Action performed by Step 9D: NONE.

Interim recommendation: HOLD disruptive
production containment pending authorized
incident-command review, service dependency
analysis, evidence preservation, and a rollback plan.

The 09:05 requirement must be reconciled with
its intended timezone and simulation timeline
before declaring the decision gate complete.

## Evidence Gaps

- Independent identity and credential attribution
- Source/destination network ownership and NAT mapping
- Process-to-network linkage across systems
- Verified clock synchronization
- Authorization and change records
- Object-transfer and exfiltration evidence
- Approved containment authority and recovery criteria

## Disposition

Synthetic event timeline: CONSOLIDATED.
Correlation candidates: DOCUMENTED.
Cross-system compromise: NOT ESTABLISHED.
Real-world compromise: NOT ESTABLISHED.
Final incident closure: PENDING.

No Kubernetes, Helm, AWS, or Linux system
changes were made by this assessment.