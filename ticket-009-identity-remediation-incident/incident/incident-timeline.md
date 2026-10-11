# Ticket #009 — Incident Timeline

## Purpose

This timeline records confirmed events, reasonable inferences, and unresolved questions related to the identity-remediation incident.

Each event is classified as:

- **Known Fact** — directly supported by available incident information or preserved evidence.
- **Inference** — a reasonable conclusion that has not yet been independently verified.
- **Unknown** — information that remains unresolved and requires investigation.

---

## Timeline

### Before 08:52

**Classification:** Unknown

The state of the remediation system immediately before execution has not yet been reconstructed.

Unknown items include:

- what identity dataset the automation received;
- when that dataset was last refreshed;
- whether the affected service account had recently changed state;
- whether account ownership or dependency information was available;
- whether the remediation rule had recently changed;
- whether previous runs had produced warnings or incorrect decisions;
- whether any approval or review occurred before this run.

These questions must be answered during reconstruction.

---

### 08:52 — Identity-Remediation Job Begins

**Classification:** Known Fact

The automated identity-remediation job began execution at 08:52.

At this stage, the following remain unknown:

- number of accounts evaluated;
- number of accounts selected for remediation;
- exact order of account processing;
- identity attributes considered;
- whether the service account had already been selected;
- whether changes occurred immediately or later during the run.

---

### 08:52–08:57 — Remediation Activity Occurs

**Classification:** Inference

IAM reports that a service account was disabled during the remediation run.

It is therefore reasonable to infer that at least one production identity change occurred during this interval.

The exact timestamp of the account change must be established from audit logs.

It is not yet known whether additional accounts were changed.

---

### 08:57 — Finance Operations Reports Application Failures

**Classification:** Known Fact

Finance Operations began reporting failures in an internal application at approximately 08:57.

The timing is consistent with the identity-remediation activity.

However, temporal proximity alone does not prove causation.

---

### Approximately 08:57–09:07 — Initial IAM Correlation

**Classification:** Known Fact / Time Partially Unknown

IAM determined that a service account had been disabled during the remediation run.

The exact time IAM made this determination is currently unknown.

IAM also reported that the automation performed the action required by its configured rule.

This indicates that the incident may involve a failure of decision context, authority boundaries, safeguards, or production controls rather than a simple execution error.

---

### 09:07 — SOC Assigned Incident Ownership

**Classification:** Known Fact

The SOC Manager assigned incident ownership at 09:07.

Initial instructions were:

- restore the affected service;
- determine why the automation believed the action was correct;
- determine why an incorrect decision was allowed to become a production change;
- evaluate whether the automation should ever run unattended again.

---

### After 09:07 — Immediate Containment Required

**Classification:** Required Response Action

The identity-remediation automation must be prevented from making additional production changes until its execution state and scheduling are known.

Evidence must be preserved before modifying automation logic.

---

## Current Causation Assessment

The working hypothesis is:

1. the 08:52 automation evaluated the service account;
2. its rule classified the account as requiring remediation;
3. the automation had sufficient production authority to disable the account;
4. the Finance application depended on that identity;
5. application failures became visible shortly afterward.

**Classification:** Inference

This hypothesis is plausible but has not yet been proven.

Evidence required to confirm or reject it includes:

- remediation decision logs;
- identity audit logs;
- account-state history;
- application dependency information;
- application authentication failures;
- service recovery results after account restoration.

---

## Key Timeline Gaps

The investigation must determine:

- exact time the service account was evaluated;
- exact time the disable operation occurred;
- exact account identifier;
- all other accounts evaluated;
- all other accounts changed;
- first application authentication failure;
- first application error;
- time IAM identified the account change;
- time containment was implemented;
- time account restoration occurred;
- time application recovery was verified.

These events will be added to the timeline as evidence is generated or discovered.
