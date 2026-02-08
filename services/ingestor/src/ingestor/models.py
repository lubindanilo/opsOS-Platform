from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class Event:
    event_id: str
    ts: datetime
    user_id: str
    event_type: str
    properties: dict[str, Any]
