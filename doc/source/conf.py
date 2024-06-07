#
# PyWavelets documentation build configuration file, created by
# sphinx-quickstart on Sun Mar 14 10:46:18 2010.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import datetime
import importlib.metadata
import os
from pathlib import Path

import jinja2.filters
import numpy as np

# FIXME: doctests need the str/repr formatting used in Numpy < 1.14.
# Should this be removed or updated?
try:
    np.set_printoptions(legacy='1.13')
except TypeError:
    pass

from sphinx.application import Sphinx

HERE = Path(__file__).parent


def preprocess_notebooks(app: Sphinx, *args, **kwargs):
    """Preprocess Markdown notebooks to convert them to IPyNB format
    and remove cells tagged with 'ignore-when-converting' metadata."""

    import jupytext
    import nbformat

    print("Converting Markdown files to IPyNB...")
    for path in (HERE / "regression").glob("*.md"):
        nb = jupytext.read(str(path))
        nb.cells = [cell for cell in nb.cells if "true" not in cell.metadata.get("ignore-when-converting", [])]
        ipynb_path = path.with_suffix(".ipynb")
        with open(ipynb_path, "w") as f:
            nbformat.write(nb, f)
            print(f"Converted {path} to {ipynb_path}")


    for path in (HERE / "regression").glob("*.ipynb"):
        with open(path) as f:
            nb = nbformat.read(f, as_version=4)
            nb.cells = [cell for cell in nb.cells if "true" not in cell.metadata.get("ignore-when-converting", [])]

        with open(path, "w") as f:
            nbformat.write(nb, f)
            print(f"Cleaned up {path}")


def setup(app):
    app.connect("builder-inited", preprocess_notebooks)

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.append(os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'jupyterlite_sphinx',
    'matplotlib.sphinxext.plot_directive',
    'myst_nb',
    'numpydoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx_togglebutton',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'myst-nb',
    'ipynb': None,  # do not parse IPyNB files
}

# The encoding of source files.
source_encoding = 'utf-8'

# General information about the project.
project = 'PyWavelets'
copyright = f'2006-{datetime.date.today().year}, The PyWavelets Developers'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.

version = importlib.metadata.version('pywavelets')
release = version

print(f"PyWavelets (VERSION {version})")

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
unused_docs = ['substitutions', ]

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['pywt.']

# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'pydata_sphinx_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further. For a list of options available for each theme, see the documentation
# at https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/index.html
html_theme_options = {
"navbar_start": ["navbar-logo"],
"navbar_center": ["navbar-nav"],
"navbar_end": ["navbar-icon-links", "theme-switcher"],
"navbar_persistent": ["search-button"],
"primary_sidebar_end": ["indices.html", "sidebar-ethical-ads.html"],
"navigation_with_keys": False,
"show_nav_level": 2,
"navigation_depth": 2,
"show_toc_level": 2,
"use_edit_page_button": True,
"github_url": "https://github.com/PyWavelets/pywt",
"secondary_sidebar_items": {
    "**": ["page-toc", "sourcelink", "edit-this-page"],
    "index": ["page-toc"],
},
"show_prev_next": True,
"footer_start": ["copyright", "sphinx-version"],
"footer_end": ["theme-version"],
"pygment_light_style": "a11y-high-contrast-light",
"pygment_dark_style": "a11y-high-contrast-dark",
"icon_links": [
        {
            "name": "Discussion group on Google Groups",
            "url": "https://groups.google.com/group/pywavelets",
            # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "icon": "fa-regular fa-comments",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        },
        {
            "name": "Explore PyWavelets",
            "url": "http://wavelets.pybytes.com/",
            "icon": "fa-solid fa-wave-square",
            "type": "fontawesome",
        }
   ],
"icon_links_label": "Quick Links",
}

# Contexts to extract GitHub links for edit buttons and theme switcher
html_context = {
    "github_url": "https://github.com", # or your GitHub Enterprise site
    "github_user": "PyWavelets",
    "github_repo": "pywt",
    "github_version": "main",
    "doc_path": "doc/source",
    "default_mode": "light",
}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = 'PyWavelets Documentation'

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# CSS files to include in the build. The file path should be relative to the
# _static directory.
html_css_files = [
    "pywavelets.css",
]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}
html_sidebars = {
    "**": ["sidebar-nav-bs",]
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_use_modindex = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
html_use_opensearch = 'http://pywavelets.readthedocs.org'

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'PyWaveletsdoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
# latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
# latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'PyWavelets.tex', 'PyWavelets Documentation',
   'The PyWavelets Developers', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ''

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_use_modindex = True

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    'substitutions.rst',
    'regression/*.ipynb'  # exclude IPyNB files from the build
]

# numpydoc_show_class_members = False
numpydoc_class_members_toctree = False

# plot_directive options
plot_include_source = True
plot_formats = [('png', 96), 'pdf']
plot_html_show_formats = False
plot_html_show_source_link = False

# -- Options for intersphinx extension ---------------------------------------

# Intersphinx to get NumPy, SciPy, and other targets
intersphinx_mapping = {
    'numpy': ('https://numpy.org/devdocs', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    }

# -- Options for JupyterLite -------------------------------------------------

global_enable_try_examples = True
try_examples_global_button_text = "Try it in your browser!"
try_examples_global_warning_text = (
"""These interactive examples with JupyterLite are experimental and
may not always work as expected. The execution of cells containing import
statements can result in high bandwidth usage and may take a long time to
load. They may not be in sync with the latest PyWavelets release.

Shall you encounter any issues, please feel free to report them on the
[PyWavelets issue tracker](https://github.com/PyWavelets/pywt/issues)."""
)

# -- Options for MyST-NB and Markdown-based content --------------------------

os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

nb_execution_mode = 'auto'
nb_execution_timeout = 60
nb_execution_allow_errors = False

nb_render_markdown_format = "myst"
render_markdown_format = "myst"

nb_remove_code_source = False
nb_remove_code_outputs = False

myst_enable_extensions = [
    'amsmath',
    'colon_fence',
    'dollarmath',
]

# nb_execution_allow_errors = True
# nb_execution_show_tb = True
