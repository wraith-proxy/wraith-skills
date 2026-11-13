# ADR 0003: Google companion

Status: proposed (Gate 3). Date: 2026-11-02. Ticket: WSK-00004.

## Context

wraith points to Google's agent skills for BigQuery, Cloud Run and IAM work
but never copies them (G21). This ADR vets the skills wraith may name.

- Companion: Google agent skills, https://github.com/google/skills, ref
  `main`, SHA 92776fbf3875a5ee7424124e398956a998483056, license Apache-2.0,
  reviewed 2026-11-02.
- Marketplace: `.claude-plugin/marketplace.json` (name `google-plugins`)
  lists plugins that live in other repositories. Three matter to wraith, each
  read read-only at the marketplace ref:
  - `bigquery`: GoogleCloudPlatform/bigquery-data-analytics-plugin, tag
    0.2.5, SHA 8e891942ffda7bc6e17e3782ffdcf217cd99b6ff. One skill plus an
    MCP server.
  - `db-context-engineering`: GoogleCloudPlatform/db-context-enrichment, tag
    v0.7.2 (subdirectory `plugin/`), SHA
    64cf72c924c4737435c331c83868fa589f8d12ac. Seven skills.
  - `knowledge-catalog`: GoogleCloudPlatform/knowledge-catalog-plugin, tag
    0.5.4, SHA fdc3b206d59d390269de608a3bcf475d2c8829c0. No SKILL.md: an MCP
    server plus a `KNOWLEDGE_CATALOG.md` context file.
- `README.md` at 92776fb carries no "under active development" note
  (`grep -n -i "active development" README.md` printed nothing, exit 1). The
  `bigquery` and `knowledge-catalog` plugin READMEs say "Currently in beta
  (pre-v1.0), and may see breaking changes". Whatever the note, every Google
  verdict below is capped at "recommend with caveat".
- Scope: 25 named skills under `skills/cloud/`, the `bigquery` plugin skill,
  the 7 `db-context-engineering` skills and the `knowledge-catalog` plugin
  are vetted. Every other folder is one out-of-scope row (not read).

## Review

Notes that apply to every row:

- **Attribution tag.** All 25 `skills/cloud/` skills (and their
  `references/attribution.md`) tell the agent to prefix each `gcloud` call with
  `CLOUDSDK_METRICS_REQUEST_ATTRIBUTION="agent-skills/1.0 (skill:<name>)"` and
  to append the same token to `User-Agent` on direct HTTP and MCP calls. The
  file says the tag "carries no user data". It is usage telemetry sent to
  Google by the companion, not by wraith (G11 covers wraith files only).
  Rows below say "attribution tag" and do not repeat the quote.
- **`--quiet`.** Several skills add `--quiet` to `gcloud`, which suppresses
  confirmation prompts.
- Commands listed are those the skill text tells the agent to run.

