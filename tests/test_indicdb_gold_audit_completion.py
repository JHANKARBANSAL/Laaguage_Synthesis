"""Independent regression checks for IndicDB gold execution audit coverage."""
import unittest

from scripts.execute_indicdb_gold import audit_completion_status


class TestGoldSQLAuditCompletion(unittest.TestCase):
    def test_complete_mapped_benchmark_no_errors(self):
        self.assertEqual(
            audit_completion_status(
                nonempty_rows=70,
                attempted_rows=70,
                execution_errors=0,
                unmapped_rows=0,
            ),
            {
                "mapped_gold_sql_execution_verified": True,
                "gold_sql_execution_verified": True,
                "all_nonempty_gold_covered": True,
            },
        )

    def test_skipped_gold_mapping_never_counts_as_full_verification(self):
        actual = audit_completion_status(
            nonempty_rows=70, attempted_rows=63, execution_errors=0, unmapped_rows=7
        )
        self.assertTrue(actual["mapped_gold_sql_execution_verified"])
        self.assertFalse(actual["gold_sql_execution_verified"])
        self.assertFalse(actual["all_nonempty_gold_covered"])

    def test_failed_reference_execution_blocks_verified_status(self):
        actual = audit_completion_status(
            nonempty_rows=70, attempted_rows=70, execution_errors=1, unmapped_rows=0
        )
        self.assertFalse(actual["mapped_gold_sql_execution_verified"])
        self.assertFalse(actual["gold_sql_execution_verified"])

    def test_zero_queries_is_not_a_success(self):
        actual = audit_completion_status(
            nonempty_rows=0, attempted_rows=0, execution_errors=0, unmapped_rows=0
        )
        self.assertFalse(actual["gold_sql_execution_verified"])

    def test_incomplete_row_accounting_is_error(self):
        with self.assertRaisesRegex(ValueError, "accounting mismatch"):
            audit_completion_status(
                nonempty_rows=70, attempted_rows=60, execution_errors=0, unmapped_rows=7
            )
