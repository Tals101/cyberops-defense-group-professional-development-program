import csv
import json
from pathlib import Path

from correlation_detector import classify_destination, correlate_security_event

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "03-Detection-Engineering" / "synthetic-data"
EVIDENCE = ROOT / "07-Evidence" / "supporting-outputs"

DATA.mkdir(parents=True, exist_ok=True)
EVIDENCE.mkdir(parents=True, exist_ok=True)

APPROVED = "http://internal-service:8080/resource"
UNAPPROVED = "http://unapproved-collector:8080/resource"

cases = []


def add(
    case_id, label, description, *,
    destination=APPROVED,
    network_time="2026-11-12T18:14:40Z",
    deployment_time="2026-11-12T18:12:00Z",
    workload="application-api",
    deployment_workload=None,
    claimed_identity="application-api",
    deployment_type="deployment_change"
):
    network = {
        "event_id": "N-" + case_id,
        "event_type": "network_request",
        "timestamp": network_time,
        "workload": workload,
    }

    if destination is not None:
        network["destination"] = destination

    if claimed_identity is not None:
        network["claimed_identity"] = claimed_identity

    deployment = {
        "event_id": "D-" + case_id,
        "event_type": deployment_type,
        "timestamp": deployment_time,
        "workload": deployment_workload or workload,
    }

    cases.append({
        "case_id": case_id,
        "label": label,
        "description": description,
        "network_event": network,
        "deployment_event": deployment,
    })


# 12 BENIGN SYNTHETIC SCENARIOS

add("B01", "benign", "Approved traffic after deployment")
add("B02", "benign", "Approved traffic outside deployment window",
    deployment_time="2026-11-12T18:00:00Z")
add("B03", "benign", "Approved traffic with missing identity",
    claimed_identity=None)
add("B04", "benign", "Approved traffic with inconsistent identity metadata",
    claimed_identity="internal-service")
add("B05", "benign", "Approved traffic before deployment",
    deployment_time="2026-11-12T18:20:00Z")
add("B06", "benign", "Approved traffic with unrelated deployment",
    deployment_workload="internal-service")
add("B07", "benign", "Approved traffic at five-minute boundary",
    network_time="2026-11-12T18:17:00Z")
add("B08", "benign", "Approved traffic with maintenance event",
    deployment_type="maintenance")
add("B09", "benign", "Normal unknown workload scenario",
    workload="unknown-application")

# These three are intentionally labeled authorized exceptions
# in synthetic ground truth, despite being absent from the allowlist.

add("B10", "benign", "Authorized diagnostic exception outside change window",
    destination=UNAPPROVED,
    deployment_time="2026-11-12T18:00:00Z")
add("B11", "benign", "Authorized exception with unrelated deployment",
    destination=UNAPPROVED,
    deployment_workload="internal-service")
add("B12", "benign", "Authorized exception following deployment",
    destination=UNAPPROVED)


# 12 SUSPICIOUS SYNTHETIC SCENARIOS

add("S01", "suspicious", "Unapproved destination after deployment",
    destination=UNAPPROVED)
add("S02", "suspicious", "Unapproved destination and identity mismatch",
    destination=UNAPPROVED,
    claimed_identity="internal-service")
add("S03", "suspicious", "Unapproved destination with missing identity",
    destination=UNAPPROVED,
    claimed_identity=None)
add("S04", "suspicious", "Unapproved destination at five-minute boundary",
    destination=UNAPPROVED,
    network_time="2026-11-12T18:17:00Z")
add("S05", "suspicious", "Unapproved destination at 299 seconds",
    destination=UNAPPROVED,
    network_time="2026-11-12T18:16:59Z")
add("S06", "suspicious", "Unapproved destination outside correlation window",
    destination=UNAPPROVED,
    deployment_time="2026-11-12T18:00:00Z")
add("S07", "suspicious", "Unapproved destination before deployment",
    destination=UNAPPROVED,
    deployment_time="2026-11-12T18:20:00Z")
add("S08", "suspicious", "Unapproved destination with unrelated deployment",
    destination=UNAPPROVED,
    deployment_workload="internal-service")
add("S09", "suspicious", "Unapproved destination without deployment event",
    destination=UNAPPROVED,
    deployment_type="maintenance")
add("S10", "suspicious", "Suspicious identity mismatch at approved destination",
    claimed_identity="internal-service")
add("S11", "suspicious", "Unknown workload contacting suspicious destination",
    destination=UNAPPROVED,
    workload="unknown-application")
