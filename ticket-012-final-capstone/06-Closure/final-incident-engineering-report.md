# TICKET 012 - FINAL INCIDENT ENGINEERING REPORT

Report Date: 2026-11-17
Incident ID: TICKET-012
Environment: Isolated Minikube Kubernetes laboratory
Namespace: ticket-012-lab
Incident Classification: Simulated multi-stage security incident
Initial Severity: High (provisional)
Production Readiness: NO-GO
Incident Closure Authorization: NOT GRANTED

---

## 1. Executive Summary

Ticket 012 investigated a simulated Kubernetes security incident
involving unexpected outbound communication, workload identity,
deployment configuration, and potential weaknesses in security
controls.

The laboratory reproduced an application contacting an
unapproved internal collector after a deployment configuration
change.

The investigation preserved Kubernetes configuration, workload
logs, operational observations, and detection evidence.

Detection engineering produced two correlation detector versions,
51 passing automated tests, and eight synthetic adversarial and
resilience validation exercises.

Operational testing demonstrated successful workload containment,
laboratory restoration, failed deployment reproduction, and
corrective rollback.

However, network-level isolation remains ineffective in the
tested Minikube configuration.

Consequently, complete security recovery has not been established.

## 2. Incident Background

The simulated scenario involved three Kubernetes workloads:

1. application-api
2. internal-service
3. unapproved-collector

Normal application communication was intended to reach
internal-service.

During the incident simulation, the application was configured
to contact unapproved-collector instead.

The collector received synthetic laboratory traffic.

No real-world compromise, malicious actor, sensitive-data
exfiltration, or production incident was demonstrated.

## 3. Investigation and Evidence Preservation

The investigation preserved:

- Initial cluster and namespace observations
- Workload and deployment configurations
- Kubernetes events and application logs
- Pre-change deployment snapshots
- Incident-stage network and collector evidence
- Detection datasets and automated test results
- Operational security-control observations
- Containment, rollback, and recovery evidence

Available evidence was retained in the Ticket 012 project.

Evidence integrity tracking uses the project's SHA256 records.

New evidence generated during later validation must also be
included in the final integrity review before packaging.

## 4. Competing Explanations

Two alternative explanations were considered:

### Explanation A - Unauthorized configuration change

A deployment change redirected application communication to
a destination outside the expected service allowlist.

This explanation is consistent with the simulated unexpected
network destination and deployment timing.

### Explanation B - Authorized test or operational activity

A diagnostic action or legitimate configuration change may
produce similar network and identity observations.

Some synthetic benign scenarios intentionally model
authorized exceptions that are absent from the static allowlist.

Deployment timing and claimed identity alone cannot reliably
establish intent or authorization.

### Assessment

The laboratory demonstrates suspicious conditions requiring
investigation, not independent proof of malicious intent.

## 5. Detection Engineering

Version 1 correlated:

- Network destination classification
- Workload identity comparison
- Deployment-change timing

Version 2 independently flagged unapproved destinations,
identity mismatches, and unknown workloads.

Deployment timing was retained as a supporting indicator
and investigation-priority modifier.

Neither detector independently authenticates claimed identity.

### Automated Testing

Total automated tests: 51
Passed: 51
Failed: 0
CLI error handling: 11 additional tests passed

Tests addressed benign cases, suspicious activity,
missing fields, malformed timestamps, duplicate records,
identity classification, and correlation boundaries.

### Synthetic Evaluation

24 labeled synthetic scenarios:
12 benign and 12 suspicious.

| Metric | Baseline | Version 1 | Version 2 |
|---|---:|---:|---:|
| True Positives | 10 | 5 | 12 |
| False Positives | 3 | 1 | 5 |
| False Negatives | 2 | 7 | 0 |
| Precision | 76.9% | 83.3% | 70.6% |
| Recall | 83.3% | 41.7% | 100.0% |

Version 2 improved recall on the constructed dataset,
but increased false-positive volume.

These measurements cannot be generalized to production.

## 6. Adversarial and Resilience Validation

Eight synthetic detector-level exercises were executed.

Behavioral checks passed: 8 of 8.

Test themes included:

- True-positive correlation
- Benign identity lookalike
- Clock skew
- Identity ambiguity
- Configuration change
- Missing deployment telemetry
- Simulated policy bypass
- Simulated rollback failure

One benign identity lookalike was classified as a
false positive despite passing its behavioral check.

