"""Control-level tests for architecture ablation switches (not accuracy measurements)."""
import unittest
from unittest.mock import patch

from indicsql.graph.workflow import execute_indicsql_pipeline


SCHEMA = {
    "dialect": "postgres",
    "schema_name": "sample",
    "tables": {
        "dim_district": {
            "columns": {"district_name": "text"},
            "foreign_keys": [],
        },
        "fact_unrelated": {
            "columns": {"unrelated_metric": "bigint"},
            "foreign_keys": [],
        },
    },
}


class Sandbox:
    def execute_query(self, query, schema_name):
        return {
            "columns": ["district_name"], "rows": [["Guntur"]],
            "row_count": 1, "execution_time_ms": 1.0,
        }


class TestAblationControl(unittest.TestCase):
    def test_full_catalog_mode_is_visible_to_synthesizer(self):
        observed = []

        def synthesize(state):
            observed.append(set(state["database_schema"]["tables"]))
            return {"generated_sql": "SELECT district_name FROM dim_district"}

        with patch("indicsql.graph.workflow.sql_synthesizer_node", side_effect=synthesize):
            full = execute_indicsql_pipeline(
                "List district names", database_schema=SCHEMA,
                database_schema_name="sample", sandbox=Sandbox(),
                ablation_full_catalog=True,
            )
            pruned = execute_indicsql_pipeline(
                "List district names", database_schema=SCHEMA,
                database_schema_name="sample", sandbox=Sandbox(),
            )

        self.assertEqual(observed[0], set(SCHEMA["tables"]))
        self.assertEqual(observed[1], {"dim_district"})
        self.assertEqual(full["execution_result"]["row_count"], 1)
        self.assertEqual(pruned["execution_result"]["row_count"], 1)

    def test_no_critic_skips_critic_but_keeps_executor_ast_guard(self):
        with patch("indicsql.graph.workflow.sql_synthesizer_node",
                   return_value={"generated_sql": "DELETE FROM dim_district"}), \
             patch("indicsql.graph.workflow.critic_node",
                   side_effect=AssertionError("Critic must be bypassed")):
            result = execute_indicsql_pipeline(
                "List district names", database_schema=SCHEMA,
                database_schema_name="sample", sandbox=Sandbox(),
                ablation_no_critic=True, max_reflections=0,
            )
        self.assertIsNone(result.get("execution_result"))
        self.assertTrue(result.get("execution_error"))
        self.assertFalse(result.get("syntax_valid"))
        self.assertEqual(len(result["ablation_attempt_history"]), 1)
        self.assertFalse(result["ablation_attempt_history"][0]["executed"])

    def test_combined_full_catalog_no_critic_no_repair(self):
        with patch("indicsql.graph.workflow.sql_synthesizer_node",
                   return_value={"generated_sql": "SELECT district_name FROM dim_district"}), \
             patch("indicsql.graph.workflow.critic_node",
                   side_effect=AssertionError("Critic must be bypassed")):
            result = execute_indicsql_pipeline(
                "List district names", database_schema=SCHEMA,
                database_schema_name="sample", sandbox=Sandbox(),
                ablation_full_catalog=True, ablation_no_critic=True,
                max_reflections=0,
            )
        self.assertEqual(len(result["ablation_attempt_history"]), 1)
        self.assertTrue(result["ablation_attempt_history"][0]["executed"])

    def test_full_catalog_requires_explicit_schema(self):
        with self.assertRaises(ValueError):
            execute_indicsql_pipeline("List district names", ablation_full_catalog=True)


if __name__ == "__main__":
    unittest.main()
