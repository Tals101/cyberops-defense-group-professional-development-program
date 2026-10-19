import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

SNAPSHOT_FILE = BASE / "evidence" / "v3-f07-prechange-snapshot.json"
WORKING_FILE = BASE / "simulation" / "v3-f07-rollback-working.json"
TEMP_RESTORE_FILE = BASE / "simulation" / "v3-f07-rollback-restore.tmp"
LOG_FILE = BASE / "evidence" / "v3-f07-rollback-failure-log.csv"

INJECT_ROLLBACK_FAILURE = True


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def write_log(record):
    exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=record.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(record)


def main():
    snapshot_hash = sha256(SNAPSHOT_FILE)
    working_before_hash = sha256(WORKING_FILE)

    try:
        shutil.copy2(SNAPSHOT_FILE, TEMP_RESTORE_FILE)

        if INJECT_ROLLBACK_FAILURE:
            raise OSError("Simulated rollback failure before authoritative state replacement.")

        TEMP_RESTORE_FILE.replace(WORKING_FILE)

    except OSError as exc:
        if TEMP_RESTORE_FILE.exists():
            TEMP_RESTORE_FILE.unlink()

        working_after_hash = sha256(WORKING_FILE)
        restored = working_after_hash == snapshot_hash

        write_log({
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "snapshot_hash": snapshot_hash,
            "working_before_hash": working_before_hash,
            "working_after_hash": working_after_hash,
            "rollback_result": "FAILED_ROLLBACK",
            "restored": restored,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "required_operator_action": "ESCALATE_MANUAL_RECOVERY",
        })

        print("FAIL: rollback did not complete.")
        print(f"Snapshot hash:       {snapshot_hash}")
        print(f"Working before hash: {working_before_hash}")
        print(f"Working after hash:  {working_after_hash}")
        print(f"Restored:            {restored}")
        print(f"Error:               {type(exc).__name__}: {exc}")
        print("Required action:      ESCALATE_MANUAL_RECOVERY")
        raise SystemExit(1)

    print("Unexpected rollback success.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
