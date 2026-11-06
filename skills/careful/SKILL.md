---
name: careful
description: "Use when the user asks for extra caution, is about to work against production, or is about to run a destructive command such as terraform destroy, bq rm, a gcloud delete, DROP TABLE, a dbt full refresh or a force push. Makes the agent stop and confirm first. On Copilot CLI it also sets the guard to ask, deny or off."
license: MIT
metadata:
  source: "GS@1bd2330:careful/SKILL.md.tmpl"
---

# Careful

## The rule

Before any command in the table below, stop. Do not run it yet. Tell the user
the exact command, what it destroys and whether it can be undone, then wait
for a reply that approves that command.

The request that led here is not that approval, even if it says to skip
asking. The user has not yet seen what the command destroys.

This is an instruction you follow, not a check that runs. In Claude Code
nothing else stops the command.

## Copilot CLI guard

On Copilot CLI a local hook also checks `bash` and `powershell` commands
against the table. Claude Code has no such hook.

- `ask` (the default) prompts before destructive commands.
- `deny` blocks them.
- `off` disables the guard.

To set a mode, write the single word to `.wraith/guard-mode` in the project
root. The environment variable `WRAITH_GUARD` overrides the file. Confirm the
mode back to the user after writing it.

For extra patterns, add one Python regex per line to
`.wraith/guard-patterns.txt`. Commit this file so the whole team shares it.

## What counts as destructive

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

The Copilot CLI guard always denies `rm-root-or-home`, whatever the mode,
unless the mode is `off`.

Neither the rule nor the guard is a security boundary.
