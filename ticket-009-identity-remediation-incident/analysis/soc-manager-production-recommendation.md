# Ticket #009 — SOC Manager Production Recommendation

## Recommendation

**NO — do not restore full unattended account disabling tomorrow morning.**

The recommended operating model is:

**Detection + recommendation + approval-gated remediation**

with only non-destructive automated actions permitted without human approval.

---

# What Authority I Am Willing to Give the System

Tomorrow morning, the automation may automatically:

- collect identity context;
- evaluate identity lifecycle signals;
- compare primary and secondary evidence;
- calculate decision confidence;
- calculate evidence trust;
- identify conflicting or incomplete evidence;
- recommend remediation;
- explain the reason for the recommendation;
- classify the required authority;
- stage a proposed action;
- create audit evidence;
- preserve snapshots;
- run health checks;
- identify actions requiring approval.

The automation may also automatically decide to:

- take no action;
- keep an account enabled;
- block an unsafe action;
- defer an action;
- escalate a decision for review.

These activities do not require destructive production authority.

---

# What Authority I Am Not Willing to Give the System

I am not recommending unrestricted authority to automatically disable production identities.

In particular, the system must not automatically disable identities when:

- evidence is conflicting;
- evidence is incomplete;
- evidence is stale;
- identity type is unknown;
- business purpose is uncertain;
- application dependencies exist;
- privilege is elevated;
- the account is a service or integration identity;
- secondary evidence is unavailable;
- rollback capability is unavailable;
- logging is unavailable;
- emergency stop is active;
- the action exceeds the configured blast-radius limit.

---

# Why

V1 demonstrated that technically correct execution of oversimplified logic can disable a legitimate production dependency.

V2 substantially improved decision quality, authority boundaries, rollback, action limits, auditability, and fail-safe behavior.

However, the emergency payroll test revealed another failure mode:

> Correct logic can still produce an unsafe remediation recommendation when the source data is wrong.

V3 successfully detected that condition.

For `payroll.emergency`:

- primary IAM evidence indicated an inactive employee identity;
- the policy recommendation was `DISABLE`;
- decision confidence was `HIGH`;
- secondary evidence identified an active critical payroll integration;
- evidence trust became `CONFLICTING`;
- authority was reduced to `REQUIRE_APPROVAL`;
- no automatic change occurred.

This is evidence that full unattended remediation remains inappropriate.

---

# Evidence Supporting the Recommendation

The recommendation is based on the following completed work:

## V1

V1 disabled identities using stale interactive-login logic without sufficient service context.

It incorrectly disabled legitimate service identities, including the Finance dependency that caused the simulated incident.

## V2

V2 added:

- identity context;
- authority classes;
- dry-run capability;
- approval boundaries;
- maximum actions per run;
- persistent deferred-action controls;
- emergency stop;
- audit requirements;
- snapshots;
- health validation;
- rollback capability.

Testing demonstrated meaningful safety improvement.

## V3

V3 added:

- independent secondary context;
- evidence corroboration;
- evidence-trust classification;
- separation of decision confidence from evidence trust.

The emergency payroll test demonstrated that V3 can prevent a HIGH-confidence destructive recommendation from receiving unattended authority when evidence conflicts.

---

# What Can Safely Run Tomorrow

## Automatic

The system may automatically:

- detect;
- evaluate;
- correlate;
- score;
- classify;
- explain;
- recommend;
- preserve evidence;
- stage proposed remediation;
- block unsafe remediation.

## Human Approval Required

A person must approve destructive production remediation.

This includes account disabling until the remaining production-readiness controls have been fully tested.

High-impact identities must remain approval-gated regardless of policy recommendation.

## Prohibited

The automation must not:

- approve its own high-impact actions;
- override conflicting evidence;
- treat missing data as evidence that an account is safe to disable;
- exceed configured action limits;
- bypass logging;
- bypass snapshot or rollback requirements;
- disable protected identity classes without required approval.

---

# Remaining Risk

Residual risk remains because:

- multiple sources can agree and still be wrong;
- application dependencies may be undocumented;
- inventories may become stale;
- attackers may manipulate trusted information;
- approval decisions may be incorrect;
- automation credentials may be compromised;
- rollback itself may fail;
- repeated or interrupted execution may expose additional failure modes.

These risks have not yet all been fully exercised in the remaining ticket phases.

---

# Who Accepts the Risk

The automation does not accept business risk.

Production risk must be accepted by the appropriate accountable human authority.

Depending on the identity and potential impact, that may include:

- IAM ownership;
- application ownership;
- Security Engineering;
- SOC management;
- business service ownership.

High-impact remediation must have an identifiable human approver.

---

# What Must Happen Before Expanding Automation Authority

Before unattended destructive authority is expanded, the system must successfully complete:

1. controlled rollback testing;
2. rollback-failure escalation testing;
3. failure-injection testing;
4. interrupted-execution testing;
5. failed-remediation testing;
6. approval-timeout testing;
7. repeated-execution/idempotency validation;
8. adversarial manipulation testing;
9. automation credential and least-privilege analysis;
10. operator-experience validation;
11. safeguard and failure-mode review;
12. production operations planning;
13. final management approval.

Only after those controls are demonstrated should limited unattended destructive remediation be reconsidered.

---

# Final Recommendation for Tomorrow Morning

**Do not restore full automatic account disabling.**

Restore the automation in a controlled operating mode that permits:

**Detection → Corroboration → Recommendation → Staging → Human Approval → Remediation**

The system may make automatic non-destructive decisions and may refuse unsafe actions.

Destructive production changes remain human-approved.

This recommendation preserves the operational value of the automation without granting it more production authority than the current evidence supports.
