---
name: odcs-contracts
description: "Use when writing, validating or changing a data contract, or when a dataset needs its schema, quality rules, SLAs or personal-data classification defined. Works in ODCS v3.2.0 (Open Data Contract Standard) YAML, treats the contract as the source of truth, and keeps dbt models in step with it."
license: MIT
metadata:
  source: new
---

# ODCS contracts

## When to use

Writing, validating or changing a data contract in ODCS v3.2.0 YAML.
Also when a dataset needs schema, quality rules, SLAs or classification.

## Rules

1. Contracts use ODCS v3.2.0: `apiVersion: v3.2.0`, `kind: DataContract`. v3.1.0 and v3.0.x contracts stay valid; do not upgrade them unless asked.
2. Validate every contract against the official v3.2.0 JSON Schema before committing. Top-level keys outside the standard are invalid; tool-specific settings go in `customProperties` with a tool prefix.
3. The contract is the source of truth and the change-management mechanism. Models are downstream: generate or check raw and staging models from the contract, and never hand-edit generated models.
4. Each schema object has a stable `name` (what consumers use) and a `physicalName` (what the source calls it). Each property has `name`, `physicalName`, `logicalType`, `physicalType`, `required`, a `description`, and `primaryKey: true` where it is part of the key.
5. Descriptions are at least 50 characters and say what the field means, not what it is called.
6. Every property holding personal or sensitive data carries `classification`, from one closed set declared per contract (for example `public`, `internal`, `pii`, `psi`). Classification decides encryption and access (wraith:bigquery).
7. Quality rules live in the contract's `quality` entries and become dbt tests. SLAs (freshness, retention, latency) live in `slaProperties` with the behaviour on breach.
8. Missing source columns fail generation. No silent passes.
9. Additive changes (a new optional property, a new object) may be automated. Type narrowing, renames, primary-key changes and optional-to-required flips are breaking: they need a major version bump, a migration plan and a consumer notice.
10. CI fails when the models on disk differ from what the contract would generate.
11. Exceptions are written down: an exemption from a lint or quality rule carries its reason in `customProperties`.
12. Every contract names an owning team. An ownerless contract is a review blocker.

## Workflow

Contracts live in `<contracts_dir>`, read from the `## wraith` block of the project's AGENTS.md. If the key is missing, ask once and suggest wraith:setup.

Create:
1. Start from the request or design: objects, keys, owners, sensitive fields. Ask for whatever is missing.
2. Draft the contract from [example-contract.yaml](references/example-contract.yaml), following [odcs-basics.md](references/odcs-basics.md).
3. Declare the classification set, classify each sensitive property, name the owning team.
4. Validate (see Commands).
5. Generate or check the models per [contract-to-dbt.md](references/contract-to-dbt.md) (wraith:dbt-bigquery).
6. Commit the contract, models and tests together.

Change:
1. Classify the change as additive or breaking (rule 9).
2. Set the new `version`: minor for additive, major for breaking.
3. Validate, then regenerate the models.
4. Run the drift check; it must show no difference.
5. For a breaking change, write the migration plan and notify consumers.

## Commands

All paths come from `<contracts_dir>`. `uvx` downloads the validator, and the agent runs it visibly.

- Validate: `uvx check-jsonschema==0.39.0 --schemafile https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/v3.2.0/schema/odcs-json-schema-v3.2.0.json <contract>`
- If the project uses datacontract-cli (pin 1.2.9): `datacontract lint <contract>` and `datacontract test <contract>`.
- If it uses wraith-modelgen: `modelgen validate --strict <contract>` and `modelgen check --from-contract --diff`.

## Review checklist

- each contract change classified as additive or breaking
- a breaking change has a version bump and consumer notice
- new fields mapped to ontology terms or flagged

## References

- [odcs-basics.md](references/odcs-basics.md): schema URL, required fields, field table, classification.
- [example-contract.yaml](references/example-contract.yaml): a trimmed official example that validates.
- [contract-to-dbt.md](references/contract-to-dbt.md): how contract parts become models, tests and freshness.
