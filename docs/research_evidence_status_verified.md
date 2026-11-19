# IndicSQL research evidence status (source-audited)

This document distinguishes **tracked repository evidence**, **recorded local audit assertions**, and **experimental claims that are not reproducible from this Git revision**. It is not a final benchmark report.

## Canonical provenance

- Benchmark: `roshankaranth/IndicDB` (Hugging Face), pinned revision `f57b0fb75d672114ae2d6e6be1a78d64056ce8af`.
- Input: seven language-specific Parquet test files; `data/benchmarks/indicdb_source_manifest.json` tracks SHA-256 digests and **17,246 physical rows across the seven files**. Physical rows are not necessarily unique semantic questions.
- The manifest records **17 distinct dataset names** within those files, while the dataset-card summary cited in the manifest states **20 databases, 237 tables, and 7.69 million rows**. These must not be conflated.
- The manifest reports the byte-matched released PostgreSQL archive/dump with **17 restored schemas, 208 tables, and 3,910,112 records**. This is an assertion of an earlier local verification, not an independently repeated restoration in this change set.
- Two trailing-underscore IHDS schema-name variants have explicit mappings in `scripts/execute_indicdb_gold.py`. The UDISE schema is unresolved/excluded by the final selection manifest.
- The dataset license subtype is **unresolved** in the checked source manifest. Do not claim a specific Creative Commons subtype or blanket permissive reuse without evidence.

## Distinct suites: never combine metrics

1. **Locally generated DuckDB development suite:** `data/benchmarks/indicdb_eval_suite_pan_india_280.json`, constructed by `scripts/build_pan_india_280_benchmark_suite.py`. It is *not* the pinned-release held-out 280 selection.
2. **Selected pinned IndicDB subset:** `data/benchmarks/indicdb_final_sealed_manifest_v2.json` documents 40 paired groups × 7 languages and an exclusion procedure. The selected keys and final outputs are gitignored, so the manifest alone does not prove a completed inference run.
3. **Local 140-query development evaluation:** `data/benchmarks/unseen_140_evaluation_report.json` reports 99.29%, whereas `reports/e2e_failure_audit.json` reports 71.43% on 140 cases. These artifacts require run-specific provenance and reconciliation; do not publish one as a verified held-out result.

## Metrics and what was fixed

The earlier `scripts/evaluate_indicdb_sealed_final.py` incremented `valid_schema_routes` whenever a model returned **any released schema name**, even a wrong one. It was inappropriate to label that percentage schema-routing **accuracy**. The evaluator now records:

- `valid_schema_routes`: model selected a permitted schema name (validity only).
- `correct_schema_routes`: selected schema matches the benchmark schema after applying verified benchmark-to-restored-schema mappings. Gold identities are checked **only after prediction**.
- `prediction_execution_successes`: generated SQL produced a result with no recorded prediction error.
- `execution_matches`: normalized predicted and gold result multisets compare equal for that recorded execution.

The evaluator now defaults to a **60,000-ms SQL statement timeout** and records the configured timeout in the result; **this is a prospective correction, not evidence that any historical result used 60 seconds**. Model generation uses a separate HTTP timeout.

## Publication gate

Do not reproduce the paper's 277/280 routing, 153/280 execution success, 63/280 execution match, 96 identifier failures, 25 timeouts, or 7 gold defects as *verified current findings* without a corresponding final-run result, receipt, model digest, frozen code revision, and executed gold-reference audit. The `benchmark_results/` directory is ignored by Git and was not present in the public tree at review.

The paper's 128-case error taxonomy mixes possible prediction failures with benchmark annotation errors. Rebuild exclusive categories from per-question traces and keep gold-query defects in a distinct reference-quality column. Empty-set matches, SQL timeout categories, and model-generation timeouts need separate counts.

## Required experiment protocol

- Fix the canonical source revision and clean worktree, model digest, exact PostgreSQL dump hash, timeout, sampling settings, seven Parquet hashes, and 40 paired keys **before evaluation**.
- Audit gold SQL and record noncomparable cases separately; report total and comparable denominators.
- Run direct-model, retrieval-only, and component ablations on the **same paired cohort** with the same model, context budget, database, SQL validator and evaluator. Keep baseline prompts and predictions.
- For language differences, use paired per-question outcomes (e.g., McNemar) where the same 40 semantic items are translated across languages; do not claim statistical significance from marginal percentages alone.
- Publish sanitized per-item execution outcomes and reproducibility receipts, excluding credentials and disallowed source data.
- Native-speaker annotation and semantic correctness are **not verified** by the tracked artifacts.

## Changes in this branch

- Correct schema-routing counter semantics and add regression tests.
- Separate prediction execution success from matching.
- Align new final-run default SQL execution timeout with the paper's stated 60 s, without rewriting historical metadata.

Remaining work requires the original ignored result files or a new genuine run against the pinned PostgreSQL dump and locked Ollama model. No baseline or ablation outcomes were fabricated.
