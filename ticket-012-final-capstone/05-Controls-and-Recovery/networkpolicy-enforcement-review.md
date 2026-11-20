# Ticket 012 - NetworkPolicy Enforcement Validation

Date: 2026-11-17
Cluster: minikube
Namespace: ticket-012-lab
Status: SECURITY CONTROL GAP CONFIRMED

## Objective

Determine whether Kubernetes NetworkPolicy prevents
application-api from contacting unapproved-collector.

## Environment

Active CNI configuration:
- bridge
- portmap
- firewall

No Calico or Cilium networking daemon was identified.

## Test Procedure

1. Identified the unapproved-collector ClusterIP.
2. Created a temporary deny-all egress NetworkPolicy.
3. Selected pods labeled app=application-api.
4. Allowed time for policy propagation.
5. Attempted a TCP connection to the collector on port 8080.
6. Removed the temporary NetworkPolicy.

## Observed Results

Policy creation: SUCCESS
Collector connection: REACHABLE
Policy deletion: SUCCESS

## Security Finding

The temporary deny-all egress policy did not block
the tested application-to-collector connection.

The current laboratory configuration must not be
treated as providing verified NetworkPolicy isolation.

The CNI firewall plugin does not, by itself,
establish Kubernetes NetworkPolicy enforcement.

## Impact

Application-level destination validation remains
effective only along the protected application path.

Code executing directly inside the application
container can reach the unapproved collector.

No real data exfiltration was performed.

## Required Remediation

Before relying on NetworkPolicy as a security control:

1. Use a networking implementation supporting
   Kubernetes NetworkPolicy enforcement.
2. Implement default-deny egress for application-api.
3. Permit only necessary approved service traffic.
4. Verify approved traffic succeeds.
5. Verify unapproved traffic is actually blocked.
6. Preserve enforcement evidence.

## Recovery Considerations

Do not change the cluster networking configuration
during the current incident investigation.

Preserve the existing laboratory state and perform
containment and rollback validation separately.

## Evidence

04-Adversarial-Validation/evidence/networkpolicy-enforcement-test.txt

## Decision

NetworkPolicy enforcement: NOT VERIFIED / TEST FAILED.

Production readiness: NO-GO.

Further isolated laboratory validation: AUTHORIZED
FOR TESTING PURPOSES ONLY.
