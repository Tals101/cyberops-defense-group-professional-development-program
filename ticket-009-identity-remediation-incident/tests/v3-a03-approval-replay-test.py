import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

WORKING_FILE = BASE / "simulation" / "v3-a03-approval-replay-working.json"
APPROVAL_FILE = BASE / "simulation" / "v3-a03-generic-approval.json"
LOG_FILE = BASE / "evidence" / "v3-a03-approval-replay-log.csv"

TARGET_USERNAME = "payroll.emergency"
DESIRED_ENABLED_STATE = False


def main():
    with APPROVAL_FILE.open("r", encoding="utf-8-sig") as handle:
        approval = json.load(handle)

    if approval.get("approval_status") != "APPROVED":
        print("FAIL: explicit approval is required.")
        raise SystemExit(1)

    with WORKING_FILE.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)

    target = None

    for account in data["accounts"]:
        if account.get("username") == TARGET_USERNAME:
            target = account
            break

    if target is None:
        print(f"FAIL: target identity not found: {TARGET_USERNAME}")
        raise SystemExit(1)

    before = bool(target.get("enabled"))

    if before == DESIRED_ENABLED_STATE:
        action = "NO_ACTION"
        result = "ALREADY_DISABLED"
    else:
        target["enabled"] = DESIRED_ENABLED_STATE
        action = "DISABLE"
        result = "SUCCESS"

        with WORKING_FILE.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")

    after = bool(target.get("enabled"))

    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "username": TARGET_USERNAME,
        "approval_reference": approval.get("approval_reference"),
        "approval_status": approval.get("approval_status"),
        "desired_enabled_state": DESIRED_ENABLED_STATE,
        "enabled_before": before,
        "action": action,
        "result": result,
        "enabled_after": after,
    }

    file_exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=record.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(record)

    print(f"Username:        {TARGET_USERNAME}")
    print(f"Approval ref:    {approval.get('approval_reference')}")
    print(f"Approval status: {approval.get('approval_status')}")
    print(f"Enabled before:  {before}")
    print(f"Action:          {action}")
    print(f"Result:          {result}")
    print(f"Enabled after:   {after}")
    print(f"Execution log:   {LOG_FILE}")


if __name__ == "__main__":
    main()
