import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SEED = 8008
random.seed(SEED)

ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "data"
DATASET_DIR.mkdir(parents=True, exist_ok=True)

TELEMETRY_FILE = DATASET_DIR / "authentication-events.csv"
TRUTH_FILE = DATASET_DIR / "authentication-ground-truth.csv"

events = []
truth = []
event_counter = 1


def add_event(ts, user, src_ip, src_host, result, account_type,
              privileged, familiarity, zone, target, scenario_id,
              classification, scenario_name):
    global event_counter

    event_id = f"AUTH-{event_counter:04d}"

    events.append({
        "event_id": event_id,
        "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S"),
        "user": user,
        "src_ip": src_ip,
        "src_host": src_host,
        "auth_result": result,
        "auth_method": "password",
        "account_type": account_type,
        "is_privileged": str(privileged).lower(),
        "source_familiarity": familiarity,
        "source_zone": zone,
        "target_system": target,
    })

    truth.append({
        "event_id": event_id,
        "scenario_id": scenario_id,
        "classification": classification,
        "scenario_name": scenario_name,
    })

    event_counter += 1


def random_business_time(day_offset):
    day = datetime(2026, 9, 21, 8, 0, 0) + timedelta(days=day_offset)

    return day + timedelta(
        hours=random.randint(0, 9),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )


ordinary_users = [
    "asmith", "bjones", "cpatel", "dlee", "egarcia",
    "fthomas", "gmartin", "hrobinson", "ikhan", "jwilson",
    "kbrown", "lchen", "mjohnson", "nclark", "odavis",
    "pmiller", "qwalker", "rhall", "sallen", "tmoore",
    "uwhite", "vyoung", "wking", "xscott", "yhill",
    "zadams", "abaker", "bnelson", "ccarter", "dmitchell",
]

workstations = [
    ("10.20.10.11", "WS-011"),
    ("10.20.10.12", "WS-012"),
    ("10.20.10.13", "WS-013"),
    ("10.20.10.14", "WS-014"),
    ("10.20.10.15", "WS-015"),
    ("10.20.10.16", "WS-016"),
    ("10.20.10.17", "WS-017"),
    ("10.20.10.18", "WS-018"),
    ("10.20.10.19", "WS-019"),
    ("10.20.10.20", "WS-020"),
]


# LEG-01 - Normal business authentication: 600 events
for i in range(600):
    user = random.choice(ordinary_users)
    src_ip, src_host = random.choice(workstations)

    result = "success" if i < 580 else "failure"

    add_event(
        random_business_time(i % 5),
        user,
        src_ip,
        src_host,
        result,
        "user",
        False,
        "familiar",
        "internal",
        "CORP-AUTH",
        "LEG-01",
        "benign",
        "Normal Business Authentication",
    )


# LEG-02 - Ordinary password mistakes: 90 events
# 30 sequences of two failures followed by success.
for i in range(30):
    user = ordinary_users[i % len(ordinary_users)]
    src_ip, src_host = workstations[i % len(workstations)]

    start = (
        datetime(2026, 9, 22, 9, 15, 0)
        + timedelta(minutes=i * 12)
    )

    for offset, result in [
        (0, "failure"),
        (18, "failure"),
        (41, "success"),
    ]:
        add_event(
            start + timedelta(seconds=offset),
            user,
            src_ip,
            src_host,
            result,
            "user",
            False,
            "familiar",
            "internal",
            "CORP-AUTH",
            "LEG-02",
            "benign",
            "Ordinary Password Mistakes",
        )


# LEG-03 - Stale service credentials: 72 failures
service_start = datetime(2026, 9, 23, 6, 0, 0)

for i in range(72):
    add_event(
        service_start + timedelta(minutes=i * 5),
        "svc_inventory",
        "10.20.30.25",
        "APP-SRV-25",
        "failure",
        "service",
        False,
        "familiar",
        "internal",
        "CORP-AUTH",
        "LEG-03",
        "benign",
        "Stale Service Credentials",
    )


# LEG-04 - Benign unfamiliar source: 48 events
remote_sources = [
    ("198.51.100.21", "REMOTE-21"),
    ("198.51.100.34", "REMOTE-34"),
    ("203.0.113.45", "REMOTE-45"),
    ("203.0.113.58", "REMOTE-58"),
]

for i in range(48):
    user = ordinary_users[i % 12]
    src_ip, src_host = remote_sources[i % len(remote_sources)]

    result = "failure" if i < 8 else "success"

    ts = (
        datetime(2026, 9, 24, 7, 30, 0)
        + timedelta(minutes=i * 11)
    )

    add_event(
        ts,
        user,
        src_ip,
        src_host,
        result,
        "user",
        False,
        "unfamiliar",
        "external",
        "VPN-AUTH",
        "LEG-04",
        "benign",
        "Benign Unfamiliar Source",
    )


# LEG-05 - Legitimate privileged administration: 45 events
admin_start = datetime(2026, 9, 24, 9, 0, 0)

for i in range(45):
    result = "failure" if i < 5 else "success"

    add_event(
        admin_start + timedelta(minutes=i * 9),
        "admin.ops",
        "10.20.40.10",
        "ADMIN-JUMP-01",
        result,
        "admin",
        True,
        "familiar",
        "admin",
        "PRIV-AUTH",
        "LEG-05",
        "benign",
        "Legitimate Privileged Administration",
    )


# SUS-01 - Concentrated brute force: 35 failures
brute_start = datetime(2026, 9, 25, 10, 5, 0)

