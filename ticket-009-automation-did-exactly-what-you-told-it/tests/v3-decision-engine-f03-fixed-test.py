import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

PRIMARY_FILE = BASE / "simulation" / "v3-identities.json"
SECONDARY_FILE = BASE / "simulation" / "v3-secondary-context.json"
DECISIONS_FILE = BASE / "evidence" / "v3-f03-fixed-decisions.csv"
LOG_FILE = BASE / "evidence"

STALE_INTERACTIVE_DAYS = 90

SUPPORTED_TYPES = {
    "employee",
    "contractor",
    "service_account",
    "privileged",
}


def text(value):
    if value is None:
        return ""
    return str(value).strip()


def lower(value):
    return text(value).lower()


def list_value(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def audit_log_preflight():
    try:
        if not LOG_FILE.parent.exists():
            raise OSError(
                f"Audit-log parent directory does not exist: {LOG_FILE.parent}"
            )

        if LOG_FILE.exists() and LOG_FILE.is_dir():
            raise IsADirectoryError(
                f"Audit-log path is a directory: {LOG_FILE}"
            )

        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(
                "audit_preflight=PASS | "
                + datetime.now(timezone.utc).isoformat()
                + "\n"
            )

    except OSError as exc:
        print("FAIL: required audit logging is unavailable.")
        print(f"Audit path: {LOG_FILE}")
        print(f"Error: {type(exc).__name__}: {exc}")
        print("No decisions or remediation occurred.")
        raise SystemExit(1)


def load_json_source(path, source_name):
    try:
        with path.open("r", encoding="utf-8-sig") as handle:
            return json.load(handle)

    except (json.JSONDecodeError, OSError) as exc:
        failure_time = datetime.now(timezone.utc).isoformat()

        log_lines = [
            f"started_utc={failure_time}",
            "mode=DRY_RUN",
            "status=FAIL_CLOSED",
            "failure_type=INPUT_READ_OR_PARSE_FAILURE",
            f"source={source_name}",
            f"path={path}",
            f"error_type={type(exc).__name__}",
            f"error={str(exc)}",
            "decision_records=0",
            "remediation_performed=False",
            "safe_to_retry_after_input_correction=True",
        ]

        LOG_FILE.write_text(
            "\n".join(log_lines) + "\n",
            encoding="utf-8",
        )

        print(
            f"FAIL: {source_name} input could not be read or parsed. "
            "No decisions or remediation occurred."
        )
        print(f"Failure log: {LOG_FILE}")

        raise SystemExit(1)


def missing_required_primary_fields(account):
    required_fields = [
        "identity_type",
        "workforce_status",
        "owner",
        "business_purpose",
        "lifecycle_state",
        "data_freshness",
        "evidence_completeness",
    ]

    missing = []

    for field in required_fields:
        value = lower(account.get(field))
        if value in {"", "unknown", "none", "null"}:
            missing.append(field)

    return missing


def primary_confidence(account):
    missing = missing_required_primary_fields(account)

    if missing:
        return "INSUFFICIENT"

    completeness = lower(account.get("evidence_completeness"))
    freshness = lower(account.get("data_freshness"))

    if completeness != "complete":
        return "INSUFFICIENT"

    if freshness != "current":
        return "LOW"

    return "HIGH"


def primary_recommendation(account):
    identity_type = lower(account.get("identity_type"))
    workforce_status = lower(account.get("workforce_status"))
    lifecycle_state = lower(account.get("lifecycle_state"))
    days_interactive = account.get("days_since_interactive_login")
    days_noninteractive = account.get("days_since_noninteractive_auth")

    if identity_type in {"employee", "contractor"}:
        if workforce_status in {"terminated", "contractor_expired"}:
            return "DISABLE", "Authoritative workforce status supports remediation."

        if lifecycle_state in {"inactive", "pending_disable"}:
            if isinstance(days_interactive, (int, float)) and days_interactive >= STALE_INTERACTIVE_DAYS:
                return "DISABLE", "Inactive lifecycle and stale interactive activity support remediation."

        return "NO_ACTION", "Primary evidence does not support destructive remediation."

    if identity_type == "service_account":
        if (
            isinstance(days_interactive, (int, float))
            and days_interactive >= STALE_INTERACTIVE_DAYS
            and isinstance(days_noninteractive, (int, float))
            and days_noninteractive <= 30
        ):
            return (
                "KEEP_ENABLED",
                "Interactive login is stale but recent non-interactive authentication indicates active service use.",
            )

        return "REVIEW", "Service identity requires contextual review."

    if identity_type == "privileged":
        return "REVIEW", "Privileged identity requires human review."

    return "REVIEW", "Identity type is unsupported or unknown."


def canonical_primary_lifecycle(account):
    workforce_status = lower(account.get("workforce_status"))
    lifecycle_state = lower(account.get("lifecycle_state"))

    if workforce_status == "terminated":
        return "terminated"

    if workforce_status == "contractor_expired":
        return "contractor_expired"

    return lifecycle_state


def evidence_trust(account, secondary):
    reasons = []
    missing = missing_required_primary_fields(account)

    if secondary is None:
        return "INCOMPLETE", ["No secondary corroborating record exists."]

    if lower(account.get("evidence_completeness")) != "complete":
        return "INCOMPLETE", ["Primary evidence is incomplete."]

    if lower(account.get("data_freshness")) != "current":
        return "STALE", ["Primary evidence is stale."]

    if lower(secondary.get("source_freshness")) != "current":
        return "STALE", ["Secondary evidence is stale."]

    secondary_confidence = lower(secondary.get("source_confidence"))
    if secondary_confidence not in {"high", "medium"}:
        return "UNKNOWN", ["Secondary-source confidence is insufficient."]

    primary_type = lower(account.get("identity_type"))
    secondary_role = lower(secondary.get("authoritative_identity_role"))

    if (
        primary_type in SUPPORTED_TYPES
        and secondary_role
        and primary_type != secondary_role
    ):
        reasons.append(
            f"Identity-role conflict: primary={primary_type}, secondary={secondary_role}."
        )

    primary_lifecycle = canonical_primary_lifecycle(account)
    secondary_lifecycle = lower(secondary.get("lifecycle_status"))

    if (
        primary_lifecycle
        and secondary_lifecycle
        and primary_lifecycle != secondary_lifecycle
    ):
        reasons.append(
            f"Lifecycle conflict: primary={primary_lifecycle}, secondary={secondary_lifecycle}."
        )

    primary_dependencies = {
        lower(item)
        for item in list_value(account.get("service_dependencies"))
        if text(item)
    }

    secondary_dependencies = {
        lower(item)
        for item in list_value(secondary.get("application_dependency"))
        if text(item)
    }

    if primary_dependencies != secondary_dependencies:
        reasons.append(
            "Dependency conflict between IAM and secondary application context."
        )

    if reasons:
        if missing:
            reasons.insert(
                0,
                "Missing required primary fields: " + ", ".join(missing) + "."
            )
        return "CONFLICTING", reasons

    if missing:
        return (
            "INCOMPLETE",
            ["Missing required primary fields: " + ", ".join(missing) + "."],
        )

    return "TRUSTED", ["Required primary and secondary evidence is sufficiently corroborated."]


def authority(account, secondary, confidence, trust):
    identity_type = lower(account.get("identity_type"))

    if identity_type not in SUPPORTED_TYPES:
        return "DO_NOT_AUTOMATE", "Identity type is unknown or unsupported."

    if trust == "UNKNOWN":
        return "DO_NOT_AUTOMATE", "Evidence trust cannot be established."

    if trust in {"CONFLICTING", "INCOMPLETE", "STALE"}:
        return "REQUIRE_APPROVAL", f"Evidence trust is {trust}."

    if confidence != "HIGH":
        return "REQUIRE_APPROVAL", f"Decision confidence is {confidence}."

    if identity_type in {"service_account", "privileged"}:
        return "REQUIRE_APPROVAL", "Identity class is protected from unattended destructive remediation."

    if secondary is not None:
        criticality = lower(secondary.get("business_criticality"))
        dependencies = list_value(secondary.get("application_dependency"))

        if criticality in {"high", "critical"}:
            return "REQUIRE_APPROVAL", f"Business criticality is {criticality}."

        if len(dependencies) > 0:
            return "REQUIRE_APPROVAL", "Secondary source identifies an application dependency."

    return "AUTO_REMEDIATE", "Evidence and identity context satisfy bounded automatic authority."


def main():
    audit_log_preflight()

    primary_data = load_json_source(
        PRIMARY_FILE,
        "PRIMARY_IDENTITY_SOURCE",
    )

    secondary_data = load_json_source(
        SECONDARY_FILE,
        "SECONDARY_CONTEXT_SOURCE",
    )

    accounts = primary_data["accounts"]

    secondary_index = {
        record["username"]: record
        for record in secondary_data["records"]
    }

    decisions = []
    log_lines = []

    started = datetime.now(timezone.utc).isoformat()

    log_lines.append(f"started_utc={started}")
    log_lines.append("mode=DRY_RUN")
    log_lines.append(f"primary_records={len(accounts)}")
    log_lines.append(f"secondary_records={len(secondary_index)}")

    for account in accounts:
        username = account["username"]
        secondary = secondary_index.get(username)

        confidence = primary_confidence(account)
        recommendation, decision_reason = primary_recommendation(account)
        trust, trust_reasons = evidence_trust(account, secondary)
        auth, authority_reason = authority(
            account,
            secondary,
            confidence,
            trust,
        )

        approval_required = "YES" if auth == "REQUIRE_APPROVAL" else "NO"

        secondary_role = ""
        secondary_lifecycle = ""
        secondary_criticality = ""
        secondary_dependencies = ""

        if secondary is not None:
            secondary_role = text(
                secondary.get("authoritative_identity_role")
            )
            secondary_lifecycle = text(
                secondary.get("lifecycle_status")
            )
            secondary_criticality = text(
                secondary.get("business_criticality")
            )
            secondary_dependencies = "; ".join(
                list_value(secondary.get("application_dependency"))
            )

        decisions.append(
            {
                "username": username,
                "primary_identity_type": text(account.get("identity_type")),
                "primary_workforce_status": text(account.get("workforce_status")),
                "primary_lifecycle_state": text(account.get("lifecycle_state")),
                "primary_owner": text(account.get("owner")),
                "primary_business_purpose": text(account.get("business_purpose")),
                "primary_dependencies": "; ".join(
                    list_value(account.get("service_dependencies"))
                ),
                "secondary_record_present": "YES" if secondary else "NO",
                "secondary_identity_role": secondary_role,
                "secondary_lifecycle_status": secondary_lifecycle,
                "secondary_business_criticality": secondary_criticality,
                "secondary_dependencies": secondary_dependencies,
                "decision_confidence": confidence,
                "evidence_trust": trust,
                "evidence_trust_reason": " | ".join(trust_reasons),
                "recommendation": recommendation,
                "decision_reason": decision_reason,
                "authority": auth,
                "authority_reason": authority_reason,
                "approval_required": approval_required,
                "actual_action": "NO_ACTION_DRY_RUN",
                "result": "DRY_RUN_ONLY",
            }
        )

        log_lines.append(
            " | ".join(
                [
                    f"username={username}",
                    f"confidence={confidence}",
                    f"trust={trust}",
                    f"recommendation={recommendation}",
                    f"authority={auth}",
                    "action=NO_ACTION_DRY_RUN",
                ]
            )
        )

    fieldnames = list(decisions[0].keys())

    with DECISIONS_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(decisions)

    completed = datetime.now(timezone.utc).isoformat()
    log_lines.append(f"completed_utc={completed}")
    log_lines.append(f"decision_records={len(decisions)}")

    LOG_FILE.write_text(
        "\n".join(log_lines) + "\n",
        encoding="utf-8",
    )

    print(f"Primary identities: {len(accounts)}")
    print(f"Secondary records: {len(secondary_index)}")
    print(f"Decision records: {len(decisions)}")
    print(f"Decisions: {DECISIONS_FILE}")
    print(f"Log: {LOG_FILE}")


if __name__ == "__main__":
    main()
