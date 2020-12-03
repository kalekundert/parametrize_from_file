import sys, os
import parametrize_from_file

## General

project = 'Parametrize From File'
copyright = '2020, Kale Kundert'
version = parametrize_from_file.__version__
release = parametrize_from_file.__version__

master_doc = 'index'
source_suffix = '.rst'
templates_path = ['_templates']
exclude_patterns = ['_build']
html_static_path = ['_static']
default_role = 'any'

## Extensions

extensions = [
        'autoclasstoc',
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.viewcode',
        'sphinx.ext.intersphinx',
        'sphinx.ext.napoleon',
        'sphinx_rtd_theme',
]
intersphinx_mapping = { #
        'python': ('https://docs.python.org/3', None),
        'pytest': ('https://docs.pytest.org/en/stable', None),
}
autosummary_generate = True
autodoc_default_options = {
        'exclude-members': '__dict__,__weakref__,__module__',
}
html_theme = 'sphinx_rtd_theme'
pygments_style = 'sphinx'

