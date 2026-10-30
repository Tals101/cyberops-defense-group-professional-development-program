# Ticket #010 — Stop Gate 1 Assessment

## Decision
PASS — Synthetic baseline failure reproduced.

## Objective
Demonstrate how an unsafe Kubernetes deployment
configuration can pass an incomplete CI/CD pipeline.

## Evidence

### Image Vulnerability Scanning
Alpine baseline image:
- HIGH vulnerabilities: 0
- CRITICAL vulnerabilities: 0
- Trivy exit code: 0

Evidence:
evidence/alpine-image-vulnerability-scan.txt

### Baseline Pipeline
- Image scan: PASS
- Kubernetes API validation: PASS
- Workload security policy: NOT CHECKED
- Pipeline exit code: 0

Evidence:
evidence/baseline-pipeline-run.txt
evidence/pipeline-image-scan.txt

### Workload Reproduction
A previous deployment using the Debian baseline
demonstrated:
- Two running Kubernetes Pods
- Privileged execution permitted
- Privilege escalation permitted
- Effective UID: 0
- Successful HTTP health response

The Alpine image was not deployed during this
pipeline test.

Evidence:
evidence/baseline-live-pods.json
evidence/baseline-live-pod-security.txt
evidence/baseline-live-health-retest.txt

### Configuration Security
Trivy identified 19 Kubernetes configuration
misconfigurations in the original unsafe lab manifest.

Evidence:
evidence/baseline-trivy-config-scan.txt

## Root-Cause Assessment
The synthetic pipeline omits enforceable workload
security validation.

Image vulnerability checks cannot substitute for
Kubernetes configuration policy enforcement.

Kubernetes API validation alone did not prevent
acceptance of the unsafe Deployment.

## Limitations
- Original incident pipeline configuration unavailable
- Original production audit records unavailable
- Alpine image not tested as a live workload
- Artifact integrity not yet tested
- Admission bypass scenarios not yet tested

## Cleanup
The original unsafe deployment was removed.
Zero ledger-api Pods remained after cleanup.

## Conclusion
Stop Gate 1 is satisfied for the synthetic lab.

The demonstrated control gap is supported by
reproducible test evidence.

## Next Phase
V1 — Implement preventive security controls
in the CI/CD pipeline.
