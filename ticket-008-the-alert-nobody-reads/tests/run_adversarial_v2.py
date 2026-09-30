import csv
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "tests" / "adversarial-v1-alerts.csv"
OUTPUT_FILE = ROOT / "tests" / "adversarial-v2-cases.csv"

alerts = []

with INPUT_FILE.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        row["start_dt"] = datetime.fromisoformat(
            row["first_observed"]
        )
        row["end_dt"] = datetime.fromisoformat(
            row["last_observed"]
        )
        alerts.append(row)

alerts.sort(
    key=lambda row: (
        row["start_dt"],
        row["alert_id"],
    )
)

cases = []
case_counter = 1


def split_values(value):
    if not value:
        return []

    return [
        item
        for item in value.split(";")
        if item
    ]


def create_case(
    case_type,
    case_name,
    member_alerts,
    primary_user="",
    primary_source="",
):
    global case_counter

    member_alerts = sorted(
        member_alerts,
        key=lambda row: (
            row["start_dt"],
            row["alert_id"],
        )
    )

    users = set()
    sources = set()
    rule_ids = set()
    event_ids = set()

    successful_authentication = False
    any_privileged = False

    for alert in member_alerts:
        rule_ids.add(alert["rule_id"])

        users.update(
            split_values(alert["related_users"])
        )

        sources.update(
            split_values(alert["related_sources"])
        )

        event_ids.update(
            split_values(alert["related_event_ids"])
        )

        if (
            alert["successful_authentication"].lower()
            == "true"
        ):
            successful_authentication = True

        if (
            alert["any_privileged"].lower()
            == "true"
        ):
            any_privileged = True

    cases.append({
        "case_id": f"ADV-V2C-{case_counter:04d}",
        "case_type": case_type,
        "case_name": case_name,
        "first_observed": member_alerts[0]["first_observed"],
        "last_observed": member_alerts[-1]["last_observed"],
        "primary_user": primary_user,
        "primary_source": primary_source,
        "related_users": ";".join(sorted(users)),
        "related_sources": ";".join(sorted(sources)),
        "v1_rule_ids": ";".join(sorted(rule_ids)),
        "member_alert_ids": ";".join(
            alert["alert_id"]
            for alert in member_alerts
        ),
        "related_event_ids": ";".join(
            sorted(event_ids)
        ),
        "failure_count": len([
            event_id
            for event_id in event_ids
        ]),
        "successful_authentication": str(
            successful_authentication
        ).lower(),
        "any_privileged": str(
            any_privileged
        ).lower(),
    })

    case_counter += 1


# ---------------------------------------------------------
# V2-01 — Authentication Attack Sequence
#
# Correlates V1-01, V1-02, and V1-05 when the same
# primary user/source pair overlaps or occurs within
# 120 minutes of the preceding signal.
# ---------------------------------------------------------

sequence_alerts = [
    alert
    for alert in alerts
    if alert["rule_id"] in {
        "V1-01",
        "V1-02",
        "V1-05",
    }
]

sequence_groups = {}

for alert in sequence_alerts:
    key = (
        alert["primary_user"],
        alert["primary_source"],
    )

    sequence_groups.setdefault(
        key,
        [],
    ).append(alert)


for key, group in sequence_groups.items():
    group.sort(
        key=lambda row: (
            row["start_dt"],
            row["alert_id"],
        )
    )

    current = []

    for alert in group:
        if not current:
            current = [alert]
            continue

        current_end = max(
            item["end_dt"]
            for item in current
        )

        if (
            alert["start_dt"]
            <= current_end + timedelta(minutes=120)
        ):
            current.append(alert)

        else:
            create_case(
                "V2-01",
                "Authentication Attack Sequence",
                current,
                primary_user=key[0],
                primary_source=key[1],
            )

            current = [alert]

    if current:
        create_case(
            "V2-01",
            "Authentication Attack Sequence",
            current,
            primary_user=key[0],
            primary_source=key[1],
        )


