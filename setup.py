from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ScribePy',
    version='0.2.0',
    description='AST-backed Python API documentation generator with Markdown and HTML output',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hipnologo/ScribePy',
    author='Fabio Carvalho',
    author_email='hipnologo@gmail.com',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='documentation api ast cli',
    entry_points={
        'console_scripts': [
            'scribepy=scribepy.cli:main',
        ],
    },
)
