from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget
from typing import List, Any

ORIENTATION = {
    "h": Gtk.Orientation.HORIZONTAL,
    "v": Gtk.Orientation.VERTICAL,
}

class Box(Gtk.Box, BaseWidget):
    """
    Bases: `Gtk.Box <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Box.html>`_, :class:`~lst.base_widget.BaseWidget`.

    The main layout widget.
    
    .. hint::
        You can use generators to set child.
        
        .. code-block::

            Widget.Box(
                child=[Widget.Label(i) for i in range(10)]
            )

    Parameters:
        child (``List[Gtk.Widget]``, optional): The list of child widgets.
        orientation (``str``, optional): Orientation of the widget. Possible values: ``"h"``, ``"v"``.

    .. code-block:: python
    
        Widget.Box(
            child=[Widget.Label(label='heh'), Widget.Label(label='heh2')],
            orientation='h',
            homogeneous=False,
            spacing=52
        )
    """


    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        child: List[Gtk.Widget] = None,
        orientation: str = "h",
        **kwargs
    ):
        Gtk.Box.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self.child = child
        self.orientation = orientation

    @GObject.Property
    def child(self) -> List[Gtk.Widget]:
        return self.get_children()

    @child.setter
    def child(self, child: list) -> None:
        for c in self.get_children():
            self.remove(c)
        if child:
            for c in child:
                if c:
                    self.add(c)

    def set_property(self, property_name: str, value: Any) -> None:
        if property_name == "orientation":
            super().set_property("orientation", ORIENTATION[value])
        else:
            super().set_property(property_name, value)
