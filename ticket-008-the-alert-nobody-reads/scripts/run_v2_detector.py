import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

V1_FILE = ROOT / "analysis" / "v1-alerts.csv"
EVENTS_FILE = ROOT / "dataset" / "authentication-events.csv"
OUTPUT_FILE = ROOT / "analysis" / "v2-cases.csv"

CORRELATION_GAP = timedelta(minutes=120)


def read_csv(path):
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


v1_alerts = read_csv(V1_FILE)
events = read_csv(EVENTS_FILE)

events_by_id = {
    row["event_id"]: row
    for row in events
}

for alert in v1_alerts:
    alert["first_dt"] = datetime.fromisoformat(
        alert["first_observed"]
    )
    alert["last_dt"] = datetime.fromisoformat(
        alert["last_observed"]
    )


def alert_event_ids(alert):
    return [
        event_id
        for event_id in alert["related_event_ids"].split(";")
        if event_id
    ]


def cluster_alerts(alerts, key_func):
    grouped = defaultdict(list)

    for alert in alerts:
        grouped[key_func(alert)].append(alert)

    clusters = []

    for key in sorted(grouped, key=lambda x: str(x)):
        rows = sorted(
            grouped[key],
            key=lambda row: (
                row["first_dt"],
                row["last_dt"],
                row["alert_id"],
            ),
        )

        if not rows:
            continue

        current = [rows[0]]
        current_end = rows[0]["last_dt"]

        for row in rows[1:]:
            if row["first_dt"] <= current_end + CORRELATION_GAP:
                current.append(row)

                if row["last_dt"] > current_end:
                    current_end = row["last_dt"]
            else:
                clusters.append(current)
                current = [row]
                current_end = row["last_dt"]

        clusters.append(current)

    return clusters


def unique_sorted(values):
    return sorted({
        value
        for value in values
        if value
    })


def build_case(rule_id, case_name, alerts):
    related_ids = []

    for alert in alerts:
        related_ids.extend(
            alert_event_ids(alert)
        )

    related_ids = sorted(
        set(related_ids),
        key=lambda event_id: (
            events_by_id[event_id]["timestamp"],
            event_id,
        ),
    )

    related_events = [
        events_by_id[event_id]
        for event_id in related_ids
    ]

    users = unique_sorted(
        row["user"]
        for row in related_events
    )

    sources = unique_sorted(
        row["src_ip"]
        for row in related_events
    )

    familiarities = unique_sorted(
        row["source_familiarity"]
        for row in related_events
    )

    failure_count = sum(
        1
        for row in related_events
        if row["auth_result"] == "failure"
    )

    any_privileged = any(
        row["is_privileged"] == "true"
        for row in related_events
    )

    successful_authentication = any(
        row["auth_result"] == "success"
        for row in related_events
    )

    contributing_alert_ids = [
        row["alert_id"]
        for row in sorted(
            alerts,
            key=lambda row: (
                row["first_dt"],
                row["alert_id"],
            ),
        )
    ]

    contributing_rule_ids = unique_sorted(
        row["rule_id"]
        for row in alerts
    )

    first_observed = min(
        row["timestamp"]
        for row in related_events
    )

    last_observed = max(
        row["timestamp"]
        for row in related_events
    )

    if len(users) == 1:
        primary_user = users[0]
    else:
        primary_user = "MULTIPLE"

    if len(sources) == 1:
        primary_source = sources[0]
    else:
        primary_source = "MULTIPLE"

    if rule_id == "V2-01":
        reason = (
            f"Correlated {len(alerts)} V1 authentication "
            f"signals for {primary_user} from "
            f"{primary_source}. Contributing rules: "
            f"{','.join(contributing_rule_ids)}."
        )

        if successful_authentication:
            reason += (
                " A successful authentication occurred "
                "within the correlated attack sequence."
            )

    elif rule_id == "V2-02":
        reason = (
            f"Correlated {len(alerts)} V1 password-spray "
            f"signals into one campaign involving "
            f"{len(sources)} sources and "
            f"{len(users)} targeted users."
        )

    elif rule_id == "V2-03":
        reason = (
            f"Correlated distributed targeting of "
            f"{primary_user} from "
            f"{len(sources)} sources."
        )

    elif rule_id == "V2-04":
        reason = (
            f"Correlated persistent service authentication "
            f"failures for {primary_user} from "
            f"{primary_source}."
        )

    else:
        reason = "Correlated V1 authentication investigation."

    return {
        "rule_id": rule_id,
        "case_name": case_name,
        "first_observed": first_observed,
        "last_observed": last_observed,
        "primary_user": primary_user,
        "primary_source": primary_source,
        "related_users": ";".join(users),
        "related_sources": ";".join(sources),
        "unique_failure_count": failure_count,
        "distinct_user_count": len(users),
        "distinct_source_count": len(sources),
        "any_privileged": str(any_privileged).lower(),
        "source_familiarity": ";".join(familiarities),
        "successful_authentication": (
            str(successful_authentication).lower()
        ),
        "contributing_v1_alert_ids": ";".join(
            contributing_alert_ids
        ),
        "contributing_v1_rule_ids": ";".join(
            contributing_rule_ids
        ),
        "related_event_ids": ";".join(related_ids),
        "reason": reason,
    }