The simulated policy-bypass and rollback scenarios
were supplemented by separate operational Kubernetes tests.

## 7. Security Controls

### Application Destination Allowlist

The application-level allowlist restricted the protected
application call path to the approved internal service.

This did not prevent arbitrary code executing in the
container from opening a direct network connection.

### Workload Service-Account Hardening

The application used a dedicated Kubernetes service account.

Testing confirmed that its Kubernetes service-account
token was not automatically mounted.

This reduces exposure of automatically mounted
Kubernetes API credentials.

### NetworkPolicy Enforcement

The active Minikube configuration used a bridge CNI
with portmap and firewall plugins.

A temporary deny-all egress NetworkPolicy was applied
to the application workload.

The application could still connect to the
unapproved collector.

Result: NetworkPolicy enforcement test failed.

Network-level isolation remains an open security finding.

## 8. Operational Containment and Recovery

The unapproved collector was temporarily scaled to
zero replicas.

During containment:

- Collector connectivity became unavailable.
- Approved application communication remained functional.

The collector was subsequently restored to one ready replica.

A separate disposable rollback workload was used
to reproduce a failed deployment.

An invalid image produced ImagePullBackOff while the
existing healthy replica remained available.

A rollback to nonexistent revision 999 was rejected.

A valid rollback restored the working image and one
ready replica.

The disposable workload was then deleted.

All three original laboratory deployments were verified
at one ready replica each.

## 9. Root Cause and Contributing Factors

### Simulated Incident Trigger

The incident scenario was initiated by changing the
application's configured destination to an unapproved
internal collector.

### Confirmed Control Gap

Application-level destination checking did not provide
container-wide outbound network enforcement.

### Additional Detection Limitations

- Version 1 depended excessively on deployment timing.
- Version 2 produced false positives from identity metadata
  and authorized exceptions.
- Claimed identity was not independently authenticated.
- Missing telemetry limited correlation certainty.
- The synthetic evaluation dataset was small.

## 10. Recommendations

Priority 1:
Implement and validate network-level egress restrictions
using a NetworkPolicy-enforcing networking implementation.

Priority 2:
Retest approved communication and unauthorized destinations
under actual network enforcement.

Priority 3:
Introduce independently verified authorization evidence
for exceptions and workload identities.

Priority 4:
Improve alert prioritization without suppressing
unapproved-destination findings.

Priority 5:
Maintain deployment rollback instructions, known-good
configuration snapshots, and recovery verification.

Priority 6:
Expand validation to additional benign and suspicious
scenarios before considering operational deployment.

## 11. Final Engineering Decision

Laboratory investigation: COMPLETED

Automated detection testing: PASSED

Synthetic adversarial validation: COMPLETED

Operational containment: PASSED

Operational rollback and restoration: PASSED

Network isolation remediation: OUTSTANDING

Complete security recovery: NOT ACHIEVED

Production Deployment Decision: NO-GO

Incident Closure Authorization: NOT GRANTED

The laboratory findings support further remediation
and retesting, not operational deployment approval.

## 12. Supporting Evidence

Primary evidence directories:

01-Incident-Management/
02-Laboratory/
03-Detection-Engineering/
04-Adversarial-Validation/evidence/
05-Controls-and-Recovery/
07-Evidence/supporting-outputs/

Key reports:

- detector-evaluation.md
- detector-v2-evaluation.md
- adversarial-validation-report.txt
- networkpolicy-enforcement-review.md
- containment-restoration-review.md
- final-recovery-validation.md

The final closure package must retain relevant
source code, configurations, logs, tests, results,
and evidence integrity records.

## 13. Incident Timeline

The following times originate from the simulated
incident notification and assignment decision points.

The original scenario does not specify a time zone.
These times must not be represented as independently
verified UTC timestamps.

| Scenario Time | Event |
|---|---|
| 08:31 | Monitoring dashboard reported green after deployment |
| 08:34 | SOC reported unusual outbound communication |
| 08:37 | Platform Engineering reported healthy application pods |
| 08:40 | IAM reported unexpected service identity activity |
| 08:42 | Lead investigating engineer assigned |
| 09:05 | Initial containment decision requested |
| 10:20 | Detection engineering decision requested |
| 13:15 | Containment versus restoration decision requested |
| 15:30 | Production and closure decisions requested |

