# Ticket #007 — Delegation Review

## Issue A — SOC Analyst Rapid Verification

**Objective Clear:** Yes. Identify the unfamiliar source IP, verify whether the sysadmin login was expected, and check for related alerts.

**Sufficient Authority:** Yes. The work required read-only SOC and asset information.

**Useful Information Returned:** Yes. The source was ultimately tied to an administrator workstation and later confirmed as authorized maintenance.

**Unnecessary Duplication:** No. The delegation allowed Issue A to progress while I investigated Issue B.

**Delegated Too Late:** No. It was delegated during initial triage.

**Should I Have Delegated More:** The administrator-maintenance confirmation could also have been assigned earlier to Infrastructure Operations.

**Follow-Up Appropriate:** Yes. I reassessed Issue A when the analyst reported the active session and privileged commands.

---

## Issue C — IT Operations Validation and Rollback

**Objective Clear:** Yes. Preserve logs, correlate the configuration change with the errors, prepare rollback, and report whether service recovered.

**Sufficient Authority:** Yes. Operations owned the configuration and service restoration.

**Useful Information Returned:** Yes. Rollback caused portal error rates to return toward baseline.

**Unnecessary Duplication:** No. Security focused on malicious-traffic questions while Operations handled restoration.

**Delegated Too Late:** No. Operations was already engaged when Issue C arrived.

**Should I Have Delegated More:** Security could have requested a more formal post-rollback health summary earlier.

**Follow-Up Appropriate:** Yes. Security retained unusual-request review after rollback.

---

## HR-LT-51 — Additional Engineer

**Objective Clear:** Yes. Determine whether HR-LT-51 showed evidence of the same or related malicious activity as HR-LT-44.

**Sufficient Authority:** Yes. The engineer could collect evidence and perform read-only investigation but required approval for disruptive containment.

**Useful Information Returned:** Yes. HR-LT-51 contacted the same destination but did not show the Word-to-PowerShell chain, persistence, credential-access indicators, or suspicious authentication activity.

**Unnecessary Duplication:** No. The assignment allowed parallel scope validation while I retained ownership of HR-LT-44 and incident coordination.

**Delegated Too Late:** No. The additional engineer was requested when the second-host alert materially expanded possible scope.

**Did I Retain Something I Should Have Delegated:** Environment-wide destination searching could also have been assigned to Network Engineering earlier.

**Follow-Up Appropriate:** Yes. The returned findings were incorporated into the scope decision and prevented unnecessary containment of HR-LT-51.

---

## Overall Delegation Assessment

Delegation was most effective when assignments were narrow, evidence-driven, and paired with clear escalation conditions.

I retained responsibility for prioritization, containment decisions, incident scope, and coordination while delegating bounded evidence collection and operational tasks.
