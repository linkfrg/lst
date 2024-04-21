from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget


class MenuItem(Gtk.MenuItem, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        on_activate: callable = None,
        on_select: callable = None,
        on_deselect: callable = None,
        child: list = None,
        **kwargs
    ):
        Gtk.MenuItem.__init__(self)
        Widget.__init__(self, **kwargs)

        self._on_activate = None
        self._on_select = None
        self._on_deselect = None

        self.on_activate = on_activate
        self.on_select = on_select
        self.on_deselect = on_deselect

        self.child = child
        self.connect('activate', lambda *args: self.on_activate() if self.on_activate else None)
        self.connect('select', lambda *args: self.on_select() if self.on_select else None)
        self.connect('deselect', lambda *args: self.on_deselect() if self.on_deselect else None)

    @GObject.Property
    def on_activate(self) -> callable:
        return self._on_activate
    
    @on_activate.setter
    def on_activate(self, value: callable) -> None:
        self._on_activate = value

    @GObject.Property
    def on_select(self) -> callable:
        return self._on_select
    
    @on_select.setter
    def on_select(self, value: callable) -> None:
        self._on_select = value

    @GObject.Property
    def on_deselect(self) -> callable:
        return self._on_deselect
    
    @on_deselect.setter
    def on_deselect(self, value: callable) -> None:
        self._on_deselect = value

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
