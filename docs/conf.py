# Nossis Docs, serverless hosting for static, private web sites
#
# Copyright (C) 2024-2025  Matthew X. Economou
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

"""Configure Sphinx.

Some neat tricks not referenced elsewhere:

- <inv:myst:std:doc#syntax/cross-referencing Add
  cross-references to source code and third-party documentation using
  either Markdown links or Intersphinx references.>

- <inv:sphinx:std:doc#usage/extensions/autodoc Document module data
  members or class attributes by using doc comments (`#: ` instead of
  `# `) immediately before a variable/attribute definition or by
  adding a docstring immediately after it.>

"""

import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path

import sphinx_book_theme

# Enable builds from outside the docs directory.
_srcpath = (Path(__file__).parent / ".." / "src").absolute()
sys.path.insert(0, str(_srcpath))

# Purge old imports in an attempt to hack around sphinx-multiversion's
# global environment.
_removals = [_mod for _mod in sys.modules if "nossis_docs" in _mod]
for _mod in _removals:
    del sys.modules[_mod]

# Configure Sphinx from dynamically loaded project metadata.
_metadata = SourceFileLoader(
    "nossis_docs", str(_srcpath / "nossis_docs" / "__init__.py")
).load_module()

project = _metadata.__app_name__
"""The project name."""

release = _metadata.__version__
"""The full version number, including the patch level (X.Y.Z)."""

version = ".".join(_metadata.__version__.split(".")[0:2])
"""The short version number (X.Y)."""

author = "Matthew X. Economou"
"""Credits for this version."""

copyright = "2024-2025"
"""The years over which the work was done."""

extensions = [
    "autodoc2",
    "myst_parser",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_multiversion",
    "sphinx_pyscript",
    "sphinx_tippy",
    "sphinx_togglebutton",
    "sphinxcontrib.cairosvgconverter",
    "sphinxext.opengraph",
    "sphinxext.rediraffe",
]
"""This documentation uses several Sphinx extensions.

{glossary}
<inv:autodoc2:std:doc#index autodoc2>
: Generate API documentation automatically.

{glossary}
<inv:myst:std:doc#index myst-parser>
: Render Markdown in documentation and docstrings.

{glossary}
<inv:sphinx:std:doc#usage/extensions/githubpages sphinx.ext.githubpages>
: Publish HTML documentation in GitHub Pages.

{glossary}
<inv:sphinx:std:doc#usage/extensions/intersphinx sphinx.ext.intersphinx>
: Link to other projects' documentation.

{glossary}
<inv:sphinx:std:doc#usage/extensions/viewcode sphinx.ext.viewcode>
: Link to highlighted source code.

{glossary}
<inv:copybutton:std:doc#index sphinx-copybutton>
: Add a `copy` button to code blocks.

{glossary}
<inv:sphinx-design:std:doc#index sphinx-design>
: Provide screen-size responsive web components.

{glossary}
<inv:smv:std:doc#index sphinx-multiversion>
: Build versioned documentation.

{glossary}
<inv:sphinx-pyscript:std:doc#index sphinx-pyscript>
: Use PyScript in built documentation.

{glossary}
<inv:sphinx-tippy:std:doc#index sphinx-tippy>
: Add rich hints (tooltips) to built documentation.

{glossary}
<inv:togglebutton:std:doc#index sphinx-togglebutton>
: Add collapsable admonitions (notes, warnings, etc.) to built
  documentation.

{glossary}
[sphinxcontrib.cairosvgconverter](https://pypi.org/project/sphinxcontrib-svg2pdfconverter/)
: Convert SVG diagrams to PDF for output formats that do not support
  SVG natively.

{glossary}
<inv:opengraph:std:doc#index sphinxext-opengraph>
: Turn web pages into Open Graph objects.

{glossary}
<inv:rediraffe:std:doc#index sphinxext-rediraffe>
: Fix broken internal links due to deleted/renamed pages.

"""

