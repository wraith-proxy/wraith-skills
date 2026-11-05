# ADR 0004: HashiCorp companion

Status: proposed (Gate 3). Date: 2026-11-02. Ticket: WSK-00004.

## Context

wraith points to the HashiCorp agent skills as a companion and never copies
them (G21). This ADR vets that companion before any wraith skill names it.

- Repository: https://github.com/hashicorp/agent-skills
- Ref reviewed: `main`, SHA `bc6b14b77481c3cbfbb06a0166be7245ed45798c`
- License: MPL-2.0
- Reviewed: 2026-11-02
- Scope: six `SKILL.md` files read in full under
  `plugins/terraform/skills/`. The other ten Terraform skills and the four
  Packer skills are listed as out of scope and were not read.

MPL-2.0 is file-level copyleft; wraith never copies these files.

Quotes below are single sentences or single commands, kept short to show a
risk or a conflict. Em dashes in quoted text are replaced per G8.

## Review

Section 2.6 stances are cited by their first words. "Commands" lists the
commands the body tells the agent to run. None of the six sets
`allowed-tools`. The examples in all six use AWS resources, not GCP.

| Skill | Purpose | Use for | Commands it may run | Risky instructions (quoted) | Conflicts with 2.6 (quoted) | Verdict |
|---|---|---|---|---|---|---|
| `plugins/terraform/skills/terraform-style-guide/SKILL.md` | Style conventions for writing and reviewing Terraform HCL. | Formatting, naming and file layout in any Terraform change. | `terraform fmt -recursive`, `terraform validate`, `tflint`, `checkov`, `tfsec` | none | none | recommend |
| `plugins/terraform/skills/terraform-test/SKILL.md` | Write and run `.tftest.hcl` tests with run blocks and mocks. | Plan-mode and mock tests for a module, beside `wraith:tdd`. | `terraform test`, `terraform test -verbose`, `terraform test -no-cleanup` | "`apply` (default, creates real resources) or `plan` (validates logic only)"; "Tests run against temporary resources" | "Automate the guardrails, not the work": an apply-mode run creates and destroys real resources with no plan review. | recommend with caveat |
| `plugins/terraform/skills/refactor-module/SKILL.md` | Split a monolithic Terraform configuration into modules. | Extracting a module and moving state with `moved` blocks. | `terraform state list`, `terraform show -json`, `terraform state mv`, `terraform plan -out=migration.tfplan`, `terraform apply migration.tfplan` | "terraform state mv aws_vpc.main module.vpc.aws_vpc.main"; "terraform apply migration.tfplan" | "Fail loud, not silent": its success criterion is "No plan differences after refactoring", which holds only if the plan is read, not assumed. | recommend with caveat |
| `plugins/terraform/skills/terraform-search-import/SKILL.md` | Discover unmanaged resources with `terraform query` and import them. | Bringing existing cloud resources under Terraform, on Terraform 1.14+. | `terraform init`, `terraform query`, `terraform query -generate-config-out=imported.tf`, `terraform plan`, `terraform apply`, `./scripts/list_resources.sh` | "terraform apply" (final step of the import workflow); `terraform init` downloads providers (network call) | "Terraform owns datasets, not tables": generated config lists every attribute, so a dataset's immutable location is copied in unchecked. | recommend with caveat |
| `plugins/terraform/skills/terraform-stacks/SKILL.md` | Write Terraform Stacks configs for HCP Terraform deployments. | Nothing: needs HCP Terraform and a Stacks-capable plan. | `terraform stacks init`, `terraform stacks configuration upload`, `terraform stacks deployment-run approve-all-plans` | "Upload configuration triggers deployment runs automatically."; "terraform stacks deployment-run approve-all-plans -deployment-run-id=..." | "Rigor is proportional to consequence and reuse": it offers `deployment_auto_approve` rules that approve plans with no human review. | do not recommend |
| `plugins/terraform/skills/terraform-policy/SKILL.md` | Write and test Terraform Policy files, convert Sentinel. | Nothing: needs the `tfpolicy` CLI and HCP Terraform. | `tfpolicy validate`, `tfpolicy test`, `npx skills add` | "npx skills add hashicorp/agent-skills/terraform/terraform-policy/skills/tfpolicy-author" (network call, installs a skill) | none | do not recommend |
| `plugins/terraform/skills/azure-verified-modules/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/terraform/skills/new-terraform-provider/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/terraform/skills/provider-actions/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/terraform/skills/provider-configuration/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/terraform/skills/provider-docs/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/terraform/skills/provider-ephemeral-resources/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/terraform/skills/provider-framework-migration/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/terraform/skills/provider-resources/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/terraform/skills/provider-test-patterns/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/terraform/skills/run-acceptance-tests/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/packer/skills/aws-ami-builder/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/packer/skills/azure-image-builder/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/packer/skills/push-to-registry/` | not read | none | none | none | none | out of scope (not read) |
| `plugins/packer/skills/windows-builder/` | not read | none | none | none | none | out of scope (not read) |

