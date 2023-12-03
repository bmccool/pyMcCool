# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
from importlib.metadata import version as get_version

# Add the project to the path so that autodoc can find it
sys.path.insert(0, os.path.abspath(os.path.join('..', 'src', 'pymccool')))

project: str = 'pymccool'
copyright: str  = '2023, Brendon McCool'
author: str = 'Brendon McCool'
release: str = get_version("pymccool")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.doctest",
    "sphinx_rtd_theme",
    "sphinx.ext.napoleon",
]

# Disable the doctests of the full package because those would require the explicit specification
# of imports. The doctests inside the source code are covered by pytest, using the --doctest-modules
# configuration option.
doctest_test_doctest_blocks = ""

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Mapping for external packages
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "opentelemetry": ("https://opentelemetry-python.readthedocs.io/en/stable/", None),
}

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
