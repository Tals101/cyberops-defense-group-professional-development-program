import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from correlation_detector import (
    normalize_timestamp,
    prepare_event,
    deduplicate_events,
    classify_destination,
    classify_identity,
    correlate_deployment_change,
    correlate_security_event,
)


class TestCorrelationDetector(unittest.TestCase):

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

    def detect(self):
        return correlate_security_event(self.network, self.deployment)

    # BENIGN SCENARIOS / FALSE-POSITIVE TESTS

    def test_01_benign_approved_after_deployment(self):
        result = self.detect()
        self.assertFalse(result["alert"])
        self.assertEqual(result["triage_level"], "none")

    def test_02_benign_approved_outside_window(self):
        self.deployment["timestamp"] = "2026-11-12T18:00:00Z"
        self.assertFalse(self.detect()["alert"])

    def test_03_benign_approved_missing_identity(self):
        del self.network["claimed_identity"]
        result = self.detect()
        self.assertEqual(result["identity_status"], "unknown")
        self.assertFalse(result["alert"])

    def test_04_benign_approved_unrelated_deployment(self):
        self.deployment["workload"] = "internal-service"
        result = self.detect()
        self.assertFalse(result["recent_deployment_change"])
        self.assertFalse(result["alert"])

    def test_05_benign_approved_before_deployment(self):
        self.network["timestamp"] = "2026-11-12T18:11:00Z"
        self.assertFalse(self.detect()["alert"])

    # SUSPICIOUS-ACTIVITY TESTS

    def test_06_unapproved_destination_generates_alert(self):
        self.network["destination"] = "http://unapproved-collector:8080/resource"
        result = self.detect()
        self.assertTrue(result["alert"])
        self.assertEqual(result["triage_level"], "review")

    def test_07_identity_mismatch_increases_priority(self):
        self.network["destination"] = "http://unapproved-collector:8080/resource"
        self.network["claimed_identity"] = "internal-service"
        result = self.detect()
        self.assertTrue(result["alert"])
        self.assertEqual(result["identity_status"], "mismatch")
        self.assertEqual(result["triage_level"], "high")

    def test_08_unapproved_with_unknown_identity(self):
        self.network["destination"] = "http://unapproved-collector:8080/resource"
        del self.network["claimed_identity"]
        result = self.detect()
        self.assertTrue(result["alert"])
        self.assertEqual(result["triage_level"], "review")

    # CURRENT RULE LIMITATIONS

    def test_09_unapproved_outside_window_not_correlated(self):
        self.network["destination"] = "http://unapproved-collector:8080/resource"
        self.deployment["timestamp"] = "2026-11-12T18:00:00Z"
        result = self.detect()
        self.assertEqual(result["destination_status"], "unapproved")
        self.assertFalse(result["alert"])

    def test_10_unapproved_before_deployment_not_correlated(self):
        self.network["destination"] = "http://unapproved-collector:8080/resource"
        self.network["timestamp"] = "2026-11-12T18:11:00Z"
        self.assertFalse(self.detect()["alert"])

    def test_11_unapproved_unrelated_deployment(self):
        self.network["destination"] = "http://unapproved-collector:8080/resource"
        self.deployment["workload"] = "internal-service"
        self.assertFalse(self.detect()["alert"])

    # UNKNOWN AND MISSING TELEMETRY

    def test_12_unknown_workload(self):
        self.network["workload"] = "unknown-application"
        self.deployment["workload"] = "unknown-application"
        result = self.detect()
        self.assertEqual(result["destination_status"], "unknown")
        self.assertFalse(result["alert"])

    def test_13_missing_destination(self):
        del self.network["destination"]
        result = self.detect()
        self.assertEqual(result["destination_status"], "unknown")
        self.assertFalse(result["alert"])

    def test_14_invalid_network_event_type(self):
        self.network["event_type"] = "authentication"
        with self.assertRaises(ValueError):
            self.detect()

    def test_15_invalid_deployment_event_type(self):
        self.deployment["event_type"] = "authentication"
        result = self.detect()
        self.assertFalse(result["recent_deployment_change"])

    # TIME-WINDOW BOUNDARIES

    def test_16_exactly_five_minutes(self):
        self.network["timestamp"] = "2026-11-12T18:17:00Z"
        self.assertTrue(
            correlate_deployment_change(self.network, self.deployment)
        )

    def test_17_more_than_five_minutes(self):
        self.network["timestamp"] = "2026-11-12T18:17:01Z"
        self.assertFalse(
            correlate_deployment_change(self.network, self.deployment)
        )

    # TIMESTAMP VALIDATION

    def test_18_timezone_conversion(self):
        result = normalize_timestamp("2026-11-12T13:14:40-05:00")
        self.assertEqual(result.isoformat(), "2026-11-12T18:14:40+00:00")

    def test_19_utc_timestamp(self):
        result = normalize_timestamp("2026-11-12T18:14:40Z")
        self.assertEqual(result.isoformat(), "2026-11-12T18:14:40+00:00")

    def test_20_missing_timezone_rejected(self):
        with self.assertRaises(ValueError):
            normalize_timestamp("2026-11-12T18:14:40")

    def test_21_malformed_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            normalize_timestamp("invalid-timestamp")

    # REQUIRED EVENT FIELDS

    def test_22_missing_event_id(self):
        del self.network["event_id"]
        with self.assertRaises(ValueError):
            prepare_event(self.network)

    def test_23_missing_event_type(self):
        del self.network["event_type"]
        with self.assertRaises(ValueError):
            prepare_event(self.network)

    def test_24_missing_timestamp(self):
        del self.network["timestamp"]
        with self.assertRaises(ValueError):
            prepare_event(self.network)

    def test_25_event_timestamp_normalization(self):
        self.network["timestamp"] = "2026-11-12T13:14:40-05:00"
        result = prepare_event(self.network)
        self.assertEqual(result["timestamp"], "2026-11-12T18:14:40Z")

    # DUPLICATE EVENT HANDLING

    def test_26_identical_duplicates(self):
        result = deduplicate_events([self.network, dict(self.network)])
        self.assertEqual(len(result["events"]), 1)
        self.assertFalse(result["duplicates"][0]["conflict"])

    def test_27_conflicting_duplicates(self):
        altered = dict(self.network)
        altered["workload"] = "different-application"
        result = deduplicate_events([self.network, altered])
        self.assertEqual(len(result["events"]), 1)
        self.assertTrue(result["duplicates"][0]["conflict"])

    def test_28_invalid_duplicate_input(self):
        with self.assertRaises(ValueError):
            deduplicate_events("not-a-list")

    # IDENTITY CLASSIFICATION

    def test_29_matching_identity(self):
        self.assertEqual(classify_identity(self.network), "matched")

    def test_30_mismatched_identity(self):
        self.network["claimed_identity"] = "internal-service"
        self.assertEqual(classify_identity(self.network), "mismatch")

    def test_31_missing_identity(self):
        del self.network["claimed_identity"]
        self.assertEqual(classify_identity(self.network), "unknown")


if __name__ == "__main__":
    unittest.main()
