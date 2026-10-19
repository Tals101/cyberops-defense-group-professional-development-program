import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

WORKING_FILE = BASE / "simulation" / "v3-f05-interrupted-working.json"
LOG_FILE = BASE / "evidence" / "v3-f05-execution-log.csv"

TARGETS = ["nora.hayes", "kevin.brooks"]
SIMULATE_INTERRUPT_AFTER = 1


def log_record(record):
    exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=record.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(record)


def main():
    with WORKING_FILE.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)

    completed_changes = 0

    for username in TARGETS:
        account = next(
            (a for a in data["accounts"] if a.get("username") == username),
            None
        )

        if account is None:
            raise SystemExit(f"FAIL: identity not found: {username}")

        before = bool(account.get("enabled"))

        if before is False:
            action = "NO_ACTION"
            result = "ALREADY_DISABLED"
        else:
            account["enabled"] = False
            action = "DISABLE"
            result = "SUCCESS"

            with WORKING_FILE.open("w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2)
                handle.write("\n")

            completed_changes += 1

        after = bool(account.get("enabled"))

        log_record({
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "username": username,
            "enabled_before": before,
            "action": action,
            "result": result,
            "enabled_after": after,
        })

        print(
            f"{username}: before={before} "
            f"action={action} result={result} after={after}"
        )

        if completed_changes >= SIMULATE_INTERRUPT_AFTER:
            print("SIMULATED INTERRUPTION: execution stopped after first state change.")
            raise SystemExit(2)

    print("Batch completed safely.")


if __name__ == "__main__":
    main()
