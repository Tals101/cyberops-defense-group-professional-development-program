# Ticket #011 - AWS Identity Investigation

Ticket: CYBEROPS-PDP-011

Engineer: Naftali Wodinsky

Report generated: 2026-11-02T19:48:33.6260615-05:00

Status: INITIAL AWS INVESTIGATION COMPLETE

Evidence classification: SYNTHETIC LABORATORY DATA

## 1. Scope and Method

This report evaluates twelve synthetic CloudTrail-style
events for the reporting service identity.

Sources:

- evidence/aws/cloudtrail-synthetic.jsonl
- evidence/aws/reference-context-synthetic.json
- evidence/aws/aws-investigation-timeline.csv

Original JSONL SHA256: 7F2CA74754DB29D78DBEE777F712BB74659D0A3FF895B77FF7114AF0A2CFAF78

Reference context SHA256: F13C716831E72CFFC9719B5A73B82C5A71FE34E40CB886DCD1DABE0E15059CA2

All event timestamps are UTC. Source IP addresses,
account identifiers, and credential identifiers are
fictional laboratory values.

The analysis does not use real AWS credentials or
establish that an actual organization was compromised.

## 2. Executive Finding

The modeled reporting identity uses the same synthetic
access-key identifier from an expected source and an
unfamiliar source.

Five events originate from 203.0.113.77, which is not
in the synthetic reference context's expected-source list.

During this sequence, the modeled API activity includes:

- Successful identity lookup.
- Successful bucket listing.
- One successful reporting-bucket GetObject request.
- One denied sensitive-bucket GetObject request.
- One denied attempt to assume ElevatedReportingRole.

This combination warrants investigation. It does not
identify the human or process responsible for the
requests, establish credential theft, or prove data
exfiltration.

## 3. Chronological Evidence Table

Time is shown as HH:MM:SS UTC on November 2, 2026.

| Time UTC | Event ID | Principal | Source IP | API | Outcome | Target |
|---|---|---|---|---|---|---|
| 12:40:00 | aws-0001 | svc-reporting-automation | 198.51.100.25 | GetCallerIdentity | SUCCESS | - |
| 12:40:20 | aws-0002 | svc-reporting-automation | 198.51.100.25 | ListBuckets | SUCCESS | - |
| 12:41:10 | aws-0003 | svc-reporting-automation | 198.51.100.25 | GetObject | SUCCESS | s3://synthetic-reporting-bucket/daily/report.csv |
| 13:05:41 | aws-0004 | svc-reporting-automation | 203.0.113.77 | GetCallerIdentity | SUCCESS | - |
| 13:06:09 | aws-0005 | svc-reporting-automation | 203.0.113.77 | ListBuckets | SUCCESS | - |
| 13:07:12 | aws-0006 | svc-reporting-automation | 203.0.113.77 | GetObject | SUCCESS | s3://synthetic-reporting-bucket/daily/report.csv |
| 13:07:55 | aws-0007 | svc-reporting-automation | 203.0.113.77 | GetObject | DENIED | s3://synthetic-sensitive-bucket/finance/private.csv |
| 13:08:33 | aws-0008 | svc-reporting-automation | 203.0.113.77 | AssumeRole | DENIED | role/ElevatedReportingRole |
| 13:09:04 | aws-0009 | analyst-admin | 203.0.113.88 | GetCallerIdentity | SUCCESS | - |
| 13:09:31 | aws-0010 | svc-backup-maintenance | 192.0.2.58 | GetObject | SUCCESS | s3://synthetic-backup-bucket/archive/checkpoint.json |
| 13:10:20 | aws-0011 | svc-reporting-automation | 198.51.100.25 | GetCallerIdentity | SUCCESS | - |
| 13:11:06 | aws-0012 | svc-reporting-automation | 198.51.100.25 | GetObject | SUCCESS | s3://synthetic-reporting-bucket/daily/report.csv |

The CSV timeline preserves complete event timestamps,
request identifiers, access-key identifiers, error
codes, and full target-resource identifiers.

## 4. Key Findings and Confidence

### F01 - Reporting Key Used From an Unfamiliar Source

Evidence: aws-0004 through aws-0008.

Observed: The modeled reporting key was used from
203.0.113.77 in five consecutive events.

Synthetic-baseline comparison: 198.51.100.25 is the
modeled expected reporting source.

Confidence in the recorded source difference: HIGH.

Confidence that the use was unauthorized: LOW.

