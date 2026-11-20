# Ticket 012 - Operational Security-Control Review

Date: 2026-11-17
Namespace: ticket-012-lab
Cluster context: minikube

## Operational Findings

### Approved Application Communication
Result: PASS

The application-api successfully called the approved internal
service and received an authorized synthetic response.

### Direct Collector Reachability
Result: NETWORK ISOLATION GAP

The application container directly contacted the unapproved
collector's health endpoint and received HTTP 200.

The application-level destination allowlist does not enforce
network isolation for arbitrary code inside the container.

No real data exfiltration was performed or demonstrated.

### Kubernetes Service-Account Token
Result: PASS

The application container did not have an automatically
mounted Kubernetes service-account token.

This limits direct access to the Kubernetes API using
an automatically mounted workload token.

## Engineering Assessment

The application allowlist and disabled service-account token
are useful controls, but neither blocks arbitrary outbound
network communication from the application container.

Network-level enforcement requires further evaluation.

The current Minikube environment must not be assumed to
enforce Kubernetes NetworkPolicy without verification.

## Evidence

04-Adversarial-Validation/evidence/operational-control-check.txt

## Decision

Operational security validation: PARTIALLY PASSED.

Unrestricted direct collector reachability remains an
open security finding.

Production readiness: NOT APPROVED.
