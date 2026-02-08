from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict
from pathlib import Path

from .csv_io import IngestError, load_events_csv
from .models import Event


def _write_jsonl(out_path: Path, events: list[Event]) -> None:
    """
    Write events to a JSONL file: 1 JSON object per line.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        for e in events:
            obj = asdict(e)  # dataclass -> dict
            obj["ts"] = obj["ts"].isoformat()  # datetime -> string for JSON
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    """
    CLI entrypoint: parse terminal arguments and run ingestion.
    """
    parser = argparse.ArgumentParser(
        prog="ingest",
        description="Convert events CSV into canonical JSONL.",
    )
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", required=True, help="Path to output JSONL")
    parser.add_argument("--strict", action="store_true", help="Fail on first error")
    args = parser.parse_args(argv)

    in_path = Path(args.input)
    out_path = Path(args.output)

    t0 = time.perf_counter()
    try:
        events, errors = load_events_csv(in_path, strict=args.strict)
    except IngestError as e:
        print(f"[ERROR] {e}")
        return 1
    dt = time.perf_counter() - t0

    _write_jsonl(out_path, events)

    print(f"[OK] events={len(events)} errors={len(errors)} time={dt:.3f}s output={out_path}")
    if errors:
        print("[WARN] sample errors:")
        for msg in errors[:5]:
            print("  -", msg)

    return 0
