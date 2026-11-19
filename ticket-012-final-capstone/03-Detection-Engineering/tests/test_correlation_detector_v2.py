import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from correlation_detector_v2 import correlate_security_event_v2


class TestCorrelationDetectorV2(unittest.TestCase):

    def setUp(self):
        self.deployment = {
            "event_id": "D001",
            "event_type": "deployment_change",
            "timestamp": "2026-11-12T18:12:00Z",
            "workload": "application-api",
        }
        self.network = {
            "event_id": "N001",
            "event_type": "network_request",
            "timestamp": "2026-11-12T18:14:40Z",
            "workload": "application-api",
            "destination": "http://internal-service:8080/resource",
            "claimed_identity": "application-api",
        }

    def test_v2_01_approved_traffic(self):
        result = correlate_security_event_v2(self.network, self.deployment)
        self.assertFalse(result["alert"])

    def test_v2_02_unapproved_traffic(self):
        self.network["destination"] = "http://unapproved-collector:8080/resource"
        result = correlate_security_event_v2(self.network, self.deployment)
        self.assertTrue(result["alert"])
        self.assertEqual(result["triage_level"], "elevated")

    def test_v2_03_unapproved_without_recent_change(self):
        self.network["destination"] = "http://unapproved-collector:8080/resource"
        self.deployment["timestamp"] = "2026-11-12T18:00:00Z"
        result = correlate_security_event_v2(self.network, self.deployment)
        self.assertTrue(result["alert"])
        self.assertEqual(result["triage_level"], "review")

    def test_v2_04_unapproved_without_deployment_telemetry(self):
        self.network["destination"] = "http://unapproved-collector:8080/resource"
        result = correlate_security_event_v2(self.network)
        self.assertTrue(result["alert"])
        self.assertIn("deployment_telemetry_missing", result["telemetry_warnings"])

    def test_v2_05_identity_mismatch(self):
        self.network["claimed_identity"] = "internal-service"
        result = correlate_security_event_v2(self.network, self.deployment)
        self.assertTrue(result["alert"])
        self.assertIn("claimed_identity_mismatch", result["reasons"])

    def test_v2_06_high_priority_correlation(self):
        self.network["destination"] = "http://unapproved-collector:8080/resource"
        self.network["claimed_identity"] = "internal-service"
        result = correlate_security_event_v2(self.network, self.deployment)
        self.assertEqual(result["triage_level"], "high")

    def test_v2_07_unknown_workload(self):
        self.network["workload"] = "unknown-application"
        result = correlate_security_event_v2(self.network, self.deployment)
        self.assertTrue(result["alert"])
        self.assertIn("workload_not_in_policy", result["reasons"])

    def test_v2_08_missing_identity_warning(self):
        del self.network["claimed_identity"]
        result = correlate_security_event_v2(self.network, self.deployment)
        self.assertFalse(result["alert"])
        self.assertIn("identity_telemetry_incomplete", result["telemetry_warnings"])

    def test_v2_09_invalid_event_type(self):
        self.network["event_type"] = "authentication"
        with self.assertRaises(ValueError):
            correlate_security_event_v2(self.network, self.deployment)


if __name__ == "__main__":
    unittest.main()
