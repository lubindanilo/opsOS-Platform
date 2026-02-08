from pathlib import Path

import pytest
from ingestor.csv_io import IngestError, load_events_csv


def test_non_strict_keeps_valid_rows(tmp_path: Path) -> None:
    p = tmp_path / "events.csv"
    # In CSV: to include quotes inside a field, you double them: "".
    p.write_text(
        "event_id,ts,user_id,event_type,properties\n"
        'e1,2026-02-04T10:00:00Z,u1,signup,"{""source"":""ads""}"\n'
        'e2,2026-02-04T10:05:00Z,,page_view,"{""page"":""home""}"\n',
        encoding="utf-8",
    )

    events, errors = load_events_csv(p, strict=False)
    assert len(events) == 1
    assert len(errors) == 1
    assert events[0].event_id == "e1"


def test_strict_raises_on_first_error(tmp_path: Path) -> None:
    p = tmp_path / "events.csv"
    p.write_text(
        'event_id,ts,user_id,event_type,properties\ne1,not-a-date,u1,signup,"{""a"":1}"\n',
        encoding="utf-8",
    )

    with pytest.raises(IngestError):
        load_events_csv(p, strict=True)