| Skill | Purpose | Use for | Commands | Risky instructions (quoted) | Conflicts with 2.6 (quoted) | Verdict |
|---|---|---|---|---|---|---|
| bigquery-basics | Manage BigQuery datasets, tables, jobs, and run SQL | wraith:bigquery needs a basic CLI recipe | `bq mk`, `bq query`, `gcloud services enable` | `bq mk --dataset --location=US my_dataset`; `--quiet`; attribution tag | "Terraform owns datasets, not tables": it creates datasets by CLI | recommend with caveat |
| bigquery-optimization | Cost, partitioning, clustering, editions and query tuning guidance | wraith:bigquery cost and layout review | `bq show`, `bq query`, `gcloud auth login`, `npx skills add` | "CTAS migrations for unpartitioned tables"; partition and dataset expirations; attribution tag | "Storage is cheap and engineering time is not": pushes expiry and TTL; "Terraform owns datasets" for dataset expirations | recommend with caveat |
| bigquery-troubleshooting | Root-cause workflow for failing, slow or costly BigQuery jobs | wraith:bigquery incident and cost-spike diagnosis | `bq show -j`, `bq show`, `gcloud config set project` | `npx skills add google/skills --skill ...`; attribution tag | none | recommend with caveat |
| bigquery-observability | INFORMATION_SCHEMA and monitoring query patterns for telemetry | wraith:bigquery slot, queue and reservation checks | `bq show`, `bq query`, `gcloud services enable` | `npx skills add google/skills --skill ...`; attribution tag | none | recommend with caveat |
| bigquery-ai-ml | SQL for AI.* functions, forecasting, anomalies, vector search | wraith:bigquery when the task is BigQuery ML or GenAI SQL | none (SQL only) | model calls bill per use; attribution tag | none | recommend with caveat |
| bigquery-udfs | Create and deploy BigQuery UDFs and remote functions | wraith:bigquery when a custom function is asked for | `bq query`, `gcloud run`, `gcloud storage rm` | `gcloud run services delete`; `DROP FUNCTION IF EXISTS`; `CREATE OR REPLACE FUNCTION`; `--quiet` | none | recommend with caveat |
| bigquery-migration-sql-translator | Translate legacy SQL dialects to GoogleSQL via BQMS MCP | wraith:dbt-bigquery for non-dbt SQL migration | `gcloud storage cp`, `gcloud storage rm -r` | `gcloud storage rm -r gs://{bucket}/{folder}`; remote MCP server call; attribution tag | none | recommend with caveat |
| dbt-sf-to-bq-translator | Translate Snowflake dbt models to BigQuery SQL | wraith:dbt-bigquery for a Snowflake to BigQuery move | `gcloud storage cp`, `gcloud bq migration-workflows create`, bundled `scripts/dbt_translator.py` | creates a cloud migration workflow (network, spend); bundled script run locally | none | recommend with caveat |
| cloud-run-basics | Deploy and run Cloud Run services, jobs, worker pools | wraith:cloud-run deploy recipes | `gcloud run deploy`, `gcloud run jobs create`, `gcloud run jobs execute` | `--allow-unauthenticated`; `gcloud run deploy SERVICE_NAME --source . --quiet`; attribution tag | none | recommend with caveat |
| cloud-run-alert-configuration | Terraform PromQL alert policies for Cloud Run | wraith:cloud-run with wraith:terraform-gcp | `gcloud run services list`, `gcloud config get-value project` | generates Terraform; no apply step in the skill | none | recommend with caveat |
| cloud-build-basics | Cloud Build concepts, triggers, manual build runs | wraith:cloud-run build and trigger setup | `gcloud builds triggers run`, `gcloud builds log`, `gcloud services enable` | a trigger run executes a build; "For production environments, select a dedicated service account" | none | recommend with caveat |
| datalineage-bigquery-asset-impact-analysis | Blast radius of a BigQuery table or view change | wraith:plan-data-review impact check | `bq show` | none | none | recommend with caveat |
| datalineage-summary | Summarize upstream and downstream lineage as a report | wraith:bigquery provenance questions | `bq show`, `gcloud storage ls` | none | none | recommend with caveat |
| iam-helper-for-policy-management | Create and edit IAM allow and deny policies | wraith:security-audit remediation advice | `gcloud iam policies`, `gcloud iam list-testable-permissions` | covers `set-iam-policy` and deleting deny policies; refuses `allUsers` grants | none | recommend with caveat |
| iam-helper-for-policy-simulator | Simulate IAM policy changes against recent access, then apply | wraith:security-audit before any IAM change | `gcloud iam simulator replay-recent-access`, `gcloud projects get-iam-policy` | `gcloud projects set-iam-policy TARGET_PROJECT_ID /tmp/proposed_policy.json`; also folder and organization variants | none | recommend with caveat |
| iam-helper-for-privileged-access-management | Manage PAM entitlements, grants and approvals | wraith:security-audit for just-in-time access | `gcloud pam entitlements`, `gcloud pam grants` | `gcloud pam entitlements delete`; `gcloud pam grants revoke GRANT_ID`; asks "explicit confirmation" before changes | none | recommend with caveat |
| iam-helper-for-troubleshooting | Diagnose IAM access denials as requester or admin | wraith:security-audit for permission errors | none in SKILL.md (bundled `scripts/`) | resolver flow can provision PAM and IAM access | none | recommend with caveat |
| google-cloud-waf-security | Well-Architected security guidance and review questions | wraith:security-audit checklist source | none | none | none | recommend with caveat |
| google-cloud-waf-reliability | Well-Architected reliability, DR and RTO/RPO guidance | wraith:plan-infra-review reliability pass | none | none | none | recommend with caveat |
| google-cloud-waf-cost-optimization | Well-Architected FinOps and rightsizing guidance | wraith:plan-infra-review cost pass | none | none | none | recommend with caveat |
| google-cloud-waf-operational-excellence | Well-Architected CI/CD, monitoring and incident guidance | wraith:plan-infra-review operations pass | none | none | none | recommend with caveat |
| cloud-logging-query-generation | Generate Cloud Logging queries from plain language | wraith:bigquery or wraith:cloud-run log debugging | none (query text only) | attribution tag | none | recommend with caveat |
| google-cloud-slo-alert-configuration | PromQL SLO alert policies as Terraform | wraith:terraform-gcp alert authoring | `gcloud --quiet apphub applications`, `gcloud --quiet asset search-all-resources` | read-only discovery with `--quiet`; generates Terraform | none | recommend with caveat |
| gcloud | gcloud safety guardrails and output reduction | any wraith skill that runs gcloud | `gcloud help`, `gcloud topic`, `gcloud compute zones list` | "Pass the `--quiet` (or `-q`) global flag on all execution commands" | none | recommend with caveat |
| google-cloud-recipe-auth | IAM, ADC and service account authentication guidance | wraith:security-audit and wraith:setup auth advice | `gcloud auth application-default login`, `gcloud auth` | advises impersonation over service account keys (safe); login opens a browser | none | recommend with caveat |
| bigquery (plugin) `skills/bigquery-ai-ml` | Older BigQuery AI/ML SQL skill plus BigQuery MCP server | wraith:bigquery only if the MCP server is wanted | MCP via `npx -y @toolbox-sdk/server@1.10.0 --prebuilt bigquery --stdio` | downloads and runs an npm package each session; declares "Read" and "Write" capability; beta "may see breaking changes"; does not match `skills/cloud/bigquery-ai-ml` (different text, `version: "1.0"` against `"1.1.1"`, different reference files) | none | recommend with caveat |
| db-context-engineering `context-engineering-init` | Set up `autoctx/` workspace and Toolbox `tools.yaml` | wraith:context-layer when a Gemini Data Analytics agent is used | MCP via `uvx google-cloud-db-context-engineering@0.7.2` and `uvx toolbox-server@1.4.0` | creates `autoctx/` and `tools.yaml` holding database connection details; runs two `uvx` packages | none | recommend with caveat |
| db-context-engineering `context-engineering-bootstrap` | Draft an initial ContextSet from the database schema | wraith:context-layer first-draft step | MCP tools only | "clear the existing folder's contents" on overwrite; reads live schemas | none | recommend with caveat |
| db-context-engineering `context-engineering-dataset-generation` | Build a golden NLQ and SQL pair dataset | wraith:context-layer evaluation data | MCP `generate_dataset`, `<source>-execute-sql` | runs generated SQL against the user's database | none | recommend with caveat |
| db-context-engineering `context-engineering-evaluate` | Score a ContextSet against the golden set with Evalbench | wraith:context-layer evaluation step | MCP `generate_evalbench_configs`, Evalbench run | needs a `context_set_id` uploaded to a Google console; database credentials in `tools.yaml` | none | recommend with caveat |
| db-context-engineering `context-engineering-hillclimb` | Iterate on a ContextSet using evaluation failures | wraith:context-layer improvement loop | MCP `<source>-execute-sql` | runs generated SQL "to verify syntax"; rewrites context files each loop | none | recommend with caveat |
| db-context-engineering `context-engineering-workflow` | Orchestrate setup, evaluate and hill-climb as one workflow | wraith:context-layer entry point | none itself (calls the other skills) | inherits the risks of the skills it calls | none | recommend with caveat |
| db-context-engineering `context-generation-guide` | Authoring rules for templates, facets and value searches | wraith:context-layer authoring reference | none | none | none | recommend with caveat |
| knowledge-catalog (plugin, no SKILL.md) | MCP server and context file for Knowledge Catalog (Dataplex) | wraith:context-layer metadata lookups | MCP via `npx -y @toolbox-sdk/server@1.9.0 --prebuilt dataplex --stdio` | downloads and runs an npm package each session; beta "may see breaking changes"; no skill text to review | none | recommend with caveat |
| Out of scope: cloud, agent platform and Gemini API (25) | `agent-platform-alert-configuration`, `agent-platform-deploy`, `agent-platform-endpoint-management`, `agent-platform-eval-flywheel`, `agent-platform-inference`, `agent-platform-migrate-from-ai-studio`, `agent-platform-model-registry`, `agent-platform-prompt-management`, `agent-platform-rag-engine-management`, `agent-platform-skill-registry`, `agent-platform-troubleshooting`, `agent-platform-tuning`, `agent-platform-tuning-management`, `gemini-agents-api`, `gemini-api`, `gemini-interactions-api`, `gemini-live-api`, `google-agents-cli-onboarding`, `google-cloud-solution-agentic-ai-bidirectional-streaming`, `google-cloud-solution-agentic-ai-borderless-data-lakehouse`, `google-cloud-solution-agentic-ai-data-science-workflow`, `google-cloud-solution-agentic-analytics-spark-knowledge-catalog`, `google-cloud-solution-build-deploy-agents`, `google-cloud-solution-guided-gke-ai-migration`, `google-cloud-solution-multi-agent-security` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, GKE (42) | `gke-ai-troubleshooting-handle-disruption-gpu-tpu`, `gke-ai-troubleshooting-jobset-interruption`, `gke-ai-troubleshooting-node-unresponsive-timeout`, `gke-ai-troubleshooting-tpu-dynamic-slices-monitoring`, `gke-ai-troubleshooting-tpu-metrics-monitoring`, `gke-ai-troubleshooting-tpu-mxla-hang`, `gke-ai-troubleshooting-tpu-partition-overlap`, `gke-ai-troubleshooting-tpu-performance-degradation`, `gke-ai-troubleshooting-tpu-reservation-stockout`, `gke-ai-troubleshooting-tpu-slice-mig-stuck-updating`, `gke-ai-troubleshooting-tpu-vbar-oom`, `gke-ai-troubleshooting-tpu-vm-repair-stuck`, `gke-alert-configuration`, `gke-app-onboarding`, `gke-backup-dr`, `gke-basics`, `gke-batch-hpc`, `gke-cluster-autoscaler`, `gke-cluster-creation`, `gke-compute-classes`, `gke-cost-analysis`, `gke-cost-optimization`, `gke-custom-golden-image-discovery`, `gke-golden-path`, `gke-inference`, `gke-manifest-generation`, `gke-multitenancy`, `gke-networking`, `gke-node-notready`, `gke-observability`, `gke-platform-security`, `gke-productionize`, `gke-reliability`, `gke-service-networking`, `gke-storage`, `gke-storage-troubleshooting`, `gke-upgrades`, `gke-workload-identity`, `gke-workload-scaling`, `gke-workload-scaling-troubleshooting`, `gke-workload-security`, `gke-workload-troubleshooting` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, API management and integration (7) | `api-gateway-backend-security-and-rate-limiting`, `api-gateway-mcp-server`, `apigee-agent-gateway-governance`, `application-design-center-design-deploy`, `application-integration-authoring`, `application-integration-basics`, `application-integration-troubleshooting` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, security and compliance (13) | `assured-workloads-basics`, `assuredworkloads-environment-assessor`, `assuredworkloads-frameworks-author`, `assuredworkloads-frameworks-navigator`, `cloud-armor-crs-rule-upgrader`, `detection-engineering-coverage-evaluation`, `google-cloud-scc-query`, `google-cloud-scc-remediation`, `secops-cases`, `secops-detection-engineering`, `secops-hunt`, `secops-investigate`, `secops-triage` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, other databases (6) | `alloydb-basics`, `bigtable-basics`, `cloud-databases-onboarding`, `cloud-sql-basics`, `google-cloud-solution-hybrid-search-alloydb`, `spanner-basics` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, BigQuery, not vetted (1) | `bigquery-bigframes` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, Firebase and device platform (2) | `developer-device-platform-basics`, `firebase-basics` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, Genkit (4) | `developing-genkit-dart`, `developing-genkit-go`, `developing-genkit-js`, `developing-genkit-python` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, observability and logging (10) | `cloud-logging-configuration-basics`, `cloud-logging-cross-project-configuration`, `cloud-logging-finops`, `cloud-monitoring-chart-generation`, `cloud-monitoring-list-time-series-request`, `cloud-monitoring-metric-selection`, `cloud-monitoring-notification-channels-configuration`, `cloud-monitoring-promql-query`, `cloud-operator`, `cloud-trace-querying` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, networking (3) | `cloud-network-insights`, `google-cloud-global-frontend-configuration`, `google-cloud-networking-observability` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, storage and Filestore (8) | `google-cloud-filestore-auditing`, `google-cloud-filestore-autoscale`, `google-cloud-filestore-log-troubleshooting`, `google-cloud-filestore-nfs-browser`, `google-cloud-storage-basics`, `google-cloud-storage-bucket-architect`, `google-cloud-storage-diagnostic`, `google-cloud-storage-fuse` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, managed Airflow (4) | `managed-airflow-dag-authoring`, `managed-airflow-dag-troubleshooting`, `managed-airflow-migrations`, `managed-airflow-recommendations` | none | none | none | none | out of scope (not read) |
| Out of scope: cloud, solutions, recipes, other Well-Architected pillars and the rest (8) | `google-cloud-recipe-foundation-builder`, `google-cloud-recipe-onboarding`, `google-cloud-solution-architecture`, `google-cloud-solution-n-tier-serverless-web-app`, `google-cloud-solution-rag-enterprise-search-gke-sqldb`, `google-cloud-waf-performance-optimization`, `google-cloud-waf-sustainability`, `workload-manager-basics` | none | none | none | none | out of scope (not read) |
| Out of scope: top-level skills/ads (14) | `data-manager-api-audience-ingestion`, `data-manager-api-event-ingestion`, `data-manager-api-setup`, `google-ads-api-account-diagnostics`, `google-ads-api-mcp-setup`, `google-ads-api-quickstart`, `google-mobile-ads-android-migrate-to-next-gen`, `google-mobile-ads-banner`, `google-mobile-ads-get-started`, `google-mobile-ads-interstitial`, `google-mobile-ads-rewarded`, `google-mobile-ads-validate`, `ima-dai-sdk`, `ima-sdk-client-side` | none | none | none | none | out of scope (not read) |
| Out of scope: top-level skills/analytics (2) | `google-analytics-admin-api-basics`, `google-analytics-data-api-basics` | none | none | none | none | out of scope (not read) |
| Out of scope: top-level skills/developers (3) | `finding-google-skills`, `migrate-to-rust`, `retrieving-developer-knowledge` | none | none | none | none | out of scope (not read) |
| Out of scope: top-level skills/identity (2) | `dpop-adoption`, `sign-in-with-google-web` | none | none | none | none | out of scope (not read) |

