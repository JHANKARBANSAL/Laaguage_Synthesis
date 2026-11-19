#!/usr/bin/env python3
"""Compare two genuine saved IndicSQL benchmark runs on an identical paired cohort.

This does not execute an LLM or fabricate baseline results. Cohort, language,
database lock, receipt SHA-256 and row-level outcomes must be present. Use this
for controlled baseline/ablation analysis, not cross-benchmark comparisons.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from scripts.audit_indicdb_run import verify_receipt


def _records(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = payload.get("records")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Both runs require nonempty per-item outcomes")
    if len(rows) != payload.get("selected_question_count"):
        raise ValueError("Result count does not match selected_question_count")
    ids: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("record_id"), str):
            raise ValueError("Invalid record")
        if row["record_id"] in ids:
            raise ValueError("Duplicate opaque record ID")
        if not isinstance(row.get("execution_match"), bool):
            raise ValueError("Unscored or gold-error case: resolve before matched EX comparison")
        if row.get("gold_error"):
            raise ValueError("Gold-reference errors require a separately audited comparable cohort")
        ids[row["record_id"]] = row
    return ids


def exact_mcnemar_p(b: int, c: int) -> float:
    """Two-sided exact McNemar binomial p-value, no scipy dependency."""
    n = b + c
    if not n:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(min(b, c) + 1))
    return min(1.0, 2.0 * tail / (2 ** n))


def compare_runs(base: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    if base.get("artifact_type") != candidate.get("artifact_type"):
        raise ValueError("Runs have different artifact types")
    if not base.get("lock_sha256") or not candidate.get("lock_sha256"):
        raise ValueError("Missing experiment lock SHA-256")
    if base.get("lock_sha256") != candidate.get("lock_sha256"):
        raise ValueError(
            "Run locks differ: do not compare as a controlled ablation without a "
            "separate validated shared-cohort/model/data manifest"
        )
    if base.get("experiment_variant") == candidate.get("experiment_variant"):
        raise ValueError("Comparison requires different named experiment variants")
    if base.get("statement_timeout_ms") != candidate.get("statement_timeout_ms"):
        raise ValueError("Statement timeouts differ between compared runs")
    a, b = _records(base), _records(candidate)
    if set(a) != set(b):
        raise ValueError("Different query cohorts: cannot compare matched EX")
    base_success = candidate_success = base_only = candidate_only = 0
    by_lang: dict[str, dict[str, int]] = {}
    for key in sorted(a):
        left, right = a[key], b[key]
        if left.get("language") != right.get("language"):
            raise ValueError("Language differs for paired item " + key)
        lang = str(left.get("language"))
        row = by_lang.setdefault(lang, {"total": 0, "baseline_matches": 0, "candidate_matches": 0})
        row["total"] += 1
        x = left["execution_match"]
        y = right["execution_match"]
        base_success += int(x)
        candidate_success += int(y)
        row["baseline_matches"] += int(x)
        row["candidate_matches"] += int(y)
        base_only += int(x and not y)
        candidate_only += int(y and not x)
    total = len(a)
    return {
        "artifact_type": "IndicSQL verified paired execution-match comparison",
        "same_cohort": True,
        "same_experiment_lock": True,
        "baseline_variant": base.get("experiment_variant"),
        "candidate_variant": candidate.get("experiment_variant"),
        "paired_queries": total,
        "baseline_execution_matches": base_success,
        "candidate_execution_matches": candidate_success,
        "baseline_ex_pct": round(100 * base_success / total, 3),
        "candidate_ex_pct": round(100 * candidate_success / total, 3),
        "candidate_minus_baseline_percentage_points": round(100 * (candidate_success-base_success) / total, 3),
        "baseline_only_correct": base_only,
        "candidate_only_correct": candidate_only,
        "mcnemar_exact_two_sided_p": exact_mcnemar_p(base_only, candidate_only),
        "per_language": by_lang,
        "limitation": "Only saved execution outcomes compared. Same lock forbids arbitrary cross-model comparisons; native-language semantics remain unverified.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--baseline-receipt", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--candidate-receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    verify_receipt(args.baseline, args.baseline_receipt, baseline)
    verify_receipt(args.candidate, args.candidate_receipt, candidate)
    result = compare_runs(baseline, candidate)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Verified paired comparison written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
