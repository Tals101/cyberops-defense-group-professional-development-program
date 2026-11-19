"""
Ticket 012 - Detector CLI Error Handling Tests

Tests the CLI using isolated temporary input and output files.
No Kubernetes changes or production connections are performed.
"""

import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CLI = (
    ROOT / "03-Detection-Engineering"
    / "src" / "detector_cli.py"
)

DATASET = (
    ROOT / "03-Detection-Engineering"
    / "synthetic-data" / "labeled-correlation-scenarios.json"
)

EVIDENCE = (
    ROOT / "07-Evidence"
    / "supporting-outputs"
    / "detector-cli-error-handling-tests.txt"
)


def sample(case_id="T01", event_id="NET-001"):
    return {
        "case_id": case_id,
        "network_event": {
            "event_id": event_id,
            "event_type": "network_request",
            "timestamp": "2026-11-12T18:14:40Z",
            "workload": "application-api",
            "destination":
                "http://unapproved-collector:8080/resource",
            "claimed_identity": "application-api",
        },
        "deployment_event": {
            "event_id": "DEP-001",
            "event_type": "deployment_change",
            "timestamp": "2026-11-12T18:12:00Z",
            "workload": "application-api",
        },
    }


class TestDetectorCLI(unittest.TestCase):

    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.folder = Path(self.workspace.name)

    def run_cli(self, payload=None, input_path=None, extra=None):
        if input_path is None:
            input_path = self.folder / "input.json"
            input_path.write_text(
                json.dumps(payload),
                encoding="utf-8"
            )

        output_path = self.folder / "output.json"

        command = [
            sys.executable,
            str(CLI),
            "--input", str(input_path),
            "--output", str(output_path),
        ]

        if extra:
            command.extend(extra)

        process = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )

        report = None

        if output_path.is_file():
            report = json.loads(
                output_path.read_text(encoding="utf-8")
            )

        return process, report

    def test_01_valid_dataset(self):
        process, report = self.run_cli(
            input_path=DATASET
        )

        self.assertEqual(process.returncode, 0)
        self.assertEqual(report["processed_cases"], 24)
        self.assertEqual(report["skipped_cases"], 0)
        self.assertEqual(report["alerts"], 17)
        self.assertEqual(report["status"], "complete")

    def test_02_custom_window(self):
        process, report = self.run_cli(
            payload=[sample()],
            extra=["--window-seconds", "60"]
        )

        self.assertEqual(process.returncode, 0)
        self.assertEqual(report["window_seconds"], 60)
        self.assertFalse(
            report["results"][0]["detection"]
            ["recent_deployment_change"]
        )
        self.assertTrue(
            report["results"][0]["detection"]["alert"]
        )

    def test_03_missing_deployment_telemetry(self):
        case = sample()
        case["deployment_event"] = None

        process, report = self.run_cli(payload=[case])

        self.assertEqual(process.returncode, 0)
        warnings = (
            report["results"][0]["detection"]
            ["telemetry_warnings"]
        )
        self.assertIn(
            "deployment_telemetry_missing", warnings
        )

    def test_04_identical_duplicate(self):
        first = sample("T01")
        second = sample("T02")

        process, report = self.run_cli(
            payload=[first, second]
        )

        self.assertEqual(process.returncode, 1)
        self.assertEqual(report["processed_cases"], 1)
        self.assertEqual(report["skipped_cases"], 1)
        self.assertIn(
            "conflicting_record=False",
            report["errors"][0]["error"]
        )

    def test_05_conflicting_duplicate(self):
        first = sample("T01")
        second = sample("T02")
        second["network_event"]["destination"] = (
            "http://internal-service:8080/resource"
        )

        process, report = self.run_cli(
            payload=[first, second]
        )

        self.assertEqual(process.returncode, 1)
        self.assertEqual(report["skipped_cases"], 1)
        self.assertIn(
            "conflicting_record=True",
            report["errors"][0]["error"]
        )

    def test_06_missing_timezone(self):
        case = sample()
        case["network_event"]["timestamp"] = (
            "2026-11-12T18:14:40"
        )

        process, report = self.run_cli(payload=[case])

        self.assertEqual(process.returncode, 1)
        self.assertEqual(report["skipped_cases"], 1)
        self.assertIn(
            "timezone",
            report["errors"][0]["error"].lower()
        )

    def test_07_missing_network_event(self):
        case = sample()
        del case["network_event"]

        process, report = self.run_cli(payload=[case])

        self.assertEqual(process.returncode, 1)
        self.assertEqual(report["skipped_cases"], 1)
        self.assertEqual(report["status"], "partial")

    def test_08_invalid_json(self):
        path = self.folder / "invalid.json"
        path.write_text(
            "{this is not valid json",
            encoding="utf-8"
        )

        process, report = self.run_cli(
            input_path=path
        )

        self.assertEqual(process.returncode, 1)
        self.assertIsNone(report)
        self.assertIn(
            "INPUT_ERROR", process.stderr
        )

    def test_09_missing_input_file(self):
        process, report = self.run_cli(
            input_path=self.folder / "does-not-exist.json"
        )

        self.assertEqual(process.returncode, 1)
        self.assertIsNone(report)
        self.assertIn(
            "INPUT_ERROR", process.stderr
        )

    def test_10_invalid_window(self):
        process, report = self.run_cli(
            payload=[sample()],
            extra=["--window-seconds", "-1"]
        )

        self.assertEqual(process.returncode, 2)
        self.assertIsNone(report)
        self.assertIn(
            "must be positive", process.stderr
        )

    def test_11_missing_required_arguments(self):
        process = subprocess.run(
            [sys.executable, str(CLI)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )

        self.assertEqual(process.returncode, 2)
        self.assertIn(
            "required", process.stderr.lower()
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        TestDetectorCLI
    )

    log = io.StringIO()

    result = unittest.TextTestRunner(
        stream=log,
        verbosity=2
    ).run(suite)

    report = (
        "TICKET 012 - DETECTOR CLI ERROR HANDLING\n"
        "Environment: Isolated synthetic tests\n\n"
        + log.getvalue()
        + "\nTESTS_EXECUTED="
        + str(result.testsRun)
        + "\nTESTS_FAILED="
        + str(len(result.failures) + len(result.errors))
        + "\nSTATUS="
        + ("PASS" if result.wasSuccessful() else "FAIL")
        + "\n"
    )

    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(report, encoding="utf-8")

    print(report)
    print("EVIDENCE_SAVED=" + str(EVIDENCE.relative_to(ROOT)))

    sys.exit(0 if result.wasSuccessful() else 1)
