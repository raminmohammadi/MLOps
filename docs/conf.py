import os
import sys

# Add your project directory to the system path to make Sphinx find your modules
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'My Project Name'
author = 'Your Name'

# The full version, including alpha/beta/rc tags
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',  # Generate documentation from docstrings
    'sphinx.ext.napoleon',  # Support NumPy-style docstrings
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'  # Use the Read the Docs theme

# Output file base name for HTML help builder.
htmlhelp_basename = 'MyProjectDoc'

# -- Options for autodoc extension -------------------------------------------

# Include both class and init docstrings from classes and __init__ methods
autoclass_content = 'both'

# -- Options for napoleon extension -----------------------------------------

# Parse Google-style docstrings
napoleon_google_docstring = True

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for HTML output -------------------------------------------------

html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',  # Google Analytics ID
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': 'white',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 3,
    'includehidden': True,
    'titles_only': False,
}

# -- Other custom settings ---------------------------------------------------

# Add any additional configuration settings specific to your project here.

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# -- Extension configuration -------------------------------------------------

