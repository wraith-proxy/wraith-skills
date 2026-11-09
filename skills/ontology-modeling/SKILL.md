---
name: ontology-modeling
description: "Use when defining what business entities are and how they relate: an ontology, taxonomy or domain model beyond a glossary. Separates meaning from facts, models the business rather than the database, and keeps a YAML source of truth with classes, properties, links, axioms and a trust lifecycle."
license: MIT
metadata:
  source: new
---

# Ontology Modeling

## When to use

Defining what business entities are and how they relate, beyond a glossary.
Covers classes, properties, links, taxonomies, axioms and their trust lifecycle.

## Rules

1. Keep five artifacts apart:
   - ontology: the schema layer of classes, properties and restrictions (what something is and what may relate to it);
   - knowledge graph: instances (what is true now);
   - taxonomy: an is-a hierarchy;
   - semantic layer: reusable metric definitions (how to calculate);
   - context graph: the slice one decision needs at runtime, or a durable record of decisions; name which.
2. Meaning is not the same as facts. Durable meaning goes in the ontology, current evidence in source systems and graphs, decision context in the agent runtime.
3. Model the business, not the database. Renaming `cust_mstr` to `Customer` keeps the source's accidents. Discover, then formalize: extract candidate entities, get expert review into a seed ontology, then re-extract with the ontology as guidance.
4. Fertility test: an ontology is vocabulary plus axioms plus annotations that fix an intended interpretation. A list of terms with definitions is a glossary; write it to the `glossary` file named in the wraith block.
5. Annotations must not contradict axioms. A class documented as a kind of Dog must not be declared disjoint from Dog.
6. Every class, property and link has a status: proposed, evaluated, accepted, remapped or retired. Candidates carry provenance and confidence. Extraction output is evidence, not knowledge.
7. Sophistication is a cost, not a default. Build an ontology only when the domain is cross-domain and interconnected; otherwise a curated glossary or index wins.
8. Centralise the resolution of meaning, not the storage of data.
9. Contracts link to the ontology: ODCS objects and properties reference ontology terms through `customProperties` (`ontologyClass`, `ontologyProperty`). An unmapped contract field is flagged in review, not blocked.
10. Use upper ontologies (BFO, DOLCE, schema.org, Dublin Core) only when interoperating with another organisation's ontology.
11. Produce OWL 2 and SHACL exports only when a consumer needs RDF. Generate them from the YAML source of truth and validate with pySHACL.

## Workflow

1. Read the `## wraith` block of AGENTS.md: `ontology_file`, `glossary`, `contracts_dir`. If a key is missing, ask once and suggest wraith:setup.
2. Apply the fertility test and the cost test (rules 4 and 7). If a glossary is enough, stop and write the terms to the `glossary` file named in the wraith block.
3. Name which of the five artifacts the user is asking for (rule 1). Only the ontology belongs in `<ontology_file>`.
4. Discover: list candidate classes, properties and links from the business process, the glossary and source systems. Mark each `proposed` with provenance and confidence (rules 3 and 6).
5. Review the candidates with the domain expert. Move each to `evaluated`, then `accepted`, `remapped` or `retired`. Never accept extraction output without that review.
6. Write or update `<ontology_file>` in the format of [references/ontology-yaml.md](references/ontology-yaml.md) and run its validation checklist. Fix every failure, including annotations that contradict axioms (rule 5).
7. Map contracts: for each ODCS object and property in `<contracts_dir>`, add `ontologyClass` or `ontologyProperty` in `customProperties`. List unmapped fields as review findings (rule 9).
8. Export to OWL 2 and SHACL only when a named consumer needs RDF, by [references/owl-shacl-export.md](references/owl-shacl-export.md) (rule 11).

## Commands

Every value is a wraith block key.

```bash
uv run python -c "import yaml; yaml.safe_load(open('<ontology_file>'))"
grep -rL "ontologyClass" <contracts_dir>
uv run pyshacl -s shapes.ttl -e ontology.ttl -f human data.ttl
```

The last command runs only after an export (rule 11).

## References

- [references/ontology-yaml.md](references/ontology-yaml.md): the source-of-truth format at `ontology_file` and the validation checklist.
- [references/example-ontology.yaml](references/example-ontology.yaml): Customer, Account and Order with one taxonomy, two links and two axioms.
- [references/owl-shacl-export.md](references/owl-shacl-export.md): YAML to OWL 2 and SHACL mapping, rdflib and pySHACL.
