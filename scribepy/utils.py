# pyscribe/utils.py

def strip_docstrings(source):
    """
    Remove docstrings from Python source code.
    """
    in_docstring = False
    lines = source.split('\n')
    new_lines = []
    for line in lines:
        if in_docstring:
            if '"""' in line:
                in_docstring = False
        elif '"""' in line:
            in_docstring = True
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)
