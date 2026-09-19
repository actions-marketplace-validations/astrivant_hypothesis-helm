"""
Maintain the built-in finding library with evidence criteria and repair guidance.
"""

from typing import Literal

from attrs import frozen

type Severity = Literal["info", "warning", "error"]

CATEGORY_RANGES = {"unclassified": (1000, 1099), "manifest": (1100, 1199), "execution": (1200, 1299)}


@frozen
class Rule:
    """
    Define one observed condition, independently of how a check reports it.

    Attributes:
        code (str): Stable identifier used by ignore policies.
        title (str): Concise name of the observed condition.
        category (str): Manifest, template, values, execution, analysis or unclassified.
        kind (Literal["violation", "warning", "diagnostic"]): Whether evidence establishes a failed contract, a gap or a limitation.
        severity (Severity): Default CI impact, independent of evidence kind.
        detection (str): Evidence required to emit this finding.
        example (str): Illustrative input or output exhibiting the condition.
        remediation (str): Suggested investigation or repair, without claiming an unobserved cause.
    """

    code: str
    title: str
    category: str
    kind: Literal["violation", "warning", "diagnostic"]
    severity: Severity
    detection: str
    example: str
    remediation: str


DEFINITIONS = (
    Rule(
        "HH1001",
        "Unclassified template failure",
        "unclassified",
        "diagnostic",
        "error",
        "Helm template exits unsuccessfully without a recognized diagnostic.",
        "A chart-specific fail message that has not been verified as an input constraint.",
        "Inspect the Helm diagnostic and reproducer; the exit alone does not establish a chart defect.",
    ),
    Rule(
        "HH1201",
        "Render invocation timed out",
        "execution",
        "diagnostic",
        "warning",
        "The Helm subprocess exceeds its invocation deadline.",
        "A render takes longer than the configured timeout.",
        "Check runner load and render cost, then adjust the timeout if appropriate. This is incomplete validation, not proof of a bug.",
    ),
    Rule(
        "HH1101",
        "Invalid YAML in rendered output",
        "manifest",
        "violation",
        "error",
        "The YAML parser rejects rendered output, or Helm reports a YAML parse error.",
        "A substituted value breaks YAML indentation.",
        "Inspect the failing YAML and template interpolation, including quoting and indentation.",
    ),
    Rule(
        "HH1102",
        "Manifest document is not an object",
        "manifest",
        "violation",
        "error",
        "A nonempty rendered document is a scalar or sequence instead of a mapping.",
        "A template emits a bare string document.",
        "Emit a resource mapping or remove the stray document.",
    ),
    Rule(
        "HH1103",
        "Missing resource API version or kind",
        "manifest",
        "violation",
        "error",
        "A resource has no nonempty string apiVersion or kind.",
        "kind: null",
        "Supply both resource identifiers in every branch that emits a resource.",
    ),
    Rule(
        "HH1104",
        "Invalid resource list",
        "manifest",
        "violation",
        "error",
        "A resource with kind List has no array-valued items field.",
        "kind: List with items: null",
        "Emit an items array, including an empty array when appropriate.",
    ),
    Rule(
        "HH1105",
        "Missing resource name",
        "manifest",
        "violation",
        "error",
        "The resource fails the tool's nonempty metadata.name contract.",
        'metadata: {name: ""}',
        "Provide a name in each resource branch; ignore this check if your workflow intentionally uses generated names.",
    ),
    Rule(
        "HH1106",
        "Duplicate resource identity",
        "manifest",
        "violation",
        "error",
        "Two resources in the checked bundle share apiVersion, kind, namespace and name.",
        "Enabling an optional component emits a second ConfigMap with the same identity.",
        "Give the resources distinct names or make their activation conditions exclusive.",
    ),
    Rule(
        "HH1107",
        "Empty resource bundle",
        "manifest",
        "violation",
        "error",
        "The active test requires resources but this configuration renders none.",
        "All resource-producing branches are disabled.",
        "Check resource activation; ignore this contract if an empty chart is intentional.",
    ),
    Rule(
        "HH1108",
        "Kubernetes schema validation failed",
        "manifest",
        "violation",
        "error",
        "The configured Kubernetes validator rejects the output.",
        "An unquoted boolean becomes a non-string ConfigMap data value.",
        "Use the validator's field path and expected type to check the template and input schema.",
    ),
    Rule(
        "HH1109",
        "Invalid manifest field type",
        "manifest",
        "violation",
        "error",
        "Helm parses the YAML but cannot decode a field into its required manifest type.",
        "An annotation contains an array instead of a string.",
        "Check the field named in Helm's decoding error and constrain its values to the required type.",
    ),
    Rule(
        "HH1011",
        "Rendered output cannot be encoded as JSON",
        "unclassified",
        "diagnostic",
        "error",
        "Manifest processing reports a JSON representation failure.",
        "A YAML tag produces an unsupported Python scalar object.",
        "Inspect YAML tags and parser support to determine whether the failure comes from an unsupported value or a chart defect.",
    ),
    Rule(
        "HH1012",
        "Unclassified baseline lint failure",
        "unclassified",
        "diagnostic",
        "error",
        "Helm lint fails on the supplied chart defaults.",
        "Lint reports an error before generated inputs are tested.",
        "Read the lint diagnostic; distinguish chart errors from missing dependencies or environment requirements.",
    ),
    Rule(
        "HH2001",
        "Undocumented values path",
        "values",
        "warning",
        "warning",
        "The audit finds a values path with no matching schema declaration.",
        "Templates read service.mode but its schema entry is absent.",
        "Document the path in values.schema.json, including its accepted values.",
    ),
    Rule(
        "HH2002",
        "Unspecified values type",
        "values",
        "warning",
        "warning",
        "A schema path declares no type, enum or const.",
        'service.mode has only a description: "Service mode".',
        "Declare the accepted type or a finite set of values.",
    ),
    Rule(
        "HH2003",
        "Missing values description",
        "values",
        "warning",
        "info",
        "A typed schema path has no description.",
        "A boolean gate is declared without explaining which component it enables.",
        "Describe the field's behavior and any requirements shared with other fields.",
    ),
    Rule(
        "HH2004",
        "No supplied default for a values path",
        "values",
        "warning",
        "warning",
        "A discovered path is absent from the original values file.",
        "A conditional branch reads credentials.token, which defaults omit.",
        "Supply a default or document when users must provide the field. Render the relevant configurations to check its requirements.",
    ),
    Rule(
        "HH2005",
        "Unresolved template value access",
        "analysis",
        "diagnostic",
        "warning",
        "Static analysis cannot resolve a template's values access.",
        "An index expression selects a key computed at runtime.",
        "Review the dynamic access and coverage report. Exercise the affected inputs to establish their rendering behavior.",
    ),
    Rule(
        "HH2006",
        "Opaque object schema",
        "values",
        "warning",
        "warning",
        "An object permits unspecified entries without named fields, patterned fields or a typed map-value schema.",
        'extraConfig: {"type": "object"} permits unspecified keys and values.',
        "Describe fields with properties, patternProperties or typed additionalProperties. "
        "Ignore HH2006 for intentional free-form configuration; tests still sample those values.",
    ),
    Rule(
        "HH2007",
        "Incomplete compiler analysis",
        "analysis",
        "warning",
        "warning",
        "An evaluated template operation needs context or semantics outside the supported compiler contract.",
        "A rejection guard depends on now, lookup, random data or an unsupported tpl expression.",
        "The candidate is retained for native Helm rendering. Review the source location and coverage; "
        "suppress HH2007 to silence this warning without dropping tests. "
        "--fail stops at this finding when its severity meets the configured threshold.",
    ),
    Rule(
        "HH3001",
        "Template accesses a missing object",
        "template",
        "violation",
        "error",
        "Helm reports a nil pointer while evaluating a template field.",
        "A template reads .Values.service.port when service is absent.",
        "Guard or default the parent object, or require it in the values schema.",
    ),
    Rule(
        "HH3002",
        "Incompatible value type in template",
        "template",
        "violation",
        "error",
        "Helm reports a wrong value type, a field unavailable on a type, or an unsupported range operand.",
        "A string-only template function receives a boolean allowed by the input schema.",
        "Align the template operation with the accepted input types, or narrow the schema.",
    ),
    Rule(
        "HH3003",
        "Undefined named template",
        "template",
        "violation",
        "error",
        "Helm reports that a called named template is not defined.",
        'include "service.name" . refers to an absent helper.',
        "Check the helper name, its definition and dependency availability.",
    ),
)

CATALOG = {rule.code: rule for rule in DEFINITIONS}
if len(CATALOG) != len(DEFINITIONS):
    raise ValueError("Finding codes must be unique")
for _rule in DEFINITIONS:
    if _rule.category in CATEGORY_RANGES:
        _lower, _upper = CATEGORY_RANGES[_rule.category]
        if not _lower <= int(_rule.code[2:]) <= _upper:
            raise ValueError(f"{_rule.code} is outside the reserved {_rule.category} range")