for i in range(35):
    add_event(
        brute_start + timedelta(seconds=i * 8),
        "mjohnson",
        "203.0.113.201",
        "EXT-201",
        "failure",
        "user",
        False,
        "unfamiliar",
        "external",
        "VPN-AUTH",
        "SUS-01",
        "suspicious",
        "Concentrated Brute-Force Activity",
    )


# SUS-02 - Eight failures followed by privileged success
priv_start = datetime(2026, 9, 26, 2, 13, 0)

for i in range(8):
    add_event(
        priv_start + timedelta(seconds=i * 22),
        "admin.backup",
        "198.51.100.88",
        "EXT-88",
        "failure",
        "admin",
        True,
        "unfamiliar",
        "external",
        "PRIV-AUTH",
        "SUS-02",
        "suspicious",
        "Failures Followed by Privileged Success",
    )

add_event(
    priv_start + timedelta(minutes=3, seconds=20),
    "admin.backup",
    "198.51.100.88",
    "EXT-88",
    "success",
    "admin",
    True,
    "unfamiliar",
    "external",
    "PRIV-AUTH",
    "SUS-02",
    "suspicious",
    "Failures Followed by Privileged Success",
)


# SUS-03 - Distributed password spray: 60 failures
spray_sources = [
    ("203.0.113.101", "SPRAY-101"),
    ("203.0.113.102", "SPRAY-102"),
    ("198.51.100.131", "SPRAY-131"),
    ("198.51.100.132", "SPRAY-132"),
    ("192.0.2.71", "SPRAY-071"),
    ("192.0.2.72", "SPRAY-072"),
]

spray_start = datetime(2026, 9, 25, 13, 0, 0)

for i in range(60):
    user = ordinary_users[i % 30]
    src_ip, src_host = spray_sources[i % len(spray_sources)]

    add_event(
        spray_start + timedelta(minutes=i * 4),
        user,
        src_ip,
        src_host,
        "failure",
        "user",
        False,
        "unfamiliar",
        "external",
        "VPN-AUTH",
        "SUS-03",
        "suspicious",
        "Distributed Password Spray",
    )


# SUS-04 - Low-and-slow attack: 18 failures
slow_start = datetime(2026, 9, 26, 0, 30, 0)

for i in range(18):
    add_event(
        slow_start + timedelta(minutes=i * 21),
        "finance.admin",
        "192.0.2.155",
        "EXT-155",
        "failure",
        "admin",
        True,
        "unfamiliar",
        "external",
        "PRIV-AUTH",
        "SUS-04",
        "suspicious",
        "Low-and-Slow Authentication Attack",
    )


# SUS-05 - Compromised familiar source: 12 failures then success
comp_start = datetime(2026, 9, 25, 16, 20, 0)

for i in range(12):
    add_event(
        comp_start + timedelta(seconds=i * 17),
        "payroll.manager",
        "10.20.10.18",
        "WS-018",
        "failure",
        "user",
        False,
        "familiar",
        "internal",
        "CORP-AUTH",
        "SUS-05",
        "suspicious",
        "Compromised Familiar Source",
    )

add_event(
    comp_start + timedelta(minutes=4),
    "payroll.manager",
    "10.20.10.18",
    "WS-018",
    "success",
    "user",
    False,
    "familiar",
    "internal",
    "CORP-AUTH",
    "SUS-05",
    "suspicious",
    "Compromised Familiar Source",
)


# SUS-06 - Distributed attack against one account: 10 failures
dist_sources = [
    ("203.0.113.211", "DIST-211"),
    ("198.51.100.212", "DIST-212"),
    ("192.0.2.213", "DIST-213"),
    ("203.0.113.214", "DIST-214"),
    ("198.51.100.215", "DIST-215"),
]

dist_start = datetime(2026, 9, 26, 4, 0, 0)

for i in range(10):
    src_ip, src_host = dist_sources[i % len(dist_sources)]

    add_event(
        dist_start + timedelta(minutes=i * 7),
        "vp.operations",
        src_ip,
        src_host,
        "failure",
        "user",
        False,
        "unfamiliar",
        "external",
        "VPN-AUTH",
        "SUS-06",
        "suspicious",
        "Distributed Attack Against One Account",
    )


# Validate expected totals.
assert len(events) == 1000, (
    f"Expected 1000 events, got {len(events)}"
)

assert len(truth) == 1000, (
    f"Expected 1000 truth rows, got {len(truth)}"
)


# Sort telemetry chronologically while preserving event IDs.
events.sort(
    key=lambda row: (
        row["timestamp"],
        row["event_id"],
    )
)


telemetry_fields = [
    "event_id",
    "timestamp",
    "user",
    "src_ip",
    "src_host",
    "auth_result",
    "auth_method",
    "account_type",
    "is_privileged",
    "source_familiarity",
    "source_zone",
    "target_system",
]

truth_fields = [
    "event_id",
    "scenario_id",
    "classification",
    "scenario_name",
]


with TELEMETRY_FILE.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=telemetry_fields,
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


benign_count = sum(
    1
    for row in truth
    if row["classification"] == "benign"
)

suspicious_count = sum(
    1
    for row in truth
    if row["classification"] == "suspicious"
)


print(f"Seed: {SEED}")
print(f"Telemetry file: {TELEMETRY_FILE}")
print(f"Ground truth file: {TRUTH_FILE}")
print(f"Total events: {len(events)}")
print(f"Benign events: {benign_count}")
print(f"Suspicious events: {suspicious_count}")
