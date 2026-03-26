# ScribePy

ScribePy turns Python modules into readable API documentation.

It parses source with the Python AST, extracts module/class/function structure, preserves signatures, and renders the result as Markdown or a self-contained HTML page. It is useful for quick internal docs, generated API references, CI artifacts, and package overviews.

## What It Does

- Parses Python modules from source strings or files
- Extracts module docstrings, imports, classes, methods, functions, decorators, and signatures
- Renders clean Markdown for docs sites and READMEs
- Renders styled standalone HTML for sharing or publishing
- Ships with a CLI for generating docs directly from a `.py` file

## Installation

```bash
pip install ScribePy
```

## CLI

Generate Markdown to stdout:

```bash
scribepy path/to/module.py
```

Generate HTML to a file:

```bash
scribepy path/to/module.py --format html --output docs/module.html
```

## Library Usage

Generate docs from a source string:

```python
from scribepy import ScribePy

source_code = '''
"""Utilities for math helpers."""

def add(x: int, y: int) -> int:
    """Add two integers."""
    return x + y
'''

scribe = ScribePy(source_code=source_code, module_name="math_helpers")

markdown_docs = scribe.generate_markdown_docs()
html_docs = scribe.generate_html_docs()
```

Parse a file and render it manually:

```python
from scribepy import parse_file, render_markdown

module = parse_file("package/example.py")
docs = render_markdown(module)
```

## Example Output

Markdown output includes:

- Module title and source path
- Module docstring
- Import inventory
- Function signatures and parameter tables
- Class sections with method breakdowns

## Development

Run tests:

```bash
pytest
```

Build a distribution:

```bash
python -m build
```

## Roadmap

- Recursive package documentation
- Optional filtering for private members
- Docstring style awareness for richer parameter descriptions
- Static site output for multi-module projects
