# IndicSQL paper evidence outline

## Claim boundary

This project is a multilingual Text-to-SQL system for seven Indic-language
variants: English, Hinglish, Hindi, Marathi, Bengali, Tamil, and Telugu. The
paper must distinguish local development diagnostics from the locked official
IndicDB evaluation.

Do not claim full IndicDB parity while `INDIA_UDISE_SCHOOL_PROFILES` lacks a
source-level identity proof. Do not infer semantic correctness from successful
SQL execution. The exact license subtype remains unresolved.

## Reproducible source evidence

- Benchmark: `roshankaranth/IndicDB` at revision
  `f57b0fb75d672114ae2d6e6be1a78d64056ce8af`.
- Seven Parquet inputs, Google Drive archive, and embedded PostgreSQL dump are
  SHA-256 verified in `data/benchmarks/indicdb_source_manifest.json`.
- The official archive declares 17 schemas and 208 tables.
- The fresh PostgreSQL 16 audit restored 17 schemas, 208 tables, and
  3,910,112 rows; its gold SQL execution artifact is
  `benchmark_results/indicdb_gold_execution_20261118_fresh_restore.json`.
- Gold SQL execution establishes executability only, not gold semantic
  correctness.

## Method

1. Detect language and extract multilingual schema/metric/entity evidence.
2. Route to a schema from released metadata without passing benchmark schema
   labels to the predictor.
3. Ground metrics, aggregation, ranking, grouping, and entity filters.
4. Generate read-only SQL and execute it with PostgreSQL statement timeouts.
5. Compare normalized result rows with the gold reference only after
   prediction.

## Evaluation protocol

The paper's final evaluation uses the sealed manifest and the official
PostgreSQL restore. The locked run records model digest, seed 42, temperature
0.05, input hashes, evaluator command, and runtime without credentials.

The local 280-query NDAP suite is an exposed engineering regression suite. Its
latest 100% score is not a final or held-out result and must not be presented
as one.

## Results tables to fill from the sealed report

| Language | Questions | Valid schema route | SQL execution success | Execution match (EX%) | Mean latency (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| English | 40 | 40 (100.0%) | 17 (42.5%) | 7 (17.5%) | 58,430 |
| Hinglish | 40 | 39 (97.5%) | 21 (52.5%) | 11 (27.5%) | 41,067 |
| Hindi | 40 | 40 (100.0%) | 24 (60.0%) | 11 (27.5%) | 46,180 |
| Marathi | 40 | 39 (97.5%) | 19 (47.5%) | 7 (17.5%) | 44,038 |
| Bengali | 40 | 39 (97.5%) | 23 (57.5%) | 8 (20.0%) | 13,225 |
| Tamil | 40 | 40 (100.0%) | 25 (62.5%) | 11 (27.5%) | 43,019 |
| Telugu | 40 | 40 (100.0%) | 24 (60.0%) | 8 (20.0%) | 25,804 |
| **Overall** | **280** | **277 (98.9%)** | **153 (54.6%)** | **63 (22.5%)** | **38,823** |

Required aggregate fields: mapped-schema denominator, UDISE exclusion count,
gold execution errors, prediction errors, empty results, and confidence
intervals for execution match.

## Ablations

Evaluate on a separate development set only:

- schema routing only;
- routing plus metric planner;
- routing plus metric/entity grounding;
- full pipeline.

Report the changes as engineering diagnostics, never as held-out gains.

## Required human review

Native reviewers for Hindi, Marathi, Bengali, Tamil, and Telugu review
naturalness, term meaning, and gold-SQL semantic alignment. Hinglish is
reviewed with Hindi. Use `docs/native_language_review_protocol.md` and retain
review decisions separately from sealed questions.

## Limitations

- UDISE schema identity is unresolved unless direct source evidence is added.
- Exact license subtype is unknown.
- Execution equivalence does not establish semantic correctness.
- Local regression data informed fixes and is not a publication-grade held-out
  test.
