from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ingest", description="OpsOS ingestor CLI")
    parser.add_argument("--input", help="Path to input file")
    parser.add_argument("--output", help="Path to output file")
    parser.add_argument("--strict", action="store_true", help="Fail on first error")
    parser.parse_args(argv)
    print("[OK] CLI is wired correctly.")
    return 0
