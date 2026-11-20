# Ticket 012 - Workload Identity Security Control

## Objective
Reduce unnecessary Kubernetes API credential exposure
in the application-api workload.

## Original Configuration
ServiceAccount: default
Kubernetes API access volume: Present

## Security Improvement
Dedicated ServiceAccount: ticket012-application-api
automountServiceAccountToken: false

## Implementation
ServiceAccount manifest:
02-Laboratory/manifests/application-api-serviceaccount.yaml

Deployment manifest:
02-Laboratory/manifests/application-api-identity-secured.yaml

## Validation Results
Deployment rollout: PASS
Dedicated ServiceAccount assigned: PASS
Automatic token mounting disabled: PASS
Standard Kubernetes API token file absent: PASS

Observed result:
TOKEN_PRESENT=False

## Security Benefit
The application no longer receives an automatically
mounted Kubernetes API token that it does not need.

This reduces unnecessary credential exposure.

## Limitations
- Does not prevent independent network connections.
- Does not remove the application's synthetic lab credential.
- Does not establish network-level containment.
- Does not independently prove that RBAC permissions are minimal.

## Assessment
Workload identity protection: PASS
Complete security containment: NOT YET VERIFIED
