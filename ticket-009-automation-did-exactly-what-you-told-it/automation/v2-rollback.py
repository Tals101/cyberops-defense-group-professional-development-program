import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SNAPSHOT_FILE = BASE_DIR / "evidence" / "v2-prechange-snapshot.json"
TARGET_FILE = BASE_DIR / "simulation" / "v2-rollback-test-working.json"
LOG_FILE = BASE_DIR / "evidence" / "v2-rollback.log"


def timestamp():
    return datetime.now(timezone.utc).isoformat()


if not SNAPSHOT_FILE.exists():
    raise SystemExit("FAIL: rollback snapshot is missing.")

if not TARGET_FILE.exists():
    raise SystemExit("FAIL: rollback target is missing.")


with SNAPSHOT_FILE.open("r", encoding="utf-8-sig") as f:
    snapshot = json.load(f)

with TARGET_FILE.open("r", encoding="utf-8-sig") as f:
    before = json.load(f)


before_map = {
    account["username"]: account
    for account in before["accounts"]
}

snapshot_map = {
    account["username"]: account
    for account in snapshot["accounts"]
}


with LOG_FILE.open("w", encoding="utf-8") as log:
    log.write(f"{timestamp()} V2 rollback started\n")

    changed_accounts = []

    for username, snapshot_account in snapshot_map.items():
        current_account = before_map.get(username)

        if current_account is None:
            continue

        if current_account != snapshot_account:
            changed_accounts.append(username)

            log.write(
                f"{timestamp()} restoring username={username} "
                f"enabled_before={current_account.get('enabled')} "
                f"enabled_restore={snapshot_account.get('enabled')}\n"
            )

    shutil.copyfile(SNAPSHOT_FILE, TARGET_FILE)

    log.write(
        f"{timestamp()} rollback completed "
        f"accounts_restored={len(changed_accounts)}\n"
    )


print("V2 rollback complete.")
print(f"Accounts restored: {len(changed_accounts)}")
print(f"Target: {TARGET_FILE}")
print(f"Log: {LOG_FILE}")
