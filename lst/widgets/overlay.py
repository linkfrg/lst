from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget

class Overlay(Gtk.Overlay, Widget):
    __gproperties__ = {**Widget.gproperties}
    
    def __init__(self, child: list, **kwargs):
        
        Gtk.Overlay.__init__(self)
        Widget.__init__(self, **kwargs)

        self.set_child(child)

    @GObject.Property
    def child(self) -> list:
        return self.get_children()

    @child.setter
    def child(self, child: Gtk.Widget) -> None:
        if child:
            if self.get_children() != []:
                self.remove(self.get_children()[0])
            self.add(child)
            self.show()
            self._child = child

    def set_child(self, child: list) -> None:
        self.child = child
