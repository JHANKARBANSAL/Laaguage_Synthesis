"""Tests for reproducible 280-query paired evaluation; no Ollama required."""
import unittest
from unittest.mock import Mock, patch

from scripts.evaluate_local_280_paired import (
    DEFAULT_SUITE, LANGUAGES, check_ollama, direct_prompt, file_hash,
    summarize, validate_cohort,
)
from indicsql.benchmark.dataset import load_benchmark_dataset


class TestLocalPaired280(unittest.TestCase):
    def test_frozen_cohort_has_280_unique_queries_and_seven_languages(self):
        queries = load_benchmark_dataset(DEFAULT_SUITE)
        validate_cohort(queries)
        self.assertEqual(len(queries), 280)
        self.assertEqual({q.language for q in queries}, LANGUAGES)
        self.assertEqual(len(file_hash(DEFAULT_SUITE)), 64)

    def test_qwen_prompt_does_not_include_gold_sql(self):
        query = load_benchmark_dataset(DEFAULT_SUITE)[0]
        prompt = direct_prompt(query.query)
        self.assertIn(query.query, prompt)
        self.assertNotIn(query.gold_sql, prompt)
        self.assertIn("All available tables", prompt)

    @patch("scripts.evaluate_local_280_paired.httpx.get")
    def test_exact_model_required_no_silent_substitution(self, request):
        request.return_value = Mock(
            status_code=200,
            json=lambda: {"models": [{"name": "other-model", "digest": "sha256"}]},
        )
        with self.assertRaises(RuntimeError):
            check_ollama("http://localhost:11434", "qwen2.5:3b")

    def test_partial_cohort_never_gets_280_accuracy(self):
        with self.assertRaises(ValueError):
            summarize([{"query_id": "one", "language": "hi"}])

    def test_full_scoring_counts_failures_without_fake_success(self):
        rows = []
        for lang in sorted(LANGUAGES):
            for i in range(40):
                rows.append({
                    "query_id": f"{lang}-{i}",
                    "language": lang, "gold_error": None, "gold_empty": False,
                    "indicsql": {"execution_success": False, "execution_match": False,
                                 "neural_generated": False, "row_count": None},
                    "qwen_direct": {"execution_success": False, "execution_match": False,
                                    "row_count": None},
                })
        result = summarize(rows)
        self.assertEqual(result["overall"]["n"], 280)
        self.assertEqual(result["overall"]["indicsql"]["execution_matches"], 0)
        self.assertEqual(result["overall"]["qwen_direct"]["execution_matches"], 0)
