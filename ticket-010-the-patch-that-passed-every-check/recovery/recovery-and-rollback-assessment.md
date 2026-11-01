# Ticket #010 - Recovery and Rollback Assessment

## Purpose

Evaluate the recovery evidence produced during the
ledger-api security investigation and identify the
remaining requirements for a controlled rollback.

## Scope

Synthetic Kubernetes and CI/CD security laboratory.

No production recovery or production rollback occurred.

## 1. Existing Baseline Cleanup Evidence

Evidence:
- evidence/baseline-cleanup-verification.txt
- investigation/stop-gate-1-report.md

The Stop Gate 1 investigation documented cleanup of
the unsafe ledger-api laboratory workload.

The assessment recorded zero remaining ledger-api Pods
after the baseline cleanup operation.

This demonstrates laboratory cleanup, not restoration
of a previously approved application release.

## 2. V2 Admission Test Cleanup

Evidence:
- evidence/v2-ephemeral-subresource-test.txt
- evidence/v2-replicaset-admission-test.txt

The V2 evidence includes cleanup operations associated
with admission-enforcement testing.

These records support the removal of temporary test
resources within the laboratory.

They do not establish application version rollback,
data restoration, or production service recovery.

## 3. V3 Release Prevention

Evidence:
- evidence/v3-final-release-regression.csv
- evidence/v3-final-release-regression.txt

The tested V3 release controls rejected unsigned,
unauthorized-signer, and vulnerable release scenarios.

Rejecting a release before deployment is a preventive
security measure. It is not a rollback operation.

## 4. Application Rollback Status

Current status: ISOLATED CONFIGURATION ROLLBACK VERIFIED.

On November 1, 2026, a controlled rehearsal was performed
in the dedicated namespace ticket-010-rollback-lab.

The rehearsal used restricted:v1.35 Pod Security Admission.

Observed sequence:

1. Revision 1 was healthy with readiness port 8080.
2. Revision 2 changed readiness port to 18081.
3. The new Pod remained unready.
4. The revised rollout timed out with exit code 1.
5. The original healthy Pod remained available.
6. kubectl rollout undo --to-revision=1 succeeded.
7. Kubernetes assigned restored revision number 3.
8. Readiness port 8080 was restored.
9. The Deployment returned to one ready and available replica.
10. The restored application returned HTTP 200 from /health.

The runtime image identity matched the earlier Minikube
baseline after rollback.

This verifies a laboratory Deployment configuration rollback.

It does not establish an image-version rollback, database
recovery, production rollback, or production service continuity.

## 5. Rehearsal Evidence and Remaining Limitations

Primary evidence:

- recovery/rollback-lab-preflight.txt
- recovery/rollback-baseline-deployment.yaml
- recovery/rollback-initial-deployment-evidence.txt
- recovery/rollback-readiness-failure-patch.json
- recovery/rollback-rehearsal-evidence.txt
- recovery/rollback-final-verification.txt

Verified:

- An isolated laboratory namespace was used.
- The failed readiness configuration was observed.
- An explicit rollback command succeeded.
- The healthy configuration was restored.
- Application health was independently rechecked.
- Restricted Pod Security Admission remained enabled.
- The original V2 policy binding was unchanged.

Outstanding:

- Docker Desktop and Minikube image IDs differed.
- Image provenance was not established end to end.
- Image-version rollback was not demonstrated.
- The custom V2 image-reference policy was not enforced
  in the separate rollback rehearsal namespace.
- Production rollback and data restoration were not tested.
- Temporary rehearsal namespace cleanup was verified on November 1, 2026.

Operational warning:

kubectl rollout undo reported that the
kubectl.kubernetes.io/last-applied-configuration annotation
was not updated. Future kubectl apply operations must be
reviewed to avoid unintentionally reapplying stale configuration.
## 6. Production Implications

Even a successful isolated rollback rehearsal will not
establish production rollback readiness.

Production readiness additionally requires approved
image digests, deployment authorization, application
health criteria, data compatibility, service continuity,
and tested recovery procedures in the target environment.

## 7. Residual Risk

Risk R06 in:
operations/residual-risk-register.csv

Status: OPEN.

Reason: End-to-end application rollback is not yet verified.

This risk remains open until appropriate rollback
evidence has been recorded and reviewed.

## 8. Final Laboratory Cleanup

Date: November 1, 2026.

The isolated Kubernetes rollback rehearsal concluded
with verified cleanup of ticket-010-rollback-lab.

Evidence:
- recovery/rollback-cleanup-verification.txt

Observed results:

- Temporary rollback namespace deletion: VERIFIED.
- Original ticket-010-lab resource inventory: UNCHANGED.
- Original V2 admission-policy binding: UNCHANGED.
- Six previously recorded recovery evidence files:
  SHA-256 integrity checks passed.
- Cleanup verification evidence: PRESERVED.

This cleanup confirms removal of the dedicated
Kubernetes rehearsal namespace. It does not establish
removal of locally cached container images or the
separate Docker registry container.

Residual risk R06 remains OPEN.

Image-version rollback, production recovery, and
end-to-end release provenance remain unverified.

## Conclusion
The investigation retains verified laboratory cleanup
and release-prevention evidence.

A Kubernetes configuration rollback was successfully
performed and independently verified in an isolated
laboratory namespace.

This is not proof of image-version rollback or
end-to-end production recovery.

Residual risk R06 remains OPEN pending broader
recovery validation and operational approval.

Production recovery readiness: NOT ESTABLISHED.