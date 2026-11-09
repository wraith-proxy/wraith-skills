---
name: plan-infra-review
description: "Use after a plan touches GCP infrastructure: Cloud Run services or jobs, Terraform, IAM, networking, secrets, schedulers or CI deploys. Reviews identity, ingress, secrets, state ownership, rollout and rollback, limits, observability, cost and blast radius, then records findings and a verdict in the plan."
license: MIT
metadata:
  source: GS@1bd2330:plan-eng-review/SKILL.md.tmpl
---

# Plan Infra Review

## When to use

When a written plan, by any author, touches Cloud Run, Terraform, IAM, networking, secrets, schedulers or CI deploys.
Runs before anyone builds the plan.

## Step 0: attack the premise

Before the checklist, ask: does this need to exist, and what already answers it? Look for a managed service, an existing service or job, or an existing Terraform module that covers it. If one does, the finding is a blocker that names it, and the review stops there until the user decides.

## Checklist

1. Could a managed service or an existing component do this?
2. Identity: one service account per workload, least-privilege roles listed, no keys, Workload Identity Federation for CI.
3. Ingress and network: public or private, authentication, egress needs.
4. Secrets: in Secret Manager, a rotation owner, nothing in Terraform state in plain text.
5. Ownership: Terraform owns it; the state location; who applies it and from where.
6. Rollout and rollback: a no-traffic revision, a smoke test and traffic steps; the rollback command is in the plan.
7. Limits: concurrency, max instances, timeouts and retries; jobs are idempotent under retry.
8. Observability: logs with severity, alerts on error rate, an SLO when users depend on it.
9. Cost: a monthly estimate, max instances and a budget alert.
10. Blast radius: what fails if this fails; dependencies listed.
11. Region and residency match the BigQuery dataset location.

## Output

Append `## Infra review (<YYYY-MM-DD>)` to the plan, containing:

| Severity | Item | Finding | Required change |
|---|---|---|---|
| blocker, should or nit | checklist number | what the plan says or omits | the edit to the plan |

Then one verdict line: `Verdict: READY`, `Verdict: READY WITH CHANGES` or `Verdict: NOT READY`.

Blockers are resolved in the plan before anyone builds it.

## Workflow

1. Read the `## wraith` block of AGENTS.md: `artifacts_dir`, `gcp_project_dev`, `gcp_project_prod`, `region`, `bigquery_location`, `deploy_method`, `terraform_dir`. If a key is missing, ask once and suggest wraith:setup.
2. Read the plan the user names; otherwise the newest `plan.md` under `<artifacts_dir>`; otherwise ask for the path. Read the Terraform or service definitions it names.
3. Run Step 0.
4. Walk the checklist in order. An item the plan does not address is a finding, never a pass. Use wraith:cloud-run for items 2, 3, 6 and 7, and wraith:terraform-gcp for items 4 and 5.
5. For items 2 to 4, when the plan adds or widens IAM, ingress or secrets, add a should finding to run wraith:security-audit on the change.
6. For item 11, compare `region` with `bigquery_location`; a mismatch for a data workload is a blocker.
7. Run the vendor second pass if installed, and fold its findings into the same table.
8. Append the output section to the plan. Do not edit the rest of the plan, and never apply anything; the author resolves the findings.

## Commands

Every value is a wraith block key. Replace `<project>` with `<gcp_project_dev>` or `<gcp_project_prod>`, and `<env>` with the environment directory used by wraith:terraform-gcp. None of them changes infrastructure.

```bash
terraform -chdir=<terraform_dir>/envs/<env> plan -var-file=terraform.tfvars -lock=false -out=review.tfplan
terraform -chdir=<terraform_dir>/envs/<env> show -json review.tfplan
gcloud run services describe <service> --project <project> --region <region>
gcloud projects get-iam-policy <project> --flatten="bindings[].members" --filter="bindings.members:<service-account>"
```

## Vendor skills

Second pass, only when installed. Companion Google skills, recommended with caveat in ADR 0003 and never copied here:

- `google-cloud-waf-reliability`: use for items 6, 7 and 10, reliability, disaster recovery and RTO and RPO.
- `google-cloud-waf-cost-optimization`: use for item 9, FinOps and rightsizing.
- `google-cloud-waf-operational-excellence`: use for items 6 and 8, CI/CD, monitoring and incidents.

Security pillar guidance (`google-cloud-waf-security`) belongs to wraith:security-audit, not this review.

They ask the agent to set an attribution tag that reports usage to Google; tell the user and let them choose. Their output is advice and never replaces wraith:cloud-run or wraith:terraform-gcp rules.

## References

- wraith:cloud-run and wraith:terraform-gcp for the rules each item checks against.
- wraith:security-audit for identity, ingress and secrets in depth.
- wraith:plan-data-review when the plan also changes data.
