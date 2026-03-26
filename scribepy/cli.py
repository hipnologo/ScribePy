"""Command-line interface for ScribePy."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .parser import parse_file
from .renderer import render_html, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scribepy",
        description="Generate Markdown or HTML API documentation from a Python module.",
    )
    parser.add_argument("path", help="Path to the Python file to document.")
    parser.add_argument(
        "--format",
        choices=("markdown", "html"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Write output to a file instead of stdout.",
    )
    parser.add_argument(
        "--module-name",
        help="Override the module name used in the generated documentation.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    module = parse_file(args.path, module_name=args.module_name)
    rendered = render_html(module) if args.format == "html" else render_markdown(module)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
