# pairs.yaml

Each domain keeps its vetted question-to-SQL examples in
`<context_dir>/<domain>/pairs.yaml`, a list of entries. See
[example-pairs.yaml](example-pairs.yaml).

## Fields

| Field | Meaning |
|---|---|
| `id` | Stable identifier, `<domain>-NNN` |
| `question` | The question as a user would ask it |
| `sql` | BigQuery Standard SQL that answers it, with fully qualified table names and a `ds` filter |
| `owner` | The expert who accepted or retired it |
| `status` | `proposed`, `accepted` or `retired` |
| `last_verified` | Date (`YYYY-MM-DD`) of the last passing dry run and expert check |
| `notes` | Grain, metric definition used, caveats |

Only `accepted` pairs are served to agents. A `retired` pair stays in the
file so a returning candidate is recognised and rejected again.

## CI check

Dry-run each accepted pair so a schema change that breaks it fails the build:

```bash
yq -r '.[] | select(.status == "accepted") | .sql' <context_dir>/<domain>/pairs.yaml |
  while IFS= read -r sql; do
    bq query --dry_run --project_id=<gcp_project_dev> \
      --location=<bigquery_location> --use_legacy_sql=false "$sql" || exit 1
  done
```

Write each `sql` on one line, or switch the loop to read NUL-separated output.
A failing pair goes back to `proposed` until the owner fixes and re-accepts it.

## Health score

Per domain:

- pairs: accepted pairs passing the dry run divided by accepted pairs;
- freshness: tables in `datasets.md` within their freshness SLA divided by tables listed.

Report both as percentages in `<context_dir>/README.md` next to the domain.
Below 100 percent on either is a finding for the cluster owner.
