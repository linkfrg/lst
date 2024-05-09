from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget


class Overlay(Gtk.Overlay, BaseWidget):
    """
    Bases: `Gtk.Overlay <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Overlay.html>`_, :class:`~lst.base_widget.BaseWidget`.

    A container that places its children on top of each other. 
    
    Parameters:
        child(``Gtk.Widget``, optional): Child widget.
    
    .. code-block:: python
    
        Widget.Overlay(
            child=Widget.Box(
                child=[
                    Widget.Label(label=1),
                    Widget.Label(label=2),
                    Widget.Label(label=3),
                ]
            )
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, child: Gtk.Widget = None, **kwargs):
        Gtk.Overlay.__init__(self)
        BaseWidget.__init__(self, **kwargs)

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
