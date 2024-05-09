from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget

class MenuItem(Gtk.MenuItem, BaseWidget):
    """
    Bases: `Gtk.MenuItem <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/MenuItem.html>`_, :class:`~lst.base_widget.BaseWidget`.
    
    A container widget, the only valid children for menus.
    
    Parameters:
        child(``Gtk.Widget``, optional): Child widget.
        on_activate(``callable``, optional): The function to call when item is activated.
        on_select(``callable``, optional): The function to call when item is selected.
        on_deselect(``callable``, optional): The function to call when item is deselected.
    
    .. code-block:: python
    
        Widget.MenuItem(
            child=Widget.Label("click me"),
            on_activate=lambda self: print(self),
            on_select=lambda self: print(self),
            on_deselect=lambda self: print(self),
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        child: Gtk.Widget = None,
        on_activate: callable = None,
        on_select: callable = None,
        on_deselect: callable = None,
        **kwargs
    ):
        Gtk.MenuItem.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self._on_activate = None
        self._on_select = None
        self._on_deselect = None

        self.on_activate = on_activate
        self.on_select = on_select
        self.on_deselect = on_deselect

        self.child = child
        self.connect('activate', lambda *args: self.on_activate(self) if self.on_activate else None)
        self.connect('select', lambda *args: self.on_select(self) if self.on_select else None)
        self.connect('deselect', lambda *args: self.on_deselect(self) if self.on_deselect else None)

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
