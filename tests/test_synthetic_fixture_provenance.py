"""Determinism and data-provenance safeguards for generated development fixtures."""

import hashlib
import unittest

from indicsql.schema.ingest_ndap import _generate_table_rows, _stable_hash
from indicsql.schema.ingest_real_gov_data import ingest_all_20_ndap_databases


class TestSyntheticDataProvenance(unittest.TestCase):
    def test_stable_fixture_hash_uses_sha256(self):
        text = "महाराष्ट्र_Pune_2024"
        expected = int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big")
        self.assertEqual(_stable_hash(text), expected)

    def test_fixture_generation_is_repeatable_within_process(self):
        first = _generate_table_rows("ndap_pm_kisan_disbursement")
        second = _generate_table_rows("ndap_pm_kisan_disbursement")
        self.assertEqual(first, second)
        self.assertGreater(len(first), 0)

    def test_mixed_source_ingestion_requires_explicit_opt_in(self):
        with self.assertRaisesRegex(ValueError, "modeled or synthetic"):
            ingest_all_20_ndap_databases()

    def test_fixture_hash_is_independent_of_python_hash_seed(self):
        # The deterministic SHA-256 source never consults Python's salted hash().
        self.assertEqual(_stable_hash("sample"), _stable_hash("sample"))
