# Ticket 012 — Containment Runbook

**Scope:** Authorized local Minikube laboratory only; historic target `unapproved-collector` in `ticket-012-lab`. Not a production authorization.

## Authority and safety gates

Before production containment, obtain explicit authorization from Incident Commander and relevant platform owner. The Ticket #012 incident decisions are **simulated**, not approvals. Confirm the cluster context and namespace; preserve the deployment manifest, ReplicaSet state, pods, logs, events, network observations and timestamps; identify service availability impact. Record original replica count and rollback command before modifying anything.

## Observed laboratory procedure

Only execute in a disposable lab after checking context:

    $ns = 'ticket-012-lab'
    if ((kubectl config current-context) -ne 'minikube') { throw 'Wrong cluster context' }
    kubectl -n $ns get deployment unapproved-collector -o yaml
    kubectl -n $ns get pods -o wide
    $original = kubectl -n $ns get deployment unapproved-collector -o jsonpath='{.spec.replicas}'
    kubectl -n $ns scale deployment/unapproved-collector --replicas=0
    kubectl -n $ns get deployment unapproved-collector

**Validate** that direct collector connectivity fails; verify authorized application-to-internal-service requests still work; record any unexpected errors. A desired-replica count alone does not demonstrate containment. Do not assume that collector removal blocks other unauthorized destinations.

## Restore only when authorized

    kubectl -n ticket-012-lab scale deployment/unapproved-collector --replicas=1
    kubectl -n ticket-012-lab rollout status deployment/unapproved-collector

The original historical replica count was 1. For any future run, restore the **captured** original count rather than assuming it is 1. Preserve before/after outputs.

## Recurrence, escalation and decision

Monitor unauthorized destinations, allowlist rejections, deployment changes, identity ambiguity, and collector reachability. If unauthorized destinations remain reachable, escalate and retain **NO-GO**; the tested NetworkPolicy was not enforcing. Historical result: containment PASS, approved flow PASS, restoration PASS; **no production containment** was performed. Evidence: `04-Adversarial-Validation/evidence/containment-restoration-results.txt`.
