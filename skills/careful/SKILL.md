---
name: careful
description: "Use when the user asks for extra caution, is about to work against production, or wants the destructive-command guard changed. Sets the wraith guard to ask, deny or off for this project and explains what it catches."
license: MIT
metadata:
  source: "GS@1bd2330:careful/SKILL.md.tmpl"
---

# Careful

The wraith guard watches shell and MCP calls for destructive commands.

## Modes

- `ask` (the default) prompts before destructive commands.
- `deny` blocks them.
- `off` disables the guard.

## Set a mode

Write the single word to `.wraith/guard-mode` in the project root. The
environment variable `WRAITH_GUARD` overrides the file. Confirm the mode back
to the user after writing it.

## Extra project patterns

Add one Python regex per line to `.wraith/guard-patterns.txt`. Commit this
file so the whole team shares it.

## What it catches

| Label | What it matches |
|---|---|
| terraform-destroy | Terraform or OpenTofu destroy |
| terraform-apply-unattended | Terraform or OpenTofu apply with auto-approve, skipping the plan review |
| terraform-state-surgery | Removing or moving resources in Terraform or OpenTofu state |
| gcloud-delete | Any gcloud command that deletes a resource |
| storage-recursive-rm | Recursive removal of Cloud Storage objects with gcloud storage or gsutil |
| bq-rm | Removing BigQuery tables or datasets with the bq tool |
| sql-destructive | SQL that drops tables, schemas or views, truncates, or deletes rows, in a bq command or an MCP call |
| dbt-full-refresh | A dbt run, build, seed or snapshot with full refresh, which rebuilds incremental tables |
| dbt-full-refresh-mcp | The same full refresh requested through an MCP call |
| dbt-prod-target | Any dbt command or MCP call aimed at the production target |
| git-force-push | A git push with force or force-with-lease |
| git-reset-hard | A git hard reset, which discards local changes |
| git-clean-force | A forced git clean, which deletes untracked files |
| git-branch-force-delete | Force-deleting a git branch |
| rm-root-or-home | Recursive rm of the filesystem root or the home directory |

`rm-root-or-home` is always denied, whatever the mode, unless the mode is
`off`.

Best-effort string matching, not a security boundary.
