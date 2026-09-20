"""
Keep the complete user configuration example shared by exports and documentation.
"""

from textwrap import dedent

from hypothesis_helm.compiler.limits import LIMITS

__all__ = ("COMPILER_EXAMPLE", "COMPLETE_EXAMPLE", "GENERATION_EXAMPLE")


COMPILER_EXAMPLE = "compiler:\n" + "".join(f"  {name}: {default}  # {description}\n" for name, (default, description) in LIMITS.items())

GENERATION_EXAMPLE = (
    dedent(
        """
    # Global defaults for fresh generated text; supplied values are preserved.
    downstream_inputs: true  # Use constraints from supported downstream field mappings.
    yaml_parser: ruamel  # Rendered manifests: ruamel, ruamel-safe or pyyaml. Values files retain round-trip editing.
    findings:
      fail_on: null  # null: existing exit behavior; info, warning or error: fail fast at that severity or higher.
      severity:  # Optional per-code overrides; ignored/enabled still control whether a finding is emitted.
        HH2001: error  # Require documented values paths when a failure threshold is enabled.
        HH2003: info  # Missing descriptions remain informational.
    # Compiler budgets are positive integers; bytes, characters and counts are separate units.
    __COMPILER_EXAMPLE__
    hypothesis:
      character_sets: ascii  # ascii or unicode; explicit enum/const literals retain their alphabet.
      control_characters:
        exclude: true  # Exclude U+0000-U+001F and U+007F-U+009F, including tabs and DEL.
        allow: ["\\n", "\\r"]  # Exceptions; [] excludes every control character.
      exclude_characters: ""  # Additional literal characters to exclude, e.g. ">|".
      max_examples: 10  # Per path property, not a shared budget for a branch.
      deadline_ms: null  # No Hypothesis per-example deadline; chart/render timeouts still apply.
      phases: [generate, shrink]  # Use [generate] to omit shrinking.
      suppress_health_check: [too_slow]  # Use [] to retain all ordinary health checks.

    input_constraints:
      - charts:
          # Every source/name pairing in this row is eligible. Patterns are case-sensitive.
          - sources:
              - https://github.com/example/charts.git
              - git@github.com:example/charts.git
              - ./charts
            names: [example, example-worker]
        path: $  # Whole chart; descendants inherit these partial overrides.
        findings:
          fail_on: error  # Override the global threshold for these charts.
          severity:
            HH2003: info  # Other code severities retain their inherited settings.
        compiler:  # Chart-wide budgets, including dependencies; only accepted with path: $.
          max_call_depth: 64  # Other limits inherit the global compiler settings.
          max_steps: 20000
        hypothesis:
          character_sets: ascii
          max_examples: 20

      - charts: [example]  # Chart.yaml names or glob patterns; any source.
        path: $.credentials
        ignored: [HH2001]  # Silence this code only within this branch.
        hypothesis:
          max_examples: 30
          deadline_ms: 5000

      - charts: [example]
        path: $.credentials.secretName
        profile: kubernetes-secret-name
        allow_empty: true  # Only if the chart's own schema also permits an empty string.
        enabled: [HH2001]  # More specific than the credentials suppression.

      - charts: [example]
        path: $.credentials.mountPath
        profile: absolute-posix-path  # Alternative to a self-contained inline schema.

      - charts: [example]
        path: $.containers[*].label
        findings:
          severity:
            HH2001: warning  # Override this branch only; fail_on still inherits.
        schema:
          type: string
          minLength: 1
          maxLength: 40
        hypothesis:
          character_sets: unicode
          control_characters:
            exclude: true
            allow: []
          exclude_characters: ">|"
          max_examples: 50
          phases: [generate]
          suppress_health_check: [too_slow, filter_too_much]

    # Whole-resource JSON schemas, relative to this configuration file.
    # Remove this entry until you supply the schema; it is required when present.
    resource_schemas:
      example.org/v1/Widget: ./schemas/widget.json
    """
    )
    .lstrip()
    .replace("__COMPILER_EXAMPLE__\n", COMPILER_EXAMPLE)
)

COMPLETE_EXAMPLE = "ignored: [HH2006]  # Other findings remain enabled.\n\n" + GENERATION_EXAMPLE
