#!/usr/bin/env python3
"""Convenience wrapper for the deck-builder Presentation Director."""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    script_path: Path = (
        Path(__file__).resolve().parents[1]
        / "skills"
        / "deck-builder"
        / "scripts"
        / "presentation_director.py"
    )
    runpy.run_path(str(script_path), run_name="__main__")


if __name__ == "__main__":
    main()
