from gi.repository import Gtk
from lst.widgets.widget import Widget
from typing import Any

JUSTIFY = {
    'left': Gtk.Justification.LEFT,
    'right': Gtk.Justification.RIGHT,
    'center': Gtk.Justification.CENTER,
    'fill': Gtk.Justification.FILL,
}

class Label(Gtk.Label, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(self, label: str = None, justify: str = 'left', use_markup: bool = False, **kwargs):
        Gtk.Label.__init__(self)
        Widget.__init__(self, **kwargs)
        self.label = label
        self.use_markup = use_markup
        self.justify = justify
    
    def set_property(self, property_name: str, value: Any) -> None:
        if property_name == "justify":
            super().set_property(property_name, JUSTIFY[value])
        else:
            super().set_property(property_name, value)