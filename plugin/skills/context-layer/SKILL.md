---
name: context-layer
description: "Use when preparing a warehouse for AI agents or text-to-SQL: grain and metric definitions, vetted question-to-SQL pairs, freshness SLAs, curated docs and health checks, so agents query correctly instead of guessing from schemas."
license: MIT
metadata:
  source: new
---

# Context Layer

## When to use

Preparing a warehouse for AI agents or text-to-SQL.
Covers per-domain datasets, vetted question-to-SQL pairs, docs, freshness and health checks.

## Rules

1. The goal: agents query the warehouse correctly instead of guessing from schemas.
2. Organise context per domain as a cluster of three things:
   - datasets: tables with schema and profiling (cardinality, sample values, partitioning);
   - pairs: vetted question-to-SQL examples;
   - docs: terminology, gotchas, and definitions that vary by team.
   Each cluster has a named owner.
3. Curation over automation: mined query history is only a candidate source, and an expert accepts every pair. Expect to reject most candidates.
4. Every table states its grain ("one row per X per ds"). Every metric names its canonical definition. Freshness SLAs state the behaviour on breach. Lineage acts as a control: downstream consumption blocks on upstream breakage.
5. Semantic layer first: when one exists (for example dbt's Semantic Layer), route metric questions through it, and fall back to raw SQL only when it does not cover the question.
6. Prefer a flat, curated index over embeddings or graph traversal when the job is picking the right document.
7. Each cluster carries a health check: tests and freshness passing, pairs still valid after schema changes, answers reproducible.
8. Context lives in `context_dir` as `<domain>/datasets.md`, `<domain>/pairs.yaml` and `<domain>/docs.md`.

## Workflow

1. Read the `## wraith` block of AGENTS.md: `context_dir`, `gcp_project_dev`, `bigquery_location`, `dev_max_bytes_billed`, `contracts_dir`, `glossary`, `ontology_file`. If a key is missing, ask once and suggest wraith:setup.
2. Pick one domain and name its owner (rule 2). Create `<context_dir>/<domain>/` if absent.
3. Write `datasets.md`: per table its grain, keys, partitioning and clustering, freshness SLA with breach behaviour, and profiling from the commands below. Take grain, owner and SLA from the ODCS contract in `<contracts_dir>` when one exists (rule 4).
4. Write `docs.md`: terms that vary by team, gotchas, and the canonical definition of each metric, linking to the semantic layer, `<glossary>` or `<ontology_file>` instead of restating them (rule 5).
5. Collect candidate pairs from expert questions and, optionally, query history. Add each as `status: proposed` in `pairs.yaml` by [references/pairs-format.md](references/pairs-format.md). The owner accepts or retires each one (rule 3).
6. Dry-run every accepted pair and record the health score (rule 7). Wire the dry run into CI.
7. Keep a flat index: one line per domain in `<context_dir>/README.md` naming its owner and files (rule 6).

## Commands

Every value is a wraith block key.

```bash
bq show --format=prettyjson --project_id=<gcp_project_dev> <dataset>.<table>
bq query --project_id=<gcp_project_dev> --location=<bigquery_location> --use_legacy_sql=false --maximum_bytes_billed=<dev_max_bytes_billed> 'SELECT COUNT(DISTINCT <key>) FROM `<dataset>.<table>` WHERE ds = CURRENT_DATE()'
bq query --dry_run --project_id=<gcp_project_dev> --location=<bigquery_location> --use_legacy_sql=false '<pair sql>'
```

## Vendor skills

Companion Google skills, installed separately and never copied here. Recommended with caveat, and only when the user already runs a Gemini Data Analytics agent or Knowledge Catalog:

- `context-engineering-workflow` (db-context-engineering plugin): use as the entry point for setup, evaluation and hill-climbing of a ContextSet.
- `context-generation-guide` (db-context-engineering plugin): use as the authoring reference for templates, facets and value searches.
- `knowledge-catalog` plugin: use for Knowledge Catalog (Dataplex) metadata lookups.

The db-context-engineering skills run generated SQL against the user's database and store connection details in `tools.yaml`; the knowledge-catalog plugin downloads and runs an npm package each session. Tell the user before either runs.

Where they and this skill disagree, this skill wins for expert acceptance of every pair and the files in `context_dir` as the source of truth (rules 3 and 8).

## References

- [references/pairs-format.md](references/pairs-format.md): `pairs.yaml` fields, the CI dry-run check and the health score.
- [references/example-pairs.yaml](references/example-pairs.yaml): two pairs.
