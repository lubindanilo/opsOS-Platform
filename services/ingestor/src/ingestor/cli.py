from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from .csv_io import IngestError, load_events_csv
from .models import Event


def _write_jsonl(out_path: Path, events: list[Event], compact_json: bool) -> None:
    """Write events to a JSONL file: 1 JSON object per line."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # If compact_json=True, remove spaces after separators to reduce output size.
    # Otherwise use the default JSON formatting.
    separators = (",", ":") if compact_json else None

    with out_path.open("w", encoding="utf-8") as f:
        for e in events:
            obj = {
                "event_id": e.event_id,
                "ts": e.ts.isoformat(),
                "user_id": e.user_id,
                "event_type": e.event_type,
                "properties": e.properties,
            }
            if separators is None:
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            else:
                f.write(json.dumps(obj, ensure_ascii=False, separators=separators) + "\n")


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint: parse terminal arguments and run ingestion."""
    parser = argparse.ArgumentParser(
        prog="ingest",
        description="Convert events CSV into canonical JSONL.",
    )
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", required=True, help="Path to output JSONL")
    parser.add_argument("--strict", action="store_true", help="Fail on first error")
    parser.add_argument(
        "--max-errors",
        type=int,
        default=50,
        help="Maximum number of errors to collect in non-strict mode",
    )
    parser.add_argument(
        "--show-errors",
        action="store_true",
        help="Print all collected errors (otherwise only the first 5)",
    )
    parser.add_argument(
        "--compact-json",
        action="store_true",
        help="Write JSON without spaces (smaller output, sometimes faster)",
    )
    args = parser.parse_args(argv)

    in_path = Path(args.input)
    out_path = Path(args.output)

    t0 = time.perf_counter()
    try:
        events, errors = load_events_csv(in_path, strict=args.strict, max_errors=args.max_errors)
    except IngestError as e:
        print(f"[ERROR] {e}")
        return 1
    dt = time.perf_counter() - t0

    _write_jsonl(out_path, events, compact_json=args.compact_json)

    print(f"[OK] events={len(events)} errors={len(errors)} time={dt:.3f}s output={out_path}")

    if errors:
        print("[WARN] errors:")
        to_show = errors if args.show_errors else errors[:5]
        for msg in to_show:
            print("  -", msg)
        if (not args.show_errors) and len(errors) > 5:
            print(f"  ... ({len(errors) - 5} more; use --show-errors to print all)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
