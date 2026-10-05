import csv
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EVENTS_FILE = ROOT / "data" / "adversarial-auth-events.csv"
TRUTH_FILE = ROOT / "data" / "adversarial-ground-truth.csv"

events = []
truth = []

event_counter = 1


def add_event(
    test_id,
    variation_name,
    timestamp,
    user,
    src_ip,
    auth_result,
    account_type="user",
    is_privileged="false",
    source_familiarity="unfamiliar",
):
    global event_counter

    event_id = f"AT-{event_counter:04d}"

    events.append({
        "event_id": event_id,
        "timestamp": timestamp.isoformat(),
        "user": user,
        "src_ip": src_ip,
        "auth_result": auth_result,
        "account_type": account_type,
        "is_privileged": is_privileged,
        "source_familiarity": source_familiarity,
    })

    truth.append({
        "event_id": event_id,
        "test_id": test_id,
        "classification": "suspicious",
        "variation_name": variation_name,
    })

    event_counter += 1


# ---------------------------------------------------------
# AT-01 — Threshold Skimming
# 4 failures / same non-privileged user / same unfamiliar source
# over 9 minutes.
# ---------------------------------------------------------
start = datetime(2026, 9, 30, 9, 0, 0)

for minutes in [0, 3, 6, 9]:
    add_event(
        test_id="AT-01",
        variation_name="Threshold Skimming",
        timestamp=start + timedelta(minutes=minutes),
        user="jcarter",
        src_ip="203.0.113.41",
        auth_result="failure",
        account_type="user",
        is_privileged="false",
        source_familiarity="unfamiliar",
    )


# ---------------------------------------------------------
# AT-02 — Distributed Many-to-Many Campaign
#
# 12 failures
# 6 users
# 4 unfamiliar sources
# 20-minute spacing
# total span = 3h40m
#
# Constraints:
# - no user/source pair reaches 5 failures
# - each source has only 3 total failures
# - each user has only 2 total failures
# - repeated attempts against a user are 120 minutes apart
# ---------------------------------------------------------
start = datetime(2026, 9, 30, 10, 0, 0)

users = [
    "aalvarez",
    "bchen",
    "dgreen",
    "emorris",
    "fpatel",
    "gwhite",
]

sources = [
    "198.51.100.41",
    "198.51.100.42",
    "198.51.100.43",
    "198.51.100.44",
]

for i in range(12):
    add_event(
        test_id="AT-02",
        variation_name="Distributed Many-to-Many Campaign",
        timestamp=start + timedelta(minutes=20 * i),
        user=users[i % len(users)],
        src_ip=sources[i % len(sources)],
        auth_result="failure",
        account_type="user",
        is_privileged="false",
        source_familiarity="unfamiliar",
    )


# ---------------------------------------------------------
# AT-03 — Familiar-Source Failures Followed by Success
#
# 4 failures within 6 minutes
# then a successful authentication at minute 8.
# ---------------------------------------------------------
start = datetime(2026, 10, 1, 9, 0, 0)

for minutes in [0, 2, 4, 6]:
    add_event(
        test_id="AT-03",
        variation_name="Familiar-Source Failures Followed by Success",
        timestamp=start + timedelta(minutes=minutes),
        user="rthomas",
        src_ip="10.20.10.44",
        auth_result="failure",
        account_type="user",
        is_privileged="false",
        source_familiarity="familiar",
    )

add_event(
    test_id="AT-03",
    variation_name="Familiar-Source Failures Followed by Success",
    timestamp=start + timedelta(minutes=8),
    user="rthomas",
    src_ip="10.20.10.44",
    auth_result="success",
    account_type="user",
    is_privileged="false",
    source_familiarity="familiar",
)


# ---------------------------------------------------------
# AT-04 — Privileged Low-and-Slow Control Case
#
# 4 failures
# privileged account
# unfamiliar source
# 30-minute spacing
# all within 120 minutes.
# ---------------------------------------------------------
start = datetime(2026, 10, 1, 12, 0, 0)

for minutes in [0, 30, 60, 90]:
    add_event(
        test_id="AT-04",
        variation_name="Privileged Low-and-Slow Control Case",
        timestamp=start + timedelta(minutes=minutes),
        user="sec.admin",
        src_ip="203.0.113.88",
        auth_result="failure",
        account_type="user",
        is_privileged="true",
        source_familiarity="unfamiliar",
    )


events.sort(
    key=lambda row: (
        row["timestamp"],
        row["event_id"],
    )
)

event_fields = [
    "event_id",
    "timestamp",
    "user",
    "src_ip",
    "auth_result",
    "account_type",
    "is_privileged",
    "source_familiarity",
]

truth_fields = [
    "event_id",
    "test_id",
    "classification",
    "variation_name",
]


with EVENTS_FILE.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=event_fields,
    )
    writer.writeheader()
    writer.writerows(events)


with TRUTH_FILE.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=truth_fields,
    )
    writer.writeheader()
    writer.writerows(truth)


print(f"Adversarial events: {len(events)}")
print(f"AT-01 events: {sum(1 for r in truth if r['test_id'] == 'AT-01')}")
print(f"AT-02 events: {sum(1 for r in truth if r['test_id'] == 'AT-02')}")
print(f"AT-03 events: {sum(1 for r in truth if r['test_id'] == 'AT-03')}")
print(f"AT-04 events: {sum(1 for r in truth if r['test_id'] == 'AT-04')}")
print(f"Events file: {EVENTS_FILE}")
print(f"Ground truth file: {TRUTH_FILE}")
