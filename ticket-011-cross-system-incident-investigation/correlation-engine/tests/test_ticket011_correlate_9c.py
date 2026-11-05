#!/usr/bin/env python3
"""Ticket 011: isolated correlation-engine unit tests."""

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest

from pathlib import Path


ROOT = Path(sys.argv[1]).resolve()
TEST_DIR = ROOT / "correlation-engine" / "tests"
ENGINE = ROOT / "correlation-engine" / "src" / "ticket011_correlate.py"
DATA = ROOT / "correlation-engine" / "sample-data"

spec = importlib.util.spec_from_file_location(
    "ticket011_correlate", ENGINE
)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


def event(key, system, time, source="", destination=""):
    return {
        "event_key": key,
        "system": system,
        "source_id": system + "_TEST",
        "time_utc": time,
        "source_ip": source,
        "destination_ip": destination,
    }


class CorrelationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(
            (DATA / "source-schema-audit-9a.json").read_text(
                encoding="utf-8-sig"
            )
        )
        cls.expected = {
            item["SourceID"]: item
            for item in cls.audit["Sources"]
        }

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(
            prefix="ticket011-test-9c-",
            dir=str(TEST_DIR)
        )
        self.addCleanup(self.temp.cleanup)
        self.fixture_path = Path(self.temp.name) / "fixture.jsonl"

    def fixture(self, records):
        content = "".join(
            json.dumps(record) + "\n"
            for record in records
        )
        self.fixture_path.write_text(
            content, encoding="utf-8"
        )
        reference = {
            "TEST": {
                "RelativePath": "fixture.jsonl",
                "SHA256": hashlib.sha256(
                    self.fixture_path.read_bytes()
                ).hexdigest(),
                "RecordCount": len(records),
            }
        }
        specification = (
            "TEST", "AWS", "fixture.jsonl", len(records)
        )
        return specification, reference

    @staticmethod
    def sample_record():
        return {
            "eventID": "synthetic-test-01",
            "eventTime": "2026-11-02T13:00:00Z",
            "sourceSystem": "aws-cloudtrail-synthetic",
            "datasetType": "SYNTHETIC",
            "eventName": "GetCallerIdentity",
            "outcome": "SUCCESS",
            "sourceIPAddress": "203.0.113.77",
            "userIdentity": {"userName": "test-user"},
        }

    def test_01_all_source_counts_and_hashes(self):
        self.assertEqual(
            self.audit["Classification"],
            "SYNTHETIC_SOURCE_SCHEMA_AUDIT"
        )
        self.assertEqual(len(engine.SOURCES), 7)
        total = 0

        for entry in engine.SOURCES:
            rows = engine.read_source(
                ROOT, entry, self.expected
            )
            self.assertEqual(len(rows), entry[3])
            total += len(rows)

        self.assertEqual(total, 42)

    def test_02_original_references_preserved(self):
        for entry in engine.SOURCES:
            rows = engine.read_source(
                ROOT, entry, self.expected
            )

            for record in rows:
                self.assertTrue(record["raw_event_id"])
                self.assertTrue(record["raw_timestamp"])
                self.assertGreaterEqual(
                    record["source_line"], 1
                )
                self.assertEqual(
                    record["evidence_class"],
                    "SYNTHETIC_RECORD"
                )
                self.assertEqual(
                    record["source_id"], entry[0]
                )

    def test_03_saved_normalization_integrity(self):
        path = DATA / "normalized-events-9b.jsonl"
        records = [
            json.loads(line)
            for line in path.read_text(
                encoding="utf-8"
            ).splitlines()
        ]

        self.assertEqual(len(records), 42)
        self.assertEqual(
            len({r["event_key"] for r in records}), 42
        )
        self.assertEqual(
            {r["system"] for r in records},
            {"AWS", "KUBERNETES", "LINUX"}
        )

        for record in records:
            self.assertEqual(
                record["evidence_class"], "SYNTHETIC_RECORD"
            )
            self.assertTrue(
                record["source_sha256"]
            )
            engine.parse_utc(record["time_utc"])

    def test_04_saved_association_safety(self):
        result = json.loads(
            (DATA / "ip-associations-9b.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(
            result["classification"],
            "SYNTHETIC_ONLY_ASSOCIATIONS"
        )
        self.assertEqual(result["source_event_count"], 42)
        self.assertEqual(result["shared_ip_count"], 2)
        self.assertEqual(result["temporal_pair_count"], 37)
        self.assertIs(
            result["causation_established"], False
        )

        for group in result["shared_ip_groups"]:
            self.assertIs(
                group["causation_established"], False
            )

        for pair in result["temporal_pairs"]:
            self.assertIs(
                pair["causation_established"], False
            )
            self.assertGreaterEqual(
                pair["delta_seconds"], 0
            )
            self.assertLessEqual(
                pair["delta_seconds"], 300
            )

    def test_05_correlations_reproduce(self):
        records = []

        for entry in engine.SOURCES:
            records.extend(
                engine.read_source(
                    ROOT, entry, self.expected
                )
            )

        groups, pairs = engine.associate(records)
        saved = json.loads(
            (DATA / "ip-associations-9b.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(groups, saved["shared_ip_groups"])
        self.assertEqual(pairs, saved["temporal_pairs"])

    def test_06_case_sensitive_field_variants(self):
        self.assertEqual(
            engine.field(
                {"eventID": "AWS-ID"},
                "eventID", "eventId"
            ),
            "AWS-ID"
        )
        self.assertEqual(
            engine.field(
                {"eventId": "LINUX-ID"},
                "eventID", "eventId"
            ),
            "LINUX-ID"
        )
        self.assertEqual(
            engine.field(
                {"sourceIP": "203.0.113.77"},
                "sourceIPAddress", "sourceIP", "sourceIp"
            ),
            "203.0.113.77"
        )
        self.assertEqual(
            engine.field(
                {"sourceIp": "192.0.2.58"},
                "sourceIPAddress", "sourceIP", "sourceIp"
            ),
            "192.0.2.58"
        )

    def test_07_nested_cloudtrail_actor(self):
        self.assertEqual(
            engine.actor_of({
                "userIdentity": {
                    "userName": "svc-reporting-automation"
                }
            }),
            "svc-reporting-automation"
        )
        self.assertEqual(
            engine.actor_of({"actor": "ops-runner"}),
            "ops-runner"
        )

    def test_08_utc_timestamp_validation(self):
        valid = engine.parse_utc(
            "2026-11-02T13:00:00Z"
        )
        self.assertEqual(
            valid.isoformat(),
            "2026-11-02T13:00:00+00:00"
        )

        for bad in (
            "2026-11-02T13:00:00",
            "2026-11-02T13:00:00+00:00",
            "not-a-timestamp"
        ):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    engine.parse_utc(bad)

    def test_09_invalid_ips_excluded(self):
        self.assertEqual(
            engine.valid_ip("999.999.999.999"), ""
        )
        self.assertEqual(
            engine.valid_ip("not-an-ip"), ""
        )
        self.assertEqual(
            engine.valid_ip("203.0.113.77"),
            "203.0.113.77"
        )

    def test_10_source_destination_roles(self):
        records = [
            event(
                "aws:a", "AWS",
                "2026-11-02T13:00:00Z",
                source="203.0.113.77"
            ),
            event(
                "linux:b", "LINUX",
                "2026-11-02T13:01:00Z",
                destination="203.0.113.77"
            ),
        ]

        groups, pairs = engine.associate(records)

        self.assertEqual(len(groups), 1)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(
            {p["role"] for p in groups[0]["members"]},
            {"source", "destination"}
        )
        self.assertEqual(
            pairs[0]["delta_seconds"], 60
        )
        self.assertFalse(
            pairs[0]["causation_established"]
        )

    def test_11_five_minute_boundary_included(self):
        records = [
            event(
                "a", "AWS",
                "2026-11-02T13:00:00Z",
                source="203.0.113.77"
            ),
            event(
                "b", "LINUX",
                "2026-11-02T13:05:00Z",
                source="203.0.113.77"
            ),
        ]

        groups, pairs = engine.associate(records)
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(
            pairs[0]["delta_seconds"], 300
        )

    def test_12_outside_time_window_excluded(self):
        records = [
            event(
                "a", "AWS",
                "2026-11-02T13:00:00Z",
                source="203.0.113.77"
            ),
            event(
                "b", "LINUX",
                "2026-11-02T13:05:01Z",
                source="203.0.113.77"
            ),
        ]

        groups, pairs = engine.associate(records)
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(pairs), 0)

    def test_13_same_system_not_cross_correlated(self):
        records = [
            event(
                "a", "AWS",
                "2026-11-02T13:00:00Z",
                source="203.0.113.77"
            ),
            event(
                "b", "AWS",
                "2026-11-02T13:01:00Z",
                source="203.0.113.77"
            ),
        ]

        groups, pairs = engine.associate(records)
        self.assertEqual(groups, [])
        self.assertEqual(pairs, [])

    def test_14_different_ips_not_correlated(self):
        records = [
            event(
                "a", "AWS",
                "2026-11-02T13:00:00Z",
                source="203.0.113.77"
            ),
            event(
                "b", "LINUX",
                "2026-11-02T13:00:00Z",
                source="203.0.113.88"
            ),
        ]

        groups, pairs = engine.associate(records)
        self.assertEqual(groups, [])
        self.assertEqual(pairs, [])

    def test_15_tampered_source_hash_rejected(self):
        spec, expected = self.fixture([
            self.sample_record()
        ])

        with self.fixture_path.open(
            "a", encoding="utf-8"
        ) as output:
            output.write(" ")

        with self.assertRaisesRegex(
            ValueError, "SHA256 changed"
        ):
            engine.read_source(
                Path(self.temp.name), spec, expected
            )

    def test_16_missing_event_id_rejected(self):
        record = self.sample_record()
        record.pop("eventID")

        spec, expected = self.fixture([record])

        with self.assertRaisesRegex(
            ValueError, "Missing/duplicate event ID"
        ):
            engine.read_source(
                Path(self.temp.name), spec, expected
            )

    def test_17_duplicate_event_id_rejected(self):
        record = self.sample_record()
        spec, expected = self.fixture([
            record, dict(record)
        ])

        with self.assertRaisesRegex(
            ValueError, "Missing/duplicate event ID"
        ):
            engine.read_source(
                Path(self.temp.name), spec, expected
            )

    def test_18_wrong_provenance_rejected(self):
        record = self.sample_record()
        record["datasetType"] = "ACTUAL_MINIKUBE_LAB"

        spec, expected = self.fixture([record])

        with self.assertRaisesRegex(
            ValueError, "provenance mismatch"
        ):
            engine.read_source(
                Path(self.temp.name), spec, expected
            )

    def test_19_invalid_timestamp_rejected(self):
        record = self.sample_record()
        record["eventTime"] = "2026-11-02T13:00:00"

        spec, expected = self.fixture([record])

        with self.assertRaises(ValueError):
            engine.read_source(
                Path(self.temp.name), spec, expected
            )

    def test_20_source_path_mismatch_rejected(self):
        spec, expected = self.fixture([
            self.sample_record()
        ])

        expected["TEST"]["RelativePath"] = "wrong.jsonl"

        with self.assertRaisesRegex(
            ValueError, "Schema audit path changed"
        ):
            engine.read_source(
                Path(self.temp.name), spec, expected
            )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        CorrelationTests
    )
    result = unittest.TextTestRunner(
        stream=sys.stdout,
        verbosity=2
    ).run(suite)

    print(
        "Tests executed: {}".format(result.testsRun)
    )
    print(
        "Failures: {}".format(len(result.failures))
    )
    print(
        "Errors: {}".format(len(result.errors))
    )

    if result.wasSuccessful() and result.testsRun == 20:
        print("STEP 9C PYTHON: PASS")
        sys.exit(0)

    print("STEP 9C PYTHON: NOT PASSED")
    sys.exit(1)