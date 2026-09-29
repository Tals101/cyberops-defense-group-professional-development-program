import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EVENTS_FILE = ROOT / "dataset" / "authentication-events.csv"
TRUTH_FILE = ROOT / "dataset" / "authentication-ground-truth.csv"
BASELINE_FILE = ROOT / "analysis" / "baseline-alerts.csv"
V1_FILE = ROOT / "analysis" / "v1-alerts.csv"
V2_FILE = ROOT / "analysis" / "v2-cases.csv"

SCORED_FILE = ROOT / "analysis" / "v2-scored-cases.csv"
SCENARIO_FILE = ROOT / "analysis" / "v2-scenario-summary.csv"
METRICS_FILE = ROOT / "analysis" / "v2-metrics.txt"

MINUTES_PER_INVESTIGATION = 5


def read_csv(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


events = read_csv(EVENTS_FILE)
truth = read_csv(TRUTH_FILE)
baseline_alerts = read_csv(BASELINE_FILE)
v1_alerts = read_csv(V1_FILE)
v2_cases = read_csv(V2_FILE)

events_by_id = {
    row["event_id"]: row
    for row in events
}

truth_by_id = {
    row["event_id"]: row
    for row in truth
}


# ---------------------------------------------------------
# Score every V2 case using ALL related authentication events.
# ---------------------------------------------------------
scored_cases = []

for case in v2_cases:
    related_ids = [
        value
        for value in case["related_event_ids"].split(";")
        if value
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

    scored = dict(case)
    scored["related_classifications"] = ";".join(
        classifications
    )
    scored["related_scenarios"] = ";".join(
        scenarios
    )
    scored["evaluation_disposition"] = disposition

    scored_cases.append(scored)


scored_fields = list(scored_cases[0].keys())

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
    writer.writerows(scored_cases)


# ---------------------------------------------------------
# Case-level quality.
# ---------------------------------------------------------
benign_only_cases = [
    row
    for row in scored_cases
    if row["evaluation_disposition"] == "benign-only"
]

suspicious_only_cases = [
    row
    for row in scored_cases
    if row["evaluation_disposition"] == "suspicious-only"
]

mixed_cases = [
    row
    for row in scored_cases
    if row["evaluation_disposition"] == "mixed"
]

cases_with_suspicious_content = [
    row
    for row in scored_cases
    if "suspicious" in row["related_classifications"]
]

cases_with_any_benign_content = [
    row
    for row in scored_cases
    if "benign" in row["related_classifications"]
]


# ---------------------------------------------------------
# Event coverage.
# ---------------------------------------------------------
covered_event_ids = set()

for case in v2_cases:
    covered_event_ids.update(
        value
        for value in case["related_event_ids"].split(";")
        if value
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
scenario_cases = defaultdict(set)
scenario_classification = {}
scenario_name = {}

for row in truth:
    sid = row["scenario_id"]

    scenario_total_events[sid] += 1
    scenario_classification[sid] = row["classification"]
    scenario_name[sid] = row["scenario_name"]

for case in v2_cases:
    related_ids = [
        value
        for value in case["related_event_ids"].split(";")
        if value
    ]

    for event_id in related_ids:
        gt = truth_by_id[event_id]
        sid = gt["scenario_id"]

        scenario_covered_events[sid].add(event_id)
        scenario_cases[sid].add(case["case_id"])


scenario_rows = []

for sid in sorted(scenario_total_events):
    total = scenario_total_events[sid]
    covered = len(scenario_covered_events[sid])
    case_count = len(scenario_cases[sid])

    scenario_rows.append({
        "scenario_id": sid,
        "classification": scenario_classification[sid],
        "scenario_name": scenario_name[sid],
        "total_events": total,
        "covered_events": covered,
        "uncovered_events": total - covered,
        "cases_referencing_scenario": case_count,
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
        "cases_referencing_scenario",
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
    if scenario_cases[sid]
}

missed_suspicious_scenarios = (
    suspicious_scenarios
    - detected_suspicious_scenarios
)


# ---------------------------------------------------------
# Explicit suspicious success coverage.
# ---------------------------------------------------------
suspicious_success_events = []

for row in truth:
    if row["classification"] != "suspicious":
        continue

    event = events_by_id[row["event_id"]]

    if event["auth_result"] == "success":
        suspicious_success_events.append(
            row["event_id"]
        )


explicit_success_event_ids = set()

for case in v2_cases:
    contributing_rules = set(
        value
        for value in case[
            "contributing_v1_rule_ids"
        ].split(";")
        if value
    )

    if "V1-02" not in contributing_rules:
        continue

    if case["successful_authentication"] != "true":
        continue

    explicit_success_event_ids.update(
        value
        for value in case["related_event_ids"].split(";")
        if value
    )


explicit_success_detections = [
    event_id
    for event_id in suspicious_success_events
    if event_id in explicit_success_event_ids
]


# ---------------------------------------------------------
# Familiar-source suspicious visibility.
# ---------------------------------------------------------
familiar_suspicious_cases = []

for case in scored_cases:
    if (
        case["evaluation_disposition"] == "suspicious-only"
        and "familiar" in case["source_familiarity"].split(";")
    ):
        familiar_suspicious_cases.append(case)


# ---------------------------------------------------------
# Case and consolidation counts.
# ---------------------------------------------------------
rule_counts = Counter(
    row["rule_id"]
    for row in v2_cases
)

baseline_count = len(baseline_alerts)
v1_count = len(v1_alerts)
v2_count = len(v2_cases)

v1_to_v2_reduction = v1_count - v2_count
v1_to_v2_reduction_percent = (
    v1_to_v2_reduction / v1_count * 100
)

baseline_hours = (
    baseline_count
    * MINUTES_PER_INVESTIGATION
    / 60
)

v1_hours = (
    v1_count
    * MINUTES_PER_INVESTIGATION
    / 60
)

v2_hours = (
    v2_count
    * MINUTES_PER_INVESTIGATION
    / 60
)

benign_only_share = (
    len(benign_only_cases)
    / v2_count
    * 100
)

scenario_retention = (
    len(detected_suspicious_scenarios)
    / len(suspicious_scenarios)
    * 100
)

spray_cases = rule_counts["V2-02"]


metrics = [
    "Ticket #008 - V2 Detection Metrics",
    "",
    f"Dataset events: {len(events)}",
    f"Baseline alerts: {baseline_count}",
    f"V1 alerts: {v1_count}",
    f"V2 cases: {v2_count}",
    (
        "V1 to V2 investigation reduction: "
        f"{v1_to_v2_reduction}"
    ),
    (
        "V1 to V2 reduction percent: "
        f"{v1_to_v2_reduction_percent:.1f}%"
    ),
    "",
    (
        "Suspicious-only V2 cases: "
        f"{len(suspicious_only_cases)}"
    ),
    (
        "Benign-only V2 cases: "
        f"{len(benign_only_cases)}"
    ),
    f"Mixed V2 cases: {len(mixed_cases)}",
    (
        "V2 benign-only case share: "
        f"{benign_only_share:.1f}%"
    ),
    (
        "V2 cases containing suspicious activity: "
        f"{len(cases_with_suspicious_content)}"
    ),
    (
        "V2 cases containing any benign activity: "
        f"{len(cases_with_any_benign_content)}"
    ),
    "",
    (
        "Suspicious events represented in V2 cases: "
        f"{len(covered_suspicious_events)} of "
        f"{len(suspicious_event_ids)}"
    ),
    (
        "Benign events represented in V2 cases: "
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
        f"{scenario_retention:.1f}%"
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
        "Explicitly represented after V2 correlation: "
        f"{len(explicit_success_detections)}"
    ),
    "",
    (
        "Suspicious V2 cases containing familiar-source "
        f"context: {len(familiar_suspicious_cases)}"
    ),
    (
        "Password-spray campaign cases: "
        f"{spray_cases}"
    ),
    "",
    (
        "Baseline workload estimate: "
        f"{baseline_hours:.2f} hours"
    ),
    (
        "V1 workload estimate: "
        f"{v1_hours:.2f} hours"
    ),
    (
        "V2 workload estimate: "
        f"{v2_hours:.2f} hours"
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
        "V2 cases are correlated investigation units. "
        "Lower case count alone does not establish "
        "improved detection quality."
    ),
    (
        "Scenario retention, suspicious success coverage, "
        "familiar-source visibility, and residual event "
        "coverage must also be reviewed."
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
        f'{row["covered_events"]}/'
        f'{row["total_events"]} events represented, '
        f'{row["cases_referencing_scenario"]} cases'
    )

print("\nCase Evaluation")

for row in scored_cases:
    print(
        f'{row["case_id"]} '
        f'{row["rule_id"]} '
        f'{row["evaluation_disposition"]} '
        f'scenarios={row["related_scenarios"]} '
        f'v1={row["contributing_v1_alert_ids"]}'
    )

print(f"\nScored cases: {SCORED_FILE}")
print(f"Scenario summary: {SCENARIO_FILE}")
print(f"Metrics: {METRICS_FILE}")