add("S12", "suspicious", "Unapproved destination at 301 seconds",
    destination=UNAPPROVED,
    network_time="2026-11-12T18:17:01Z")


assert len(cases) == 24
assert sum(c["label"] == "benign" for c in cases) == 12
assert sum(c["label"] == "suspicious" for c in cases) == 12

dataset_path = DATA / "labeled-correlation-scenarios.json"

dataset_path.write_text(
    json.dumps({
        "dataset_type": "synthetic",
        "description": "Ticket 012 labeled detector evaluation scenarios",
        "cases": cases,
    }, indent=2),
    encoding="utf-8",
)

results = []

for item in cases:
    network = item["network_event"]
    deployment = item["deployment_event"]

    baseline_alert = classify_destination(network) == "unapproved"
    correlated = correlate_security_event(network, deployment)

    results.append({
        "case_id": item["case_id"],
        "expected_label": item["label"],
        "description": item["description"],
        "baseline_alert": baseline_alert,
        "correlated_alert": correlated["alert"],
        "destination_status": correlated["destination_status"],
        "identity_status": correlated["identity_status"],
        "recent_deployment_change": correlated["recent_deployment_change"],
        "triage_level": correlated["triage_level"],
    })


def calculate_metrics(prediction_field):
    tp = fp = tn = fn = 0

    for row in results:
        actual = row["expected_label"] == "suspicious"
        predicted = row[prediction_field]

        if actual and predicted:
            tp += 1
        elif not actual and predicted:
            fp += 1
        elif not actual and not predicted:
            tn += 1
        else:
            fn += 1

    return {
        "TP": tp, "FP": fp, "TN": tn, "FN": fn,
        "precision": round(tp / (tp + fp), 3) if tp + fp else 0,
        "recall": round(tp / (tp + fn), 3) if tp + fn else 0,
        "false_positive_rate": round(fp / (fp + tn), 3) if fp + tn else 0,
    }


baseline = calculate_metrics("baseline_alert")
candidate = calculate_metrics("correlated_alert")

summary = {
    "dataset_type": "synthetic",
    "total_cases": len(cases),
    "benign_cases": 12,
    "suspicious_cases": 12,
    "baseline_definition": "Alert on any unapproved destination",
    "candidate_definition": "Unapproved destination AND recent deployment",
    "baseline_metrics": baseline,
    "candidate_metrics": candidate,
    "limitations": [
        "Synthetic labels are scenario assumptions, not observed incidents",
        "Authorized exceptions are not represented in the static allowlist",
        "Correlation may miss suspicious traffic without a recent deployment",
        "Identity fields are compared, not independently authenticated",
    ],
}

(EVIDENCE / "baseline-comparison-results.json").write_text(
    json.dumps(summary, indent=2), encoding="utf-8"
)

with (EVIDENCE / "baseline-comparison-predictions.csv").open(
    "w", newline="", encoding="utf-8"
) as output:
    writer = csv.DictWriter(output, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

lines = [
    "TICKET 012 - SYNTHETIC BASELINE COMPARISON",
    "24 labeled scenarios: 12 benign and 12 suspicious",
    "",
]

for name, metrics in [
    ("Destination-only baseline", baseline),
    ("Multi-dimensional correlation", candidate),
]:
    lines.extend([
        name,
        "TP={TP} FP={FP} TN={TN} FN={FN}".format(**metrics),
        "Precision={precision:.3f} Recall={recall:.3f} FPR={false_positive_rate:.3f}".format(**metrics),
        "",
    ])

for field, name in [
    ("baseline_alert", "BASELINE"),
    ("correlated_alert", "CORRELATION"),
]:
    lines.append(name + " FALSE NEGATIVES:")
    lines.extend(
        row["case_id"] + ": " + row["description"]
        for row in results
        if row["expected_label"] == "suspicious" and not row[field]
    )
    lines.append("")
    lines.append(name + " FALSE POSITIVES:")
    lines.extend(
        row["case_id"] + ": " + row["description"]
        for row in results
        if row["expected_label"] == "benign" and row[field]
    )
    lines.append("")

lines.append("All labels and authorized exceptions are synthetic assumptions.")
lines.append("Passing tests does not establish production detection effectiveness.")

report = "\n".join(lines) + "\n"

(EVIDENCE / "baseline-comparison-report.txt").write_text(
    report, encoding="utf-8"
)

print(report)
print("Generated labeled dataset, JSON metrics, CSV predictions, and report.")
