"""PreToolUse guard: ask or deny on destructive shell and MCP calls."""

import json
import os
import re
import sys
from pathlib import Path

MODES = ("ask", "deny", "off")
SHELL = ("shell",)
MCP = ("mcp",)
BOTH = ("shell", "mcp")

PATTERNS = [
    ("terraform-destroy", SHELL, r"\b(terraform|tofu)\s+destroy\b"),
    (
        "terraform-auto-approve",
        SHELL,
        r"\b(terraform|tofu)\s+apply\b[^|;&]*-auto-approve",
    ),
    (
        "terraform-state-surgery",
        SHELL,
        r"\b(terraform|tofu)\s+state\s+(rm|mv)\b",
    ),
    ("gcloud-delete", SHELL, r"\bgcloud\s+(?:[\w-]+\s+){0,5}delete\b"),
    (
        "storage-recursive-rm",
        SHELL,
        (
            r"\b(gcloud\s+storage\s+rm|gsutil\s+(?:-m\s+)?rm)\b"
            r"[^|;&]*\s(-r|-R|--recursive)\b"
        ),
    ),
    ("bq-rm", SHELL, r"\bbq\s+(rm|rmdir)\b"),
    (
        "sql-destructive",
        BOTH,
        (
            r"\b(drop\s+(table|schema|view|external\s+table)"
            r"|truncate\s+table|delete\s+from)\b"
        ),
    ),
    (
        "dbt-full-refresh",
        SHELL,
        r"\bdbt\s+(run|build|seed|snapshot)\b[^|;&]*--full-refresh",
    ),
    ("dbt-full-refresh-mcp", MCP, r'"full_refresh"\s*:\s*true|--full-refresh'),
    (
        "dbt-prod-target",
        BOTH,
        (
            r"(--target|-t)\s+(prod|production|prd)\b"
            r'|"target"\s*:\s*"(prod|production|prd)"'
        ),
    ),
    (
        "git-force-push",
        SHELL,
        r"\bgit\s+push\b[^|;&]*(\s-f\b|--force\b|--force-with-lease\b)",
    ),
    ("git-reset-hard", SHELL, r"\bgit\s+reset\s+--hard\b"),
    ("git-clean-force", SHELL, r"\bgit\s+clean\s+-[a-z]*f"),
    ("git-branch-force-delete", SHELL, r"\bgit\s+branch\s+(?-i:-D)\b"),
    (
        "rm-root-or-home",
        SHELL,
        (
            r"\brm\s+(?:-\w+\s+)*-\w*[rR]\w*\s+(?:-\w+\s+)*"
            r"(?:/|~|\$HOME)/?\*?(?:\s|$)"
        ),
    ),
]
COMPILED = [
    (label, kinds, re.compile(rx, re.IGNORECASE))
    for label, kinds, rx in PATTERNS
]
QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")
BQ = re.compile(r"\bbq\b", re.IGNORECASE)


def extract(payload):
    name = payload.get("tool_name")
    if isinstance(name, str):
        args = payload.get("tool_input") or {}
        if name in ("Bash", "bash", "powershell"):
            return ("shell", str(args.get("command", "")))
        if name.startswith("mcp__"):
            return ("mcp", json.dumps(args))
    name = payload.get("toolName")
    if name in ("bash", "powershell", "shell"):
        args = payload.get("toolArgs") or {}
        if isinstance(args, str):
            args = json.loads(args)
        return ("shell", str(args.get("command", "")))
    return None


def mode_for(env, cwd):
    value = env.get("WRAITH_GUARD")
    if value in MODES:
        return value
    try:
        first = (cwd / ".wraith" / "guard-mode").read_text().splitlines()[0]
        first = first.strip()
        if first in MODES:
            return first
    except (OSError, IndexError):
        pass
    return "ask"


def _project_patterns(cwd):
    found = []
    try:
        lines = (cwd / ".wraith" / "guard-patterns.txt").read_text()
    except OSError:
        return found
    for line in lines.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            found.append(re.compile(line, re.IGNORECASE))
        except re.error:
            continue
    return found


def decide(kind, text, mode, extra):
    if mode == "off":
        return None
    stripped = QUOTED.sub(" ", text) if kind == "shell" else text
    for label, kinds, rx in COMPILED:
        if kind not in kinds:
            continue
        if label == "sql-destructive":
            if kind == "shell" and not BQ.search(stripped):
                continue
            target = text
        else:
            target = stripped
        if rx.search(target):
            if label == "rm-root-or-home":
                return ("deny", label)
            return (mode, label)
    for pattern in extra:
        if pattern.search(text):
            return (mode, "project-pattern")
    return None


def render(host, decision, reason):
    if host == "claude":
        return json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": decision,
                    "permissionDecisionReason": reason,
                }
            }
        )
    return json.dumps(
        {
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    )


def main(argv, stdin, stdout, env):
    try:
        host = argv[1] if len(argv) > 1 else "claude"
        payload = json.loads(stdin.read())
        found = extract(payload)
        if found is None:
            return 0
        kind, text = found
        cwd = Path(payload.get("cwd") or os.getcwd())
        mode = mode_for(env, cwd)
        result = decide(kind, text, mode, _project_patterns(cwd))
        if result is None:
            return 0
        decision, label = result
        reason = (
            f"wraith guard: {label} (mode {mode}). Confirm with the user "
            "before running this. Change the mode with wraith:careful."
        )
        stdout.write(render(host, decision, reason))
    except Exception:  # noqa: BLE001
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv, sys.stdin, sys.stdout, os.environ))
