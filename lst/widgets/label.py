from gi.repository import Gtk
from lst.widgets.widget import Widget


class Label(Gtk.Label, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(self, label: str = None, use_markup: bool = False, **kwargs):
        Gtk.Label.__init__(self)
        Widget.__init__(self, **kwargs)
        self.set_label(label)
        self.set_use_markup(use_markup)

    def set_label(self, value: str) -> None:
        self.set_property('label', value)

    def set_use_markup(self, value: bool) -> None:
        self.set_property('use_markup', value)
