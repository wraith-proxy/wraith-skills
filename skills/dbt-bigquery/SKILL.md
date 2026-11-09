---
name: dbt-bigquery
description: "Use when creating, changing, testing or running dbt models on BigQuery: layering, incremental strategies, ds snapshots, SCD2, partitioning and clustering, sources and freshness, contracts and safe runs against dev targets."
license: MIT
metadata:
  source: new
---

# dbt on BigQuery

## When to use

Creating, changing, testing or running dbt models on BigQuery.
Models are built from an ODCS contract (wraith:odcs-contracts).
Project values come from the `## wraith` block of AGENTS.md.

## Rules

1. dbt is a build system for SQL. The commitment is to the contract, not to dbt.
2. Layers follow the work:
   - raw: source-aligned, generated from the contract, incremental merge with dedup;
   - staging: typed, renamed to contract names, a `ds` snapshot;
   - intermediate: only when logic is reused or complex;
   - marts: consumer-facing, contract enforced.
3. Datestamp first: snapshot models are partitioned on a DATE column `ds`. Each run writes exactly one `ds` with `incremental_strategy='insert_overwrite'`. The value comes from `{{ var('ds') }}` set by the orchestrator, so a backfill is a rerun with an earlier `ds`.
4. SCD2 only for regulated audit trails. Build it by full rebuild from the `ds` snapshots with LEAD over `ds`; never a hand-rolled merge, and no dbt snapshots for new work.
5. Uniqueness on snapshots is tested on `(key, ds)`.
6. Raw dedup uses `incremental_strategy='merge'`, with `unique_key` set to the contract primary key and `row_number()` on the loaded-at column. Read new rows with a lookback window, never a strict greater-than high-water mark.
7. Always set `partition_by` (DATE or TIMESTAMP, never BYTES) and `cluster_by` (at most 4 columns used in filters and joins).
8. Incremental models set `on_schema_change='fail'`.
9. Full rebuild (`table`) until scan cost is measurably too high; state the cost threshold in the model's description. `dbt run --full-refresh` is the migration story for anything rebuildable from source. Raw tables that cannot be rebuilt set `full_refresh: false`.
10. Marts set `contract: {enforced: true}` with a `data_type` per column.
11. Tests come from the contract quality rules. Add dbt unit tests for non-trivial logic. Every source with an SLA has freshness configured.
12. Orphans surface as NULLs (LEFT JOIN to optional relations). A silently dropped row is invisible corruption.
13. Ratios use `SAFE_DIVIDE`.
14. A metric is defined in one model; dashboards read it and never redefine it.
15. Build at the most granular meaningful grain and aggregate late.
16. Agents run dbt only against `dbt_target_dev`, with `maximum_bytes_billed` set to `dev_max_bytes_billed` in that profile. `dbt_target_prod` runs happen only through wraith:deploy, with the user's go-ahead.
17. Run dbt from `dbt_project_dir`. `target/`, `logs/` and `dbt_packages/` are gitignored. CI runs `dbt deps` before `dbt build`.
18. When scanning dbt output, match `ERROR creating|ERROR in|Database Error|Compilation Error`, never bare `ERROR`.
19. After changing an extract, run `dbt test --select source:<name>` on a real sample before any full rebuild.
20. No hardcoded date literals in models; use vars or `ds`.

## Workflow

1. Read the `## wraith` block of AGENTS.md. If `dbt_project_dir`,
   `dbt_target_dev`, `dbt_target_prod`, `dev_max_bytes_billed`,
   `gcp_project_dev`, `bigquery_location` or `contracts_dir` is missing, ask
   once and suggest wraith:setup.
2. Read the contract in `<contracts_dir>`; mapping to models and tests is in
   wraith:odcs-contracts.
3. Write the test first, following `references/data-tests.md`:
   contract-derived tests and a unit test for non-trivial logic.
4. Write the model in its layer using the patterns in `references/patterns.md`.
5. Run against `<dbt_target_dev>` only, from `<dbt_project_dir>`.
6. Scan output with the rule 18 pattern; fix and rerun.
7. Production runs go through wraith:deploy with the user's go-ahead.

## Commands

All run from `<dbt_project_dir>`. `dbt deps` downloads packages from the
network; the agent runs it visibly, never from a hook.

- `dbt deps`
- `dbt build --target <dbt_target_dev> --select <model>+ --vars '{ds: <YYYY-MM-DD>}'`
- `dbt test --target <dbt_target_dev> --select source:<name>`
- `dbt source freshness --target <dbt_target_dev>`
- `dbt run --target <dbt_target_dev> --select <model> --full-refresh` (rule 9 only)

## dbt Labs skills

When dbt Labs' dbt plugin is installed, use its skills for generic dbt mechanics:

- `running-dbt-commands`: any dbt command run from a wraith skill.
- `using-dbt-for-analytics-engineering`: everyday dbt model work.
- `adding-dbt-unit-test`: test-first work on a dbt model, beside `references/data-tests.md`.
- `maintaining-dbt-documentation`: backfilling model and column descriptions, with review.

Where they and this skill disagree, this skill wins for contract-first models, ds snapshots and SCD2, BigQuery cost guards and production safety (rules 3, 4, 9 and 16).

## Review checklist

- grain stated in the model description
- no `SELECT *` in models
- partition filter on large sources
- `SAFE_DIVIDE` for ratios
- optional relations use LEFT JOIN, so orphans surface as NULL
- incremental models set `on_schema_change: fail`
- no hardcoded date literals (use vars or `ds`)
- a test for every contract quality rule
- marts have the contract enforced

## When it fails

- Compile errors happen before any SQL runs; runtime errors come from the warehouse. Read `target/run_results.json` and `logs/dbt.log` for the failing node.
- Match `ERROR creating|ERROR in|Database Error|Compilation Error`, never bare `ERROR`: the summary line prints `ERROR=0` on success.
- Connection problems: run `dbt debug`.
- Rerun just the failing model with `--select <model>` to keep the loop fast.

## References

- [Patterns](references/patterns.md): raw merge, `ds` snapshot, SCD2 rebuild, dev profile.
- [CI](references/ci.md): `dbt deps`, slim build, Workload Identity Federation.
- [Data tests](references/data-tests.md): generic tests from contract rules, unit tests, golden files, backtests.
