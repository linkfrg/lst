from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget


class Switch(Gtk.Switch, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        state: bool = False,
        on_activate: callable = None,
        on_deactivate: callable = None,
        **kwargs,
    ):
        Gtk.Switch.__init__(self)
        Widget.__init__(self, **kwargs)
        self._on_activate = None
        self._on_deactivate = None
        self.on_activate = on_activate
        self.on_deactivate = on_deactivate

        self.state = state
        self.connect("state-set", lambda *args: self.__callback())

    def __callback(self) -> None:
        if self.state:
            if self._on_deactivate:
                self._on_deactivate(self)
        else:
            if self._on_activate:
                self._on_activate(self)

    @GObject.Property
    def on_activate(self) -> callable:
        return self._on_activate

    @on_activate.setter
    def on_activate(self, value: callable) -> None:
        self._on_activate = value

    @GObject.Property
    def on_deactivate(self) -> callable:
        return self._on_deactivate

    @on_deactivate.setter
    def on_deactivate(self, value: callable) -> None:
        self._on_deactivate = value
