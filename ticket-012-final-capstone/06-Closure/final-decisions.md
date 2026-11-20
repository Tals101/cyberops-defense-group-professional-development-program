# Ticket 012 — Final Decisions and Authorization Record

**All incident-command decisions below are simulated recommendations, not actual approvals.** The engineering submission does not grant authority to modify production resources.

## Decision Point 1 — 09:05: Contain or preserve evidence?

**Observed/reported:** SOC unapproved outbound destination; IAM unexpected identity usage; changed deployment automation; no independently proven compromise.  
**Tradeoff:** Immediate isolation may reduce exposure but interrupt customer-facing service and destroy ephemeral evidence; delay may permit recurrence.  
**Recommendation:** Preserve and correlate evidence immediately, increase monitoring and prepare reversible containment; escalate if ongoing unauthorized activity is confirmed.  
**Authority:** Incident Commander plus platform owner before production containment.  
**Status:** PROPOSED, NOT AUTHORIZED. Details: `01-Incident-Management/decision-log.md`.

## Decision Point 2 — 10:20: Detection priority and deployment

**Finding:** V1: TP=5, FP=1, FN=7; V2: TP=12, FP=5, FN=0 in **24 synthetic labeled cases**. Evidence spans destination, claimed workload identity, and deployment timing.  
**Recommendation:** Maintain high *provisional* incident priority; investigate original destination, independently verified service identity, exception approval and deployment authorization. Do **not** deploy the detector operationally on these synthetic results alone.  
**Silent-failure risks:** missing network/deployment telemetry, clock skew, incorrect allowlist, identity ambiguity, approved exceptions, and small evaluation sample.  
**Status:** INVESTIGATION RECOMMENDATION ONLY.

## Decision Point 3 — 13:15: Restore previous deployment or remain isolated?

**Tradeoff:** Restore for service continuity versus potential recurrence of unauthorized connectivity. A rollback may restore an image while leaving network exposure unresolved.  
**Recommendation:** Preserve evidence, identify a known-good version, require controlled restore/rollback, validate both functionality and **security enforcement**; maintain containment or escalate if unauthorized connections persist.  
**Authority:** Incident Commander, Security Operations and platform owner for production action.  
**Status:** PROPOSED, NOT AUTHORIZED FOR PRODUCTION.

## Final Decision Point — 15:30

### A. Production readiness: **NO-GO**

Allowlist restriction and no-auto-mount ServiceAccount tests passed in their respective scopes; direct collector access remained reachable during the deny-all egress NetworkPolicy experiment. The detector produced synthetic false positives and does not independently authenticate identity.

**Conditions for reconsideration:** enforce egress restrictions with an appropriate CNI; verify allowed traffic passes and forbidden traffic fails; extend detector testing; obtain formal security/platform deployment authorization.

### B. Incident closure: **NOT READY FOR AUTHORIZED CLOSURE**

Operational containment, restoration and corrective rollback passed, but network enforcement remediation is outstanding, and simulated observations do not prove a real compromise or its cause.

**Conditions for reconsideration:** implement and document remediation, retest affected controls, resolve/approve residual risks through the authorized process, complete evidence review, and obtain actual Incident Commander sign-off.

**Conclusion:** Technical investigation is completed for this capstone; security remediation and actual incident closure are not completed. No simulated approval is represented as real authorization.
