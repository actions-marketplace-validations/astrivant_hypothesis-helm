"""
Track lexical bindings independently of a template's dot context.
"""

from __future__ import annotations

from attrs import define, field

UNRESOLVED = object()


@define
class Scope:
    """
    Preserve declaration shadowing and assignments to the nearest enclosing binding.

    Attributes:
        bindings (dict[str, object]): Variables declared in this lexical block.
        parent (Scope | None): Enclosing block within the same template invocation.
    """

    bindings: dict[str, object] = field(factory=dict)
    parent: Scope | None = None

    def lookup(self, name: str) -> object:
        """
        Find a variable without crossing a template invocation boundary.

        Args:
            name (str): Variable name, including its dollar prefix.

        Returns:
            object: The nearest binding, or an unresolved marker.
        """
        if name in self.bindings:
            return self.bindings[name]
        return self.parent.lookup(name) if self.parent is not None else UNRESOLVED

    def bind(self, name: str, value: object, *, assign: bool = False) -> None:
        """
        Declare locally or update an existing binding in its owning block.

        Args:
            name (str): Variable being declared or assigned.
            value (object): Evaluated value, possibly explicitly unresolved.
            assign (bool): Update an existing declaration for Go's equals operator.

        Returns:
            None: The owning scope is updated.

        Raises:
            KeyError: Assignment targets a variable that has not been declared.
        """
        if not assign or name in self.bindings:
            self.bindings[name] = value
        elif self.parent is not None:
            self.parent.bind(name, value, assign=True)
        else:
            raise KeyError(name)
