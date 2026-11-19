"""
Ticket 012 - Detection CLI

Processes synthetic event-pair exports using correlation
detector Version 2.

Exit codes:
0 = all records processed successfully
1 = input/output error or one or more invalid records
2 = invalid command-line arguments
"""

import argparse
import json
import sys
from pathlib import Path

from correlation_detector import prepare_event
from correlation_detector_v2 import correlate_security_event_v2


def positive_integer(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Expected an integer")

    if number <= 0:
        raise argparse.ArgumentTypeError(
            "Correlation window must be positive"
        )

    return number


def explain(result):
    reasons = result["reasons"]

    if reasons:
        explanation = (
            "Alert generated: " + ", ".join(reasons) + "."
        )
    else:
        explanation = (
            "No alert generated from available indicators."
        )

    if result["recent_deployment_change"]:
        explanation += (
            " A deployment change occurred within "
            "the configured correlation window."
        )

    if result["telemetry_warnings"]:
        explanation += (
            " Telemetry limitations: "
            + ", ".join(result["telemetry_warnings"])
            + "."
        )

    return explanation


def extract_cases(data):
    if isinstance(data, dict) and isinstance(
        data.get("cases"), list
    ):
        return data["cases"]

    if isinstance(data, dict) and "network_event" in data:
        return [data]

    if isinstance(data, list):
        return data

    raise ValueError(
        "Expected a case, a list of cases, "
        "or an object containing a cases list"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Ticket 012 correlation detector CLI"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input JSON file"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output JSON file"
    )

    parser.add_argument(
        "--window-seconds",
        type=positive_integer,
        default=300,
        help="Deployment correlation window (default: 300)"
    )

    args = parser.parse_args()

    try:
        data = json.loads(
            Path(args.input).read_text(encoding="utf-8")
        )
        cases = extract_cases(data)
    except (OSError, ValueError) as error:
        print("INPUT_ERROR=" + str(error), file=sys.stderr)
        return 1

    results = []
    errors = []
    seen_network_events = {}

    for index, case in enumerate(cases, start=1):
        case_id = (
            case.get("case_id", f"case-{index}")
            if isinstance(case, dict)
            else f"case-{index}"
        )

        try:
            if not isinstance(case, dict):
                raise ValueError("Case must be an object")

            network = prepare_event(
                case.get("network_event")
            )

            deployment = case.get("deployment_event")

            if deployment is not None:
                deployment = prepare_event(deployment)

            event_id = network["event_id"]

            if event_id in seen_network_events:
                conflict = (
                    network != seen_network_events[event_id]
                )

                raise ValueError(
                    "Duplicate network event_id: "
                    + event_id
                    + "; conflicting_record="
                    + str(conflict)
                )

            seen_network_events[event_id] = network

            result = correlate_security_event_v2(
                network,
                deployment,
                window_seconds=args.window_seconds
            )

            results.append({
                "case_id": case_id,
                "label": case.get("label"),
                "network_event_id": event_id,
                "detection": result,
                "explanation": explain(result),
            })

        except (ValueError, TypeError) as error:
            errors.append({
                "case_id": case_id,
                "error": str(error),
            })

    alert_count = sum(
        bool(item["detection"]["alert"])
        for item in results
    )

    report = {
        "detector": "ticket012-correlation-v2",
        "dataset_type": (
            data.get("dataset_type", "unspecified")
            if isinstance(data, dict)
            else "unspecified"
        ),
        "window_seconds": args.window_seconds,
        "total_cases": len(cases),
        "processed_cases": len(results),
        "skipped_cases": len(errors),
        "alerts": alert_count,
        "results": results,
        "errors": errors,
        "limitations": [
            "Claimed identities are not independently authenticated",
            "Synthetic labels do not establish real compromise",
            "Missing telemetry can weaken correlation",
            "CLI input uses structured network/deployment event pairs"
        ],
        "status": "complete" if not errors else "partial",
    }

    try:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8"
        )
    except OSError as error:
        print("OUTPUT_ERROR=" + str(error), file=sys.stderr)
        return 1

    print("TICKET 012 - DETECTOR CLI")
    print("TOTAL_CASES=" + str(len(cases)))
    print("PROCESSED_CASES=" + str(len(results)))
    print("SKIPPED_CASES=" + str(len(errors)))
    print("ALERTS=" + str(alert_count))
    print("WINDOW_SECONDS=" + str(args.window_seconds))
    print("OUTPUT=" + str(output))
    print("PROCESSING_STATUS=" + report["status"].upper())

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
