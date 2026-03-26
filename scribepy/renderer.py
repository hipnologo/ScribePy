"""Render structured documentation as Markdown or HTML."""

from __future__ import annotations

from html import escape

from .models import ClassDoc, FunctionDoc, ModuleDoc


def render_markdown(module: ModuleDoc, include_source_path: bool = True) -> str:
    """Render a parsed module to Markdown."""
    lines: list[str] = [f"# {module.name}"]

    if include_source_path and module.path:
        lines.append("")
        lines.append(f"`Source:` `{module.path}`")

    if module.docstring:
        lines.append("")
        lines.append(module.docstring.strip())

    if module.imports:
        lines.append("")
        lines.append("## Imports")
        lines.append("")
        for imported in module.imports:
            lines.append(f"- `{imported}`")

    if module.functions:
        lines.append("")
        lines.append("## Functions")
        for function in module.functions:
            lines.extend(_render_function_markdown(function, level=3))

    if module.classes:
        lines.append("")
        lines.append("## Classes")
        for class_doc in module.classes:
            lines.extend(_render_class_markdown(class_doc))

    return "\n".join(lines).strip() + "\n"


def render_html(module: ModuleDoc, include_source_path: bool = True) -> str:
    """Render a parsed module to a self-contained HTML page."""
    body = _render_module_html(module, include_source_path=include_source_path)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(module.name)} API Documentation</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f5f1e8;
      --surface: rgba(255, 252, 245, 0.92);
      --ink: #1d1a16;
      --muted: #5c544b;
      --border: #d7c7b0;
      --accent: #0f766e;
      --accent-soft: #d9f3ef;
      --code-bg: #f0e7d8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top, rgba(15, 118, 110, 0.16), transparent 30%),
        linear-gradient(180deg, #f6f1e7 0%, #eee4d0 100%);
      line-height: 1.65;
    }}
    main {{
      max-width: 960px;
      margin: 0 auto;
      padding: 48px 20px 80px;
    }}
    article {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 24px;
      padding: 32px;
      box-shadow: 0 20px 50px rgba(61, 41, 20, 0.08);
      backdrop-filter: blur(10px);
    }}
    h1, h2, h3, h4 {{ line-height: 1.15; }}
    h1 {{
      font-size: clamp(2.5rem, 5vw, 4rem);
      margin-top: 0;
      letter-spacing: -0.04em;
    }}
    h2 {{
      margin-top: 2.5rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border);
    }}
    code {{
      background: var(--code-bg);
      padding: 0.15rem 0.35rem;
      border-radius: 6px;
      font-family: Consolas, "SFMono-Regular", monospace;
      font-size: 0.95em;
    }}
    pre {{
      background: #201a16;
      color: #f7f1e8;
      padding: 1rem 1.1rem;
      border-radius: 14px;
      overflow-x: auto;
    }}
    ul {{ padding-left: 1.2rem; }}
    blockquote {{
      margin-left: 0;
      padding-left: 1rem;
      border-left: 4px solid var(--accent);
      color: var(--muted);
    }}
    a {{ color: var(--accent); }}
  </style>
</head>
<body>
  <main>
    <article>
      {body}
    </article>
  </main>
