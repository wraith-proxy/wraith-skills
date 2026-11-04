import io
import json

import guard
import pytest

CASES = [
    ("terraform-destroy", "terraform destroy", "terraform plan"),
    (
        "terraform-apply-unattended",
        "tofu apply -auto-approve",
        "terraform apply plan.out",
    ),
    (
        "terraform-state-surgery",
        "terraform state rm a.b",
        "terraform state list",
    ),
    ("gcloud-delete", "gcloud run services delete x", "gcloud run deploy x"),
    (
        "storage-recursive-rm",
        "gsutil -m rm -r gs://b/x",
        "gsutil rm gs://b/x",
    ),
    ("bq-rm", "bq rm -f d.t", "bq ls"),
    ("sql-destructive", "bq query 'DROP TABLE d.t'", "bq query 'select 1'"),
    (
        "dbt-full-refresh",
        "dbt run --full-refresh",
        "dbt run --select x",
    ),
    ("git-force-push", "git push --force origin x", "git push origin x"),
    ("git-reset-hard", "git reset --hard HEAD~1", "git reset --soft HEAD~1"),
    ("git-clean-force", "git clean -fd", "git clean -n"),
    ("git-branch-force-delete", "git branch -D x", "git branch -d x"),
    ("dbt-prod-target", "dbt run --target prod", "dbt run --target dev"),
    ("rm-root-or-home", "rm -rf ~", "rm -rf build"),
]


@pytest.mark.parametrize("label,bad,good", CASES)
def test_patterns(label, bad, good):
    hit = guard.decide("shell", bad, "ask", [])
    assert hit is not None and hit[1] == label
    assert guard.decide("shell", good, "ask", []) is None


def test_mcp_patterns():
    hit = guard.decide("mcp", '{"sql": "DROP TABLE a"}', "ask", [])
    assert hit == ("ask", "sql-destructive")
    hit = guard.decide("mcp", '{"target": "prod"}', "ask", [])
    assert hit == ("ask", "dbt-prod-target")


@pytest.mark.parametrize(
    "cmd",
    ['grep -rn "terraform destroy" docs/', 'echo "drop table x"'],
)
def test_guard_ignores_quoted_text(cmd):
    assert guard.decide("shell", cmd, "ask", []) is None


def test_sql_destructive_needs_bq():
    cmd = "bq query 'DROP TABLE d.t'"
    assert guard.decide("shell", cmd, "ask", []) == ("ask", "sql-destructive")
    assert guard.decide("shell", "psql -c 'DROP TABLE t'", "ask", []) is None


def test_guard_catches_mcp_full_refresh():
    payload = {
        "tool_name": "mcp__dbt__build",
        "tool_input": {"full_refresh": True},
    }
    kind, text = guard.extract(payload)
    assert guard.decide(kind, text, "ask", []) == (
        "ask",
        "dbt-full-refresh-mcp",
    )


def test_rm_root_always_denied_in_ask_mode():
    assert guard.decide("shell", "rm -rf /", "ask", []) == (
        "deny",
        "rm-root-or-home",
    )


def test_mode_off_allows_everything():
    assert guard.decide("shell", "rm -rf /", "off", []) is None


def test_deny_mode_returns_deny():
    assert guard.decide("shell", "git reset --hard", "deny", [])[0] == "deny"


def test_extract_variants():
    assert guard.extract({"tool_name": "Read", "tool_input": {}}) is None
    assert guard.extract({"toolName": "skill", "toolArgs": {}}) is None
    assert guard.extract(
        {"toolName": "bash", "toolArgs": '{"command": "ls"}'}
    ) == ("shell", "ls")
    assert guard.extract(
        {"toolName": "bash", "toolArgs": {"command": "ls"}}
    ) == ("shell", "ls")
    assert guard.extract(
        {"tool_name": "powershell", "tool_input": {"command": "ls"}}
    ) == ("shell", "ls")


def test_env_overrides_file(tmp_path):
    (tmp_path / ".wraith").mkdir()
    (tmp_path / ".wraith" / "guard-mode").write_text("deny\n")
    assert guard.mode_for({}, tmp_path) == "deny"
    assert guard.mode_for({"WRAITH_GUARD": "off"}, tmp_path) == "off"
    assert guard.mode_for({"WRAITH_GUARD": "bogus"}, tmp_path) == "deny"
    (tmp_path / ".wraith" / "guard-mode").write_text("junk\n")
    assert guard.mode_for({}, tmp_path) == "ask"
    (tmp_path / ".wraith" / "guard-mode").write_text("")
    assert guard.mode_for({}, tmp_path) == "ask"


