from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget

TRANSITION_TYPE = {
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
        child: Gtk.Widget,
        reveal: bool = False,
        transition_duration=500,
        transition_type="none",
        **kwargs,
    ):
        Gtk.Revealer.__init__(self)
        Widget.__init__(self, **kwargs)

        self.set_reveal_child(reveal)
        self.set_transition_duration(transition_duration)
        self.set_transition_type(transition_type)

        self.set_child(child)

    @GObject.Property
    def child(self) -> list:
        return self.get_children()[0]

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

    def set_transition_type(self, value: str) -> None:
        super().set_transition_type(TRANSITION_TYPE[value])

    def toggle(self):
        if self.get_reveal_child():
            self.set_reveal_child(False)
        else:
            self.set_reveal_child(True)
