# ScribePy

ScribePy is a Python library for generating documentation from Python source code.

[![License: Apache License 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Forks](https://img.shields.io/github/forks/hipnologo/ScribePy)](https://github.com/hipnologo/ScribePy/network/members)
[![Stars](https://img.shields.io/github/stars/hipnologo/ScribePy)](https://github.com/hipnologo/ScribePy/stargazers)
[![Issues](https://img.shields.io/github/issues/hipnologo/ScribePy)](https://github.com/hipnologo/ScribePy/issues)

## Installation

You can install ScribePy using pip:

``` bash
pip install ScribePy
```

## Usage

To use ScribePy, you first need to create an instance of the `ScribePy` class:

```python
from ScribePy import ScribePy

source_code = '''
def add(x, y):
    """
    Add two numbers together.
    """
    return x + y
'''

p = ScribePy(source_code)
```

Once you have an instance of the ScribePy class, you can generate HTML documentation using the generate_html_docs method:

```python
docs = p.generate_html_docs()
print(docs)
```

This will generate HTML documentation for the provided source code.

### Documentation
For more information, see the [official documentation](https://pypi.org/project/ScribePy/) or the [GitHub repository](https://pypi.org/project/ScribePy/).

### Contributing
Contributions are welcome! To contribute to ScribePy, please follow these guidelines:

* Fork the repository.
* Create a new branch for your changes.
* Make your changes and write tests for them.
* Run the tests using pytest to make sure they pass.
* Submit a pull request.

For more information on how to contribute, please see the [contributing guidelines](https://github.com/hipnologo/ScribePy/blob/main/CONTRIBUTING.md) in the GitHub repository.

### Support
If you have any questions or need help using ScribePy, please post a question or [open an issue](https://github.com/hipnologo/ScribePy/issues) on GitHub.