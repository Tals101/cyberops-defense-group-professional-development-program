import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "simulation" / "v2-malformed-input.json"
CONFIG_FILE = BASE_DIR / "automation" / "v2-config.json"
DECISIONS_FILE = BASE_DIR / "evidence" / "v2-malformed-input-decisions.csv"
LOG_FILE = BASE_DIR / "evidence" / "v2-malformed-input.log"


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def classify_confidence(account):
    if account.get("evidence_completeness") == "incomplete":
        return "INSUFFICIENT"

    if account.get("evidence_completeness") == "conflicting":
        return "LOW"

    if account.get("data_freshness") not in ("current",):
        return "LOW"

    return "HIGH"


def classify_authority(account, confidence):
    identity_type = account.get("identity_type")
    privilege = account.get("privilege")
    dependencies = account.get("service_dependencies", [])

    if identity_type in (None, "unknown"):
        return "DO_NOT_AUTOMATE"

    if confidence in ("LOW", "INSUFFICIENT"):
        return "REQUIRE_APPROVAL"

    if identity_type in ("service_account", "privileged"):
        return "REQUIRE_APPROVAL"

    if privilege not in ("standard",):
        return "REQUIRE_APPROVAL"

    if dependencies:
        return "REQUIRE_APPROVAL"

    return "AUTO_REMEDIATE"


def evaluate(account, stale_days):
    username = account["username"]
    identity_type = account.get("identity_type")
    workforce_status = account.get("workforce_status")
    interactive_age = account.get("days_since_interactive_login")
    noninteractive_age = account.get("days_since_noninteractive_auth")
    lifecycle_state = account.get("lifecycle_state")

    confidence = classify_confidence(account)
    authority = classify_authority(account, confidence)

    recommendation = "NO_ACTION"
    reason = "No remediation condition matched."

    if identity_type in ("employee", "contractor"):
        if workforce_status in ("terminated", "contractor_expired"):
            recommendation = "DISABLE"
            reason = f"Workforce status is {workforce_status}."

        elif (
            lifecycle_state == "inactive"
            and isinstance(interactive_age, (int, float))
            and interactive_age >= stale_days
        ):
            recommendation = "DISABLE"
            reason = (
                f"Inactive lifecycle state with interactive login age "
                f"{interactive_age} days."
            )

    elif identity_type == "service_account":
        if (
            isinstance(interactive_age, (int, float))
            and interactive_age >= stale_days
        ):
            if isinstance(noninteractive_age, (int, float)) and noninteractive_age <= 30:
                recommendation = "KEEP_ENABLED"
                reason = (
                    "Interactive login is stale, but recent non-interactive "
                    "authentication indicates active service use."
                )
            else:
                recommendation = "REVIEW"
                reason = (
                    "Service account appears stale and requires owner and "
                    "dependency review before remediation."
                )

    elif identity_type == "privileged":
        recommendation = "REVIEW"
        reason = "Privileged identity requires approval for remediation."

    else:
        recommendation = "REVIEW"
        reason = "Identity type is unknown or unsupported."

    if confidence in ("LOW", "INSUFFICIENT"):
        if recommendation == "DISABLE":
            recommendation = "REVIEW"
        reason += f" Confidence={confidence}; unattended remediation not permitted."

    return {
        "username": username,
        "identity_type": identity_type,
        "workforce_status": workforce_status,
        "days_since_interactive_login": interactive_age,
        "days_since_noninteractive_auth": noninteractive_age,
        "confidence": confidence,
        "authority": authority,
        "recommendation": recommendation,
        "reason": reason,
    }


with INPUT_FILE.open("r", encoding="utf-8-sig") as f:
    data = json.load(f)

with CONFIG_FILE.open("r", encoding="utf-8-sig") as f:
    config = json.load(f)

if config.get("mode") != "dry_run":
    raise SystemExit("V2 decision engine requires mode=dry_run for this phase.")

rows = []

with LOG_FILE.open("w", encoding="utf-8") as log:
    log.write(f"{timestamp()} V2 dry run started\n")

    for account in data["accounts"]:
        result = evaluate(
            account,
            config["stale_interactive_days"]
        )

        rows.append(result)

        log.write(
            f"{timestamp()} "
            f"username={result['username']} "
            f"confidence={result['confidence']} "
            f"authority={result['authority']} "
            f"recommendation={result['recommendation']}\n"
        )

    log.write(f"{timestamp()} V2 dry run completed\n")


fieldnames = [
    "username",
    "identity_type",
    "workforce_status",
    "days_since_interactive_login",
    "days_since_noninteractive_auth",
    "confidence",
    "authority",
    "recommendation",
    "reason",
]

with DECISIONS_FILE.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


print("V2 dry run complete.")
print(f"Input:     {INPUT_FILE}")
print(f"Config:    {CONFIG_FILE}")
print(f"Decisions: {DECISIONS_FILE}")
print(f"Log:       {LOG_FILE}")

