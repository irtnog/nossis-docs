# nossis-docs, serverless hosting for static, private web sites that
# works like GitHub Pages
#
# Copyright (C) 2024  Matthew X. Economou
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.

import sphinx_book_theme

from nossis_docs import __app_name__, __version__

project = __app_name__
author = "Matthew X. Economou"
copyright = "2024"
release = __version__
version = release

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_multiversion",
    "sphinx_pyscript",
    "sphinx_tippy",
    "sphinx_togglebutton",
    "sphinxext.opengraph",
    "sphinxext.rediraffe",
]
nitpicky = True
suppress_warnings = ["myst.strikethrough"]
locale_dirs = ["_locales"]
templates_path = ["_templates"]
exclude_patterns = [".*", "Thumbs.db", ".DS_Store"]

myst_enable_extensions = [
    "amsmath",
    "attrs_block",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_dmath_double_inline = True
myst_enable_checkboxes = True
myst_footnote_transition = True
myst_heading_anchors = 2

html_theme = "sphinx_book_theme"
html_theme_path = [sphinx_book_theme.get_html_theme_path()]
html_theme_options = {
    "home_page_in_toc": True,
    "repository_url": "https://github.com/irtnog/nossis-docs",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_repository_button": True,
    "use_edit_page_button": True,
    "use_issues_button": True,
}
html_favicon = "_static/favicon-32x32.png"
html_static_path = ["_static"]
html_sidebars = {
    "**": [
        "navbar-logo.html",
        "icon-links.html",
        "search-button-field.html",
        "sbt-sidebar-nav.html",
        "versioning.html",
    ]
}

# generate documentation for tagged releases only
smv_branch_whitelist = None
