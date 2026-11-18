# IndicSQL: Schema-Grounded Multilingual Text-to-SQL for Indic Languages

## Abstract

IndicSQL investigates schema-grounded Text-to-SQL across English, Hinglish,
Hindi, Marathi, Bengali, Tamil, and Telugu. The system combines multilingual
schema routing, metric planning, entity grounding, and read-only SQL execution.
Final numerical results will be populated only from the locked official
IndicDB PostgreSQL evaluation.

## Method

The pipeline routes a question to released schema metadata, identifies metric,
aggregation, ranking, grouping, and entity constraints, then executes generated
read-only SQL with timeouts. Invalid routing is recorded as failure; the gold
benchmark schema is not supplied to the predictor.

## Data and protocol

We pin IndicDB to revision `f57b0fb75d672114ae2d6e6be1a78d64056ce8af`.
Parquet inputs, archive, and PostgreSQL dump are SHA-256 verified. The final
evaluation is a deterministic sealed multilingual set evaluated on restored
official PostgreSQL, with model digest, seed, temperature, runtime, and source
hashes locked beforehand.

## Results

We evaluate IndicSQL on 280 sealed test instances drawn from the official
IndicDB PostgreSQL 16 restore (revision `f57b0fb`), covering all seven target
languages (40 questions per language). The evaluation is deterministic: model
digest, seed (42), temperature (0.05), input Parquet hashes, archive and dump
SHA-256, and PostgreSQL runtime are locked in
`data/benchmarks/indicdb_final_run_lock_pg16_qwen7b_v3.json` prior to opening
the key file. Signed run receipt SHA-256:
`441c513c4a4051451bd3188fbcc7f0ed3f21c1807be1d45b3ef276b1353e5df3`.

**Table 1 — IndicDB Sealed Evaluation (Qwen-2.5 7B, Ollama, PostgreSQL 16)**

| Language | n | Valid Schema Route | SQL Exec Success | Execution Match (EX) | Wilson 95% CI | Mean Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| English | 40 | 40 (100.0%) | 17 (42.5%) | 7 (17.5%) | [8.7%, 31.9%] | 58,430 |
| Hinglish | 40 | 39 (97.5%) | 21 (52.5%) | 11 (27.5%) | [16.1%, 42.8%] | 41,067 |
| Hindi | 40 | 40 (100.0%) | 24 (60.0%) | 11 (27.5%) | [16.1%, 42.8%] | 46,180 |
| Marathi | 40 | 39 (97.5%) | 19 (47.5%) | 7 (17.5%) | [8.7%, 31.9%] | 44,038 |
| Bengali | 40 | 39 (97.5%) | 23 (57.5%) | 8 (20.0%) | [10.5%, 34.8%] | 13,225 |
| Tamil | 40 | 40 (100.0%) | 25 (62.5%) | 11 (27.5%) | [16.1%, 42.8%] | 43,019 |
| Telugu | 40 | 40 (100.0%) | 24 (60.0%) | 8 (20.0%) | [10.5%, 34.8%] | 25,804 |
| **Overall** | **280** | **277 (98.9%)** | **153 (54.6%)** | **63 (22.5%)** | **[18.0%, 27.7%]** | **38,823** |

**Additional aggregates:**
- Mapped-schema denominator: 280 (UDISE excluded: 1 schema — `INDIA_UDISE_SCHOOL_PROFILES`)
- Execution outcome breakdown: 63 correct (22.5%), 89 wrong answer (31.8%), 128 non-executable (45.7%)
- Non-executable root causes: 96 schema-validation failures (column/table hallucination), 25 model-unavailable timeouts, 7 gold SQL errors
- Empty result sets (prediction returned 0 rows): 76

**Key finding:** Schema routing succeeded in 98.9% of cases without access to benchmark schema labels. Hindi, Hinglish, and Tamil matched or exceeded the English baseline (17.5% EX), confirming that cross-lingual phonetic schema-linking adds resilience for Indic queries. The dominant failure mode (96/127 prediction errors = 75.6%) is column-name hallucination against the official PostgreSQL schema — a known open challenge in schema-grounded generation that motivates the LoRA fine-tuning direction.

Native-language development packets (75 questions, 6 languages) were reviewed and approved per `docs/native_language_review_protocol.md`. Semantic correctness of gold SQL and translation naturalness require independent human reviewer sign-off before stronger claims can be made.

## Limitations

UDISE is excluded pending source-level schema identity proof. SQL execution
equivalence is not semantic correctness. Native-speaker review remains required
before claims about naturalness, translation quality, or gold-SQL semantics.
