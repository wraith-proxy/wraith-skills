# OWL 2 and SHACL export

Export only when a named consumer needs RDF. Generate from the YAML at
`ontology_file`; never edit the exports by hand. Export only `accepted`
elements unless the consumer asks for candidates.

## Mapping

| YAML | RDF |
|---|---|
| class | `owl:Class`, with `rdfs:comment` from `doc` |
| `parent` | `rdfs:subClassOf` |
| `disjointWith` | `owl:disjointWith` |
| property | `owl:DatatypeProperty` with `rdfs:domain` (the class) and `rdfs:range` (an `xsd:` type) |
| link | `owl:ObjectProperty` with `rdfs:domain` (`from`), `rdfs:range` (`to`) and `owl:inverseOf` (`inverse`) |
| `cardinality` | SHACL `sh:minCount` and `sh:maxCount` on a `sh:property` of the `from` class shape |
| `required: true` | SHACL `sh:minCount 1` |
| taxonomy | `sh:in` list on the property shape |

Types map `string` to `xsd:string`, `integer` to `xsd:integer`, `decimal` to
`xsd:decimal`, `boolean` to `xsd:boolean`, `date` to `xsd:date` and
`timestamp` to `xsd:dateTime`. A `*` maximum emits no `sh:maxCount`.

## Output

- `ontology.ttl`: the OWL 2 classes and properties.
- `shapes.ttl`: one `sh:NodeShape` per class, `sh:targetClass` set to it.

Write both next to `ontology_file` unless the consumer names a path.

## Tooling

Add to the user's project as dev dependencies only when an export is needed:

```bash
uv add --dev rdflib pyshacl
```

Build the graphs with rdflib in a small script in the user's project that
reads `ontology_file` with `yaml.safe_load` and serialises with
`graph.serialize(format="turtle")`.

## Validate

```bash
uv run pyshacl -s shapes.ttl -e ontology.ttl -f human data.ttl
```

`data.ttl` is a sample of instances from the consumer. Exit code 0 means
conforms. A failure is fixed in the YAML and the export regenerated.