## Decision

Every Google verdict is "recommend with caveat", so a wraith skill may name
any vetted skill above, never an out-of-scope one. Only wraith skills that
exist under `skills/` point to Google skills:

| wraith skill | Points to |
|---|---|
| wraith:bigquery | bigquery-basics, bigquery-optimization, bigquery-troubleshooting, bigquery-observability, bigquery-ai-ml, bigquery-udfs, datalineage-summary, datalineage-bigquery-asset-impact-analysis, cloud-logging-query-generation |
| wraith:dbt-bigquery | dbt-sf-to-bq-translator, bigquery-migration-sql-translator (migration work only) |
| wraith:cloud-run | cloud-run-basics, cloud-build-basics, cloud-run-alert-configuration |
| wraith:terraform-gcp | cloud-run-alert-configuration, google-cloud-slo-alert-configuration (Terraform output only; wraith runs the plan and apply) |
| wraith:security-audit | google-cloud-waf-security, iam-helper-for-troubleshooting, iam-helper-for-policy-simulator, iam-helper-for-policy-management, iam-helper-for-privileged-access-management, google-cloud-recipe-auth |
| wraith:plan-infra-review | google-cloud-waf-reliability, google-cloud-waf-cost-optimization, google-cloud-waf-operational-excellence |
| wraith:plan-data-review | datalineage-bigquery-asset-impact-analysis, bigquery-optimization |
| wraith:context-layer | context-engineering-workflow and context-generation-guide from db-context-engineering, and the knowledge-catalog plugin, only when the user already runs a Gemini Data Analytics agent or Knowledge Catalog |