Reason: No independent change approval, network egress
history, workload attribution, or credential-custody
evidence has been collected.

### F02 - Elevated Role Assumption Was Denied

Evidence: aws-0008.

Observed: AssumeRole targeting ElevatedReportingRole
has outcome DENIED and errorCode AccessDenied.

Confidence in this modeled request outcome: HIGH.

Confidence that no other role assumption succeeded: LOW.

Reason: One denied attempt cannot exclude successful
requests outside the dataset.

### F03 - S3 Reporting Object Request Succeeded

Evidence: aws-0006.

Observed: A GetObject event against the reporting
bucket has outcome SUCCESS.

Confidence in the modeled API outcome: HIGH.

Confidence that object bytes were actually received
and exfiltrated: NOT ESTABLISHED.

Additional object-access logs, relevant request and
response evidence, and destination context would be
needed to determine what data was transferred.

### F04 - Sensitive Object Request Was Denied

Evidence: aws-0007.

Observed: GetObject targeting synthetic-sensitive-bucket
was denied with AccessDenied.

Confidence in the modeled denial: HIGH.

The denial does not establish whether the same identity
accessed other sensitive objects.

### F05 - Unfamiliar IP Can Be Legitimate

Evidence: aws-0009 and synthetic reference context.

The model identifies analyst-admin at 203.0.113.88 as
an approved administrator under SYNTH-CHANGE-011-001.

Confidence that the synthetic context labels this
activity approved: HIGH.

Independent approval verification: NOT PERFORMED.

This is a deliberately modeled alternative to treating
every unfamiliar IP as malicious.

### F06 - Cross-System Relationship Unresolved

No Kubernetes or Linux evidence has yet been evaluated
in this AWS investigation.

Confidence in a connection to either system:
INSUFFICIENT EVIDENCE.

Timestamp proximity cannot establish causation.

## 5. Alternative Explanations

H-AWS-01: A compromised reporting credential was used
from an unauthorized execution environment.

Status: POSSIBLE; not established.

H-AWS-02: Authorized reporting automation used a
different network egress path or approved temporary host.

Status: POSSIBLE; approval records unavailable.

H-AWS-03: The role and sensitive-object requests reflect
configuration troubleshooting or an unauthorized
privilege-access attempt.

Status: INCONCLUSIVE; intent not established.

H-AWS-04: AWS events are unrelated to the Kubernetes
and Linux alerts.

Status: POSSIBLE; independent sources not yet analyzed.

## 6. Potential Impact

Modeled identity affected:
svc-reporting-automation.

Modeled access-key identifier:
SYNTH-KEY-REPORTING-01.

Potential reporting data exposure:
A reporting-bucket GetObject request succeeded.

Sensitive-data exposure:
The specifically modeled sensitive-object request
was denied; broader exposure remains unassessed.

Privilege escalation:
An elevated-role request was denied. No successful
role assumption appears in this twelve-event dataset.

Business impact:
Disabling the service identity could interrupt critical
financial-reporting operations.

Actual unauthorized access or exfiltration:
NOT ESTABLISHED.

## 7. Evidence Required Before Attribution

- Validate access-key inventory, ownership, and custody.
- Review credential distribution and rotation history.
- Verify approved source networks and change records.
- Check complete CloudTrail management and S3 data events.
- Investigate relevant request IDs and S3 object-access
  evidence, including data-transfer visibility.
- Review STS activity for all successful role sessions.
- Examine workload identity and credential mounting.
- Obtain Kubernetes audit and runtime process evidence.
- Obtain Linux SSH, process, and scheduled-task evidence.
- Compare cross-system identities and network paths.
- Confirm log coverage, clock synchronization, and
  retention windows.

## 8. Preliminary Disposition

AWS credential-use anomaly: SUPPORTED BY SYNTHETIC DATA.

Credential compromise: UNCONFIRMED.

Successful elevation: NOT OBSERVED IN THIS DATASET.

Sensitive-object access attempt: DENIED IN THIS DATASET.

Reporting-object API access: MODELED SUCCESS.

Data exfiltration: NOT ESTABLISHED.

AWS/Kubernetes/Linux causal relationship: UNDETERMINED.

Production containment: NOT AUTHORIZED BY THIS REPORT.

No destructive actions were taken.

## 9. Next Investigation Workstream

Investigate Kubernetes process activity, workload
identity, ServiceAccount privileges, outbound network
connections, and any supported credential-access path.

Preserve the AWS findings as an independent baseline.