These are scenario milestones, not proof that the
reported security activity actually occurred.

The separate laboratory experiments used recorded
timestamps and synthetic test events.

Detailed chronology:
01-Incident-Management/incident-timeline.md

Operational evidence:
07-Evidence/supporting-outputs/
04-Adversarial-Validation/evidence/

## 14. Laboratory Architecture

The laboratory was deployed in the isolated
Minikube namespace ticket-012-lab.

### Application API

The application-api workload represents the
customer-facing application.

The secured laboratory version uses:

- Image: ticket012-application-api:lab-v2
- A dedicated Kubernetes service account
- Automatic service-account token mounting disabled
- Non-root execution and restricted capabilities
- An application-level destination allowlist

### Internal Service

The internal-service workload represents the
approved internal application dependency.

Its approved application endpoint is:

http://internal-service:8080/resource

A synthetic authentication token supports
the laboratory request workflow.

### Unapproved Collector

The unapproved-collector workload represents
the unexpected destination used during the
simulated incident.

It received synthetic laboratory traffic.
No real customer data was transmitted.

### Communication Paths

Approved path:

application-api -> internal-service

Suspicious simulated path:

application-api -> unapproved-collector

The protected application call path rejected
unapproved destinations.

However, a direct connection from within the
application container remained possible.

### Network Enforcement Limitation

The tested Minikube bridge-based CNI did not
enforce the temporary deny-all egress policy.

The application allowlist therefore did not
provide container-wide network isolation.

Additional architecture details:
02-Laboratory/architecture.md
02-Laboratory/incident-scenario.md

## 15. Investigation Scope and Impact

### Scope

This investigation covered:

- Kubernetes workload and deployment state
- Application network communication
- Synthetic service identity information
- Deployment and configuration changes
- Detection engineering and correlation logic
- Application and workload security controls
- Containment, rollback, and recovery procedures

### Observed Laboratory Impact

The simulated application contacted an
unapproved internal collector.

The control experiments demonstrated an
unenforced network restriction.

The controlled collector containment exercise
temporarily made the collector unavailable.

Approved application communication continued.

The rollback experiment reproduced an invalid
image deployment and successful corrective undo.

### Production Impact

No production environment was investigated
or changed as part of the laboratory.

No verified production outage, attacker,
data exfiltration, or customer impact was
established by the synthetic evidence.

The original incident notification reports
are scenario inputs, not independent proof
of a real-world compromise.

## 16. Residual Risks and Unresolved Questions

### Residual Risk 1 - Network Isolation

The tested deny-all egress NetworkPolicy
did not block the direct connection.

Status: OPEN.

### Residual Risk 2 - Identity Attribution

The detector compares claimed identity
with workload metadata.

This does not independently establish
the identity of the requesting process.

Status: OPEN.

### Residual Risk 3 - Detection False Positives

Version 2 improved recall on the synthetic
dataset but generated five false positives.

Authorization exceptions require stronger
independent evidence.

Status: OPEN.

### Residual Risk 4 - Limited Evaluation

The labeled dataset contains only
24 synthetic cases.

Production detection performance remains
unknown.

Status: OPEN.

### Unresolved Questions

- What independent evidence would establish
  whether the original activity was authorized?
- Would a policy-enforcing CNI block all
  tested unauthorized network paths?
- How would the detector perform on larger,
  more representative operational telemetry?
- What authorization and change records would
  substantiate legitimate exceptions?

Complete security remediation has not
been demonstrated.

## 17. Lessons Learned

1. Healthy Kubernetes workloads do not prove
   the absence of security incidents.

2. A successful deployment pipeline does not
   establish deployment authorization.

3. An application allowlist is not equivalent
   to enforced network isolation.

4. A configured NetworkPolicy must be tested
   for actual enforcement.

5. Claimed service identities must not be
   treated as independently authenticated.

6. Higher detection recall can substantially
   increase false-positive workload.

7. Synthetic detector checks must be separated
   from operational security-control tests.

8. Successful rollback and healthy replicas
   do not prove complete security recovery.

9. Evidence preservation and explicit
   authorization must precede consequential
   production response actions.

10. A defensible NO-GO recommendation is
    appropriate when material control gaps
    remain unresolved.

---

Final Status: TECHNICAL INVESTIGATION COMPLETE
Security Remediation Status: INCOMPLETE
Closure Decision: NOT AUTHORIZED
