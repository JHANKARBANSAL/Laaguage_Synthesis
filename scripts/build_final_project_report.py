#!/usr/bin/env python3
"""Build the evidence-bounded IndicSQL final project report from local artifacts."""

from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = Path('/Users/jhankar/Downloads/Body Format (1).docx')
OUTPUT = ROOT / 'reports/IndicSQL_Final_Project_Report.docx'
ASSETS = ROOT / 'reports/indicsql_report_assets'
FINAL = ROOT / 'benchmark_results/sealed_final/indicdb_final_results_pg16_qwen7b_v3.json'
GOLD = ROOT / 'benchmark_results/indicdb_gold_execution_20261118_fresh_restore.json'
DEV = ROOT / 'benchmark_results/query_audit_pan_india_280_20261118_semantic_recheck_v4/evaluation_report.json'


def shade(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), fill)
    tc_pr.append(shd)


def border_table(table) -> None:
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        element = OxmlElement(f'w:{edge}')
        element.set(qn('w:val'), 'single')
        element.set(qn('w:sz'), '4')
        element.set(qn('w:color'), 'D9D9D9')
        borders.append(element)
    tbl_pr.append(borders)


def set_cell_text(cell, text: str, bold: bool = False, color: str | None = None) -> None:
    cell.text = ''
    para = cell.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(str(text))
    run.bold = bold
    run.font.name = 'Times New Roman'
    run.font.size = Pt(9)
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def add_table(doc, headers: list[str], rows: list[list[str]], widths: list[float] | None = None) -> None:
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    border_table(table)
    for cell, header in zip(table.rows[0].cells, headers):
        shade(cell, '1F4E78')
        set_cell_text(cell, header, bold=True, color='FFFFFF')
    for index, row in enumerate(rows):
        cells = table.add_row().cells
        for cell, value in zip(cells, row):
            if index % 2:
                shade(cell, 'EAF2F8')
            set_cell_text(cell, value)
    if widths:
        for row in table.rows:
            for cell, width in zip(row.cells, widths):
                cell.width = Inches(width)
    doc.add_paragraph()


def add_heading(doc, text: str, level: int = 1) -> None:
    paragraph = doc.add_paragraph()
    paragraph.style = f'Heading {min(level, 3)}'
    run = paragraph.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0, 0, 0)


def add_body(doc, text: str, bold_prefix: str | None = None) -> None:
    paragraph = doc.add_paragraph(style='Body Text')
    paragraph.paragraph_format.space_after = Pt(6)
    paragraph.paragraph_format.line_spacing = 1.15
    if bold_prefix and text.startswith(bold_prefix):
        paragraph.add_run(bold_prefix).bold = True
        paragraph.add_run(text[len(bold_prefix):])
    else:
        paragraph.add_run(text)
    for run in paragraph.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)


def add_bullets(doc, items: list[str]) -> None:
    for item in items:
        paragraph = doc.add_paragraph(style='List Bullet')
        run = paragraph.add_run(item)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)


def page_break(doc) -> None:
    doc.add_section(WD_SECTION.NEW_PAGE)


