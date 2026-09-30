# Ticket #008 — Detection Drift Analysis

## Purpose

Explain why an authentication detection that performs well today may become noisy, ineffective, or misleading over time.

Detection quality is not permanent.

Changes in users, infrastructure, authentication technology, business processes, telemetry, and attacker behavior can alter the meaning of the same detection logic.

---

# What Is Detection Drift?

Detection drift occurs when the environment changes enough that previously validated detection assumptions no longer match operational reality.

The detection code may remain unchanged while:

- benign behavior changes;
- malicious behavior changes;
- telemetry changes;
- enrichment changes;
- infrastructure changes;
- analyst workload changes.

As a result, a detection may produce:

- more false positives;
- more false negatives;
- misleading severity;
- poor grouping;
- missing context;
- reduced analyst trust.

---

# Why Ticket #008 Is Vulnerable to Drift

The V1/V2 strategy depends on several assumptions.

These include:

- authentication events are consistently logged;
- usernames remain stable identifiers;
- source addresses provide useful context;
- privilege information is accurate;
- source familiarity remains meaningful;
- thresholds continue to separate common benign behavior from suspicious activity;
- correlation windows remain operationally appropriate;
- V1 alerts continue to represent useful signals for V2.

Any of these assumptions may change.

---

# Workforce Changes

## Potential Changes

Examples include:

- workforce growth;
- workforce reduction;
- seasonal employees;
- remote-work expansion;
- return-to-office changes;
- contractor growth;
- acquisitions;
- new business units;
- changes in shift schedules.

## Possible Detection Impact

Workforce changes may alter:

- normal login frequency;
- failure rates;
- source diversity;
- account volume;
- geographic patterns;
- time-of-day patterns.

A threshold that once represented unusual behavior may become normal.

The opposite can also occur.

---

# Remote Work and VPN Changes

## Potential Changes

Examples include:

- new VPN gateways;
- cloud VPN services;
- split tunneling;
- zero-trust access platforms;
- shared egress infrastructure;
- new remote-access providers.

## Possible Detection Impact

Many users may begin appearing from:

- common shared sources;
- rotating addresses;
- unfamiliar networks;
- cloud-hosted access infrastructure.

This can affect:

- source familiarity;
- one-source/many-user logic;
- source-based correlation;
- perceived attack distribution.

A previously suspicious many-user source may become normal after a network architecture change.

---

# Identity Provider Changes

## Potential Changes

Examples include:

- migration between identity providers;
- multiple identity providers;
- federation changes;
- new SSO applications;
- conditional-access changes.

## Possible Detection Impact

Telemetry fields may change.

Examples include:

- username format;
- source representation;
- success/failure terminology;
- application identifiers;
- privilege context;
- event timing.

Rules may stop firing even though authentication activity continues.

---

# MFA Changes

## Potential Changes

Examples include:

- broader MFA deployment;
- new MFA provider;
- push authentication;
- hardware tokens;
- risk-based MFA;
- number matching.

## Possible Detection Impact

Authentication failure meaning may change.

A failed event may represent:

- wrong password;
- rejected MFA;
- expired challenge;
- device-registration issue;
- user cancellation.

Raw failure counts may become less meaningful unless event context is preserved.

---

# Passwordless Authentication

## Potential Changes

Examples include:

- passkeys;
- FIDO2;
- certificate authentication;
- device-based authentication;
- biometrics.

## Possible Detection Impact

Password-failure patterns may decline substantially.

A rule designed around repeated password failures could become less useful even while account-takeover risk remains.

Detection strategy may need to shift toward:

- device anomalies;
- token abuse;
- suspicious session creation;
- unfamiliar authentication methods;
- unusual identity-provider behavior.

---

# Service-Account Changes

## Potential Changes

Examples include:

- automation growth;
- service-account consolidation;
- credential rotation;
- managed identities;
- application migrations.

## Possible Detection Impact

A pattern like LEG-03 may:

- disappear;
- increase;
- change source;
- change timing;
- involve multiple hosts.

A service-account pattern previously understood as benign could become suspicious after architecture changes.

A previously suspicious service-account pattern could become expected business behavior.

---

# Cloud Migration

## Potential Changes

Examples include:

- application migration to cloud platforms;
- SaaS adoption;
- hybrid identity;
- cloud-hosted desktops;
- cloud-native services.

## Possible Detection Impact

Authentication may originate from:

- shared cloud addresses;
- provider infrastructure;
- proxy services;
- federated identity systems.

Traditional source-IP assumptions may become weaker.

---

# Network Redesign

## Potential Changes

Examples include:

- NAT changes;
- proxy deployment;
- new segmentation;
- new egress gateways;
- SD-WAN;
- zero-trust network access.

## Possible Detection Impact

Multiple endpoints may suddenly appear from one address.

One endpoint may appear from many addresses.

This can directly affect:

- V1-03 one-source/many-user logic;
- V1-04 many-source/one-user logic;
- source familiarity;
- V2 grouping.

---

# Logging and Schema Changes

## Potential Changes

Examples include:

- field renaming;
- timestamp format changes;
- dropped fields;
- new event IDs;
- normalized schemas;
- ingestion delay;
- duplicate ingestion.

## Possible Detection Impact

This can cause:

- silent detector failure;
- duplicate alerts;
- incorrect counts;
- broken time windows;
- missing privilege context;
- false unfamiliar-source classifications.

Telemetry drift can look like improved detection health if alert volume simply drops.

---

# Source Familiarity Drift

