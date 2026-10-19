import hashlib
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

SNAPSHOT = BASE / "evidence" / "v3-rollback-prechange-snapshot.json"
WORKING = BASE / "simulation" / "v3-rollback-working.json"
LOG = BASE / "evidence" / "v3-rollback-test.log"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main():
    started_utc = datetime.now(timezone.utc).isoformat()

    if not SNAPSHOT.exists():
        print("FAIL: rollback snapshot is missing.")
        raise SystemExit(1)

    if not WORKING.exists():
        print("FAIL: rollback working file is missing.")
        raise SystemExit(1)

    snapshot_hash_before = sha256(SNAPSHOT)
    working_hash_before = sha256(WORKING)

    start = time.perf_counter()

    shutil.copyfile(SNAPSHOT, WORKING)

    elapsed_seconds = time.perf_counter() - start

    working_hash_after = sha256(WORKING)

    restored = working_hash_after == snapshot_hash_before

    log_lines = [
        f"started_utc={started_utc}",
        "test=V3_CONTROLLED_ROLLBACK",
        "identity=payroll.emergency",
        f"snapshot_hash={snapshot_hash_before}",
        f"working_hash_before={working_hash_before}",
        "rollback_trigger=incorrect_test_disable_detected",
        "rollback_action=restore_prechange_snapshot",
        f"working_hash_after={working_hash_after}",
        f"restored_exact_state={restored}",
        f"elapsed_recovery_seconds={elapsed_seconds:.6f}",
    ]

    LOG.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print(f"Snapshot hash:       {snapshot_hash_before}")
    print(f"Working before:      {working_hash_before}")
    print(f"Working after:       {working_hash_after}")
    print(f"Exact state restored: {restored}")
    print(f"Elapsed seconds:      {elapsed_seconds:.6f}")
    print(f"Log: {LOG}")

    if not restored:
        print("FAIL: rollback did not restore the exact pre-change state.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
