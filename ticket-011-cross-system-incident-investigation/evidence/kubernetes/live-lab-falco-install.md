# Ticket 011 - Falco Helm Installation

Classification: ACTUAL MINIKUBE LAB OPERATION

Timestamp: 2026-11-02T20:41:33.1470193-05:00

Chart: falcosecurity/falco
Chart version: 9.1.0
Release: ticket011-falco
Monitoring namespace: ticket-011-monitoring
Kubernetes context: minikube

## Configuration

- Modern eBPF driver selected
- Least-privileged capability mode requested
- Falco JSON output enabled
- Standard output logging enabled
- HTTP/program/file/syslog output disabled
- Automatic artifact following disabled
- Initial artifact installation retains chart defaults
- Falcosidekick disabled

## Verified Deployment

Falco Helm installation command: SUCCESS
Falco DaemonSet object: PRESENT
DaemonSet name: ticket011-falco

Rendered manifest SHA256: 767C0457F1418A8A679B7D8FD6080D47288F4FD1F9BB2D1D0F4C9DFA1A60FA6E

## Security Scope

The monitoring namespace permits elevated capabilities
required by Falco.

The Falco DaemonSet can potentially monitor activity
from other workloads on the shared Minikube node.

This is not application-namespace-only observation.

Ticket 010 namespace UID: UNCHANGED
Reporting API Deployment UID: UNCHANGED
Reporting API availability: 1/1

## Not Yet Established

- Falco Pod readiness
- Modern eBPF driver initialization
- Successful kernel event capture
- Shell-execution detection
- Complete monitoring coverage

These must be tested before runtime detection is
reported as successful.

No production or AWS resources were modified.