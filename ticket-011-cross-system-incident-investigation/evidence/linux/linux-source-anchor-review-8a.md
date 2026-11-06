# Ticket 011 - Linux Investigation Source Review

Ticket: CYBEROPS-PDP-011
Review UTC: 2026-11-03T18:49:33.4380907+00:00

## Scope

Investigate possible Linux authentication,
execution, and persistence activity in relation
to the existing synthetic AWS and Kubernetes
incident scenarios.

## Initial Linux Evidence Status

NO_LINUX_EVENT_DATASET_PRESENT

Existing non-placeholder Linux files:
0

## Source Integrity

- evidence\aws\aws-investigation-timeline.csv : 4900A2274D355AFF8D6D5174B375D5DB48B943F8A8046B17EDABE31FD78E574F
- evidence\aws\DATASET-PROVENANCE.md : 06948D459096B4C52496529530F609414E7CBC2631168EE267D97A308D722899
- evidence\aws\reference-context-synthetic.json : F13C716831E72CFFC9719B5A73B82C5A71FE34E40CB886DCD1DABE0E15059CA2
- evidence\kubernetes\DATASET-PROVENANCE.md : D117C0F425DD0DAD9EFE7D54058CDE00F0847E47A2D3470CC67DC0CAF2D5336E
- incident-report\hypothesis-register.md : DB4AF063DBF66E79BE8D63002661AD897A05559F5AE844609633B3FCBF0E2DE5
- incident-report\aws-identity-investigation.md : EA34A383012E8F71EBC62541D0ED4AA793170D5FDE840E1252291D125BE948BC

## Proposed Linux Investigation Coverage

1. Successful and failed SSH authentication
2. User and privilege changes
3. Suspicious process execution
4. Cron or systemd persistence indicators
5. Outbound network activity
6. Host and user identity attribution
7. Evidence integrity and timestamp consistency

## Evidence Provenance Rules

Any newly generated Linux incident records
must be explicitly marked SYNTHETIC.

They must not be represented as actual
authentication logs or observations from
the user's Linux hosts.

Source timestamps and event identifiers
must be preserved when analyzing existing data.

A shared IP address or adjacent timestamp
does not establish a common attacker.

The Kubernetes ServiceAccount token is
not automatically an AWS credential.

Any cross-system causal claim requires
independent evidence of identity, access,
or process/network linkage.

## Containment Boundary

The 09:05 containment stop gate is an
investigation requirement. Its actual
decision and execution status remain
subject to separate verification.

No live Linux system is accessed in this step.
No persistence mechanism is installed.
No production, AWS, or Kubernetes resources
are modified.

## Source Documents Reviewed

========== evidence\aws\aws-investigation-timeline.csv ==========

SHA256: 4900A2274D355AFF8D6D5174B375D5DB48B943F8A8046B17EDABE31FD78E574F

