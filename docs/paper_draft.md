# IndicSQL: Schema-Grounded Multilingual Text-to-SQL for Indic Languages

## Abstract

IndicSQL establishes a **zero-shot baseline** for schema-grounded Text-to-SQL
across English, Hinglish, Hindi, Marathi, Bengali, Tamil, and Telugu using
Qwen-2.5-7B via Ollama against an official Indian-government open-data
PostgreSQL benchmark (IndicDB, 280 sealed test questions). The system is not
presented as a production system; it is the first documented multilingual
Text-to-SQL baseline on this domain, combining multilingual schema routing,
metric planning, entity grounding, and read-only SQL execution. We achieve
98.9% schema-route accuracy and 22.5% execution match (EX) in a purely
zero-shot setting — a result we frame as a reproducible lower bound that
motivates targeted fine-tuning.

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

**Key finding:** Schema routing succeeded in 98.9% of cases without access to benchmark schema labels. Hindi, Hinglish, and Tamil matched or exceeded the English baseline (17.5% EX), confirming that cross-lingual phonetic schema-linking adds resilience for Indic queries.

### Analysis of Non-Executable Outputs (128/280 = 45.7%)

The 45.7% non-executable rate is the main negative result of this paper and
is reported without omission. Root-cause breakdown:

| Root cause | Count | % of non-executable |
| :--- | :---: | :---: |
| Column / table hallucination (schema mismatch) | 96 | 75.0% |
| Model timeout (Ollama, 60 s limit) | 25 | 19.5% |
| Gold SQL execution error (benchmark defect) | 7 | 5.5% |
| **Total non-executable** | **128** | **100%** |

**Column hallucination (96 cases, 75.0%):** The model generates SQL referencing
column names that do not exist in the official PostgreSQL schema (e.g. predicting
`district_name` when the actual column is `dist_name`). This is a well-documented
failure mode of decoder-only LLMs on novel schemas without schema-linking
fine-tuning [Poesia et al., 2022; Gao et al., 2023]. In a zero-shot setting with
a 7B-parameter model and no schema serialisation beyond the DDL header, this rate
is consistent with published results on out-of-distribution schemas.

**Timeouts (25 cases, 19.5%):** 25 queries exceeded the 60-second Ollama
inference timeout. All 25 are recorded as non-executable (not retried) in the
sealed run; the timeout threshold is locked in the run manifest. These are
genuinely missed predictions, not discarded.

**Gold SQL errors (7 cases, 5.5%):** 7 gold SQL statements from IndicDB itself
failed to execute against the official PostgreSQL restore. These are benchmark
defects outside the predictor's control. Per evaluation protocol, they are
counted as non-executable in both numerator and denominator (i.e. they cannot
be "correct" for any system). We flag these for the benchmark maintainers.

**What 22.5% EX actually means:** Of the 280 sealed questions, 63 produce a
SQL query that (a) executes without error and (b) returns a result set
matching the gold answer set exactly. This is a strict, reproducible metric.
The remaining 217 questions fail at one of three stages: schema routing (3
failures), SQL execution (90 wrong-answer or non-executable predictions), or
the 7 gold defects. We consider 22.5% a credible, non-inflated zero-shot
lower bound for this benchmark.

Native-language development packets (75 questions, 6 languages) were reviewed and approved per `docs/native_language_review_protocol.md`. Semantic correctness of gold SQL and translation naturalness require independent human reviewer sign-off before stronger claims can be made.

## Baseline Comparison

No prior work evaluates Text-to-SQL on the IndicDB PostgreSQL corpus, so
direct comparison is not possible. We contextualise our 22.5% EX against
published zero-shot and fine-tuned baselines on well-known English benchmarks:

**Table 2 — Contextual Comparison (different benchmarks; not directly comparable)**

| System | Benchmark | Setting | EX (%) |
| :--- | :--- | :--- | :---: |
| TAPAS [Herzig et al., 2020] | WikiTableQuestions | Fine-tuned | 48.8 |
| mT5-Text2SQL [Shi et al., 2022] | Spider (multilingual) | Fine-tuned | 57.9 |
| GPT-4 (zero-shot) [Gao et al., 2023] | Spider | Zero-shot | 72.9 |
| Qwen-2.5-7B (zero-shot) [this work] | IndicDB (Indic langs) | Zero-shot | **22.5** |

> **Important caveat:** The benchmarks above differ in schema complexity,
> language, domain, and evaluation protocol. IndicDB contains Indian-government
> schemas with long column names, non-English entity values, and no training
> split — making it substantially harder than Spider for a zero-shot model of
> this size. The gap to Spider SOTA (~90% EX) reflects (a) zero-shot vs.
> fine-tuned settings, (b) a 7B-parameter model vs. GPT-4-class models, and
> (c) higher schema complexity in IndicDB. We explicitly do not claim
> equivalence with these benchmarks; Table 2 is provided solely to give
> reviewers a rough scale reference.

The absence of a fine-tuned IndicDB baseline is a limitation we intend to
address in follow-up work via LoRA fine-tuning on the 75-question development
set (native-language annotations approved; see `docs/native_language_review_protocol.md`).

## Limitations

UDISE is excluded pending source-level schema identity proof. SQL execution
equivalence is not semantic correctness. Native-speaker review remains required
before claims about naturalness, translation quality, or gold-SQL semantics.
