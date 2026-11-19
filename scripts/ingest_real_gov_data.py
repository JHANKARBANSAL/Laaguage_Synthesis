#!/usr/bin/env python3
"""
CLI Script to Ingest Authentic Government of India Open Datasets into IndicSQL.
Populates all 20 NDAP benchmark databases with genuine, authentic data.

Usage:
    uv run python scripts/ingest_real_gov_data.py
    uv run python scripts/ingest_real_gov_data.py --api-key YOUR_DATA_GOV_IN_KEY
"""

import argparse
import sys
from indicsql.schema.ingest_real_gov_data import ingest_all_20_ndap_databases


def main():
    parser = argparse.ArgumentParser(
        description="Ingest authentic Government of India open datasets across all 20 NDAP benchmark tables."
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Optional data.gov.in API key. If omitted, uses public sandbox key or DATA_GOV_IN_API_KEY env var.",
    )

    parser.add_argument(
        "--allow-modeled-data", action="store_true",
        help="Explicitly allow modeled/synthetic development values; never for paper benchmarks.",
    )
    args = parser.parse_args()
    print("Preparing mixed-source NDAP-style DEVELOPMENT data (not official IndicDB benchmark)...")
    summary = ingest_all_20_ndap_databases(\n        api_key=args.api_key, allow_modeled_data=args.allow_modeled_data\n    )

    print("\n📊 Ingestion Results Summary (20 NDAP Tables):")
    total_records = 0
    for table, count in summary.items():
        total_records += count
        print(f"  • {table:<36}: {count:>7} records")
    print(f"\n✨ Total Records Ingested: {total_records:,}")
    print("Mixed-source development datasets updated; these are NOT official benchmark data.")


if __name__ == "__main__":
    main()
