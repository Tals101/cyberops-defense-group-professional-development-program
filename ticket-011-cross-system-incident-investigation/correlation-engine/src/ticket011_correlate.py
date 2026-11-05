#!/usr/bin/env python3
"""Ticket 011: synthetic-only event correlation."""

import hashlib
import ipaddress
import itertools
import json
import sys

from collections import defaultdict
from datetime import datetime
from pathlib import Path


SOURCES = (
    (
        "AWS_CLOUDTRAIL", "AWS",
        "evidence/aws/cloudtrail-synthetic.jsonl", 12
    ),
    (
        "K8S_AUDIT", "KUBERNETES",
        "evidence/kubernetes/kubernetes-audit-synthetic.jsonl", 6
    ),
    (
        "K8S_FALCO", "KUBERNETES",
        "evidence/kubernetes/falco-runtime-synthetic.jsonl", 4
    ),
    (
        "K8S_NETWORK", "KUBERNETES",
        "evidence/kubernetes/network-flow-synthetic.jsonl", 2
    ),
    (
        "LINUX_AUTH", "LINUX",
        "evidence/linux/linux-auth-synthetic.jsonl", 9
    ),
    (
        "LINUX_PROCESS", "LINUX",
        "evidence/linux/linux-process-persistence-synthetic.jsonl", 6
    ),
    (
        "LINUX_NETWORK", "LINUX",
        "evidence/linux/linux-network-synthetic.jsonl", 3
    ),
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().lower()


def field(record, *keys):
    for key in keys:
        value = record.get(key)
        if value is not None and value != "":
            return str(value)
    return ""


def actor_of(record):
    identity = record.get("userIdentity") or {}

    if not isinstance(identity, dict):
        identity = {}

    return field(
        record, "actor", "actorIdentity"
    ) or field(
        identity, "userName", "principalId", "arn"
    )


def parse_utc(value):
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(
            "Expected explicit UTC timestamp ending in Z"
        )

    parsed = datetime.fromisoformat(
        value[:-1] + "+00:00"
    )

    if parsed.utcoffset().total_seconds() != 0:
        raise ValueError("Timestamp not UTC")

    return parsed


def valid_ip(value):
    if not value:
        return ""

    try:
        return str(ipaddress.ip_address(value))
    except ValueError:
        return ""


def read_source(root, spec, expected):
    sid, scope, relative, expected_count = spec

    info = expected[sid]

    if info["RelativePath"].replace("\\", "/") != relative:
        raise ValueError(
            "Schema audit path changed for " + sid
        )

    path = root / relative

    if not path.is_file():
        raise ValueError("Missing source: " + relative)

    current_hash = sha256(path)

    if current_hash != info["SHA256"].lower():
        raise ValueError(
            "Source SHA256 changed: " + relative
        )

    rows = []
    seen_ids = set()

    for lineno, line in enumerate(
        path.read_text(encoding="utf-8-sig").splitlines(), 1
    ):
        if not line.strip():
            raise ValueError(
                "Blank JSONL line: " + relative
            )

        raw = json.loads(line)

        if not isinstance(raw, dict):
            raise ValueError(
                "JSONL object expected: " + relative
            )

        required_type = (
            "SYNTHETIC_LABORATORY_DATA"
            if scope == "LINUX"
            else "SYNTHETIC"
        )

        dataset_type = raw.get("datasetType")

        if dataset_type != required_type:
            raise ValueError(
                "Synthetic provenance mismatch: " + relative
            )

        original_id = field(
            raw, "eventID", "eventId"
        )

        if not original_id or original_id in seen_ids:
            raise ValueError(
                "Missing/duplicate event ID: " + relative
            )

        seen_ids.add(original_id)

        original_time = raw.get("eventTime")
        stamp = parse_utc(original_time)

        request = raw.get("requestParameters") or {}

        if not isinstance(request, dict):
            request = {}

        rows.append({
            "event_key": sid + ":" + original_id,
            "source_id": sid,
            "system": scope,
            "evidence_class": "SYNTHETIC_RECORD",
            "source_file": relative,
            "source_line": lineno,
            "source_sha256": current_hash,
            "raw_event_id": original_id,
            "raw_timestamp": original_time,
            "time_utc": stamp.isoformat().replace(
                "+00:00", "Z"
            ),
            "raw_source_system": field(
                raw, "sourceSystem"
            ),
            "dataset_type": dataset_type,
            "action": field(
                raw, "action", "eventName"
            ),
            "outcome": field(raw, "outcome"),
            "actor": actor_of(raw),
            "source_ip": field(
                raw,
                "sourceIPAddress",
                "sourceIP",
                "sourceIp"
            ),
            "destination_ip": field(
                raw, "destinationIP", "destinationIp"
            ),
            "request_id": field(
                raw, "requestID", "requestId"
            ),
            "session_id": field(raw, "sessionId"),
            "process_id": field(raw, "processId"),
            "pod_uid": field(raw, "podUID"),
            "container_id": field(raw, "containerID"),
            "target": field(
                raw, "targetResource", "target"
            ) or field(
                request, "targetResource"
            ),
            "rule": field(raw, "ruleName"),
        })

    if (
        len(rows) != expected_count
        or len(rows) != int(info["RecordCount"])
    ):
        raise ValueError(
            "Record count changed: " + relative
        )

    return rows


def associate(events):
    by_address = defaultdict(list)

    for event in events:
        for column, role in (
            ("source_ip", "source"),
            ("destination_ip", "destination")
        ):
            ip = valid_ip(event[column])

            if not ip:
                continue

            by_address[ip].append({
                "event_key": event["event_key"],
                "system": event["system"],
                "source_id": event["source_id"],
                "time_utc": event["time_utc"],
                "role": role,
            })

    overlaps = []
    temporal_pairs = []

    for ip in sorted(by_address):
        members = sorted(
            by_address[ip],
            key=lambda e: (
                e["time_utc"],
                e["event_key"],
                e["role"]
            )
        )

        systems = sorted({
            member["system"]
            for member in members
        })

        if len(systems) < 2:
            continue

        overlaps.append({
            "ip": ip,
            "systems": systems,
            "members": members,
            "relationship": "SHARED_LITERAL_IP_ONLY",
            "causation_established": False,
        })

        for a, b in itertools.combinations(members, 2):
            if a["system"] == b["system"]:
                continue

            first_time = parse_utc(a["time_utc"])
            second_time = parse_utc(b["time_utc"])

            delta = abs(
                (first_time - second_time).total_seconds()
            )

            if delta <= 300:
                temporal_pairs.append({
                    "ip": ip,
                    "first_event": a["event_key"],
                    "first_role": a["role"],
                    "second_event": b["event_key"],
                    "second_role": b["role"],
                    "delta_seconds": delta,
                    "relationship": (
                        "SHARED_IP_AND_WITHIN_5_MINUTES"
                    ),
                    "causation_established": False,
                })

    temporal_pairs.sort(
        key=lambda x: (
            x["ip"],
            x["delta_seconds"],
            x["first_event"],
            x["second_event"]
        )
    )

    return overlaps, temporal_pairs


def main():
    if len(sys.argv) != 2:
        raise ValueError(
            "Usage: python ticket011_correlate.py PROJECT_ROOT"
        )

    root = Path(sys.argv[1]).resolve()

    if root.name != (
        "ticket-011-cross-system-incident-investigation"
    ):
        raise ValueError("Incorrect Ticket 011 project root")

    outdir = root / "correlation-engine/sample-data"

    audit_path = outdir / "source-schema-audit-9a.json"

    audit = json.loads(
        audit_path.read_text(encoding="utf-8-sig")
    )

    if audit.get("Classification") != (
        "SYNTHETIC_SOURCE_SCHEMA_AUDIT"
    ):
        raise ValueError("Schema audit provenance mismatch")

    if (
        int(audit["SourceCount"]) != 7
        or int(audit["TotalRecordCount"]) != 42
    ):
        raise ValueError("Schema audit counts mismatch")

    expected = {
        row["SourceID"]: row
        for row in audit["Sources"]
    }

    if set(expected) != {s[0] for s in SOURCES}:
        raise ValueError("Schema source IDs mismatch")

    normalized_path = outdir / "normalized-events-9b.jsonl"
    association_path = outdir / "ip-associations-9b.json"
    report_path = outdir / "correlation-summary-9b.md"

    for path in (
        normalized_path,
        association_path,
        report_path
    ):
        if path.exists():
            raise ValueError(
                "Refusing overwrite: " + str(path)
            )

    print("=== NORMALIZE SEVEN SYNTHETIC SOURCES ===")

    all_events = []

    for spec in SOURCES:
        part = read_source(root, spec, expected)

        all_events.extend(part)

        print(
            "{}: {} validated".format(
                spec[0], len(part)
            )
        )

    if (
        len(all_events) != 42
        or len({
            e["event_key"] for e in all_events
        }) != 42
    ):
        raise ValueError(
            "Expected 42 distinct source-qualified events"
        )

    all_events.sort(
        key=lambda e: (
            e["time_utc"],
            e["event_key"]
        )
    )

    print("=== IDENTIFY CANDIDATE ASSOCIATIONS ===")

    overlaps, pairs = associate(all_events)

    output = {
        "ticket": "CYBEROPS-PDP-011",
        "classification": "SYNTHETIC_ONLY_ASSOCIATIONS",
        "source_event_count": len(all_events),
        "shared_ip_count": len(overlaps),
        "temporal_pair_count": len(pairs),
        "correlation_window_seconds": 300,
        "causation_established": False,
        "shared_ip_groups": overlaps,
        "temporal_pairs": pairs,
        "limitations": [
            "A shared IP is not common-actor attribution.",
            "Source and destination roles remain distinct.",
            "Time proximity does not establish causation.",
            "Clock synchronization is not independently verified.",
            "Kubernetes ServiceAccount tokens are not AWS keys.",
            "An allowed connection does not prove exfiltration.",
            "Actual Minikube tests are excluded from this analysis.",
        ],
    }

    lines = [
        json.dumps(
            event,
            sort_keys=True,
            separators=(",", ":")
        )
        for event in all_events
    ]

    heading = [
        "# Ticket 011 - Initial Synthetic Cross-System Correlation",
        "",
        "**Classification: SYNTHETIC LABORATORY DATA ONLY**",
        "",
        "Original files were not modified. Source SHA256 hashes were checked.",
        "",
        "- Source datasets: 7",
        "- Normalized synthetic events: 42",
        "- Cross-system shared-IP groups: {}".format(
            len(overlaps)
        ),
        "- Cross-system five-minute IP pairs: {}".format(
            len(pairs)
        ),
        "- Cross-system causation: NOT ESTABLISHED",
        "",
        "## Shared-address candidate groups",
        "",
    ]

    for group in overlaps:
        heading.append(
            "- `{}`: {} ({} source/destination occurrences)".format(
                group["ip"],
                ", ".join(group["systems"]),
                len(group["members"])
            )
        )

    if not overlaps:
        heading.append(
            "No cross-system shared-IP groups found."
        )

    heading.extend([
        "",
        "## Evidence interpretation",
        "",
        "Each normalized record retains its original event ID,",
        "timestamp, source file, source line number, and SHA256.",
        "Source and destination IP directions are preserved.",
        "",
        "Shared IPs and five-minute pairs are candidate associations.",
        "They do not prove shared identity, compromise, or causation.",
        "Independent attribution and network mapping are required.",
        "",
        "## Next validation",
        "",
        "Test schema variations, corrupted source hashes,",
        "invalid timestamps, missing event IDs, and false matches.",
    ])

    print("=== SAVE CORRELATION OUTPUTS ===")

    with normalized_path.open(
        "x", encoding="utf-8", newline="\n"
    ) as stream:
        stream.write("\n".join(lines) + "\n")

    with association_path.open(
        "x", encoding="utf-8", newline="\n"
    ) as stream:
        json.dump(output, stream, indent=2)
        stream.write("\n")

    with report_path.open(
        "x", encoding="utf-8", newline="\n"
    ) as stream:
        stream.write("\n".join(heading) + "\n")

    validated = [
        json.loads(line)
        for line in normalized_path.read_text(
            encoding="utf-8"
        ).splitlines()
    ]

    saved = json.loads(
        association_path.read_text(encoding="utf-8")
    )

    if (
        len(validated) != 42
        or saved["causation_established"] is not False
    ):
        raise ValueError("Saved output verification failed")

    print("Normalized synthetic events: 42")
    print(
        "Cross-system shared-IP groups: {}".format(
            len(overlaps)
        )
    )
    print(
        "Temporal shared-IP pairs: {}".format(
            len(pairs)
        )
    )
    print("Cross-system causation: NOT ESTABLISHED")
    print("STEP 9B PYTHON: PASS")


if __name__ == "__main__":
    try:
        main()
    except (
        OSError,
        KeyError,
        ValueError,
        TypeError,
        json.JSONDecodeError
    ) as error:
        print(
            "STEP 9B PYTHON: NOT PASSED - {}".format(error),
            file=sys.stderr
        )
        sys.exit(1)