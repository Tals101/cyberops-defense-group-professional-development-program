# Ticket 012 - Evidence Inventory

## Evidence Collection Information

Collection Date: 2026-11-10
Time Zone: America/New_York (UTC-05:00)
Environment: Local Minikube Kubernetes Laboratory
Investigation: TICKET-012

## Collected Baseline Evidence

| ID | Evidence File | Description |
|----|---------------|-------------|
| E001 | initial-namespaces.txt | Kubernetes namespace inventory |
| E002 | initial-nodes.txt | Kubernetes node information |
| E003 | initial-pods.txt | Existing Kubernetes workloads |
| E004 | initial-deployments.txt | Deployment inventory |
| E005 | initial-services.txt | Kubernetes service inventory |
| E006 | initial-events.txt | Available Kubernetes events |
| E007 | baseline-timestamp.txt | Evidence collection timestamp |

## Evidence Location

07-Evidence/supporting-outputs/

## Evidence Integrity

SHA-256 hashes recorded in:
07-Evidence/SHA256SUMS.txt

Original evidence files should remain unchanged.

## Missing Incident Evidence

- Original suspicious outbound connection logs
- Service identity authentication records
- Internal resource access logs
- Original CI/CD deployment logs
- Application configuration before and after deployment
- Original SOC alert details
- Confirmed incident timestamps and time zone

## Evidence Limitations

The collected baseline describes the local laboratory,
not the original reported corporate incident.

The reported incident has not been independently verified.

Missing logs limit our ability to determine root cause,
attribute identity activity, and confirm compromise.

## Evidence Preservation Status

Initial local baseline collected and hashed.
Original incident evidence remains unavailable.
Investigation remains open.

## Additional Evidence

| ID | Evidence File | Description |
|----|---------------|-------------|
| E008 | integrity-verification.txt | Successful SHA-256 verification of seven original evidence files |

## Integrity Verification Result

Seven original evidence files passed SHA-256 verification.
The verification output was saved and its hash added to SHA256SUMS.txt.

## Internal Service Security Testing

Evidence ID: E009
Evidence File: internal-service-test-logs.txt
Evidence Location: 07-Evidence/supporting-outputs/

### Test Results
- Health endpoint returned HTTP 200.
- Authorized resource request returned HTTP 200.
- Invalid authentication token returned HTTP 403.

### Assessment
The internal service accepted the configured synthetic
credentials and rejected the tested incorrect token.

These tests do not establish comprehensive authentication
security or independently verify caller identity.

### Evidence Notes
- Logs contain UTC timestamps.
- Docker client output includes a PowerShell error-stream
  formatting artifact.
- Original log file preserved without modification.

## Kubernetes Application Communication Evidence

Evidence ID: E010
Evidence File: kubernetes-internal-service-logs.txt
Description: Internal service logs showing health checks and resource access.

Evidence ID: E011
Evidence File: kubernetes-application-api-logs.txt
Description: Application API logs showing successful internal communication.

## Verified Observations

- Both Kubernetes workloads were Running and Ready.
- Application API contacted the internal service.
- The internal service returned HTTP 200.
- The application API recorded HTTP 200.
- Both applications recorded matching request times.
- All activity was performed in the simulated laboratory.

## Investigation Assessment

Authorized laboratory communication was demonstrated.
This establishes a baseline for later comparisons with
suspicious or policy-violating activity.

No compromise has been established.

## Pre-Incident Laboratory Configuration

Evidence ID: E012
Evidence File: prechange-deployments.yaml
Evidence Location: 07-Evidence/supporting-outputs/

### Description
Snapshot of the application-api and internal-service
Kubernetes deployment configurations before introducing
the simulated suspicious activity.

### Purpose
- Preserve the original deployment configuration.
- Support comparison with modified deployments.
- Provide evidence for rollback and recovery.
- Establish a configuration baseline.

### Integrity
SHA-256 hash recorded in SHA256SUMS.txt.

### Status
Original configuration snapshot preserved.
No simulated suspicious changes introduced yet.

## Collector Pre-Incident Logs

Evidence ID: E013
Evidence File: collector-preincident-logs.txt
Evidence Location: 07-Evidence/supporting-outputs/

### Description
Timestamped Kubernetes logs collected from the
unapproved-collector deployment before executing
the simulated suspicious resource request.

### Observations
- Normal /health requests recorded.
- HTTP 200 responses observed.
- Source IP addresses recorded.
- Claimed identity fields recorded.
- Routine health checks are not evidence of compromise.

### Purpose
- Establish pre-incident activity.
- Distinguish normal health checks from suspicious requests.
- Support timeline reconstruction.
- Provide baseline telemetry for detection testing.

### Integrity
SHA-256 hash recorded in SHA256SUMS.txt.

### Status
Pre-incident log snapshot preserved.
Simulated suspicious resource traffic not yet executed.

## Collector Incident Logs

Evidence ID: E014
Evidence File: collector-incident-logs.txt
Evidence Location: 07-Evidence/supporting-outputs/

### Description
Timestamped Kubernetes logs from the unapproved-collector
deployment following the controlled incident simulation.

