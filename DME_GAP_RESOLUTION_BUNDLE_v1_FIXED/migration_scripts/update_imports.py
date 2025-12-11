"""Template helper to update Python import paths when migrating to the monorepo.

Searches for old-style imports and rewrites them to the new `services.*` layout.
This is intentionally conservative and should be reviewed before running.
"""

from __future__ import annotations

import re
from pathlib import Path


PATTERNS = [
    (re.compile(r"from\s+dme_core_v5\b"), "from services.dme_core_v5"),
]


def rewrite_file(path: Path) -> None:
    text = path.read_text()
    original = text
    for pattern, repl in PATTERNS:
        text = pattern.sub(repl, text)
    if text != original:
        print(f"Rewriting imports in {path}")
        path.write_text(text)


def main(root: str = "dme-platform") -> None:
    for p in Path(root).rglob("*.py"):
        rewrite_file(p)


if __name__ == "__main__":
    main()
