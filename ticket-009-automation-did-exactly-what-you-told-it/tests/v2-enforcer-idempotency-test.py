import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATE_FILE = BASE_DIR / "simulation" / "v2-idempotency-working.json"
CONFIG_FILE = BASE_DIR / "automation" / "v2-config.json"
DECISIONS_FILE = BASE_DIR / "evidence" / "v2-dry-run-decisions.csv"
SNAPSHOT_FILE = BASE_DIR / "evidence" / "v2-prechange-snapshot.json"

OUTPUT_FILE = BASE_DIR / "simulation" / "v2-idempotency-after.json"
ENFORCEMENT_LOG = BASE_DIR / "evidence" / "v2-idempotency.log"
RESULTS_FILE = BASE_DIR / "evidence" / "v2-idempotency-results.csv"


def timestamp():
    return datetime.now(timezone.utc).isoformat()


if not SNAPSHOT_FILE.exists():
    raise SystemExit("FAIL: required pre-change snapshot is missing.")

with CONFIG_FILE.open("r", encoding="utf-8-sig") as f:
    config = json.load(f)

with STATE_FILE.open("r", encoding="utf-8-sig") as f:
    state = json.load(f)

with DECISIONS_FILE.open("r", encoding="utf-8-sig") as f:
    decisions = list(csv.DictReader(f))

max_changes = int(config["max_state_changes_per_run"])

decision_map = {
    row["username"]: row
    for row in decisions
}

changes_made = 0
results = []

with ENFORCEMENT_LOG.open("w", encoding="utf-8") as log:
    log.write(f"{timestamp()} V2 enforcement started\n")
    log.write(f"{timestamp()} max_state_changes_per_run={max_changes}\n")

    for account in state["accounts"]:
        username = account["username"]
        decision = decision_map.get(username)

        if decision is None:
            results.append({
                "username": username,
                "authority": "UNKNOWN",
                "recommendation": "UNKNOWN",
                "action": "NO_ACTION",
                "result": "NO_DECISION_RECORD"
            })
            log.write(
                f"{timestamp()} username={username} "
                f"result=NO_DECISION_RECORD\n"
            )
            continue

        authority = decision["authority"]
        recommendation = decision["recommendation"]

        action = "NO_ACTION"
        result = "NOT_ELIGIBLE"

        if authority == "AUTO_REMEDIATE" and recommendation == "DISABLE":

            if changes_made >= max_changes:
                action = "STAGE_ONLY"
                result = "RUN_LIMIT_REACHED"

            elif not account.get("enabled", False):
                action = "NO_ACTION"
                result = "ALREADY_DISABLED"

            else:
                before_enabled = account["enabled"]
                account["enabled"] = False
                changes_made += 1

                action = "DISABLE"
                result = "SUCCESS"

                log.write(
                    f"{timestamp()} username={username} "
                    f"before_enabled={before_enabled} "
                    f"after_enabled={account['enabled']} "
                    f"action=DISABLE result=SUCCESS "
                    f"change_number={changes_made}\n"
                )

        elif recommendation in ("KEEP_ENABLED", "NO_ACTION"):
            action = "NO_ACTION"
            result = "RECOMMENDATION_NO_CHANGE"

        elif authority == "REQUIRE_APPROVAL":
            action = "STAGE_ONLY"
            result = "APPROVAL_REQUIRED"

        elif authority == "DO_NOT_AUTOMATE":
            action = "NO_ACTION"
            result = "AUTOMATION_PROHIBITED"

        results.append({
            "username": username,
            "authority": authority,
            "recommendation": recommendation,
            "action": action,
            "result": result
        })

    log.write(
        f"{timestamp()} V2 enforcement completed "
        f"changes_made={changes_made}\n"
    )


with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)


fieldnames = [
    "username",
    "authority",
    "recommendation",
    "action",
    "result"
]

with RESULTS_FILE.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)


print("V2 enforcement complete.")
print(f"Changes made: {changes_made}")
print(f"Maximum allowed: {max_changes}")
print(f"Output: {OUTPUT_FILE}")
print(f"Results: {RESULTS_FILE}")
print(f"Log: {ENFORCEMENT_LOG}")


