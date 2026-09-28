import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EVENTS_FILE = ROOT / "dataset" / "authentication-events.csv"
TRUTH_FILE = ROOT / "dataset" / "authentication-ground-truth.csv"
V1_FILE = ROOT / "analysis" / "v1-alerts.csv"
BASELINE_FILE = ROOT / "analysis" / "baseline-alerts.csv"

SCORED_FILE = ROOT / "analysis" / "v1-scored-alerts.csv"
SCENARIO_FILE = ROOT / "analysis" / "v1-scenario-summary.csv"
METRICS_FILE = ROOT / "analysis" / "v1-metrics.txt"

MINUTES_PER_ALERT = 5


def read_csv(path):
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


events = read_csv(EVENTS_FILE)
truth = read_csv(TRUTH_FILE)
v1_alerts = read_csv(V1_FILE)
baseline_alerts = read_csv(BASELINE_FILE)

events_by_id = {
    row["event_id"]: row
    for row in events
}

truth_by_id = {
    row["event_id"]: row
    for row in truth
}


# ---------------------------------------------------------
# Score each V1 alert using ALL related events.
# ---------------------------------------------------------
scored_alerts = []

for alert in v1_alerts:
    related_ids = [
        x
        for x in alert["related_event_ids"].split(";")
        if x
    ]

    related_truth = [
        truth_by_id[event_id]
        for event_id in related_ids
    ]

    classifications = sorted({
        row["classification"]
        for row in related_truth
    })

    scenarios = sorted({
        row["scenario_id"]
        for row in related_truth
    })

    if classifications == ["benign"]:
        disposition = "benign-only"
    elif classifications == ["suspicious"]:
        disposition = "suspicious-only"
    else:
        disposition = "mixed"

    scored = dict(alert)
    scored["related_classifications"] = ";".join(classifications)
    scored["related_scenarios"] = ";".join(scenarios)
    scored["evaluation_disposition"] = disposition

    scored_alerts.append(scored)


scored_fields = list(scored_alerts[0].keys())

with SCORED_FILE.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=scored_fields,
    )
    writer.writeheader()
    writer.writerows(scored_alerts)


# ---------------------------------------------------------
# Alert-level quality.
# ---------------------------------------------------------
benign_only_alerts = [
    row
    for row in scored_alerts
    if row["evaluation_disposition"] == "benign-only"
]

suspicious_only_alerts = [
    row
    for row in scored_alerts
    if row["evaluation_disposition"] == "suspicious-only"
]

mixed_alerts = [
    row
    for row in scored_alerts
    if row["evaluation_disposition"] == "mixed"
]

alerts_with_suspicious_content = [
    row
    for row in scored_alerts
    if "suspicious" in row["related_classifications"]
]

alerts_with_any_benign_content = [
    row
    for row in scored_alerts
    if "benign" in row["related_classifications"]
]


# ---------------------------------------------------------
# Determine event coverage through related_event_ids.
# ---------------------------------------------------------
covered_event_ids = set()

for alert in v1_alerts:
    covered_event_ids.update(
        x
        for x in alert["related_event_ids"].split(";")
        if x
    )

suspicious_event_ids = {
    row["event_id"]
    for row in truth
    if row["classification"] == "suspicious"
}

benign_event_ids = {
    row["event_id"]
    for row in truth
    if row["classification"] == "benign"
}

covered_suspicious_events = (
    covered_event_ids & suspicious_event_ids
)

covered_benign_events = (
    covered_event_ids & benign_event_ids
)


# ---------------------------------------------------------
# Scenario coverage.
# ---------------------------------------------------------
scenario_total_events = Counter()
scenario_covered_events = defaultdict(set)
scenario_alerts = defaultdict(set)
scenario_classification = {}
scenario_name = {}

for row in truth:
    sid = row["scenario_id"]
    scenario_total_events[sid] += 1
    scenario_classification[sid] = row["classification"]
    scenario_name[sid] = row["scenario_name"]

for alert in v1_alerts:
    related_ids = [
        x
        for x in alert["related_event_ids"].split(";")
        if x
    ]

    for event_id in related_ids:
        gt = truth_by_id[event_id]
        sid = gt["scenario_id"]

        scenario_covered_events[sid].add(event_id)
        scenario_alerts[sid].add(alert["alert_id"])


scenario_rows = []

for sid in sorted(scenario_total_events):
    total = scenario_total_events[sid]
    covered = len(scenario_covered_events[sid])
    alert_count = len(scenario_alerts[sid])

    scenario_rows.append({
        "scenario_id": sid,
        "classification": scenario_classification[sid],
        "scenario_name": scenario_name[sid],
        "total_events": total,
        "covered_events": covered,
        "uncovered_events": total - covered,
        "alerts_referencing_scenario": alert_count,
        "event_coverage_percent": (
            f"{(covered / total * 100):.1f}"
        ),
    })


with SCENARIO_FILE.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    fields = [
        "scenario_id",
        "classification",
        "scenario_name",
        "total_events",
        "covered_events",
        "uncovered_events",
        "alerts_referencing_scenario",
        "event_coverage_percent",
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fields,
    )
    writer.writeheader()
    writer.writerows(scenario_rows)


