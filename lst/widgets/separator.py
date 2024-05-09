from gi.repository import Gtk
from lst.base_widget import BaseWidget

ORIENTATION = {
    "h": Gtk.Orientation.HORIZONTAL,
    "v": Gtk.Orientation.VERTICAL,
}

class Separator(Gtk.Separator, BaseWidget):
    """
    Bases: `Gtk.Separator <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Separator.html>`_, :class:`~lst.base_widget.BaseWidget`.
    
    A separator.

    Parameters:
        orientation (``str``, optional): Orientation of the widget. Possible values: ``"h"``, ``"v"``.

    .. code-block:: python
    
        Widget.Separator(
            orientation='h'
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, orientation: str = "h", **kwargs):
        Gtk.Separator.__init__(self, orientation=ORIENTATION[orientation])
        BaseWidget.__init__(self, **kwargs)