Source familiarity is particularly vulnerable to environmental change.

A source marked familiar today may become:

- decommissioned;
- reassigned;
- compromised;
- shared by more users;
- replaced by dynamic addressing.

A source marked unfamiliar today may become part of normal operations tomorrow.

Therefore:

`familiar` must remain context, not trust.

Familiarity logic should be periodically recalculated and validated.

---

# Threshold Drift

Current thresholds were validated against the Ticket #008 dataset and adversarial tests.

Examples include:

- 5 failures within 10 minutes;
- 5 distinct users within 120 minutes;
- 3 distinct sources within 60 minutes;
- 4 privileged failures within 120 minutes.

These thresholds should not be treated as universal constants.

They may drift because of:

- higher user population;
- application changes;
- authentication retries;
- automation;
- attack-rate changes;
- new infrastructure.

Threshold review should use observed operational data rather than intuition alone.

---

# Time-Window Drift

Attackers may deliberately change timing to avoid correlation windows.

Business processes may also become slower or faster.

Examples:

- attacks spread across days;
- automated systems retry less frequently;
- cloud authentication introduces delayed events;
- new applications create bursts of benign failures.

Time windows must therefore be periodically revalidated.

---

# Attacker Tradecraft Drift

Attackers adapt to detections.

Possible changes include:

- threshold skimming;
- source rotation;
- username rotation;
- longer time intervals;
- compromised familiar endpoints;
- residential proxies;
- cloud-hosted infrastructure;
- token theft;
- session hijacking;
- MFA fatigue;
- passwordless authentication abuse.

Ticket #008 adversarial testing already demonstrated that distributed activity can evade the current analytical perspective.

Future attacker behavior may create additional blind spots.

---

# Analyst Behavior Drift

Detection performance also depends on analyst behavior.

Warning signs include:

- rapid repetitive closures;
- investigation shortcuts;
- ignored low-severity cases;
- overreliance on source familiarity;
- assumption that repeated alerts are always benign;
- growing backlog.

An alert can remain technically accurate while becoming operationally ineffective.

---

# Business Process Drift

New business workflows may resemble suspicious behavior.

Examples include:

- bulk account provisioning;
- migration testing;
- password resets;
- new monitoring tools;
- automated inventory systems;
- penetration testing;
- vendor access.

These changes can create new benign patterns that were absent during original validation.

---

# Severity Drift

Severity assumptions can also change.

For example:

- a formerly standard account may become privileged;
- an application may become business critical;
- a source network may become higher risk;
- successful authentication may have different impact depending on system sensitivity.

Severity must reflect current context, not only historical rule definitions.

---

# Case-Correlation Drift

V2 depends on V1 alerts.

Therefore:

- weaker V1 output reduces V2 visibility;
- noisy V1 output can distort V2 grouping;
- missing fields can break correlation;
- changed source identity can split one campaign;
- shared infrastructure can over-merge unrelated activity.

V2 health must be evaluated together with V1 health.

---

# Drift Indicators

Potential drift indicators include:

- sudden alert-volume change;
- sudden case-volume change;
- large increase in benign dispositions;
- disappearance of a rule that historically fired;
- unexpected growth in one rule;
- increase in missing enrichment;
- increased analyst complaints;
- higher triage time;
- more duplicate cases;
- new incident misses;
- Purple Team evasion success;
- unusual changes in source diversity;
- unusual changes in user diversity.

---

# Drift Review Questions

During periodic review, ask:

1. Has authentication volume materially changed?
2. Has the workforce changed?
3. Has remote access changed?
4. Has identity infrastructure changed?
5. Has MFA changed?
6. Has passwordless authentication expanded?
7. Have service accounts changed?
8. Has network architecture changed?
9. Have logging fields changed?
10. Has source familiarity remained reliable?
11. Are thresholds still meaningful?
12. Are time windows still meaningful?
13. Are analysts still investigating cases?
14. Are duplicate cases increasing?
15. Have new false negatives appeared?
16. Have attacker techniques changed?
17. Are successful authentications still visible?
18. Is privileged-account context accurate?
19. Is V2 still receiving valid V1 signals?
20. Does the detection still reduce analyst workload without unacceptable coverage loss?

---

# Drift Response

If meaningful drift is identified:

1. Preserve the current detection version.
2. Document the environmental change.
3. Measure the operational effect.
4. Reevaluate assumptions.
5. Create a testable change proposal.
6. Define expected benefits and risks.
7. Test against current benign activity.
8. Test against known suspicious scenarios.
9. Rerun adversarial tests.
10. Compare results before deployment.

Do not respond to drift with undocumented threshold changes or broad suppression.

---

# Relationship to Known Ticket #008 Blind Spots

The current documented blind spots include:

- threshold skimming;
- distributed many-user/many-source activity;
- sub-threshold suspicious successes;
- attacks visible only through broader historical context.

Detection drift could make these blind spots larger.

It could also introduce entirely new blind spots.

For that reason, the false-negative register must be treated as a living operational artifact.

---

# Production Implication

A good detection today is not automatically a good detection six months from now.

Production readiness therefore requires:

- scheduled health review;
- drift monitoring;
- analyst feedback;
- adversarial retesting;
- version control;
- rollback capability;
- continued false-negative tracking.

Detection engineering is an ongoing lifecycle rather than a one-time tuning exercise.

---

# Phase 9 Status

Detection Drift Analysis completed.

The Detection Operations Plan and Detection Drift Analysis together define how Ticket #008 should be maintained after deployment.
