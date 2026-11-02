# dbt CI

CI builds into a CI dataset with its own target. It never uses
`<dbt_target_prod>`; production runs go through wraith:deploy.

## Steps

1. Check out the repository.
2. Authenticate with Workload Identity Federation. No service account key
   is stored.
3. Install dbt and run `dbt deps` (downloads packages; visible in the log).
4. If a production manifest artifact exists, run a slim build:
   `dbt build --target ci --select state:modified+ --defer --state <prod manifest dir>`
5. Otherwise run a full `dbt build --target ci` into the CI dataset.

Deferral is for this CI slim build only (rule 3 wins elsewhere).

## GitHub Actions sketch

```yaml
permissions:
  contents: read
  id-token: write
jobs:
  dbt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093 # v3.0.0
        with:
          workload_identity_provider: <workload_identity_provider>
          service_account: <ci_service_account>
      - run: dbt deps
        working-directory: <dbt_project_dir>
      - run: dbt build --target ci
        working-directory: <dbt_project_dir>
```

The `ci` target uses `method: oauth` and sets `maximum_bytes_billed`. The
service account can write only to the CI dataset.
