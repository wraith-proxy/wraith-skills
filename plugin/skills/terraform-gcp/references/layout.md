# Layout

`<terraform_dir>` comes from the wraith block (default value `infra`).

```text
<terraform_dir>/modules/<name>/
<terraform_dir>/envs/<env>/
  main.tf
  backend.tf
  terraform.tfvars
```

One state per environment: the prefix differs, the bucket has object
versioning and uniform bucket-level access.

```hcl
# backend.tf
terraform {
  required_version = "~> 1.17"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 8.9"
    }
  }

  backend "gcs" {
    bucket = "<state-bucket>"
    prefix = "<env>"
  }
}
```

Project and region come from variables set in `terraform.tfvars`
(`<gcp_project_dev>` or `<gcp_project_prod>`, `<region>`), never literals.

```hcl
# main.tf
locals {
  labels = {
    env    = var.env
    owner  = var.owner
    system = var.system
  }
}
```

Pass `local.labels` to every resource that supports labels.
