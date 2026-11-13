---
name: security-audit
description: "Use before shipping changes to IAM, secrets, networking, containers, CI or anything handling personal data, or when asked for a security review. Audits least privilege, credentials, ingress, supply chain and personal-data handling on GCP and writes findings with severity and evidence."
license: MIT
metadata:
  source: "GS@1bd2330:cso/SKILL.md.tmpl, AA@8ae6164:security/security-cloud-security-architect.md"
---

# Security audit

Read-only. Look, run read-only commands, and write the report. Change nothing.
For a large repository, dispatch `wraith:security-engineer` to take one
checklist area each and fold the results into one table.

## Settings

Read the `## wraith` block of the project's AGENTS.md. You need
`artifacts_dir` (default `docs/wraith`) and `gcp_project_dev` and
`gcp_project_prod` for the cloud checks. If a key is missing, ask once and
suggest `wraith:setup`.

## Checklist

Work through every item. For each, state how you checked it and what you found.

1. IAM:
   - primitive roles (owner or editor) on workloads;
   - user-managed service account keys (`gcloud iam service-accounts keys list --iam-account <sa> --managed-by=user` must be empty);
   - impersonation chains;
   - project-level BigQuery admin.

   How to check: `gcloud projects get-iam-policy <project>` and look for
   `roles/owner` and `roles/editor` on service accounts, `roles/bigquery.admin`
   at project level, and `roles/iam.serviceAccountTokenCreator` grants. Run the
   key listing for each workload service account.
2. Secrets: in the repository or its history (run detect-secrets or gitleaks if installed, and say which ran); Secret Manager usage; secrets in Terraform state or variables.

   How to check: run whichever scanner is installed over the tree and history.
   Grep Terraform for `secret`, `password` and `key` in variables and outputs,
   and check that runtime secrets come from Secret Manager references.
3. Network: `allUsers` or `allAuthenticatedUsers` bindings, public buckets, ingress settings.

   How to check: grep the IAM policies and Terraform for both principals,
   run `gcloud storage buckets list` and inspect bucket policies, and read
   Cloud Run `ingress` and unauthenticated-invoker settings.
4. Supply chain: dependencies pinned and locked; images by digest; GitHub Actions pinned by SHA; no unpinned launchers.

   How to check: look for lock files, `FROM image@sha256:` in Dockerfiles,
   `uses: owner/repo@<40-char sha>` in workflows, and bare `uvx`, `npx` or
   `latest` launchers.
5. Data:
   - every personal-data column classified in its contract;
   - an encryption or crypto-shred path;
   - retention for raw plaintext;
   - Data Access audit logs enabled for datasets holding personal data.

   How to check: read the ODCS contracts for classification, find the key or
   shred mechanism, find the retention setting on raw tables, and read the
   project audit config for BigQuery data access logs.
6. CI/CD: Workload Identity Federation, a least-privilege deploy service account, `permissions:` blocks, branch protection on main, and every third-party action pinned by full SHA.

   How to check: read the workflows for credential JSON secrets versus
   WIF, a top-level `permissions:` block per workflow, the deploy account's
   roles, and `gh api repos/<owner>/<repo>/branches/main/protection`.
7. Containers: non-root, a minimal base, no secrets in layers.

   How to check: read each Dockerfile for `USER`, the base image, and
   `COPY` or `ARG` lines that carry credentials or `.env` files.

## Second pass

When the companions are installed, also run Google's
`google-cloud-waf-security`, `iam-helper-for-troubleshooting`,
`iam-helper-for-policy-simulator`, `iam-helper-for-policy-management`,
`iam-helper-for-privileged-access-management` and `google-cloud-recipe-auth`,
and fold their findings into the table. Name them only; do not copy their
text. If one is not installed, list it under checks that could not run.

## Output

Write `<artifacts_dir>/<date>-<topic>/security.md` with:

- a table with columns severity (critical, high, medium or low), area,
  evidence (file:line or quoted command output) and fix;
- then the checks that could not run, and why;
- the closing line: "Best-effort review, not a penetration test."
