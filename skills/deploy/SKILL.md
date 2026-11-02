---
name: deploy
description: "Use when deploying to a shared or production GCP environment: Cloud Run rollouts with traffic splitting, production dbt runs, and the post-deploy watch on errors, latency, freshness and row counts, with the rollback written before traffic moves."
license: MIT
metadata:
  source: GS@1bd2330:land-and-deploy/SKILL.md.tmpl, GS@1bd2330:canary/SKILL.md.tmpl
---

# Deploy

Move a verified change into a shared or production environment, watch it, and leave a record. Nothing here is improvised: the rollback exists before traffic moves, and every step that touches production waits for the user's go.

## Settings

Read the `## wraith` block of the project's `AGENTS.md`. Keys used here: `artifacts_dir` (default `docs/wraith`), `gcp_project_prod`, `region`, `dbt_target_prod`, `deploy_method`, `terraform_dir`. When a key is missing, ask once and suggest `wraith:setup`. Never hardcode project ids, regions or job names; use the values from the block.

`deploy.md` and `qa.md` live in `<artifacts_dir>/<YYYY-MM-DD>-<topic>/`.

## Preconditions

- the change is merged to main;
- qa.md has verdict PASS or PASS WITH NOTES;
- the rollback command is written in deploy.md;
- the user said go in this conversation.

If any is missing, stop.

Check each one, do not assume it. Read `qa.md` for the verdict. Confirm the merge with `git log` on main. If `qa.md` is absent, suggest `wraith:qa`. A go from an earlier conversation does not count: ask again, naming what will change in production.

## Cloud Run service

- Follow the wraith:cloud-run rollout.
- Hold 10 percent for 10 minutes, 50 percent for 10 minutes, then 100 percent, watching the 5xx rate, p95 latency and ERROR logs at each step.
- On a breach, roll back immediately, then use wraith:systematic-debugging.

The rollout is: write the rollback, deploy the image by digest with `--no-traffic` and a tag, smoke test the tag URL, then shift traffic. Use `<service>`, `<gcp_project_prod>` and `<region>` from the settings.

At each step, before moving to the next percentage, record:

| Signal | Where | Breach |
|---|---|---|
| 5xx rate | Cloud Monitoring request count by response class | Above the baseline recorded before the rollout |
| p95 latency | Cloud Monitoring request latencies | Clearly above baseline for the whole hold |
| ERROR logs | `gcloud logging read` filtered to the new revision | New error signatures not seen on the previous revision |

State the baseline numbers before shifting any traffic, so a breach is a comparison and not a feeling. A breach means roll back first and ask questions after. The rollback is one traffic command back to the previous revision; run the exact command written in deploy.md.

## dbt production run

1. Update the Cloud Run Job image and execute it once with `--wait`.
2. Check the execution status and logs.
3. Run `dbt test` and `dbt source freshness` against prod, through the job or the CI path the project defines.
4. Compare today's row counts with the previous `ds`. A difference above the threshold stated in the plan pauses for the user.

Details:

- The job is `<job>` in `<gcp_project_prod>` and `<region>`. The target is `dbt_target_prod`. Follow the job pattern in wraith:cloud-run.
- Pin the image by digest. Record the previous digest in deploy.md as part of the rollback.
- Do not run the job against prod from a local shell unless the project defines that path.
- A failed execution is not retried blindly. Read the logs, then use wraith:systematic-debugging.
- If the plan states no row-count threshold, ask the user for one before the run, not after.

## Post-deploy watch

- For 30 minutes after full traffic or the production run, watch error rate, latency, freshness and row counts.
- Write `deploy.md` with:
  - what was deployed (digests, revision names, job execution ids);
  - timestamps;
  - the watch results;
  - the rollback command.

Take a reading at the start, the middle and the end of the window, and quote each from the tool output. A quiet window is a result: write it down. If a signal breaches during the watch, roll back with the command in deploy.md and then debug.

## deploy.md

Write it to `<artifacts_dir>/<YYYY-MM-DD>-<topic>/deploy.md`. Create the rollback section before the rollout starts and fill the rest as you go:

```markdown
# Deploy: <topic>

## Rollback
<exact command, with previous revision or digest>

## Deployed
- service revision / job image digest / execution id

## Timeline
- <timestamp> step and result

## Watch results
- error rate, latency, freshness, row counts, with readings

## Outcome
Deployed / Rolled back, and why
```

## Stop and ask

- Any precondition is missing.
- A breach or a row-count difference above the threshold.
- Anything not covered by the user's go, such as a Terraform apply when `deploy_method` is `terraform`: show the plan and wait.
