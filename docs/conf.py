# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _get_version

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "logging-extras"
copyright = "2021, Zobayer Hasan"
author = "Zobayer Hasan"

# The full version, including alpha/beta/rc tags. Derived from the installed
# package metadata (setuptools_scm), so it tracks the git tag automatically.
try:
    release = _get_version("logging-extras")
except PackageNotFoundError:  # package not installed (e.g. building without an install)
    release = "0.0.0"
source_suffix = ".rst"
master_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["build", "venv"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# pip install sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Autodoc defaults
autodoc_default_options = {
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": False,
    "exclude-members": "__weakref__,__dict__",
}
