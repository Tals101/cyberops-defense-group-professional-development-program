# Ticket 011 - Detection Enhancement 2

Classification: LOCAL RULE DESIGN AND HELM RENDER
Timestamp UTC: 2026-11-03T17:54:00.1077261+00:00

## Objective

Detect attempted access to the Kubernetes
ServiceAccount token path by the reporting container.

Rule: Ticket011 Reporting ServiceAccount Token Access Attempt

## Detection Logic

- File-open syscalls: open, openat, openat2
- Exit events, including failed open operations
- Ticket 011 reporting container image
- ServiceAccount token path
- Alert includes syscall result, not token contents

The condition matches an attempted open. It
does not establish that a token was present,
read successfully, or exfiltrated.

## Expected Hardened Pod Behavior

The Ticket 011 reporting Pod was previously
verified to have token automount disabled.

A future positive control should first verify
the token is absent, then attempt an open
without reading any token contents.

An ENOENT result would indicate a missing file.
It would not indicate credential compromise.

## Negative Control

Execute a direct Python health check without
accessing the ServiceAccount token path.

## Security Scope

Both custom rules are retained in the proposed
Helm values.

No elevated capabilities, hostPath mounts, or
cluster-wide RBAC were added by this design.

## Evidence

Enhancement 2 rule SHA256:
3CD99AA9CBAE42446A2245FFB09CDAC14D51CE91ACE18D8BB6A583B31F759DA3

Proposed Helm values SHA256:
5AB68154603A6BBC3CA1B1D575255465F9A815FF6D626D67F43B0AF692291139

Original Enhancement 1 values SHA256:
FA64D9C83A650D420169141AD0133F6264B8A20AE21493468FCAEF4C34B68923

## Status

Helm rendering: PASS
Rule syntax validation: PENDING
Live Falco deployment: NOT PERFORMED
Live positive control: NOT PERFORMED
Live negative control: NOT PERFORMED

No Kubernetes resources were modified.