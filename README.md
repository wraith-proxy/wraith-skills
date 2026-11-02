# wraith

wraith is a plugin of skills and agents for data and infrastructure
engineering on GCP: dbt, BigQuery, Cloud Run, Terraform, ODCS data contracts
and ontologies. It runs the work as a plan, build, review, ship sprint, and it
works in both Claude Code and GitHub Copilot from one repository.

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

wraith runs two local Python hooks and sends nothing anywhere.