def test_project_patterns(tmp_path):
    (tmp_path / ".wraith").mkdir()
    (tmp_path / ".wraith" / "guard-patterns.txt").write_text(
        "# c\n\n(bad\nfoo-bar\n"
    )
    extra = guard._project_patterns(tmp_path)
    assert len(extra) == 1
    assert guard.decide("shell", "run FOO-BAR", "ask", extra) == (
        "ask",
        "project-pattern",
    )
    assert guard.decide("mcp", '{"a": "foo-bar"}', "ask", extra) is not None
    assert guard._project_patterns(tmp_path / "none") == []


def _run(host, payload, env=None):
    out = io.StringIO()
    stdin = io.StringIO(
        payload if isinstance(payload, str) else json.dumps(payload)
    )
    rc = guard.main(["guard.py", host], stdin, out, env or {})
    return rc, out.getvalue()


def test_claude_output_shape(tmp_path):
    rc, out = _run(
        "claude",
        {
            "tool_name": "Bash",
            "tool_input": {"command": "git reset --hard"},
            "cwd": str(tmp_path),
        },
    )
    data = json.loads(out)["hookSpecificOutput"]
    assert rc == 0
    assert data["hookEventName"] == "PreToolUse"
    assert data["permissionDecision"] == "ask"
    assert data["permissionDecisionReason"] == (
        "wraith guard: git-reset-hard (mode ask). Confirm with the user "
        "before running this. Change the mode with wraith:careful."
    )


def test_copilot_output_shape(tmp_path):
    rc, out = _run(
        "copilot",
        {
            "toolName": "bash",
            "toolArgs": {"command": "git reset --hard"},
            "cwd": str(tmp_path),
        },
    )
    data = json.loads(out)
    assert rc == 0
    assert data["permissionDecision"] == "ask"
    assert "hookSpecificOutput" not in data


def test_allow_prints_nothing(tmp_path):
    rc, out = _run(
        "claude",
        {
            "tool_name": "Bash",
            "tool_input": {"command": "ls"},
            "cwd": str(tmp_path),
        },
    )
    assert (rc, out) == (0, "")
    assert _run("claude", {"tool_name": "Read"}) == (0, "")


def test_guard_internal_error_fails_open():
    assert _run("claude", "{not json") == (0, "")


MCP_SAMPLES = {
    "sql-destructive": {"sql": "DROP TABLE a"},
    "dbt-full-refresh-mcp": {"full_refresh": True},
    "dbt-prod-target": {"target": "prod"},
}
REWRITE_KEYS = {"updatedInput", "updated_input", "modifiedArgs"}


def _keys(node):
    if isinstance(node, dict):
        for key, value in node.items():
            yield key
            yield from _keys(value)
    elif isinstance(node, list):
        for item in node:
            yield from _keys(item)


def _decision(data):
    inner = data.get("hookSpecificOutput", data)
    return inner["permissionDecision"]


def _payloads(host, cwd):
    shell = {"claude": "Bash", "copilot": "bash"}[host]
    for label, bad, _ in CASES:
        if host == "claude":
            yield {
                "tool_name": shell,
                "tool_input": {"command": bad},
                "cwd": cwd,
            }
        else:
            yield {
                "toolName": shell,
                "toolArgs": {"command": bad},
                "cwd": cwd,
            }
    if host == "claude":
        for args in MCP_SAMPLES.values():
            yield {
                "tool_name": "mcp__x__y",
                "tool_input": args,
                "cwd": cwd,
            }


def test_every_pattern_every_mode_emits_only_ask_or_deny(tmp_path):
    covered = {c[0] for c in CASES} | set(MCP_SAMPLES)
    assert {label for label, _, _ in guard.PATTERNS} <= covered
    emitted = 0
    for host in ("claude", "copilot"):
        for mode in guard.MODES:
            for payload in _payloads(host, str(tmp_path)):
                rc, out = _run(host, payload, {"WRAITH_GUARD": mode})
                assert rc == 0
                if mode == "off":
                    assert out == ""
                    continue
                assert out != ""
                data = json.loads(out)
                assert _decision(data) in ("ask", "deny")
                assert not REWRITE_KEYS & set(_keys(data))
                emitted += 1
    assert emitted > 0


def test_render_refuses_anything_but_ask_or_deny():
    for host in ("claude", "copilot"):
        for decision in ("allow", "approve", "", None):
            with pytest.raises(Exception):  # noqa: B017
                guard.render(host, decision, "r")
        for decision in ("ask", "deny"):
            assert decision in guard.render(host, decision, "r")


def test_main_prints_nothing_when_decision_is_allow(tmp_path, monkeypatch):
    monkeypatch.setattr(
        guard, "decide", lambda *a, **k: ("allow", "terraform-destroy")
    )
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": "terraform destroy"},
        "cwd": str(tmp_path),
    }
    assert _run("claude", payload) == (0, "")
