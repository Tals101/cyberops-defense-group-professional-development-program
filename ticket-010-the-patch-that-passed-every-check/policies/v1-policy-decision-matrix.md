# Ticket #010 — V1 Security Policy Decision Matrix

## Purpose
Define preventive security controls for the ledger-api
CI/CD deployment workflow.

Status: PROPOSED — Implementation and testing pending.

## Blocking Policies

P01 — Privileged Containers
Requirement: privileged must be false or omitted.
Decision: BLOCK if true.

P02 — Privilege Escalation
Requirement: allowPrivilegeEscalation must be false.
Decision: BLOCK if true or missing.

P03 — Root Execution
Requirement: runAsNonRoot must be true and an
explicit runAsUser must be greater than zero.
Decision: BLOCK on root, missing, or conflicting values.

P04 — Immutable Images
Requirement: Production images must use a digest
reference containing @sha256.
Decision: BLOCK mutable tag-only references.
Lab exceptions require separate authorization.

P05 — Resource Configuration
Requirement: CPU and memory requests and limits
must be specified.
Decision: BLOCK missing or invalid settings.

P06 — Additional Runtime Hardening
Requirement: Drop ALL Linux capabilities and use
an approved seccomp profile.
Decision: BLOCK noncompliant settings.

## Warning Policy

P07 — Read-Only Root Filesystem
Requirement: Prefer readOnlyRootFilesystem: true.
Decision: WARN during V1.
Production enforcement decision requires further review.

## Exception Management
- No automatic exceptions based solely on annotations.
- Security approval required before any exception.
- Record justification, scope, owner, and expiration.
- Preserve exception decisions in audit evidence.
- CI exceptions do not override cluster admission.
- No exceptions approved at this stage.

## Enforcement Design
1. Scan container image vulnerabilities.
2. Validate Kubernetes configuration.
3. Evaluate mandatory workload policies.
4. Block release on any mandatory policy violation.
5. Preserve reports and exit codes.
6. Require explicit authorization before deployment.

## Failure Handling
- Missing mandatory security fields: BLOCK.
- Policy evaluation errors: BLOCK.
- Unavailable required scanning tool: BLOCK.
- Missing evidence: BLOCK.
- Warnings remain visible in release reports.

## Scope
V1 applies to the synthetic ledger-api workflow.

Actual admission enforcement will be addressed in V2.
Artifact integrity enforcement will be addressed in V3.

## Validation Status
Design documented.
Implementation not yet tested.
