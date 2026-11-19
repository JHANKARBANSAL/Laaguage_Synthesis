#!/usr/bin/env python3
"""Audit official aligned IndicDB gold SQL from pinned language Parquets.

Use --postgres-dsn-env to additionally execute one reference SQL per paired
question. Default mode validates structure only; no correctness claims.
Selected sealed question text and SQL are intentionally not exported.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path

from indicsql.benchmark.indicdb import load_aligned_indicdb_queries
from indicsql.sandbox.validator import validate_postgres_readonly_sql
from scripts.execute_indicdb_gold import build_schema_mapping


def audit_gold(parquet_dir: Path, archive: Path, dsn: str | None = None) -> dict:
    aligned, keys = load_aligned_indicdb_queries(parquet_dir)
    mappings = build_schema_mapping(archive)
    sandbox = None
    if dsn:
        from indicsql.sandbox.postgres_engine import PostgresSandbox
        sandbox = PostgresSandbox(dsn, statement_timeout_ms=60_000)
    summary: Counter[str] = Counter()
    records: list[dict] = []
    try:
        reference = aligned["en"]
        for (pair_id, dataset_name), item in zip(keys, reference):
            valid, reason = validate_postgres_readonly_sql(item.gold_sql)
            mapping = mappings.get(dataset_name)
            execution_error = None
            row_count = None
            if sandbox is not None and valid and mapping is not None:
                try:
                    output = sandbox.execute_query(item.gold_sql, mapping["postgres_schema_name"])
                    row_count = output["row_count"]
                    summary["gold_executed"] += 1
                except Exception as exc:
                    execution_error = type(exc).__name__
            record = {
                "opaque_key": hashlib.sha256(f"{pair_id}\0{dataset_name}".encode("utf-8")).hexdigest()[:18],
                "sql_valid_readonly": valid,
                "schema_mapping_available": mapping is not None,
                "gold_execution_attempted": bool(sandbox is not None and valid and mapping is not None),
                "gold_execution_error_type": execution_error,
                "gold_result_row_count": row_count,
            }
            records.append(record)
            summary["aligned_pairs"] += 1
            summary["valid_readonly_gold"] += valid
            summary["mapped_gold"] += mapping is not None
            summary["gold_execution_errors"] += execution_error is not None
    finally:
        if sandbox is not None:
            sandbox.close()
    return {
        "artifact_type": "IndicDB gold SQL independent structural and optional execution audit",
        "aligned_language_count": len(aligned),
        "summary": dict(summary),
        "records": records,
        "notes": [
            "Passing SQL parsing and execution does not prove gold SQL answers the language question correctly.",
            "Native-speaker semantic review remains separate.",
            "This covers aligned Parquet pairs, not automatically the sealed 40-pair selection.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parquet-dir", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--postgres-dsn-env", default=None, help="Name of env var containing read-only DB DSN")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    dsn = None
    if args.postgres_dsn_env:
        dsn = os.environ.get(args.postgres_dsn_env)
        if not dsn:
            parser.error("Requested PostgreSQL DSN environment variable is not set")
    result = audit_gold(args.parquet_dir, args.archive, dsn=dsn)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote gold SQL audit: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
