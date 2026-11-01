# Ticket #010 - Supplemental Engineering Notebook

## Purpose and Record Integrity

This document supplements, but does not replace,
notebook/engineering-notebook.md.

The original engineering notebook is preserved without
editing its historical observations or conclusions.

This supplement was compiled retrospectively using
existing project reports, tests, and recorded evidence.

The dates of some intermediate engineering work sessions
and actual hours worked were not independently recorded.
No dates or work durations have been invented.

## Session 1 - October 25, 2026

### Objective

Investigate the unsafe ledger-api deployment and
establish the baseline security-control failure.

### Recorded Activities

- Reviewed the incident scenario and unsafe manifest.
- Inspected Kubernetes validation behavior.
- Evaluated container security misconfigurations.
- Performed baseline image vulnerability assessment.
- Separated Kubernetes admission findings from image
  vulnerability-scan results.

### Engineering Findings

Server-side Kubernetes validation accepted the unsafe
baseline manifest, demonstrating the admission gap.

Independent image scanning produced security findings
that would require enforcement by an appropriate gate.

### Evidence

- notebook/engineering-notebook.md
- investigation/initial-investigation.md
- investigation/stop-gate-1-report.md
- evidence/baseline-server-dry-run.txt
- evidence/baseline-image-vulnerability-scan.txt

### Time Spent

Actual work duration: NOT RECORDED.

The original notebook's incomplete time-tracking field
remains unchanged.

## Subsequent Engineering Workstreams

The following sections are retrospective workstream
summaries. They are not claims of separate dated sessions.

### V1 - Policy-as-Code and Pipeline Controls

Work date(s): NOT INDEPENDENTLY RECORDED.

Activities:

- Evaluated configuration and release-gate controls.
- Tested vulnerable and approved laboratory scenarios.
- Recorded scanner decisions and control limitations.
- Assessed registry allowlist behavior independently
  from scanner registry findings.

Engineering decision:

Do not treat a scanner warning, policy detection, or
successful allowlist check as proof of complete
release-security enforcement.

Evidence:

- investigation/v1-security-control-assessment.md
- pipeline/
- tests/
- evidence/

Actual work duration: NOT RECORDED.

### V2 - Kubernetes Admission Enforcement

Work date(s): NOT INDEPENDENTLY RECORDED.

Activities:

- Tested restricted Pod Security Admission.
- Evaluated custom image-reference enforcement.
- Tested rejection of an unapproved registry.
- Evaluated ephemeral-container admission behavior.
- Preserved positive and negative test results.

Engineering decision:

Admission enforcement must protect workload paths,
including relevant subresource operations.

Evidence:

- investigation/v2-admission-security-assessment.md
- admission/
- tests/
- evidence/v2-psa-unsafe-pod-rejection.txt
- evidence/v2-unapproved-registry-rejection.txt
- evidence/v2-ephemeral-subresource-test.txt

Actual work duration: NOT RECORDED.

### V3 - Artifact Integrity and Release Decisions

Work date(s): NOT INDEPENDENTLY RECORDED.

Activities:

- Evaluated release-image identity and trust checks.
- Tested signing and signer-trust controls.
- Tested vulnerability and freshness failures.
- Preserved negative controls and final regression results.
- Analyzed differences between laboratory trust and
  production verification requirements.

Engineering decision:

A successful local release test does not establish
production readiness without complete trust,
provenance, approval, and operational validation.

Evidence:

- investigation/v3-engineering-assessment.md
- supply-chain/
- pipeline/
- evidence/v3-final-release-regression.csv
- closure/v3-ticket-closure-report.md

Actual work duration: NOT RECORDED.

### Consolidated Adversarial Assessment

Work date(s): NOT INDEPENDENTLY RECORDED.

Thirteen scenarios were consolidated.

Twelve outcomes have supporting verification.

A02 remains classified as detection-only because the
exact fixture's release-gate result is not independently
established by the cited record.

Evidence:

- tests/adversarial-test-matrix.csv
- tests/adversarial-test-matrix.md

Actual work duration: NOT RECORDED.

## Recovery Work - November 1, 2026

### Objective

Test Kubernetes recovery of a healthy application
configuration after a deliberately unsuccessful update.

### Recorded Timeline

11:11:09 EST - Initial baseline evidence recorded.

12:06:43 EST - Controlled rollback rehearsal recorded.

12:09:44 EST - Independent final verification recorded.

12:14:45 EST - Cleanup verification recorded.

These are evidence-record timestamps. They do not
establish total active engineering time.

### Initial Baseline

- Dedicated namespace: ticket-010-rollback-lab.
- Restricted Pod Security Admission enforced.
- Deployment revision 1 established.
- Application readiness and HTTP /health verified.
- Minikube image ID matched the running Pod.
- Docker Desktop and Minikube image IDs differed.

### Controlled Failure and Rollback

- Revision 2 changed readiness port from 8080 to 18081.
- New Pod failed readiness.
- Rollout timed out with exit code 1.
- Original healthy replica remained available.
- kubectl rollout undo succeeded.
- Restored configuration became revision 3.
- Readiness port returned to 8080.
- Application health returned HTTP 200.

### Independent Verification and Cleanup

- Restored application health was checked again.
- Runtime image identity was unchanged from the
  recorded Minikube baseline.
- Original admission-policy binding remained unchanged.
- Isolated test namespace was deleted.
- Cleanup and evidence integrity were verified.

### Evidence

- recovery/rollback-initial-deployment-evidence.txt
- recovery/rollback-readiness-failure-patch.json
- recovery/rollback-rehearsal-evidence.txt
- recovery/rollback-final-verification.txt
- recovery/rollback-cleanup-verification.txt
- recovery/recovery-and-rollback-assessment.md

### Engineering Decision

The rehearsal verifies an isolated Kubernetes
configuration rollback.

It does not establish an image-version rollback,
production recovery, complete image provenance,
or enforcement of the V2 image-reference policy
inside the separate recovery namespace.

Residual risk R06 remains OPEN.

Actual work duration: NOT RECORDED.

## Time-Tracking Limitations

See notebook/session-time-ledger.csv.

Known dates and evidence timestamps have been retained.
Intermediate workstream dates and actual work hours
require the engineer's own records or confirmation.

Do not interpret elapsed time between evidence records
as actual time worked.

## Current Closure Assessment

The original incident and engineering evidence remain
the basis of the investigation.

The supplemental notebook records later work and
its limitations without rewriting earlier findings.

The laboratory security and recovery tests support
technical closure documentation, not authorization
to deploy the workload to production.

Production readiness: NOT ESTABLISHED.
