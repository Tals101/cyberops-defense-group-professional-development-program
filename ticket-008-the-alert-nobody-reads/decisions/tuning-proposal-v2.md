# Ticket #008 — Tuning Proposal V2

## Phase 6 — V2 Design

## Purpose

V2 will reduce remaining analyst workload through case-level correlation rather than source suppression.

V1 reduced baseline noise substantially, but several V1 alerts can still represent the same logical investigation.

V2 will preserve familiar internal-source visibility because Ticket #008 demonstrated that familiar does not necessarily mean benign.

The manager's proposed blanket familiar-address suppression will not be implemented.

---

# Lessons Carried Forward

## Baseline

The original detector produced 597 alerts, including substantial duplication and benign noise.

Individual authentication events could generate several alerts for the same underlying behavior.

## V1

V1 reduced alert volume to 15 while retaining all six seeded suspicious scenarios.

V1 also detected both suspicious success-after-failure transitions missed by the baseline.

However, V1 still produced multiple investigation units for some single logical incidents.

Examples include:

- six separate V1-03 alerts for the distributed password-spray campaign;
- multiple alerts for SUS-02 describing rapid failures, privileged activity, and later successful authentication;
- multiple alerts for SUS-05 describing repeated failures and later successful authentication.

## Alert Review

Analysts need an answer to the question:

"Do I need to act on this activity?"

Several related signals presented separately still require the analyst to reconstruct one investigation manually.

## Manager Suppression Request

Blanket suppression of familiar internal addresses is rejected.

Internal does not automatically mean trusted.

Familiar does not automatically mean benign.

SUS-05 demonstrates that malicious authentication activity can originate from a familiar internal source.

---

# V2 Design Principle

V2 will consolidate related security signals into investigation cases.

The detector will retain the individual risk signals as case context while avoiding separate alerts when the signals belong to the same logical incident.

No user, source, account, internal network, or service account will be globally whitelisted.

---

# Proposed V2 Correlation

## V2-01 — Authentication Attack Sequence

Combine related same-user and same-source authentication signals into one investigation case when they occur within the same correlated sequence.

A case may contain one or more of the following signals:

- rapid repeated failures;
- privileged-account risk;
- unfamiliar-source context;
- suspicious success after failures;
- low-and-slow privileged activity.

A later suspicious success should update the existing case rather than create an unrelated second investigation.

The case must explicitly record that the successful authentication occurred.

---

## V2-02 — Password Spray Campaign

Correlate qualifying one-source-to-many-user spray detections into a broader campaign investigation when the source-specific activity occurs within the same campaign time range.

The campaign should include:

- all participating sources;
- all targeted users;
- total failures;
- first and last observed timestamps;
- source familiarity;
- privileged-account involvement, if present.

The purpose is to avoid presenting each participating spray source as an independent incident when the activity is part of one coordinated campaign.

---

## V2-03 — Distributed Targeting Case

Preserve many-sources-to-one-user detection.

Correlate the activity into one investigation case containing all participating sources and the targeted account.

---

## V2-04 — Persistent Service Authentication Case

Preserve persistent service-account failure visibility.

Continue grouping repetitive stable failures into one investigation case.

Do not whitelist the service account or its source.

Material changes in source, authentication outcome, privilege, or attack pattern must remain available for separate escalation.

---

# Familiar Internal Sources

V2 will not suppress alerts solely because a source is familiar or internal.

Source familiarity will remain contextual information.

A familiar source may reduce uncertainty in some investigations, but it will not override behavioral evidence.

This preserves coverage for compromised internal hosts and credential abuse.

---

# Expected Benefit

V2 should reduce the remaining duplicate investigation effort in V1.

The largest expected reductions are:

- six separate password-spray source alerts consolidated into campaign-level visibility;
- multiple alerts describing the same user/source compromise sequence consolidated into one case;
- reduced manual reconstruction of relationships between related alerts.

V2 should therefore create fewer analyst investigation units while retaining the security meaning contained in V1.

---

# Expected Cost

V2 introduces additional correlation logic.

Cases will contain more context than individual alerts and may require more careful state handling.

The detector must correctly decide when signals belong to the same investigation and when they represent separate incidents.

Over-correlation could incorrectly merge unrelated attacks.

---

# Expected Coverage Change

Target suspicious scenario coverage:

6 of 6.

Target suspicious success-after-failure coverage:

2 of 2.

V2 should preserve:

- concentrated brute force;
- privileged failure followed by success;
- password spray;
- low-and-slow privileged attack;
- compromised familiar source;
- distributed targeting.

No coverage reduction is expected from familiar-source suppression because no such suppression will be implemented.

---

# Residual Risk

V2 may still miss attacks that remain below the underlying V1 correlation conditions.

Residual risks include:

- fewer than five rapid failures;
- spray activity against fewer than five users;
- distributed targeting from fewer than three sources;
- activity spread outside the defined correlation windows;
- attack behavior that resembles stable service-account failure;
- incorrect case merging when unrelated activity overlaps in time;
- incorrect case separation when one campaign operates over a longer period.

Underlying telemetry must remain available even when an event does not create its own investigation case.

---

# Success Metrics

V2 will be considered successful on the frozen Ticket #008 dataset only if all of the following are true:

1. Total V2 investigation cases are fewer than V1's 15 alerts.
2. All 6 suspicious scenarios remain detected.
3. Suspicious scenarios completely missed remain 0.
4. Both suspicious successful-authentication transitions remain explicitly represented.
5. Benign-only investigation cases do not exceed V1's 1.
6. No familiar/internal source, user, service account, or network is globally suppressed or whitelisted.
7. Password-spray campaign alerting is less fragmented than V1's six separate V1-03 alerts.
8. Multiple security signals belonging to the same authentication sequence are consolidated without losing their risk context.
9. Estimated analyst workload is lower than V1's 1.25 hours using the same five-minute-per-investigation assumption.
10. Any decrease in event-level representation or scenario coverage is documented rather than hidden.

Alert count alone will not determine whether V2 is better.

---

# Pre-Implementation Status

V2 design is documented.

V2 has not been implemented.

V2 has not been executed.

The frozen 1,000-event dataset remains unchanged.

The original detector and V1 remain preserved.