`gcloud` is named by any wraith skill that tells the agent to run `gcloud`.

When a Google skill and wraith disagree, wraith wins, citing PLAN section 2.6:

- Datasets: "Terraform owns datasets, not tables." A wraith skill never runs
  the `bq mk --dataset` recipe from bigquery-basics, and never applies the
  dataset expirations from bigquery-optimization; both go through Terraform.
- Retention: "Storage is cheap and engineering time is not." Partition
  expiry and TTL advice from bigquery-optimization is raised with the user,
  not applied.
- Contracts and standards: "The contract is the source of truth" and
  "Standards are enforced, and exceptions are written down with a reason."
  Companion output is advice and never replaces a contract or a standard.
- Guardrails: "Automate the guardrails, not the work." Anything that changes
  production, IAM, or spend (cloud-run-basics deploys,
  `--allow-unauthenticated`, `set-iam-policy`, PAM changes,
  `gcloud storage rm -r`) needs the user's
  go-ahead in the current conversation (G17), whatever `--quiet` suggests.
- Telemetry: wraith skills tell the user that the attribution tag reports
  usage to Google and leave the choice to them (G11).

## Install

Commands from ADR 0001 C10, verified on both hosts:

| Companion | Host | Command that worked | Lands in |
|---|---|---|---|
| GCP | Claude Code | `claude plugin marketplace add google/skills` (name `google-plugins`), `claude plugin install bigquery@google-plugins` | plugin cache, `bigquery` 0.2.5 |
| GCP | Claude Code | `npx skills add google/skills --skill cloud-run-basics -a claude-code -y` | project `.claude/skills/cloud-run-basics/` |
| GCP | Copilot | `npx skills add google/skills --skill bigquery-basics -a github-copilot -y` | project `.agents/skills/bigquery-basics/` |

