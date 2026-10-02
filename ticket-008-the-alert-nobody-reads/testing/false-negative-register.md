# Ticket #008 — False-Negative Register

## Purpose

Maintain a visible record of known authentication scenarios that the current V1/V2 strategy does not reliably detect.

A missed scenario should not be hidden simply because overall alert volume improved.

Each entry documents:

- the scenario;
- whether it was detected;
- why it was detected or missed;
- the security risk;
- compensating detections or controls;
- whether the remaining risk is currently acceptable.

This register should remain a living operational artifact.

---

# False-Negative Register

| Scenario | Detected? | Why / Why Not? | Risk | Compensating Detection / Control | Acceptable? |
|---|---|---|---|---|---|
| Threshold skimming — 4 failures against one non-privileged user from one unfamiliar source within approximately 9 minutes | No | V1-01 requires 5 failures within 10 minutes. No other V1 rule applied, so V2 received no signal. | Moderate. Attackers may deliberately remain immediately below numeric thresholds. | Historical anomaly detection; repeated sub-threshold behavior analysis; endpoint or identity risk context; user reporting; MFA and account-lockout controls where appropriate. | Conditionally acceptable while monitored. Do not lower the threshold without measuring benign impact. |
| Distributed many-user/many-source campaign | No | Activity was distributed across multiple users, multiple sources, and a broader time period so no V1 entity relationship exceeded its threshold. V2 cannot correlate events that never produced V1 alerts. | High. An attacker can distribute credential testing to avoid concentrated threshold-based detection. | Complementary campaign-level many-user/many-source detection; identity protection; broader historical analytics; endpoint/network correlation. | No as a long-term standalone risk. Requires complementary detection evaluation. |
| Familiar-source failures followed by sub-threshold success | No | Four failures followed by success remained below the non-privileged V1-02 threshold. Source familiarity did not suppress an alert; no rule independently covered the sequence. | High. A compromised familiar endpoint could obtain a successful login without crossing current thresholds. | Suspicious-success detection using device identity, endpoint risk, historical account/device pairing, identity-provider risk, session monitoring, MFA context. | No as a permanent blind spot. Requires complementary contextual detection. |
| Purple Team distributed low-rate multi-entity activity | No | The detector assumed attack behavior would concentrate around a measurable user, source, or time-window relationship. The attacker intentionally avoided that concentration. | High. Campaign-level malicious behavior may remain invisible when viewed only through individual entity relationships. | Separate distributed-authentication campaign detection; broader time windows; campaign-level analytics; Purple Team retesting. | No. Preserve as an architectural gap until compensated. |
| Activity visible only over a broader historical period | Not reliably | Current V1 rules use defined rolling windows. Malicious activity outside those windows may never accumulate enough evidence for a signal. | Moderate to High depending on target and outcome. | Long-term behavioral analytics; identity baselining; UEBA-style analytics; scheduled retrospective hunts. | Conditionally acceptable only with complementary historical monitoring. |
| Malicious behavior with missing or inconsistent telemetry | Not reliably | V1 depends on timestamp, account, source, and authentication result. Missing or malformed fields can prevent threshold or correlation logic from functioning correctly. | High if telemetry loss is significant or silent. | Data-quality monitoring; ingestion-health alerts; identity-provider monitoring; independent endpoint and network telemetry. | No if required telemetry is materially degraded. Detection health review required. |
| V1 signal loss causing V2 case loss | No independent recovery | V2 is a correlation layer. If V1 does not produce an alert, V2 does not independently inspect raw events to recover the missed activity. | High for behaviors outside V1 coverage. | V1 health monitoring; complementary raw-event detections; adversarial testing; false-negative tracking. | Acceptable only as a documented architectural characteristic with complementary coverage. |

---

# Confirmed Adversarial Test Results

## AT-01 — Threshold Skimming

Result:

Missed.

Evidence:

- 4 suspicious events;
- no V1 alert;
- no V2 case.

Primary gap:

Threshold limitation.

Current decision:

Do not automatically lower V1-01.

Evaluate broader historical or contextual detection instead.

---

## AT-02 — Distributed Many-to-Many Campaign

Result:

Missed.

Evidence:

- 12 suspicious events;
- 6 usernames;
- 4 unfamiliar sources;
- approximately 4 hours;
- no V1 alert;
- no V2 case.

Primary gap:

Detection architecture / analytical perspective.

Current decision:

Evaluate a complementary distributed-authentication campaign detection.

Do not overload V2 with unrelated campaign-detection logic.

---

## AT-03 — Familiar-Source Failures Followed by Success

Result:

Missed.

Evidence:

- 4 failures;
- 1 success;
- same non-privileged user;
- same familiar source;
- no V1 alert;
- no V2 case.

Primary gap:

Sub-threshold suspicious-success coverage.

Current decision:

Do not suppress familiar sources.

Evaluate contextual suspicious-success detection.

---

## AT-04 — Privileged Low-and-Slow

Result:

Detected.

Evidence:

- V1 alert: ADV-V1-0001;
- rule: V1-05;
- V2 case: ADV-V2C-0001;
- case type: V2-01.

This scenario is included in the register as a validation boundary rather than a current false negative.

It demonstrates that privileged low-and-slow coverage remains present.

---

# Risk Classification Guidance

## High

Use when a blind spot could plausibly result in:

- successful account compromise;
- privileged-account compromise;
- broad credential attack;
- meaningful loss of authentication visibility;
- campaign-level evasion.

## Moderate

Use when:

- behavior is suspicious but commonly overlaps benign activity;
- immediate compromise evidence is absent;
- compensating controls provide meaningful additional protection.

Risk level should be reviewed if business or technical context changes.

---

# What Does Not Count as an Acceptable Fix?

The following should not automatically be treated as solutions:

- lowering every threshold after one miss;
- blanket suppression of familiar addresses;
- blanket service-account whitelisting;
- broad internal-network exclusions;
- adding every attack technique into one increasingly complex rule;
- claiming V2 provides coverage when no V1 signal exists;
- ignoring a miss because overall alert volume improved.

---

# Preferred Response to a False Negative

For each false negative:

1. Preserve the evidence.
2. Confirm whether telemetry existed.
3. Determine which detector assumption failed.
4. Classify the gap as:
   - tuning;
   - architecture;
   - telemetry;
   - enrichment;
   - acceptable residual risk.
5. Evaluate the security significance.
6. Determine whether the right response is:
   - tuning;
   - complementary detection;
   - improved telemetry;
   - endpoint control;
   - identity control;
   - network control;
   - historical hunting;
   - accepted risk.
7. Test the proposed response against benign activity.
8. Update this register.

---

# Current Priority

The highest-priority unresolved false negative is:

Distributed many-user/many-source authentication activity.

Reason:

The Purple Team and adversarial tests independently demonstrated that malicious behavior can remain below the current user, source, and timing thresholds while still forming a suspicious campaign at a broader level.

Recommended next analytical perspective:

A separate campaign-level detector using:

- broader observation windows;
- total failure count;
- distinct user count;
- distinct source count;
- user/source relationship density;
- privilege involvement;
- successful authentication context;
- historical deviation.

---

# Review Frequency

Review this register:

- during monthly detection-health review;
- during quarterly coverage review;
- after Purple Team exercises;
- after confirmed authentication incidents;
- after major detection changes;
- after telemetry or identity-infrastructure changes.

Closed items should remain historically documented rather than silently removed.

---

# Status

False-Negative Register created.

Known misses from Purple Team and adversarial testing are formally documented.

The next closure artifact is the Detection Change Record.
