from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget

class Scroll(Gtk.ScrolledWindow, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(self, child: Gtk.Widget = None, **kwargs):
        
        Gtk.ScrolledWindow.__init__(self)
        Widget.__init__(self, **kwargs)

        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.set_child(child)

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