"TimestampUTC","EventID","RequestID","SourceSystem","Principal","AccessKeyIdentifier","SourceIP","EventName","TargetResource","Outcome","ErrorCode","AnalystFlag"
"2026-11-02T12:40:00Z","aws-0001","synthetic-request-0001","aws-cloudtrail-synthetic","svc-reporting-automation","SYNTH-KEY-REPORTING-01","198.51.100.25","GetCallerIdentity",,"SUCCESS",,"NONE"
"2026-11-02T12:40:20Z","aws-0002","synthetic-request-0002","aws-cloudtrail-synthetic","svc-reporting-automation","SYNTH-KEY-REPORTING-01","198.51.100.25","ListBuckets",,"SUCCESS",,"NONE"
"2026-11-02T12:41:10Z","aws-0003","synthetic-request-0003","aws-cloudtrail-synthetic","svc-reporting-automation","SYNTH-KEY-REPORTING-01","198.51.100.25","GetObject","arn:aws:s3:::synthetic-reporting-bucket/daily/report.csv","SUCCESS",,"NONE"
"2026-11-02T13:05:41Z","aws-0004","synthetic-request-0004","aws-cloudtrail-synthetic","svc-reporting-automation","SYNTH-KEY-REPORTING-01","203.0.113.77","GetCallerIdentity",,"SUCCESS",,"UNFAMILIAR_SOURCE_PER_SYNTHETIC_BASELINE"
"2026-11-02T13:06:09Z","aws-0005","synthetic-request-0005","aws-cloudtrail-synthetic","svc-reporting-automation","SYNTH-KEY-REPORTING-01","203.0.113.77","ListBuckets",,"SUCCESS",,"UNFAMILIAR_SOURCE_PER_SYNTHETIC_BASELINE"
"2026-11-02T13:07:12Z","aws-0006","synthetic-request-0006","aws-cloudtrail-synthetic","svc-reporting-automation","SYNTH-KEY-REPORTING-01","203.0.113.77","GetObject","arn:aws:s3:::synthetic-reporting-bucket/daily/report.csv","SUCCESS",,"UNFAMILIAR_SOURCE_PER_SYNTHETIC_BASELINE"
"2026-11-02T13:07:55Z","aws-0007","synthetic-request-0007","aws-cloudtrail-synthetic","svc-reporting-automation","SYNTH-KEY-REPORTING-01","203.0.113.77","GetObject","arn:aws:s3:::synthetic-sensitive-bucket/finance/private.csv","DENIED","AccessDenied","UNFAMILIAR_SOURCE_PER_SYNTHETIC_BASELINE"
"2026-11-02T13:08:33Z","aws-0008","synthetic-request-0008","aws-cloudtrail-synthetic","svc-reporting-automation","SYNTH-KEY-REPORTING-01","203.0.113.77","AssumeRole","arn:aws:iam::111122223333:role/ElevatedReportingRole","DENIED","AccessDenied","UNFAMILIAR_SOURCE_PER_SYNTHETIC_BASELINE"
"2026-11-02T13:09:04Z","aws-0009","synthetic-request-0009","aws-cloudtrail-synthetic","analyst-admin","SYNTH-KEY-ADMIN-01","203.0.113.88","GetCallerIdentity",,"SUCCESS",,"APPROVED_PER_SYNTHETIC_REFERENCE"
"2026-11-02T13:09:31Z","aws-0010","synthetic-request-0010","aws-cloudtrail-synthetic","svc-backup-maintenance","SYNTH-KEY-BACKUP-01","192.0.2.58","GetObject","arn:aws:s3:::synthetic-backup-bucket/archive/checkpoint.json","SUCCESS",,"NONE"
"2026-11-02T13:10:20Z","aws-0011","synthetic-request-0011","aws-cloudtrail-synthetic","svc-reporting-automation","SYNTH-KEY-REPORTING-01","198.51.100.25","GetCallerIdentity",,"SUCCESS",,"NONE"
"2026-11-02T13:11:06Z","aws-0012","synthetic-request-0012","aws-cloudtrail-synthetic","svc-reporting-automation","SYNTH-KEY-REPORTING-01","198.51.100.25","GetObject","arn:aws:s3:::synthetic-reporting-bucket/daily/report.csv","SUCCESS",,"NONE"


========== evidence\aws\DATASET-PROVENANCE.md ==========

SHA256: 06948D459096B4C52496529530F609414E7CBC2631168EE267D97A308D722899

# AWS Dataset Provenance - Ticket 011

## Classification

SYNTHETIC LABORATORY EVIDENCE

These records are generated for an authorized training
scenario. They are not exports from a real AWS account.

## Time Reference

The simulated incident date is November 2, 2026.

All eventTime fields are UTC.

The records contain routine activity before and during
the suspicious-activity window.

## Source Data

- cloudtrail-synthetic.jsonl
- reference-context-synthetic.json

## Design

Twelve synthetic API activity records include:

- Expected reporting automation
- Reporting credentials used from an unfamiliar IP
- Successful reporting-bucket access
- Denied sensitive-bucket access
- Denied elevated-role assumption
- Approved administrator activity from another IP
- Routine backup operations
- Simultaneous authorized reporting operations

## Analysis Limitations

The record set contains intentionally modeled outcomes.

It does not establish a real breach, prove data
exfiltration, or demonstrate a Kubernetes-to-AWS or
Linux-to-AWS connection.

CloudTrail-style GetObject success is an indication
of an allowed API request in this simulation. Actual
object content transfer would require additional
evidence.

The synthetic reference context is provided for
training evaluation. It is not independently verified
business authorization evidence.

Do not infer causation solely from event timestamps.

No real AWS API calls or account changes were made.

========== evidence\aws\reference-context-synthetic.json ==========

SHA256: F13C716831E72CFFC9719B5A73B82C5A71FE34E40CB886DCD1DABE0E15059CA2

