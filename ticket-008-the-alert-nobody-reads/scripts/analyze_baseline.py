import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EVENTS_FILE = ROOT / "dataset" / "authentication-events.csv"
TRUTH_FILE = ROOT / "dataset" / "authentication-ground-truth.csv"
ALERTS_FILE = ROOT / "analysis" / "baseline-alerts.csv"

SCORED_FILE = ROOT / "analysis" / "baseline-scored-alerts.csv"
SCENARIO_FILE = ROOT / "analysis" / "baseline-scenario-summary.csv"
METRICS_FILE = ROOT / "analysis" / "baseline-metrics.txt"

# Lab workload assumption only.
MINUTES_PER_ALERT = 5


def read_csv(path):
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


events = read_csv(EVENTS_FILE)
truth = read_csv(TRUTH_FILE)
alerts = read_csv(ALERTS_FILE)

truth_by_event = {
    row["event_id"]: row
    for row in truth
}

events_by_id = {
    row["event_id"]: row
    for row in events
}

scored_alerts = []

for alert in alerts:
    gt = truth_by_event[alert["event_id"]]

    scored = dict(alert)
    scored["scenario_id"] = gt["scenario_id"]
    scored["classification"] = gt["classification"]
    scored["scenario_name"] = gt["scenario_name"]

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


alerted_event_ids = {
    row["event_id"]
    for row in alerts
}

benign_event_ids = {
    row["event_id"]
    for row in truth
    if row["classification"] == "benign"
}

suspicious_event_ids = {
    row["event_id"]
    for row in truth
    if row["classification"] == "suspicious"
}

alerted_benign_events = alerted_event_ids & benign_event_ids
alerted_suspicious_events = alerted_event_ids & suspicious_event_ids
missed_suspicious_events = suspicious_event_ids - alerted_event_ids

benign_alerts = [
    row
    for row in scored_alerts
    if row["classification"] == "benign"
]

suspicious_alerts = [
    row
    for row in scored_alerts
    if row["classification"] == "suspicious"
]


# Redundancy:
# Every alert beyond the first alert tied to the same event is counted
# as an additional/redundant alert for baseline workload purposes.
redundant_alerts = len(alerts) - len(alerted_event_ids)

alert_level_benign_share = (
    len(benign_alerts) / len(alerts) * 100
)

suspicious_event_detection_rate = (
    len(alerted_suspicious_events)
    / len(suspicious_event_ids)
    * 100
)

benign_event_alert_rate = (
    len(alerted_benign_events)
    / len(benign_event_ids)
    * 100
)

redundancy_rate = (
    redundant_alerts / len(alerts) * 100
)


# Scenario-level measurements.
scenario_total_events = Counter()
scenario_alert_count = Counter()
scenario_alerted_events = defaultdict(set)
scenario_classification = {}
scenario_name = {}

for row in truth:
    sid = row["scenario_id"]
    scenario_total_events[sid] += 1
    scenario_classification[sid] = row["classification"]
    scenario_name[sid] = row["scenario_name"]

for row in scored_alerts:
    sid = row["scenario_id"]
    scenario_alert_count[sid] += 1
    scenario_alerted_events[sid].add(row["event_id"])


scenario_rows = []

for sid in sorted(scenario_total_events):
    total = scenario_total_events[sid]
    alerted = len(scenario_alerted_events[sid])
    missed = total - alerted

    scenario_rows.append({
        "scenario_id": sid,
        "classification": scenario_classification[sid],
        "scenario_name": scenario_name[sid],
        "total_events": total,
        "alerted_events": alerted,
        "missed_events": missed,
        "total_alerts": scenario_alert_count[sid],
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
        "alerted_events",
        "missed_events",
        "total_alerts",
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

alerted_suspicious_scenarios = {
    row["scenario_id"]
    for row in scored_alerts
    if row["classification"] == "suspicious"
}

missed_suspicious_scenarios = (
    suspicious_scenarios
    - alerted_suspicious_scenarios
)


unique_users = {
    row["user"]
    for row in alerts
}

unique_sources = {
    row["src_ip"]
    for row in alerts
}

analyst_minutes = len(alerts) * MINUTES_PER_ALERT
analyst_hours = analyst_minutes / 60


metrics = [
    "Ticket #008 - Baseline Detection Metrics",
    "",
    f"Total authentication events: {len(events)}",
    f"Total alerts: {len(alerts)}",
    f"Unique alerted events: {len(alerted_event_ids)}",
    f"Unique users alerted: {len(unique_users)}",
    f"Unique sources alerted: {len(unique_sources)}",
    "",
    f"Benign alerts: {len(benign_alerts)}",
    f"Suspicious alerts: {len(suspicious_alerts)}",
    (
        "Alert-level benign share: "
        f"{alert_level_benign_share:.1f}%"
    ),
    "",
    f"Redundant/additional alerts: {redundant_alerts}",
    f"Redundancy rate: {redundancy_rate:.1f}%",
    "",
    f"Benign events alerted: {len(alerted_benign_events)}",
    (
        "Benign event alert rate: "
        f"{benign_event_alert_rate:.1f}%"
    ),
    "",
    (
        "Suspicious events alerted: "
        f"{len(alerted_suspicious_events)}"
    ),
    (
        "Suspicious events missed: "
        f"{len(missed_suspicious_events)}"
    ),
    (
        "Suspicious event detection rate: "
        f"{suspicious_event_detection_rate:.1f}%"
    ),
    "",
    (
        "Suspicious scenarios detected: "
        f"{len(alerted_suspicious_scenarios)} "
        f"of {len(suspicious_scenarios)}"
    ),
    (
        "Suspicious scenarios completely missed: "
        f"{len(missed_suspicious_scenarios)}"
    ),
    "",
    (
        f"Workload assumption: "
        f"{MINUTES_PER_ALERT} minutes per alert"
    ),
    (
        f"Estimated baseline analyst workload: "
        f"{analyst_hours:.2f} hours"
    ),
    "",
    "Important:",
    (
        "Scenario-level detection does not mean every important "
        "event or attack transition was detected."
    ),
    (
        "A scenario may be counted as detected when at least one "
        "event from that scenario generated an alert."
    ),
]


METRICS_FILE.write_text(
    "\n".join(metrics) + "\n",
    encoding="utf-8",
)


print("\n".join(metrics))

print("\nScenario Summary")

for row in scenario_rows:
    print(
        f'{row["scenario_id"]}: '
        f'{row["total_events"]} events, '
        f'{row["alerted_events"]} alerted events, '
        f'{row["missed_events"]} missed events, '
        f'{row["total_alerts"]} alerts'
    )

print(f"\nScored alerts: {SCORED_FILE}")
print(f"Scenario summary: {SCENARIO_FILE}")
print(f"Metrics: {METRICS_FILE}")
