# dbt as a Cloud Run Job

Values in angle brackets come from the wraith block. See wraith:dbt-bigquery for the project itself.

## Dockerfile

Resolve digests with `docker buildx imagetools inspect python:3.12-slim` (and the same for the uv image). Never guess a digest.

```dockerfile
FROM ghcr.io/astral-sh/uv:<version>@sha256:<digest> AS uv
FROM python:3.12-slim@sha256:<digest>
COPY --from=uv /uv /usr/local/bin/uv
RUN useradd --create-home runner
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY <dbt_project_dir> ./dbt
ENV PATH="/app/.venv/bin:$PATH" DBT_PROFILES_DIR=/app/dbt
USER runner
WORKDIR /app/dbt
# ds defaults to yesterday (UTC); set DS to rerun one day.
ENTRYPOINT ["sh", "-c", "exec dbt build --target \"$DBT_TARGET\" --vars \"{ds: ${DS:-$(date -u -d yesterday +%F)}}\""]
```

## profiles.yml

```yaml
<profile_name>:
  target: <dbt_target_prod>
  outputs:
    <dbt_target_prod>:
      type: bigquery
      method: oauth
      project: <gcp_project_prod>
      dataset: <dataset>
      location: <bigquery_location>
      maximum_bytes_billed: <max_bytes_billed>
      threads: 4
```

No keyfile. The attached service account supplies credentials.

## Create and update the job

`ds` is passed as a dbt var, so rerunning one ds gives the same result. The entrypoint defaults it to yesterday (UTC); `DS` overrides it.

```bash
gcloud run jobs create <job> \
  --image <region>-docker.pkg.dev/<project>/<repo>/<image>@sha256:<digest> \
  --set-env-vars DBT_TARGET=<dbt_target_prod> \
  --service-account <sa>@<project>.iam.gserviceaccount.com \
  --task-timeout 1800s --max-retries 1 --tasks 1 --parallelism 1 \
  --project <project> --region <region>

gcloud run jobs update <job> \
  --image <region>-docker.pkg.dev/<project>/<repo>/<image>@sha256:<digest> \
  --service-account <sa>@<project>.iam.gserviceaccount.com \
  --task-timeout 1800s --max-retries 1 --tasks 1 --parallelism 1 \
  --project <project> --region <region>
```

Rerun one ds by hand:

```bash
gcloud run jobs execute <job> --project <project> --region <region> \
  --update-env-vars DS=<YYYY-MM-DD>
```

## Cloud Scheduler trigger

The scheduler service account needs `roles/run.invoker` on the job. The body is empty, so each run builds yesterday.

```bash
gcloud scheduler jobs create http <job>-daily \
  --schedule "0 6 * * *" --time-zone "Etc/UTC" \
  --uri "https://run.googleapis.com/v2/projects/<project>/locations/<region>/jobs/<job>:run" \
  --http-method POST \
  --oauth-service-account-email <scheduler-sa>@<project>.iam.gserviceaccount.com \
  --message-body '{}' \
  --project <project> --location <region>
```
