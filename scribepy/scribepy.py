# scribepy/scribepy.py

from markdown import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

def generate_html_docs(source_code):
    """
    Generate HTML documentation from Python source code.
    """
    lexer = get_lexer_by_name('python', stripall=True)
    formatter = html.HtmlFormatter()
    highlighted_code = highlight(source_code, lexer, formatter)
    markdown_code = markdown(highlighted_code, extensions=['markdown.extensions.tables'])
    return markdown_code

class scribepy:
    """
    A class for generating documentation from Python source code.
    """
    def __init__(self, source_code):
        self.source_code = source_code

    def generate_html_docs(self):
        """
        Generate HTML documentation from the source code.
        """
        return generate_html_docs(self.source_code)
