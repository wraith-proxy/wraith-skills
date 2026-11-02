import io
import json
from pathlib import Path

import session_start

ROOT = Path(__file__).resolve().parent.parent


def test_router_text_strips_frontmatter():
    text = session_start.router_text(ROOT)
    assert text.startswith("<wraith-router>\nYou have the wraith plugin.")
    assert text.endswith("</wraith-router>")
    assert "license: MIT" not in text
    assert "# Using wraith" in text


def test_router_size_under_8000():
    assert len(session_start.router_text(ROOT)) <= 8000


def _run(host):
    out = io.StringIO()
    rc = session_start.main(["session_start.py", host], out)
    return rc, out.getvalue()


def test_session_start_shapes():
    rc, out = _run("claude")
    data = json.loads(out)["hookSpecificOutput"]
    assert rc == 0
    assert data["hookEventName"] == "SessionStart"
    assert "<wraith-router>" in data["additionalContext"]
    rc, out = _run("copilot")
    assert "<wraith-router>" in json.loads(out)["additionalContext"]


def test_missing_router_fails_open(monkeypatch, tmp_path):
    def boom(root):
        raise FileNotFoundError

    monkeypatch.setattr(session_start, "router_text", boom)
    assert _run("claude") == (0, "")


def test_router_without_frontmatter(tmp_path):
    (tmp_path / "skills" / "using-wraith").mkdir(parents=True)
    (tmp_path / "skills" / "using-wraith" / "SKILL.md").write_text("body\n")
    assert "\nbody\n" in session_start.router_text(tmp_path)
