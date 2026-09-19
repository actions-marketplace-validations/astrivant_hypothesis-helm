"""
Give the shared fixture varied values depths without changing its rendered behavior.
"""

import json
from pathlib import Path

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.schemas.contracts import mapping, sequence

from hypothesis_helm_benchmarking.charts.fixture import FixtureWorkspace, chart_path, record_change


def nest_inputs(logical: Path, *, workspace: FixtureWorkspace | None = None) -> dict[str, list[str]]:
    """
    Put successive inputs at depths one, two and three and preserve schema constraints.

    Args:
        logical (Path): Shared fixture identity or physical chart directory.
        workspace (FixtureWorkspace | None): Owner of the generated chart.

    Returns:
        dict[str, list[str]]: Original oracle selectors mapped to their new values paths.
    """
    chart = chart_path(logical, workspace=workspace)
    schema = mapping(json.loads((chart / "values.schema.json").read_text()))
    defaults = mapping(yamlio.load((chart / "values.yaml").read_text()))
    paths = {name: [*(f"level{depth}" for depth in range(index % 3)), name] for index, name in enumerate(defaults)}

    def nested_schema(fragment: dict[str, object], *, closed: bool = False) -> dict[str, object]:
        """
        Move flat property constraints to the same nested paths as the values.

        Args:
            fragment (dict[str, object]): Base schema or conditional property constraint.
            closed (bool): Require the full object hierarchy in the base schema.

        Returns:
            dict[str, object]: Equivalent constraint on nested inputs.
        """
        result: dict[str, object] = {"properties": {}}
        for name, spec in mapping(fragment.get("properties", {})).items():
            node = result
            for part in paths[name][:-1]:
                properties = mapping(node.setdefault("properties", {}))
                node = mapping(properties.setdefault(part, {"properties": {}}))
            mapping(node["properties"])[paths[name][-1]] = spec

        def close(node: dict[str, object]) -> None:
            """
            Require all known fields while keeping each nested object closed.

            Args:
                node (dict[str, object]): Newly constructed object schema.

            Returns:
                None: Finite object constraints are installed recursively.
            """
            properties = mapping(node["properties"])
            node.update(type="object", required=list(properties), additionalProperties=False)
            for child in properties.values():
                if "properties" in mapping(child):
                    close(mapping(child))

        if closed:
            close(result)
        return result

    output_schema = nested_schema(schema, closed=True)
    if "allOf" in schema:
        output_schema["allOf"] = [
            {branch: nested_schema(mapping(fragment)) for branch, fragment in mapping(condition).items()}
            for condition in sequence(schema["allOf"])
        ]
    values: dict[str, object] = {}
    for name, path in paths.items():
        node = values
        for part in path[:-1]:
            node = mapping(node.setdefault(part, {}))
        node[path[-1]] = defaults[name]
    (chart / "values.yaml").write_text(yamlio.dump(values))
    (chart / "values.schema.json").write_text(json.dumps(output_schema, indent=2) + "\n")
    for template in (chart / "templates").glob("*.yaml"):
        text = template.read_text()
        for name in sorted(paths, key=len, reverse=True):
            text = text.replace(f".Values.{name}", ".Values." + ".".join(paths[name]))
        template.write_text(text)
    metadata_path = chart / "benchmark.json"
    metadata = json.loads(metadata_path.read_text())
    metadata["values_paths"] = paths
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")
    record_change(logical, "nested_inputs", {}, workspace=workspace)
    return paths
