---
name: using-wraith
description: "Use when the user asks what wraith does or which wraith skill or agent fits a data or GCP task. Lists the wraith skills and agents and the rules they share."
license: MIT
metadata:
  source: GS@1bd2330:ETHOS.md
---

# Using wraith

wraith is a plugin of skills and agents for data and infrastructure work on GCP: dbt on BigQuery, ODCS data contracts, ontologies, Cloud Run and Terraform.

## Instruction priority

The user's direct requests first, then the project's AGENTS.md and CLAUDE.md, then wraith skills, then companion skills, then defaults.

## Shared rules

- Project specifics come from the `## wraith` block in the project's AGENTS.md. Never guess a command, project, region or target; if the block is missing, ask once and suggest wraith:setup.
- AI recommends, the user decides: production changes, pushes, deletes and spending need the user's explicit go-ahead in this conversation.
- A number without its mechanism is a rumour: say how every number was measured.
- Anything that touches state outside the process will one day run twice, so make it idempotent.
- Before destructive data and infra commands, follow wraith:careful.

## Skills

| Need | Skill |
|---|---|
| Review a plan that touches data | wraith:plan-data-review |
| Review a plan that touches GCP infrastructure | wraith:plan-infra-review |
| Write or change a data contract | wraith:odcs-contracts |
| Build or fix dbt models on BigQuery | wraith:dbt-bigquery |
| BigQuery cost, access or erasure | wraith:bigquery |
| Cloud Run services and jobs | wraith:cloud-run |
| Terraform on GCP | wraith:terraform-gcp |
| What business entities mean | wraith:ontology-modeling |
| Make the warehouse usable by AI agents | wraith:context-layer |
| IAM, secrets, ingress or personal data | wraith:security-audit |
| Prove a change against a dev target | wraith:qa |
| Production rollout | wraith:deploy |
| Destructive or production commands | wraith:careful |
| Configure wraith for a repository | wraith:setup |
| This list | wraith:using-wraith |

## Agents

| Agent | Dispatch when |
|---|---|
| wraith:data-engineer | dbt on BigQuery, ODCS contracts, pipelines, backfills and data quality. |
| wraith:platform-engineer | Terraform, Cloud Run, IAM, Workload Identity Federation and CI/CD. |
| wraith:sre | Observability, alerts, SLOs, incident triage and post-deploy watches. |
| wraith:security-engineer | Security and privacy review of GCP and data work. |
| wraith:ontologist | Ontology and context-layer work. |

## Companions

wraith names companion skills and never copies them. All are optional; every wraith skill works without them.

- Vendor mechanics: dbt Labs, Google and HashiCorp skills, listed in each wraith skill.
- General workflow (designs, plans, test-first work, debugging, code review, handoffs): obra/superpowers and mattpocock/skills.

Where a companion and a wraith skill disagree on data or GCP work, the wraith rule wins.

## Safety

wraith:careful is an instruction, not a security boundary. Keep the host's permission prompts on.