cases = []


# ---------------------------------------------------------
# V2-01 — Authentication Attack Sequence
# ---------------------------------------------------------
sequence_alerts = [
    row
    for row in v1_alerts
    if row["rule_id"] in {
        "V1-01",
        "V1-02",
        "V1-05",
    }
]

sequence_clusters = cluster_alerts(
    sequence_alerts,
    lambda row: (
        row["primary_user"],
        row["primary_source"],
    ),
)

for cluster in sequence_clusters:
    cases.append(
        build_case(
            "V2-01",
            "Authentication Attack Sequence",
            cluster,
        )
    )


# ---------------------------------------------------------
# V2-02 — Password Spray Campaign
# ---------------------------------------------------------
spray_alerts = [
    row
    for row in v1_alerts
    if row["rule_id"] == "V1-03"
]

spray_clusters = cluster_alerts(
    spray_alerts,
    lambda row: "password-spray-campaign",
)

for cluster in spray_clusters:
    cases.append(
        build_case(
            "V2-02",
            "Password Spray Campaign",
            cluster,
        )
    )


# ---------------------------------------------------------
# V2-03 — Distributed Targeting Case
# ---------------------------------------------------------
distributed_alerts = [
    row
    for row in v1_alerts
    if row["rule_id"] == "V1-04"
]

distributed_clusters = cluster_alerts(
    distributed_alerts,
    lambda row: row["primary_user"],
)

for cluster in distributed_clusters:
    cases.append(
        build_case(
            "V2-03",
            "Distributed Targeting Case",
            cluster,
        )
    )


# ---------------------------------------------------------
# V2-04 — Persistent Service Authentication Case
# ---------------------------------------------------------
service_alerts = [
    row
    for row in v1_alerts
    if row["rule_id"] == "V1-06"
]

service_clusters = cluster_alerts(
    service_alerts,
    lambda row: (
        row["primary_user"],
        row["primary_source"],
    ),
)

for cluster in service_clusters:
    cases.append(
        build_case(
            "V2-04",
            "Persistent Service Authentication Case",
            cluster,
        )
    )


# ---------------------------------------------------------
# Sort and assign stable case IDs.
# ---------------------------------------------------------
cases.sort(
    key=lambda row: (
        row["first_observed"],
        row["rule_id"],
        row["primary_user"],
        row["primary_source"],
    )
)

for index, case in enumerate(cases, start=1):
    case["case_id"] = f"V2C-{index:04d}"


fields = [
    "case_id",
    "rule_id",
    "case_name",
    "first_observed",
    "last_observed",
    "primary_user",
    "primary_source",
    "related_users",
    "related_sources",
    "unique_failure_count",
    "distinct_user_count",
    "distinct_source_count",
    "any_privileged",
    "source_familiarity",
    "successful_authentication",
    "contributing_v1_alert_ids",
    "contributing_v1_rule_ids",
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
    writer.writerows(cases)


counts = defaultdict(int)

for case in cases:
    counts[case["rule_id"]] += 1


print(f"Input V1 alerts: {len(v1_alerts)}")
print(f"Input authentication events: {len(events)}")
print(f"Total V2 cases: {len(cases)}")

for rule_id in sorted(counts):
    print(f"{rule_id}: {counts[rule_id]}")

print(f"Output file: {OUTPUT_FILE}")

