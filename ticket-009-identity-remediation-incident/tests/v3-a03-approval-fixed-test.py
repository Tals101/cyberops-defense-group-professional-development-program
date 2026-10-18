import csv
import json
import sqlite3
import os
import base64
import hashlib
import hmac
from datetime import timedelta
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

WORKING_FILE = BASE / "simulation" / "v3-a03-fixed-working.json"
APPROVAL_FILE = BASE / "simulation" / "v3-a03-valid-approval.json"
LOG_FILE = BASE / "evidence" / "v3-a03-approval-fixed-log.csv"

LEDGER_FILE = BASE / "evidence" / "v3-a03-approval-consumption.sqlite"

TARGET_USERNAME = "nora.hayes"
DESIRED_ENABLED_STATE = False



def verify_approval(approval):
    required = [
        "approval_id",
        "target_username",
        "requested_action",
        "approval_status",
        "approved_by",
        "issued_at_utc",
        "expires_at_utc",
        "signature_hmac_sha256",
    ]

    for field in required:
        if not isinstance(approval.get(field), str) or not approval[field].strip():
            raise ValueError(f"Missing or invalid approval field: {field}")

    encoded_key = os.environ.get("A03_APPROVAL_HMAC_KEY")
    if not encoded_key:
        raise ValueError("Approval verification key unavailable")

    key = base64.b64decode(encoded_key, validate=True)

    signed_fields = {
        k: v for k, v in approval.items()
        if k != "signature_hmac_sha256"
    }

    payload = json.dumps(
        signed_fields,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    expected = hmac.new(key, payload, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected, approval["signature_hmac_sha256"]):
        raise ValueError("Approval signature verification failed")

    if approval["approval_status"] != "APPROVED":
        raise ValueError("Approval status is not APPROVED")

    if approval["approved_by"] != "soc.manager":
        raise ValueError("Unauthorized approver")

    if approval["target_username"] != TARGET_USERNAME:
        raise ValueError("Approval target mismatch")

    expected_action = (
        "ENABLE" if DESIRED_ENABLED_STATE else "DISABLE"
    )

    if approval["requested_action"] != expected_action:
        raise ValueError("Approval action mismatch")

    issued = datetime.fromisoformat(
        approval["issued_at_utc"].replace("Z", "+00:00")
    )
    expires = datetime.fromisoformat(
        approval["expires_at_utc"].replace("Z", "+00:00")
    )

    if issued.tzinfo is None or expires.tzinfo is None:
        raise ValueError("Approval timestamps must include timezone")

    now = datetime.now(timezone.utc)

    if issued > now:
        raise ValueError("Approval issued in the future")

    if expires <= now:
        raise ValueError("Approval expired")

    if expires <= issued or expires - issued > timedelta(minutes=30):
        raise ValueError("Invalid approval validity window")

    return approval["approval_id"]



def consume_approval(approval):
    """Reserve the approval ID permanently before remediation."""
    try:
        with sqlite3.connect(LEDGER_FILE, timeout=5) as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("""
                CREATE TABLE IF NOT EXISTS consumed_approvals (
                    approval_id TEXT PRIMARY KEY,
                    target_username TEXT NOT NULL,
                    requested_action TEXT NOT NULL,
                    consumed_at_utc TEXT NOT NULL
                )
            """)

            db.execute(
                """
                INSERT INTO consumed_approvals
                (approval_id, target_username, requested_action, consumed_at_utc)
                VALUES (?, ?, ?, ?)
                """,
                (
                    approval["approval_id"],
                    approval["target_username"],
                    approval["requested_action"],
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            db.commit()

    except sqlite3.IntegrityError:
        raise ValueError("Approval replay blocked: ID already consumed")
    except sqlite3.Error as exc:
        raise ValueError(f"Approval ledger unavailable: {exc}")


def main():
    with APPROVAL_FILE.open("r", encoding="utf-8-sig") as handle:
        approval = json.load(handle)

    try:
        approval_id = verify_approval(approval)
    except (ValueError, KeyError, TypeError) as exc:
        print(f"BLOCKED: {exc}")
        raise SystemExit(1)

    print(f"Verified approval: {approval_id}")

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

    try:
        consume_approval(approval)
    except ValueError as exc:
        print(f"BLOCKED: {exc}")
        raise SystemExit(1)

    print(f"Approval reserved: {approval_id}")

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
        "approval_id": approval.get("approval_id"),
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
    print(f"Approval ref:    {approval.get('approval_id')}")
    print(f"Approval status: {approval.get('approval_status')}")
    print(f"Enabled before:  {before}")
    print(f"Action:          {action}")
    print(f"Result:          {result}")
    print(f"Enabled after:   {after}")
    print(f"Execution log:   {LOG_FILE}")


if __name__ == "__main__":
    main()


