# ScribePy

AST-backed Python API documentation generator with Markdown and HTML output.

ScribePy parses Python modules, builds a structured model of classes and functions, and renders readable docs for READMEs, docs sites, CI artifacts, and internal references.

## Table of Contents

- [ScribePy](#scribepy)
  - [Table of Contents](#table-of-contents)
  - [Why ScribePy](#why-scribepy)
  - [Features](#features)
  - [Quick Start](#quick-start)
  - [Installation](#installation)
  - [CLI Usage](#cli-usage)
  - [Python API](#python-api)
    - [High-Level Wrapper](#high-level-wrapper)
    - [Functional API](#functional-api)
    - [Source String Helpers](#source-string-helpers)
  - [Development](#development)
  - [Contributing](#contributing)
  - [Roadmap](#roadmap)
  - [License](#license)

## Why ScribePy

- Zero runtime introspection: built from source code using Python AST
- Predictable output: ideal for CI pipelines and reproducible docs
- Works as CLI and library: use it in local scripts or automated tooling
- Two output formats: Markdown for docs repos and standalone HTML for sharing

## Features

- Parse Python modules from file paths or in-memory source strings
- Extract module docstrings, imports, classes, methods, functions, decorators, and signatures
- Render Markdown API docs
- Render standalone HTML API docs
- Override module name when needed (CLI or API)

## Quick Start

Install:

```bash
pip install ScribePy
```

Generate Markdown to stdout:

```bash
scribepy path/to/module.py
```

Generate HTML and write to a file:

```bash
scribepy path/to/module.py --format html --output docs/module.html
```

## Installation

From PyPI:

```bash
pip install ScribePy
```

From source:

```bash
git clone https://github.com/hipnologo/ScribePy.git
cd ScribePy
pip install -e .
```

## CLI Usage

```bash
scribepy <path> [--format markdown|html] [--output FILE] [--module-name NAME]
```

Examples:

```bash
# Markdown to stdout
scribepy package/example.py

# HTML to file
scribepy package/example.py --format html --output docs/example.html

# Override detected module name
scribepy package/example.py --module-name my_public_api
```

Arguments:

- `path`: path to the Python file to document
- `--format`: output format (`markdown` or `html`), default is `markdown`
- `--output`, `-o`: write output to file instead of stdout
- `--module-name`: override module name used in generated docs

## Python API

### High-Level Wrapper

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

### Functional API

```python
from scribepy import parse_file, render_markdown

module = parse_file("package/example.py")
docs = render_markdown(module)
```

### Source String Helpers

```python
from scribepy import generate_markdown_docs, generate_html_docs

source = "def ping() -> str:\n    return 'pong'\n"
md = generate_markdown_docs(source, module_name="health")
html = generate_html_docs(source, module_name="health")
```

## Development

Set up a local dev environment:

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
pip install -e .
pip install pytest build
```

Run tests:

```bash
pytest
```

Build distribution artifacts:

```bash
python -m build
```

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Add or update tests for your changes
4. Open a pull request with a clear description

For bug reports and feature requests, use GitHub Issues.

## Roadmap

- Recursive package documentation
- Optional filtering for private members
- Docstring style awareness for richer parameter descriptions
- Static site output for multi-module projects

## License

Apache License 2.0. See `LICENSE` for details.
