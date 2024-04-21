from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget
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


class Revealer(Gtk.Revealer, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        child: Gtk.Widget = None,
        reveal_child: bool = False,
        transition_duration: int = 500,
        transition_type: str = "none",
        **kwargs,
    ):
        Gtk.Revealer.__init__(self)
        Widget.__init__(self, **kwargs)

        self.reveal_child = reveal_child
        self.transition_duration = transition_duration
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
