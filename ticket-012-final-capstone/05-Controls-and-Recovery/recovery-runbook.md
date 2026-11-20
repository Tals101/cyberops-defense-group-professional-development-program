# Ticket 012 — Recovery and Rollback Runbook

**Scope:** Simulated/local Minikube only. The historic disposable `ticket012-rollback-probe` was deleted after testing. Do not execute probe-specific commands against existing application workloads.

## Entry/authorization gates

Preserve all pre-change evidence, identify known-good image and configuration, document impact, confirm relevant owner and Incident Commander approval for real production rollback, and define functional/security acceptance checks. **Ready pods do not prove safe recovery**.

## Failure signals

Inspect desired/ready/updated replica counts, image tags, ReplicaSets, pod status, Kubernetes events, application flow and security-control enforcement:

    kubectl -n ticket-012-lab get deployments -o wide
    kubectl -n ticket-012-lab get pods -o wide
    kubectl -n ticket-012-lab get events --sort-by=.lastTimestamp

Treat `ErrImagePull`, `ImagePullBackOff`, wrong image, failed rollout, broken approved flow, or unblocked unapproved egress as failures or incomplete recovery.

## Observed operational validation

A disposable test deployment started with `ticket012-unapproved-collector:lab-v1`. An update to nonexistent `example.invalid/ticket012-missing:lab-v2` caused **ImagePullBackOff** on the new pod while the old ready pod remained. An attempted `rollout undo --to-revision=999` returned error (invalid operator-selected revision). A normal `rollout undo` restored the known-good image, one ready replica and one updated replica. The disposable deployment was deleted; three original deployments were verified at 1/1 ready. This was **not** a control-plane rollback failure or a demonstrated complete service outage.

Historical example, **do not run now** because probe was deleted:

    kubectl -n ticket-012-lab rollout history deployment/ticket012-rollback-probe
    kubectl -n ticket-012-lab rollout undo deployment/ticket012-rollback-probe
    kubectl -n ticket-012-lab rollout status deployment/ticket012-rollback-probe

## Recovery acceptance checklist

Confirm known-good image, original configuration and service-account policy; verify ready *and updated* replicas; verify approved application behavior; verify logging/detection; independently verify that disallowed traffic is blocked; preserve rollback history, outcomes and authorization records. If outbound isolation remains unenforced, mark **security recovery incomplete**, even when operational recovery passes.

## Evidence and decision

`04-Adversarial-Validation/evidence/rollback-failure-recovery-results.txt`, `rollback-recovered-status.txt`, `rollback-probe-rollout-history.txt`, `05-Controls-and-Recovery/final-recovery-validation.md`. Operational recovery PASS; egress remediation OUTSTANDING; production **NO-GO**; incident closure **NOT AUTHORIZED**.
