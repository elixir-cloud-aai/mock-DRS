from setuptools import (setup, find_packages)

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='mock-DRS',
    version='0.1.0',
    author='Elixir Europe',
    author_email='vani11537@one.ducic.ac.in',
    description='Flask- and MongoDB-powered GA4GH DRS server',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    url='https://github.com/elixir-europe/mock-DRS.git',
    packages=find_packages(),
    keywords=(
        'ga4gh wes workflow elixir rest restful api app server openapi '
        'swagger mongodb python flask'
    ),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['connexion', 'Flask-Cors', 'Flask-PyMongo'],
)
