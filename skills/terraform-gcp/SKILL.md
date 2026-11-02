---
name: terraform-gcp
description: "Use when writing, reviewing, planning or applying Terraform for GCP: state, providers, modules, IAM bindings, Workload Identity Federation for CI, BigQuery datasets, Cloud Run, and a safe plan and apply workflow."
license: MIT
metadata:
  source: new
---

# Terraform on GCP

## When to use

Writing, reviewing, planning or applying Terraform for GCP: state, providers, modules, IAM, CI auth, BigQuery datasets and Cloud Run.
Read the `## wraith` block of `AGENTS.md` first; if a key below is missing, ask once and suggest `wraith:setup`.

## Rules

1. State lives in a GCS bucket with object versioning and uniform bucket-level access, one state per environment. Never local state for shared infrastructure.
2. Pin `required_version` and providers (`~>` on the minor of the current major, per ADR 0001 C9b), and commit `.terraform.lock.hcl`.
3. Terraform owns datasets, never tables. Datasets, buckets holding data and KMS keys set `lifecycle { prevent_destroy = true }`; datasets also set `delete_contents_on_destroy = false`.
4. IAM uses additive `google_*_iam_member` by default. Authoritative `_iam_binding` or `_iam_policy` only when the module owns the whole role on that resource, and never both for the same role and resource.
5. CI authenticates with Workload Identity Federation (GitHub OIDC to service account impersonation). No service account keys exist anywhere.
6. Workflow:
   - `terraform fmt -check`, then `terraform validate`, then `terraform plan -out=tfplan`.
   - Review the plan. Any destroy or replace of a stateful resource stops the work and asks the user.
   - Then `terraform apply tfplan`. Never `apply -auto-approve` outside CI applying an approved plan.
7. Modules are small, versioned by git tag (never `ref=main`), with typed inputs and validation blocks.
8. No hardcoded project ids or regions: use variables plus one tfvars file per environment.
9. Every resource that supports labels carries `env`, `owner` and `system`.
10. Bring existing resources in with `import` blocks. `terraform state rm` or `mv` only with the user's go-ahead.
11. Detect drift with a scheduled `terraform plan -detailed-exitcode`. Exit code 2 means drift and opens an issue.

## Workflow

1. Read the wraith block: `<terraform_dir>`, `<gcp_project_dev>`, `<gcp_project_prod>`, `<region>`, `<bigquery_location>`. Ask once for any that is missing and suggest `wraith:setup`.
2. Work in `<terraform_dir>/envs/<env>/`, starting with dev. Layout and backend: `references/layout.md`.
3. Pin versions: `required_version = "~> 1.17"` and provider `hashicorp/google` with `version = "~> 8.9"`.
4. Run fmt, validate and plan as in rule 6, then read the plan.
5. For production changes or any stateful destroy or replace, stop and get the user's explicit go-ahead; hand the plan to `wraith:plan-infra-review`.
6. Apply the saved plan with `terraform apply tfplan`.
7. For CI, set up Workload Identity Federation: `references/wif-github.md`.
8. Dataset and table work: `wraith:bigquery`. Service work: `wraith:cloud-run`. Release: `wraith:deploy`.

## Commands

`terraform init` downloads providers and modules (network call); run it visibly.

- `terraform -chdir=<terraform_dir>/envs/<env> init`
- `terraform -chdir=<terraform_dir>/envs/<env> fmt -check`
- `terraform -chdir=<terraform_dir>/envs/<env> validate`
- `terraform -chdir=<terraform_dir>/envs/<env> plan -var-file=terraform.tfvars -out=tfplan`
- `terraform -chdir=<terraform_dir>/envs/<env> apply tfplan`
- `terraform -chdir=<terraform_dir>/envs/<env> plan -detailed-exitcode`

## Vendor skills

HashiCorp skills from `hashicorp/agent-skills` (plugin `terraform`), vetted in ADR 0004. Referenced by name, never copied.

- `terraform-style-guide`: Formatting, naming and file layout in any Terraform change.
- `terraform-test`: Plan-mode and mock tests for a module, beside `wraith:tdd`.
- `refactor-module`: Extracting a module and moving state with `moved` blocks.
- `terraform-search-import`: Bringing existing cloud resources under Terraform, on Terraform 1.14+.

Google skills, vetted in ADR 0003. Terraform output only; this skill runs the plan and apply:

- `cloud-run-alert-configuration`: PromQL alert policies for Cloud Run, with `wraith:cloud-run`.
- `google-cloud-slo-alert-configuration`: PromQL SLO alert policies.

They ask the agent to set an attribution tag that reports usage to Google; tell the user and let them choose.

Where a companion step disagrees with this skill:

- `refactor-module` runs `terraform state mv` as a plain step. Here it runs only after the user's go-ahead, and `moved` blocks are preferred because they show in the plan.
- `terraform-test` apply-mode creates real resources. Here apply-mode tests run only in a dev project, with the user's go-ahead.
- `terraform-search-import` ends with a bare `terraform apply`. Here the plan is read first and the apply takes the saved plan.

Where they and this skill disagree, this skill wins for dataset ownership and `prevent_destroy`, additive IAM, Workload Identity Federation, and plan review before apply (rules 3, 4, 5 and 6).

## References

- `references/layout.md`: directory layout, GCS backend, labels locals.
- `references/wif-github.md`: Workload Identity Federation for GitHub Actions.
