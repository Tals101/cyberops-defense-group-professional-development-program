# Ticket #008 — Detection Operations Plan

## Purpose

Define how the authentication detections will be operated, reviewed, changed, monitored, and retired after deployment.

The goal is to ensure that the tuned detections remain useful over time rather than becoming another source of ignored alerts.

---

# Detection Scope

This operations plan applies to:

- V1 authentication detections;
- V2 correlation logic;
- analyst-facing authentication cases;
- future complementary authentication detections created to address documented blind spots.

The plan does not assume that one detector will cover every authentication-abuse technique.

---

# Detection Owner

Primary owner:

SOC Detection Engineering

Operational partners:

- SOC Operations;
- Identity and Access Management;
- Endpoint Security;
- Infrastructure / Platform Operations;
- Incident Response.

The Detection Engineering owner is responsible for maintaining detection logic and measurement.

SOC Operations provides analyst feedback regarding alert usefulness, confusion, false positives, duplicate cases, and investigation burden.

---

# Review Frequency

## Routine Review

Review detection health at least monthly.

The review should include:

- alert and case volume;
- benign-case rate;
- suspicious-case rate when ground truth is available;
- analyst disposition trends;
- duplicate or redundant cases;
- successful-authentication cases;
- privileged-account cases;
- rule-specific volume;
- data-quality issues;
- average investigation time when available.

## Quarterly Review

Perform a deeper review at least quarterly.

The quarterly review should include:

- threshold performance;
- known false negatives;
- Purple Team results;
- business and infrastructure changes;
- authentication technology changes;
- source-familiarity assumptions;
- user and service-account behavior;
- detection drift;
- opportunities for retirement or redesign.

## Event-Driven Review

Review immediately when:

- alert volume changes unexpectedly;
- a major authentication incident is missed;
- analysts begin ignoring or mass-closing cases;
- authentication logging changes;
- identity infrastructure changes;
- a major business migration occurs;
- a new attack technique is observed;
- Purple Team or incident-response testing demonstrates a meaningful blind spot.

---

# Detection Health Metrics

Track at minimum:

## Volume Metrics

- total V1 alerts;
- total V2 cases;
- alerts per rule;
- cases per case type;
- daily and weekly volume;
- volume by account type;
- volume by source familiarity.

## Quality Metrics

- known benign cases;
- known suspicious cases;
- false-positive rate where ground truth exists;
- false-negative scenarios identified through testing;
- duplicate or redundant case rate;
- analyst escalation rate;
- analyst closure-without-action rate.

## Coverage Metrics

- suspicious scenarios detected;
- suspicious successful authentications detected;
- privileged-account attack scenarios detected;
- distributed attack scenarios detected;
- known blind spots still unresolved.

## Analyst Experience Metrics

Where available:

- median triage time;
- median investigation time;
- percentage of alerts closed without investigation;
- analyst feedback on alert clarity;
- number of analyst requests for additional context;
- repeat alerts for the same underlying activity.

---

# Health Thresholds and Warning Indicators

Operational review should be triggered when any of the following occur:

- sudden increase or decrease in alert volume without an expected business explanation;
- large increase in benign cases;
- repeated duplicate cases;
- suspicious-success cases stop appearing despite continued authentication activity;
- privileged-account detection volume unexpectedly drops to zero;
- analysts consistently close cases without meaningful review;
- source-familiarity fields become unavailable or unreliable;
- key telemetry fields become null or inconsistent;
- authentication event volume changes materially.

These are warning indicators, not automatic proof that the detection is broken.

---

# Data Dependencies

The detections depend on reliable authentication telemetry containing, at minimum:

- event timestamp;
- account or username;
- source address or source identity;
- authentication result.

Additional useful fields include:

- account type;
- privilege context;
- source familiarity;
- destination system;
- authentication application;
- identity provider;
- device identity;
- endpoint risk;
- geographic or network context.

V2 additionally depends on valid V1 alert output.

If V1 stops producing usable signals, V2 cannot independently recover the underlying activity.

---

# Data Quality Monitoring

Monitor for:

- missing timestamps;
- malformed timestamps;
- missing usernames;
- missing source addresses;
- missing authentication result;
- unexpected field-value changes;
- duplicate ingestion;
- delayed ingestion;
- major event-volume changes;
- privilege-context failures;
- source-familiarity enrichment failures.

If a required field becomes unreliable, detection health must be reviewed before interpreting a reduction in alerts as an improvement.

---

# Known Failure Conditions

The current detection architecture may fail to identify:

- activity deliberately kept below numeric thresholds;
- many-user/many-source distributed attacks;
- suspicious successes that remain below correlation thresholds;
- attacks visible only over a broader historical period;
- attacks where source or account identity is not consistently represented;
- activity lost because required telemetry is missing;
- malicious activity occurring outside the defined time windows.

These conditions are documented residual risks and must remain visible in the false-negative register.

---

# Change Triggers

A detection change should be considered when:

- adversarial testing identifies a repeatable evasion;
- confirmed incidents reveal a blind spot;
- analyst feedback identifies excessive noise;
- alert context is insufficient for rapid triage;
- authentication technology changes;
- new account types are introduced;
- infrastructure or workforce patterns materially change;
- source-familiarity logic becomes unreliable;
- business processes create new benign patterns;
- rule volume changes without explanation.

A change trigger does not automatically mean a threshold should be adjusted.

---

# Change Management Requirements

Before changing detection logic:

