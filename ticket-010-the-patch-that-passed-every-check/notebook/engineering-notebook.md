# Ticket #010 — Engineering Notebook
## The Patch That Passed Every Check

Project: CyberOps Defense Group
Role: Security / DevSecOps Engineer
Environment: Synthetic Kubernetes and CI/CD lab

---

## Session 1 — October 25, 2026

### Objective
Establish the investigation workspace and prepare to examine the unsafe ledger-api deployment.

### Work Completed
1. Verified Git repository is on branch main.
2. Confirmed working tree is clean and synchronized with origin/main.
3. Created the ticket-010 project directory.
4. Created 13 subdirectories for investigation, implementation, testing, evidence, and closure.

### Initial Incident Information
- Application: ledger-api
- Namespace: production
- Reported deployment: October 22, 2026, at 21:47
- Reported security finding: October 23, 2026, at 08:15

### Configuration Risks Reported
- Privileged container enabled
- Privilege escalation permitted
- Container configured to run as root
- Mutable image tag used
- Resource limits absent
- No documented admission-policy enforcement

### Preliminary Assessment
The supplied incident record indicates that the pipeline reported successful security checks and rollout despite unsafe workload settings.

The actual root cause has not yet been established.

### Evidence Status
The incident description and CI/CD log excerpt are supplied evidence.
No independent reproduction or tool validation has been performed.

### Next Actions
1. Preserve the supplied baseline configuration.
2. Analyze the CI/CD control gaps.
3. Document competing root-cause hypotheses.
4. Reproduce the unsafe acceptance condition.

### Time Tracking
Session duration: To be recorded from actual work time.

### Status
Investigation preparation in progress.

---

## Session 1 — Baseline Security Validation Results

### Kubernetes Server-Side Validation
Command: kubectl create --dry-run=server

Observed result:
- Unsafe Deployment accepted
- Exit code: 0
- No Deployment created

Evidence: evidence/baseline-server-dry-run.txt

### Trivy Configuration Scan
Tool version: 0.70.0
Target: kubernetes/ledger-api-unsafe-lab.yaml

Observed results:
- Total checks: 98
- Successful checks: 79
- Failed checks: 19
- High: 3
- Medium: 5
- Low: 11
- Exit code: 1

Evidence: evidence/baseline-trivy-config-scan.txt

### Tool Limitation
Trivy reported that a policy module requiring version
0.72.0 or newer was skipped. Coverage is not assumed
to be complete.

### Engineering Finding
Kubernetes accepted the unsafe Deployment configuration
during server-side dry-run validation, while Trivy
identified multiple security misconfigurations.

The tests demonstrate different security decisions by
the two validation mechanisms.

### Limitations
- No actual workload has been deployed.
- Pod admission has not been independently tested.
- Original CI/CD behavior has not been reproduced.
- Root cause remains undetermined.

### Next Action
Prepare a runnable synthetic ledger-api application
and reproduce the baseline deployment in the isolated
ticket-010-lab namespace.

### Stop Gate 1
IN PROGRESS — Additional reproduction evidence required.

---

## Session 1 — Image Vulnerability Scan

### Test
Trivy image vulnerability scan of:
ledger-api:ticket010-baseline

### Configuration
- Scanner: vulnerability
- Severity threshold: HIGH,CRITICAL
- Exit code on findings: 1

### Observed Results
- Vulnerability database download completed
- Operating system: Debian 13.7
- High vulnerabilities: 44
- Critical vulnerabilities: 0
- Scan exit code: 1

### Evidence
evidence/baseline-image-vulnerability-scan.txt

### Engineering Interpretation
The baseline container image failed the enforced
vulnerability threshold.

A CI/CD pipeline correctly enforcing this scan result
would block this particular image.

This result does not invalidate our demonstrated
Kubernetes admission-control gap.

Image vulnerability scanning and Kubernetes workload
configuration validation evaluate different risks.

### Next Action
Establish a reproducible baseline pipeline that
separately evaluates image vulnerability decisions
and Kubernetes workload-security decisions.

Preserve this failed image scan as a negative result.
Do not suppress vulnerabilities merely to force a pass.

### Stop Gate 1
IN PROGRESS — Pipeline control-gap demonstration remains.

---
