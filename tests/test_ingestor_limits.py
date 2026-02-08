from pathlib import Path

from ingestor.csv_io import load_events_csv


def test_max_errors_limits_collected_errors(tmp_path: Path) -> None:
    p = tmp_path / "events.csv"
    p.write_text(
        "event_id,ts,user_id,event_type,properties\n"
        'e1,not-a-date,u1,signup,"{""a"":1}"\n'
        'e2,not-a-date,u1,signup,"{""a"":1}"\n'
        'e3,not-a-date,u1,signup,"{""a"":1}"\n',
        encoding="utf-8",
    )

    events, errors = load_events_csv(p, strict=False, max_errors=1)
    assert len(events) == 0
    assert len(errors) == 1
