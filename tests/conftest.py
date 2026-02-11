from __future__ import annotations

import sys
from pathlib import Path

# Add monorepo service source folder to Python import path
ROOT = Path(__file__).resolve().parents[1]
INGESTOR_SRC = ROOT / "services" / "ingestor" / "src"
sys.path.insert(0, str(INGESTOR_SRC))
