#!/usr/bin/env python3
"""Independently audit an IndicSQL sealed-run JSON receipt (no model required).

This tool never infers missing experiment results. It is NOT a substitute
for executing gold SQL or obtaining native-speaker annotations.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def wilson_interval(successes: int, total: int, z: float = 1.96) -> list[float] | None:
    if total <= 0:
        return None
    p = successes / total
    den = 1 + (z * z) / total
    center = (p + (z * z) / (2 * total)) / den
    spread = z * math.sqrt(p * (1 - p) / total + (z * z) / (4 * total * total)) / den
    return [round(100 * (center - spread), 3), round(100 * (center + spread), 3)]


def _bucket(record: dict[str, Any]) -> str:
    """Assign an exclusive, evidence-based primary outcome category."""
    if record.get("gold_error"):
        return "gold_reference_execution_error"
    if record.get("schema_route_correct") is False:
        return "incorrect_schema_route"
    if record.get("schema_route_valid") is False or not record.get("routed_schema"):
        return "invalid_or_missing_schema_route"
    if record.get("prediction_error"):
        error = str(record["prediction_error"]).lower()
        if "timeout" in error or "canceling statement" in error or "statement timeout" in error:
            return "prediction_execution_timeout"
        return "prediction_execution_error_unclassified"
    if record.get("prediction_execution_success") is False:
        return "prediction_missing_result"
    if record.get("execution_match") is True:
        if record.get("prediction_row_count") == 0 and record.get("gold_row_count") == 0:
            return "empty_result_match_requires_review"
        return "execution_match"
    if record.get("execution_match") is False:
        return "semantic_execution_mismatch"
    return "not_comparable_or_missing_status"


def audit_result(payload: dict[str, Any], expected_queries: int | None = None) -> dict[str, Any]:
    if payload.get("artifact_type") != "IndicDB sealed final evaluation":
        raise ValueError("Not an IndicDB sealed final evaluation result")
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("Missing per-question records; aggregate-only claims cannot be audited")
    if expected_queries is not None and len(records) != expected_queries:
        raise ValueError(f"Expected {expected_queries} records; found {len(records)}")
    if payload.get("selected_question_count") != len(records):
        raise ValueError("Selected question count differs from recorded rows")

    ids = [r.get("record_id") for r in records]
    if any(not isinstance(r, dict) for r in records) or any(not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("Missing or duplicate opaque per-question record IDs")

    languages: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record.get("execution_match") is True and record.get("prediction_error"):
            raise ValueError(f"Contradictory execution match and prediction error: {record['record_id']}")
        languages[str(record.get("language", "unknown"))].append(record)

    def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
        n = len(rows)
        schema_valid = sum(r.get("schema_route_valid") is True for r in rows)
        schema_correct = sum(r.get("schema_route_correct") is True for r in rows)
        execution_ok = sum(r.get("prediction_execution_success") is True for r in rows)
        matches = sum(r.get("execution_match") is True for r in rows)
        comparable = sum(r.get("execution_match") is not None for r in rows)
        empty_matches = sum(
            r.get("execution_match") is True
            and r.get("prediction_row_count") == 0
            and r.get("gold_row_count") == 0
            for r in rows
        )
        return {
            "n": n, "valid_schema_names": schema_valid, "correct_schema_routes": schema_correct,
            "prediction_execution_success": execution_ok, "execution_matches": matches,
            "comparable": comparable, "empty_result_matches": empty_matches,
            "schema_routing_accuracy_pct": round(100 * schema_correct / n, 3) if n else None,
            "execution_success_pct": round(100 * execution_ok / n, 3) if n else None,
            "execution_match_pct_all": round(100 * matches / n, 3) if n else None,
            "execution_match_pct_comparable": round(100 * matches / comparable, 3) if comparable else None,
            "wilson_95pct_for_all_ex": wilson_interval(matches, n),
            "outcome_categories": dict(Counter(_bucket(r) for r in rows)),
        }

    return {
        "source_artifact": payload["artifact_type"],
        "lock_sha256": payload.get("lock_sha256"),
        "selected_question_count": len(records),
        "overall": metrics(records),
        "per_language": {k: metrics(v) for k, v in sorted(languages.items())},
        "warnings": [
            "Metrics are recomputed from saved records; source predictions and PostgreSQL results were not independently rerun.",
            "Wrong-schema classification requires the route_correct field from the fixed evaluator.",
            "Identifier hallucinations cannot be proven from error strings alone.",
            "Empty-result matches and gold-reference defects require separate manual review.",
            "A saved result without a matching SHA-256 receipt and model/data lock is not a reproduced experiment.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("--expected-queries", type=int, default=280)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    raw = json.loads(args.results.read_text(encoding="utf-8"))
    report = audit_result(raw, args.expected_queries)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
