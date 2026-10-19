# Ticket #009 — Automation Authority Model

## Purpose

This document defines which identity-remediation actions may occur automatically, which require human approval, and which should not be performed by unattended automation.

The classification is based on:

- quality and completeness of evidence;
- consequence of an incorrect decision;
- identity privilege;
- service dependencies;
- reversibility;
- speed of potential damage;
- recovery complexity;
- operational ownership.

An action is not classified as safe merely because it can technically be reversed.

---

# Category 1 — AUTO-REMEDIATE

## Qualification

An action may be automatically executed only when:

- evidence is complete and current;
- multiple independent signals agree;
- identity type is known;
- account ownership is known;
- no critical service dependency exists;
- privilege is low;
- lifecycle state supports the action;
- impact of an incorrect decision is limited;
- rollback is tested and reliable;
- the action remains within configured run-level limits.

## Required Confidence

High confidence.

The automation must have enough corroborating evidence that reasonable alternative explanations are unlikely.

A single inactivity field is not sufficient.

## Potential Impact if Wrong

Low and contained.

Incorrect remediation should not reasonably create:

- production outage;
- administrator lockout;
- loss of recovery capability;
- material business interruption.

## Rollback

Rollback must be:

- predefined;
- tested;
- logged;
- executable quickly.

## Speed of Damage

Damage should occur slowly enough that monitoring or automated validation can detect failure before broader impact occurs.

## Required Evidence

Examples include:

- current lifecycle data;
- identity type;
- owner;
- authentication history;
- data freshness;
- approval status;
- evidence completeness.

## Decision Owner

Security engineering owns the automation policy.

IAM owns identity lifecycle correctness.

Operational owners must define protected dependencies.

## Example Actions

Possible auto-remediation actions include:

- disabling a standard, non-privileged terminated workforce identity when authoritative HR termination data is current and corroborated;
- revoking an expired low-risk temporary entitlement when ownership and lifecycle data agree;
- removing a clearly expired non-critical access assignment with tested rollback.

---

# Category 2 — REQUIRE APPROVAL

## Qualification

Actions require approval when:

- the identity supports a service;
- the identity is privileged;
- operational dependencies exist;
- evidence contains ambiguity;
- several sources disagree;
- the potential impact is moderate or high;
- rollback may require coordination;
- business ownership must be confirmed.

Automation may detect, analyze, recommend, and stage these actions.

It may not independently perform the final state change.

## Required Confidence

Moderate to high confidence.

The system may strongly recommend remediation, but consequence or uncertainty prevents unattended enforcement.

## Potential Impact if Wrong

Examples include:

- application outage;
- service interruption;
- loss of administrative access;
- failed scheduled processing;
- business workflow disruption.

## Rollback

Rollback should exist, but the existence of rollback alone does not justify unattended execution.

Restoration may require:

- application-owner validation;
- credential restoration;
- token refresh;
- service restart;
- downstream recovery.

## Speed of Damage

Impact may occur immediately after the identity state changes.

Therefore approval must occur before execution.

## Required Evidence

Before approval, automation must provide:

- proposed action;
- identity type;
- owner;
- business purpose;
- privilege;
- interactive activity;
- non-interactive activity;
- service dependencies;
- lifecycle state;
- approval state;
- evidence completeness;
- data freshness;
- expected impact;
- rollback information.

## Decision Owner

Approval should come from an authorized owner appropriate to the risk.

Examples:

- IAM;
- application owner;
- infrastructure owner;
- security operations;
- designated privileged-access approver.

## Example Actions

Require approval for:

- disabling service accounts;
- disabling privileged identities;
- changing identities with production dependencies;
- remediating ambiguous identities;
- disabling accounts where evidence sources conflict;
- high-impact entitlement removal.

---

# Category 3 — DO NOT AUTOMATE

## Qualification

An action belongs in this category when:

- identity type cannot be established;
- critical evidence is missing;
- data cannot be trusted;
- rollback is uncertain;
- incorrect action could prevent incident recovery;
- consequences could be catastrophic;
- the automation cannot reliably determine downstream impact.

Automation may collect evidence and generate alerts.

It must not execute the final remediation.

## Required Confidence

Confidence is insufficient for unattended action regardless of the apparent rule match.

## Potential Impact if Wrong

Potential consequences include:

- organization-wide outage;
- loss of emergency access;
- disabling identity infrastructure;
- disabling security monitoring;
- loss of recovery capability;
- widespread administrator lockout.

## Rollback

Rollback may be:

- uncertain;
- slow;
- dependent on unavailable systems;
- dependent on the identity being changed.

Such conditions make unattended remediation inappropriate.

## Speed of Damage

Impact may be immediate and widespread.

Damage may occur faster than operators can detect and reverse it.

## Required Evidence

Automation may gather:

- identity information;
- dependency data;
- authentication history;
- privilege;
- configuration state;
- risk indicators.

However, evidence gathering must not automatically grant remediation authority.

## Decision Owner

A specifically authorized human decision maker or formal emergency process owns the action.

## Example Actions

Do not automate unattended:

- disabling break-glass identities;
- disabling core IAM platform identities;
- disabling identities required to operate the recovery mechanism;
- disabling identities when identity type is unknown and privilege is high;
- destructive identity deletion where rollback is uncertain;
- mass remediation beyond configured safety limits.

---

# Authority Escalation Principle

Automation authority decreases as:

- privilege increases;
- dependency increases;
- uncertainty increases;
- blast radius increases;
- rollback confidence decreases.

Automation authority increases only when:

- evidence quality improves;
- impact is bounded;
- rollback is proven;
- dependencies are understood;
- monitoring can validate the result.

---

# Detection Is Not Authorization

A detection rule may correctly identify risk without being authorized to remediate it automatically.

V2 must therefore separate:

1. detection;
2. evidence collection;
3. classification;
4. recommendation;
5. approval;
6. enforcement;
7. validation;
8. rollback.

A positive detection is not itself permission to change production state.

---

# Proposed V2 Authority Boundary

## V2 May Automatically

- collect identity context;
- evaluate risk indicators;
- classify confidence;
- generate remediation recommendations;
- create pre-change snapshots;
- perform low-impact actions explicitly classified as AUTO-REMEDIATE;
- verify post-change health;
- halt further actions when safety conditions fail.

## V2 May Recommend but Not Automatically Execute

- service-account disablement;
- privileged-account disablement;
- remediation where service dependencies exist;
- remediation with conflicting evidence;
- remediation with incomplete ownership information;
- high-impact entitlement changes.

## V2 Must Never Perform Unattended

- destructive identity deletion;
- break-glass account disablement;
- remediation beyond configured run limits;
- high-impact changes when rollback capability is unavailable;
- changes when required logging is unavailable;
- changes involving an unrecognized identity type;
- changes when critical evidence is missing.

---

# Safe Authority Principle

The amount of authority granted to automation must be proportional to:

- confidence in the decision;
- quality of the evidence;
- reversibility of the action;
- consequence of being wrong.

V1 violated this principle.

V2 must enforce it.