### Observations
- Incident request timestamp: 2026-11-12T18:14:40.669127661Z
- Destination: unapproved-collector
- Request path: /resource
- HTTP status: 200
- Claimed identity: application-api
- Source IP: 10.244.1.170
- Policy label: unapproved

### Analysis
The logs confirm that a simulated resource request reached
the unapproved collector.

The claimed identity is supplied by an HTTP request header
and is not independently authenticated by the collector.

This was an authorized laboratory simulation.
The evidence does not establish a real compromise.

### Purpose
- Document unexpected service communication.
- Support incident timeline reconstruction.
- Provide telemetry for correlation detection.
- Support future containment and recovery testing.

### Integrity
SHA-256 hash recorded in SHA256SUMS.txt.

### Status
Incident evidence preserved.
Controlled suspicious resource request confirmed.

## Incident Application Deployment Configuration

Evidence ID: E015
Evidence File: incident-application-deployment.yaml
Evidence Location: 07-Evidence/supporting-outputs/

### Description
Kubernetes deployment configuration captured after
the controlled incident simulation was introduced.

### Observations
- Deployment: application-api
- Namespace: ticket-012-lab
- Configuration variable: INTERNAL_URL
- Modified destination: http://unapproved-collector:8080/resource
- Original destination: http://internal-service:8080/resource

### Analysis
The deployment configuration confirms that application-api
was redirected to an unapproved internal destination.

The change was deliberately introduced as part of an
authorized laboratory security simulation.

This evidence establishes the modified configuration,
but does not establish malicious intent.

### Purpose
- Document the simulated configuration change.
- Correlate deployment changes with network activity.
- Support comparison with the pre-incident baseline.
- Support containment and recovery validation.

### Integrity
SHA-256 hash recorded in SHA256SUMS.txt.

### Status
Modified deployment configuration preserved.
Approved configuration not yet restored.

## Incident Kubernetes Events

Evidence ID: E016
Evidence File: incident-kubernetes-events.txt
Evidence Location: 07-Evidence/supporting-outputs/

### Description
Kubernetes events captured after the simulated
application deployment configuration change.

### Observations
- New application-api ReplicaSet created.
- New application-api pod started successfully.
- Previous application-api pod terminated.
- Kubernetes deployment scaling events recorded.
- Readiness probe warning observed on previous pod.

### Analysis
The events support reconstruction of the application
deployment rollout during the simulated incident.

The readiness probe warning requires contextual review
and does not independently establish compromise.

Event ages are relative and should be correlated with
timestamped logs and deployment evidence.

### Purpose
- Document Kubernetes rollout activity.
- Support incident timeline reconstruction.
- Correlate deployment changes with application traffic.
- Support investigation of deployment health.

### Integrity
SHA-256 hash recorded in SHA256SUMS.txt.

### Status
Incident Kubernetes events preserved.
Approved application configuration not yet restored.

## Application API Incident Logs

Evidence ID: E017
Evidence File: application-api-incident-logs.txt
Evidence Location: 07-Evidence/supporting-outputs/

### Description
Timestamped Kubernetes logs collected from application-api
after executing the controlled incident simulation.

### Observations
- Request path: /call-internal
- Request timestamp: 2026-11-12T18:14:40.669445480Z
- HTTP status: 200
- Collector request timestamp: 2026-11-12T18:14:40.669127661Z
- Collector request path: /resource

### Analysis
The application and collector logs contain closely
correlated timestamps and successful HTTP responses.

Together with the modified deployment configuration,
these observations support the conclusion that the
application contacted the unapproved collector.

The activity was deliberately generated in an
authorized laboratory simulation and does not
establish a real security compromise.

### Purpose
- Preserve application-side incident telemetry.
- Correlate sending and receiving service activity.
- Support incident timeline reconstruction.
- Provide evidence for detection engineering.
- Support containment and recovery validation.

### Integrity
SHA-256 hash recorded in SHA256SUMS.txt.

### Status
Application incident logs preserved.
Approved application configuration not yet restored.

## Application Destination Allowlist Negative Test

Evidence ID: E018
Evidence File: allowlist-negative-retest-rejection.txt
Evidence Location: 07-Evidence/supporting-outputs/

### Description
Timestamped application security event captured during
the repeated destination allowlist negative test.

### Observations
- Test date: 2026-11-15
- Rejection timestamp: 2026-11-15T15:26:16.360869261Z
- Application: application-api
- Event: destination_allowlist_rejection
- Rejected destination: http://unapproved-collector:8080/resource
- HTTP response: 403 Forbidden

### Analysis
The application rejected the configured unapproved
destination before issuing its normal internal request.

The test demonstrates application-level destination
validation for the /call-internal request path.

This control does not establish network-level isolation
or prevent independent connections from the container.

### Evidence Limitation
An earlier log collection contained only later health
checks and did not preserve the original rejection event.
This subsequent test captured a fresh rejection event.

### Integrity
SHA-256 hash recorded in SHA256SUMS.txt.

### Status
Negative security test passed.
Rejection evidence preserved.
Approved application configuration not yet restored.
