# Ticket #008 — The Alert Nobody Reads

## Detection Engineering Portfolio Project

This project demonstrates an end-to-end detection engineering workflow focused on improving a noisy authentication detection without simply suppressing alerts or raising thresholds until the problem disappeared.

The original detector generated **597 alerts from 1,000 authentication events**, creating excessive analyst workload and making meaningful activity difficult to distinguish from benign noise.

The project progressed through baseline measurement, V1 tuning, V2 correlation, analyst usability testing, Purple Team validation, adversarial testing, false-negative analysis, and production-readiness planning.

---

## Key Results

| Metric | Original | V1 | V2 |
|---|---:|---:|---:|
| Alerts / Analyst Units | 597 | 15 | 7 |
| Estimated Analyst Workload | 49.75 hours | 1.25 hours | 0.58 hours |
| Suspicious Scenarios Detected | 6 / 6 | 6 / 6 | 6 / 6 |
| Suspicious Successful Authentications Detected | 0 / 2 | 2 / 2 | 2 / 2 |
| Suspicious Events Represented | 143 / 145 | 64 / 145 | 64 / 145 |
| Known Benign Alerts / Cases | 248 alerts | 1 alert | 1 case |

**Important:** Raw alert counts and case counts are not equivalent sensitivity measurements. V2 reduces analyst-facing workload by correlating V1 signals into cases; it does not independently restore event-level sensitivity removed during V1 tuning.

---

## Problem

The original authentication detector had useful coverage but produced too much repetitive signal.

Major problems included:

- every failed authentication generated an alert;
- the same event could trigger multiple rules;
- stale service credentials created large volumes of benign noise;
- successful authentication after suspicious failures was not explicitly correlated;
- distributed attacks were difficult for analysts to interpret;
- familiar or internal sources could still contain malicious activity;
- analysts were expected to reconstruct attack sequences manually from fragmented alerts.

The goal was not simply to create fewer alerts.

The goal was to create **better security signal per unit of analyst attention while preserving meaningful attack coverage**.

---

## Engineering Progression

    Authentication Events
            |
            v
    Original Detector
    597 alerts
            |
            v
    Baseline Measurement + Noise Analysis
            |
            v
    V1 Behavioral Detection
    15 alerts
            |
            v
    V2 Correlation
    7 analyst cases
            |
            v
    Analyst Usability Review
            |
            v
    Purple Team + Adversarial Testing
            |
            v
    Known False Negatives + Production Controls

---

## Baseline

The baseline established the actual cost and behavior of the original detector before tuning.

Key findings included:

- **597 total alerts**
- **308 unique alerting events**
- **289 redundant/additional alerts**
- **248 known benign alerts**
- **41.5% benign alert share**
- approximately **49.75 analyst hours** at five minutes per alert

The largest benign contributor was a stale service credential scenario that produced **142 alerts** by itself.

See:

- [Detection Health Assessment](baseline/detection-health-assessment.md)
- [Dataset Design](baseline/dataset-design.md)
- [Original Detector](baseline/original-detection/original-detector.md)
- [Baseline Detection Report](baseline/baseline-results/baseline-detection-report.md)
- [Noise Analysis](baseline/noise-analysis.md)

---

## V1 — Behavioral Tuning

V1 replaced event-by-event alerting with behavioral conditions such as:

- repeated failures by the same user and source;
- success following recent failures;
- password spraying across multiple users;
- distributed targeting of one account;
- privileged-account failure patterns;
- persistent service-account failures.

V1 reduced the workload from **597 alerts to 15 alerts** while retaining representation of all six suspicious scenarios.

The design intentionally avoided broad whitelists and blanket suppression of familiar internal addresses.

See:

- [V1 Proposal](tuning/v1-proposal.md)
- [V1 Detector](tuning/v1/v1-detector.md)
- [V1 Evaluation](tuning/v1-results/v1-evaluation-report.md)
- [Manager Suppression Response](tuning/manager-suppression-response.md)

---

## V2 — Analyst-Facing Correlation

V2 correlated related V1 alerts into higher-level analyst cases.

Examples included:

- authentication attack sequences;
- password spray campaigns;
- distributed targeting;
- persistent service-account activity.

This reduced **15 V1 alerts to 7 V2 cases** while preserving the same six suspicious scenarios represented by V1.

See:

- [V2 Design](tuning/v2-design.md)
- [V2 Detector](tuning/v2/v2-detector.md)
- [V2 Evaluation](tuning/v2-results/v2-evaluation-report.md)
- [Original vs V1 vs V2 Comparison](testing/comparison.md)

