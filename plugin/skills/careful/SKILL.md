---
name: careful
description: "Use when the user asks for extra caution, is about to work against production, or is about to run a destructive command such as terraform destroy, bq rm, a gcloud delete, DROP TABLE, a dbt full refresh or a force push. Makes the agent stop and confirm first."
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

This is an instruction you follow, not a check that runs. Nothing else in
wraith stops the command.

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

This rule is not a security boundary.
