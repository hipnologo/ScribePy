# tests/test_scribepy.py

from scribepy import ScribePy

def test_generate_html_docs():
    source_code = '''
    def add(x, y):
        """
        Add two numbers together.
        """
        return x + y
    '''
    p = ScribePy(source_code)
    docs = p.generate_html_docs()
    assert isinstance(docs, str)
    assert 'Add two numbers together' in docs
