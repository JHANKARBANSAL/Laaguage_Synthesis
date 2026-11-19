#!/usr/bin/env python3
"""Generate LaTeX tables, JSON metrics and a figure ONLY from verified sealed runs.

Never use static percentages or copied claims. Validates SHA-256 receipt and
per-question result availability first. No results => no tables or figures.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape

from scripts.audit_indicdb_run import audit_result, verify_receipt

LANGUAGE_LABELS = {
    "en": "English", "hi-en": "Hinglish", "hi": "Hindi",
    "mr": "Marathi", "bn": "Bengali", "ta": "Tamil", "te": "Telugu",
}


def _rate(matches: int, n: int) -> str:
    return f"{100 * matches / n:.2f}\\%" if n else "N/A"


def make_latex(report: dict) -> str:
    overall = report["overall"]
    if overall["routing_status_available"] != overall["n"]:
        raise ValueError("Schema routing coverage incomplete; refusing to generate paper table")
    if overall["execution_status_available"] != overall["n"]:
        raise ValueError("SQL execution coverage incomplete; refusing to generate paper table")
    table = [
        "% Generated automatically from receipt-verified sealed experimental records.",
        "% Do not edit counts by hand.",
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{IndicSQL execution evaluation on a fixed paired cohort.}",
        r"\label{tab:indicsql-verified-language}",
        r"\begin{tabular}{lrrrr}",
        r"\hline",
        r"Language & Queries & Correct route & Executable & EX \\",
        r"\hline",
    ]
    for lang in ("en", "hi-en", "hi", "mr", "bn", "ta", "te"):
        if lang not in report["per_language"]:
            raise ValueError("Missing required language: " + lang)
        metric = report["per_language"][lang]
        table.append(
            f"{LANGUAGE_LABELS[lang]} & {metric['n']} & "
            f"{metric['correct_schema_routes']} & {metric['prediction_execution_success']} & "
            f"{_rate(metric['execution_matches'], metric['n'])} \\\\"
        )
    table += [
        r"\hline",
        f"Overall & {overall['n']} & {overall['correct_schema_routes']} & "
        f"{overall['prediction_execution_success']} & {_rate(overall['execution_matches'], overall['n'])} \\\\",
        r"\hline",
        r"\end{tabular}",
        r"\end{table}",
        "",
        "% EX counts a predicted result match against executed gold SQL; no native-speaker",
        "% semantic validity is implied. Count and separately disclose gold errors,",
        "% empty-result matches and any difference between all/comparable denominators.",
        f"% Gold reference execution failures: {overall['outcome_categories'].get('gold_reference_execution_error', 0)}",
        f"% Empty-result matches requiring review: {overall['empty_result_matches']}",
    ]
    return "\n".join(table) + "\n"


def make_svg(report: dict) -> str:
    rows = [(LANGUAGE_LABELS[k], v["execution_match_pct_all"] or 0)
            for k, v in report["per_language"].items() if k in LANGUAGE_LABELS]
    if len(rows) != 7:
        raise ValueError("Figure requires all seven IndicDB benchmark languages")
    width, height = 850, 420
    graph_left, graph_top, graph_h = 95, 45, 275
    rects = []
    for index, (label, pct) in enumerate(rows):
        x = graph_left + index * 103
        bar_h = graph_h * pct / 100
        y = graph_top + graph_h - bar_h
        rects.append(f'<rect x="{x}" y="{y:.2f}" width="53" height="{bar_h:.2f}" fill="#384c84" />')
        rects.append(f'<text x="{x+27}" y="{y-7:.2f}" text-anchor="middle" font-size="13">{pct:.1f}%</text>')
        rects.append(f'<text x="{x+27}" y="{graph_top+graph_h+30}" text-anchor="middle" font-size="12">{escape(label)}</text>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        f'<rect width="100%" height="100%" fill="white"/>'
        f'<text x="28" y="25" font-size="18" font-family="sans-serif">Verified IndicDB execution matches by language</text>'
        f'<line x1="{graph_left-10}" y1="{graph_top+graph_h}" x2="{width-25}" y2="{graph_top+graph_h}" stroke="#333"/>'
        f'{"".join(rects)}'
        f'<text x="25" y="390" font-size="12">Rates use all questions per language; verify gold errors before publication.</text>'
        f'</svg>\n'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-queries", type=int, default=280)
    args = parser.parse_args()
    raw = json.loads(args.results.read_text(encoding="utf-8"))
    verify_receipt(args.results, args.receipt, raw)
    if raw.get("experiment_variant") != "full":
        parser.error("Paper main-result tables require the full model variant")
    report = audit_result(raw, expected_queries=args.expected_queries)
    if args.expected_queries == 280:
        expected_languages = set(LANGUAGE_LABELS)
        if set(report["per_language"]) != expected_languages or any(
            m["n"] != 40 for m in report["per_language"].values()
        ):
            parser.error("Sealed 280 run must contain precisely 40 questions in each of seven languages")
    latex = make_latex(report)
    figure = make_svg(report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "verified_metrics.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (args.output_dir / "verified_metrics.tex").write_text(latex, encoding="utf-8")
    (args.output_dir / "verified_language_ex.svg").write_text(figure, encoding="utf-8")
    print(f"Receipt-verified research artifacts: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
