# wraith-skills

wraith is a plugin of skills and agents for data and infrastructure
engineering on GCP, run as a plan, build, review, ship sprint.
It serves Claude Code and GitHub Copilot from one repository.

## Commands

- `uv sync`
- `uv run pytest`
- `uv run python scripts/lint_skills.py`
- `uv run python scripts/build_copilot.py`
- `uv run python scripts/privacy_scan.py`
- `claude plugin validate --strict .`
- `claude plugin eval .`

## Rules

PLAN.md section 3 (Global constraints) applies to every change.

- Portable frontmatter only (G5).
- No em dash (G8).
- Never edit `com.github.copilot/agents/` (G19).
- Commit format `👻 <type>/WSK-<5 digits>: <summary>` (G4).
- No private data (G12).