Not checked in C10, so unverified:

| Plugin | Host | Command | Status |
|---|---|---|---|
| db-context-engineering | Claude Code | `claude plugin install db-context-engineering@google-plugins` | unverified (not checked in C10) |
| knowledge-catalog | Claude Code | `claude plugin install knowledge-catalog@google-plugins` | unverified (not checked in C10) |

Caveats from C10:

- Only the `bigquery-ai-ml` skill of the `bigquery` plugin is bundled, plus a
  BigQuery MCP server. The other `skills/cloud/` skills sit outside any
  plugin, so they come from `npx skills`.
- `npx skills` (npm `skills` 1.7.4) needs Node >=22.20.0.
- It writes `skills-lock.json` to the project root.
- It has install telemetry, and ends with "Review skills before use; they run
  with full agent permissions."
- The `bigquery`, `db-context-engineering` and `knowledge-catalog` plugins
  start MCP servers with `npx -y` or `uvx`, which download packages when the
  session starts.

## Consequences

- wraith names Google skills by name and never copies them (G21). Names stay
  valid only while the reviewed SHA's folders exist; the Phase 7 sync should
  flag a renamed or removed skill.
- Because every verdict is capped, no wraith skill may depend on a Google
  skill to finish its own work. The Google skill is a pointer, not a step.
