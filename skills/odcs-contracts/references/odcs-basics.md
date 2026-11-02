# ODCS basics

ODCS is the Open Data Contract Standard from Bitol. Contracts here use
v3.2.0. A working example is in [example-contract.yaml](example-contract.yaml).

## Schema URL

Validate against the official JSON Schema at the v3.2.0 tag:

```
https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/v3.2.0/schema/odcs-json-schema-v3.2.0.json
```

The `apiVersion` enum still accepts v3.1.0 and v3.0.x, so older contracts
stay valid. Do not upgrade them unless asked.

## Required top-level fields

The schema's top-level `required` list is exactly four fields:

| Field | Value |
|---|---|
| `version` | The contract's own version, semantic (`1.0.0`) |
| `apiVersion` | `v3.2.0` |
| `kind` | `DataContract` |
| `id` | A unique identifier, for example a UUID |

Wraith adds two of its own requirements on top of the standard: a `team`
with a `name` (an owner), and a `schema` with at least one object. The
`team` object form is current; the array form is deprecated.

## Fields the rules use

| Level | Field | Meaning |
|---|---|---|
| Object | `name` | Stable name consumers use (required by the schema) |
| Object | `physicalName` | What the source calls the table |
| Object | `properties` | The list of properties |
| Object | `quality` | Object-level quality rules |
| Property | `name` | Stable column name consumers use (required) |
| Property | `physicalName` | What the source calls the column |
| Property | `logicalType` | Portable type: `string`, `integer`, `timestamp`, ... |
| Property | `physicalType` | The type in the source system |
| Property | `required` | Whether nulls are forbidden |
| Property | `primaryKey` | `true` where the property is part of the key |
| Property | `primaryKeyPosition` | Order within a composite key, from 1 |
| Property | `description` | What the field means, at least 50 characters |
| Property | `classification` | Sensitivity label (see below) |
| Property | `quality` | Property-level quality rules (`metric`, `mustBe`) |
| Top | `slaProperties` | List of `property`, `value`, `unit`, `element` |
| Top | `team` | Owner: `name`, `members` |
| Top | `customProperties` | List of `property`, `value`; the only extension point |

## Classification

`classification` is a free string in the standard, so the closed set is a
wraith convention. The v3.2.0 schema has no field for declaring the set, so
declare it per contract in top-level `customProperties`, with the list as
`value`:

```yaml
customProperties:
  - property: wraith.classifications
    value: [public, internal, pii, psi]
```

Every property that holds personal or sensitive data then sets
`classification` to one member of that list. Reviewers check that no
property uses a label outside it.

## Exemptions and extensions

Top-level keys outside the standard are invalid. Put tool settings in
`customProperties` with a tool prefix (`dbt.`, `wraith.`). Record an
exemption from a lint or quality rule the same way, with its reason:

```yaml
customProperties:
  - property: wraith.exemption.description-length
    value: "Legacy column, meaning documented in the source catalogue."
```

## Versioning

Use semantic versions in `version`. Additive changes bump minor. Breaking
changes (type narrowing, renames, primary-key changes, optional to
required) bump major and need a migration plan and a consumer notice.
