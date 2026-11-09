---
name: qa
description: "Use after implementation and review, before shipping. Proves a data change against a dev target (build, tests, contract checks, comparison with production, freshness) or an infrastructure change (plan review, no-traffic revision smoke test, logs) and writes an evidence report with a verdict."
license: MIT
metadata:
  source: GS@1bd2330:qa/SKILL.md.tmpl
---

# QA

Prove the change works with evidence, not belief. Run the checks, quote
the output, and give a verdict. This skill reports; it does not fix.

## Settings

Read the `## wraith` block of the project's AGENTS.md: `artifacts_dir`
(default `docs/wraith`), `dbt_project_dir`, `dbt_target_dev`,
`gcp_project_dev`, `region`, `terraform_dir`, `dev_max_bytes_billed`.
When a key you need is missing, ask once and suggest `wraith:setup`.

## Choose the branch

- Models, contracts or SQL changed: run the Data branch.
- Terraform, Cloud Run or IAM changed: run the Infra branch.
- Both changed: run both and report each under its own heading.

Everything runs against dev. Anything that touches production, or spends
beyond `dev_max_bytes_billed`, needs the user's explicit go-ahead in
this conversation.

## Data branch

1. List the changed models: `git diff --name-only <base>...HEAD -- <dbt_project_dir>/models`.
2. Build into dev from `dbt_project_dir`: `dbt build --select <changed models>+ --target <dbt_target_dev>`. Match failures per wraith:dbt-bigquery rule 18.
3. Run the contract checks from wraith:odcs-contracts (validate and drift).
4. Compare with production for one recent `ds`, dry-running each comparison first, using [data-diff.md](references/data-diff.md):
   - row counts;
   - key coverage in both directions;
   - the NULL rate per column;
   - the sums of key metrics.
5. Freshness: `dbt source freshness --select source:<touched source> --target <dbt_target_dev>`.
6. Every number in the report states how it was measured.

## Infra branch

1. Run `terraform plan -out=tfplan` in the environment directory. Summarise adds, changes and destroys. Any destroy or replace of a stateful resource makes the verdict FAIL until the user approves it.
2. Cloud Run:
   - Deploy a no-traffic tagged revision in dev (wraith:cloud-run rollout).
   - Smoke-test the tag through the gcloud proxy, which handles authentication: `gcloud run services proxy <service> --tag <tag> --project <project> --region <region> --port 8080 &`, then `curl -fsS http://localhost:8080/healthz`, then stop the proxy with `kill %1`.
   - Read that revision's ERROR logs for the last 10 minutes.
3. List the IAM bindings the change adds or removes.

## Report

Write `<artifacts_dir>/<date>-<topic>/qa.md` with these sections:

- Scope;
- Commands, each with its quoted output;
- Results: a table of check, expected, actual and mechanism;
- Verdict: PASS, PASS WITH NOTES or FAIL.

Use FAIL when any check fails or cannot be run. Use PASS WITH NOTES only
for findings that do not block shipping, and list each one. Do not
round, estimate or recall a number: copy it from the command output.

## Rules

- Never mark a check passed that you did not run.
- A command that errors is a failed check, not a skipped one.
- If the evidence is thin, say so in the verdict and name what is missing.