def make_figures(final: dict) -> tuple[Path, Path, Path]:
    ASSETS.mkdir(parents=True, exist_ok=True)
    labels = ['English', 'Hinglish', 'Hindi', 'Marathi', 'Bengali', 'Tamil', 'Telugu']
    keys = ['en', 'hi-en', 'hi', 'mr', 'bn', 'ta', 'te']
    data = final['per_language']
    route = [100 * data[k]['valid_schema_routes'] / 40 for k in keys]
    match = [100 * data[k]['execution_matches'] / 40 for k in keys]
    fig, ax = plt.subplots(figsize=(9.5, 4.6), dpi=180)
    x = list(range(len(labels)))
    ax.bar([i - 0.19 for i in x], route, 0.38, label='Valid schema route', color='#1f77b4')
    ax.bar([i + 0.19 for i in x], match, 0.38, label='Execution match / all attempts', color='#d95f02')
    ax.set_ylim(0, 110); ax.set_ylabel('Percent'); ax.set_xticks(x, labels, rotation=25, ha='right')
    ax.set_title('Locked official IndicDB evaluation by language')
    ax.legend(frameon=False); ax.grid(axis='y', alpha=.25)
    fig.tight_layout(); language_path = ASSETS / 'sealed_language_metrics.png'; fig.savefig(language_path); plt.close(fig)

    records = final['records']
    categories = ['Valid route', 'Prediction executed', 'Comparable outputs', 'Execution matches']
    values = [sum(x['routed_schema'] is not None for x in records),
              sum(not x['prediction_error'] for x in records),
              sum(x['execution_match'] is not None for x in records),
              sum(x['execution_match'] is True for x in records)]
    fig, ax = plt.subplots(figsize=(8.2, 4.5), dpi=180)
    bars = ax.bar(categories, values, color=['#1f77b4', '#6baed6', '#fdae6b', '#d95f02'])
    ax.set_ylim(0, 300); ax.set_ylabel('Queries out of 280'); ax.set_title('Evaluation funnel on the sealed official set')
    ax.grid(axis='y', alpha=.25)
    for bar, value in zip(bars, values): ax.text(bar.get_x()+bar.get_width()/2, value+5, str(value), ha='center', fontsize=10)
    fig.tight_layout(); funnel_path = ASSETS / 'sealed_evaluation_funnel.png'; fig.savefig(funnel_path); plt.close(fig)
    fig, ax = plt.subplots(figsize=(9.5, 4.2), dpi=180)
    ax.axis('off')
    steps = [
        ('Question\nand language', '#DCEEFF'), ('Schema router\nreleased metadata', '#EDE0FF'),
        ('PostgreSQL schema\ncontext', '#FFF1C9'), ('Qwen2.5 7B\nSQL synthesis', '#FCE1E1'),
        ('Read only SQL\nvalidation', '#DDF4E6'), ('PostgreSQL execution\nresult comparison', '#DCEEFF')]
    for i, (label, color) in enumerate(steps):
        x0 = .02 + i * .163
        rect = plt.Rectangle((x0, .34), .135, .32, transform=ax.transAxes, facecolor=color, edgecolor='#1F4E78', linewidth=1.5)
        ax.add_patch(rect); ax.text(x0+.0675, .5, label, transform=ax.transAxes, ha='center', va='center', fontsize=9, weight='bold')
        if i < len(steps)-1: ax.annotate('', xy=(x0+.16, .5), xytext=(x0+.137, .5), xycoords=ax.transAxes, arrowprops={'arrowstyle':'->','lw':1.4})
    ax.set_title('IndicSQL locked official evaluation path', fontsize=14, weight='bold')
    fig.tight_layout(); architecture_path = ASSETS / 'verified_architecture.png'; fig.savefig(architecture_path); plt.close(fig)
    return language_path, funnel_path, architecture_path


def clear_body(doc: Document) -> None:
    body = doc._element.body
    for child in list(body):
        if child.tag != qn('w:sectPr'):
            body.remove(child)


