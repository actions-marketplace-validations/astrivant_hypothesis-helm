"""
Generate isolated structural cases and independent exact manifest oracles.
"""

import json
from pathlib import Path
from textwrap import dedent

from hypothesis_helm.schemas.contracts import mapping

from scripts.benchmarking.workload import expected_output

STRUCTURES = (
    "constraints",
    "control-flow",
    "dependencies",
    "interactions",
    "equivalence",
    "boundaries",
)


def write_structure(chart: Path, name: str, offset: int) -> dict[str, object]:
    """
    Add one isolated structure while retaining the common normal-quantile observable.

    Args:
        chart (Path): Existing generated chart.
        name (str): Structural case name.
        offset (int): First input after the quantile bits.

    Returns:
        dict[str, object]: Structural metadata and finite domain size.
    """
    if name not in STRUCTURES:
        raise ValueError(f"unknown structure: {name}")
    schema_path = chart / "values.schema.json"
    schema = mapping(json.loads(schema_path.read_text()))
    properties = mapping(schema["properties"])
    paths = [f"input{offset + bit:03d}" for bit in range(4)]
    if any(path not in properties for path in paths):
        raise ValueError("structural cases require four inputs beyond quantile selectors")
    a, b, c, d = [".Values." + path for path in paths]
    if name == "constraints":
        schema["allOf"] = [
            {
                "if": {"properties": {paths[0]: {"const": True}}},
                "then": {"properties": {paths[1]: {"const": True}}},
                "else": {"properties": {paths[1]: {"const": False}}},
            }
        ]
        template = dedent(
            f"""
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: case-state
            data:
              coupled: "{{{{ {a} }}}}"
            """
        ).removeprefix("\n")
    elif name == "control-flow":
        template = dedent(
            f"""
            {{{{ if {a} }}}}
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: case-state
            data:
              gate: open
            {{{{ end }}}}
            {{{{ range until (ternary 3 1 {b}) }}}}
            ---
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: case-loop-{{{{ . }}}}
            data:
              member: present
            {{{{ end }}}}
            """
        ).removeprefix("\n")
    elif name == "dependencies":
        port = "{{ if " + a + " }}8080{{ else }}80{{ end }}"
        template = dedent(
            f"""
            apiVersion: v1
            kind: Service
            metadata:
              name: case-service
            spec:
              ports:
                - port: {port}
                  targetPort: {port}
            ---
            apiVersion: networking.k8s.io/v1
            kind: Ingress
            metadata:
              name: case-ingress
            spec:
              defaultBackend:
                service:
                  name: case-service
                  port:
                    number: {port}
            """
        ).removeprefix("\n")
    elif name == "interactions":
        template = dedent(
            """
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: case-state
            data:
              base: present
            """
        ).removeprefix("\n")
        template += "".join("{{ if " + path + " }}" for path in (a, b, c, d))
        template += dedent(
            f"""

            ---
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: case-rare
            data:
              region: rare
            {"{{ end }}" * 4}
            """
        ).removeprefix("\n")
    elif name == "equivalence":
        template = dedent(
            """
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: case-state
            data:
              constant: unchanged
            """
        ).removeprefix("\n")
    else:
        properties[paths[0]] = {"type": "integer", "enum": [0, 1, 2]}
        template = dedent(
            f"""
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: case-state
            data:
              replicas: "{{{{ {a} }}}}"
            {{{{ if ge (int {a}) 2 }}}}
            ---
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: case-boundary
            data:
              region: high
            {{{{ end }}}}
            """
        ).removeprefix("\n")
        defaults = (
            (chart / "values.yaml").read_text().replace(paths[0] + ": false", paths[0] + ": 0")
        )
        (chart / "values.yaml").write_text(defaults)
    schema["properties"] = properties
    schema_path.write_text(json.dumps(schema, indent=2) + "\n")
    (chart / "templates/structure.yaml").write_text(template)
    return {
        "name": name,
        "paths": paths,
        "oracle": "scripts.benchmarking.structures.expected_manifests",
    }


def valid_assignment(values: dict[str, object], spec: dict[str, object]) -> bool:
    """
    Independently decide the fixture's cross-input constraint.

    Args:
        values (dict[str, object]): Complete candidate assignment.
        spec (dict[str, object]): Generator metadata.

    Returns:
        bool: Assignment is allowed by the fixture contract.
    """
    structure = mapping(spec["structure"])
    paths = structure["paths"]
    assert isinstance(paths, list)
    return structure["name"] != "constraints" or values[str(paths[0])] == values[str(paths[1])]


def configmap(name: str, data: dict[str, object]) -> dict[str, object]:
    """
    Construct an oracle ConfigMap without inspecting the template.

    Args:
        name (str): Fixed resource name.
        data (dict[str, object]): Expected scalar fields.

    Returns:
        dict[str, object]: Complete expected resource.
    """
    return {"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": name}, "data": data}


def expected_manifests(
    values: dict[str, object], spec: dict[str, object]
) -> list[dict[str, object]]:
    """
    Calculate exact expected outputs for each structural fixture.

    Args:
        values (dict[str, object]): Complete valid input assignment.
        spec (dict[str, object]): Generator metadata.

    Returns:
        list[dict[str, object]]: Full expected manifest bundle, independent of Helm and compiler.
    """
    structure = mapping(spec["structure"])
    paths = structure["paths"]
    assert isinstance(paths, list)
    a, b, c, d = [values[str(path)] for path in paths]
    result = [configmap("matrix", {"value": expected_output(values, spec)})]
    match structure["name"]:
        case "constraints":
            result.append(configmap("case-state", {"coupled": str(a).lower()}))
        case "control-flow":
            if a:
                result.append(configmap("case-state", {"gate": "open"}))
            result.extend(
                configmap(f"case-loop-{index}", {"member": "present"})
                for index in range(3 if b else 1)
            )
        case "dependencies":
            port = 8080 if a else 80
            result.extend(
                [
                    {
                        "apiVersion": "v1",
                        "kind": "Service",
                        "metadata": {"name": "case-service"},
                        "spec": {"ports": [{"port": port, "targetPort": port}]},
                    },
                    {
                        "apiVersion": "networking.k8s.io/v1",
                        "kind": "Ingress",
                        "metadata": {"name": "case-ingress"},
                        "spec": {
                            "defaultBackend": {
                                "service": {"name": "case-service", "port": {"number": port}}
                            }
                        },
                    },
                ]
            )
        case "interactions":
            result.append(configmap("case-state", {"base": "present"}))
            if a and b and c and d:
                result.append(configmap("case-rare", {"region": "rare"}))
        case "equivalence":
            result.append(configmap("case-state", {"constant": "unchanged"}))
        case "boundaries":
            result.append(configmap("case-state", {"replicas": str(a)}))
            if int(str(a)) >= 2:
                result.append(configmap("case-boundary", {"region": "high"}))
        case _:
            raise ValueError("unknown structural oracle")
    return result
