"""AST-backed parser for extracting Python API documentation."""

from __future__ import annotations

import ast
from pathlib import Path

from .models import ClassDoc, FunctionDoc, ModuleDoc, ParameterDoc


def parse_source(source_code: str, module_name: str = "module", path: str | None = None) -> ModuleDoc:
    """Parse Python source code into a structured module representation."""
    tree = ast.parse(source_code)
    module = ModuleDoc(
        name=module_name,
        path=path,
        docstring=ast.get_docstring(tree) or "",
        imports=[],
        functions=[],
        classes=[],
    )

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module.imports.extend(_parse_import(node))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            module.functions.append(_parse_function(node))
        elif isinstance(node, ast.ClassDef):
            module.classes.append(_parse_class(node))

    return module


def parse_file(path: str | Path, module_name: str | None = None) -> ModuleDoc:
    """Parse a Python file from disk."""
    file_path = Path(path)
    source_code = file_path.read_text(encoding="utf-8")
    return parse_source(
        source_code=source_code,
        module_name=module_name or file_path.stem,
        path=str(file_path),
    )


def _parse_import(node: ast.Import | ast.ImportFrom) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]

    prefix = "." * node.level + (node.module or "")
    return [f"{prefix}.{alias.name}".strip(".") for alias in node.names]


def _parse_class(node: ast.ClassDef) -> ClassDoc:
    methods = [
        _parse_function(member)
        for member in node.body
        if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    return ClassDoc(
        name=node.name,
        docstring=ast.get_docstring(node) or "",
        decorators=[_expr_to_source(item) for item in node.decorator_list],
        bases=[_expr_to_source(base) for base in node.bases],
        methods=methods,
        lineno=node.lineno,
    )


def _parse_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> FunctionDoc:
    parameters = _parse_parameters(node.args)
    signature = _build_signature(node.name, parameters, _annotation(node.returns))
    return FunctionDoc(
        name=node.name,
        signature=signature,
        docstring=ast.get_docstring(node) or "",
        decorators=[_expr_to_source(item) for item in node.decorator_list],
        returns=_annotation(node.returns),
        parameters=parameters,
        lineno=node.lineno,
        is_async=isinstance(node, ast.AsyncFunctionDef),
    )


def _parse_parameters(args: ast.arguments) -> list[ParameterDoc]:
    parameters: list[ParameterDoc] = []

    positional = list(args.posonlyargs) + list(args.args)
    positional_defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)

    for arg, default in zip(positional, positional_defaults):
        kind = "positional_only" if arg in args.posonlyargs else "positional_or_keyword"
        parameters.append(_parameter_doc(arg, default, kind))

    if args.vararg:
        parameters.append(_parameter_doc(args.vararg, None, "var_positional"))

    if args.kwonlyargs and not args.vararg:
        parameters.append(ParameterDoc(name="*", kind="keyword_only_marker"))

    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        parameters.append(_parameter_doc(arg, default, "keyword_only"))

    if args.kwarg:
        parameters.append(_parameter_doc(args.kwarg, None, "var_keyword"))

    return parameters


def _parameter_doc(arg: ast.arg, default: ast.expr | None, kind: str) -> ParameterDoc:
    return ParameterDoc(
        name=arg.arg,
        annotation=_annotation(arg.annotation),
        default=_expr_to_source(default) if default is not None else None,
        kind=kind,
    )


def _build_signature(name: str, parameters: list[ParameterDoc], returns: str | None) -> str:
    rendered: list[str] = []
    seen_kwonly = False
    positional_only_count = sum(param.kind == "positional_only" for param in parameters)
    positional_seen = 0

    for param in parameters:
        if param.kind == "keyword_only_marker":
            rendered.append("*")
            seen_kwonly = True
            continue

        if param.kind == "var_positional":
            rendered.append(_render_parameter(param, prefix="*"))
            seen_kwonly = True
        elif param.kind == "var_keyword":
            rendered.append(_render_parameter(param, prefix="**"))
        else:
            rendered.append(_render_parameter(param))

        if param.kind == "positional_only":
            positional_seen += 1
            if positional_seen == positional_only_count:
                rendered.append("/")

    signature = f"{name}({', '.join(rendered)})"
    if returns:
        signature += f" -> {returns}"
    return signature


def _render_parameter(parameter: ParameterDoc, prefix: str = "") -> str:
    text = f"{prefix}{parameter.name}"
    if parameter.annotation:
        text += f": {parameter.annotation}"
    if parameter.default is not None:
        text += f" = {parameter.default}"
    return text


def _annotation(node: ast.expr | None) -> str | None:
    return _expr_to_source(node) if node is not None else None


def _expr_to_source(node: ast.AST | None) -> str:
    if node is None:
        return ""
    if hasattr(ast, "unparse"):
        return ast.unparse(node)
    return ""
