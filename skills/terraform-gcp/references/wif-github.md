# Workload Identity Federation for GitHub Actions

No service account keys. GitHub OIDC tokens are exchanged for short-lived
impersonation of the deploy service account.

```hcl
resource "google_iam_workload_identity_pool" "github" {
  project                   = var.project_id
  workload_identity_pool_id = "github"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
  }

  attribute_condition = "assertion.repository == \"<owner>/<repo>\""

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account" "deploy" {
  project      = var.project_id
  account_id   = "deploy"
  display_name = "CI deploy"
}

resource "google_service_account_iam_member" "wif_deploy" {
  service_account_id = google_service_account.deploy.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/<owner>/<repo>"
}
```

Grant the deploy service account its project roles with additive
`google_project_iam_member` resources, never `_iam_binding`.

The pool provider resource name feeds the workflow below as
`workload_identity_provider`
(`projects/<number>/locations/global/workloadIdentityPools/github/providers/github`).

```yaml
permissions:
  contents: read
  id-token: write

steps:
  - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
  - uses: google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093 # v3.0.0
    with:
      workload_identity_provider: <provider resource name>
      service_account: deploy@<project_id>.iam.gserviceaccount.com
```
