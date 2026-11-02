# Data and infrastructure triage

Run the red loop first. Then use the section for the failing system.

## dbt

- Compile errors happen before any SQL runs; runtime errors come from the warehouse. Read `target/run_results.json` and `logs/dbt.log` for the failing node.
- Match `ERROR creating|ERROR in|Database Error|Compilation Error`, never bare `ERROR`: the summary line prints `ERROR=0` on success.
- Connection problems: run `dbt debug`.
- Rerun just the failing model with `--select <model>` to keep the loop fast.

## BigQuery

- "Resources exceeded": reduce sort and window sizes, use approximate aggregates, prune partitions.
- "Quota exceeded": check rate limits, or concurrent DML on one table.
- "bytes billed" limit hit: dry-run the query and prune partitions and columns.
- "Access Denied": name the principal and the missing permission. Use `gcloud projects get-iam-policy <project>` and the IAM Policy Troubleshooter.
- Inspect any job with `bq show -j <job_id>`.

## Cloud Run

- A revision that will not start: not listening on `$PORT`, wrong image architecture, missing secret access, or a failing startup probe.
- 5xx: read `gcloud logging read 'resource.type="cloud_run_revision" AND severity>=ERROR' --project <p> --freshness=1h`.
- 429: max instances or concurrency is too low for the load.
- Memory limit exceeded: raise the limit or reduce per-request memory.
- Request timeout versus task timeout: services and jobs have different limits; check which one fired.

## Terraform

- A held state lock: find the holder first. Never force-unlock without the user.
- API not enabled: enable it, then rerun the plan.
- Permission denied: the plan principal lacks a role; name it and the permission.
- Drift: run `terraform plan -detailed-exitcode`; exit code 2 means changes are pending.

## Closing rule

One hypothesis at a time; record each with the evidence that ruled it in or out.
