from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .models import Event


class IngestError(Exception):
    """Error raised when ingestion fails."""


def _parse_ts(value: str) -> datetime:
    v = value.strip()
    # support ISO timestamps like 2026-02-04T10:00:00Z
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    dt = datetime.fromisoformat(v)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt


def load_events_csv(
    path: Path, *, strict: bool = False, max_errors: int = 50
) -> tuple[list[Event], list[str]]:
    """
    Read events from a CSV file and return (events, errors).

    strict=True  -> stop at first error (raise IngestError)
    strict=False -> keep going and collect errors (up to max_errors)
    """
    if not path.exists():
        raise IngestError(f"Input file not found: {path}")

    events: list[Event] = []
    errors: list[str] = []

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"event_id", "ts", "user_id", "event_type", "properties"}

        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise IngestError(
                f"CSV must contain columns: {sorted(required)}; got: {reader.fieldnames}"
            )

        for line_no, row in enumerate(reader, start=2):  # header is line 1
            try:
                event_id = (row["event_id"] or "").strip()
                user_id = (row["user_id"] or "").strip()
                event_type = (row["event_type"] or "").strip()
                ts = _parse_ts(row["ts"] or "")

                props_raw = (row["properties"] or "").strip()
                properties: dict[str, Any]
                if props_raw == "":
                    properties = {}
                else:
                    obj = json.loads(props_raw)
                    if not isinstance(obj, dict):
                        raise ValueError("properties must be a JSON object")
                    properties = obj

                if not event_id or not user_id or not event_type:
                    raise ValueError("event_id, user_id, event_type must be non-empty")

                events.append(
                    Event(
                        event_id=event_id,
                        ts=ts,
                        user_id=user_id,
                        event_type=event_type,
                        properties=properties,
                    )
                )
            except Exception as e:
                msg = f"line {line_no}: {type(e).__name__}: {e}"
                if strict:
                    raise IngestError(msg) from e
                errors.append(msg)
                if len(errors) >= max_errors:
                    break

    return events, errors