---

## Purple Team Finding

The project intentionally preserves an important failure.

Purple Team testing demonstrated that an attacker could distribute activity across multiple usernames, multiple source addresses, and longer time intervals.

Because no single entity exceeded the primary thresholds, the expected alert did not fire.

This exposed an architectural limitation: the detector assumed suspicious behavior would eventually concentrate around a measurable user, source, or time window.

The miss was preserved rather than hidden or immediately tuned away.

See:

- [Purple Team Blind-Spot Analysis](testing/purple-team-analysis.md)
- [False-Negative Register](testing/false-negative-register.md)

---

## Adversarial Testing

Four adversarial variations were created:

1. threshold skimming;
2. distributed many-to-many authentication activity;
3. familiar-source failures followed by success;
4. privileged low-and-slow authentication failures.

Results:

- AT-01 — missed
- AT-02 — missed
- AT-03 — missed
- AT-04 — detected

The most important finding was that **V2 correlation cannot create detection sensitivity that V1 never produced**.

See:

- [Adversarial Test Plan](testing/adversarial-test-plan.md)
- [Adversarial Testing Report](testing/adversarial-testing.md)
- [Adversarial V1 Output](evidence/adversarial-v1-alerts.csv)
- [Adversarial V2 Output](evidence/adversarial-v2-cases.csv)

---

## Analyst Experience

The final analyst-facing design emphasizes:

- plain-language explanation;
- severity;
- user/account context;
- source and familiarity context;
- successful-authentication details;
- related users and sources;
- duration and event counts;
- triggering signals;
- recommended investigation checks.

See:

- [Original Analyst Experience](analyst-experience/original-alert.md)
- [Final Alert Design](analyst-experience/final-alert.md)
- [Analyst Usability Test](analyst-experience/analyst-test.md)
- [Before / After Analyst Experience](analyst-experience/before-after.md)

---

## Production Readiness

Operational controls include:

- ownership;
- routine review cadence;
- detection drift;
- data dependencies;
- change approval;
- exception management;
- rollback;
- analyst feedback;
- false-negative review;
- Purple Team follow-up;
- retirement criteria.

See:

- [Detection Operations Plan](operations/detection-operations-plan.md)
- [Detection Drift Analysis](operations/detection-drift.md)
- [Detection Change Record](operations/detection-change-record.md)

---

## Management Artifacts

- [Detection Engineering Decision Brief](management/decision-brief.md)
- [Measurement Summary](management/measurement-summary.md)

---

## Data and Reproducibility

The project uses synthetic authentication telemetry and separate ground truth.

Primary data:

- `data/authentication-events.csv`
- `data/authentication-ground-truth.csv`
- `data/adversarial-auth-events.csv`
- `data/adversarial-ground-truth.csv`

Primary scripts:

- `scripts/generate_auth_dataset.py`
- `scripts/run_baseline_detector.py`
- `scripts/analyze_baseline.py`
- `scripts/run_v1_detector.py`
- `scripts/analyze_v1.py`
- `scripts/run_v2_detector.py`
- `scripts/analyze_v2.py`
- `scripts/generate_adversarial_dataset.py`
- `scripts/run_adversarial_v1.py`
- `scripts/run_adversarial_v2.py`

Adversarial workflow:

    python scripts/generate_adversarial_dataset.py
    python scripts/run_adversarial_v1.py
    python scripts/run_adversarial_v2.py

---

## Repository Structure

    ticket-008-the-alert-nobody-reads/
    |
    |-- README.md
    |-- engineering-notebook.md
    |-- lessons-learned.md
    |
    |-- baseline/
    |-- tuning/
    |-- testing/
    |-- analyst-experience/
    |-- operations/
    |-- management/
    |-- scripts/
    |-- data/
    `-- evidence/

---

## Supporting Documentation

- [Engineering Notebook](engineering-notebook.md)
- [Lessons Learned](lessons-learned.md)
- [Supporting Evidence Index](evidence/supporting-evidence-index.md)
- [Final Detection Engineering Report — Source](evidence/final-detection-engineering-report-source.md)
- [Interview Preparation](evidence/interview-preparation.md)

---

## Engineering Principle

This project does not present detection engineering as a straight line from bad rule to perfect rule.

The Git history intentionally preserves the actual progression:

**baseline established → V1 proposed → V1 tested → V2 designed → Purple Team failure discovered → adversarial testing → final analyst design → production-readiness controls**

The failed assumptions and known false negatives are part of the engineering evidence, not something removed from the record.
