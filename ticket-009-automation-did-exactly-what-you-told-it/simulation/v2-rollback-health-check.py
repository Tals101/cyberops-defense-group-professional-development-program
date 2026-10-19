import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATE_FILE = BASE_DIR / "simulation" / "v2-rollback-test-working.json"
LOG_FILE = BASE_DIR / "evidence" / "v2-rollback-health.log"

DEPENDENCY = "Finance LedgerBridge"


def timestamp():
    return datetime.now(timezone.utc).isoformat()


with STATE_FILE.open("r", encoding="utf-8-sig") as f:
    data = json.load(f)

dependent_accounts = [
    account
    for account in data["accounts"]
    if DEPENDENCY in account.get("service_dependencies", [])
]

with LOG_FILE.open("w", encoding="utf-8") as log:
    log.write(f"{timestamp()} Rollback recovery validation started\n")
    log.write(f"{timestamp()} dependency={DEPENDENCY}\n")

    if not dependent_accounts:
        log.write(f"{timestamp()} APPLICATION_STATUS=FAILED reason=dependency_not_found\n")
        print("FAIL: Finance dependency not found.")
        raise SystemExit(2)

    failed = False

    for account in dependent_accounts:
        username = account["username"]
        enabled = account["enabled"]

        log.write(
            f"{timestamp()} dependency_account={username} enabled={enabled}\n"
        )

        if not enabled:
            failed = True

    if failed:
        log.write(f"{timestamp()} APPLICATION_STATUS=FAILED\n")
        print("FAIL: Finance dependency remains unavailable after rollback.")
        raise SystemExit(2)

    log.write(f"{timestamp()} APPLICATION_STATUS=HEALTHY\n")
    print("PASS: Finance dependency recovered after rollback.")