# ---------------------------------------------------------
# V2-02 — Password Spray Campaign
#
# Merge V1-03 alerts whose time ranges overlap or whose
# next signal starts within 120 minutes after the current
# campaign end.
# ---------------------------------------------------------

spray_alerts = [
    alert
    for alert in alerts
    if alert["rule_id"] == "V1-03"
]

spray_alerts.sort(
    key=lambda row: (
        row["start_dt"],
        row["alert_id"],
    )
)

current = []

for alert in spray_alerts:
    if not current:
        current = [alert]
        continue

    current_end = max(
        item["end_dt"]
        for item in current
    )

    if (
        alert["start_dt"]
        <= current_end + timedelta(minutes=120)
    ):
        current.append(alert)

    else:
        create_case(
            "V2-02",
            "Password Spray Campaign",
            current,
        )

        current = [alert]

if current:
    create_case(
        "V2-02",
        "Password Spray Campaign",
        current,
    )


# ---------------------------------------------------------
# V2-03 — Distributed Targeting
#
# Group V1-04 alerts by targeted user.
# ---------------------------------------------------------

distributed_groups = {}

for alert in alerts:
    if alert["rule_id"] != "V1-04":
        continue

    user = alert["primary_user"]

    distributed_groups.setdefault(
        user,
        [],
    ).append(alert)


for user, group in distributed_groups.items():
    group.sort(
        key=lambda row: (
            row["start_dt"],
            row["alert_id"],
        )
    )

    current = []

    for alert in group:
        if not current:
            current = [alert]
            continue

        current_end = max(
            item["end_dt"]
            for item in current
        )

        if (
            alert["start_dt"]
            <= current_end + timedelta(minutes=120)
        ):
            current.append(alert)

        else:
            create_case(
                "V2-03",
                "Distributed Targeting",
                current,
                primary_user=user,
            )

            current = [alert]

    if current:
        create_case(
            "V2-03",
            "Distributed Targeting",
            current,
            primary_user=user,
        )


# ---------------------------------------------------------
# V2-04 — Persistent Service Authentication Case
#
# Group V1-06 alerts by service user/source.
# ---------------------------------------------------------

service_groups = {}

for alert in alerts:
    if alert["rule_id"] != "V1-06":
        continue

    key = (
        alert["primary_user"],
        alert["primary_source"],
    )

    service_groups.setdefault(
        key,
        [],
    ).append(alert)


for key, group in service_groups.items():
    group.sort(
        key=lambda row: (
            row["start_dt"],
            row["alert_id"],
        )
    )

    current = []

    for alert in group:
        if not current:
            current = [alert]
            continue

        current_end = max(
            item["end_dt"]
            for item in current
        )

        if (
            alert["start_dt"]
            <= current_end + timedelta(minutes=120)
        ):
            current.append(alert)

        else:
            create_case(
                "V2-04",
                "Persistent Service Authentication Case",
                current,
                primary_user=key[0],
                primary_source=key[1],
            )

            current = [alert]

    if current:
        create_case(
            "V2-04",
            "Persistent Service Authentication Case",
            current,
            primary_user=key[0],
            primary_source=key[1],
        )


fields = [
    "case_id",
    "case_type",
    "case_name",
    "first_observed",
    "last_observed",
    "primary_user",
    "primary_source",
    "related_users",
    "related_sources",
    "v1_rule_ids",
    "member_alert_ids",
    "related_event_ids",
    "failure_count",
    "successful_authentication",
    "any_privileged",
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


print(f"Adversarial V1 alerts consumed: {len(alerts)}")
print(f"V2 cases produced: {len(cases)}")

for case in cases:
    print(
        f"{case['case_id']} "
        f"{case['case_type']} "
        f"user={case['primary_user']} "
        f"source={case['primary_source']}"
    )

print(f"Output file: {OUTPUT_FILE}")
