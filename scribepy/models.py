"""Structured documentation models used by the parser and renderers."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ParameterDoc:
    """Represents a callable parameter."""

    name: str
    annotation: str | None = None
    default: str | None = None
    kind: str = "positional_or_keyword"


@dataclass(slots=True)
class FunctionDoc:
    """Represents a module-level function or class method."""

    name: str
    signature: str
    docstring: str
    decorators: list[str] = field(default_factory=list)
    returns: str | None = None
    parameters: list[ParameterDoc] = field(default_factory=list)
    lineno: int = 0
    is_async: bool = False


@dataclass(slots=True)
class ClassDoc:
    """Represents a documented Python class."""

    name: str
    docstring: str
    decorators: list[str] = field(default_factory=list)
    bases: list[str] = field(default_factory=list)
    methods: list[FunctionDoc] = field(default_factory=list)
    lineno: int = 0


@dataclass(slots=True)
class ModuleDoc:
    """Represents parsed documentation for a single module."""

    name: str
    path: str | None
    docstring: str
    imports: list[str] = field(default_factory=list)
    functions: list[FunctionDoc] = field(default_factory=list)
    classes: list[ClassDoc] = field(default_factory=list)
