import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "dataset" / "authentication-events.csv"
OUTPUT_FILE = ROOT / "analysis" / "v1-alerts.csv"

events = []

with INPUT_FILE.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        row["dt"] = datetime.fromisoformat(row["timestamp"])
        events.append(row)

events.sort(key=lambda row: (row["dt"], row["event_id"]))

alerts = []
alert_counter = 1

# Failure histories.
user_source_failures = defaultdict(list)
source_failures = defaultdict(list)
user_failures = defaultdict(list)

# Prevent repeated alerts for the same investigation pattern.
alerted_keys = set()


def recent(rows, now, minutes):
    cutoff = now - timedelta(minutes=minutes)

    return [
        row
        for row in rows
        if row["dt"] >= cutoff and row["dt"] <= now
    ]


def unique_values(rows, field):
    return sorted({
        row[field]
        for row in rows
        if row.get(field)
    })


def add_alert(
    rule_id,
    rule_name,
    trigger_event,
    related_events,
    primary_user="",
    primary_source="",
    success=False,
    reason="",
):
    global alert_counter

    related_sorted = sorted(
        related_events,
        key=lambda row: (row["dt"], row["event_id"])
    )

    users = unique_values(related_sorted, "user")
    sources = unique_values(related_sorted, "src_ip")
    familiarities = unique_values(
        related_sorted,
        "source_familiarity",
    )

    failure_count = sum(
        1
        for row in related_sorted
        if row["auth_result"] == "failure"
    )

    any_privileged = any(
        row["is_privileged"] == "true"
        for row in related_sorted
    )

    alerts.append({
        "alert_id": f"V1-{alert_counter:04d}",
        "rule_id": rule_id,
        "rule_name": rule_name,
        "first_observed": related_sorted[0]["timestamp"],
        "last_observed": related_sorted[-1]["timestamp"],
        "trigger_event_id": trigger_event["event_id"],
        "primary_user": primary_user,
        "primary_source": primary_source,
        "related_users": ";".join(users),
        "related_sources": ";".join(sources),
        "failure_count": failure_count,
        "distinct_user_count": len(users),
        "distinct_source_count": len(sources),
        "any_privileged": str(any_privileged).lower(),
        "source_familiarity": ";".join(familiarities),
        "successful_authentication": str(success).lower(),
        "related_event_ids": ";".join(
            row["event_id"]
            for row in related_sorted
        ),
        "reason": reason,
    })

    alert_counter += 1


