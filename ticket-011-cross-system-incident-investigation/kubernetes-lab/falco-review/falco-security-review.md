# Ticket 011 - Falco Helm Security Review

Classification: LOCAL HELM TEMPLATE REVIEW

Timestamp: 2026-11-02T20:33:19.9427423-05:00

Chart: falcosecurity/falco
Chart version: 9.1.0
Proposed release: ticket011-falco
Proposed namespace: ticket-011-monitoring

## Proposed Configuration

- Driver: modern_ebpf
- Least-privileged modern eBPF mode: requested
- Controller: DaemonSet

## Rendered Manifest Inspection

- DaemonSet: 1 matching manifest entries
- ClusterRole: 0 matching manifest entries
- ClusterRoleBinding: 0 matching manifest entries
- HostPathMount: 6 matching manifest entries
- HostPID: 0 matching manifest entries
- PrivilegedContainer: 0 matching manifest entries
- CapabilityBPF: 1 matching manifest entries
- CapabilityPerfmon: 1 matching manifest entries

## Important Security Considerations

The proposed Falco DaemonSet operates at node scope,
even when its Kubernetes objects are installed in a
dedicated namespace.

The modern eBPF driver requires elevated Linux
capabilities and access to kernel event information.

The least-privileged setting is a requested Helm
configuration. This report does not prove that every
rendered container uses minimum privileges.

Review the complete rendered manifests, including
init containers, host mounts, RBAC, security contexts,
and workload images, before any installation.

## Evidence

- falco-review-values.yaml
- falco-chart-metadata.yaml
- falco-rendered-manifests.yaml

## Status

Chart rendering: COMPLETE
Security inspection: PRELIMINARY
Falco installation: NOT PERFORMED
Kernel driver loading: NOT TESTED
Runtime detection alerts: NOT TESTED

No Kubernetes resources were created or modified.