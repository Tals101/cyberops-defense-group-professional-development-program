# Ticket #010 — Initial Incident Investigation

## Investigation Status
OPEN — Root cause not yet established.

## Reported Timeline

October 22, 2026:
- 21:41:08 — Build successful
- 21:42:16 — Dependency scan passed
- 21:43:02 — Container vulnerability scan passed
- 21:44:11 — Deployment validation passed
- 21:47:29 — Kubernetes rollout successful

October 23, 2026:
- 08:15:00 — Unsafe security configuration identified

## Established Information
The assignment reports that:
- The ledger-api deployment was accepted.
- The pipeline reported successful checks.
- The supplied manifest enables privileged execution.
- The container is configured to run as root.
- Privilege escalation is permitted.
- The image uses a mutable tag.
- Resource limits are absent.

These are reported facts, not independently verified observations.

## Competing Root-Cause Hypotheses

H1 — Missing Workload Security Validation
The pipeline scanned container vulnerabilities but did not evaluate Kubernetes securityContext settings.

H2 — Incomplete Security Policy
Deployment validation executed but lacked rules covering the unsafe configuration.

H3 — Artifact Mismatch
The manifest approved during validation differed from the manifest eventually deployed.

H4 — Deployment Authorization Gap
Kubernetes accepted the workload because applicable admission restrictions were absent, ineffective, or not enforced for this deployment.

H5 — Unauthorized or Accidental Modification
The configuration changed during development or deployment without appropriate detection.

## Evidence Gaps
- Complete pipeline configuration and logs
- Exact deployment-validation commands and policies
- Git history of the deployment manifest
- Approved versus deployed artifact hashes
- Kubernetes admission-control configuration
- Kubernetes audit records
- Change approvals and deployment identities

## Initial Assessment
The configuration presents significant security risk.

The available evidence does not establish malicious activity, actual privilege abuse, or the precise control failure.

## Current Conclusion
Root cause: UNDETERMINED

Next action: Investigate control coverage and reproduce the unsafe acceptance condition in an isolated lab.
