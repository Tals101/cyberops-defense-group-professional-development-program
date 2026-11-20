# Ticket 012 - Containment and Recovery Assessment

Date: 2026-11-17
Environment: Minikube laboratory
Namespace: ticket-012-lab

## 1. Objective

Validate controlled containment of the simulated
unapproved collector while preserving legitimate
application functionality.

Restore the laboratory after completing the test.

## 2. Evidence Preservation

Before containment, the collector deployment
configuration and available logs were preserved.

Evidence files:

- precontainment-collector.yaml
- precontainment-collector-logs.txt
- containment-restoration-results.txt

Location: 04-Adversarial-Validation/evidence/

## 3. Containment Execution

Action:
Scale unapproved-collector from one replica to zero.

Observed results:

- Collector became unavailable.
- Direct connections to the collector failed.
- Application-to-internal-service communication
  continued to return an authorized response.

Assessment: CONTAINMENT TEST PASSED.

## 4. Laboratory Restoration

Action:
Restore unapproved-collector to its original
replica count of one.

Observed results:

- Kubernetes rollout completed.
- One collector replica became ready.
- Laboratory workload configuration was restored.

Assessment: LABORATORY RESTORATION PASSED.

Restoring the collector was necessary to return
the controlled laboratory to its baseline state.
It was not a security remediation.

## 5. Outstanding Security Risks

The underlying network-isolation weakness remains.

Previous tests demonstrated that application-api
could directly reach unapproved-collector despite
an application-level destination allowlist.

A temporary deny-all egress NetworkPolicy also
failed to block that connection.

The current bridge CNI must not be assumed
to enforce Kubernetes NetworkPolicy.

## 6. Recovery Assessment

Operational laboratory restoration: PASS

Complete security recovery: NOT ACHIEVED

Network isolation remediation: OUTSTANDING

Failed or incomplete rollback exercise:
COMPLETED - invalid revision rejected; valid rollback restored lab-v1

Production readiness: NO-GO

Incident closure authorization: NOT GRANTED

## 7. Required Follow-up

- Conduct a separate failed/incomplete rollback test.
- Preserve rollback and recovery evidence.
- Validate network isolation using an enforcing CNI.
- Retest legitimate and unauthorized traffic.
- Complete the final recovery and closure review.

## 8. Scope

All activity was conducted in the controlled
Ticket 012 Kubernetes laboratory.

No real compromise or data exfiltration
was performed or demonstrated.

