"""Merge upstream changes into vendored files and report what needs review."""

from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

COMPANIONS = ("DBT", "GCP", "TF")
SKIP_DIRS = {".git", ".upstream", ".venv", "node_modules"}

RISK_PATTERNS = {
    "dbt-full-refresh": r"--full-refresh",
    "terraform-apply": r"\bterraform\s+(apply|destroy)\b",
    "auto-approve": r"auto-approve",
    "pipe-to-shell": r"curl[^\n]*\|\s*(ba)?sh",
    "rm-recursive": r"\brm\s+-\w*r",
    "no-verify": r"--no-verify",
    "telemetry": r"telemetry|analytics",
    "unpinned-launcher": r"\b(npx|uvx)\s+[\w@/.-]+@latest\b",
    "new-url": r"https?://",
}
RISK_RES = {k: re.compile(v) for k, v in RISK_PATTERNS.items()}

ENTRY = re.compile(r"^([A-Z]+)@([0-9a-f]+):(.+)$")
SOURCE_LINE = re.compile(r"^\s*source:\s*(.+?)\s*$")
COMMENT_SOURCE = re.compile(r"^(?:<!--|#)\s*source:\s*(.+?)\s*(?:-->)?\s*$")

Entry = tuple[str, str, str]


def _entries(value: str) -> list[Entry]:
    value = value.strip().strip("\"'")
    found = []
    for part in value.split(","):
        match = ENTRY.match(part.strip())
        if match:
            found.append((match[1], match[2], match[3]))
    return found


def _file_entries(path: Path) -> list[Entry]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return []
    if path.name == "SKILL.md":
        if not lines or lines[0].strip() != "---":
            return []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            match = SOURCE_LINE.match(line)
            if match:
                return _entries(match[1])
        return []
    head = lines[:2] if lines and lines[0].startswith("#!") else lines[:1]
    for line in head[-1:]:
        match = COMMENT_SOURCE.match(line)
        if match:
            return _entries(match[1])
    return []


def provenance(root: Path) -> dict[str, list[Entry]]:
    found: dict[str, list[Entry]] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if SKIP_DIRS & set(rel.parts) or not path.is_file():
            continue
        entries = _file_entries(path)
        if entries:
            found[rel.as_posix()] = entries
    return found


