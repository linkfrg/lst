from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget

ORIENTATION = {
    "h": Gtk.Orientation.HORIZONTAL,
    "v": Gtk.Orientation.VERTICAL,
}

class Box(Gtk.Box, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        child: list = None,
        orientation: str = "h",
        homogeneous: bool = False,
        spacing: int = 0,
        **kwargs
    ):
        Gtk.Box.__init__(self, orientation=ORIENTATION[orientation], homogeneous=homogeneous, spacing=spacing)
        Widget.__init__(self, **kwargs)

        self.set_child(child)

    @GObject.Property
    def child(self) -> list:
        return self.get_children()

    @child.setter
    def child(self, child: list) -> None:
        for c in self.get_children():
            self.remove(c)
        if child:
            for c in child:
                if c:
                    self.add(c)

    def set_child(self, child: list) -> None:
        self.child = child
