import re
from pathlib import Path

import pytest
import yaml
from commitizen.version_increment import VersionIncrement

ROOT = Path(__file__).resolve().parent.parent
CZ = yaml.safe_load((ROOT / ".cz.yaml").read_text())["commitizen"]
CUSTOM = CZ["customize"]

RELEASING = ["feature", "fix", "bug", "break"]
NON_RELEASING = ["docs", "chore", "ci", "test", "refactor"]


def subject(kind):
    return f"\U0001f47b {kind}/WSK-00017: add the thing"


def bump(message):
    return VersionIncrement.get_highest_by_messages(
        [message], CUSTOM["bump_pattern"], CUSTOM["bump_map"]
    )


@pytest.mark.parametrize("kind", RELEASING + NON_RELEASING)
def test_schema_pattern_accepts_every_type(kind):
    assert re.match(CUSTOM["schema_pattern"], subject(kind))


def test_schema_pattern_rejects_unknown_type():
    assert not re.match(CUSTOM["schema_pattern"], subject("wip"))


def test_schema_pattern_rejects_bad_ticket():
    bad = "\U0001f47b docs/WSK-1: short ticket"
    assert not re.match(CUSTOM["schema_pattern"], bad)


@pytest.mark.parametrize("kind", RELEASING)
def test_bump_pattern_matches_releasing_types(kind):
    assert re.search(CUSTOM["bump_pattern"], subject(kind))


@pytest.mark.parametrize("kind", NON_RELEASING)
def test_bump_pattern_ignores_non_releasing_types(kind):
    assert not re.search(CUSTOM["bump_pattern"], subject(kind))


@pytest.mark.parametrize(
    ("kind", "expected"),
    [
        ("break", VersionIncrement.MAJOR),
        ("feature", VersionIncrement.MINOR),
        ("fix", VersionIncrement.PATCH),
        ("bug", VersionIncrement.PATCH),
    ],
)
def test_releasing_types_bump_by_their_level(kind, expected):
    assert bump(subject(kind)) == expected


@pytest.mark.parametrize("kind", NON_RELEASING)
def test_non_releasing_types_do_not_bump(kind):
    assert bump(subject(kind)) == VersionIncrement.NONE


def test_release_bot_bump_message_does_not_bump():
    message = (
        CZ["bump_message"]
        .replace("$current_version", "0.5.8")
        .replace("$new_version", "0.5.9")
    )
    assert message.startswith(":ghost: chore: release v0.5.8 -> v0.5.9")
    assert bump(message) == VersionIncrement.NONE


def test_releasing_line_in_docs_body_does_not_bump():
    message = subject("docs") + "\n\n* \U0001f47b fix/WSK-00099: something\n"
    assert bump(message) == VersionIncrement.NONE
