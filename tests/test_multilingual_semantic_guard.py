"""Multilingual question/metric guard regressions for IndicSQL (five scripts)."""

import unittest

from indicsql.agents.semantic_guard import extract_query_concepts, metric_mismatch_reason
from indicsql.agents.schema_linker import schema_linker_node


CASES = {
    "en": "How many farmers in Bihar are literate?",
    "hi": "बिहार में कितने किसान साक्षर हैं?",
    "mr": "बिहारमध्ये किती शेतकरी साक्षर आहेत?",
    "bn": "বিহারে কতজন কৃষক সাক্ষর?",
    "ta": "பீகாரில் எத்தனை விவசாயிகள் எழுத்தறிவு பெற்றவர்கள்?",
    "te": "బీహార్‌లో ఎంతమంది రైతులు అక్షరాస్యులు?",
}


class SemanticGuardTests(unittest.TestCase):
    def test_farmer_and_literacy_recognized_in_six_languages(self):
        for language, question in CASES.items():
            with self.subTest(language=language):
                concepts = extract_query_concepts(question)
                self.assertIn("farmer", concepts)
                self.assertIn("literacy", concepts)

    def test_missing_joint_statistic_fails_before_sql_generation(self):
        for language, question in CASES.items():
            with self.subTest(language=language):
                result = schema_linker_node({
                    "raw_query": question, "canonical_query": question,
                    "detected_lang": language, "audit_trace": [],
                })
                self.assertIn("does not record literacy status", result["schema_linking_error"])
                self.assertEqual(result["target_database"], "")

    def test_wrong_beneficiary_sql_is_blocked(self):
        question = CASES["te"]
        sql = ("SELECT SUM(farmer_beneficiaries) "
               "FROM ndap_pm_kisan_disbursement;")
        reason = metric_mismatch_reason(question, sql)
        self.assertIsNotNone(reason)
        self.assertIn("literacy", reason)

    def test_correct_literacy_sql_is_not_rejected(self):
        sql = ("SELECT district_name, female_literacy_rate "
               "FROM ndap_education_stats LIMIT 5;")
        self.assertIsNone(metric_mismatch_reason(
            "Which districts have the highest female literacy rate?", sql
        ))

    def test_gender_specific_guard(self):
        wrong = ("SELECT district_name, male_literacy_rate "
                 "FROM ndap_education_stats LIMIT 5;")
        self.assertIn("female", metric_mismatch_reason(
            "Which districts have the highest female literacy rate?", wrong
        ))

    def test_unsupported_metric_is_not_force_guessed(self):
        # Unknown topics do not get a fabricated metric classification.
        self.assertIsNone(metric_mismatch_reason(
            "What is the orbital velocity of Neptune?",
            "SELECT district_name FROM ndap_education_stats LIMIT 5;",
        ))

    def test_beneficiary_metric_must_match(self):
        sql = "SELECT amount_inr FROM ndap_pm_kisan_disbursement LIMIT 5;"
        self.assertIn("beneficiaries", metric_mismatch_reason(
            "Show PM KISAN farmer beneficiaries", sql
        ))


if __name__ == "__main__":
    unittest.main()