{
    "datasetType":  "SYNTHETIC",
    "incidentDate":  "2026-11-02",
    "timestampTimezone":  "UTC",
    "awsAccount":  "111122223333",
    "sourceIpNote":  "All IP addresses use documentation-only ranges.",
    "reportingIdentity":  {
                              "principal":  "svc-reporting-automation",
                              "accessKeyIdentifier":  "SYNTH-KEY-REPORTING-01",
                              "expectedSourceIps":  [
                                                        "198.51.100.25"
                                                    ],
                              "unfamiliarSourceIp":  "203.0.113.77",
                              "approvedReportingBucket":  "synthetic-reporting-bucket",
                              "normalOperations":  [
                                                       "GetCallerIdentity",
                                                       "ListBuckets",
                                                       "GetObject"
                                                   ]
                          },
    "legitimateAdministrator":  {
                                    "principal":  "analyst-admin",
                                    "sourceIp":  "203.0.113.88",
                                    "approvalReference":  "SYNTH-CHANGE-011-001",
                                    "note":  "Approved temporary administrative access."
                                },
    "routineBackupIdentity":  {
                                  "principal":  "svc-backup-maintenance",
                                  "sourceIp":  "192.0.2.58",
                                  "bucket":  "synthetic-backup-bucket"
                              },
    "limitations":  [
                        "Reference context is synthetic, not independent production evidence.",
                        "A successful API call does not alone prove which bytes were received.",
                        "The outcome of one AssumeRole attempt does not establish all possible role activity.",
                        "AWS events alone cannot establish Kubernetes or Linux causation."
                    ]
}

========== evidence\kubernetes\DATASET-PROVENANCE.md ==========

SHA256: D117C0F425DD0DAD9EFE7D54058CDE00F0847E47A2D3470CC67DC0CAF2D5336E

# Kubernetes Evidence Provenance - Ticket 011

## Classification

SYNTHETIC LABORATORY EVIDENCE

These are modeled Kubernetes audit, Falco-style
runtime, and network-flow records.

They are not exports from a production cluster
or observations collected from a running Pod.

## Scenario

A reporting-api Pod in the simulated
production-reporting namespace exhibits:

- Routine application and network activity
- A successful Kubernetes exec API operation
- An unexpected shell process
- A read of the Kubernetes ServiceAccount token file
- A connection to an unfamiliar external destination
- A denied Kubernetes Secret request
- A denied ephemeral-container modification
- A denied Deployment modification
- Later administrative workload inspection

## Relationship to AWS Evidence

The external address 203.0.113.77 appears as a
Kubernetes outbound destination in this dataset.

The same address appears as an AWS API source
in the separately generated AWS dataset.

This is a possible investigative association.
It is NOT proof of shared origin, credential theft,
a common operator, or causal linkage.

NAT mapping, destination attribution, process-to-
network attribution, AWS credential access evidence,
and independent infrastructure records are absent.

The modeled ServiceAccount token is a Kubernetes
identity credential, not an AWS access key.

## Evidence Limitations

All timestamps are UTC on November 2, 2026.

The synthetic workload context is a modeled snapshot,
not an authoritative live RBAC inspection.

A successful exec API operation does not prove who
spawned every subsequent process.

A token-file read does not prove successful token
exfiltration or AWS credential exposure.

An allowed network connection does not establish
its content, intent, or successful data transfer.

Denied workload modifications do not rule out
persistence mechanisms outside the modeled events.

No real cluster resources were created, changed,
deleted, or queried to generate these records.

========== incident-report\hypothesis-register.md ==========

SHA256: DB4AF063DBF66E79BE8D63002661AD897A05559F5AE844609633B3FCBF0E2DE5

# Ticket #011 - Initial Incident Hypothesis Register

All hypotheses below are UNTESTED.

## H01 - Related Cross-System Compromise

A shared identity or access path could explain
AWS, Kubernetes, and Linux activity.

Status: UNTESTED

Required evidence:
Credential identity, network path, source attribution,
and independent cross-system corroboration.

## H02 - AWS Incident Only

AWS credential use may be unauthorized while
Kubernetes and Linux events are independent.

Status: UNTESTED

Required evidence:
AWS identity, authorization, role-assumption outcome,
and legitimate-use comparison.

## H03 - Kubernetes Incident Only

Runtime activity may represent an isolated
workload compromise unrelated to AWS or Linux.

Status: UNTESTED

Required evidence:
Process ancestry, Pod identity, credential access,
network destination, and audit events.

## H04 - Linux Incident Only

SSH activity and scheduled-task creation may
indicate unauthorized host access and persistence.

Status: UNTESTED

Required evidence:
Authentication identities, source attribution,
scheduled-task content, and process history.

## H05 - Benign or Partially Coincidental Activity

Some or all alerts may reflect legitimate operations
or independent events occurring close together.

Status: UNTESTED

Required evidence:
Approved automation schedules, administrator activity,
source-IP ownership, and business context.

## Decision Rule

Timestamp proximity alone does not establish causation.

Each hypothesis must be supported, contradicted, or
left inconclusive using preserved evidence.

Initial incident disposition: UNDETERMINED.


========== incident-report\aws-identity-investigation.md ==========

SHA256: EA34A383012E8F71EBC62541D0ED4AA793170D5FDE840E1252291D125BE948BC

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

## Next Step

Construct a bounded synthetic Linux event dataset
only after reviewing the source timelines.

Then assess authentication, persistence,
and possible cross-system relationships,
recording alternative explanations and gaps.