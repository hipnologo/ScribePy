from setuptools import setup, find_packages

setup(
    name='ScribePy',
    version='0.1.0',
    description='Python library for generating documentation',
    url='https://github.com/hipnologo/ScribePy',
    author='Fabio Carvalho',
    author_email='email@fabioac.com',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
