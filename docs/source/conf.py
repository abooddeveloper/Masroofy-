# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# docs/source/conf.py
import os
import sys
import django

# Add Django project to Python path
# This allows Sphinx to find your Django modules
sys.path.insert(0, os.path.abspath('../..'))

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'softwareProject.settings'

# Initialize Django
django.setup()



project = 'Masroofy'
copyright = '2026, Abdelrahman Mohamed Abdelrahman'
author = 'Abdelrahman Mohamed Abdelrahman'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',      # Auto-document from docstrings
    'sphinx.ext.napoleon',     # Support Google-style docstrings
    'sphinx.ext.viewcode',     # Add links to source code
    'sphinx.ext.todo',         # Support todo items
    'sphinx_autodoc_typehints', # Show type hints
]

# Add any paths that contain templates here
templates_path = ['_templates']

# List of patterns to exclude
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Napoleon settings (for Google-style docstrings) -------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

# -- Autodoc settings -------------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
}