from gi.repository import Gtk
from lst.widgets.widget import Widget

class FileChooserButton(Gtk.FileChooserButton, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(self, title: str = None, **kwargs):
        Gtk.FileChooserButton.__init__(self)
        Widget.__init__(self, **kwargs)
        self.title = title
