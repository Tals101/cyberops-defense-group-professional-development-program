# Ticket 012 — Consolidated Security Control Validation

## Control 1: Application destination allowlist

**Implementation:** Secured `ticket012-application-api:lab-v2`, approved path `http://internal-service:8080/resource`.  
**Negative test:** Unapproved application-mediated request returned **HTTP 403**, with security log.  
**Approved flow:** Returned `{"result":"authorized","data":"synthetic"}`.  
**Assessment:** **PASS for that application call path**, not for all code running inside the container.

## Control 2: Workload identity exposure reduction

**Implementation:** Dedicated `ticket012-application-api` ServiceAccount, `automountServiceAccountToken: false`, non-root, capability drop and privilege-escalation restrictions.  
**Observed:** `TOKEN_PRESENT=False` and authorized application call succeeded.  
**Assessment:** **PASS for preventing automatic Kubernetes API token mounting**, not proof of independently authenticated application identity.

## Enforcement gap: NetworkPolicy

**Test:** Temporary deny-all egress NetworkPolicy, matching application workload, on bridge-based Minikube CNI.  
**Observed:** Direct collector TCP connectivity remained **reachable**. Test policy removed after evidence capture.  
**Assessment:** **FAIL**. Configuration did not provide enforced egress isolation. A configured policy is not evidence of enforcement.

## Operational containment and restoration

Collector scaled 1 → 0 replicas; direct connection unavailable while approved application flow remained authorized; then collector restored to 1 ready replica. **PASS for this lab containment/restoration cycle**, without establishing network-level isolation.

## Final result and evidence

- Allowlist: PASS, scoped.
- ServiceAccount hardening: PASS, scoped.
- Approved application flow: PASS.
- Network isolation: FAIL, unresolved.
- Recovery: PASS operationally, but security recovery incomplete.
- Production readiness: **NO-GO**; closure: **NOT AUTHORIZED**.

See `combined-control-validation.md`, `operational-control-review.md`, `networkpolicy-enforcement-review.md`, `final-recovery-validation.md`, and `04-Adversarial-Validation/evidence/` for source observations.
