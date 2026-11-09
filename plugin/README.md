# wraith

Skills and agents for data and infrastructure engineering on GCP: dbt on
BigQuery, ODCS data contracts, ontologies, Cloud Run and Terraform. wraith
reviews data and infrastructure plans before anyone builds them, writes and
validates data contracts, keeps dbt models in step with them, and stops to ask
before destructive commands on production.

## Install

Claude Code:

```bash
claude plugin marketplace add wraith-proxy/wraith-skills
claude plugin install wraith@wraith-proxy
```

GitHub Copilot CLI:

```bash
copilot plugin marketplace add wraith-proxy/wraith-skills
copilot plugin install wraith@wraith-proxy
```

## What wraith runs, sends and stores

wraith runs nothing on its own. It has no hooks and no MCP servers; it is
skills and agents your agent reads when they apply. It stores nothing, sends
nothing, fetches nothing, collects no telemetry and checks for no updates.

Skills tell your agent to run commands that contact these services, with your
own credentials and under your permission prompts:

- Google Cloud (`gcloud`, `bq`, Cloud Run, BigQuery, IAM)
- dbt (`dbt` against your warehouse)
- Terraform providers and registries (`terraform init`, `plan`, `apply`)
- Package indexes (`uvx`, for example `uvx check-jsonschema`)
- GitHub (`gh`, read-only checks in security reviews)

wraith itself receives nothing from them.

Full documentation: https://github.com/wraith-proxy/wraith-skills. See
[PRIVACY.md](PRIVACY.md), [TERMS.md](TERMS.md), [SUPPORT.md](SUPPORT.md) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
