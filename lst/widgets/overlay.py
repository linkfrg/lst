from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget


class Overlay(Gtk.Overlay, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(self, child: list = None, **kwargs):
        Gtk.Overlay.__init__(self)
        Widget.__init__(self, **kwargs)

        self.child = child

    @GObject.Property
    def child(self) -> Gtk.Widget:
        if self.get_children() != []:
            return self.get_children()[0]

    @child.setter
    def child(self, child: Gtk.Widget) -> None:
        if self.get_children() != []:
            self.remove(self.get_children()[0])
        if child:
            self.add(child)
