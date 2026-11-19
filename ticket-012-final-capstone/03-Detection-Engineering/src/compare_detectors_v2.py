import csv
import json
from pathlib import Path

from correlation_detector import classify_destination, correlate_security_event
from correlation_detector_v2 import correlate_security_event_v2

ROOT = Path(__file__).resolve().parents[2]

dataset_path = (
    ROOT / "03-Detection-Engineering" /
    "synthetic-data" / "labeled-correlation-scenarios.json"
)

evidence = ROOT / "07-Evidence" / "supporting-outputs"

dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
cases = dataset["cases"]

results = []

for case in cases:
    network = case["network_event"]
    deployment = case["deployment_event"]

    baseline = classify_destination(network) == "unapproved"
    version_1 = correlate_security_event(network, deployment)
    version_2 = correlate_security_event_v2(network, deployment)

    results.append({
        "case_id": case["case_id"],
        "expected_label": case["label"],
        "description": case["description"],
        "baseline_alert": baseline,
        "v1_alert": version_1["alert"],
        "v2_alert": version_2["alert"],
        "v1_priority": version_1["triage_level"],
        "v2_priority": version_2["triage_level"],
        "v2_reasons": ";".join(version_2["reasons"]),
        "v2_warnings": ";".join(version_2["telemetry_warnings"]),
    })


def metrics(field):
    tp = fp = tn = fn = 0

    for row in results:
        actual = row["expected_label"] == "suspicious"
        predicted = row[field]

        if actual and predicted:
            tp += 1
        elif not actual and predicted:
            fp += 1
        elif not actual and not predicted:
            tn += 1
        else:
            fn += 1

    return {
        "TP": tp,
        "FP": fp,
        "TN": tn,
        "FN": fn,
        "precision": round(tp / (tp + fp), 3) if tp + fp else 0,
        "recall": round(tp / (tp + fn), 3) if tp + fn else 0,
        "false_positive_rate": round(fp / (fp + tn), 3) if fp + tn else 0,
    }


comparison = {
    "dataset_type": "synthetic",
    "case_count": len(cases),
    "baseline": metrics("baseline_alert"),
    "version_1": metrics("v1_alert"),
    "version_2": metrics("v2_alert"),
    "limitations": [
        "Synthetic scenarios do not establish production performance.",
        "Authorized exceptions are not independently verified.",
        "Claimed identity is not authenticated.",
        "Unknown workloads may generate false positives."
    ],
}

json_path = evidence / "detector-v1-v2-comparison.json"
csv_path = evidence / "detector-v1-v2-predictions.csv"
report_path = evidence / "detector-v1-v2-comparison.txt"

json_path.write_text(json.dumps(comparison, indent=2), encoding="utf-8")

with csv_path.open("w", newline="", encoding="utf-8") as output:
    writer = csv.DictWriter(output, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

lines = [
    "TICKET 012 - DETECTOR VERSION COMPARISON",
    "Synthetic scenarios: " + str(len(cases)),
    "",
]

for name in ("baseline", "version_1", "version_2"):
    m = comparison[name]
    lines.extend([
        name.upper(),
        "TP={TP} FP={FP} TN={TN} FN={FN}".format(**m),
        "Precision={precision:.3f} Recall={recall:.3f} FPR={false_positive_rate:.3f}".format(**m),
        "",
    ])

for name, field in (
    ("BASELINE", "baseline_alert"),
    ("VERSION 1", "v1_alert"),
    ("VERSION 2", "v2_alert"),
):
    lines.append(name + " FALSE NEGATIVES:")
    matches = [
        r["case_id"] for r in results
        if r["expected_label"] == "suspicious" and not r[field]
    ]
    lines.append(", ".join(matches) if matches else "None")
    lines.append(name + " FALSE POSITIVES:")
    matches = [
        r["case_id"] for r in results
        if r["expected_label"] == "benign" and r[field]
    ]
    lines.append(", ".join(matches) if matches else "None")
    lines.append("")

lines.append("All scenarios and expected labels are synthetic.")
report = "\n".join(lines) + "\n"

report_path.write_text(report, encoding="utf-8")
print(report)
print("Comparison evidence saved.")
