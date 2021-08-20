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
trim_footnote_reference_space = True
nitpicky = True

rst_epilog = """\
.. _JSON: https://www.json.org/json-en.html
.. _YAML: https://yaml.org/
.. _TOML: https://toml.io/en/
.. _NestedText: https://nestedtext.org/en/latest/
.. _pytest: https://docs.pytest.org/en/stable/getting-started.html
.. _voluptuous: https://github.com/alecthomas/voluptuous
.. _schema: https://github.com/keleshev/schema

.. |PFF| replace:: *Parametrize From File*
.. |NS| replace:: :py:class:`Namespace <parametrize_from_file.Namespace>`
.. |NS_eval| replace:: :py:class:`Namespace.eval <parametrize_from_file.Namespace.eval>`
.. |NS_exec| replace:: :py:class:`Namespace.exec <parametrize_from_file.Namespace.exec>`
.. |NS_exec_lookup| replace:: :py:class:`Namespace.exec_and_lookup <parametrize_from_file.Namespace.exec_and_lookup>`
.. |NS_error| replace:: :py:class:`Namespace.error <parametrize_from_file.Namespace.error>`
.. |MagicMock| replace:: :py:class:`MagicMock <unittest.mock.MagicMock>`
"""

## Extensions

extensions = [
        'autoclasstoc',
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.viewcode',
        'sphinx.ext.intersphinx',
        'sphinx.ext.napoleon',
        'sphinx_toolbox.decorators',
        'sphinx_rtd_theme',
]
intersphinx_mapping = { #
        'python': ('https://docs.python.org/3', None),
        'pytest': ('https://docs.pytest.org/en/stable', None),
        'pandas': ('https://pandas.pydata.org/pandas-docs/stable', None),
}
autosummary_generate = True
autodoc_default_options = {
        'exclude-members': '__dict__,__weakref__,__module__',
}
autodoc_member_order = 'bysource'
autodoc_typehints = 'none'
html_theme = 'sphinx_rtd_theme'
pygments_style = 'sphinx'
napoleon_custom_sections = [
        "Details",
]

def ignore_dict_return_annotations(app, what, name, obj, options, signature, return_annotation):
    if 'Namespace' in name:
        return_annotation = None

    return signature, return_annotation

def setup(app):
    app.connect('autodoc-process-signature', ignore_dict_return_annotations)