</body>
</html>
"""


def _render_class_markdown(class_doc: ClassDoc) -> list[str]:
    lines = ["", f"### `{class_doc.name}`"]
    lines.append("")
    lines.append(f"`Class:` `{_class_signature(class_doc)}`")

    if class_doc.decorators:
        lines.append("")
        lines.append(f"`Decorators:` {', '.join(f'`@{item}`' for item in class_doc.decorators)}")

    if class_doc.docstring:
        lines.append("")
        lines.append(class_doc.docstring.strip())

    if class_doc.methods:
        lines.append("")
        lines.append("#### Methods")
        for method in class_doc.methods:
            lines.extend(_render_function_markdown(method, level=5))

    return lines


def _render_function_markdown(function: FunctionDoc, level: int) -> list[str]:
    heading = "#" * level
    lines = ["", f"{heading} `{function.name}`", "", f"```python\n{function.signature}\n```"]

    if function.decorators:
        lines.append("")
        lines.append(f"`Decorators:` {', '.join(f'`@{item}`' for item in function.decorators)}")

    if function.docstring:
        lines.append("")
        lines.append(function.docstring.strip())

    if function.parameters:
        parameter_rows = [
            "| Parameter | Type | Default | Kind |",
            "| --- | --- | --- | --- |",
        ]
        for parameter in function.parameters:
            if parameter.kind == "keyword_only_marker":
                continue
            parameter_rows.append(
                "| `{name}` | `{annotation}` | `{default}` | `{kind}` |".format(
                    name=parameter.name,
                    annotation=parameter.annotation or "",
                    default=parameter.default or "",
                    kind=parameter.kind,
                )
            )
        if len(parameter_rows) > 2:
            lines.append("")
            lines.append("Parameters:")
            lines.extend(parameter_rows)

    return lines


def _class_signature(class_doc: ClassDoc) -> str:
    if not class_doc.bases:
        return class_doc.name
    return f"{class_doc.name}({', '.join(class_doc.bases)})"


def _render_module_html(module: ModuleDoc, include_source_path: bool) -> str:
    parts = [f"<h1>{escape(module.name)}</h1>"]

    if include_source_path and module.path:
        parts.append(f"<p><strong>Source:</strong> <code>{escape(module.path)}</code></p>")

    if module.docstring:
        parts.append(f"<p>{escape(module.docstring.strip())}</p>")

    if module.imports:
        parts.append("<h2>Imports</h2><ul>")
        parts.extend(f"<li><code>{escape(imported)}</code></li>" for imported in module.imports)
        parts.append("</ul>")

    if module.functions:
        parts.append("<h2>Functions</h2>")
        parts.extend(_render_function_html(function, heading="h3") for function in module.functions)

    if module.classes:
        parts.append("<h2>Classes</h2>")
        parts.extend(_render_class_html(class_doc) for class_doc in module.classes)

    return "".join(parts)


def _render_class_html(class_doc: ClassDoc) -> str:
    parts = [f"<section><h3><code>{escape(class_doc.name)}</code></h3>"]
    parts.append(f"<p><strong>Class:</strong> <code>{escape(_class_signature(class_doc))}</code></p>")

    if class_doc.decorators:
        decorators = ", ".join(f"<code>@{escape(item)}</code>" for item in class_doc.decorators)
        parts.append(f"<p><strong>Decorators:</strong> {decorators}</p>")

    if class_doc.docstring:
        parts.append(f"<p>{escape(class_doc.docstring.strip())}</p>")

    if class_doc.methods:
        parts.append("<h4>Methods</h4>")
        parts.extend(_render_function_html(method, heading="h5") for method in class_doc.methods)

    parts.append("</section>")
    return "".join(parts)


def _render_function_html(function: FunctionDoc, heading: str) -> str:
    parts = [f"<section><{heading}><code>{escape(function.name)}</code></{heading}>"]
    parts.append(f"<pre><code>{escape(function.signature)}</code></pre>")

    if function.decorators:
        decorators = ", ".join(f"<code>@{escape(item)}</code>" for item in function.decorators)
        parts.append(f"<p><strong>Decorators:</strong> {decorators}</p>")

    if function.docstring:
        parts.append(f"<p>{escape(function.docstring.strip())}</p>")

    table = _render_parameter_table_html(function)
    if table:
        parts.append(table)

    parts.append("</section>")
    return "".join(parts)


def _render_parameter_table_html(function: FunctionDoc) -> str:
    rows = []
    for parameter in function.parameters:
        if parameter.kind == "keyword_only_marker":
            continue
        rows.append(
            "<tr>"
            f"<td><code>{escape(parameter.name)}</code></td>"
            f"<td><code>{escape(parameter.annotation or '')}</code></td>"
            f"<td><code>{escape(parameter.default or '')}</code></td>"
            f"<td><code>{escape(parameter.kind)}</code></td>"
            "</tr>"
        )

    if not rows:
        return ""

    return (
        "<table>"
        "<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Kind</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
    )
