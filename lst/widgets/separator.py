from gi.repository import Gtk
from lst.widgets.widget import Widget

class Separator(Gtk.Separator, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(self, **kwargs):
        Gtk.Separator.__init__(self)
        Widget.__init__(self, **kwargs)

