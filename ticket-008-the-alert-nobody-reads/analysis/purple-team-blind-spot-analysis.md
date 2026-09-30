# Ticket #008 — Purple Team Blind-Spot Analysis

## Decision Point #2 — You Created a Blind Spot

## Purple Team Observation

The revised detection successfully identified the straightforward repeated-failure attack.

A second simulated attacker distributed authentication activity across:

- multiple usernames;
- multiple source addresses;
- longer time intervals.

No individual user/source combination exceeded the primary correlation threshold.

The expected alert was not produced.

---

# What Assumption Did the Detector Make?

The detector assumed that meaningful authentication attacks would eventually become concentrated enough around a measurable entity relationship to cross a defined threshold.

Examples include:

- repeated failures for the same user and source;
- one source targeting several users;
- several sources targeting one user;
- repeated privileged-account activity within a defined window.

The design therefore depends on sufficient concentration in at least one entity or correlation window.

---

# How Did the Simulated Behavior Violate That Assumption?

The attacker deliberately spread activity across several dimensions at the same time.

Instead of concentrating attempts against one user, one source, or one short time window, the attacker distributed attempts across:

- multiple users;
- multiple sources;
- longer intervals.

Each individual slice remained below the existing correlation thresholds.

The malicious pattern existed mainly at the campaign level.

---

# Classification of the Gap

Primary classification:

Detection architecture / analytical perspective problem.

Secondary classification:

Tuning limitation.

This is not primarily a telemetry problem because the underlying authentication events were available.

The failure occurred because the detector analyzed them through relationships and time windows the attacker deliberately avoided.

---

# Is This Acceptable Residual Risk?

Not without additional consideration.

The Purple Team demonstrated a practical evasion strategy.

The activity can appear ordinary at the individual-event level while becoming suspicious when viewed collectively.

This should be preserved as a known false-negative condition.

---

# Different Analytical Perspective

A complementary campaign-level detection could examine:

- total failures across a broader period;
- number of distinct users targeted;
- number of distinct sources participating;
- many-user / many-source combinations;
- low-rate distributed failures;
- deviation from historical authentication behavior;
- privileged-account involvement;
- successful authentications associated with participating entities.

---

# Would Solving This Inside the Same Rule Make It Too Complicated?

Potentially yes.

Adding every distributed, low-rate, multi-entity attack pattern into the current detector could make:

- logic harder to explain;
- thresholds harder to validate;
- alerts harder to interpret;
- testing more difficult;
- false-positive behavior harder to diagnose;
- future tuning riskier.

---

# One Detector or Multiple Complementary Detections?

Multiple complementary detections are preferred.

V2 should continue detecting the concentrated and correlated authentication patterns it was designed for.

A separate complementary detection should focus on distributed campaign behavior across broader entity and time dimensions.

This keeps both detections understandable and independently measurable.

---

# Decision

Do not immediately modify V2.

Preserve the Purple Team miss as a documented false negative.

Treat it as an architectural detection gap that should be evaluated through a complementary distributed-authentication detection rather than adding more complexity to the existing V2 logic.

V2 remains useful for the patterns it was designed to detect, but it is not sufficient as the only authentication-abuse detection.

---

# Recommended Response

1. Preserve the failed Purple Team test as evidence.
2. Add the distributed multi-user/multi-source behavior to the false-negative register.
3. Include this scenario in adversarial testing.
4. Evaluate a separate complementary distributed-authentication detection.
5. Test future complementary logic against both malicious and realistic benign distributed activity.
6. Do not weaken the existing V2 detections because of this separate attack pattern.

---

# Current Status

Purple Team blind spot documented.

No V2 logic has been changed.

No new detection rule has been implemented.

The miss remains preserved for Phase 7 adversarial testing and final risk documentation.
