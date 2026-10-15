import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

WORKING_FILE = BASE / "simulation" / "v3-f06-failed-remediation-working.json"
TEMP_FILE = BASE / "simulation" / "v3-f06-failed-remediation-working.tmp"
LOG_FILE = BASE / "evidence" / "v3-f06-remediation-failure-log.csv"

TARGET_USERNAME = "nora.hayes"
APPROVAL_STATUS = "APPROVED"
INJECT_WRITE_FAILURE = True


def log_record(record):
    exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=record.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(record)


def main():
    if APPROVAL_STATUS != "APPROVED":
        raise SystemExit("FAIL: explicit approval is required.")

    with WORKING_FILE.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)

    target = next(
        (a for a in data["accounts"] if a.get("username") == TARGET_USERNAME),
        None
    )

    if target is None:
        raise SystemExit(f"FAIL: identity not found: {TARGET_USERNAME}")

    before = bool(target.get("enabled"))

    if before is False:
        print("NO_ACTION: target already disabled.")
        raise SystemExit(0)

    target["enabled"] = False

    try:
        with TEMP_FILE.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")

        if INJECT_WRITE_FAILURE:
            raise OSError("Simulated remediation write failure before atomic replace.")

        os.replace(TEMP_FILE, WORKING_FILE)

    except OSError as exc:
        if TEMP_FILE.exists():
            TEMP_FILE.unlink()

        with WORKING_FILE.open("r", encoding="utf-8-sig") as handle:
            persisted = json.load(handle)

        persisted_target = next(
            a for a in persisted["accounts"]
            if a.get("username") == TARGET_USERNAME
        )

        after = bool(persisted_target.get("enabled"))

        log_record({
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "username": TARGET_USERNAME,
            "approval_status": APPROVAL_STATUS,
            "enabled_before": before,
            "attempted_action": "DISABLE",
            "result": "FAILED_REMEDIATION",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "enabled_after": after,
            "state_change_committed": False,
        })

        print("FAIL: remediation could not be committed.")
        print(f"Username:       {TARGET_USERNAME}")
        print(f"Enabled before: {before}")
        print(f"Enabled after:  {after}")
        print(f"Error:          {type(exc).__name__}: {exc}")
        print("State change committed: False")
        raise SystemExit(1)

    print("Unexpected success.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
