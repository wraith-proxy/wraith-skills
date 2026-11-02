import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE = ROOT / "hooks" / "hooks.json"
COPILOT = ROOT / "com.github.copilot" / "hooks" / "hooks.json"


def test_claude_hooks_quote_plugin_root():
    hooks = json.loads(CLAUDE.read_text())["hooks"]
    start = hooks["SessionStart"][0]
    pre = hooks["PreToolUse"][0]
    assert start["matcher"] == "startup|clear|compact"
    assert pre["matcher"] == "Bash|mcp__.*"
    for entry in (start, pre):
        cmd = entry["hooks"][0]
        assert cmd["timeout"] == 10
        assert '"${CLAUDE_PLUGIN_ROOT}/hooks/' in cmd["command"]
        assert cmd["command"].startswith("python3 ")


def test_copilot_hooks_fail_open():
    data = json.loads(COPILOT.read_text())
    assert data["version"] == 1
    for entries in data["hooks"].values():
        for entry in entries:
            assert entry["bash"].endswith("|| true")
            assert '"${PLUGIN_ROOT}/hooks/' in entry["bash"]
            assert entry["timeoutSec"] == 10
    pre = data["hooks"]["preToolUse"][0]
    assert pre["matcher"] == "bash|powershell"


def test_hook_scripts_exist():
    assert (ROOT / "hooks" / "guard.py").is_file()
    assert (ROOT / "hooks" / "session_start.py").is_file()
