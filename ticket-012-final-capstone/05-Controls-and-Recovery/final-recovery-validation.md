# Ticket 012 - Final Recovery Validation Report

Date: 2026-11-17
Environment: Minikube
Namespace: ticket-012-lab

## Executive Summary

Controlled containment, laboratory restoration,
failed-deployment handling, and corrective rollback
were successfully demonstrated.

Network isolation remains unresolved.

Overall security recovery: INCOMPLETE.
Production readiness: NO-GO.

## 1. Containment Validation

Target: unapproved-collector

Action:
Temporarily scale the deployment from one replica
to zero.

Observed results:

- Collector became unavailable.
- Direct collector connection failed.
- Approved application communication continued.
- The collector was subsequently restored to one
  ready replica.

Result: PASS.

## 2. Failed Deployment Validation

Target: ticket012-rollback-probe

Initial image:
ticket012-unapproved-collector:lab-v1

Simulated failed update:
example.invalid/ticket012-missing:lab-v2

Observed results:

- The new pod entered ImagePullBackOff.
- The original healthy pod remained available.
- Kubernetes did not successfully deploy the new image.

Result: EXPECTED FAILURE REPRODUCED.

No application outage was demonstrated in this test.

## 3. Failed Rollback Attempt

Attempted rollback revision: 999

Observed result:
Kubernetes rejected the request because the
specified revision did not exist.

Exit code: 1

Result: EXPECTED OPERATOR ERROR REPRODUCED.

This was an invalid-revision test, not a simulated
Kubernetes control-plane failure.

## 4. Corrective Rollback

Action:
Execute a valid Kubernetes rollout undo.

Observed results:

- Working lab-v1 image restored.
- Ready replicas: 1.
- Updated replicas: 1.
- Rollout completed successfully.

Result: PASS.

## 5. Laboratory Cleanup

The disposable ticket012-rollback-probe
deployment was deleted.

Original deployments verified:

- application-api: 1/1 ready
- internal-service: 1/1 ready
- unapproved-collector: 1/1 ready

Result: PASS.

## 6. Outstanding Security Findings

The current Minikube bridge CNI did not enforce
the tested deny-all egress NetworkPolicy.

The application container remained capable of
directly contacting unapproved-collector before
workload-level containment.

Application destination validation does not
provide complete network isolation.

## 7. Final Recovery Assessment

Containment execution: PASS

Laboratory restoration: PASS

Failed deployment reproduction: PASS

Invalid rollback handling: PASS

Corrective rollback: PASS

Temporary workload cleanup: PASS

Network isolation remediation: INCOMPLETE

Complete security recovery: NOT ACHIEVED

Production readiness: NO-GO

Incident closure authorization: NOT GRANTED

## 8. Evidence References

04-Adversarial-Validation/evidence/

- containment-restoration-results.txt
- precontainment-collector.yaml
- precontainment-collector-logs.txt
- networkpolicy-enforcement-test.txt
- rollback-probe-prechange.yaml
- rollback-probe-failed-update-status.txt
- rollback-probe-failed-update.yaml
- invalid-rollback-attempt.txt
- rollback-failure-recovery-results.txt
- rollback-recovered-status.txt
- rollback-probe-rollout-history.txt

## 9. Scope and Limitations

All tests were performed in the isolated
Ticket 012 Kubernetes laboratory.

The collector and network activity were synthetic.

No real compromise or data exfiltration was
performed or demonstrated.

Successful operational restoration does not
constitute proof of complete security recovery.

Further remediation and authorization are required
before production use or incident closure.
