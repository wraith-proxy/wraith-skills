# Ontology YAML

The ontology's source of truth is one YAML file at `ontology_file` from the
wraith block. OWL 2 and SHACL exports are generated from it, never edited by
hand. See [example-ontology.yaml](example-ontology.yaml).

## Top-level keys

| Key | Holds |
|---|---|
| `meta` | `name`, `version`, `owner` |
| `classes` | classes keyed by name |
| `taxonomies` | controlled value sets keyed by name |
| `links` | relations between classes keyed by name |
| `axioms` | a list of rules that fix the interpretation |

## Status values

Every class, property and link carries `status`, one of:

- `proposed`: a candidate from extraction or a request; carries provenance and confidence.
- `evaluated`: reviewed by a domain expert, not yet decided.
- `accepted`: part of the ontology; consumers may rely on it.
- `remapped`: replaced; `doc` names the element that replaces it.
- `retired`: no longer valid; kept so old references resolve.

## Classes

```yaml
classes:
  Customer:
    doc: A person or organisation that holds at least one Account.
    status: accepted
    parent: Party          # optional, another class
    disjointWith: [Supplier]  # optional, list of classes
    properties:
      customer_id:
        type: string
        required: true
        doc: Stable identifier issued at onboarding.
        status: accepted
```

- `doc` is at least one sentence saying what the thing is, not where it is stored.
- Property `type` is one of `string`, `integer`, `decimal`, `boolean`, `date`, `timestamp`, or a taxonomy name.

## Taxonomies

```yaml
taxonomies:
  AccountType:
    doc: The product family an Account belongs to.
    values:
      current: Everyday account with a card.
      savings: Interest-bearing account without a card.
```

## Links

```yaml
links:
  holds:
    from: Customer
    to: Account
    cardinality: "1..*"
    inverse: heldBy
    doc: A Customer holds one or more Accounts.
    status: accepted
    provenance: onboarding process review, 2026-10-01
    confidence: high
```

- `cardinality` is written `min..max`, with `*` for unbounded: `0..1`, `1..1`, `0..*`, `1..*`.
- `provenance` says where the link came from (expert, document, extraction run). `confidence` is `low`, `medium` or `high`.

## Axioms

```yaml
axioms:
  - id: AX-001
    statement: Every Order is placed against exactly one Account.
    rationale: Billing and refunds resolve through the Account.
```

## Validation checklist

Run this on every change to `ontology_file` and fix every failure:

1. Every link `from` and `to`, and every class `parent`, is a key under `classes`.
2. No class lists its own `parent` (or any ancestor) in `disjointWith`.
3. Every element with `status: accepted` has a non-empty `doc`.
4. Every axiom has a non-empty `rationale`.

Also check, as review findings rather than failures:

- every `proposed` element has `provenance` and `confidence`;
- every `remapped` element names its replacement in `doc`;
- no `doc` contradicts an axiom.