def main() -> None:
    final = json.loads(FINAL.read_text())
    gold = json.loads(GOLD.read_text())
    dev = json.loads(DEV.read_text())
    lang_fig, funnel_fig, architecture_fig = make_figures(final)
    shutil.copy2(TEMPLATE, OUTPUT)
    doc = Document(OUTPUT)
    clear_body(doc)

    normal = doc.styles['Normal']; normal.font.name = 'Times New Roman'; normal.font.size = Pt(11)
    title = doc.add_paragraph(style='Title'); title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('IndicSQL Final Project Report'); run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    subtitle = doc.add_paragraph(); subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = subtitle.add_run('Schema Grounded Multilingual Text to SQL for Seven Indic Language Variants'); r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(15)
    doc.add_paragraph()
    for line in ('Prepared using the supplied BML Munjal University report format', 'Candidate name and university roll number to be completed by the student', 'Supervisor name and designation to be completed by the supervisor'):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run(line).font.name = 'Times New Roman'
    page_break(doc)

    add_heading(doc, 'Abstract')
    add_body(doc, 'IndicSQL is a schema grounded multilingual Text to SQL system for English, Hinglish, Hindi, Marathi, Bengali, Tamil, and Telugu. The system combines language handling, schema routing, metric and entity grounding, local Qwen based SQL generation, SQL validation, and read only database execution. The project verified the source identity of the pinned IndicDB Parquet files, source archive, and PostgreSQL dump by SHA 256. A locked final evaluation used 280 questions from a replacement sealed multilingual set and an official PostgreSQL 16 restore. The evaluation recorded 98.93 percent valid schema routes, 54.64 percent prediction execution success, and 41.45 percent execution equivalence among 152 comparable executions. These results establish a reproducible baseline and expose remaining SQL synthesis and schema grounding failures. They do not establish native language naturalness or gold SQL semantic correctness, which still require human review.')
    add_heading(doc, 'Declaration and Report Scope')
    add_body(doc, 'This report records the implemented system, evidence, and current measured results. Student identity, roll number, supervisor name, and submission dates are intentionally left as placeholders because they were not present in the repository. The report does not claim complete IndicDB parity because the UDISE benchmark to archive schema identity remains unresolved.')
    page_break(doc)

    add_heading(doc, 'Introduction')
    add_heading(doc, 'Problem Statement', 2)
    add_body(doc, 'Natural language access to public data is difficult when users ask in multiple scripts, use transliteration or code mixing, and expect exact numerical answers. Text to SQL systems must select a schema, identify a metric and aggregation, preserve filters, generate safe SQL, and execute it against the intended database. The problem becomes harder when benchmark schema labels and released database schema names do not align exactly.')
    add_heading(doc, 'Objectives', 2)
    add_bullets(doc, ['Support seven language variants with a common Text to SQL pipeline.', 'Ground tables, metrics, aggregations, rankings, time grouping, and entities from user questions.', 'Execute only read only SQL with validation and statement timeouts.', 'Make benchmark evaluation reproducible through pinned sources, hashes, locks, and sealed final testing.', 'Report limitations rather than substituting benchmark metadata for model predictions.'])
    add_heading(doc, 'Related Work', 2)
    add_body(doc, 'Spider introduced cross domain Text to SQL evaluation with unseen databases [1]. BIRD extended evaluation toward database grounded questions and execution based measures on larger real world databases [2]. IndicSQL uses these evaluation principles while focusing on multilingual schema and metric grounding. Qwen2.5 is used as the local locked generation model in the official run [3].')
    add_table(doc, ['Work', 'Contribution', 'Relation to IndicSQL'], [['Spider [1]', 'Cross domain Text to SQL benchmark', 'Motivates schema generalization'], ['BIRD [2]', 'Database grounded execution evaluation', 'Motivates execution based reporting'], ['IndicDB [4]', 'Seven language benchmark source', 'Pinned source for this project'], ['Qwen2.5 [3]', 'Open weight language model family', 'Local locked SQL generation model']])
    page_break(doc)

    add_heading(doc, 'Data and Source Verification')
    add_body(doc, 'The benchmark was pinned to roshankaranth IndicDB revision f57b0fb75d672114ae2d6e6be1a78d64056ce8af. All seven downloaded Parquet files matched the recorded SHA 256 values. The downloaded source archive and embedded PostgreSQL dump also matched the verified source manifest.')
    add_table(doc, ['Artifact', 'Verified evidence'], [['Language splits', 'Seven Parquet files for English, Hinglish, Hindi, Marathi, Bengali, Tamil, and Telugu'], ['Physical benchmark rows', '17,246 rows; 17,241 nonblank SQL statements parsed'], ['Source archive', '17 released schema configurations and 208 declared tables'], ['Restored PostgreSQL catalog', '17 schemas, 208 tables, 3,910,112 rows'], ['Gold SQL audit', f"{gold['queries_attempted']:,} mapped statements attempted; {gold['execution_error_count']} execution errors; {gold['empty_result_count']:,} empty results"]])
    add_body(doc, 'The benchmark contains 14 exact schema name matches. Three benchmark names are unresolved, including INDIA UDISE SCHOOL PROFILES. UDISE rows are excluded from the final mapped schema denominator. Successful gold SQL execution demonstrates executability, not that every gold query is semantically correct.')
    add_heading(doc, 'Development and Final Set Separation', 2)
    add_body(doc, 'The exposed local 280 query NDAP suite was used for engineering regression. Its final local score reached 100 percent execution equivalence, but it is not reported as held out accuracy because its failures informed implementation changes. The official final set was separately selected with a deterministic hash rule and evaluated after model and runtime locking.')
    page_break(doc)

    add_heading(doc, 'System Methodology')
    add_body(doc, 'The deployed evaluation path receives a question, routes it using released schema metadata, loads the selected PostgreSQL schema context, generates SQL with the locked local Qwen2.5 7B model, validates read only SQL, executes it with a statement timeout, and compares normalized rows with gold SQL only after prediction. Benchmark dataset names are not passed to the predictor for schema selection.')
    doc.add_picture(str(architecture_fig), width=Inches(6.35))
    cap = doc.add_paragraph('Figure 1. Verified evaluation path used for the locked official run.'); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_heading(doc, 'Safety and Reliability Controls', 2)
    add_table(doc, ['Control', 'Implemented behavior'], [['Read only validator', 'Rejects non SELECT and non WITH SQL before database execution'], ['Schema routing', 'Invalid router output is recorded as a failure and is not replaced with a gold schema'], ['Timeout', 'Official PostgreSQL execution uses statement timeouts'], ['Source integrity', 'Parquet, archive, and dump hashes are checked before locked execution'], ['Sealed evaluation', 'Selected keys are read only after runtime and lock validation'], ['Audit output', 'Final report excludes final question text and gold SQL']])
    add_heading(doc, 'Engineering Improvements', 2)
    add_bullets(doc, ['Metric planner handling metric columns, aggregation, ranking, grouping, and time scope.', 'Entity grounding for state, district, commodity, and sector values.', 'Multilingual vocabulary coverage and phonetic normalization.', 'Schema based SQL validation and read only PostgreSQL sandbox execution.', 'Focused regression tests for fallback synthesis, metric selection, and sealed evaluation safeguards.'])
    page_break(doc)

    add_heading(doc, 'Evaluation Design')
    add_body(doc, 'The final run used qwen2.5 7B through a local Ollama endpoint, temperature 0.05, seed 42, and a PostgreSQL 16.16 restore. The lock recorded source hashes, model digest, evaluator command, and runtime metadata without credentials or selected keys. The final replacement set consisted of 40 multilingual groups and 280 questions. Previously opened sealed keys were excluded from this replacement set.')
    add_table(doc, ['Metric', 'Definition'], [['Valid schema route', 'Router returned an exact released schema name'], ['Prediction execution success', 'Generated SQL executed without a prediction error'], ['Comparable execution', 'Both predicted SQL and gold SQL returned results'], ['Execution equivalence', 'Order independent normalized predicted rows equal gold rows'], ['Latency', 'End to end time recorded for the evaluated question']])
    add_body(doc, 'Execution equivalence is a program level metric. It must not be interpreted as native speaker validation, answer usefulness, or gold SQL semantic correctness.')
    page_break(doc)

    add_heading(doc, 'Results')
    records = final['records']
    comparable = [x for x in records if x['execution_match'] is not None]
    matches = sum(x['execution_match'] is True for x in records)
    pred_success = sum(not x['prediction_error'] for x in records)
    valid_routes = sum(x['routed_schema'] is not None for x in records)
    add_body(doc, f'The locked official evaluation completed all 280 selected questions. It produced {valid_routes}/280 valid schema routes (98.93 percent), {pred_success}/280 prediction executions without recorded errors (54.64 percent), and {matches}/280 matches over all attempts (22.50 percent). Among {len(comparable)} comparable predicted and gold executions, {matches} matched, yielding 41.45 percent execution equivalence. This is the official measured baseline for the locked configuration, not a claim of semantic correctness.')
    lang_names = {'en': 'English', 'hi-en': 'Hinglish', 'hi': 'Hindi', 'mr': 'Marathi', 'bn': 'Bengali', 'ta': 'Tamil', 'te': 'Telugu'}
    rows = []
    for key in ['en', 'hi-en', 'hi', 'mr', 'bn', 'ta', 'te']:
        m = final['per_language'][key]; r = [x for x in records if x['language'] == key]; c = [x for x in r if x['execution_match'] is not None]
        rows.append([lang_names[key], '40', f"{m['valid_schema_routes']}/40", f"{40-m['prediction_errors']}/40", f"{sum(x['execution_match'] is True for x in r)}/{len(c)}", f"{sum(x['latency_ms'] for x in r)/40/1000:.1f}"])
    add_table(doc, ['Language', 'Questions', 'Valid routes', 'Prediction success', 'Match / comparable', 'Mean latency s'], rows)
    doc.add_picture(str(lang_fig), width=Inches(6.1)); cap = doc.add_paragraph('Figure 2. Valid schema routing and execution matches by language on the locked official evaluation.'); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(str(funnel_fig), width=Inches(5.9)); cap = doc.add_paragraph('Figure 3. Evaluation funnel on the 280 question locked official set.'); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    page_break(doc)

    add_heading(doc, 'Error Analysis')
    errors = Counter(x['prediction_error'] for x in records if x['prediction_error'])
    add_table(doc, ['Observed outcome', 'Count', 'Interpretation'], [['Prediction errors', str(sum(errors.values())), 'SQL generation, schema validation, router, or execution failure'], ['Invalid schema router output', str(errors.get('invalid_schema_router_output', 0)), 'No gold schema replacement was applied'], ['Gold execution errors', str(sum(bool(x['gold_error']) for x in records)), 'Gold reference could not be executed under read only validation'], ['Comparable but nonmatching outputs', str(len(comparable)-matches), 'Predicted execution completed but rows differed from gold'], ['UDISE benchmark rows', 'Excluded', 'Source level schema identity remains unresolved']])
    add_body(doc, 'The principal engineering gap is not basic schema-route coverage, which was high in this locked run. The dominant problem is reliable SQL synthesis against complex official schemas: 127 predictions recorded an error, and 89 comparable executions did not match gold output. The next research iteration should improve schema specific SQL generation and join planning, then use a fresh sealed evaluation rather than tuning this result.')
    page_break(doc)

    add_heading(doc, 'Conclusion and Future Scope')
    add_heading(doc, 'Conclusion', 2)
    add_body(doc, 'IndicSQL delivers a reproducible multilingual Text to SQL engineering platform with source verification, schema routing, metric and entity grounding, local model inference, SQL safety controls, and official PostgreSQL evaluation. The project completed a locked final evaluation and produced a transparent baseline. The result is useful because it separates strong source and routing evidence from weaker end to end SQL synthesis performance.')
    add_heading(doc, 'Future Scope', 2)
    add_bullets(doc, ['Complete native speaker review for question naturalness, translation terms, and gold SQL semantics.', 'Obtain direct evidence for the UDISE schema identity or retain its explicit exclusion.', 'Improve schema specific join planning and SQL generation for complex normalized official schemas.', 'Evaluate a new sealed set only after model and code are frozen.', 'Compare controlled model and planner ablations under the same official PostgreSQL protocol.'])
    add_heading(doc, 'Limitations', 2)
    add_body(doc, 'The final report does not claim full benchmark parity, native language quality, gold SQL semantic correctness, or an exact source license subtype. The local 100 percent development regression score is explicitly separated from the official locked result because it was used during engineering iterations.')
    page_break(doc)

    add_heading(doc, 'References')
    refs = [
        '[1] T. Yu et al., Spider A Large Scale Human Labeled Dataset for Complex and Cross Domain Semantic Parsing and Text to SQL Task, EMNLP 2018.',
        '[2] J. Li et al., Can LLM Already Serve as a Database Interface A BIg Bench for Large Scale Database Grounded Text to SQLs, NeurIPS 2023.',
        '[3] A. Yang et al., Qwen2.5 Technical Report, arXiv 2412.15115, 2024.',
        '[4] R. Karanth, IndicDB dataset, Hugging Face, pinned project revision f57b0fb75d672114ae2d6e6be1a78d64056ce8af.',
        '[5] IndicSQL repository artifacts: source manifest, sealed final manifest and lock, fresh PostgreSQL gold execution audit, and sealed final evaluation report.'
    ]
    for ref in refs: add_body(doc, ref)
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == '__main__':
    main()
