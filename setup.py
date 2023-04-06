from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ScribePy',
    version='0.1.2',
    description='Python library for generating documentation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hipnologo/ScribePy',
    author='Fabio Carvalho',
    author_email='hipnologo@gmail.com',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='documentation',
    install_requires=[
        'markdown>=3.3.3',
        'Pygments>=2.7.4',
    ],
)
