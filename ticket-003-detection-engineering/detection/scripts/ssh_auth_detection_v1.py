#!/usr/bin/env python3

import re
import sys
from datetime import datetime
from collections import defaultdict

LOG_FILE = sys.argv[1] if len(sys.argv) > 1 else "/var/log/auth.log"

THRESHOLD = 5
WINDOW_SECONDS = 120

failed_pattern = re.compile(
    r"Failed password for (?P<username>\S+) "
    r"from (?P<source_ip>\S+) port (?P<port>\d+)"
)

repeated_pattern = re.compile(
    r"message repeated (?P<count>\d+) times: "
    r"\[ Failed password for (?P<username>\S+) "
    r"from (?P<source_ip>\S+) port (?P<port>\d+)"
)

events = []

with open(LOG_FILE, "r") as log:
    for line in log:

        timestamp_text = line.split()[0]

        try:
            timestamp = datetime.fromisoformat(timestamp_text)
        except ValueError:
            continue

        repeated_match = repeated_pattern.search(line)

        if repeated_match:
            events.append(
                {
                    "timestamp": timestamp,
                    "username": repeated_match.group("username"),
                    "source_ip": repeated_match.group("source_ip"),
                    "count": int(repeated_match.group("count")),
                }
            )
            continue

        failed_match = failed_pattern.search(line)

        if failed_match:
            events.append(
                {
                    "timestamp": timestamp,
                    "username": failed_match.group("username"),
                    "source_ip": failed_match.group("source_ip"),
                    "count": 1,
                }
            )

grouped_events = defaultdict(list)

for event in events:
    key = (event["username"], event["source_ip"])
    grouped_events[key].append(event)

for (username, source_ip), group in grouped_events.items():

    for start_index in range(len(group)):

        start_time = group[start_index]["timestamp"]
        failure_count = 0
        end_time = start_time

        for event in group[start_index:]:

            elapsed = (
                event["timestamp"] - start_time
            ).total_seconds()

            if elapsed > WINDOW_SECONDS:
                break

            failure_count += event["count"]
            end_time = event["timestamp"]

        if failure_count >= THRESHOLD:

            duration = (
                end_time - start_time
            ).total_seconds()

            print("=== SUSPICIOUS SSH AUTHENTICATION DETECTED ===")
            print(f"User: {username}")
            print(f"Source IP: {source_ip}")
            print(f"Failed attempts: {failure_count}")
            print(f"Window: {duration:.0f} seconds")
            print(f"Threshold: {THRESHOLD} failures in {WINDOW_SECONDS} seconds")
            print(f"First event: {start_time.isoformat()}")
            print(f"Last event: {end_time.isoformat()}")

            break
