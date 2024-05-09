from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget
from typing import List


class Menu(Gtk.Menu, BaseWidget):
    """
    Subclass of `Gtk.Menu <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Menu.html>`_
    
    A drop down menu consisting of a list of :class:`~lst.widgets.Widget.MenuItem`.

    Parameters:
        child(``List[Gtk.MenuItem]``, optional): A list of :class:`~lst.widgets.Widget.MenuItem`.

    .. code-block:: python

        Widget.Menu(
            child=[
                Widget.Menuitem(child=Widget.Label("Entry 1")),
                Widget.Menuitem(child=Widget.Label("Entry 2")),
            ]
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        child: List[Gtk.MenuItem] = None,
        **kwargs
    ):
        Gtk.Menu.__init__(self)
        BaseWidget.__init__(self, **kwargs)

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
