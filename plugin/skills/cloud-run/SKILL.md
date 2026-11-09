---
name: cloud-run
description: "Use when building, deploying or operating a Cloud Run service or job: containers, service accounts, secrets, scaling, timeouts, ingress and auth, revisions and traffic splits, scheduled jobs such as dbt runs, smoke tests and rollback."
license: MIT
metadata:
  source: new
---

# Cloud Run

## When to use

Building, deploying or operating a Cloud Run service or job on GCP.
Covers images, identity, secrets, limits, rollout, rollback and scheduled dbt jobs.

## Rules

1. Use a Service for request-driven HTTP and a Job for run-to-completion batch work (dbt builds, ingestion). Schedule jobs with Cloud Scheduler calling the Jobs API, or with Workflows when steps depend on each other.
2. One service account per service or job, granted only what it uses (for dbt: `roles/bigquery.jobUser` on the project and `roles/bigquery.dataEditor` on the datasets it writes). Never the default compute service account.
3. Secrets come from Secret Manager, referenced by version and mounted as environment variables or files. Never put them in images, env files or plain Terraform variables.
4. Default to `--no-allow-unauthenticated`. Callers get `roles/run.invoker` or go through IAP. `allUsers` only for endpoints the plan names as public.
5. Images:
   - a base image pinned by digest;
   - `uv sync --frozen`;
   - a non-root user;
   - listen on `$PORT`;
   - exit cleanly on SIGTERM within 10 seconds;
   - log JSON to stdout with a `severity` field.
6. Images live in Artifact Registry in the service's region, tagged with the git SHA; deploys reference the digest.
7. Set every limit explicitly:
   - services: CPU, memory, concurrency, max instances (the cost cap), min instances (0 unless cold starts hurt) and request timeout;
   - jobs: task count, parallelism, max retries and task timeout.
   Jobs are idempotent: a retried task produces the same result.
8. Rollout:
   - Write the rollback command first: `gcloud run services update-traffic <service> --to-revisions <previous>=100`.
   - Deploy with `--no-traffic --tag candidate` and smoke-test the tag URL.
   - Then move traffic to 10, 50 and 100 percent, watching errors and latency.
9. A `/healthz` endpoint answers without touching dependencies. Alert on the 5xx rate from logs.
10. When `deploy_method` is `terraform`, the service definition lives in Terraform; `gcloud run deploy` is only for spikes or the image update step.
11. Every gcloud command passes `--project` and `--region` explicitly.
12. The region comes from `region` in the wraith block and matches the BigQuery dataset location for data workloads.

## Workflow

1. Read the `## wraith` block of AGENTS.md: `gcp_project_dev`, `gcp_project_prod`, `region`, `deploy_method`, `terraform_dir`, `dbt_target_dev`, `dbt_target_prod`, `bigquery_location`. If a key is missing, ask once and suggest wraith:setup.
2. Choose Service or Job (rule 1) and create its dedicated service account (rule 2).
3. Build the image, pin the base by digest, push to Artifact Registry tagged with the git SHA (rules 5 and 6).
4. Set all limits (rule 7). For a dbt job follow [references/dbt-job.md](references/dbt-job.md).
5. If `deploy_method` is `terraform`, change the definition in `<terraform_dir>` and plan it with wraith:terraform-gcp; otherwise use gcloud.
6. Roll out a service by [references/rollout.md](references/rollout.md). Production changes need the user's go-ahead in this conversation.
7. Check `region` matches `bigquery_location` for data workloads (rule 12) and review the plan with wraith:plan-infra-review if it adds spend or IAM.

## Commands

Every value is a wraith block key. Replace `<project>` with `<gcp_project_dev>` or `<gcp_project_prod>`.

```bash
gcloud run services describe <service> --project <project> --region <region>
gcloud run jobs execute <job> --project <project> --region <region> --wait
gcloud run revisions list --service <service> --project <project> --region <region>
```

For the deploy flow see wraith:deploy.

## Vendor skills

Companion Google skills, installed separately and never copied here:

- `cloud-run-basics`: use for deploying and running Cloud Run services, jobs and worker pools.
- `cloud-build-basics`: use for Cloud Build concepts, triggers and manual build runs.
- `cloud-run-alert-configuration`: use for Terraform PromQL alert policies for Cloud Run (with wraith:terraform-gcp).

Some of these skills add an attribution tag to what they generate. Tell the user and let them choose whether to keep it.

Where they and this skill disagree, this skill wins for identity, secrets, private-by-default ingress and the rollout (rules 2, 3, 4 and 8).

## Review checklist

- a dedicated service account
- no `allUsers` invoker unless the plan says public
- secrets from Secret Manager
- max instances set
- image deployed by digest
- health endpoint does not touch dependencies

## When it fails

- A revision that will not start: not listening on `$PORT`, wrong image architecture, missing secret access, or a failing startup probe.
- 5xx: read `gcloud logging read 'resource.type="cloud_run_revision" AND severity>=ERROR' --project <p> --freshness=1h`.
- 429: max instances or concurrency is too low for the load.
- Memory limit exceeded: raise the limit or reduce per-request memory.
- Request timeout versus task timeout: services and jobs have different limits; check which one fired.

## References

- [references/dbt-job.md](references/dbt-job.md): Dockerfile, profiles.yml, job commands and Scheduler trigger for a dbt Cloud Run Job (see also wraith:dbt-bigquery).
- [references/rollout.md](references/rollout.md): build, no-traffic deploy, smoke test, traffic steps, rollback, error-log query.
