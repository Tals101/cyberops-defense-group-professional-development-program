import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

IDENTITIES = BASE / "simulation" / "identities-original.json"
DECISIONS = BASE / "evidence" / "v2-dry-run-decisions.csv"
ENFORCEMENT = BASE / "evidence" / "v2-enforcement-results.csv"
OUTPUT = BASE / "evidence" / "v2-automation-decision-record.csv"


with IDENTITIES.open("r", encoding="utf-8-sig") as f:
    identity_data = json.load(f)

with DECISIONS.open("r", encoding="utf-8-sig") as f:
    decisions = {
        row["username"]: row
        for row in csv.DictReader(f)
    }

with ENFORCEMENT.open("r", encoding="utf-8-sig") as f:
    enforcement = {
        row["username"]: row
        for row in csv.DictReader(f)
    }


records = []

for account in identity_data["accounts"]:
    username = account["username"]

    decision = decisions.get(username, {})
    action = enforcement.get(username, {})

    dependencies = account.get("service_dependencies", [])
    if isinstance(dependencies, list):
        dependencies = "; ".join(dependencies)

    approval_required = (
        "YES"
        if decision.get("authority") == "REQUIRE_APPROVAL"
        else "NO"
    )

    actual_action = action.get("action", "UNKNOWN")
    result = action.get("result", "UNKNOWN")

    reversible = (
        "YES"
        if actual_action in ("DISABLE", "NO_ACTION", "STAGE_ONLY")
        else "UNKNOWN"
    )

    if actual_action == "DISABLE":
        recovery_method = "Restore enabled state from pre-change snapshot and validate dependent services."
    elif actual_action == "STAGE_ONLY":
        recovery_method = "No production state change occurred; no rollback required."
    elif actual_action == "NO_ACTION":
        recovery_method = "No production state change occurred; no rollback required."
    else:
        recovery_method = "Review required."

    records.append({
        "identity": username,
        "identity_type": account.get("identity_type"),
        "workforce_status": account.get("workforce_status"),
        "owner": account.get("owner"),
        "business_purpose": account.get("business_purpose"),
        "days_since_interactive_login": account.get("days_since_interactive_login"),
        "days_since_noninteractive_auth": account.get("days_since_noninteractive_auth"),
        "privilege": account.get("privilege"),
        "service_dependencies": dependencies,
        "approval_status": account.get("approval_status"),
        "lifecycle_state": account.get("lifecycle_state"),
        "data_freshness": account.get("data_freshness"),
        "evidence_completeness": account.get("evidence_completeness"),
        "enabled_before": account.get("enabled"),
        "confidence": decision.get("confidence"),
        "decision": decision.get("recommendation"),
        "decision_reason": decision.get("reason"),
        "authority": decision.get("authority"),
        "approval_required": approval_required,
        "proposed_action": decision.get("recommendation"),
        "actual_action": actual_action,
        "result": result,
        "reversible": reversible,
        "recovery_method": recovery_method,
        "evidence_sources": (
            "simulation/identities-original.json; "
            "evidence/v2-dry-run-decisions.csv; "
            "evidence/v2-enforcement-results.csv"
        )
    })


fieldnames = [
    "identity",
    "identity_type",
    "workforce_status",
    "owner",
    "business_purpose",
    "days_since_interactive_login",
    "days_since_noninteractive_auth",
    "privilege",
    "service_dependencies",
    "approval_status",
    "lifecycle_state",
    "data_freshness",
    "evidence_completeness",
    "enabled_before",
    "confidence",
    "decision",
    "decision_reason",
    "authority",
    "approval_required",
    "proposed_action",
    "actual_action",
    "result",
    "reversible",
    "recovery_method",
    "evidence_sources"
]


with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)


print(f"Decision records created: {len(records)}")
print(f"Output: {OUTPUT}")
