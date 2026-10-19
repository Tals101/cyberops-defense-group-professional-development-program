import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATE_FILE = BASE_DIR / "simulation" / "identities-v2-after.json"
LOG_FILE = BASE_DIR / "evidence" / "v2-postchange-health.log"

FINANCE_DEPENDENCY = "Finance LedgerBridge"


def timestamp():
    return datetime.now(timezone.utc).isoformat()


with STATE_FILE.open("r", encoding="utf-8-sig") as f:
    data = json.load(f)

dependent_accounts = [
    account
    for account in data["accounts"]
    if FINANCE_DEPENDENCY in account.get("service_dependencies", [])
]

with LOG_FILE.open("w", encoding="utf-8") as log:
    log.write(f"{timestamp()} V2 post-change health validation started\n")
    log.write(f"{timestamp()} dependency={FINANCE_DEPENDENCY}\n")

    if not dependent_accounts:
        message = "FAIL: Finance dependency account not found."
        log.write(f"{timestamp()} {message}\n")
        print(message)
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
            log.write(
                f"{timestamp()} AUTHENTICATION_FAILURE "
                f"dependency_account={username} reason=identity_disabled\n"
            )

    if failed:
        log.write(f"{timestamp()} APPLICATION_STATUS=FAILED\n")
        print("FAIL: Finance LedgerBridge dependency is unavailable.")
        raise SystemExit(2)

    log.write(f"{timestamp()} APPLICATION_STATUS=HEALTHY\n")
    print("PASS: Finance LedgerBridge dependency remains available.")
