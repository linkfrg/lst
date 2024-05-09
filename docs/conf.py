import os
import sys

sys.path.insert(0, os.path.abspath(".."))
from lst.widgets import Widget

project = "lst"
copyright = "2024, linkfrg"
author = "linkfrg"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_title = "LST Wiki"


def get_widget_template(name):
    return f"""{name}
{'-'*len(name)}

.. autoclass:: lst.widgets.Widget.{name}
"""


os.makedirs("widgets/generated", exist_ok=True)

for name in Widget.__dict__:
    if not name.startswith("__"):
        with open(f"widgets/generated/{name}.rst", "w") as file:
            file.write(get_widget_template(name))
