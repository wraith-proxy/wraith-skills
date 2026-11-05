import os
import subprocess
from pathlib import Path

import pytest
import yaml

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"
AUTO_MERGE = "Enable auto-merge on safe syncs"
STUB_GH = """#!/bin/bash
echo "gh $*" >> "$STUB_LOG"
case "$1 $2" in
  "api repos/"*)
    [ "$RULES" = fail ] && exit 1
    echo "$RULES";;
  "pr view") echo "x";;
  "api graphql") [ "$GQL" = ok ] || exit 1;;
esac
exit 0
"""


def text(name):
    return (WORKFLOWS / name).read_text(encoding="utf-8")


def sync_steps():
    return yaml.safe_load(text("upstream-sync.yml"))["jobs"]["sync"]["steps"]


def sync_step(name):
    return next(s for s in sync_steps() if s.get("name") == name)


def test_ci_has_only_the_test_job():
    assert list(yaml.safe_load(text("ci.yml"))["jobs"]) == ["test"]


def test_ci_does_not_rerun_on_pr_edits():
    assert "edited" not in text("ci.yml")


@pytest.mark.parametrize("name", ["ci.yml", "upstream-sync.yml"])
def test_no_automerge_title_tag(name):
    assert "[automerge]" not in text(name)


def test_sync_auto_merges_only_safe_syncs():
    condition = sync_step(AUTO_MERGE)["if"]
    assert "steps.sync.outputs.code == '10'" in condition
    assert "steps.evals.outputs.ok != 'false'" in condition


def test_sync_auto_merge_uses_the_app_token():
    token = sync_step(AUTO_MERGE)["env"]["GH_TOKEN"]
    assert token == "${{ steps.app.outputs.token }}"


def test_sync_auto_merge_runs_after_the_risk_flag():
    names = [s.get("name") for s in sync_steps()]
    assert names.index("Flag risky syncs") < names.index(AUTO_MERGE)


def test_sync_auto_merge_squashes_with_the_pr_title():
    run = sync_step(AUTO_MERGE)["run"]
    assert "mergeMethod: SQUASH" in run
    assert "commitHeadline: $headline" in run


@pytest.mark.parametrize(
    ("rules", "graphql", "enabled"),
    [
        ("1", "ok", True),
        ("0", "ok", False),
        ("fail", "ok", False),
        ("1", "refused", False),
    ],
)
def test_auto_merge_needs_a_required_check_or_waits_for_review(
    tmp_path, rules, graphql, enabled
):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    gh = bin_dir / "gh"
    gh.write_text(STUB_GH)
    gh.chmod(0o755)
    log = tmp_path / "gh.log"
    log.touch()
    env = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "RULES": rules,
        "GQL": graphql,
        "STUB_LOG": str(log),
        "PR_URL": "https://example.com/pr/1",
        "GITHUB_REPOSITORY": "owner/repo",
    }
    result = subprocess.run(
        ["bash", "-e", "-c", sync_step(AUTO_MERGE)["run"]],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert ("auto-merge enabled" in result.stdout) is enabled
    assert ("--add-label needs-review" in log.read_text()) is not enabled