suspicious_scenarios = {
    row["scenario_id"]
    for row in truth
    if row["classification"] == "suspicious"
}

detected_suspicious_scenarios = {
    sid
    for sid in suspicious_scenarios
    if scenario_alerts[sid]
}

missed_suspicious_scenarios = (
    suspicious_scenarios
    - detected_suspicious_scenarios
)


# ---------------------------------------------------------
# Explicit success-after-failure coverage.
# ---------------------------------------------------------
suspicious_success_events = []

for row in truth:
    if row["classification"] != "suspicious":
        continue

    event = events_by_id[row["event_id"]]

    if event["auth_result"] == "success":
        suspicious_success_events.append(row["event_id"])


v1_success_trigger_ids = {
    row["trigger_event_id"]
    for row in v1_alerts
    if row["rule_id"] == "V1-02"
}

explicit_success_detections = [
    event_id
    for event_id in suspicious_success_events
    if event_id in v1_success_trigger_ids
]


# ---------------------------------------------------------
# Rule counts.
# ---------------------------------------------------------
rule_counts = Counter(
    row["rule_id"]
    for row in v1_alerts
)


# ---------------------------------------------------------
# Workload and comparison.
# ---------------------------------------------------------
baseline_count = len(baseline_alerts)
v1_count = len(v1_alerts)

alert_reduction = baseline_count - v1_count
alert_reduction_percent = (
    alert_reduction / baseline_count * 100
)

baseline_hours = (
    baseline_count * MINUTES_PER_ALERT / 60
)

v1_hours = (
    v1_count * MINUTES_PER_ALERT / 60
)

benign_only_share = (
    len(benign_only_alerts)
    / v1_count
    * 100
)

suspicious_scenario_retention = (
    len(detected_suspicious_scenarios)
    / len(suspicious_scenarios)
    * 100
)


metrics = [
    "Ticket #008 - V1 Detection Metrics",
    "",
    f"Dataset events: {len(events)}",
    f"Baseline alerts: {baseline_count}",
    f"V1 alerts: {v1_count}",
    f"Alert reduction: {alert_reduction}",
    (
        "Alert reduction percent: "
        f"{alert_reduction_percent:.1f}%"
    ),
    "",
    f"Suspicious-only V1 alerts: {len(suspicious_only_alerts)}",
    f"Benign-only V1 alerts: {len(benign_only_alerts)}",
    f"Mixed V1 alerts: {len(mixed_alerts)}",
    (
        "V1 benign-only alert share: "
        f"{benign_only_share:.1f}%"
    ),
    (
        "V1 alerts containing suspicious activity: "
        f"{len(alerts_with_suspicious_content)}"
    ),
    (
        "V1 alerts containing any benign activity: "
        f"{len(alerts_with_any_benign_content)}"
    ),
    "",
    (
        "Suspicious events represented in V1 alerts: "
        f"{len(covered_suspicious_events)} of "
        f"{len(suspicious_event_ids)}"
    ),
    (
        "Benign events represented in V1 alerts: "
        f"{len(covered_benign_events)} of "
        f"{len(benign_event_ids)}"
    ),
    "",
    (
        "Suspicious scenarios detected: "
        f"{len(detected_suspicious_scenarios)} of "
        f"{len(suspicious_scenarios)}"
    ),
    (
        "Suspicious scenario retention: "
        f"{suspicious_scenario_retention:.1f}%"
    ),
    (
        "Suspicious scenarios completely missed: "
        f"{len(missed_suspicious_scenarios)}"
    ),
    "",
    (
        "Suspicious successful-authentication events: "
        f"{len(suspicious_success_events)}"
    ),
    (
        "Explicitly detected by V1-02: "
        f"{len(explicit_success_detections)}"
    ),
    "",
    (
        f"Baseline workload estimate: "
        f"{baseline_hours:.2f} hours"
    ),
    (
        f"V1 workload estimate: "
        f"{v1_hours:.2f} hours"
    ),
    "",
    "Rule Counts:",
]

for rule_id in sorted(rule_counts):
    metrics.append(
        f"{rule_id}: {rule_counts[rule_id]}"
    )

metrics.extend([
    "",
    "Important:",
    (
        "V1 alerts are investigation units, so event-level "
        "coverage is not directly equivalent to the baseline "
        "per-event alert rate."
    ),
    (
        "Scenario retention and explicit high-risk transition "
        "coverage are required before V1 can be considered "
        "better rather than merely quieter."
    ),
])


METRICS_FILE.write_text(
    "\n".join(metrics) + "\n",
    encoding="utf-8",
)


print("\n".join(metrics))

print("\nScenario Summary")

for row in scenario_rows:
    print(
        f'{row["scenario_id"]}: '
        f'{row["covered_events"]}/{row["total_events"]} '
        f'events represented, '
        f'{row["alerts_referencing_scenario"]} alerts'
    )

print("\nAlert Evaluation")

for row in scored_alerts:
    print(
        f'{row["alert_id"]} '
        f'{row["rule_id"]} '
        f'{row["evaluation_disposition"]} '
        f'scenarios={row["related_scenarios"]}'
    )

print(f"\nScored alerts: {SCORED_FILE}")
print(f"Scenario summary: {SCENARIO_FILE}")
print(f"Metrics: {METRICS_FILE}")
