#!/usr/bin/env python3
"""Same-cohort local NDAP 280-question IndicSQL vs direct Qwen evaluator.

This is a previously-used REGRESSION suite, not an official held-out IndicDB
benchmark. Reference SQL is from the local suite, not the official PostgreSQL
gold annotations. No Ollama inference means no evaluation result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from time import perf_counter

import httpx
import sqlglot
from sqlglot import exp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from indicsql.agents.sql_synthesizer import _ollama_client
from indicsql.benchmark.dataset import load_benchmark_dataset
from indicsql.benchmark.evaluator import are_tabular_results_equivalent
from indicsql.graph.workflow import execute_indicsql_pipeline
from indicsql.schema.catalog import NDAPCatalog
from indicsql.sandbox.duckdb_engine import DuckDBSandbox
from indicsql.sandbox.validator import validate_and_limit_sql

DEFAULT_SUITE = ROOT / "data/benchmarks/indicdb_eval_suite_pan_india_280.json"
LANGUAGES = {"en", "hi", "hi-en", "bn", "mr", "ta", "te"}


def file_hash(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for part in iter(lambda: handle.read(1048576), b""):
            h.update(part)
    return h.hexdigest()


def validate_cohort(queries):
    if len(queries) != 280 or len({q.query_id for q in queries}) != 280:
        raise ValueError("Must use exactly 280 distinct regression queries")
    counts = Counter(q.language for q in queries)
    if set(counts) != LANGUAGES or any(count != 40 for count in counts.values()):
        raise ValueError("Expected exactly 40 questions for each of seven languages")


def check_ollama(url, model):
    response = httpx.get(url.rstrip("/") + "/api/tags", timeout=15)
    response.raise_for_status()
    models = {x["name"]: x for x in response.json().get("models", [])}
    if model not in models or not models[model].get("digest"):
        raise RuntimeError("Exact Qwen model and digest must be installed; no fallback allowed")
    return models[model]["digest"]


def direct_prompt(question):
    tables = []
    for name in sorted(NDAPCatalog.list_tables()):
        cols = NDAPCatalog.get_table_schema(name).get("columns", {})
        tables.append(name + "(" + ", ".join(sorted(cols)) + ")")
    return (
        "Generate one valid DuckDB read-only SELECT for the question. "
        "Use only available columns/tables. No explanation, no markdown.\n"
        "All available tables:\n" + "\n".join(tables) +
        "\nQuestion: " + question + "\nSQL:"
    )


def execute_safe(sql, sandbox):
    statements = sqlglot.parse(sql, read="duckdb")
    if len(statements) != 1 or not isinstance(statements[0], exp.Query):
        raise ValueError("SQL must be exactly one SELECT/WITH query")
    allowed, normalized = validate_and_limit_sql(sql)
    if not allowed:
        raise ValueError(normalized)
    return sandbox.execute_query(normalized)


def evaluate_item(query, sandbox, url, model, timeout):
    item = {"query_id": query.query_id, "language": query.language,
            "domain": query.domain, "difficulty": query.difficulty}
    try:
        gold = execute_safe(query.gold_sql, sandbox)
        item["gold_error"] = None
    except Exception as error:
        item["gold_error"] = str(error)
        gold = None
    item["gold_empty"] = gold is not None and not gold["rows"]

    started = perf_counter()
    try:
        state = execute_indicsql_pipeline(
            query.query, query_id=query.query_id, language_override=query.language,
            sandbox=sandbox,
        )
        output = state.get("execution_result")
        error = state.get("execution_error")
        if error or not state.get("generated_sql") or output is None:
            output = None
        methods = [step.get("method") for step in state.get("audit_trace", [])
                   if step.get("agent") == "SQLSynthesizerAgent"]
        item["indicsql"] = {
            "sql": state.get("generated_sql", ""), "error": error,
            "execution_success": output is not None,
            "execution_match": None if gold is None else
                bool(output is not None and are_tabular_results_equivalent(output, gold)),
            "row_count": None if output is None else output["row_count"],
            "methods": methods,
            "neural_generated": any(str(m).startswith("ollama_") for m in methods),
            "elapsed_ms": round((perf_counter()-started)*1000, 2),
        }
    except Exception as error:
        item["indicsql"] = {
            "sql": "", "error": str(error), "execution_success": False,
            "execution_match": None if gold is None else False, "row_count": None,
            "methods": [], "neural_generated": False,
            "elapsed_ms": round((perf_counter()-started)*1000, 2),
        }

    started = perf_counter()
    raw = ""
    output = None
    error = None
    inference_completed = False
    try:
        response = httpx.post(
            url.rstrip("/") + "/api/generate",
            json={"model": model, "prompt": direct_prompt(query.query), "stream": False,
                  "options": {"temperature": 0.05, "seed": 42}},
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("done") is not True:
            raise RuntimeError("Qwen did not finish generation")
        inference_completed = True
        raw = str(data.get("response") or "").strip()
        fenced = re.fullmatch(r"```(?:sql)?\s*(.*?)\s*```", raw, re.I | re.S)
        if fenced:
            raw = fenced.group(1)
        if not raw:
            raise RuntimeError("Empty Qwen SQL output")
        output = execute_safe(raw, sandbox)
    except Exception as exc:
        error = str(exc)
    item["qwen_direct"] = {
        "sql": raw, "error": error, "inference_completed": inference_completed,
        "execution_success": output is not None,
        "execution_match": None if gold is None else
            bool(output is not None and are_tabular_results_equivalent(output, gold)),
        "row_count": None if output is None else output["row_count"],
        "elapsed_ms": round((perf_counter()-started)*1000, 2),
    }
    return item


def summarize(records):
    if len(records) != 280 or len({r["query_id"] for r in records}) != 280:
        raise ValueError("Cannot calculate 280-query metrics from incomplete results")
    if Counter(r["language"] for r in records) != Counter({lang: 40 for lang in LANGUAGES}):
        raise ValueError("Incorrect language cohort")
    def metrics(rows):
        return {
            "n": len(rows), "gold_errors": sum(bool(r["gold_error"]) for r in rows),
            "gold_empty": sum(r["gold_empty"] for r in rows),
            "indicsql": {
                "execution_success": sum(r["indicsql"]["execution_success"] for r in rows),
                "execution_matches": sum(r["indicsql"]["execution_match"] is True for r in rows),
                "neural_generated": sum(r["indicsql"]["neural_generated"] for r in rows),
            },
            "qwen_direct": {
                "execution_success": sum(r["qwen_direct"]["execution_success"] for r in rows),
                "execution_matches": sum(r["qwen_direct"]["execution_match"] is True for r in rows),
            },
            "empty_empty_matches_needing_review": sum(
                r["gold_empty"] and r[m]["execution_match"] is True and r[m]["row_count"] == 0
                for r in rows for m in ("indicsql", "qwen_direct")
            ),
        }
    return {"overall": metrics(records), "per_language": {
        lang: metrics([r for r in records if r["language"] == lang])
        for lang in sorted(LANGUAGES)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--parquet-dir", type=Path, default=ROOT / "data/parquet_stores")
    parser.add_argument("--ollama-url", default=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))
    parser.add_argument("--model", default="qwen2.5:3b")
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=280)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    queries = load_benchmark_dataset(args.suite)
    validate_cohort(queries)
    if not 1 <= args.start <= args.end <= 280:
        parser.error("Invalid 280-question range")
    digest = check_ollama(args.ollama_url, args.model)
    _ollama_client.base_url = args.ollama_url.rstrip("/")
    _ollama_client.model_name = args.model
    _ollama_client._is_active = True
    _ollama_client.timeout = args.timeout
    sandbox = DuckDBSandbox(parquet_dir=args.parquet_dir)
    files = sorted(args.parquet_dir.rglob("*.parquet"))
    if not files:
        raise RuntimeError("No DuckDB fixture Parquet files")
    meta = {
        "artifact_type": "local_ndap_280_paired_regression",
        "official_indicdb_score": False, "held_out": False,
        "local_development_informed_suite": True,
        "model": args.model, "model_digest": digest,
        "suite_sha256": file_hash(args.suite),
        "data_sha256": {str(p.relative_to(args.parquet_dir)): file_hash(p) for p in files},
        "start": args.start, "end": args.end,
        "comparison": "IndicSQL full agent (may use heuristic fallback) versus direct Qwen given full catalog",
    }
    checkpoint = args.output.with_suffix(".checkpoint.json")
    records = []
    if args.resume and checkpoint.exists():
        saved = json.loads(checkpoint.read_text(encoding="utf-8"))
        if saved["metadata"] != meta:
            raise ValueError("Checkpoint inputs/model differ")
        records = saved["records"]
    cohort = queries[args.start-1:args.end]
    ids = {q.query_id for q in cohort}
    done = {r["query_id"] for r in records}
    if len(done) != len(records) or not done.issubset(ids):
        raise ValueError("Checkpoint has duplicate or foreign IDs")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        for index, query in enumerate(cohort, args.start):
            if query.query_id in done:
                continue
            row = evaluate_item(query, sandbox, args.ollama_url, args.model, args.timeout)
            records.append(row)
            checkpoint.write_text(json.dumps({"metadata": meta, "records": records},
                                             ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"{index}/{args.end}: {query.query_id} IndicSQL={row['indicsql']['execution_match']} Qwen={row['qwen_direct']['execution_match']}", flush=True)
    finally:
        sandbox.close()
    if len(records) != len(cohort):
        raise RuntimeError("Incomplete paired inference")
    if not all(r["qwen_direct"].get("inference_completed") for r in records):
        raise RuntimeError("One or more direct Qwen generations did not complete; partial checkpoint retained")
    result = {"metadata": meta, "records": records}
    if args.start == 1 and args.end == 280:
        result["metrics"] = summarize(records)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Completed {len(records)} paired questions: {args.output}")


if __name__ == "__main__":
    main()