for event in events:
    now = event["dt"]
    user = event["user"]
    source = event["src_ip"]
    user_source_key = (user, source)

    # ---------------------------------------------------------
    # SUCCESS EVENTS
    # ---------------------------------------------------------
    if event["auth_result"] == "success":

        failures_10 = recent(
            user_source_failures[user_source_key],
            now,
            10,
        )

        # V1-02 - Suspicious Success After Failures
        success_key = ("V1-02", user, source)

        enough_failures = len(failures_10) >= 5
        privileged_failures = (
            event["is_privileged"] == "true"
            and len(failures_10) >= 3
        )

        if (
            success_key not in alerted_keys
            and (enough_failures or privileged_failures)
        ):
            related = failures_10 + [event]

            add_alert(
                "V1-02",
                "Suspicious Success After Failures",
                event,
                related,
                primary_user=user,
                primary_source=source,
                success=True,
                reason=(
                    f"Successful authentication followed "
                    f"{len(failures_10)} failures for "
                    f"{user} from {source} within 10 minutes."
                ),
            )

            alerted_keys.add(success_key)

        continue

    # ---------------------------------------------------------
    # FAILURE EVENTS
    # ---------------------------------------------------------
    if event["auth_result"] != "failure":
        continue

    user_source_failures[user_source_key].append(event)
    source_failures[source].append(event)
    user_failures[user].append(event)

    # ---------------------------------------------------------
    # V1-01 - Rapid Repeated Authentication Failures
    # ---------------------------------------------------------
    failures_10 = recent(
        user_source_failures[user_source_key],
        now,
        10,
    )

    rapid_key = ("V1-01", user, source)

    if (
        rapid_key not in alerted_keys
        and len(failures_10) >= 5
    ):
        add_alert(
            "V1-01",
            "Rapid Repeated Authentication Failures",
            event,
            failures_10,
            primary_user=user,
            primary_source=source,
            reason=(
                f"{len(failures_10)} failures for "
                f"{user} from {source} within 10 minutes."
            ),
        )

        alerted_keys.add(rapid_key)

    # ---------------------------------------------------------
    # V1-03 - Password Spray: One Source, Many Users
    # ---------------------------------------------------------
    source_120 = recent(
        source_failures[source],
        now,
        120,
    )

    source_users = unique_values(
        source_120,
        "user",
    )

    spray_key = ("V1-03", source)

    if (
        spray_key not in alerted_keys
        and len(source_users) >= 5
    ):
        add_alert(
            "V1-03",
            "Password Spray - One Source, Many Users",
            event,
            source_120,
            primary_source=source,
            reason=(
                f"Source {source} generated failures "
                f"against {len(source_users)} distinct "
                f"users within 120 minutes."
            ),
        )

        alerted_keys.add(spray_key)

    # ---------------------------------------------------------
    # V1-04 - Distributed Targeting: Many Sources, One User
    # ---------------------------------------------------------
    user_60 = recent(
        user_failures[user],
        now,
        60,
    )

    user_sources = unique_values(
        user_60,
        "src_ip",
    )

    distributed_key = ("V1-04", user)

    if (
        distributed_key not in alerted_keys
        and len(user_sources) >= 3
    ):
        add_alert(
            "V1-04",
            "Distributed Targeting - Many Sources, One User",
            event,
            user_60,
            primary_user=user,
            reason=(
                f"User {user} received failures from "
                f"{len(user_sources)} distinct sources "
                f"within 60 minutes."
            ),
        )

        alerted_keys.add(distributed_key)

    # ---------------------------------------------------------
    # V1-05 - Low-and-Slow Privileged Authentication
    # ---------------------------------------------------------
    privileged_120 = recent(
        user_source_failures[user_source_key],
        now,
        120,
    )

    privileged_key = ("V1-05", user, source)

    if (
        privileged_key not in alerted_keys
        and event["is_privileged"] == "true"
        and event["source_familiarity"] == "unfamiliar"
        and len(privileged_120) >= 4
    ):
        add_alert(
            "V1-05",
            "Low-and-Slow Privileged Authentication Activity",
            event,
            privileged_120,
            primary_user=user,
            primary_source=source,
            reason=(
                f"Privileged account {user} received "
                f"{len(privileged_120)} failures from "
                f"unfamiliar source {source} "
                f"within 120 minutes."
            ),
        )

        alerted_keys.add(privileged_key)

    # ---------------------------------------------------------
    # V1-06 - Persistent Service Authentication Failure
    # ---------------------------------------------------------
    service_15 = recent(
        user_source_failures[user_source_key],
        now,
        15,
    )

    service_key = ("V1-06", user, source)

    if (
        service_key not in alerted_keys
        and event["account_type"] == "service"
        and len(service_15) >= 3
    ):
        add_alert(
            "V1-06",
            "Persistent Service Authentication Failure",
            event,
            service_15,
            primary_user=user,
            primary_source=source,
            reason=(
                f"Service account {user} generated "
                f"{len(service_15)} failures from "
                f"{source} within 15 minutes."
            ),
        )

        alerted_keys.add(service_key)


fields = [
    "alert_id",
    "rule_id",
    "rule_name",
    "first_observed",
    "last_observed",
    "trigger_event_id",
    "primary_user",
    "primary_source",
    "related_users",
    "related_sources",
    "failure_count",
    "distinct_user_count",
    "distinct_source_count",
    "any_privileged",
    "source_familiarity",
    "successful_authentication",
    "related_event_ids",
    "reason",
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
print(f"Total V1 alerts: {len(alerts)}")

for rule_id in sorted(rule_counts):
    print(f"{rule_id}: {rule_counts[rule_id]}")

print(f"Output file: {OUTPUT_FILE}")
