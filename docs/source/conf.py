import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "judobase"
copyright = "2025, ddzgoev"
author = "ddzgoev"

from judobase import __version__

release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.autosummary",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "en"

html_baseurl = "https://anotherjudorating.github.io/judobase/"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_context = {
    "display_github": True,
    "github_user": "anotherjudorating",
    "github_repo": "judobase",
    "github_version": "master",
    "conf_py_path": "/docs/source/",
}
html_logo = "_static/ijf-logo.png"

autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = False
autosummary_generate = True