def merge_file(ours: Path, base: Path, theirs: Path) -> tuple[str, bool]:
    result = subprocess.run(
        ["git", "merge-file", "-p", str(ours), str(base), str(theirs)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode < 0 or result.returncode > 127:
        raise RuntimeError(result.stderr.strip())
    return result.stdout, result.returncode == 0


def risk_scan(diff_text: str) -> list[str]:
    hits = []
    for line in diff_text.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        added = line[1:]
        for label, pattern in RISK_RES.items():
            if pattern.search(added):
                hits.append(f"{label}: {added.strip()}")
    return hits


def _git(directory: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(directory), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _sha(directory: Path) -> str:
    return _git(directory, "rev-parse", "HEAD")


def _ref(directory: Path) -> str:
    return _git(directory, "describe", "--tags", "--exact-match") or "-"


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, NotADirectoryError, UnicodeDecodeError):
        return None


def _diff(old: str, new: str, name: str) -> str:
    return "".join(
        difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            f"a/{name}",
            f"b/{name}",
        )
    )


@dataclass
class Row:
    path: str
    status: str
    hits: list[str] = field(default_factory=list)


@dataclass
class Change:
    key: str
    upstream: str
    diff: str


def _sync_file(
    root: Path, rel: str, entries: list[Entry], old: Path, new: Path
) -> tuple[Row | None, Change | None]:
    changed = []
    for key, _sha7, upath in entries:
        before = _read(old / key / upath)
        after = _read(new / key / upath)
        if before is None or before == after:
            continue
        changed.append((key, upath, before, after))
    if not changed:
        return None, None
    key, upath, before, after = changed[0]
    if len(entries) > 1:
        return Row(rel, "composite"), None
    if after is None:
        return Row(rel, "removed"), None
    diff = _diff(before, after, upath)
    hits = risk_scan(diff)
    change = Change(key, upath, diff)
    ours = root / rel
    with tempfile.TemporaryDirectory() as tmp:
        base_file = Path(tmp) / "base"
        theirs_file = Path(tmp) / "theirs"
        base_file.write_text(before, encoding="utf-8")
        theirs_file.write_text(after, encoding="utf-8")
        merged, clean = merge_file(ours, base_file, theirs_file)
    if not clean:
        return Row(rel, "conflict", hits), change
    old7 = entries[0][1]
    new7 = _sha(new / key)[:7]
    merged = merged.replace(f"{key}@{old7}:{upath}", f"{key}@{new7}:{upath}")
    ours.write_text(merged, encoding="utf-8")
    return Row(rel, "clean", hits), change


def _companion_drift(old: Path, new: Path) -> dict[str, list[Row]]:
    drift: dict[str, list[Row]] = {}
    for key in COMPANIONS:
        if not (new / key).is_dir():
            continue
        if _sha(old / key) == _sha(new / key):
            continue
        rows = []
        for path in sorted((new / key).rglob("SKILL.md")):
            rel = path.relative_to(new / key)
            if ".git" in rel.parts:
                continue
            before = _read(old / key / rel) or ""
            after = _read(path) or ""
            if before != after:
                diff = _diff(before, after, rel.as_posix())
                rows.append(Row(rel.as_posix(), "changed", risk_scan(diff)))
        drift[key] = rows
    return drift


def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def _report(
    pins: list[tuple[str, str, str, str]],
    rows: list[Row],
    changes: dict[str, Change],
    drift: dict[str, list[Row]],
) -> str:
    out = ["# Upstream sync", "", "| KEY | Old ref | New ref | New SHA |"]
    out.append("|---|---|---|---|")
    for key, old_ref, new_ref, sha in pins:
        out.append(f"| {key} | {old_ref} | {new_ref} | {sha} |")
    out += ["", "| File | Status | Hits |", "|---|---|---|"]
    for row in rows:
        hits = "<br>".join(_cell(h) for h in row.hits)
        out.append(f"| {row.path} | {row.status} | {hits} |")
    for rel, change in changes.items():
        out += [
            "",
            "<details>",
            f"<summary>{change.key}:{change.upstream} ({rel})</summary>",
            "",
            "```diff",
            change.diff.rstrip("\n"),
            "```",
            "",
            "</details>",
        ]
    if drift:
        out += ["", "## Companion drift"]
        for key, drows in drift.items():
            out += ["", f"### {key}", ""]
            if not drows:
                out.append("No SKILL.md changes.")
            for row in drows:
                out.append(f"- {row.path}")
                out += [f"  - {_cell(h)}" for h in row.hits]
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old", type=Path, required=True)
    parser.add_argument("--new", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parent.parent
    )
    args = parser.parse_args(argv)

    rows: list[Row] = []
    changes: dict[str, Change] = {}
    blocked: set[str] = set()
    for rel, entries in provenance(args.root).items():
        row, change = _sync_file(args.root, rel, entries, args.old, args.new)
        if row:
            rows.append(row)
            if row.status != "clean":
                blocked.update(key for key, _, _ in entries)
        if change:
            changes[rel] = change
    drift = _companion_drift(args.old, args.new)

    pins = []
    for path in sorted(p for p in args.new.iterdir() if p.is_dir()):
        pins.append(
            (path.name, _ref(args.old / path.name), _ref(path), _sha(path))
        )
    args.report.write_text(
        _report(pins, rows, changes, drift), encoding="utf-8"
    )
    # Pins the workflow may bump: a KEY with any unmerged file keeps its
    # old pin, or the next run would diff from the new one and lose it.
    print(
        " ".join(
            key
            for key, _, _, sha in pins
            if key not in COMPANIONS
            and key not in blocked
            and _sha(args.old / key) != sha
        )
    )

    companion_hits = any(r.hits for d in drift.values() for r in d)
    if any(r.status != "clean" or r.hits for r in rows) or companion_hits:
        return 20
    return 10 if rows else 0


if __name__ == "__main__":
    sys.exit(main())
