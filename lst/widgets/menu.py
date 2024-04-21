from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget
from typing import List


class Menu(Gtk.Menu, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        child: list = None,
        **kwargs
    ):
        Gtk.Menu.__init__(self)
        Widget.__init__(self, **kwargs)

        self.child = child

    @GObject.Property
    def child(self) -> List[Gtk.MenuItem]:
        return self.get_children()

    @child.setter
    def child(self, child: List[Gtk.MenuItem]) -> None:
        for c in self.get_children():
            self.remove(c)
        if child:
            for c in child:
                if c:
                    self.add(c)
