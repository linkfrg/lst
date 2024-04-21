from gi.repository import Gtk
from lst.widgets.widget import Widget

ORIENTATION = {
    "h": Gtk.Orientation.HORIZONTAL,
    "v": Gtk.Orientation.VERTICAL,
}

class Separator(Gtk.Separator, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(self, orientation: str = "h", **kwargs):
        Gtk.Separator.__init__(self, orientation=ORIENTATION[orientation])
        Widget.__init__(self, **kwargs)

