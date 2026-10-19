import csv
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "simulation" / "identities-original.json"
OUTPUT_FILE = BASE_DIR / "simulation" / "identities-v1-after.json"
DECISIONS_FILE = BASE_DIR / "evidence" / "v1-decisions.csv"
LOG_FILE = BASE_DIR / "evidence" / "v1-remediation.log"

STALE_INTERACTIVE_DAYS = 90


def timestamp():
    return datetime.now(timezone.utc).isoformat()


with INPUT_FILE.open("r", encoding="utf-8-sig") as f:
    original = json.load(f)

working = deepcopy(original)

decision_rows = []

with LOG_FILE.open("w", encoding="utf-8") as log:
    log.write(f"{timestamp()} V1 remediation started\n")
    log.write(
        f"{timestamp()} Rule: disable enabled accounts with "
        f"days_since_interactive_login >= {STALE_INTERACTIVE_DAYS}\n"
    )

    for account in working["accounts"]:
        username = account["username"]
        before_enabled = account["enabled"]
        interactive_age = account.get("days_since_interactive_login")

        decision = "KEEP_ENABLED"
        action_result = "NO_CHANGE"
        reason = ""

        if not before_enabled:
            decision = "NO_ACTION"
            reason = "Account already disabled."

        elif (
            isinstance(interactive_age, (int, float))
            and interactive_age >= STALE_INTERACTIVE_DAYS
        ):
            decision = "DISABLE"
            account["enabled"] = False
            action_result = "SUCCESS"
            reason = (
                f"Interactive login age {interactive_age} days "
                f"meets or exceeds {STALE_INTERACTIVE_DAYS}-day threshold."
            )

        elif interactive_age is None:
            decision = "KEEP_ENABLED"
            reason = "Interactive login age unavailable; V1 threshold not matched."

        else:
            reason = (
                f"Interactive login age {interactive_age} days "
                f"is below {STALE_INTERACTIVE_DAYS}-day threshold."
            )

        after_enabled = account["enabled"]

        decision_rows.append(
            {
                "timestamp_utc": timestamp(),
                "username": username,
                "identity_type": account.get("identity_type"),
                "days_since_interactive_login": interactive_age,
                "decision": decision,
                "action_result": action_result,
                "before_enabled": before_enabled,
                "after_enabled": after_enabled,
                "reason": reason,
            }
        )

        log.write(
            f"{timestamp()} username={username} "
            f"interactive_age={interactive_age} "
            f"decision={decision} "
            f"result={action_result} "
            f"before_enabled={before_enabled} "
            f"after_enabled={after_enabled}\n"
        )

    log.write(f"{timestamp()} V1 remediation completed\n")


with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(working, f, indent=2)


fieldnames = [
    "timestamp_utc",
    "username",
    "identity_type",
    "days_since_interactive_login",
    "decision",
    "action_result",
    "before_enabled",
    "after_enabled",
    "reason",
]

with DECISIONS_FILE.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(decision_rows)


print("V1 remediation complete.")
print(f"Input:     {INPUT_FILE}")
print(f"State:     {OUTPUT_FILE}")
print(f"Decisions: {DECISIONS_FILE}")
print(f"Log:       {LOG_FILE}")
