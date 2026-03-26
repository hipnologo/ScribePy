"""High-level compatibility facade for generating Python API documentation."""

from __future__ import annotations

from pathlib import Path

from .parser import parse_file, parse_source
from .renderer import render_html, render_markdown


def generate_markdown_docs(source_code: str, module_name: str = "module") -> str:
    """Generate Markdown API documentation from Python source code."""
    return render_markdown(parse_source(source_code, module_name=module_name), include_source_path=False)


def generate_html_docs(source_code: str, module_name: str = "module") -> str:
    """Generate HTML API documentation from Python source code."""
    return render_html(parse_source(source_code, module_name=module_name), include_source_path=False)


class ScribePy:
    """Convenience wrapper for documenting Python source code or files."""

    def __init__(self, source_code: str | None = None, *, path: str | None = None, module_name: str | None = None):
        if source_code is None and path is None:
            raise ValueError("Provide either source_code or path.")
        self.source_code = source_code
        self.path = path
        self.module_name = module_name

    def parse(self):
        """Return the structured documentation model."""
        if self.path is not None:
            file_path = Path(self.path)
            return parse_file(file_path, module_name=self.module_name or file_path.stem)
        return parse_source(self.source_code or "", module_name=self.module_name or "module")

    def generate_markdown_docs(self) -> str:
        """Generate Markdown documentation."""
        return render_markdown(self.parse(), include_source_path=self.path is not None)

    def generate_html_docs(self) -> str:
        """Generate HTML documentation."""
        return render_html(self.parse(), include_source_path=self.path is not None)
