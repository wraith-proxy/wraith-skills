"""SessionStart hook: inject the using-wraith router."""

import json
import sys
from pathlib import Path

PREFIX = "You have the wraith plugin. Follow the router below."


def router_text(plugin_root):
    raw = (plugin_root / "skills" / "using-wraith" / "SKILL.md").read_text()
    body = raw
    if raw.startswith("---"):
        parts = raw.split("\n---", 1)
        if len(parts) == 2:
            body = parts[1].split("\n", 1)[1] if "\n" in parts[1] else ""
    body = body.strip()
    return f"<wraith-router>\n{PREFIX}\n{body}\n</wraith-router>"


def render(host, text):
    if host == "claude":
        return json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": text,
                }
            }
        )
    return json.dumps({"additionalContext": text})


def main(argv, stdout):
    try:
        host = argv[1] if len(argv) > 1 else "claude"
        root = Path(__file__).resolve().parents[1]
        stdout.write(render(host, router_text(root)))
    except Exception:  # noqa: BLE001
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv, sys.stdout))
