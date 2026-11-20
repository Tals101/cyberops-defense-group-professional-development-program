# TICKET 012 - EXECUTIVE INCIDENT BRIEF

**Report Date:** November 17, 2026
**Incident ID:** TICKET-012
**Environment:** Controlled Kubernetes Laboratory
**Initial Severity:** High (Provisional)

**Production Decision: NO-GO**
**Incident Closure: NOT AUTHORIZED**

---

## Executive Summary

Ticket 012 investigated a simulated multi-stage
Kubernetes security incident involving unexpected
network communication, workload identity, deployment
changes, and security-control weaknesses.

The laboratory reproduced an application communicating
with an unapproved internal collector following a
configuration change.

The investigation successfully demonstrated detection
engineering, evidence preservation, incident containment,
and recovery procedures.

However, testing identified an unresolved weakness:
the current Kubernetes networking configuration did
not enforce the tested outbound network restrictions.

**Complete security recovery has not been achieved.**

## Key Investigation Findings

### 1. Unexpected Network Communication

The application was redirected from its approved
internal service to a simulated unapproved collector.

The collector received synthetic laboratory traffic.

No real compromise or sensitive-data exfiltration
was demonstrated.

### 2. Detection Engineering

Two detector versions were developed and evaluated.

**Automated testing:** 51 of 51 tests passed.

The evaluation used 24 labeled synthetic scenarios.

| Metric | Version 1 | Version 2 |
|---|---:|---:|
| True Positives | 5 | 12 |
| False Positives | 1 | 5 |
| False Negatives | 7 | 0 |
| Recall | 41.7% | 100.0% |

Version 2 detected all suspicious cases in the
constructed dataset, but generated additional false
positives.

These findings do not establish production performance.

### 3. Adversarial and Resilience Validation

Eight synthetic detector-level exercises were executed.

**Behavioral checks passed: 8 of 8.**

One benign scenario generated a false-positive alert.

Separate operational Kubernetes tests examined
network restrictions, containment, failed deployment,
and recovery.

### 4. Security Controls

The application destination allowlist successfully
restricted its protected communication path.

The application's Kubernetes service-account token
was not automatically mounted.

However, direct connections from the application
container to the unapproved collector remained possible.

A temporary deny-all egress NetworkPolicy did not
block the tested connection.

**Network isolation remains an open finding.**

### 5. Containment and Recovery

Controlled containment successfully made the
unapproved collector unavailable while preserving
approved application communication.

The laboratory was subsequently restored.

A separate rollback experiment demonstrated:

- An expected failed container-image deployment.
- Rejection of an invalid rollback revision.
- Successful corrective rollback.
- Restoration of the working container image.
- Removal of the disposable test workload.

All three original laboratory deployments were
verified healthy following the experiment.

## Business and Operational Implications

The investigation demonstrates that successful
application-level controls and operational recovery
do not necessarily establish complete security.

Without enforced network isolation, code executing
inside a compromised container could potentially
communicate with destinations outside the application's
approved request path.

The detector also requires stronger authorization
evidence and broader validation to reduce false
positives while maintaining detection sensitivity.

## Recommended Next Actions

**Priority 1 - Network Enforcement**

Implement a compatible network-policy-enforcing
solution in an appropriate isolated environment.

Verify approved traffic succeeds and unapproved
traffic is blocked.

**Priority 2 - Detection Improvements**

Add independently verified identity and exception
authorization evidence.

Retest using expanded benign and suspicious scenarios.

**Priority 3 - Recovery Assurance**

Maintain tested containment procedures, known-good
deployment configurations, and rollback instructions.

**Priority 4 - Final Remediation Review**

Reassess control effectiveness and detection results
before considering operational deployment or
incident closure.

## Final Executive Decision

**Technical Investigation:** Completed

**Laboratory Testing:** Completed

**Operational Containment and Restoration:** Passed

**Network Isolation Remediation:** Outstanding

**Complete Security Recovery:** Not Achieved

**Production Deployment:** NO-GO

**Incident Closure Authorization:** NOT GRANTED

The appropriate next action is remediation and
revalidation, not unrestricted operational deployment
or final incident closure.

---

**Scope:** All activity was performed within a
controlled synthetic Kubernetes laboratory.
No production incident or real data exfiltration
is claimed.