## Decision

- `wraith:terraform-gcp` may point to `terraform-style-guide`,
  `terraform-test`, `refactor-module` and `terraform-search-import`.
- `wraith:review` may point to `terraform-style-guide` for its checklist.
- `wraith:plan-infra-review` may point to `terraform-style-guide` and
  `refactor-module` (the plan must show no unintended changes).
- `wraith:security-audit` points to no companion skill. The style guide's
  security note defers to a `SECURITY.md` that is not in the skill.
- No wraith skill points to a "do not recommend" skill. Stacks and Policy
  need HCP Terraform and are outside the GCP sprint.

Where a companion instruction disagrees with a wraith rule, the wraith rule
wins, citing section 2.6 and the `wraith:terraform-gcp` rules: plan reviewed
before apply; no `apply -auto-approve` outside CI applying an approved plan;
`prevent_destroy` on datasets, buckets and KMS keys; additive `_iam_member`;
Workload Identity Federation (no keys); `state rm` and `state mv` only with
the user's go-ahead (G17).

- Contradiction: `refactor-module` runs `terraform state mv` as a plain
  step. In wraith it runs only after the user says go, and `moved` blocks
  are preferred because they show in the plan.
- Contradiction: `terraform-test` apply-mode runs create and destroy real
  resources with no reviewed plan. In wraith, dev uses `command = plan` and
  mocks; apply-mode tests run only in a dev project under the dev cost cap
  and with the user's go-ahead (G17).
- Gap: `terraform-search-import` ends with a bare `terraform apply`. In
  wraith the plan is read first, and the apply takes the saved plan.
- Gap: the companions' resources carry no `prevent_destroy`. Imported or
  extracted datasets, buckets and KMS keys get it, per "Terraform owns
  datasets, not tables. dbt owns tables. Dataset location is immutable."
- The style guide's example `provider` blocks use static regions and
  `aws` credentials. Credentials follow Workload Identity Federation, never
  keys.
- Any command that downloads (`terraform init`, `npx`) or calls the network
  is named in the wraith skill and runs visibly (G11).

## Install

Copied from the ADR 0001 C10 table.

| Host | Command that worked | Lands in |
|---|---|---|
| Claude Code | `claude plugin marketplace add hashicorp/agent-skills`, `claude plugin install terraform@hashicorp` | plugin cache, `terraform` 1.0.0, 16 skills |
| Copilot | `copilot plugin marketplace add hashicorp/agent-skills`, `copilot plugin install terraform@hashicorp` | `~/.copilot/installed-plugins/hashicorp/`, 16 skills |

The `terraform` plugin carries all 16 Terraform skills, including the ten
that are out of scope here. The Packer skills belong to a separate plugin
and are not installed by these commands.

## Consequences

- Six skills are vetted: one is recommended, three are recommended with a
  caveat and two are not recommended. Fourteen more are out of scope.
- Wraith skills name only the companion skills listed under Decision (G21).
- The examples are AWS-based, so a wraith skill uses them for structure and
  never for resource arguments.
- The MPL-2.0 license is file-level copyleft, so nothing is vendored. Only
  names are referenced.
- The companion is optional. Every wraith skill works with it absent and
  says so.
- If the pinned ref moves, this ADR is re-run before the pointers change.

## Addendum 2026-11-05: pin bumped to 5e30fa5

Ticket: WSK-00081. The TF pin moved from bc6b14b to
5e30fa5c867ba6777c37e4206babfd08049c396f, one upstream commit ("add Agent
Plugins root manifests"). No `SKILL.md` and no file in a skill folder
changed. The commit adds a root `plugin.json` for the terraform and packer
plugins and edits README, AGENTS.md and CHANGELOG text. The terraform
manifest holds metadata only (name, version, author, links, license,
keywords). The packer manifest adds display text for another host. Neither
declares hooks, MCP servers or commands, and the install commands above do
not install packer. Verdicts unchanged. The owner accepts the bump by
merging it.
