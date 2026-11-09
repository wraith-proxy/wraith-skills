---
name: bigquery
description: "Use for BigQuery work outside dbt modelling: query cost and performance, dry runs, bytes and slot analysis, partition pruning, dataset design and location, access control, policy tags, and crypto-shredding personal data."
license: MIT
metadata:
  source: new
---

# BigQuery

## When to use

Use for BigQuery work outside dbt modelling: cost and performance, dry runs, partition pruning, dataset location, access, and crypto-shredding.
Project values come from the `## wraith` block of AGENTS.md: `gcp_project_dev`, `gcp_project_prod`, `bigquery_location`, `dev_max_bytes_billed`, `terraform_dir`. If a key is missing, ask once and suggest wraith:setup.

## Rules

1. BigQuery is OLAP, not OLTP: batch merges, no row-by-row updates, no transactional workloads.
2. Dry-run before running anything over an unfamiliar or large table: `bq query --dry_run --use_legacy_sql=false --project_id=<project> '<sql>'`. Report the bytes, and set `--maximum_bytes_billed` on ad-hoc queries.
3. Every number in a cost or performance answer states its mechanism: which INFORMATION_SCHEMA view, which filter, which period.
4. Filter on the partition column with constants or parameters so pruning works. Large partitioned tables set `require_partition_filter = true`.
5. Select only the columns needed; `SELECT *` bills every column.
6. Dataset location is immutable. Choose it once from `bigquery_location`. Terraform creates datasets; dbt creates tables.
7. Grant access at dataset level to groups or service accounts. No project-level `roles/bigquery.admin` for workloads. Share through authorized views or datasets. Protect classified columns with policy tags or encryption.
8. BYTES columns cannot be partition or cluster keys.
9. The right to be forgotten is a crypto-shred, not a delete ([crypto-shredding.md](references/crypto-shredding.md)).
10. MERGE statements filter the target's partitions to limit scanned bytes.

## Workflow

Cost investigation:

1. Find the top cost by query and by user over 30 days.
2. Attribute each cost to a model, job or person.
3. Propose fixes.
4. Estimate the saving, stating the mechanism.

## Commands

Dry run on the dev project, then the capped run:

```bash
bq query --dry_run --use_legacy_sql=false --project_id=<gcp_project_dev> '<sql>'
bq query --use_legacy_sql=false --project_id=<gcp_project_dev> --maximum_bytes_billed=<dev_max_bytes_billed> '<sql>'
```

Cost queries: substitute `<bigquery_location>` in [cost-queries.md](references/cost-queries.md), then dry-run each one first.
Changes to `gcp_project_prod`, datasets (`terraform_dir`) or spend above the cap need the user's go-ahead in this conversation.

## Vendor skills

These Google skills are companions. Name them, do not copy them. Each is recommended with caveat.

- `bigquery-basics`: wraith:bigquery needs a basic CLI recipe
- `bigquery-optimization`: wraith:bigquery cost and layout review
- `bigquery-troubleshooting`: wraith:bigquery incident and cost-spike diagnosis
- `bigquery-observability`: wraith:bigquery slot, queue and reservation checks
- `bigquery-ai-ml`: wraith:bigquery when the task is BigQuery ML or GenAI SQL
- `bigquery-udfs`: wraith:bigquery when a custom function is asked for
- `datalineage-summary`: wraith:bigquery provenance questions
- `datalineage-bigquery-asset-impact-analysis`: wraith:plan-data-review impact check
- `cloud-logging-query-generation`: wraith:bigquery or wraith:cloud-run log debugging

Telemetry: these skills ask the agent to set an attribution tag that reports usage to Google; tell the user and let them choose.

Where they and this skill disagree, this skill wins for dry runs and cost caps, dataset ownership and location, access, and crypto-shredding (rules 2, 6, 7 and 9). Google publishes its skills from main without release tags, so their commands go through wraith:plan-infra-review before touching shared environments.

## Review checklist

- dry-run bytes stated for new heavy queries
- `require_partition_filter` on large partitioned tables
- no project-level admin grants
- classified columns protected by policy tag or encryption

## When it fails

- "Resources exceeded": reduce sort and window sizes, use approximate aggregates, prune partitions.
- "Quota exceeded": check rate limits, or concurrent DML on one table.
- "bytes billed" limit hit: dry-run the query and prune partitions and columns.
- "Access Denied": name the principal and the missing permission. Use `gcloud projects get-iam-policy <project>` and the IAM Policy Troubleshooter.
- Inspect any job with `bq show -j <job_id>`.

## References

- [cost-queries.md](references/cost-queries.md): four INFORMATION_SCHEMA.JOBS cost queries.
- [crypto-shredding.md](references/crypto-shredding.md): erasure by key deletion; classification comes from wraith:odcs-contracts.
- Related: wraith:dbt-bigquery for tables, wraith:terraform-gcp for datasets.