intersphinx_mapping = {
    "black": ("https://black.readthedocs.io/en/stable/", None),
    "myst": ("https://myst-parser.readthedocs.io/en/latest/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "book-theme": ("https://sphinx-book-theme.readthedocs.io/en/stable/", None),
    "pydata-theme": ("https://pydata-sphinx-theme.readthedocs.io/en/latest/", None),
    "copybutton": ("https://sphinx-copybutton.readthedocs.io/en/latest/", None),
    "smv": ("https://sphinx-contrib.github.io/multiversion/main/", None),
    "sphinx-design": ("https://sphinx-design.readthedocs.io/en/latest/", None),
    "sphinx-pyscript": ("https://sphinx-pyscript.readthedocs.io/en/latest/", None),
    "sphinx-tippy": ("https://sphinx-tippy.readthedocs.io/en/latest/", None),
    "togglebutton": ("https://sphinx-togglebutton.readthedocs.io/en/latest/", None),
    "opengraph": ("https://sphinxext-opengraph.readthedocs.io/en/latest/", None),
    "rediraffe": ("https://sphinxext-rediraffe.readthedocs.io/en/latest/", None),
    "sphobjinv": ("https://sphobjinv.readthedocs.io/en/latest/", None),
}
"""Cross-reference other Sphinx documentation project.s

Use the <inv:sphobjinv:std:doc#cli/suggest `sphobjinv suggest`>
command to find intersphinx references using the documentation URL,
e.g., `sphobjinv suggest -u
https://sphobjinv.readthedocs.io/en/latest/cli/suggest.html suggest`.

"""

nitpicky = True

suppress_warnings = ["myst.strikethrough"]

locale_dirs = ["_locales"]

templates_path = ["_templates"]
"""These directories contain documentation templates.

Paths are relative to this file's parent directory.

"""

exclude_patterns = [".*", "Thumbs.db", ".DS_Store"]
"""Ignore these files/folders when sourcing content."""

autodoc2_packages = [
    {
        "module": "nossis_docs",
        "path": str(_srcpath),
    },
]
"""Search these locations for code to document."""

autodoc2_render_plugin = "myst"
"""Render docstrings using <inv:myst:std:doc#index MyST Markdown>."""

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
"""Enable all MyST parser extensions.

For more information, refer to
<inv:myst-parser:std:label#syntax/extensions the documentation>.

"""

myst_dmath_double_inline = True

myst_enable_checkboxes = True

myst_footnote_transition = True

myst_heading_anchors = 2

html_theme = "sphinx_book_theme"
"""Use the Sphinx Book Theme template for web content."""

html_theme_path = [sphinx_book_theme.get_html_theme_path()]

html_theme_options = {
    "home_page_in_toc": True,
    "repository_url": "https://github.com/irtnog/nossis-docs",
    "path_to_docs": "docs",
    "use_edit_page_button": True,
    "use_repository_button": True,
    "use_issues_button": True,
    "use_fullscreen_button": True,
}
"""Configure web content generation.

{glossary}
<inv:book-theme:std:doc#sections/sidebar-primary home_page_in_toc>
: Add the home page to the table of contents.

{glossary}
<inv:book-theme:std:doc#components/source-files repository_url,
path_to_docs, use_edit_page_button, use_repository_button,
use_issues_button>
: Link to doc sources and include buttons for suggesting edits or
  creating new issues.

{glossary}
<inv:book-theme:std:doc#reference use_fullscreen_button>
: Add a button to show the site full screen.

"""

html_favicon = "_static/favicon-32x32.png"

html_static_path = ["_static"]

html_sidebars = {
    "**": [
        "navbar-logo.html",
        "icon-links.html",
        "search-button-field.html",
        "sbt-sidebar-nav.html",
        "versions.html",
    ]
}

smv_branch_whitelist = r"^(?!(gh-pages$|main$|master$|releases?(/.*)?$)).*$"
"""Generate documentation for feature branches."""

smv_tag_whitelist = r"^v\d+\.\d+\.\d+$"
"""Generate documentation for tagged releases."""

smv_released_pattern = r".*tags.*"

smv_remote_whitelist = r"^origin$"

smv_prefer_remote_refs = True