- The attribution tag means a user who installs these skills sends usage tags
  to Google. The README Companions section must say so.
- Plugin MCP servers fetch packages at run time. wraith hooks and bundled
  files stay offline (G11); the user opts in by installing the plugin.
- The plugin `bigquery-ai-ml` and the `skills/cloud/bigquery-ai-ml` skill
  differ. wraith points to the `skills/cloud/` copy unless the MCP server is
  wanted.
- 133 `skills/cloud/` folders and the ads, analytics, developers and identity
  areas were not read. A later ADR must vet any of them before wraith names
  one.

## Addendum 2026-11-03: pin bumped to 0c369ce

Ticket: WSK-00014. The GCP pin moved from 92776fb to
0c369ce1c8ab5f93b1d28752b8bea622b2eedcdc after a read-only re-vet of the 14
changed skills (issue 19). No injection, destructive command or unexpected
host was found. Accepted by the owner: the `agent-platform-*` skills gained a
"Usage Attribution" block that tags gcloud environment variables and
User-Agent headers with the skill name and version. It is opt-out and states
that it carries no user data. wraith still never copies these skills (G21).

## Addendum 2026-11-05: pin bumped to f70aa02

Ticket: WSK-00080. The GCP pin moved from 0c369ce to
f70aa02c5e8d1360169af143f4bfc0af68d73012. Sixteen skills changed upstream;
one of them is named under Decision: `dbt-sf-to-bq-translator` (upstream
commit 0f2afff, version 1.1.2 to 1.1.3). Its whole folder was read:
`SKILL.md`, `references/dbt_migration_patterns.md` and
`scripts/dbt_translator.py`.

