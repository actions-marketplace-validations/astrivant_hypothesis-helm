"""
Keep the complete user configuration example shared by exports and documentation.
"""

from textwrap import dedent

GENERATION_EXAMPLE = dedent(
    """
    # Global defaults for fresh generated text; supplied values are preserved.
    downstream_inputs: true  # Use constraints from supported downstream field mappings.
    compiler:
      max_call_depth: 16  # Nested helper calls analyzed; --compiler-call-depth overrides this.
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
).lstrip()

COMPLETE_EXAMPLE = "ignored: [HH2006]  # Other findings remain enabled.\n\n" + GENERATION_EXAMPLE
