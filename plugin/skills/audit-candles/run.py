#!/usr/bin/env python3
"""Read-only local CLI entry point for the bundled educational engine."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "runtime" / "src"))
from candleaudit.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
