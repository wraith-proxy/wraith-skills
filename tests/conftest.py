import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
for sub in ("hooks", "scripts"):
    sys.path.insert(0, str(ROOT / sub))


@pytest.fixture(autouse=True)
def isolate_git(monkeypatch):
    """Keep tests' git calls inside their own temp repos.

    A git hook (pre-commit runs pytest from one) exports GIT_DIR and
    friends. Inherited, they point a test's `git -C tmp init` and commits
    at the developer's real repository: commits, tags and config land
    there, and from a linked worktree the repo can turn bare (#95).
    """
    for name in [n for n in os.environ if n.startswith("GIT_")]:
        monkeypatch.delenv(name)
