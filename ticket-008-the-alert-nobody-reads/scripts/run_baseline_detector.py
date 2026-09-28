import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "dataset" / "authentication-events.csv"
OUTPUT_FILE = ROOT / "analysis" / "baseline-alerts.csv"

events = []

with INPUT_FILE.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        row["dt"] = datetime.fromisoformat(row["timestamp"])
        events.append(row)

events.sort(key=lambda row: (row["dt"], row["event_id"]))

alerts = []
alert_counter = 1

failure_history = defaultdict(list)


def add_alert(event, rule_id, rule_name, detail):
    global alert_counter

    alerts.append({
        "alert_id": f"BASE-{alert_counter:04d}",
        "event_id": event["event_id"],
        "timestamp": event["timestamp"],
        "user": event["user"],
        "src_ip": event["src_ip"],
        "src_host": event["src_host"],
        "auth_result": event["auth_result"],
        "account_type": event["account_type"],
        "is_privileged": event["is_privileged"],
        "source_familiarity": event["source_familiarity"],
        "source_zone": event["source_zone"],
        "target_system": event["target_system"],
        "rule_id": rule_id,
        "rule_name": rule_name,
        "detail": detail,
    })

    alert_counter += 1


for event in events:

    if event["auth_result"] != "failure":
        continue

    user = event["user"]
    now = event["dt"]

    # Rule 1 - every failed authentication alerts.
    add_alert(
        event,
        "BASE-R1",
        "Failed Authentication",
        "Individual authentication failure observed.",
    )

    # Maintain rolling 10-minute failure history for the user.
    cutoff = now - timedelta(minutes=10)

    failure_history[user] = [
        ts
        for ts in failure_history[user]
        if ts >= cutoff
    ]

    failure_history[user].append(now)

    # Rule 2 - repeated failure alert.
    if len(failure_history[user]) >= 3:
        add_alert(
            event,
            "BASE-R2",
            "Repeated Failures",
            (
                f"{len(failure_history[user])} failures for "
                f"{user} within rolling 10-minute window."
            ),
        )

    # Rule 3 - unfamiliar source failure.
    if event["source_familiarity"] == "unfamiliar":
        add_alert(
            event,
            "BASE-R3",
            "Unfamiliar Source Failure",
            "Failed authentication originated from unfamiliar source.",
        )

    # Rule 4 - privileged account failure.
    if event["is_privileged"] == "true":
        add_alert(
            event,
            "BASE-R4",
            "Privileged Account Failure",
            "Failed authentication involved a privileged account.",
        )


fields = [
    "alert_id",
    "event_id",
    "timestamp",
    "user",
    "src_ip",
    "src_host",
    "auth_result",
    "account_type",
    "is_privileged",
    "source_familiarity",
    "source_zone",
    "target_system",
    "rule_id",
    "rule_name",
    "detail",
]


with OUTPUT_FILE.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=fields,
    )

    writer.writeheader()
    writer.writerows(alerts)


rule_counts = defaultdict(int)

for alert in alerts:
    rule_counts[alert["rule_id"]] += 1


print(f"Input events: {len(events)}")
print(f"Total baseline alerts: {len(alerts)}")

for rule_id in sorted(rule_counts):
    print(f"{rule_id}: {rule_counts[rule_id]}")

print(f"Output file: {OUTPUT_FILE}")
