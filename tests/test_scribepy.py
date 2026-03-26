from __future__ import annotations

from pathlib import Path
import textwrap
import uuid

from scribepy import ScribePy, generate_html_docs, generate_markdown_docs, parse_source
from scribepy.cli import main


SOURCE = textwrap.dedent(
    '''
    """Utilities used across the project."""

    import os
    from pathlib import Path

    def add(x: int, y: int = 1) -> int:
        """Add two numbers together."""
        return x + y

    class Greeter:
        """Simple greeting helper."""

        def hello(self, name: str) -> str:
            """Return a greeting."""
            return f"Hello {name}"
    '''
)


SCRATCH_ROOT = Path("tests_runtime")


def _scratch_dir() -> Path:
    path = SCRATCH_ROOT / uuid.uuid4().hex
    path.mkdir(parents=True, exist_ok=False)
    return path


def test_parse_source_extracts_structure():
    module = parse_source(SOURCE, module_name="demo")

    assert module.name == "demo"
    assert module.docstring == "Utilities used across the project."
    assert "os" in module.imports
    assert "pathlib.Path" in module.imports
    assert module.functions[0].signature == "add(x: int, y: int = 1) -> int"
    assert module.classes[0].methods[0].signature == "hello(self, name: str) -> str"


def test_generate_markdown_docs_contains_api_sections():
    docs = generate_markdown_docs(SOURCE, module_name="demo")

    assert "# demo" in docs
    assert "## Functions" in docs
    assert "Add two numbers together." in docs
    assert "| `x` | `int` | `` | `positional_or_keyword` |" in docs
    assert "### `Greeter`" in docs


def test_generate_html_docs_returns_standalone_page():
    docs = generate_html_docs(SOURCE, module_name="demo")

    assert docs.startswith("<!DOCTYPE html>")
    assert "<title>demo API Documentation</title>" in docs
    assert "Simple greeting helper." in docs


def test_file_backed_scribepy_includes_source_path():
    temp_dir = _scratch_dir()
    file_path = temp_dir / "helpers.py"
    file_path.write_text(SOURCE, encoding="utf-8")

    docs = ScribePy(path=str(file_path)).generate_markdown_docs()

    assert str(file_path) in docs
    assert "# helpers" in docs


def test_cli_writes_output_file():
    temp_dir = _scratch_dir()
    source_file = temp_dir / "helpers.py"
    output_file = temp_dir / "helpers.md"
    source_file.write_text(SOURCE, encoding="utf-8")

    exit_code = main([str(source_file), "--output", str(output_file)])

    assert exit_code == 0
    written = output_file.read_text(encoding="utf-8")
    assert "# helpers" in written
    assert "## Classes" in written


def test_markdown_output_escapes_html_in_untrusted_content():
    source = textwrap.dedent(
        '''
        """<script>alert("xss")</script>"""

        def demo(value: str = "<img src=x onerror=alert(1)>") -> str:
            """`code` <b>bold</b>"""
            return value
        '''
    )

    docs = generate_markdown_docs(source, module_name='unsafe<script>alert(1)</script>')

    assert "<script>" not in docs
    assert "<img" not in docs
    assert "<b>" not in docs
    assert "&lt;script&gt;alert(" in docs
    assert "&lt;img src=x onerror=alert(1)&gt;" in docs
    assert "&lt;b&gt;bold&lt;/b&gt;" in docs
