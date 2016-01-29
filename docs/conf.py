# -*- coding: utf-8 -*-

import sys
import os
from os.path import abspath

sys.path.insert(0, abspath('..'))
import kaneda
sys.path.pop(0)

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.doctest',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'kaneda'
copyright = u'2016, APSL'

version = '0.1'
release = '0.1'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']
htmlhelp_basename = 'kanedadoc'
