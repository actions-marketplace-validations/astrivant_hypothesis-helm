# Astrivant integration observation

A local run against `../astrivant/helm/astrivant` with Helm 3.18.0-rc.2,
Hypothesis 6.168.0, and seed 0 passed default rendering, then found this
schema-valid override (JSON):

```json
{"\u007f": null}
```

The root schema permits additional properties. Helm rejected the key with
`yaml: control characters are not allowed`. The property runner saved the
counterexample after 26 attempts, including shrinking. This is an input-domain
mismatch between JSON Schema and Helm's conversion, not a proven application bug.
Restricting root additional properties is one possible chart contract change;
this framework deliberately does not silently narrow the schema to hide the issue.

Replay using this object in a JSON values file and
`helm template hypothesis ../astrivant/helm/astrivant --values <file>`.
The neighboring checkout can change, so this observation is not a fixed expected
failure in the test suite. The source chart was not modified.
