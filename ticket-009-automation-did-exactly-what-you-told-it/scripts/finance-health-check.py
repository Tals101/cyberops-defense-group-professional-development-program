import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATE_FILE = BASE_DIR / "simulation" / "identities-v1-after.json"
LOG_FILE = BASE_DIR / "evidence" / "finance-application.log"

DEPENDENCY = "Finance LedgerBridge"


def timestamp():
    return datetime.now(timezone.utc).isoformat()


with STATE_FILE.open("r", encoding="utf-8-sig") as f:
    data = json.load(f)

dependent_accounts = []

for account in data["accounts"]:
    dependencies = account.get("service_dependencies", [])

    if DEPENDENCY in dependencies:
        dependent_accounts.append(account)

with LOG_FILE.open("w", encoding="utf-8") as log:
    log.write(f"{timestamp()} Simulated Finance application health check started\n")
    log.write(f"{timestamp()} Required dependency={DEPENDENCY}\n")

    if not dependent_accounts:
        message = "FAIL: No identity providing the required Finance dependency was found."
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
                f"dependency_account={username} "
                f"reason=identity_disabled\n"
            )

    if failed:
        message = (
            "FAIL: Finance LedgerBridge cannot authenticate because "
            "a required identity is disabled."
        )
        log.write(f"{timestamp()} APPLICATION_STATUS=FAILED\n")
        print(message)
        raise SystemExit(2)

    message = "PASS: Finance LedgerBridge authentication dependency is available."
    log.write(f"{timestamp()} APPLICATION_STATUS=HEALTHY\n")
    print(message)