- Cast semantics now match Snowflake one to one. `CAST` and `::TYPE`
  become `CAST`, which fails on bad data; only `TRY_CAST` and `TRY_TO_*`
  become `SAFE_CAST`. Before, every cast was a `SAFE_CAST`, which turns
  malformed keys into `NULL` without a word. The skill now agrees with
  "Fail loud, not silent".
- The script gains regex rewrites from `TRY_CAST` to `SAFE_CAST`. Its
  imports are unchanged, and the added lines add no command, host,
  network call or telemetry.
- The other fifteen changed skills are not named by wraith and were not
  read, as above.

Verdict unchanged: recommend with caveat, migration work only. The owner
accepts the bump by merging it.

## Addendum 2026-11-06: pin bumped to c2cf4ba

Ticket: WSK-00098. Drafted by the nightly upstream sync
(#95). The GCP pin moves from f70aa02 to
c2cf4ba74c0e47f0e7a81d29e053e740998a0ae2. Named skills changed: `gcloud`, `google-cloud-recipe-auth`.
Files changed: 2. Automated scan: no risk hits.

No machine read (no usable answer from the machine read),
so a human must read the diff in the pull request before
accepting it.

The owner accepts the bump by merging it, after reading the diff in
the pull request.

## Addendum 2026-11-07: pin bumped to 993b979

Ticket: WSK-00102. Drafted by the nightly upstream sync
(#95). The GCP pin moves from c2cf4ba to
993b979cf055de97dd15d4d5751d2672de561679. Named skills changed: `bigquery-ai-ml`.
Files changed: 11. Automated scan: no risk hits.

No machine read (no usable answer from the machine read),
so a human must read the diff in the pull request before
accepting it.

The owner accepts the bump by merging it, after reading the diff in
the pull request.

## Addendum 2026-11-13: pin bumped to 85f227e

Ticket: WSK-00116. Drafted by the nightly upstream sync
(#95). The GCP pin moves from 993b979 to
85f227ea6a8f347d34b76039d826c446f891f75d. Named skills changed: `bigquery-observability`, `bigquery-udfs`, `datalineage-summary`, `gcloud`, `google-cloud-waf-security`, `iam-helper-for-privileged-access-management`.
Files changed: 16. Automated scan: 16 risk hits (new-url).

No machine read (no usable answer from the machine read),
so a human must read the diff in the pull request before
accepting it.

The owner accepts the bump by merging it, after reading the diff in
the pull request.
