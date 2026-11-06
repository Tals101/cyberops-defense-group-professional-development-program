# Ticket 011 - Detection Engineering Verification

Ticket: CYBEROPS-PDP-011
Classification: ACTUAL ISOLATED MINIKUBE LAB
Verified UTC: 2026-11-03T18:20:14.3953515+00:00

## Live Falco Baseline

- Helm release: ticket011-falco
- Namespace: ticket-011-monitoring
- Helm revision: 3
- Release status: deployed
- Falco DaemonSet: 1/1 ready and available
- Two custom rule ConfigMap entries verified

## Detection Enhancements

1. Ticket011 Unexpected Shell In Reporting Image

   Detects shell execution in the reporting image,
   including noninteractive shell launches.

2. Ticket011 Reporting ServiceAccount Token Access Attempt

   Detects attempts to open the Kubernetes
   ServiceAccount token path in the reporting image,
   including failed opens of nonexistent files.

## Validated Live Controls

| Test | Result | Attributed alerts |
|---|---|---:|
| Enhancement 1 positive | DETECTED_AND_ATTRIBUTED | 1 |
| Enhancement 1 negative | PASS_NO_CUSTOM_RULE_ALERT | 0 |
| Enhancement 2 positive | DETECTED_AND_ATTRIBUTED_FAILED_OPEN | 1 |
| Enhancement 2 negative | PASS_NO_TOKEN_ACCESS_ALERT | 0 |

All four controls passed their recorded checks.

The token-access positive test returned ENOENT.
The token was absent and no credential was read.

These results demonstrate behavior only in the
specific isolated laboratory tests.

## Evidence Inventory

Evidence files found before creating this report:
59

- evidence\aws\.gitkeep
- evidence\aws\aws-investigation-timeline.csv
- evidence\aws\cloudtrail-synthetic.jsonl
- evidence\aws\DATASET-PROVENANCE.md
- evidence\aws\reference-context-synthetic.json
- evidence\kubernetes\.gitkeep
- evidence\kubernetes\DATASET-PROVENANCE.md
- evidence\kubernetes\falco-enhancement1-deployment-attempt.txt
- evidence\kubernetes\falco-enhancement1-deployment-result.md
- evidence\kubernetes\falco-enhancement1-design.md
- evidence\kubernetes\falco-enhancement1-rule-validation.txt
- evidence\kubernetes\falco-enhancement2-deployment-attempt.txt
- evidence\kubernetes\falco-enhancement2-deployment-result.md
- evidence\kubernetes\falco-enhancement2-design.md
- evidence\kubernetes\falco-enhancement2-recovery-check.txt
- evidence\kubernetes\falco-enhancement2-rule-validation.txt
- evidence\kubernetes\falco-enhancement2-v2-rule-validation.txt
- evidence\kubernetes\falco-runtime-synthetic.jsonl
- evidence\kubernetes\kubernetes-audit-synthetic.jsonl
- evidence\kubernetes\live-lab-deployment.json
- evidence\kubernetes\live-lab-deployment-verification.md
- evidence\kubernetes\live-lab-ebpf-readiness.txt
- evidence\kubernetes\live-lab-falco-crash-review-6q.txt
- evidence\kubernetes\live-lab-falco-daemonset.json
- evidence\kubernetes\live-lab-falco-enhancement1-negative.json
- evidence\kubernetes\live-lab-falco-enhancement1-negative.md
- evidence\kubernetes\live-lab-falco-enhancement1-positive.json
- evidence\kubernetes\live-lab-falco-enhancement1-positive.md
- evidence\kubernetes\live-lab-falco-enhancement2-negative.json
- evidence\kubernetes\live-lab-falco-enhancement2-negative.md
- evidence\kubernetes\live-lab-falco-enhancement2-positive.json
- evidence\kubernetes\live-lab-falco-enhancement2-positive.md
- evidence\kubernetes\live-lab-falco-install.md
- evidence\kubernetes\live-lab-falco-negative-control.json
- evidence\kubernetes\live-lab-falco-negative-control.md
- evidence\kubernetes\live-lab-falco-preflight.txt
- evidence\kubernetes\live-lab-falco-readiness-recheck-6q.txt
- evidence\kubernetes\live-lab-falco-runtime-daemonset.json
- evidence\kubernetes\live-lab-falco-runtime-pods.json
- evidence\kubernetes\live-lab-falco-shell-test.json
- evidence\kubernetes\live-lab-falco-shell-test.md
- evidence\kubernetes\live-lab-falco-startup-diagnostics.txt
- evidence\kubernetes\live-lab-http-container-logs.txt
- evidence\kubernetes\live-lab-http-results.json
- evidence\kubernetes\live-lab-http-validation.md
- evidence\kubernetes\live-lab-image-build.txt
- evidence\kubernetes\live-lab-image-load.txt
- evidence\kubernetes\live-lab-namespace.json
- evidence\kubernetes\live-lab-namespace-setup.md
- evidence\kubernetes\live-lab-pod.json
- evidence\kubernetes\live-lab-rbac-validation.json
- evidence\kubernetes\live-lab-runtime-security.json
- evidence\kubernetes\live-lab-security-boundary-assessment.md
- evidence\kubernetes\live-lab-service.json
- evidence\kubernetes\live-lab-serviceaccount.json
- evidence\kubernetes\live-lab-service-endpoints.json
- evidence\kubernetes\network-flow-synthetic.jsonl
- evidence\kubernetes\workload-context-synthetic.json
- evidence\linux\.gitkeep

## Project Directory Inventory

- adversarial-testing
- closure
- correlation-engine
- detection-engineering
- evidence
- incident-report
- kubernetes-lab
- notebook
- operations

## Ticket Closure Items Requiring Separate Audit

- Confirm at least eight distinct adversarial tests
  with outcomes and supporting evidence.
- Review AWS, Linux, and Kubernetes evidence
  correlation and establish event chronology.
- Verify the documented 09:05 containment
  decision and evidence stop gate.
- Review incident analysis, root cause, impact,
  recommendations, and lessons learned.
- Confirm completeness of final closure artifacts
  and the submission package.

These items are not declared complete by this
detection-engineering verification.

## Operational Limitations

An earlier Falco exit-code-255 observation has
not been conclusively explained.

A Kubernetes AppArmor annotation deprecation
warning remains a maintenance consideration.

Synthetic incident evidence must remain explicitly
distinguished from actual Minikube observations.

No production or AWS environment was modified
by the validation steps documented here.