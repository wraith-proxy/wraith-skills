---
name: plan-data-review
description: "Use after a plan touches data: new or changed dbt models, ODCS contracts, BigQuery tables, pipelines or backfills. Reviews grain, keys, contract changes, ds snapshots versus SCD2, idempotency, partitioning, cost, personal data and rollback, then records findings and a verdict in the plan."
license: MIT
metadata:
  source: GS@1bd2330:plan-eng-review/SKILL.md.tmpl
---

# Plan Data Review

## When to use

After wraith:writing-plans, when the plan touches dbt models, ODCS contracts, BigQuery tables, pipelines or backfills.
Runs before wraith:orchestrating-agents.

## Step 0: attack the premise

Before the checklist, ask: does this need to exist, and what already answers it? Look for an existing model, table, contract or metric that serves the consumer. If one does, the finding is a blocker that names it, and the review stops there until the user decides.

## Checklist

1. Consumer and decision named; the cost of wrong, late and down stated.
2. Contract exists or is part of the plan; the change is classified as additive or breaking; an owner is named.
3. Grain stated as "one row per X per ds"; keys and uniqueness scope stated.
4. Temporal model is a `ds` snapshot by default; SCD2 is justified by a regulated audit need.
5. Rerunning one `ds` gives the same output, and the backfill path is written.
6. Partitioning, clustering and `require_partition_filter` set; cost estimated (dry-run bytes times runs per day) against the stated threshold.
7. Personal data: classification, the encryption or crypto-shred path, and access.
8. Quality: tests from contract rules, a freshness SLA, no silent drops.
9. Lineage and blast radius: downstream models and dashboards listed; a consumer notice for breaking changes.
10. Rollback: how to undo it (rebuild from source, restore from time travel, or the previous `ds`).
11. Late-arriving data: how rows that land after their `ds` are handled.

## Output

Append `## Data review (<YYYY-MM-DD>)` to the plan, containing:

| Severity | Item | Finding | Required change |
|---|---|---|---|
| blocker, should or nit | checklist number | what the plan says or omits | the edit to the plan |

Then one verdict line: `Verdict: READY`, `Verdict: READY WITH CHANGES` or `Verdict: NOT READY`.

Blockers are resolved in the plan before wraith:orchestrating-agents runs.

## Workflow

1. Read the `## wraith` block of AGENTS.md: `artifacts_dir`, `contracts_dir`, `dbt_project_dir`, `gcp_project_dev`, `bigquery_location`, `dev_max_bytes_billed`. If a key is missing, ask once and suggest wraith:setup.
2. Read the plan at `<artifacts_dir>/<YYYY-MM-DD>-<topic>/plan.md` and every contract and model it names.
3. Run Step 0.
4. Walk the checklist in order. An item the plan does not address is a finding, never a pass. Use wraith:odcs-contracts for item 2, wraith:dbt-bigquery for items 3 to 5 and 8, and wraith:bigquery for items 6 and 7.
5. For item 6, dry-run each new or changed query and multiply the bytes by runs per day.
6. Run the vendor second pass if installed, and fold its findings into the same table.
7. Append the output section to the plan. Do not edit the rest of the plan; the author resolves the findings.

## Commands

Every value is a wraith block key.

```bash
bq query --dry_run --project_id=<gcp_project_dev> --location=<bigquery_location> --use_legacy_sql=false '<sql>'
bq show --format=prettyjson --project_id=<gcp_project_dev> <dataset>.<table>
dbt ls --project-dir <dbt_project_dir> --select <model>+ --resource-type model exposure
```

The last command lists downstream models and exposures for item 9.

## Vendor skills

Second pass, only when installed. Companion Google skills, recommended with caveat in ADR 0003 and never copied here:

- `datalineage-bigquery-asset-impact-analysis`: use for item 9, the blast radius of a changed table or view.
- `bigquery-optimization`: use for item 6, partitioning, clustering and query cost.

They ask the agent to set an attribution tag that reports usage to Google; tell the user and let them choose. Partition expiry or TTL advice from bigquery-optimization is raised with the user, not added to the plan as a required change.

## References

- wraith:writing-plans for the plan format and location.
- wraith:odcs-contracts, wraith:dbt-bigquery and wraith:bigquery for the rules each item checks against.
- wraith:plan-infra-review when the plan also changes GCP infrastructure.
