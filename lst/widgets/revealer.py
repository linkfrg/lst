from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget
from typing import Any


TRANSITION_TYPE = {
    None: Gtk.RevealerTransitionType.NONE,
    "none": Gtk.RevealerTransitionType.NONE,
    "crossfade": Gtk.RevealerTransitionType.CROSSFADE,
    "slideright": Gtk.RevealerTransitionType.SLIDE_RIGHT,
    "slideleft": Gtk.RevealerTransitionType.SLIDE_LEFT,
    "slideup": Gtk.RevealerTransitionType.SLIDE_UP,
    "slidedown": Gtk.RevealerTransitionType.SLIDE_DOWN,
}


class Revealer(Gtk.Revealer, BaseWidget):
    """
    Bases: `Gtk.Revealer <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Revealer.html>`_, :class:`~lst.base_widget.BaseWidget`.
    
    A container which animates the transition of its child from invisible to visible.

    Parameters:
        child(``Gtk.Widget``, optional): Child widget.
        transition_type(``str``, optional): Transition type. 
        Possible values: ``"none"``, ``"crossfade"``, ``"slideright"``, ``"slideleft"``, ``"slideup"``, ``"slidedown"``.
    
    .. code-block:: python
    
        Widget.Revealer(
            child=Widget.Label('animation!!!'),
            transition_type='slideright',
            transition_duration=500,
            reveal_child=True, # Whether child is revealed.
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        child: Gtk.Widget = None,
        transition_type: str = "none",
        **kwargs,
    ):
        Gtk.Revealer.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self.transition_type = transition_type
        self.child = child

    @GObject.Property
    def child(self) -> list:
        if self.get_children() != []:
            return self.get_children()[0]

    @child.setter
    def child(self, child: Gtk.Widget) -> None:
        if self.get_children() != []:
            self.remove(self.get_children()[0])
        if child:
            self.add(child)

    def set_property(self, name: str, value: Any) -> None:
        if name == "transition_type":
            super().set_property(name, TRANSITION_TYPE[value])
        else:
            super().set_property(name, value)

    def toggle(self):
        if self.get_reveal_child():
            self.set_reveal_child(False)
        else:
            self.set_reveal_child(True)
