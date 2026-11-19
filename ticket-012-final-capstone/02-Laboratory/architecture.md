# Ticket 012 - Laboratory Architecture

## Purpose
Reproduce and investigate a simulated security incident
in a local Kubernetes environment.

## Environment
Cluster: Minikube
Namespace: ticket-012-lab
Testing: Local laboratory only

## Planned Components

1. application-api
   - Simulated customer-facing application
   - Communicates with the internal service
   - Uses a synthetic application identity

2. internal-service
   - Simulated internal business resource
   - Receives requests from application-api
   - Records access attempts

## Planned Investigation

- Establish normal application behavior.
- Simulate an approved service connection.
- Introduce a deployment configuration change.
- Simulate suspicious communication locally.
- Investigate workload, identity, and network evidence.
- Compare malicious and non-malicious explanations.

## Safety
- No production systems.
- No real customer information.
- No real credentials.
- No external targets.
- All suspicious activity remains within the laboratory.

## Status
Architecture proposed.
Workloads not yet deployed.
