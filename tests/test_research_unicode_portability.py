"""Regression tests for Indic UTF-8 and sealed audit accounting on Windows/Linux."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_indicdb_run import audit_result


class TestUnicodeAndResearchAuditor(unittest.TestCase):
    def test_native_scripts_json_roundtrip_explicit_utf8(self):
        examples = {
            "hi": "बिहार में कितने किसान हैं?",
            "mr": "महाराष्ट्रात किती शेतकरी आहेत?",
            "bn": "পশ্চিমবঙ্গে কতজন কৃষক আছেন?",
            "ta": "தமிழ்நாட்டில் எத்தனை விவசாயிகள் உள்ளனர்?",
            "te": "తెలంగాణలో ఎంతమంది రైతులు ఉన్నారు?",
            "hi-en": "Bihar mein kitne farmers hain?",
        }
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "indic.json"
            file.write_text(json.dumps(examples, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(json.loads(file.read_text(encoding="utf-8")), examples)

    def test_audit_never_misreports_missing_routing_as_zero_percent(self):
        payload = {
            "artifact_type": "IndicDB sealed final evaluation",
            "selected_question_count": 1,
            "records": [{
                "record_id": "opaque-1", "language": "hi",
                "routed_schema": "INDIA_X",
                "prediction_row_count": 0, "gold_row_count": 0,
                "execution_match": True,
            }],
        }
        report = audit_result(payload, expected_queries=1)
        self.assertIsNone(report["overall"]["schema_routing_accuracy_pct"])
        self.assertIsNone(report["overall"]["execution_success_pct"])
        self.assertEqual(report["overall"]["empty_result_matches"], 1)
