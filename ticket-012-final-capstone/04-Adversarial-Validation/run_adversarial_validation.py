"""
Ticket 012 - Adversarial and Resilience Validation

Eight synthetic detector-level exercises.
Operational Kubernetes validation is tracked separately.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT / "03-Detection-Engineering" / "src")
)

from correlation_detector_v2 import correlate_security_event_v2

EVIDENCE = ROOT / "04-Adversarial-Validation" / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)

APPROVED = "http://internal-service:8080/resource"
UNAPPROVED = "http://unapproved-collector:8080/resource"

scenarios = []


def add(
    case_id,
    title,
    truth,
    *,
    destination=APPROVED,
    network_time="2026-11-12T18:14:40Z",
    deployment_time="2026-11-12T18:12:00Z",
    identity="application-api",
    deployment_type="deployment_change",
    missing_deployment=False,
    expected_alert=True,
    expected_recent=False,
    expected_warning=None,
    expected_reason=None,
    note=""
):
    network = {
        "event_id": "N-" + case_id,
        "event_type": "network_request",
        "timestamp": network_time,
        "workload": "application-api",
        "destination": destination,
    }

    if identity is not None:
        network["claimed_identity"] = identity

    deployment = None if missing_deployment else {
        "event_id": "D-" + case_id,
        "event_type": deployment_type,
        "timestamp": deployment_time,
        "workload": "application-api",
    }

    scenarios.append({
        "case_id": case_id,
        "title": title,
        "ground_truth": truth,
        "network_event": network,
        "deployment_event": deployment,
        "expected_alert": expected_alert,
        "expected_recent_change": expected_recent,
        "expected_warning": expected_warning,
        "expected_reason": expected_reason,
        "limitation_note": note,
    })


# 1. True positive with three indicators
add(
    "AV01", "True positive", "suspicious",
    destination=UNAPPROVED,
    identity="internal-service",
    expected_recent=True,
    expected_reason="claimed_identity_mismatch",
    note="Claimed identity is not independently authenticated."
)

# 2. Benign lookalike that produces a false positive
add(
    "AV02", "Benign identity lookalike", "benign",
    identity="internal-service",
    expected_recent=True,
    expected_reason="claimed_identity_mismatch",
    note="Known false positive: metadata mismatch without verified misuse."
)

# 3. Simulated two-second negative clock skew
add(
    "AV03", "Clock skew", "suspicious",
    destination=UNAPPROVED,
    network_time="2026-11-12T18:11:58Z",
    expected_recent=False,
    expected_reason="unapproved_destination",
    note="Temporal correlation is lost; independent destination alert remains."
)

# 4. Missing claimed identity
add(
    "AV04", "Identity ambiguity", "suspicious",
    destination=UNAPPROVED,
    identity=None,
    expected_recent=True,
    expected_warning="identity_telemetry_incomplete",
    note="Missing identity must not be interpreted as authenticated."
)

# 5. Configuration change without deployment-change telemetry
add(
    "AV05", "Configuration change", "suspicious",
    destination=UNAPPROVED,
    deployment_type="config_change",
    expected_recent=False,
    expected_warning="deployment_change_not_available",
    note="Configuration events are not yet independently correlated."
)

# 6. Deployment telemetry unavailable
add(
    "AV06", "Missing deployment telemetry", "suspicious",
    destination=UNAPPROVED,
    missing_deployment=True,
    expected_recent=False,
    expected_warning="deployment_telemetry_missing",
    note="Detection must not depend solely on available deployment data."
)

# 7. Simulated direct-to-collector policy bypass
add(
    "AV07", "Simulated policy bypass", "suspicious",
    destination=UNAPPROVED,
    expected_recent=True,
    expected_reason="unapproved_destination",
    note="Synthetic direct-call event only; actual network enforcement untested here."
)

# 8. Simulated continuing unauthorized traffic after rollback
add(
    "AV08", "Simulated rollback failure", "suspicious",
    destination=UNAPPROVED,
    network_time="2026-11-12T18:30:00Z",
    deployment_time="2026-11-12T18:20:00Z",
    expected_recent=False,
    expected_reason="unapproved_destination",
    note="Post-rollback traffic simulated; no Kubernetes rollback executed here."
)

assert len(scenarios) == 8

results = []

for item in scenarios:
    result = correlate_security_event_v2(
        item["network_event"],
        item["deployment_event"]
    )

    checks = {
        "alert": result["alert"] == item["expected_alert"],
        "recent_change": (
            result["recent_deployment_change"]
            == item["expected_recent_change"]
        ),
    }

    if item["expected_warning"]:
        checks["warning"] = (
            item["expected_warning"] in result["telemetry_warnings"]
        )

    if item["expected_reason"]:
        checks["reason"] = (
            item["expected_reason"] in result["reasons"]
        )

    passed = all(checks.values())
    predicted_suspicious = result["alert"]
    actually_suspicious = item["ground_truth"] == "suspicious"

    if predicted_suspicious and actually_suspicious:
        classification = "true_positive"
    elif predicted_suspicious and not actually_suspicious:
        classification = "false_positive"
    elif not predicted_suspicious and actually_suspicious:
        classification = "false_negative"
    else:
        classification = "true_negative"

    results.append({
        "case_id": item["case_id"],
        "title": item["title"],
        "scope": "synthetic_detector_validation",
        "ground_truth": item["ground_truth"],
        "classification": classification,
        "checks": checks,
        "test_passed": passed,
        "detector_result": result,
        "limitation_note": item["limitation_note"],
    })

passed_count = sum(row["test_passed"] for row in results)

summary = {
    "test_type": "synthetic_adversarial_and_resilience",
    "test_count": len(results),
    "passed": passed_count,
    "failed": len(results) - passed_count,
    "operational_validation_completed": False,
    "results": results,
}

json_path = EVIDENCE / "adversarial-validation-results.json"
report_path = EVIDENCE / "adversarial-validation-report.txt"

json_path.write_text(
    json.dumps(summary, indent=2),
    encoding="utf-8"
)

lines = [
    "TICKET 012 - ADVERSARIAL AND RESILIENCE VALIDATION",
    "Scope: Synthetic detector-level execution",
    "",
]

for item in results:
    status = "PASS" if item["test_passed"] else "FAIL"
    lines.append(
        f'{item["case_id"]} {status} - {item["title"]}'
    )
    lines.append(
        "  Classification: " + item["classification"]
    )
    lines.append(
        "  Note: " + item["limitation_note"]
    )

lines.extend([
    "",
    f"RESULT: {passed_count}/{len(results)} behavioral checks passed",
    "",
    "PASS indicates expected detector behavior, not necessarily",
    "correct classification of benign versus suspicious traffic.",
    "",
    "Operational Kubernetes policy bypass and rollback",
    "failure exercises remain outstanding.",
])

report = "\n".join(lines) + "\n"

report_path.write_text(report, encoding="utf-8")

print(report)
print("JSON evidence:", json_path)
print("Text evidence:", report_path)

sys.exit(0 if passed_count == len(results) else 1)
