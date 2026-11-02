# Review checklists

## dbt and SQL

- grain stated in the model description
- no `SELECT *` in models
- partition filter on large sources
- `SAFE_DIVIDE` for ratios
- optional relations use LEFT JOIN, so orphans surface as NULL
- incremental models set `on_schema_change: fail`
- no hardcoded date literals (use vars or `ds`)
- a test for every contract quality rule
- marts have the contract enforced

## BigQuery

- dry-run bytes stated for new heavy queries
- `require_partition_filter` on large partitioned tables
- no project-level admin grants
- classified columns protected by policy tag or encryption

## Terraform

- `prevent_destroy` on datasets, buckets with data, and KMS keys
- additive `iam_member` unless the module owns the role
- no service account keys
- pinned provider and module versions
- labels present
- no hardcoded project ids

## Cloud Run

- a dedicated service account
- no `allUsers` invoker unless the plan says public
- secrets from Secret Manager
- max instances set
- image deployed by digest
- health endpoint does not touch dependencies

## Python

- ruff clean at line length 79
- behaviour-level tests
- mocks only at boundaries
- no `print` in library code

## CI

- actions pinned by full SHA
- Workload Identity Federation, no keys
- least-privilege `permissions` blocks

## Contracts and ontology

- each contract change classified as additive or breaking
- a breaking change has a version bump and consumer notice
- new fields mapped to ontology terms or flagged
