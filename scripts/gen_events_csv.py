from __future__ import annotations

import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path


def main() -> None:
    out = Path("data/perf/events_1m.csv")
    out.parent.mkdir(parents=True, exist_ok=True)

    n = 1_000_000
    start = datetime(2026, 2, 1, tzinfo=UTC)

    rng = random.Random(42)
    event_types = ["signup", "page_view", "purchase", "logout"]

    with out.open("w", encoding="utf-8", newline="") as f:
        f.write("event_id,ts,user_id,event_type,properties\n")
        for i in range(n):
            ts = start + timedelta(seconds=i)
            user_id = f"u{rng.randint(1, 200_000)}"
            et = rng.choice(event_types)
            props = {"v": rng.randint(1, 100), "src": rng.choice(["ads", "seo", "ref"])}
            # CSV: quotes inside field are doubled
            props_str = json.dumps(props).replace('"', '""')
            f.write(f'e{i},{ts.isoformat()},{user_id},{et},"{props_str}"\n')

    print(f"[OK] wrote {n:,} rows to {out}")


if __name__ == "__main__":
    main()
