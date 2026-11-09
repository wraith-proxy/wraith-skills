# Service rollout

Placeholders: `<project>` is `<gcp_project_dev>` or `<gcp_project_prod>`; `<region>` is `region`. Production steps need the user's go-ahead.

## 1. Write the rollback first

```bash
gcloud run services update-traffic <service> --to-revisions <previous>=100 \
  --project <project> --region <region>
```

## 2. Build and push

```bash
gcloud builds submit --tag <region>-docker.pkg.dev/<project>/<repo>/<image>:<git-sha> \
  --project <project> --region <region>
```

Resolve the digest and deploy by it, not by tag.

## 3. Deploy with no traffic and a tag

```bash
gcloud run deploy <service> --image <region>-docker.pkg.dev/<project>/<repo>/<image>@sha256:<digest> \
  --no-traffic --tag candidate --no-allow-unauthenticated \
  --project <project> --region <region>
```

## 4. Smoke test the tag

The gcloud proxy handles authentication, so no token passes through the command line.

```bash
gcloud run services proxy <service> --tag <tag> \
  --project <project> --region <region> --port 8080 &
curl -fsS http://localhost:8080/healthz
kill %1
```

## 5. Move traffic

```bash
gcloud run services update-traffic <service> --to-tags candidate=10 --project <project> --region <region>
gcloud run services update-traffic <service> --to-tags candidate=50 --project <project> --region <region>
gcloud run services update-traffic <service> --to-latest --project <project> --region <region>
```

Check errors and latency between each step before the next.

## 6. Rollback

Run the command from step 1.

## 7. Error-log query

```bash
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="<service>" AND severity>=ERROR' \
  --freshness 30m --limit 50 --project <project>
```
