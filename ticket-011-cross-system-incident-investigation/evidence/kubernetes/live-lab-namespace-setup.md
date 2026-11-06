# Ticket 011 - Live Kubernetes Namespace Setup

Evidence type: ACTUAL MINIKUBE LAB OBSERVATION

Verification timestamp: 2026-11-02T20:03:16.8757586-05:00

Context: minikube

Namespace: ticket-011-lab

Security admission profile: restricted

Manifest: kubernetes-lab/manifests/namespace.yaml

API response: evidence/kubernetes/live-lab-namespace.json

## Scope

Created one new, isolated namespace.

No Pods or Deployments were created in this step.

No Ticket 010 Kubernetes resources were intentionally
modified.

## Evidence distinction

The live namespace snapshot is actual laboratory evidence.

Previously created Kubernetes JSONL records remain
SYNTHETIC and are not claimed as Falco or audit
telemetry from the running cluster.

## Next step

Deploy a nonprivileged reporting-api test workload
and validate its actual runtime security configuration.