import csv
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

WORKING_FILE = BASE / "simulation" / "v3-f08-approval-timeout-working.json"
LOG_FILE = BASE / "evidence" / "v3-f08-approval-timeout-log.csv"

TARGET_USERNAME = "payroll.emergency"
APPROVAL_STATUS = "PENDING"
APPROVAL_REQUESTED_AT = datetime.now(timezone.utc) - timedelta(hours=3)
APPROVAL_TIMEOUT_MINUTES = 60


def log_record(record):
    exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=record.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(record)


def main():
    now = datetime.now(timezone.utc)

    with WORKING_FILE.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)

    target = next(
        (a for a in data["accounts"] if a.get("username") == TARGET_USERNAME),
        None
    )

    if target is None:
        raise SystemExit(f"FAIL: identity not found: {TARGET_USERNAME}")

    before = bool(target.get("enabled"))

    approval_age_minutes = int(
        (now - APPROVAL_REQUESTED_AT).total_seconds() / 60
    )

    timed_out = (
        APPROVAL_STATUS == "PENDING"
        and approval_age_minutes > APPROVAL_TIMEOUT_MINUTES
    )

    if timed_out:
        after = before

        log_record({
            "timestamp_utc": now.isoformat(),
            "username": TARGET_USERNAME,
            "approval_status": APPROVAL_STATUS,
            "approval_age_minutes": approval_age_minutes,
            "approval_timeout_minutes": APPROVAL_TIMEOUT_MINUTES,
            "attempted_action": "DISABLE",
            "result": "APPROVAL_TIMEOUT",
            "enabled_before": before,
            "enabled_after": after,
            "state_change_committed": False,
            "required_operator_action": "ESCALATE_APPROVAL_TIMEOUT",
        })

        print("BLOCKED: approval window expired.")
        print(f"Username:               {TARGET_USERNAME}")
        print(f"Approval status:        {APPROVAL_STATUS}")
        print(f"Approval age minutes:   {approval_age_minutes}")
        print(f"Approval timeout:       {APPROVAL_TIMEOUT_MINUTES}")
        print(f"Enabled before:         {before}")
        print(f"Enabled after:          {after}")
        print("State change committed: False")
        print("Required action:        ESCALATE_APPROVAL_TIMEOUT")
        raise SystemExit(1)

    print("Unexpected condition: timeout control did not trigger.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