1. Document the reason for the proposed change.
2. Identify the expected benefit.
3. Identify the expected coverage cost.
4. Define measurable success criteria.
5. Preserve the current logic.
6. Test the proposed logic against benign and suspicious scenarios.
7. Test known false-negative scenarios.
8. Compare before and after results.
9. Document any new residual risk.
10. Define rollback criteria.

Do not make production changes solely because an individual alert appears inconvenient.

---

# Exceptions

Exceptions should be narrow, documented, time-limited, and reviewable.

Examples may include:

- temporary maintenance activity;
- controlled testing;
- known migration behavior;
- temporary service-account issues.

Blanket exclusions based only on:

- internal address;
- familiar source;
- service account;
- business unit;
- privileged administrator;

should not be approved without evidence that the exclusion does not create unacceptable detection loss.

---

# Exception Approver

Recommended approver:

SOC Detection Engineering Lead or SOC Manager.

Higher-risk exceptions involving:

- privileged accounts;
- authentication successes;
- broad network ranges;
- entire account classes;

should require additional review from the appropriate security owner.

---

# Exception Expiration

Every exception should include:

- creation date;
- reason;
- owner;
- approved scope;
- expiration date;
- review date.

Exceptions should expire automatically where technically possible.

Permanent exceptions should be avoided unless the behavior has been thoroughly validated and independently monitored.

---

# Versioning

Each detection change should have:

- version identifier;
- date;
- change description;
- reason;
- expected effect;
- observed effect;
- coverage gained;
- coverage lost;
- rollback reference.

The existing Original, V1, and V2 versions should remain preserved for comparison.

---

# Rollback

Rollback should be possible when a change causes:

- major false-positive increase;
- unexpected loss of coverage;
- analyst workload increase;
- broken case correlation;
- incorrect severity;
- telemetry incompatibility;
- unstable or unexplained behavior.

Rollback should restore the last validated detection version rather than creating an emergency untested rule.

---

# Analyst Feedback Loop

SOC analysts should have a simple method to report:

- confusing alerts;
- missing context;
- recurring benign patterns;
- duplicate cases;
- suspected false positives;
- suspected false negatives;
- incorrect severity;
- useful or unnecessary alert fields.

Detection Engineering should review this feedback during routine detection-health reviews.

Analyst feedback should be treated as operational evidence, not automatically as a request to suppress an alert.

---

# False-Negative Review

Known false negatives should be reviewed at least quarterly.

For each known miss, determine whether it should be addressed through:

- tuning;
- complementary detection;
- improved telemetry;
- endpoint detection;
- identity protection;
- network controls;
- user behavior analytics;
- preventive control;
- accepted residual risk.

The objective is not to force every gap into one rule.

---

# Complementary Detection Strategy

The current V1/V2 architecture should be supplemented when a different analytical perspective is required.

Examples include:

- distributed many-user/many-source campaigns;
- long-term sub-threshold behavior;
- suspicious successful authentications using identity and device risk;
- historical behavior anomalies.

Complementary detections should be independently measurable and explainable.

---

# Production Validation

Before production deployment or major revision:

- validate required fields;
- validate expected rule firing;
- validate successful-authentication correlation;
- validate privileged-account logic;
- validate case grouping;
- validate severity;
- validate analyst-facing context;
- verify that known benign patterns do not dominate output;
- verify that known suspicious scenarios remain detectable;
- rerun adversarial tests.

---

# Detection Drift Monitoring

Detection performance should not be assumed to remain stable.

Review for drift caused by:

- remote-work changes;
- workforce growth or reduction;
- mergers or acquisitions;
- new offices;
- new VPN infrastructure;
- new identity providers;
- MFA changes;
- passwordless authentication;
- service-account changes;
- cloud migration;
- network redesign;
- new endpoint management platforms;
- logging schema changes;
- attacker tradecraft changes;
- new automation or scripted business processes.

A stable detection rule can still become operationally poor if the environment changes around it.

---

# Retirement Criteria

A detection may be retired when:

- the underlying technology is no longer used;
- the detection is replaced by a measurably better control;
- required telemetry is permanently unavailable;
- the behavior is covered more effectively by another detection;
- the rule no longer represents relevant attacker behavior;
- the detection creates more operational harm than measurable security value and cannot be reasonably corrected.

Retirement should be documented and approved.

Do not silently disable detections.

---

# Current Production-Readiness Assessment

The V1/V2 authentication detection strategy has demonstrated:

- major workload reduction compared with the original detector;
- preserved coverage across the six original suspicious scenarios;
- explicit detection of suspicious successful authentications that the original detector missed;
- improved case-level correlation;
- improved analyst-facing context;
- preserved privileged low-and-slow coverage.

Known limitations remain:

- threshold-skimming attacks;
- distributed many-user/many-source campaigns;
- sub-threshold suspicious successes;
- dependence on V1 signals for V2 case creation.

These limitations require continued monitoring and complementary detection work.

---

# Production Recommendation

The tuned V1/V2 strategy can proceed to production-readiness review with documented residual risk.

Deployment should include:

- ongoing health measurement;
- analyst feedback;
- false-negative tracking;
- version control;
- rollback capability;
- scheduled detection-drift reviews;
- complementary detection development for the most important documented gaps.

The detection should not be treated as complete or permanently tuned.

---

# Phase 9 Status

Detection Operations Plan completed.

The next production-readiness artifact is the Detection Drift Analysis.
