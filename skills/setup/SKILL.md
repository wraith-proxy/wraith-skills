---
name: setup
description: "Use once per repository before relying on the other wraith skills, or when the user asks to configure wraith. Records the project's commands, GCP projects, dbt targets and conventions in an AGENTS.md wraith block that every wraith skill reads, and recommends vendor companions."
license: MIT
metadata:
  source: MP@d1478fc:skills/engineering/setup-matt-pocock-skills/SKILL.md
---

# Setup

Scaffold the per-repo configuration that the other wraith skills read. This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Detect

Look at the current repo. Read whatever exists; don't assume:

- `dbt_project.yml`
- `*.tf`
- `Dockerfile`
- `pyproject.toml`
- `.github/workflows/`
- YAML files with `apiVersion: v3` (ODCS contracts)
- ontology YAML
- existing `AGENTS.md` and `CLAUDE.md`

### 2. Ask

Summarise what is present and what is missing. For each missing key, ask one question at a time, proposing the detected value. Lead with the recommended answer so the user can accept it in a word.

### 3. Write

Show the user a draft, let them edit, then write or update this block in `AGENTS.md` (creating `AGENTS.md` if needed). The values below are examples:

```markdown
## wraith
<!-- Read by the wraith plugin. Edit freely. -->
- test_command: uv run pytest
- lint_command: uv run ruff check .
- release_tooling: commitizen; CI bumps the version on merge
- artifacts_dir: docs/wraith
- knowledge_dir: .claude/knowledge
- glossary: GLOSSARY.md
- adr_dir: docs/adr
- gcp_project_dev: example-project-dev
- gcp_project_prod: example-project-prod
- region: europe-west2
- bigquery_location: europe-west2
- dbt_project_dir: dbt
- dbt_target_dev: dev
- dbt_target_prod: prod
- dev_max_bytes_billed: 10000000000
- contracts_dir: contracts
- ontology_file: ontology/ontology.yaml
- context_dir: context
- deploy_method: terraform
- terraform_dir: infra
```

### 4. CLAUDE.md

If `CLAUDE.md` is missing, create it containing `@AGENTS.md`. If it exists without that import, append the line `@AGENTS.md`.

### 5. Guard mode

Add `.wraith/guard-mode` to `.gitignore`.

### 6. Companions

Recommend missing companions. Never install anything yourself. For each one, recommend the companion and tell the user to install it with the commands in the wraith README's Companions section, after skimming its SKILL.md first:

- `dbt_project.yml` present and no `using-dbt-for-analytics-engineering` skill listed: dbt Labs' dbt plugin.
- `*.tf` files present and no `terraform-style-guide` skill listed: HashiCorp's terraform plugin.
- BigQuery in use (`dbt-bigquery`, `google-cloud-bigquery` or `bq` in the repo) and no `bigquery-basics` skill listed: Google's BigQuery skills.
- A Cloud Run service or job defined and no `cloud-run-basics` skill listed: Google's `cloud-run-basics`.

### 7. Issue trackers

Do not create issue-tracker files.
