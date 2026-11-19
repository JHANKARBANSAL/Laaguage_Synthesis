#!/usr/bin/env python3
"""Merge seven real 40-question paired-run shards into a verified 280 report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.evaluate_local_280_paired import LANGUAGES, summarize


def combine(shards: list[dict]) -> dict:
    if len(shards) != 7:
        raise ValueError("Expected exactly seven independently executed 40-case shards")
    first = shards[0]["metadata"]
    common = ("artifact_type", "official_indicdb_score", "held_out",
              "local_development_informed_suite", "model", "model_digest",
              "suite_sha256", "data_sha256", "comparison")
    ranges = set()
    all_rows = []
    for shard in shards:
        meta = shard["metadata"]
        for key in common:
            if meta[key] != first[key]:
                raise ValueError(f"Mismatched shard {key}: abort comparison")
        pair = (meta["start"], meta["end"])
        if pair in ranges or pair[1] - pair[0] != 39:
            raise ValueError("Duplicate or non-40-query shard")
        ranges.add(pair)
        if len(shard["records"]) != 40:
            raise ValueError("Incomplete shard cannot be merged")
        if any(row["qwen_direct"].get("inference_completed") is not True for row in shard["records"]):
            raise ValueError("Qwen was not executed on every item")
        all_rows.extend(shard["records"])
    if ranges != {(start, start + 39) for start in range(1, 281, 40)}:
        raise ValueError("Shards fail to cover indices 1 through 280 exactly")
    if len(all_rows) != 280 or len({row["query_id"] for row in all_rows}) != 280:
        raise ValueError("Duplicate or missing paired queries")
    metrics = summarize(all_rows)
    return {
        "metadata": {key: first[key] for key in common},
        "experimental_warning": (
            "LOCAL DEVELOPMENT-INFORMED NDAP 280 REGRESSION ONLY. "
            "Not independent held-out accuracy or official IndicDB performance."
        ),
        "metrics": metrics,
        "records": all_rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shards-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    paths = sorted(args.shards_dir.rglob("paired-shard-*.json"))
    shards = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    result = combine(shards)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for language, counts in result["metrics"]["per_language"].items():
        print(f"{language}: n={counts['n']}, IndicSQL matches={counts['indicsql']['execution_matches']}, "
              f"Qwen direct matches={counts['qwen_direct']['execution_matches']}")
    print("Finished comparing verified same-cohort local regression runs; no official performance claim.")


if __name__ == "__main__":
    main()
