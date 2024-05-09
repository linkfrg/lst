from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget

class Scroll(Gtk.ScrolledWindow, BaseWidget):
    """
    Bases: `Gtk.ScrolledWindow <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/ScrolledWindow.html>`_, :class:`~lst.base_widget.BaseWidget`.
    
    A container that accepts a single child widget and makes that child scrollable.

    Parameters:
        child(``Gtk.Widget``, optional): Child widget.
    
    .. code-block:: python

        Widget.Scroll(
            child=Widget.Box(
                orientation="v",
                child=[Widget.Label(i) for i in range(30)]
            )
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, child: Gtk.Widget = None, **kwargs):
        
        Gtk.ScrolledWindow.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

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
