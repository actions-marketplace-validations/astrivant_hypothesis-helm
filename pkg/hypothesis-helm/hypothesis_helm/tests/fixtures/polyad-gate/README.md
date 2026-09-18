# Polyad custom-resource test fixture

<!-- toc:start -->
**Table of contents**

- [Snapshot](#snapshot)
- [Coverage](#coverage)
<!-- toc:end -->

Source: [astrivant/polyad](https://github.com/astrivant/polyad), revision
`3d77e3e694db0f72b92a9a9e1285a80e42610e4d`, copied from the local `../reflow` checkout.
Upstream files retain their GPL-3.0 license; see the repository [license](../../../../../../LICENSE).

## Snapshot

`Chart.yaml`, `templates/`, and `crds/gates.yaml` are unchanged copies from `charts/polyad-crds/`.
`schemas/gate.json` is copied from `pkg/polyad-schemas/polyad_schemas/resources/gate.v1alpha1.schema.json`.
The resource catalog and values schema retain only the Gate entry and shared renderer controls.
The values and tool configuration are local test inputs. No neighboring checkout or network is needed in CI.

## Coverage

Tests render the real helper and `tpl` implementation with Helm, validate custom-resource boundaries,
reject missing or mismatched resource schemas, and preserve schemas in saved suites.
A separate direct-mapping template exercises input-domain inference and reports a deliberately introduced
output defect. Mixed bundles route custom resources to their supplied schema and built-ins to kubeconform.

Gate's CEL expression requires exactly one of `expression` and `delaySeconds`. JSON Schema validation does
not execute that rule, admission webhooks, or controller behavior; those require Kubernetes-side tests.
