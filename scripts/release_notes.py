"""Build the final release notes from generated notes and RELEASE_NOTES.md."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

HEADING = "## What changes for you"
PIN_LINE = "- Companion pins updated to reviewed refs"
RELEASING = ("### Features", "### Breaking Changes")
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
PIN_BUMP = re.compile(r"^- .*companion pin", re.IGNORECASE)


def _group_pins(generated: str) -> str:
    out: list[str] = []
    for line in generated.splitlines():
        if PIN_BUMP.match(line):
            if PIN_LINE not in out:
                out.append(PIN_LINE)
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if generated.endswith("\n") else "")


def build_notes(generated: str, user_notes: str | None) -> str:
    generated = _group_pins(generated)
    user = COMMENT.sub("", user_notes or "").strip()
    lines = generated.splitlines()
    if not user or not any(h in lines for h in RELEASING):
        return generated
    return f"{HEADING}\n\n{user}\n\n{generated}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generated", required=True, type=Path)
    parser.add_argument("--user", type=Path)
    args = parser.parse_args(argv)
    user = args.user.read_text() if args.user else None
    print(build_notes(args.generated.read_text(), user), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
